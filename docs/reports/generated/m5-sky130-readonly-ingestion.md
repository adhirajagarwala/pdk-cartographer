# M5 Sky130 Read-Only Ingestion Report

This report is generated from an external Sky130 PDK installation. Raw PDK files are not committed to this repository.

M5 is read-only exploration of Liberty metadata and parser compatibility. It is not production signoff, static timing analysis, or a claim of full Liberty support.

## PDK Root Strategy

- Preferred environment variable: `PDK_CARTOGRAPHER_PDK_ROOT`
- Display root: `$PDK_CARTOGRAPHER_PDK_ROOT`
- Generated artifacts store relative paths from the configured PDK root.
- Raw Liberty contents are not copied, embedded, or summarized as source text.

## Variants Found

| Variant | Relative Path | Liberty Files |
| --- | --- | ---: |
| sky130A | `ciel/sky130/versions/d815bb30c9afdf9e264c276a8a2b533108dea3d0/sky130A` | 737 |
| sky130B | `ciel/sky130/versions/d815bb30c9afdf9e264c276a8a2b533108dea3d0/sky130B` | 737 |

## Liberty File Inventory Summary

- Total `.lib` files discovered: 1474

### Standard-Cell Family Counts

| Family | Count |
| --- | ---: |
| sky130_fd_sc_hd | 36 |
| sky130_fd_sc_hvl | 122 |

### Inferred Corner Summary

| Corner | Count |
| --- | ---: |
| ff_085C_5v50 | 2 |
| ff_085C_5v50_lv1v95 | 2 |
| ff_100C_1v65 | 2 |
| ff_100C_1v95 | 2 |
| ff_100C_5v50 | 2 |
| ff_100C_5v50_lowhv1v65_lv1v95 | 2 |
| ff_100C_5v50_lv1v95 | 2 |
| ff_150C_5v50 | 2 |
| ff_150C_5v50_lv1v95 | 2 |
| ff_n40C_1v56 | 2 |
| ff_n40C_1v65 | 2 |
| ff_n40C_1v76 | 2 |
| ff_n40C_1v95 | 2 |
| ff_n40C_1v95_ccsnoise | 2 |
| ff_n40C_4v40 | 2 |
| ff_n40C_4v40_lv1v95 | 2 |
| ff_n40C_4v95 | 2 |
| ff_n40C_4v95_lv1v95 | 2 |
| ff_n40C_5v50 | 2 |
| ff_n40C_5v50_ccsnoise | 2 |
| ff_n40C_5v50_lowhv1v65_lv1v95 | 2 |
| ff_n40C_5v50_lv1v95 | 2 |
| ff_n40C_5v50_lv1v95_ccsnoise | 2 |
| gpiov2_pad_ff_ff_100C_1v95_5v50 | 2 |
| gpiov2_pad_ff_ff_n40C_1v95_5v50 | 2 |
| gpiov2_pad_ff_ff_n40C_1v95_5v50_nointpwr | 2 |
| gpiov2_pad_ff_ss_100C_1v65_1v65 | 2 |
| gpiov2_pad_ff_ss_100C_1v95_1v65 | 2 |
| gpiov2_pad_ff_ss_100C_1v95_1v95 | 2 |
| gpiov2_pad_ff_ss_n40C_1v65_1v65 | 2 |
| Other inferred corners | 1392 |

## Selected Target Subset

| Variant | Family | Corner | Size Bytes | Relative Path |
| --- | --- | --- | ---: | --- |
| sky130A | sky130_fd_sc_hd | tt_025C_1v80 | 12841637 | `ciel/sky130/versions/d815bb30c9afdf9e264c276a8a2b533108dea3d0/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib` |
| sky130A | sky130_fd_sc_hd | ff_100C_1v95 | 12842685 | `ciel/sky130/versions/d815bb30c9afdf9e264c276a8a2b533108dea3d0/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__ff_100C_1v95.lib` |
| sky130A | sky130_fd_sc_hd | ss_100C_1v40 | 12847083 | `ciel/sky130/versions/d815bb30c9afdf9e264c276a8a2b533108dea3d0/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__ss_100C_1v40.lib` |

## Parser Compatibility Table

| File | Success | Library | Cells | Timing Tables | Error |
| --- | --- | --- | ---: | ---: | --- |
| `ciel/sky130/versions/d815bb30c9afdf9e264c276a8a2b533108dea3d0/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib` | yes | sky130_fd_sc_hd__tt_025C_1v80 | 428 | 5368 |  |
| `ciel/sky130/versions/d815bb30c9afdf9e264c276a8a2b533108dea3d0/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__ff_100C_1v95.lib` | yes | sky130_fd_sc_hd__ff_100C_1v95 | 428 | 5368 |  |
| `ciel/sky130/versions/d815bb30c9afdf9e264c276a8a2b533108dea3d0/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__ss_100C_1v40.lib` | yes | sky130_fd_sc_hd__ss_100C_1v40 | 428 | 5368 |  |

## Parser Compatibility Summary

- Parse successes: 3
- Parse failures: 0
- Scope warning: The current parser is a fixture-first educational Liberty subset parser. These results are compatibility probes only and do not claim full Liberty support or production signoff readiness.

## Limitations

- The current parser remains a fixture-first educational subset parser.
- Successful parsing of the selected subset does not imply full Liberty compliance.
- The report records metadata only and does not dump raw Liberty text.
- M5 does not perform timing interpolation, static timing analysis, physical layout analysis, or signoff validation.
- Results depend on the external PDK version selected by the environment.

## M6 Handoff

- Use the M5 manifest and compatibility results as the input baseline for M6 report polishing and broader corner comparison.
- Keep raw PDK files external and continue committing only small generated summary artifacts.
- Treat parser extensions as bounded compatibility improvements, not a full Liberty parser rewrite.
