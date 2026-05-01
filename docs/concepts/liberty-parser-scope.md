# Liberty Parser Scope

M2 turns the first minimal Liberty reader into a small, documented parser core.
The parser is still fixture-first: it is designed around synthetic educational
fixtures in this repository, not around full production Liberty coverage.

## Architecture

The parser has three layers.

The lexer in `src/pdk_cartographer/liberty/lexer.py` converts Liberty-like text
into positioned tokens. It recognizes identifiers, quoted strings, numbers,
punctuation, line comments, block comments, and end-of-file. Tokens carry line
and column information so parser errors can point near the malformed input.

The generic parser in `src/pdk_cartographer/liberty/parser.py` consumes those
tokens and builds a group/attribute tree using the dataclasses in
`src/pdk_cartographer/liberty/ast.py`. A `LibertyGroup` stores its group name,
arguments, simple attributes, nested groups, and source location. This layer is
useful because Liberty is structurally group-oriented: `library`, `cell`, `pin`,
and `timing` all follow the same broad pattern.

The typed extraction layer converts the generic tree into model dataclasses in
`src/pdk_cartographer/liberty/models.py`. M2 extracts `Library`, `Cell`, `Pin`,
and `TimingArc` objects with dictionaries for name-indexed lookup and preserved
simple attributes for atlas work. M4 extends those models with
`LookupTableTemplate` and `TimingTable` records for the timing-table fixtures.

M3 consumes those typed models in `src/pdk_cartographer/atlas/` to build
deterministic cell records, library summaries, and Markdown/CSV/JSON artifacts
from the synthetic M3 fixtures. M4 consumes the extended timing-table models in
`src/pdk_cartographer/timing/` to build structural timing-table summaries.

## Supported Subset

The parser supports enough Liberty-like syntax for the repository fixtures:

- `library(name) { ... }`
- nested `cell(name)`, `pin(name)`, and minimal `timing()` groups
- simple scalar attributes using `name : value;`
- quoted string values
- numeric values
- identifier values
- simple comma-separated values where fixtures need them
- complex attributes such as `index_1("...");` and `values("...", "...");`
- `lu_table_template` groups in the M4 fixtures
- timing-table groups under `timing()` for the M4 fixtures
- line comments beginning with `//`
- block comments using `/* ... */`
- whitespace between tokens

The typed model extraction currently captures:

- library name
- simple library-level attributes
- cell names
- cell area
- simple cell attributes
- pin names
- pin direction
- pin function
- pin capacitance
- simple pin attributes
- minimal timing arc fields: `related_pin`, `timing_sense`, and `timing_type`
- lookup-table template names, axis variables, and numeric axes
- timing-table kind, template reference, resolved axes, and values matrix

## Intentionally Unsupported

M4 parses a small timing-table subset for synthetic fixtures, including
`cell_rise`, `cell_fall`, `rise_transition`, and `fall_transition`. It does not
interpret timing surfaces, do interpolation, plot timing data, or perform static
timing analysis.

The parser also does not support full Liberty grammar coverage. Unsupported
areas include bus syntax, escaped identifiers beyond the current tiny subset,
conditional timing expressions, includes, production-scale syntax recovery,
power tables, and broader standard-cell characterization semantics.

This parser is not Liberty-complete and should not be described as a compliant
Liberty parser. It is a tested educational subset parser.

## Milestone Boundaries

Real Sky130 ingestion is deferred to M5, after the fixture parser, atlas model,
timing-table explorer, and reports have stronger boundaries.

LEF, DEF, and GDS are out of scope for the current Liberty-first milestones.
LEF exploration should wait until the Liberty-side model and reporting work are
solid.
