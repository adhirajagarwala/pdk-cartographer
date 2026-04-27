# Documentation

This documentation records how `pdk-cartographer` is being built as a serious student EDA/PDK exploration toolkit. The project starts with synthetic Liberty fixtures so the code can be tested and explained before any real Sky130 ingestion is attempted.

## Concept Notes

- [PDK Anatomy](concepts/pdk-anatomy.md) explains the major kinds of files that make up a process design kit and where Liberty fits.
- [Liberty Basics](concepts/liberty-basics.md) describes libraries, cells, pins, scalar metadata, timing arcs, and timing tables at a high level.
- [Standard Cells](concepts/standard-cells.md) explains cell-level metadata such as area, pins, combinational behavior, sequential behavior, and naming conventions.
- [Timing Corners](concepts/timing-corners.md) explains process, voltage, and temperature corners and why timing changes across them.

## M1 Records

- [M1 Repo Foundation](milestones/m1-repo-foundation.md) defines the scope, exclusions, acceptance criteria, and M2 handoff.
- [2026-04-27 M1 Kickoff Log](logs/2026-04-27-m1-kickoff.md) records the first project decisions.
- [M1 Foundation Report](reports/m1-foundation-report.md) summarizes the foundation state and parser scope.

## Roadmap

The top-level [ROADMAP.md](../ROADMAP.md) tracks the milestone sequence from synthetic fixtures toward later read-only Sky130 Liberty ingestion.
