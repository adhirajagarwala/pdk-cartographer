# 2026-04-27 M3 Standard Cell Atlas

## Context

M3 starts from the M2 Liberty Parser Core. The parser already produces typed
`Library`, `Cell`, `Pin`, and `TimingArc` objects from synthetic educational
Liberty fixtures. The M3 task is to summarize that parsed metadata into a
readable atlas without broadening the project into real PDK ingestion.

## Decisions

- Built the atlas layer on top of the M2 typed parser models rather than
  adding another parser path.
- Added immutable atlas-facing dataclasses for cell records, library summaries,
  and full atlas snapshots.
- Kept classification conservative: simple family and drive suffix extraction,
  clock-like pin detection, generic DFF/LATCH sequential hints, and unknown
  fallback when metadata is insufficient.
- Used only the Python standard library for Markdown, CSV, and JSON renderers.
- Added a repo-local generator script,
  `scripts/generate_fixture_atlas.py`, rather than a package CLI.
- Generated deterministic Markdown, CSV, and JSON artifacts from synthetic
  fixtures.
- Kept all source data synthetic and educational.
- Avoided real Sky130 ingestion, copied PDK files, timing analysis,
  lookup-table exploration, LEF/DEF/GDS parsing, and external toolchain setup.

## Risks

- The atlas can look authoritative if the synthetic-fixture boundary is not
  repeated clearly. Generated reports and docs must keep saying that this is
  not real Sky130 data.
- Classification helpers are intentionally generic. They should not grow into
  Sky130-specific naming rules before real read-only ingestion exists.
- Timing arc counts are useful metadata, but they should not be described as
  timing analysis.

## Next Steps

- Keep M3 focused on atlas reports and documentation polish.
- Use M4 for fixture-backed Timing Table Explorer work.
- Defer real Sky130 read-only ingestion to M5.
- Keep LEF exploration later, after Liberty parsing and reporting are solid.
- Continue validating with `python scripts/generate_fixture_atlas.py`,
  `python -m pytest`, `ruff check .`, and `mypy src`.
