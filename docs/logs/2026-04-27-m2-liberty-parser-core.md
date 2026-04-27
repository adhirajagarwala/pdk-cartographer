# 2026-04-27 M2 Liberty Parser Core

## Context

M2 started from the M1 foundation on the `m2-liberty-parser-core` feature
branch. M1 had tiny synthetic Liberty fixtures and a minimal handwritten parser.
The M2 task was to make that parser core more credible without crossing into
real Sky130 ingestion or full Liberty parser claims.

## Decisions

- Created the feature branch `m2-liberty-parser-core` from a clean M1 baseline.
- Split tokenization into a dedicated lexer with line and column tracking.
- Added a generic group/attribute tree before typed model extraction.
- Strengthened typed dataclasses for `Library`, `Cell`, `Pin`, and `TimingArc`.
- Added dictionary-based lookup for cells and pins to support later atlas work.
- Expanded the synthetic fixture suite with multi-cell, timing-arc, and parser
  edge-case examples.
- Added diagnostics objects and custom parser/lexer exceptions.
- Kept all fixture data synthetic and clearly marked as educational.
- Avoided real Sky130 ingestion, timing lookup-table parsing, LEF/DEF/GDS work,
  package CLI work, and external toolchain setup.

## Risks

- It would be easy for the parser to drift into a broad Liberty implementation
  without a clear need. M2 limits grammar support to fixture-driven behavior.
- Public documentation must not imply that synthetic fixture parsing proves
  real PDK readiness.
- Later Sky130 ingestion will need read-only handling and source attribution
  rather than copied PDK files in the repository.

## Next Steps

- Use the typed model layer in M3 to build a Standard Cell Atlas.
- Keep M3 focused on metadata summaries rather than timing-table analysis.
- Defer real Sky130 read-only ingestion until M5.
- Continue running `python -m pytest`, `ruff check .`, and `mypy src` as the
  local quality gate.
