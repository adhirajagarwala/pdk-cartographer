# M5 Sky130 Read-Only Ingestion Report

## Objective

M5 moves from synthetic Liberty fixtures to careful read-only exploration of a
real external Sky130 PDK installation. The goal is to discover the Liberty file
layout, generate safe summary artifacts, and probe parser compatibility without
copying raw PDK files into this repository.

This milestone is not static timing analysis, timing interpolation, full
Liberty compliance, or production timing signoff.

## External PDK Root

The preferred setup is:

```bash
export PDK_CARTOGRAPHER_PDK_ROOT="$HOME/pdks/ciel"
```

If `PDK_CARTOGRAPHER_PDK_ROOT` is not set, the code falls back to `PDK_ROOT`.
The scripts use the configured root as external source material and write only
small generated summaries into the repo.

## Discovery Package

M5 adds `pdk_cartographer.pdk`, which includes:

- environment configuration helpers
- bounded Sky130 variant discovery
- typed models for PDK roots, variants, and Liberty files
- Liberty family and corner inference
- manifest generation
- parser compatibility reports

Discovery supports roots that directly point to `sky130A` or `sky130B`, and
roots that contain those directories deeper in a Ciel-style tree.

## Generated Artifacts

The M5 scripts write:

- `data/derived/m5_sky130_readonly/sky130_liberty_files.csv`
- `data/derived/m5_sky130_readonly/sky130_liberty_manifest.json`
- `data/derived/m5_sky130_readonly/sky130_parse_compatibility.json`
- `docs/reports/generated/m5-sky130-readonly-ingestion.md`

These files contain metadata such as relative paths, file sizes, inferred
families, inferred corners, selected-target flags, and compact parser results.
They do not contain raw Liberty source text.

## Selected Liberty Subset

M5 selects at most three real Liberty files for the first parser compatibility
probe. The selection prefers:

- `sky130A`
- `sky130_fd_sc_hd`
- one TT-like corner
- one FF-like corner
- one SS-like corner

The current external install has a single TT `sky130_fd_sc_hd` corner plus
multiple FF and SS corners. Selecting one TT, one FF, and one SS file is the
right M5 scope: it gives meaningful real-file coverage without turning the
milestone into a full PDK parser rewrite.

## Parser Compatibility

The compatibility probe attempts to parse the selected files and records:

- success or failure
- library name when parsed
- cell count when parsed
- timing table count when parsed
- compact error class and message when parsing fails

The current parser remains an educational subset parser built from synthetic
fixtures. A successful probe is useful evidence that selected real files can be
read, but it is not a claim of complete Liberty support.

## Tests

M5 tests use temporary fake PDK trees. They cover environment variable
selection, missing roots, nested Sky130 discovery, family and corner inference,
relative path normalization, manifest writers, selected subset logic,
compatibility success/failure records, and generated report rendering.

CI should not need a real Sky130 installation.

## Limitations

- No raw PDK files are committed.
- No symlinks into the external PDK are created.
- No OpenLane, OpenROAD, Docker, LEF, DEF, or GDS work is included.
- No static timing analysis is performed.
- No timing interpolation or timing plots are produced.
- Full Liberty compliance is not claimed.
- Production timing signoff is not claimed.

## M6 Handoff

M6 should build on the M5 manifest and compatibility output. The most natural
next step is broader report polish and corner comparison that remains honest
about parser scope and read-only PDK handling.
