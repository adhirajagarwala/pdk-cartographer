# Roadmap

`pdk-cartographer` grows from synthetic fixtures toward careful, read-only PDK exploration. Each milestone should leave behind tested code, honest documentation, and reproducible engineering notes. Project documentation lives under [docs/](docs/README.md).

## M1 - Repo Foundation and Liberty Fixtures

Establish repository guardrails, documentation, local development expectations, tiny synthetic Liberty fixtures, and a minimal fixture-subset parser. M1 is fixture-first and does not ingest Sky130.

## M2 - Liberty Parser Core

Implement a small handwritten Liberty subset parser that reads synthetic fixtures and extracts useful metadata such as libraries, library attributes, cells, pins, areas, pin capacitance, output functions, and minimal timing arc fields. M2 adds a lexer, generic group/attribute tree, typed models, parser diagnostics, expanded synthetic fixtures, and tests. It remains fixture-first and does not claim full Liberty compliance.

## M3 - Standard Cell Atlas

Build a standard-cell metadata atlas over parsed synthetic Liberty data. M3 summarizes cell inventory, area ranking, pin roles, output functions, family grouping, conservative combinational/sequential/unknown classification, and generated Markdown/CSV/JSON artifacts. It remains synthetic-fixture-only and does not claim real Sky130 ingestion or timing analysis.

## M4 - Timing Table Explorer

Extend Liberty handling toward fixture-backed timing-table structure. M4 parses tiny synthetic lookup-table templates and timing tables, summarizes table kinds, axes, dimensions, related pins, and arc metadata, and generates deterministic Markdown/CSV/JSON reports. It does not perform static timing analysis, interpolate values, or claim real Sky130 timing analysis.

## M5 - Real Sky130 Read-Only Ingestion

Add carefully scoped, read-only ingestion of real Sky130 Liberty files after the fixture parser, atlas layer, timing-table explorer, and docs are solid. Real PDK data should be treated as source material, not copied wholesale into the repository.

## M6 - PDK Atlas Reports and Portfolio Release

Produce polished reports and portfolio-ready documentation that connect PDK anatomy, Liberty metadata, parser output, and engineering limitations.

## Later Work

LEF exploration comes later, after Liberty parsing, atlas reporting, and real read-only Liberty ingestion are solid. DEF, GDS, OpenLane/OpenROAD integration, Docker-based flows, and silicon experiments are outside the initial Liberty-first roadmap.
