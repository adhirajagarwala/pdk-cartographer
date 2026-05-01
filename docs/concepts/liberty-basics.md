# Liberty Basics

Liberty files describe cell-library information used by digital implementation and timing tools. A Liberty file does not contain transistor layout. Instead, it gives tool-readable metadata about standard cells: what cells exist, what pins they expose, how pins behave logically, and how timing depends on load, slew, and operating conditions.

## Core Structure

A `library` group names a cell library and usually contains units, default settings, operating conditions, lookup table templates, and many `cell` groups.

A `cell` group describes one standard cell variant, such as an inverter or flip-flop. Common cell metadata includes `area`, leakage or power information, and one or more `pin` groups.

A `pin` group describes an input, output, clock, or other port. Useful scalar attributes include:

- `direction`: whether the pin is an input, output, inout, or internal role.
- `function`: a Boolean expression for output pins when the cell behavior can be described simply.
- `capacitance`: the input capacitance seen by upstream drivers.

## Timing Arcs

Timing arcs describe timing relationships between pins. For example, an inverter output can have an arc related to its input with `timing_sense : negative_unate`. A sequential cell can have clock-to-output arcs, setup/hold checks, and other timing relationships.

M2 captures only a minimal arc shape: `related_pin`, `timing_sense`, and `timing_type` when present. That is enough to teach where timing metadata lives without pretending to implement static timing analysis.

## Lookup Tables

Production Liberty timing data often uses lookup tables indexed by input transition, output load, voltage, temperature, or other variables. These tables provide numerical timing and power values that production timing tools can use as part of timing analysis.

M4 parses a small synthetic timing-table subset: lookup-table templates, `index_1`, `index_2`, `values`, and the `cell_rise`, `cell_fall`, `rise_transition`, and `fall_transition` table groups used by the fixtures. It reports table shape and metadata only. It does not interpolate values or perform static timing analysis.

For the exact parser boundary, see [Liberty Parser Scope](liberty-parser-scope.md).
