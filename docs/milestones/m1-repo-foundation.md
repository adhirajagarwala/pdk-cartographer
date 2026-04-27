# M1 Repo Foundation and Liberty Fixtures

M1 establishes `pdk-cartographer` as a clean, fixture-first repository. The milestone is about guardrails, structure, tiny synthetic Liberty examples, a minimal parser surface, and serious documentation.

## Scope

- Repository bootstrap files and durable project instructions.
- Python 3.11+ `src/pdk_cartographer` package layout.
- Standard `venv` plus `pip` workflow.
- pytest, ruff, and mypy quality gates.
- Tiny synthetic Liberty fixtures for combinational and sequential-looking cells.
- A handwritten parser for the fixture subset only.
- Concept documentation, engineering log, and foundation report.

## Exclusions

M1 does not include Sky130 downloads, copied Sky130 Liberty files, OpenLane, OpenROAD, Docker, LEF/DEF/GDS parsing, timing plots, ring oscillator experiments, package CLI work, GitHub remote creation, commits, or tags without explicit approval.

The parser is not Liberty-complete. It intentionally does not parse lookup tables, real timing surfaces, buses, includes, conditional timing expressions, or full grammar edge cases.

## Acceptance Criteria

- The repository has clear guardrails and no accidental dependency on CurveCraft.
- `pyproject.toml` supports editable installation with `python -m pip install -e ".[dev]"`.
- The package imports as `pdk_cartographer`.
- Synthetic Liberty fixtures are small, understandable, and explicitly marked as not copied from Sky130.
- Parser dataclasses and tests cover library, cell, area, pin, and minimal timing arc metadata.
- Documentation explains the fixture-first approach and defers real PDK ingestion.
- `python -m pytest`, `ruff check .`, and `mypy src` pass locally.

## Handoff to M2

M2 should deepen the Liberty parser core while preserving the M1 boundary: small, tested, documented parsing behavior before real Sky130 files. The next useful step is to make parser errors clearer and broaden supported scalar syntax only when tests require it.
