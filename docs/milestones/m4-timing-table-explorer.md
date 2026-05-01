# M4 - Timing Table Explorer

## Goal

M4 extends the fixture-first Liberty parser toward timing-table concepts. It
parses small synthetic Liberty timing fixtures, models lookup-table templates
and timing tables, summarizes arc/table structure, and renders deterministic
Markdown, CSV, and JSON artifacts.

## Deliverables

- Synthetic timing-table fixtures under `data/fixtures/liberty/`.
- Parser support for `lu_table_template`, `index_1`, `index_2`, `values`, and
  the M4 timing table kinds.
- Typed Liberty models for lookup-table templates and timing tables.
- A `pdk_cartographer.timing` explorer package for deterministic structural
  summaries.
- Standard-library Markdown, CSV, and JSON renderers.
- Repo-local generator script:
  `scripts/generate_fixture_timing_report.py`.
- Generated synthetic timing-table artifacts:
  - `docs/reports/generated/m4-fixture-timing-table-explorer.md`
  - `data/derived/m4_timing_table_explorer/fixture_timing_tables.csv`
  - `data/derived/m4_timing_table_explorer/fixture_timing_summary.json`
- Tests for parsing, malformed dimensions, summarization, rendering, and the
  generated-artifact path.
- Documentation for timing-table concepts, limitations, and the M5 handoff.

## Acceptance Criteria

- M1, M2, and M3 behavior continues to pass the local validation gate.
- Timing-table fixtures are clearly synthetic educational fixtures and are not
  copied from Sky130 or any real PDK.
- Lookup-table templates expose axis variables and index points.
- Timing tables attach to the correct timing arcs.
- Malformed table dimensions produce useful parser errors.
- Explorer summaries report table counts, table kinds, dimensions, related
  pins, timing metadata, axis names, and value ranges.
- Generated Markdown, CSV, and JSON outputs are deterministic.
- Reports clearly state that they use synthetic fixtures only.
- No package CLI is added.

## Exclusions

M4 does not download or copy real Sky130 data. It does not perform static timing
analysis, timing interpolation, timing plotting, OpenLane/OpenROAD integration,
Docker setup, LEF/DEF/GDS parsing, ring oscillator experiments, or future
milestone implementation.

The parser remains a documented educational Liberty subset, not a full Liberty
implementation.

## Handoff to M5

M5 is Real Sky130 Read-Only Ingestion. M4 leaves behind tested timing-table
structure models and reports so M5 can approach real Sky130 Liberty files
carefully, read-only, and without copying PDK source files into the repository.
