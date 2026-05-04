# 2026-05-03 - M5 Sky130 Read-Only Ingestion

## Decisions

- Used Ciel as the external Sky130 setup path instead of building `open_pdks`
  from source.
- Kept the external PDK under `$HOME/pdks/ciel` and configured the project with
  `PDK_CARTOGRAPHER_PDK_ROOT`.
- Added explicit `.gitignore` protections for local PDK roots, external mounts,
  and common raw PDK file extensions.
- Added a `pdk_cartographer.pdk` package for environment-driven discovery,
  typed models, manifest generation, and report generation.
- Generated only small summary artifacts under `data/derived/m5_sky130_readonly`
  and `docs/reports/generated`.
- Selected a max-three real Liberty subset from `sky130A/sky130_fd_sc_hd`: one
  TT-like file, one FF-like file, and one SS-like file.
- Treated parser results as compatibility probes, not full Liberty compliance.
- Kept all tests based on temporary fake PDK trees so CI does not need a real
  Sky130 installation.

## Observations

The discovered Ciel Sky130 install contains both `sky130A` and `sky130B`, with
many Liberty files across multiple families and corners. The selected subset is
small enough to be reviewable but still exercises real Liberty syntax at a much
larger scale than the synthetic fixtures.

The current parser can record library name, cell count, and timing table count
for the selected subset. That result is useful, but it should stay framed as a
compatibility result. It does not prove full Liberty support.

## Risks

Real Liberty files can be large and easy to accidentally copy into a repo. M5
therefore depends on both ignore rules and documentation discipline.

The generated artifacts include relative paths that reveal the external PDK
layout and selected PDK hash. That is acceptable for reproducibility, but local
absolute user paths should stay out of committed artifacts.

## Next Steps

- Complete M5 docs and final audit.
- Keep generated artifacts deterministic and small.
- Use M6 to polish the report story and broaden corner comparison if that stays
  useful for the portfolio arc.
