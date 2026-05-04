# M5 - Real Sky130 Read-Only Ingestion

## Goal

M5 discovers a real external Sky130 PDK installation, builds safe Liberty
manifests and reports, and probes the current parser against a selected real
Liberty subset. The milestone is read-only with respect to PDK files.

## Deliverables

- External PDK root discovery through `PDK_CARTOGRAPHER_PDK_ROOT`, with
  fallback to `PDK_ROOT`.
- Bounded Sky130 variant discovery for `sky130A` and `sky130B`.
- Typed PDK discovery models for roots, variants, and Liberty files.
- Generated Liberty inventory artifacts:
  - `data/derived/m5_sky130_readonly/sky130_liberty_files.csv`
  - `data/derived/m5_sky130_readonly/sky130_liberty_manifest.json`
- Generated parser compatibility artifact:
  - `data/derived/m5_sky130_readonly/sky130_parse_compatibility.json`
- Generated Markdown report:
  - `docs/reports/generated/m5-sky130-readonly-ingestion.md`
- Tests using temporary fake PDK trees so CI does not require Sky130.
- Documentation for read-only ingestion, external roots, limitations, and M6
  handoff.

## Acceptance Criteria

- `PDK_CARTOGRAPHER_PDK_ROOT` is preferred over `PDK_ROOT`.
- Missing PDK roots fail clearly in scripts and return empty discovery results
  in library code.
- Discovery supports roots that directly contain Sky130 variants and roots that
  contain nested Ciel-style installs.
- Discovery is bounded and read-only.
- Generated artifacts use relative paths from the configured PDK root and avoid
  hardcoded personal paths.
- Raw PDK files are not copied, symlinked, or committed.
- The selected subset is at most three Liberty files and prefers
  `sky130A/sky130_fd_sc_hd` with TT, FF, and SS style corners when available.
- Parser compatibility records success or failure per selected file without
  dumping raw Liberty text or large stack traces.
- Reports state that M5 is read-only exploration, not static timing analysis,
  full Liberty compliance, or production signoff.
- `python -m pytest`, `ruff check .`, and `mypy src` pass.

## Exclusions

M5 does not add OpenLane, OpenROAD, Docker, LEF/DEF/GDS parsing, static timing
analysis, timing interpolation, timing plots, ring oscillators, `silicon-dossier`,
`register-city`, or CurveCraft changes.

M5 does not claim that the parser is a complete Liberty implementation.

## Handoff to M6

M6 should broaden or polish reports based on the M5 manifest and compatibility
findings. Corner comparison and portfolio-ready explanation are appropriate
next steps. Raw PDK files should remain external and environment-driven.
