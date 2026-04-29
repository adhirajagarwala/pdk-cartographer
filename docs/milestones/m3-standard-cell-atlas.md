# M3 Standard Cell Atlas

## Goal

M3 builds a fixture-first Standard Cell Atlas on top of the M2 Liberty parser.
The goal is to turn parsed synthetic Liberty metadata into deterministic,
portfolio-ready summaries: cell inventory, area ranking, pin summaries, family
grouping, cell-kind classification, and generated Markdown, CSV, and JSON
artifacts.

## Deliverables

- `src/pdk_cartographer/atlas/` package with typed atlas models.
- Conservative classification helpers for family, drive strength, clock-like
  pins, and cell kind.
- Summarizer that converts parsed `Library` objects into `CellRecord` entries
  and aggregate library summary metadata.
- Standard-library-only renderers for Markdown, CSV, and JSON.
- Repo-local generator script:
  `scripts/generate_fixture_atlas.py`
- Generated fixture artifacts:
  - `docs/reports/generated/m3-fixture-standard-cell-atlas.md`
  - `data/derived/m3_standard_cell_atlas/fixture_cell_inventory.csv`
  - `data/derived/m3_standard_cell_atlas/fixture_library_summary.json`
- Tests for classification, summarization, rendering, and the equivalent
  artifact generation path.
- Concept note, engineering log, milestone note, and engineering report.

## Acceptance Criteria

- The atlas accepts one or more parsed synthetic Liberty `Library` objects.
- Cell records are emitted in deterministic order by library name and cell
  name.
- Records include library name, cell name, area, family, drive strength, cell
  kind, pin categories, output functions, pin capacitance, and timing arc
  count.
- Summaries include cell count, area statistics, family counts, cell-kind
  counts, and largest/smallest cells when area data exists.
- Markdown output includes overview, source fixtures, library summary, cell
  inventory, area ranking, family summary, cell-kind summary, and limitations.
- CSV output has one row per cell record and stable column order.
- JSON output includes summary metadata and source fixture paths.
- Generated artifacts clearly state they are based on synthetic educational
  Liberty fixtures, not real Sky130 data.
- `python scripts/generate_fixture_atlas.py`, `python -m pytest`,
  `ruff check .`, and `mypy src` pass.

## Exclusions

M3 excludes real Sky130 ingestion, copied real PDK files, timing lookup-table
exploration, static timing analysis, timing plots, LEF/DEF/GDS parsing,
OpenLane/OpenROAD, Docker, package CLI work, and future milestone
implementation.

The atlas does not claim full Liberty support or real Sky130 analysis.

## Handoff to M4

M4 is the Timing Table Explorer. It should build from the parser and atlas
foundation, but focus on fixture-backed timing-table structure rather than
expanding the M3 atlas into real PDK ingestion. Real Sky130 read-only ingestion
remains deferred to M5.
