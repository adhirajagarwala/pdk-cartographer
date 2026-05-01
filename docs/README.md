# Documentation

This documentation records how `pdk-cartographer` is being built as a serious student EDA/PDK exploration toolkit. The project starts with synthetic Liberty fixtures so the code can be tested and explained before any real Sky130 ingestion is attempted.

## Concept Notes

- [PDK Anatomy](concepts/pdk-anatomy.md) explains the major kinds of files that make up a process design kit and where Liberty fits.
- [Liberty Basics](concepts/liberty-basics.md) describes libraries, cells, pins, scalar metadata, timing arcs, and timing tables at a high level.
- [Liberty Parser Scope](concepts/liberty-parser-scope.md) documents the M2 fixture-first parser architecture, supported subset, and exclusions.
- [Standard Cells](concepts/standard-cells.md) explains cell-level metadata such as area, pins, combinational behavior, sequential behavior, and naming conventions.
- [Standard Cell Atlas](concepts/standard-cell-atlas.md) explains the M3 atlas layer, cell records, area ranking, pin summaries, family grouping, classification rules, and limitations.
- [Timing Table Explorer](concepts/timing-table-explorer.md) explains the M4 timing-table subset, lookup-table templates, slew/load axes, summaries, and limitations.
- [Timing Corners](concepts/timing-corners.md) explains process, voltage, and temperature corners and why timing changes across them.

## M1 Records

- [M1 Repo Foundation](milestones/m1-repo-foundation.md) defines the scope, exclusions, acceptance criteria, and M2 handoff.
- [2026-04-27 M1 Kickoff Log](logs/2026-04-27-m1-kickoff.md) records the first project decisions.
- [M1 Foundation Report](reports/m1-foundation-report.md) summarizes the foundation state and parser scope.

## M2 Records

- [M2 Liberty Parser Core](milestones/m2-liberty-parser-core.md) defines the parser-core milestone scope, deliverables, acceptance criteria, exclusions, and M3 handoff.
- [2026-04-27 M2 Parser-Core Log](logs/2026-04-27-m2-liberty-parser-core.md) records the parser architecture, fixture, and diagnostics decisions.
- [M2 Liberty Parser Core Report](reports/m2-liberty-parser-core-report.md) summarizes the implementation, tests, limitations, and handoff to M3.

## M3 Records

- [M3 Standard Cell Atlas](milestones/m3-standard-cell-atlas.md) defines the atlas milestone scope, deliverables, acceptance criteria, exclusions, and M4 handoff.
- [2026-04-27 M3 Standard Cell Atlas Log](logs/2026-04-27-m3-standard-cell-atlas.md) records the atlas model, renderer, generator, and synthetic-data decisions.
- [M3 Standard Cell Atlas Report](reports/m3-standard-cell-atlas-report.md) summarizes the implementation, generated artifacts, tests, limitations, and handoff to M4.
- [Generated M3 Fixture Standard Cell Atlas](reports/generated/m3-fixture-standard-cell-atlas.md) is the deterministic Markdown artifact generated from synthetic Liberty fixtures.

## M4 Records

- [M4 Timing Table Explorer](milestones/m4-timing-table-explorer.md) defines the timing-table milestone scope, deliverables, acceptance criteria, exclusions, and M5 handoff.
- [2026-05-01 M4 Timing Table Explorer Log](logs/2026-05-01-m4-timing-table-explorer.md) records parser, explorer, renderer, generator, and workflow decisions.
- [M4 Timing Table Explorer Report](reports/m4-timing-table-explorer-report.md) summarizes the implementation, generated artifacts, tests, limitations, and handoff to M5.
- [Generated M4 Fixture Timing Table Explorer](reports/generated/m4-fixture-timing-table-explorer.md) is the deterministic Markdown artifact generated from synthetic timing-table Liberty fixtures.

## Roadmap

The top-level [ROADMAP.md](../ROADMAP.md) tracks the milestone sequence from synthetic fixtures toward later read-only Sky130 Liberty ingestion.
