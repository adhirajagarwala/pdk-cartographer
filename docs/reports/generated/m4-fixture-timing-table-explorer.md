# M4 Fixture Timing Table Explorer

This report is generated from synthetic educational Liberty fixtures, not real Sky130 data.

## Overview

- Libraries: 3
- Cells: 4
- Timing tables: 12

## Source Fixtures

- `data/fixtures/liberty/multi_cell_combinational.lib`
- `data/fixtures/liberty/parser_edge_cases.lib`
- `data/fixtures/liberty/timing_arcs.lib`
- `data/fixtures/liberty/timing_table_2x2.lib`
- `data/fixtures/liberty/timing_table_3x3.lib`
- `data/fixtures/liberty/timing_table_edge_cases.lib`
- `data/fixtures/liberty/tiny_combinational.lib`
- `data/fixtures/liberty/tiny_sequential.lib`

## Timing Table Inventory

| Library | Cell | Pin | Related Pin | Type | Sense | Table | Template | Axis 1 | Axis 2 | Rows | Columns | Min | Max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| synthetic_timing_table_2x2 | INV_X1 | Y | A | combinational | negative_unate | cell_fall | timing_2x2 | input_net_transition | total_output_net_capacitance | 2 | 2 | 0.01 | 0.037 |
| synthetic_timing_table_2x2 | INV_X1 | Y | A | combinational | negative_unate | cell_rise | timing_2x2 | input_net_transition | total_output_net_capacitance | 2 | 2 | 0.012 | 0.041 |
| synthetic_timing_table_2x2 | INV_X1 | Y | A | combinational | negative_unate | fall_transition | timing_2x2 | input_net_transition | total_output_net_capacitance | 2 | 2 | 0.005 | 0.018 |
| synthetic_timing_table_2x2 | INV_X1 | Y | A | combinational | negative_unate | rise_transition | timing_2x2 | input_net_transition | total_output_net_capacitance | 2 | 2 | 0.006 | 0.02 |
| synthetic_timing_table_3x3 | NAND2_X1 | Y | A | combinational | negative_unate | cell_fall | timing_3x3 | input_net_transition | total_output_net_capacitance | 3 | 3 | 0.014 | 0.071 |
| synthetic_timing_table_3x3 | NAND2_X1 | Y | A | combinational | negative_unate | cell_rise | timing_3x3 | input_net_transition | total_output_net_capacitance | 3 | 3 | 0.018 | 0.083 |
| synthetic_timing_table_3x3 | NAND2_X1 | Y | A | combinational | negative_unate | fall_transition | timing_3x3 | input_net_transition | total_output_net_capacitance | 3 | 3 | 0.007 | 0.039 |
| synthetic_timing_table_3x3 | NAND2_X1 | Y | A | combinational | negative_unate | rise_transition | timing_3x3 | input_net_transition | total_output_net_capacitance | 3 | 3 | 0.008 | 0.043 |
| synthetic_timing_table_3x3 | NAND2_X1 | Y | B | combinational | negative_unate | cell_fall | timing_3x3 | input_net_transition | total_output_net_capacitance | 3 | 3 | 0.015 | 0.074 |
| synthetic_timing_table_3x3 | NAND2_X1 | Y | B | combinational | negative_unate | cell_rise | timing_3x3 | input_net_transition | total_output_net_capacitance | 3 | 3 | 0.019 | 0.086 |
| synthetic_timing_table_edge_cases | BUF_X2 | Y | A | combinational | positive_unate | cell_rise | edge_template | input_net_transition | total_output_net_capacitance | 2 | 2 | 0.011 | 0.044 |
| synthetic_timing_table_edge_cases | DFF_X1 | Q | CLK | rising_edge |  | cell_rise | edge_template | input_net_transition | total_output_net_capacitance | 2 | 2 | 0.032 | 0.09 |

## Table Kind Summary

| Table Kind | Count |
| --- | ---: |
| cell_fall | 3 |
| cell_rise | 5 |
| fall_transition | 2 |
| rise_transition | 2 |

## Axis and Dimension Summary

| Dimension | Count |
| --- | ---: |
| 2x2 | 6 |
| 3x3 | 6 |

## Timing Arc Summary

### Timing Types

| Timing Type | Count |
| --- | ---: |
| combinational | 11 |
| rising_edge | 1 |

### Timing Senses

| Timing Sense | Count |
| --- | ---: |
| negative_unate | 10 |
| positive_unate | 1 |

## What This Does Not Do

- M4 does not perform static timing analysis.
- M4 does not interpolate timing values.
- M4 does not model physical layout, routing, parasitics, or signoff timing.

## Limitations

- This report uses synthetic educational Liberty fixtures only.
- It does not contain or analyze real Sky130 Liberty files.
- Values are reported as table-shape metadata, not validated delays.
- Only the small fixture-backed timing-table subset is supported.
