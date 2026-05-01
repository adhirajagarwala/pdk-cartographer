# Timing Table Explorer

Liberty timing tables describe how a timing quantity changes across a small grid
of operating points. In common cell-library characterization, one axis is input
slew and another axis is output load. A timing tool can use those tables as part
of timing analysis, but M4 only parses and reports their structure.

## Lookup-Table Templates

A `lu_table_template` group names the shape of a reusable table. It can define
which physical ideas the axes represent and which numeric index points belong to
each axis.

The M4 synthetic fixtures use a narrow two-axis subset:

- `variable_1 : input_net_transition;`
- `variable_2 : total_output_net_capacitance;`
- `index_1("...");`
- `index_2("...");`

In these fixtures, `index_1` represents input transition or slew points, and
`index_2` represents output capacitance or load points. The values are tiny
educational numbers, not characterized Sky130 data.

## Timing Tables

Timing tables live under a `timing()` group on a pin. The timing group can name
the related input pin and describe arc metadata such as `timing_type` and
`timing_sense`. The table groups then attach numerical surfaces to that arc.

M4 handles four table kinds:

- `cell_rise`: output rising delay values.
- `cell_fall`: output falling delay values.
- `rise_transition`: output rising transition values.
- `fall_transition`: output falling transition values.

The parser reads the table kind, optional template reference, resolved axis
indices, and the rectangular values matrix. The explorer summarizes table
counts, dimensions, related pins, arc metadata, axis names, and structural
minimum/maximum values.

## M4 Boundary

M4 is synthetic-fixture-only. It does not ingest real Sky130 Liberty files and
does not claim real Sky130 timing analysis.

M4 does not perform static timing analysis, interpolate between table points,
plot timing data, or parse full Liberty. It is a deliberately small extension of
the M2 parser so the project can explain lookup-table structure before touching
real PDK data.

Real Sky130 read-only Liberty ingestion is deferred to M5. LEF, DEF, and GDS
remain out of scope.
