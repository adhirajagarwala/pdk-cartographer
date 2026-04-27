# M2 Liberty Parser Core

## Goal

M2 strengthens the fixture-first Liberty parser into a small, tested parser core
that can support later standard-cell atlas work. It remains handwritten,
synthetic-fixture based, and intentionally limited.

## Deliverables

- A lexer that recognizes identifiers, strings, numbers, punctuation, comments,
  and source locations.
- A generic Liberty group/attribute tree.
- Typed `Library`, `Cell`, `Pin`, and `TimingArc` dataclasses for extracted
  metadata.
- Public parser API functions:
  - `parse_liberty_text(text: str)`
  - `parse_liberty_file(path: str | pathlib.Path)`
- Expanded synthetic fixtures:
  - `multi_cell_combinational.lib`
  - `timing_arcs.lib`
  - `parser_edge_cases.lib`
- Parser diagnostics with clear messages and line/column context where
  available.
- Tests for lexer behavior, generic group parsing, typed extraction, fixtures,
  timing arcs, and diagnostics.
- Concept documentation, engineering log, and an M2 report.

## Acceptance Criteria

- The parser extracts library names and simple library attributes.
- The parser extracts multiple cells, cell area, pins, pin direction, pin
  function, pin capacitance, and preserved simple attributes.
- Minimal timing arcs capture `related_pin`, `timing_sense`, and `timing_type`.
- All synthetic fixtures parse successfully.
- Malformed fixture text raises a custom parser error with a useful message.
- `python -m pytest`, `ruff check .`, and `mypy src` pass.
- Documentation clearly states that the parser is fixture-first and not
  Liberty-complete.

## Exclusions

M2 excludes real Sky130 ingestion, copied real PDK files, timing lookup-table
parsing, LEF/DEF/GDS parsing, OpenLane/OpenROAD, Docker, timing plots, ring
oscillator experiments, package CLI work, and future project implementation.

## Handoff to M3

M3 should build a Standard Cell Atlas on top of the M2 typed models. The next
step is not more grammar breadth for its own sake; it is using parsed fixture
metadata to summarize cells, areas, pins, functions, and timing arc structure in
a readable report-oriented way.
