# M3 Standard Cell Atlas Report

## Objective

M3 adds a Standard Cell Atlas layer to `pdk-cartographer`. The atlas converts
parsed synthetic Liberty fixture data into deterministic engineering artifacts:
a Markdown report, a CSV cell inventory, and a JSON library summary.

This is not a real Sky130 analysis report. No real Sky130 Liberty files were
downloaded, copied, or ingested. The atlas is a fixture-backed metadata report,
not a full PDK characterization flow.

## Starting Point From M2

M2 delivered a fixture-first Liberty parser core. It tokenizes Liberty-like
text, builds a generic group/attribute tree, and extracts typed `Library`,
`Cell`, `Pin`, and `TimingArc` objects. Those typed objects preserve enough
metadata for an atlas: library names, cell names, area, pin direction, pin
function, pin capacitance, and minimal timing arc fields.

M3 keeps the parser boundary intact. It does not add new Liberty grammar
coverage for timing lookup tables, real PDK syntax, or physical layout formats.

## Atlas Architecture

The M3 atlas package has four responsibilities:

- `models.py` defines atlas-facing dataclasses.
- `classify.py` provides conservative metadata classification helpers.
- `summarize.py` converts parsed Liberty libraries into deterministic cell
  records and aggregate summary statistics.
- `render.py` emits Markdown, CSV, and JSON artifacts using only the Python
  standard library.

The repo-local generator script, `scripts/generate_fixture_atlas.py`, parses
every `.lib` file under `data/fixtures/liberty`, builds a `StandardCellAtlas`,
and writes the generated artifacts to stable paths.

## Cell Record Model

Each `CellRecord` captures:

- library name
- cell name
- area, when available
- family
- drive strength, when a simple suffix is present
- cell kind
- input pins
- output pins
- clock-like pins
- other pins
- output function strings
- pin capacitance values
- timing arc count

The records are sorted by library name and cell name for deterministic tests
and reproducible reports.

## Classification Rules

The classification layer is intentionally conservative:

- Family extraction removes generic drive suffixes such as `_X1`, `_X2`, or
  `_X16`.
- Drive strength extraction reports suffixes such as `X1` when present.
- Clock-like pins are limited to generic names such as `CLK`, `CK`, and
  `clock`.
- Sequential cells are identified by clock-like pins or generic name markers
  such as `DFF` and `LATCH`.
- Combinational cells require output function metadata and no sequential
  indicator.
- Cells without enough metadata are classified as `unknown`.

These rules are report organization rules. They are not real Sky130 naming
rules, not formal functional verification, and not timing validation.

## Fixture Suite

M3 uses the synthetic fixtures already present in the repository:

- `multi_cell_combinational.lib`
- `parser_edge_cases.lib`
- `timing_arcs.lib`
- `tiny_combinational.lib`
- `tiny_sequential.lib`

The fixtures exercise multiple cells, simple areas, pin directions, output
functions, capacitance values, clock-like pins, preserved attributes, and
minimal timing arc metadata. They are educational examples and are not copied
from Sky130 or any real PDK.

## Generated Artifacts

The generator writes:

- `docs/reports/generated/m3-fixture-standard-cell-atlas.md`
- `data/derived/m3_standard_cell_atlas/fixture_cell_inventory.csv`
- `data/derived/m3_standard_cell_atlas/fixture_library_summary.json`

The generated Markdown report includes overview, source fixtures, library
summary, cell inventory, area ranking, family summary, cell-kind summary, and
limitations. The CSV provides one row per cell record. The JSON stores summary
metadata and source fixture paths.

Each generated artifact path is deterministic. The Markdown and JSON outputs
explicitly state that the atlas is generated from synthetic educational Liberty
fixtures, not real Sky130 data.

## Tests and Quality Gates

M3 expands the test suite across atlas classification, summarization,
rendering, and artifact generation behavior. The tests cover:

- family extraction and drive strength extraction
- combinational, sequential, and unknown classification
- clock-like pin detection
- all synthetic fixtures
- deterministic ordering
- area min, max, mean, largest cells, and smallest cells
- family counts and cell-kind counts
- pin categories, pin counts, and timing arc counts
- Markdown section coverage and synthetic-data wording
- stable CSV headers and one row per cell
- JSON summary metadata
- deterministic render outputs
- equivalent generation path for the documented artifacts

The validation gate is:

```bash
python scripts/generate_fixture_atlas.py
python -m pytest
ruff check .
mypy src
```

At the time this report was written, the M3 implementation had 56 passing
pytest tests, ruff passing, and mypy passing.

## Limitations

M3 does not ingest real Sky130 files. It does not claim full Liberty grammar
support, full standard-cell characterization, timing analysis, timing-table
interpretation, or physical layout analysis.

The atlas reports fixture metadata. Area values are synthetic educational
values. Timing arc counts are counts of parsed metadata groups, not timing
analysis. Cell-kind classification is conservative labeling for report
organization.

LEF, DEF, and GDS parsing remain out of scope. OpenLane, OpenROAD, Docker, and
package CLI work are also outside M3.

## M4 Handoff

M4 is the Timing Table Explorer. It should add fixture-backed work around
timing-table structure while keeping the same honesty boundary: educational
metadata exploration is not signoff timing and not real Sky130 analysis. Real
Sky130 read-only ingestion remains deferred to M5.
