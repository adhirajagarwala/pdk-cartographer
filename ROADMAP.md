# Roadmap

`pdk-cartographer` grows from synthetic fixtures toward careful, read-only PDK exploration. Each milestone should leave behind tested code, honest documentation, and reproducible engineering notes. M1 documentation lives under [docs/](docs/README.md).

## M1 - Repo Foundation and Liberty Fixtures

Establish repository guardrails, documentation, local development expectations, tiny synthetic Liberty fixtures, and a minimal fixture-subset parser. M1 is fixture-first and does not ingest Sky130.

## M2 - Liberty Parser Core

Implement a small handwritten Liberty subset parser that reads the M1 fixtures and extracts useful metadata such as libraries, cells, pins, areas, and minimal timing arc fields. The parser should document what it does not support.

## M3 - Standard Cell Atlas

Build a standard-cell metadata view over parsed Liberty data. Focus on names, areas, pin roles, simple boolean functions, and readable summaries that help explain how a cell library is organized.

## M4 - Timing Table Explorer

Extend Liberty handling toward timing-table structure and corner-aware metadata. This milestone can inspect timing tables, but must remain clear about educational analysis versus signoff timing.

## M5 - Real Sky130 Read-Only Ingestion

Add carefully scoped, read-only ingestion of real Sky130 Liberty files after the fixture parser and docs are solid. Real PDK data should be treated as source material, not copied wholesale into the repository.

## M6 - PDK Atlas Reports and Portfolio Release

Produce polished reports and portfolio-ready documentation that connect PDK anatomy, Liberty metadata, parser output, and engineering limitations.

## Later Work

LEF exploration comes later, after Liberty work is solid. DEF, GDS, OpenLane/OpenROAD integration, Docker-based flows, and silicon experiments are outside the initial Liberty-first roadmap.
