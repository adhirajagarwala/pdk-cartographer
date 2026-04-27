"""Handwritten parser for the tiny M1 Liberty fixture subset.

This is not a complete Liberty parser. It is intentionally scoped to the small
synthetic fixtures in this repository so M1 can teach the shape of Liberty
metadata without downloading or copying Sky130 files.

Supported in M1:
- group syntax such as library(...), cell(...), pin(...), and timing()
- scalar attributes using ``name : value;``
- library names, cell names, cell area, pin attributes, and minimal timing arcs

Not supported in M1:
- lookup table parsing or numerical timing table interpretation
- conditional timing expressions, bus syntax, escaped identifiers, or includes
- full Liberty grammar compatibility
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from pdk_cartographer.liberty.models import Cell, Library, Pin, TimingArc


class LibertyParseError(ValueError):
    """Raised when fixture Liberty text cannot be parsed."""


@dataclass(frozen=True)
class _Group:
    kind: str
    name: str | None = None
    attrs: dict[str, str] = field(default_factory=dict)
    children: tuple[_Group, ...] = field(default_factory=tuple)


_TOKEN_RE = re.compile(
    r'"(?:\\.|[^"\\])*"'
    r"|[A-Za-z_][A-Za-z0-9_.$-]*"
    r"|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"
    r"|[{}():;,]"
)

_COMMENT_RE = re.compile(r"/\*.*?\*/|//[^\n]*", re.DOTALL)


def parse_liberty_file(path: str | Path) -> Library:
    """Parse a small Liberty fixture file."""

    return parse_liberty(Path(path).read_text(encoding="utf-8"))


def parse_liberty(text: str) -> Library:
    """Parse Liberty fixture text into a :class:`Library`."""

    tokens = _tokenize(text)
    groups = _TokenParser(tokens).parse_groups()
    libraries = [group for group in groups if group.kind == "library"]
    if len(libraries) != 1:
        raise LibertyParseError("expected exactly one library group")
    return _build_library(libraries[0])


def _tokenize(text: str) -> list[str]:
    stripped = _COMMENT_RE.sub("", text)
    tokens = _TOKEN_RE.findall(stripped)
    if not tokens:
        raise LibertyParseError("no Liberty tokens found")
    return tokens


class _TokenParser:
    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens
        self._pos = 0

    def parse_groups(self) -> tuple[_Group, ...]:
        groups: list[_Group] = []
        while not self._at_end():
            if self._peek() == "}":
                break
            groups.append(self._parse_group())
        return tuple(groups)

    def _parse_group(self) -> _Group:
        kind = self._consume_identifier()
        name = self._parse_group_name()
        self._consume("{")

        attrs: dict[str, str] = {}
        children: list[_Group] = []
        while self._peek() != "}":
            key = self._consume_identifier()
            next_token = self._peek()
            if next_token == ":":
                self._consume(":")
                attrs[key] = self._parse_attr_value()
            elif next_token == "(":
                children.append(self._parse_child_group(key))
            else:
                raise LibertyParseError(
                    f"expected ':' or '(' after {key!r}, got {next_token!r}"
                )

        self._consume("}")
        if not self._at_end() and self._peek() == ";":
            self._consume(";")
        return _Group(kind=kind, name=name, attrs=attrs, children=tuple(children))

    def _parse_child_group(self, kind: str) -> _Group:
        name = self._parse_group_name()
        self._consume("{")

        attrs: dict[str, str] = {}
        children: list[_Group] = []
        while self._peek() != "}":
            key = self._consume_identifier()
            next_token = self._peek()
            if next_token == ":":
                self._consume(":")
                attrs[key] = self._parse_attr_value()
            elif next_token == "(":
                children.append(self._parse_child_group(key))
            else:
                raise LibertyParseError(
                    f"expected ':' or '(' after {key!r}, got {next_token!r}"
                )

        self._consume("}")
        if not self._at_end() and self._peek() == ";":
            self._consume(";")
        return _Group(kind=kind, name=name, attrs=attrs, children=tuple(children))

    def _parse_group_name(self) -> str | None:
        self._consume("(")
        values: list[str] = []
        while self._peek() != ")":
            token = self._advance()
            if token != ",":
                values.append(token)
        self._consume(")")
        if not values:
            return None
        return _clean_value(values[0])

    def _parse_attr_value(self) -> str:
        values: list[str] = []
        while self._peek() != ";":
            values.append(self._advance())
        self._consume(";")
        if not values:
            raise LibertyParseError("empty attribute value")
        return " ".join(_clean_value(value) for value in values)

    def _consume_identifier(self) -> str:
        token = self._advance()
        if token in {"{", "}", "(", ")", ":", ";", ","}:
            raise LibertyParseError(f"expected identifier, got {token!r}")
        return token

    def _consume(self, expected: str) -> None:
        token = self._advance()
        if token != expected:
            raise LibertyParseError(f"expected {expected!r}, got {token!r}")

    def _advance(self) -> str:
        if self._at_end():
            raise LibertyParseError("unexpected end of Liberty text")
        token = self._tokens[self._pos]
        self._pos += 1
        return token

    def _peek(self) -> str:
        if self._at_end():
            raise LibertyParseError("unexpected end of Liberty text")
        return self._tokens[self._pos]

    def _at_end(self) -> bool:
        return self._pos >= len(self._tokens)


def _build_library(group: _Group) -> Library:
    if group.name is None:
        raise LibertyParseError("library group is missing a name")
    cells = tuple(
        _build_cell(child) for child in group.children if child.kind == "cell"
    )
    return Library(name=group.name, cells=cells)


def _build_cell(group: _Group) -> Cell:
    if group.name is None:
        raise LibertyParseError("cell group is missing a name")
    pins = tuple(_build_pin(child) for child in group.children if child.kind == "pin")
    return Cell(
        name=group.name,
        area=_optional_float(group.attrs.get("area")),
        pins=pins,
    )


def _build_pin(group: _Group) -> Pin:
    if group.name is None:
        raise LibertyParseError("pin group is missing a name")
    timing_arcs = tuple(
        _build_timing_arc(child) for child in group.children if child.kind == "timing"
    )
    return Pin(
        name=group.name,
        direction=group.attrs.get("direction"),
        function=group.attrs.get("function"),
        capacitance=_optional_float(group.attrs.get("capacitance")),
        timing_arcs=timing_arcs,
    )


def _build_timing_arc(group: _Group) -> TimingArc:
    return TimingArc(
        related_pin=group.attrs.get("related_pin"),
        timing_sense=group.attrs.get("timing_sense"),
        timing_type=group.attrs.get("timing_type"),
    )


def _optional_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError as exc:
        raise LibertyParseError(f"expected numeric value, got {value!r}") from exc


def _clean_value(value: str) -> str:
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1].replace(r"\"", '"')
    return value
