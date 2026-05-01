"""Public parser API for the synthetic Liberty fixture subset.

This is not a complete Liberty parser. It is intentionally scoped to the small
synthetic fixtures in this repository so pdk-cartographer can teach the shape
of Liberty metadata without downloading or copying Sky130 files.

Supported subset:
- group syntax such as ``library(...) { ... }``, ``cell(...)``, ``pin(...)``,
  and minimal ``timing()`` groups
- scalar attributes using ``name : value;``
- complex attributes using ``name(value, ...);`` for fixture timing tables
- simple comma-separated attribute values for fixture-oriented metadata
- line comments using ``//`` and block comments using ``/* ... */``
- library names, cell names, cell area, pin attributes, and minimal timing arcs

The generic parser builds a small group/attribute tree first, then the public
``parse_liberty_text`` and ``parse_liberty_file`` helpers convert that tree into
typed model dataclasses suitable for later Standard Cell Atlas work.

Still intentionally unsupported:
- full Liberty timing-table semantics or numerical timing analysis
- production lookup table parsing beyond the small M4 fixture subset
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
from pdk_cartographer.liberty.models import (
    Cell,
    Library,
    LookupTableTemplate,
    Pin,
    TimingArc,
    TimingTable,
)

TIMING_TABLE_GROUP_NAMES = {
    "cell_rise",
    "cell_fall",
    "rise_transition",
    "fall_transition",
}


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
                attrs[key.value] = self._parse_scalar_attribute(key)
            elif next_token.kind == TokenKind.LPAREN:
                item = self._parse_complex_attribute_or_child_group(key)
                if isinstance(item, LibertyAttribute):
                    attrs[item.name] = item
                else:
                    children.append(item)
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

    def _parse_group_args(self) -> tuple[LibertyScalar, ...]:
        self._consume(TokenKind.LPAREN)
        values: list[LibertyScalar] = []
        while self._peek().kind != TokenKind.RPAREN:
            values.append(self._parse_value())
            if self._peek().kind == TokenKind.COMMA:
                self._consume(TokenKind.COMMA)
            elif self._peek().kind != TokenKind.RPAREN:
                self._raise_expected("',' or ')'", self._peek())
        self._consume(TokenKind.RPAREN)
        return tuple(values)

    def _parse_complex_attribute_or_child_group(
        self, kind: Token
    ) -> LibertyAttribute | LibertyGroup:
        args = self._parse_group_args()
        if self._peek().kind == TokenKind.SEMICOLON:
            self._consume(TokenKind.SEMICOLON)
            if not args:
                raise LibertyParseError(
                    LibertyDiagnostic(
                        f"empty complex attribute value for {kind.value!r}",
                        line=kind.line,
                        column=kind.column,
                    )
                )
            value: LibertyValue = args[0] if len(args) == 1 else args
            return LibertyAttribute(
                name=kind.value,
                value=value,
                location=_location(kind),
            )
        if self._peek().kind == TokenKind.LBRACE:
            return self._parse_child_group_body(kind, args)
        self._raise_expected("';' or '{'", self._peek())

    def _parse_child_group(self, kind: Token) -> LibertyGroup:
        args = self._parse_group_args()
        return self._parse_child_group_body(kind, args)

    def _parse_child_group_body(
        self,
        kind: Token,
        args: tuple[LibertyScalar, ...],
    ) -> LibertyGroup:
        self._consume(TokenKind.LBRACE)

        attrs: dict[str, LibertyAttribute] = {}
        children: list[LibertyGroup] = []
        while self._peek().kind != TokenKind.RBRACE:
            key = self._consume_identifier()
            next_token = self._peek()
            if next_token.kind == TokenKind.COLON:
                attrs[key.value] = self._parse_scalar_attribute(key)
            elif next_token.kind == TokenKind.LPAREN:
                item = self._parse_complex_attribute_or_child_group(key)
                if isinstance(item, LibertyAttribute):
                    attrs[item.name] = item
                else:
                    children.append(item)
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

    def _parse_scalar_attribute(self, name: Token) -> LibertyAttribute:
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

    def _parse_value(self) -> LibertyScalar:
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
    lookup_table_templates = {
        template.name: template
        for template in (
            _build_lookup_table_template(child)
            for child in group.child_groups("lu_table_template")
        )
    }
    cells = {
        cell.name: cell
        for cell in (
            _build_cell(child, lookup_table_templates)
            for child in group.child_groups("cell")
        )
    }
    return Library(
        name=name,
        cells=cells,
        attributes=_attributes(group),
        lookup_table_templates=lookup_table_templates,
    )


def _build_cell(
    group: LibertyGroup,
    lookup_table_templates: dict[str, LookupTableTemplate],
) -> Cell:
    name = group.first_arg_as_string()
    if name is None:
        raise LibertyParseError(
            _group_diagnostic(group, "cell group is missing a name")
        )
    pins = {
        pin.name: pin
        for pin in (
            _build_pin(child, lookup_table_templates)
            for child in group.child_groups("pin")
        )
    }
    return Cell(
        name=name,
        area=_optional_float(_attr_value(group, "area")),
        pins=pins,
        attributes=_attributes(group),
    )


def _build_pin(
    group: LibertyGroup,
    lookup_table_templates: dict[str, LookupTableTemplate],
) -> Pin:
    name = group.first_arg_as_string()
    if name is None:
        raise LibertyParseError(_group_diagnostic(group, "pin group is missing a name"))
    timing_arcs = [
        _build_timing_arc(child, lookup_table_templates)
        for child in group.child_groups("timing")
    ]
    return Pin(
        name=name,
        direction=_optional_string(_attr_value(group, "direction")),
        function=_optional_string(_attr_value(group, "function")),
        capacitance=_optional_float(_attr_value(group, "capacitance")),
        attributes=_attributes(group),
        timing_arcs=timing_arcs,
    )


def _build_timing_arc(
    group: LibertyGroup,
    lookup_table_templates: dict[str, LookupTableTemplate],
) -> TimingArc:
    return TimingArc(
        related_pin=_optional_string(_attr_value(group, "related_pin")),
        timing_sense=_optional_string(_attr_value(group, "timing_sense")),
        timing_type=_optional_string(_attr_value(group, "timing_type")),
        attributes=_attributes(group),
        timing_tables=tuple(
            _build_timing_table(child, lookup_table_templates)
            for child in group.groups
            if child.name in TIMING_TABLE_GROUP_NAMES
        ),
    )


def _build_lookup_table_template(group: LibertyGroup) -> LookupTableTemplate:
    name = group.first_arg_as_string()
    if name is None:
        raise LibertyParseError(
            _group_diagnostic(group, "lu_table_template group is missing a name")
        )
    return LookupTableTemplate(
        name=name,
        variable_1=_optional_string(_attr_value(group, "variable_1")),
        variable_2=_optional_string(_attr_value(group, "variable_2")),
        index_1=_number_tuple(_attr_value(group, "index_1"), "index_1"),
        index_2=_number_tuple(_attr_value(group, "index_2"), "index_2"),
    )


def _build_timing_table(
    group: LibertyGroup,
    lookup_table_templates: dict[str, LookupTableTemplate],
) -> TimingTable:
    template_name = group.first_arg_as_string()
    template = (
        lookup_table_templates.get(template_name)
        if template_name is not None
        else None
    )
    index_1 = _number_tuple(_attr_value(group, "index_1"), "index_1")
    index_2 = _number_tuple(_attr_value(group, "index_2"), "index_2")
    if template is not None:
        index_1 = index_1 or template.index_1
        index_2 = index_2 or template.index_2
    values = _number_matrix(_attr_value(group, "values"), "values")
    _validate_timing_table_dimensions(group, index_1, index_2, values)
    return TimingTable(
        table_kind=group.name,
        template_name=template_name,
        index_1=index_1,
        index_2=index_2,
        values=values,
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


def _number_tuple(value: LibertyValue | None, label: str) -> tuple[float, ...]:
    if value is None:
        return ()
    numbers: list[float] = []
    values = value if isinstance(value, tuple) else (value,)
    for item in values:
        if isinstance(item, float):
            numbers.append(item)
        else:
            numbers.extend(_parse_number_list(item, label))
    return tuple(numbers)


def _number_matrix(
    value: LibertyValue | None,
    label: str,
) -> tuple[tuple[float, ...], ...]:
    if value is None:
        return ()
    rows: list[tuple[float, ...]] = []
    values = value if isinstance(value, tuple) else (value,)
    for item in values:
        if isinstance(item, float):
            rows.append((item,))
            continue
        for row in item.split(";"):
            if row.strip():
                rows.append(tuple(_parse_number_list(row, label)))
    return tuple(rows)


def _parse_number_list(value: str, label: str) -> tuple[float, ...]:
    numbers: list[float] = []
    for raw_part in value.split(","):
        part = raw_part.strip()
        if not part:
            continue
        try:
            numbers.append(float(part))
        except ValueError as exc:
            raise LibertyParseError(
                f"expected numeric {label} value, got {part!r}"
            ) from exc
    return tuple(numbers)


def _validate_timing_table_dimensions(
    group: LibertyGroup,
    index_1: tuple[float, ...],
    index_2: tuple[float, ...],
    values: tuple[tuple[float, ...], ...],
) -> None:
    if not values:
        return
    if index_1 and len(values) != len(index_1):
        raise LibertyParseError(
            _group_diagnostic(
                group,
                f"{group.name} values row count {len(values)} does not match "
                f"index_1 length {len(index_1)}",
            )
        )
    if index_2:
        for row_number, row in enumerate(values, start=1):
            if len(row) != len(index_2):
                raise LibertyParseError(
                    _group_diagnostic(
                        group,
                        f"{group.name} values row {row_number} length {len(row)} "
                        f"does not match index_2 length {len(index_2)}",
                    )
                )


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
