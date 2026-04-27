# pdk-cartographer

Sky130 PDK Explorer and Experiment Atlas

A fixture-first exploration toolkit for Liberty timing, standard-cell metadata, and PDK anatomy.

## Status

M2 Liberty Parser Core implemented on the `m2-liberty-parser-core` branch.

This repository is a serious student-built EDA/PDK exploration toolkit. M1 established durable project boundaries, documentation structure, synthetic fixtures, and quality expectations. M2 strengthens the fixture-first Liberty parser core with a lexer, generic group parser, typed model extraction, diagnostics, expanded synthetic fixtures, and focused tests.

Real Sky130 ingestion has not started. The current parser is not a full Liberty parser and should be treated as a documented educational subset.

## Why This Exists After CurveCraft

CurveCraft focused on compact-model fitting and ngspice validation. `pdk-cartographer` moves into the digital PDK side of the semiconductor stack: Liberty timing metadata, standard-cell organization, timing corners, and the anatomy of files that support ASIC implementation flows.

The point is not to pretend to replace production EDA tools. The point is to build a readable, tested atlas that explains what PDK artifacts contain, how small pieces can be parsed safely, and where educational experiments stop before becoming claims about silicon or signoff accuracy.

## What M1 and M2 Include

- Repo guardrails and contribution notes.
- A Python 3.11+ foundation using the `src/pdk_cartographer` package layout.
- Tiny synthetic Liberty fixtures marked clearly as educational data.
- A fixture-oriented Liberty parser core with lexer/tokenizer, generic group tree, typed models, and diagnostics.
- Documentation for PDK anatomy, Liberty basics, standard cells, and timing corners.
- Local validation expectations using pytest, ruff, and mypy.
- Engineering logs, milestone notes, and foundation/parser-core reports.

## What M1 and M2 Do Not Include

- No Sky130 download or copied Sky130 source files.
- No OpenLane, OpenROAD, Docker, or external PDK toolchain setup.
- No LEF, DEF, or GDS parsing.
- No timing lookup-table parsing.
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
- [M1 kickoff log](docs/logs/2026-04-27-m1-kickoff.md)
- [M2 parser-core log](docs/logs/2026-04-27-m2-liberty-parser-core.md)
- [Roadmap](ROADMAP.md)
