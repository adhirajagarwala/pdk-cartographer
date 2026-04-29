# Standard Cell Atlas

The M3 Standard Cell Atlas is the report layer built on top of the M2 Liberty
parser. In this project, an atlas is a deterministic summary of parsed
standard-cell metadata: which cells exist, how large they are in the fixture
data, what pins they expose, which broad family each name belongs to, and
whether the available metadata suggests combinational, sequential, or unknown
cell behavior.

M3 is synthetic-fixture-only. It does not ingest real Sky130 Liberty files and
does not claim full Sky130 analysis. Real Sky130 read-only ingestion is deferred
to M5. LEF, DEF, and GDS remain out of scope for this milestone.

## From Liberty Models to Cell Records

The M2 parser converts each synthetic Liberty file into a typed `Library`
object containing `Cell`, `Pin`, and `TimingArc` records. The atlas layer reads
those typed objects and produces one `CellRecord` per parsed cell.

Each record preserves:

- source library name
- cell name
- area, when present
- extracted family name
- extracted drive-strength suffix, when present
- conservative cell kind
- input, output, clock-like, and other pin names
- output function strings
- pin capacitance values
- timing arc count

The atlas does not interpret timing lookup tables, does not run static timing
analysis, and does not infer physical layout properties.

## Area Ranking

Area ranking sorts cells with available area metadata to show the largest and
smallest cells in the synthetic fixture set. The area values are educational
fixture values only. They should be read as examples of how an atlas can rank
cell metadata, not as Sky130 measurements.

## Pin Summaries

Pin summaries group pins by simple Liberty direction and conservative
clock-like naming:

- input pins come from `direction : input`
- output pins come from `direction : output`
- clock-like pins are names such as `CLK`, `CK`, or `clock`
- other pins preserve anything outside those categories

These categories are intended for readable inventory reports. They are not a
replacement for full Liberty semantic analysis.

## Family Grouping and Drive Strength

The family helper removes simple generic drive suffixes such as `_X1`, `_X2`,
or `_X16`. For example, `NAND2_X1` becomes family `NAND2` with drive strength
`X1`.

The rule is deliberately generic. It does not encode Sky130-specific naming
conventions, voltage variants, threshold variants, or process library
subfamilies.

## Cell-Kind Classification

Classification is conservative:

- `sequential` is used when a cell name contains generic markers such as `DFF`
  or `LATCH`, or when the cell has clock-like pins such as `CLK`, `CK`, or
  `clock`.
- `combinational` is used only when an output function is present and no
  sequential indicator is found.
- `unknown` is used when the fixture metadata is insufficient.

This classification is useful for organizing reports. It is not proof of real
cell behavior, not a formal functional model, and not timing validation.

## Milestone Boundary

M3 stops at a fixture-generated atlas with Markdown, CSV, and JSON artifacts.
M4 is the Timing Table Explorer milestone. M5 is the first milestone intended
to approach real Sky130 Liberty ingestion, and even there the intended mode is
read-only source handling rather than copying real PDK files into this
repository.
