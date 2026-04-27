# M1 Foundation Report

## Objective

M1 establishes `pdk-cartographer` as a fixture-first exploration toolkit for Liberty timing metadata, standard-cell organization, and PDK anatomy. This is a foundation report, not a Sky130 analysis report. No real Sky130 files have been downloaded, copied, or ingested.

## Repository Structure

The repository contains bootstrap documentation, a Python package skeleton, synthetic Liberty fixtures, parser modules, tests, and M1 documentation.

- `src/pdk_cartographer` holds the package code.
- `src/pdk_cartographer/liberty` holds Liberty dataclasses and the fixture-subset parser.
- `data/fixtures/liberty` holds tiny synthetic `.lib` files.
- `tests` verifies import behavior and parser behavior.
- `docs` records concepts, milestone scope, engineering decisions, and reports.

## Fixture Philosophy

The fixtures are intentionally synthetic and small. They use realistic Liberty-like syntax to teach structure without copying Sky130 data or pretending to represent a characterized cell library. This makes parser behavior auditable and keeps the project safe for a public portfolio repository.

## Minimal Parser Scope

The M1 parser extracts:

- library name
- cell names
- cell area
- pin names
- pin direction
- pin function
- pin capacitance
- minimal timing arc fields such as `related_pin`, `timing_sense`, and `timing_type`

The parser is handwritten and structured around tokenization plus group parsing. It is scoped to the current fixtures and is not Liberty-complete.

## Tests and Quality Gates

The current quality expectation is:

```bash
python -m pytest
ruff check .
mypy src
```

Tests cover package import and both Liberty fixture files. Ruff and mypy are part of the M1 development contract so style and type drift are visible early.

## Limitations

M1 does not parse timing lookup tables, buses, includes, conditional timing expressions, LEF/DEF/GDS files, or real Sky130 libraries. It does not install OpenLane, OpenROAD, Docker, or any external PDK flow. It does not provide a package CLI.

## M2 Handoff

M2 should strengthen the Liberty parser core by improving error messages, documenting the supported subset more formally, and adding tests only for syntax the project actually needs. Real Sky130 read-only ingestion remains deferred until later milestones.
