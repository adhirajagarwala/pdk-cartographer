# M2 Liberty Parser Core Report

## Objective

M2 builds a small Liberty parser core for `pdk-cartographer`. The milestone
strengthens the M1 fixture parser into a layered implementation with a lexer,
generic group parser, typed model extraction, diagnostics, expanded fixtures,
and focused tests.

This is not a real Sky130 analysis report. No Sky130 Liberty files were
downloaded, copied, or ingested. The parser is not a full Liberty parser.

## Starting Point From M1

M1 established the repository structure, Python package layout, quality gates,
synthetic Liberty fixtures, and a minimal parser. That parser could read tiny
fixture files and extract library, cell, pin, area, and minimal timing arc
metadata.

M2 keeps that foundation but replaces the one-piece parser shape with a cleaner
architecture that is easier to test and easier to explain in a portfolio
review.

## Parser Architecture

The lexer converts text into positioned tokens. It recognizes identifiers,
quoted strings, numbers, punctuation, line comments, block comments, and EOF.
Line and column tracking make malformed fixture input easier to debug.

The generic parser builds a `LibertyGroup` and `LibertyAttribute` tree. This
matches Liberty's nested structure without immediately committing to a specific
standard-cell model. The same generic machinery can represent `library`, `cell`,
`pin`, and `timing` groups.

Typed extraction then converts the generic tree into `Library`, `Cell`, `Pin`,
and `TimingArc` dataclasses. These models are deliberately small and oriented
toward later atlas generation.

## Fixture Suite

M2 keeps the original M1 fixtures:

- `tiny_combinational.lib`
- `tiny_sequential.lib`

M2 adds three synthetic fixtures:

- `multi_cell_combinational.lib` covers several generic combinational cells,
  areas, pins, capacitances, and output functions.
- `timing_arcs.lib` covers minimal timing groups under an output pin with
  `related_pin`, `timing_sense`, and `timing_type`.
- `parser_edge_cases.lib` covers comments, whitespace, quoted strings, numeric
  attributes, nested groups, and preserved custom attributes.

Every fixture is synthetic educational data and is marked as not copied from
Sky130 or any real PDK.

## Extracted Data Model

The M2 typed model extracts:

- library name
- simple library attributes
- multiple cells by name
- cell area
- simple cell attributes
- pins by name
- pin direction
- pin function
- pin capacitance
- simple pin attributes
- timing arcs attached to the pin where their `timing()` group appears
- `related_pin`, `timing_sense`, `timing_type`, and simple timing attributes

Cells and pins use dictionaries for direct lookup. Timing arcs use lists because
a pin can have multiple arcs with different related pins or timing meanings.

## Tests and Quality Gates

M2 expands tests across four areas:

- lexer behavior
- parser and generic group-tree behavior
- typed model behavior
- diagnostics behavior

The current validation gate is:

```bash
python -m pytest
ruff check .
mypy src
```

At the time this report was written, the M2 implementation had 24 passing
pytest tests, ruff passing, and mypy passing.

## Limitations

M2 does not parse timing lookup tables, timing surfaces, bus syntax, includes,
conditional timing expressions, power tables, or the full Liberty grammar. It
does not perform static timing analysis. It does not parse LEF, DEF, or GDS.

The parser should be described as a fixture-first Liberty subset parser, not as
a compliant production Liberty parser.

## M3 Handoff

M3 should use the M2 typed model to build a Standard Cell Atlas. The atlas can
summarize cells, areas, pins, functions, and minimal timing arc relationships
from synthetic fixtures. Real Sky130 read-only ingestion remains deferred to M5.
