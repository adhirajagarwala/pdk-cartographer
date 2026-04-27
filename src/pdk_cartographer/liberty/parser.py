"""Public parser API for the synthetic Liberty fixture subset.

This is not a complete Liberty parser. It is intentionally scoped to the small
synthetic fixtures in this repository so pdk-cartographer can teach the shape
of Liberty metadata without downloading or copying Sky130 files.

Supported subset:
- group syntax such as ``library(...) { ... }``, ``cell(...)``, ``pin(...)``,
  and minimal ``timing()`` groups
- scalar attributes using ``name : value;``
- simple comma-separated attribute values for fixture-oriented metadata
- line comments using ``//`` and block comments using ``/* ... */``
- library names, cell names, cell area, pin attributes, and minimal timing arcs

The generic parser builds a small group/attribute tree first, then the public
``parse_liberty_text`` and ``parse_liberty_file`` helpers convert that tree into
typed model dataclasses suitable for later Standard Cell Atlas work.

Not supported in M2:
- timing lookup table parsing or numerical timing table interpretation
- conditional timing expressions, bus syntax, escaped identifiers, or includes
- full Liberty grammar compatibility
"""

from __future__ import annotations

from pathlib import Path
from typing import NoReturn

from pdk_cartographer.liberty.ast import (
    LibertyAttribute,
    LibertyGroup,
    LibertyScalar,
    LibertyValue,
    SourceLocation,
)
from pdk_cartographer.liberty.diagnostics import LibertyDiagnostic, LibertyParseError
from pdk_cartographer.liberty.lexer import Token, TokenKind, tokenize
from pdk_cartographer.liberty.models import Cell, Library, Pin, TimingArc


def parse_liberty_file(path: str | Path) -> Library:
    """Parse a small Liberty fixture file."""

    return parse_liberty_text(Path(path).read_text(encoding="utf-8"))


def parse_liberty_text(text: str) -> Library:
    """Parse Liberty fixture text into a :class:`Library`."""

    groups = parse_liberty_groups(text)
    libraries = [group for group in groups if group.name == "library"]
    if len(libraries) != 1:
        raise LibertyParseError("expected exactly one library group")
    return _build_library(libraries[0])


def parse_liberty(text: str) -> Library:
    """Compatibility alias for :func:`parse_liberty_text`."""

    return parse_liberty_text(text)


def parse_liberty_groups(text: str) -> tuple[LibertyGroup, ...]:
    """Parse Liberty fixture text into generic group/attribute AST nodes."""

    tokens = tokenize(text)
    return _TokenParser(tokens).parse_groups()


class _TokenParser:
    def __init__(self, tokens: tuple[Token, ...]) -> None:
        self._tokens = tokens
        self._pos = 0

    def parse_groups(self) -> tuple[LibertyGroup, ...]:
        groups: list[LibertyGroup] = []
        if self._peek().kind == TokenKind.EOF:
            raise LibertyParseError(LibertyDiagnostic("no Liberty tokens found"))
        while self._peek().kind != TokenKind.EOF:
            if self._peek().kind == TokenKind.RBRACE:
                break
            groups.append(self._parse_group())
        return tuple(groups)

    def _parse_group(self) -> LibertyGroup:
        kind = self._consume_identifier()
        args = self._parse_group_args()
        self._consume(TokenKind.LBRACE)

        attrs: dict[str, LibertyAttribute] = {}
        children: list[LibertyGroup] = []
        while self._peek().kind != TokenKind.RBRACE:
            key = self._consume_identifier()
            next_token = self._peek()
            if next_token.kind == TokenKind.COLON:
                attrs[key.value] = self._parse_attribute(key)
            elif next_token.kind == TokenKind.LPAREN:
                children.append(self._parse_child_group(key))
            else:
                self._raise_expected("':' or '('", next_token)

        self._consume(TokenKind.RBRACE)
        if self._peek().kind == TokenKind.SEMICOLON:
            self._consume(TokenKind.SEMICOLON)
        return LibertyGroup(
            name=kind.value,
            args=args,
            attributes=attrs,
            groups=tuple(children),
            location=_location(kind),
        )

    def _parse_child_group(self, kind: Token) -> LibertyGroup:
        args = self._parse_group_args()
        self._consume(TokenKind.LBRACE)

        attrs: dict[str, LibertyAttribute] = {}
        children: list[LibertyGroup] = []
        while self._peek().kind != TokenKind.RBRACE:
            key = self._consume_identifier()
            next_token = self._peek()
            if next_token.kind == TokenKind.COLON:
                attrs[key.value] = self._parse_attribute(key)
            elif next_token.kind == TokenKind.LPAREN:
                children.append(self._parse_child_group(key))
            else:
                self._raise_expected("':' or '('", next_token)

        self._consume(TokenKind.RBRACE)
        if self._peek().kind == TokenKind.SEMICOLON:
            self._consume(TokenKind.SEMICOLON)
        return LibertyGroup(
            name=kind.value,
            args=args,
            attributes=attrs,
            groups=tuple(children),
            location=_location(kind),
        )

    def _parse_group_args(self) -> tuple[LibertyValue, ...]:
        self._consume(TokenKind.LPAREN)
        values: list[LibertyValue] = []
        while self._peek().kind != TokenKind.RPAREN:
            values.append(self._parse_value())
            if self._peek().kind == TokenKind.COMMA:
                self._consume(TokenKind.COMMA)
            elif self._peek().kind != TokenKind.RPAREN:
                self._raise_expected("',' or ')'", self._peek())
        self._consume(TokenKind.RPAREN)
        return tuple(values)

    def _parse_attribute(self, name: Token) -> LibertyAttribute:
        self._consume(TokenKind.COLON)
        values: list[LibertyScalar] = []
        while self._peek().kind != TokenKind.SEMICOLON:
            values.append(self._parse_scalar_value())
            if self._peek().kind == TokenKind.COMMA:
                self._consume(TokenKind.COMMA)
            elif self._peek().kind != TokenKind.SEMICOLON:
                self._raise_expected("',' or ';'", self._peek())
        self._consume(TokenKind.SEMICOLON)
        if not values:
            raise LibertyParseError(
                LibertyDiagnostic(
                    f"empty attribute value for {name.value!r}",
                    line=name.line,
                    column=name.column,
                )
            )
        value: LibertyValue = values[0] if len(values) == 1 else tuple(values)
        return LibertyAttribute(name=name.value, value=value, location=_location(name))

    def _parse_value(self) -> LibertyValue:
        return self._parse_scalar_value()

    def _parse_scalar_value(self) -> LibertyScalar:
        token = self._advance()
        if token.kind == TokenKind.IDENTIFIER or token.kind == TokenKind.STRING:
            return token.value
        if token.kind == TokenKind.NUMBER:
            return _number_value(token)
        self._raise_expected("identifier, string, or number", token)

    def _consume_identifier(self) -> Token:
        token = self._advance()
        if token.kind != TokenKind.IDENTIFIER:
            self._raise_expected("identifier", token)
        return token

    def _consume(self, expected: TokenKind) -> None:
        token = self._advance()
        if token.kind != expected:
            self._raise_expected(expected.value, token)

    def _advance(self) -> Token:
        token = self._tokens[self._pos]
        if token.kind == TokenKind.EOF:
            raise LibertyParseError(
                LibertyDiagnostic(
                    "unexpected end of Liberty text",
                    line=token.line,
                    column=token.column,
                )
            )
        self._pos += 1
        return token

    def _peek(self) -> Token:
        return self._tokens[self._pos]

    def _raise_expected(self, expected: str, token: Token) -> NoReturn:
        raise LibertyParseError(
            LibertyDiagnostic(
                f"expected {expected}, got {token.value!r}",
                line=token.line,
                column=token.column,
            )
        )


def _build_library(group: LibertyGroup) -> Library:
    name = group.first_arg_as_string()
    if name is None:
        raise LibertyParseError(
            _group_diagnostic(group, "library group is missing a name")
        )
    cells = {
        cell.name: cell
        for cell in (_build_cell(child) for child in group.child_groups("cell"))
    }
    return Library(name=name, cells=cells, attributes=_attributes(group))


def _build_cell(group: LibertyGroup) -> Cell:
    name = group.first_arg_as_string()
    if name is None:
        raise LibertyParseError(
            _group_diagnostic(group, "cell group is missing a name")
        )
    pins = {
        pin.name: pin
        for pin in (_build_pin(child) for child in group.child_groups("pin"))
    }
    return Cell(
        name=name,
        area=_optional_float(_attr_value(group, "area")),
        pins=pins,
        attributes=_attributes(group),
    )


def _build_pin(group: LibertyGroup) -> Pin:
    name = group.first_arg_as_string()
    if name is None:
        raise LibertyParseError(_group_diagnostic(group, "pin group is missing a name"))
    timing_arcs = [_build_timing_arc(child) for child in group.child_groups("timing")]
    return Pin(
        name=name,
        direction=_optional_string(_attr_value(group, "direction")),
        function=_optional_string(_attr_value(group, "function")),
        capacitance=_optional_float(_attr_value(group, "capacitance")),
        attributes=_attributes(group),
        timing_arcs=timing_arcs,
    )


def _build_timing_arc(group: LibertyGroup) -> TimingArc:
    return TimingArc(
        related_pin=_optional_string(_attr_value(group, "related_pin")),
        timing_sense=_optional_string(_attr_value(group, "timing_sense")),
        timing_type=_optional_string(_attr_value(group, "timing_type")),
        attributes=_attributes(group),
    )


def _attributes(group: LibertyGroup) -> dict[str, LibertyValue]:
    return {
        name: attribute.value
        for name, attribute in group.attributes.items()
    }


def _attr_value(group: LibertyGroup, name: str) -> LibertyValue | None:
    attribute = group.attributes.get(name)
    if attribute is None:
        return None
    return attribute.value


def _optional_float(value: LibertyValue | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, tuple):
        raise LibertyParseError(f"expected numeric value, got list {value!r}")
    try:
        return float(value)
    except ValueError as exc:
        raise LibertyParseError(f"expected numeric value, got {value!r}") from exc


def _optional_string(value: LibertyValue | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, tuple):
        raise LibertyParseError(f"expected scalar value, got list {value!r}")
    return str(value)


def _number_value(token: Token) -> float:
    try:
        return float(token.value)
    except ValueError as exc:
        raise LibertyParseError(
            LibertyDiagnostic(
                f"expected numeric value, got {token.value!r}",
                line=token.line,
                column=token.column,
            )
        ) from exc


def _location(token: Token) -> SourceLocation:
    return SourceLocation(line=token.line, column=token.column)


def _group_diagnostic(group: LibertyGroup, message: str) -> LibertyDiagnostic:
    if group.location is None:
        return LibertyDiagnostic(message)
    return LibertyDiagnostic(
        message,
        line=group.location.line,
        column=group.location.column,
    )
