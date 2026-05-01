# M4 Timing Table Explorer Report

## Objective

M4 adds a timing-table explorer for small synthetic Liberty fixtures. The goal
is to make lookup-table templates, slew/load axes, timing table shapes, and
timing arc metadata visible in deterministic portfolio artifacts.

This milestone does not ingest real Sky130 data, perform static timing
analysis, interpolate timing values, or claim full Liberty compliance.

## Starting Point From M3

M3 left the project with a fixture-first Liberty parser, typed library/cell/pin
models, a Standard Cell Atlas, generated Markdown/CSV/JSON artifacts, and a
local quality gate. M4 builds on that parser and preserves the M3 atlas
behavior.

## Timing-Table Parser Extension

The parser now supports a narrow timing-table subset for the M4 fixtures:

- `lu_table_template(template_name) { ... }`
- `variable_1` and `variable_2`
- `index_1("...")` and `index_2("...")`
- `values("...", "...")`
- `cell_rise`, `cell_fall`, `rise_transition`, and `fall_transition`

Timing tables are attached to the parsed timing arc that contains them. When a
table references a known lookup-table template, the parser resolves the template
indices onto the table. Dimension checks report useful parser errors when a
table matrix does not match the available axes.

## Fixture Suite

M4 adds three synthetic educational fixtures:

- `data/fixtures/liberty/timing_table_2x2.lib`
- `data/fixtures/liberty/timing_table_3x3.lib`
- `data/fixtures/liberty/timing_table_edge_cases.lib`

These fixtures are intentionally tiny. They are not copied from Sky130 or any
real PDK.

## Lookup-Table Template Model

The lookup-table template model records the template name, optional axis
variables, and parsed numeric index axes. In the M4 fixtures, the axes represent
input transition and output capacitance concepts, but the values remain
synthetic.

## Timing-Table Record Model

The timing-table explorer emits one record per timing table. Each record
includes the library, cell, pin, related pin, timing type, timing sense, table
kind, template name, axis variables, table dimensions, and structural min/max
values.

The record model is descriptive. It does not calculate path delay, check setup
or hold timing, or interpolate between lookup points.

## Explorer Summary Outputs

The explorer summarizes:

- total timing table count
- table-kind counts
- timing type and timing sense counts
- dimension counts such as `2x2` and `3x3`
- source libraries and cells
- deterministic source fixture paths

The ordering is deterministic so regenerated reports remain stable.

## Generated Artifacts

The repo-local generator script writes:

- `docs/reports/generated/m4-fixture-timing-table-explorer.md`
- `data/derived/m4_timing_table_explorer/fixture_timing_tables.csv`
- `data/derived/m4_timing_table_explorer/fixture_timing_summary.json`

The generated Markdown report states that it uses synthetic educational Liberty
fixtures, not real Sky130 data.

## Tests and Quality Gates

M4 adds tests for lookup-template parsing, axis parsing, matrix parsing, all
four timing table kinds, timing-arc attachment, malformed dimensions, explorer
summaries, renderer determinism, and the generator path.

The expected local gate is:

```bash
python scripts/generate_fixture_timing_report.py
python scripts/generate_fixture_atlas.py
python -m pytest
ruff check .
mypy src
```

## Limitations

M4 is limited to synthetic fixtures and a small documented Liberty subset. It
does not support production-scale Liberty recovery, bus syntax, power tables,
conditional timing expressions, full characterization semantics, static timing
analysis, timing interpolation, or timing plots.

M4 also does not add LEF, DEF, GDS, OpenLane, OpenROAD, Docker, or a package
CLI.

## M5 Handoff

M5 should add carefully scoped real Sky130 read-only Liberty ingestion. It
should reuse the M4 timing-table structure where appropriate, preserve the
synthetic fixture tests, and keep real PDK files out of the repository.
