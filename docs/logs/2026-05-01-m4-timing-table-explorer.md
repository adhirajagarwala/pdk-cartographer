# 2026-05-01 - M4 Timing Table Explorer

## Decisions

- Built the timing-table parser subset on top of the M2 generic Liberty parser
  instead of adding a separate ad hoc reader.
- Kept the synthetic fixture-first philosophy from M1 through M3.
- Added typed models for lookup-table templates and timing tables.
- Added explorer summaries that describe table shape and metadata without doing
  static timing analysis.
- Used standard-library renderers for Markdown, CSV, and JSON outputs.
- Added a repo-local generator script instead of a package CLI.
- Did not add timing plots, interpolation, real Sky130 ingestion, LEF/DEF/GDS
  parsing, OpenLane/OpenROAD, Docker, or future milestone work.
- Kept the no-PR workflow guardrail: milestone work stays local, validated, and
  fast-forwarded rather than merged through GitHub web/API flows.

## Risks

Timing tables can look like timing analysis because they contain numerical
delay and transition data. M4 documentation and generated reports therefore
need to keep saying that the numbers are synthetic fixture data and that no
static timing analysis is performed.

The parser now accepts more Liberty-like syntax than M2, but it is still a
small educational subset. Future work should avoid describing it as full
Liberty compliance.

M4 fixtures live beside earlier fixtures, so generator scripts need explicit
fixture selection when an older milestone artifact should remain stable.

## Next Steps

- Complete the M4 final audit and release-readiness checklist.
- Regenerate M3 and M4 artifacts as part of the final gate.
- Review docs and generated outputs for consistent synthetic-only language.
- Prepare M5 as read-only real Sky130 Liberty ingestion, without copying PDK
  source files into this repository.
