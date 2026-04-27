# pdk-cartographer

Sky130 PDK Explorer and Experiment Atlas

A fixture-first exploration toolkit for Liberty timing, standard-cell metadata, and PDK anatomy.

## Status

M1 starting / foundation phase.

This repository is beginning as a serious student-built EDA/PDK exploration toolkit. M1 is intentionally small: it establishes durable project boundaries, documentation structure, synthetic fixtures, and quality expectations before any real Sky130 ingestion.

## Why This Exists After CurveCraft

CurveCraft focused on compact-model fitting and ngspice validation. `pdk-cartographer` moves into the digital PDK side of the semiconductor stack: Liberty timing metadata, standard-cell organization, timing corners, and the anatomy of files that support ASIC implementation flows.

The point is not to pretend to replace production EDA tools. The point is to build a readable, tested atlas that explains what PDK artifacts contain, how small pieces can be parsed safely, and where educational experiments stop before becoming claims about silicon or signoff accuracy.

## What M1 Includes

- Repo guardrails and contribution notes.
- A Python 3.11+ foundation using the `src/pdk_cartographer` package layout.
- Tiny synthetic Liberty fixtures marked clearly as educational data.
- A minimal fixture-oriented Liberty parser.
- Documentation for PDK anatomy, Liberty basics, standard cells, and timing corners.
- Local validation expectations using pytest, ruff, and mypy.
- Engineering logs and a foundation report.

## What M1 Does Not Include

- No Sky130 download or copied Sky130 source files.
- No OpenLane, OpenROAD, Docker, or external PDK toolchain setup.
- No LEF, DEF, or GDS parsing.
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
- [M1 kickoff log](docs/logs/2026-04-27-m1-kickoff.md)
- [Roadmap](ROADMAP.md)
