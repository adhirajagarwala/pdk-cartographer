# pdk-cartographer

Sky130 PDK Explorer and Experiment Atlas

A fixture-first exploration toolkit for Liberty timing, standard-cell metadata, and PDK anatomy.

## Status

M5 Real Sky130 Read-Only Ingestion is in progress on the `m5-sky130-readonly-ingestion` branch. M1 through M4 are complete, and M5 now adds external Sky130 discovery, safe generated manifests, and parser compatibility probes.

This repository is a serious student-built EDA/PDK exploration toolkit. M1 established durable project boundaries, documentation structure, synthetic fixtures, and quality expectations. M2 strengthens the fixture-first Liberty parser core with a lexer, generic group parser, typed model extraction, diagnostics, expanded synthetic fixtures, and focused tests.

M3 adds a Standard Cell Atlas layer on top of the M2 parser. It summarizes synthetic Liberty fixture cells into deterministic records, area rankings, pin summaries, family counts, conservative combinational/sequential/unknown classification, and generated Markdown/CSV/JSON artifacts.

M4 adds a Timing Table Explorer. It parses small synthetic lookup-table templates and timing tables, summarizes slew/load table shapes and timing arc metadata, and generates deterministic Markdown/CSV/JSON artifacts.

Real Sky130 ingestion starts in M5 as read-only external PDK exploration. Raw PDK files are not stored in this repository; use `PDK_CARTOGRAPHER_PDK_ROOT` to point at an external Sky130 installation, with `PDK_ROOT` as a fallback. The current parser is not a full Liberty parser and should be treated as a documented educational subset.

## Why This Exists After CurveCraft

CurveCraft focused on compact-model fitting and ngspice validation. `pdk-cartographer` moves into the digital PDK side of the semiconductor stack: Liberty timing metadata, standard-cell organization, timing corners, and the anatomy of files that support ASIC implementation flows.

The point is not to pretend to replace production EDA tools. The point is to build a readable, tested atlas that explains what PDK artifacts contain, how small pieces can be parsed safely, and where educational experiments stop before becoming claims about silicon or signoff accuracy.

## What M1 Through M4 Include

- Repo guardrails and contribution notes.
- A Python 3.11+ foundation using the `src/pdk_cartographer` package layout.
- Tiny synthetic Liberty fixtures marked clearly as educational data.
- A fixture-oriented Liberty parser core with lexer/tokenizer, generic group tree, typed models, and diagnostics.
- A Standard Cell Atlas package for fixture-derived cell records, area rankings, pin summaries, family grouping, and conservative cell-kind classification.
- Timing-table fixtures covering lookup-table templates, `index_1`, `index_2`, `values`, and the four M4 table kinds.
- Parser models for synthetic lookup-table templates and timing tables.
- A Timing Table Explorer package for structural table summaries.
- Standard-library Markdown, CSV, and JSON renderers.
- A repo-local fixture atlas generator script.
- A repo-local fixture timing report generator script.
- Generated synthetic fixture atlas and timing-table artifacts.
- Documentation for PDK anatomy, Liberty basics, standard cells, and timing corners.
- Local validation expectations using pytest, ruff, and mypy.
- Engineering logs, milestone notes, and foundation/parser-core/atlas/timing-table reports.

## What M5 Adds

- Environment-driven external PDK root discovery using `PDK_CARTOGRAPHER_PDK_ROOT`, then `PDK_ROOT`.
- Bounded read-only discovery of `sky130A` and `sky130B` directories.
- Real Sky130 Liberty manifests with relative paths, sizes, inferred families, and inferred corners.
- A selected max-three `sky130_fd_sc_hd` parser-probe subset covering one TT-like, one FF-like, and one SS-like corner when available.
- Parser compatibility JSON that records success/failure, library names, cell counts, timing table counts, and compact errors without dumping raw Liberty text.
- A generated M5 read-only ingestion report.
- Tests that use temporary fake PDK trees so CI does not require a real Sky130 install.

## What M1 Through M5 Do Not Include

- No copied Sky130 source files.
- No symlinked Sky130 source files.
- No OpenLane, OpenROAD, or Docker setup.
- No LEF, DEF, or GDS parsing.
- No static timing analysis or production timing signoff.
- No timing interpolation.
- No timing plots.
- No ring oscillator experiments.
- No silicon-dossier or register-city work.
- No package CLI.
- No fake badges.
- No GitHub remote creation, commits, or tags without explicit approval.

## Roadmap Summary

- M1 - Repo Foundation and Liberty Fixtures.
- M2 - Liberty Parser Core.
- M3 - Standard Cell Atlas.
- M4 - Timing Table Explorer.
- M5 - Real Sky130 Read-Only Ingestion.
- M6 - PDK Atlas Reports and Portfolio Release.

LEF exploration belongs later, after Liberty structure and reporting are solid.

## Documentation

- [Documentation index](docs/README.md)
- [M1 foundation report](docs/reports/m1-foundation-report.md)
- [M2 Liberty Parser Core report](docs/reports/m2-liberty-parser-core-report.md)
- [M3 Standard Cell Atlas report](docs/reports/m3-standard-cell-atlas-report.md)
- [Generated M3 fixture atlas](docs/reports/generated/m3-fixture-standard-cell-atlas.md)
- [M4 Timing Table Explorer report](docs/reports/m4-timing-table-explorer-report.md)
- [Generated M4 fixture timing-table explorer](docs/reports/generated/m4-fixture-timing-table-explorer.md)
- [Real PDK read-only ingestion concept note](docs/concepts/real-pdk-readonly-ingestion.md)
- [M5 Sky130 Read-Only Ingestion milestone](docs/milestones/m5-sky130-readonly-ingestion.md)
- [M5 Sky130 Read-Only Ingestion report](docs/reports/m5-sky130-readonly-ingestion-report.md)
- [Generated M5 Sky130 read-only ingestion report](docs/reports/generated/m5-sky130-readonly-ingestion.md)
- [M1 kickoff log](docs/logs/2026-04-27-m1-kickoff.md)
- [M2 parser-core log](docs/logs/2026-04-27-m2-liberty-parser-core.md)
- [M3 standard-cell atlas log](docs/logs/2026-04-27-m3-standard-cell-atlas.md)
- [M4 timing-table explorer log](docs/logs/2026-05-01-m4-timing-table-explorer.md)
- [M5 Sky130 read-only ingestion log](docs/logs/2026-05-03-m5-sky130-readonly-ingestion.md)
- [Roadmap](ROADMAP.md)
