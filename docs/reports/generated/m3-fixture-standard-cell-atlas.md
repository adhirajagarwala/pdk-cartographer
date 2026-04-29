# M3 Fixture Standard Cell Atlas

This atlas is generated from synthetic educational Liberty fixtures, not real Sky130 data.

## Overview

- Libraries: 5
- Cells: 7
- Area min: 1.2
- Area max: 4.8
- Area mean: 2.15714

## Source Fixtures

- `data/fixtures/liberty/multi_cell_combinational.lib`
- `data/fixtures/liberty/parser_edge_cases.lib`
- `data/fixtures/liberty/timing_arcs.lib`
- `data/fixtures/liberty/tiny_combinational.lib`
- `data/fixtures/liberty/tiny_sequential.lib`

## Library Summary

| Library |
| --- |
| synthetic_multi_cell_combinational |
| synthetic_parser_edge_cases |
| synthetic_timing_arcs |
| tiny_synthetic_combinational |
| tiny_synthetic_sequential |

## Cell Inventory

| Library | Cell | Area | Family | Drive | Kind | Inputs | Outputs | Clocks | Other Pins | Timing Arcs |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | ---: |
| synthetic_multi_cell_combinational | INV_X1 | 1.2 | INV | X1 | combinational | A | Y |  |  | 0 |
| synthetic_multi_cell_combinational | NAND2_X1 | 1.85 | NAND2 | X1 | combinational | A;B | Y |  |  | 0 |
| synthetic_multi_cell_combinational | NOR2_X1 | 1.95 | NOR2 | X1 | combinational | A;B | Y |  |  | 0 |
| synthetic_parser_edge_cases | EDGE_BUF_X1 | 2.05 | EDGE_BUF | X1 | combinational | A | Y |  |  | 1 |
| synthetic_timing_arcs | NAND2_X1 | 1.85 | NAND2 | X1 | combinational | A;B | Y |  |  | 2 |
| tiny_synthetic_combinational | TINY_INV_X1 | 1.4 | TINY_INV | X1 | combinational | A | Y |  |  | 1 |
| tiny_synthetic_sequential | TINY_DFF_X1 | 4.8 | TINY_DFF | X1 | sequential | CLK;D | Q | CLK |  | 2 |

## Area Ranking

### Largest Cells

- `TINY_DFF_X1`
- `EDGE_BUF_X1`
- `NOR2_X1`
- `NAND2_X1`
- `NAND2_X1`

### Smallest Cells

- `INV_X1`
- `TINY_INV_X1`
- `NAND2_X1`
- `NAND2_X1`
- `NOR2_X1`

## Family Summary

| Family | Count |
| --- | ---: |
| EDGE_BUF | 1 |
| INV | 1 |
| NAND2 | 2 |
| NOR2 | 1 |
| TINY_DFF | 1 |
| TINY_INV | 1 |

## Cell Kind Summary

| Cell Kind | Count |
| --- | ---: |
| combinational | 6 |
| sequential | 1 |

## Limitations

- This report uses synthetic educational Liberty fixtures only.
- It does not contain or analyze real Sky130 Liberty files.
- Cell kind classification is conservative metadata labeling, not timing or functional proof.
- Timing arc counts are metadata counts only; no lookup-table exploration or static timing analysis is performed.
