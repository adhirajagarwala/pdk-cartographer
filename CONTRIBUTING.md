# Contributing

`pdk-cartographer` is a fixture-first EE/semiconductor portfolio project. Contributions should keep the repository technically honest, small enough to review, and clear about the difference between synthetic educational fixtures and real PDK data.

## Local Setup

M1 uses standard Python tooling only:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

Development dependencies will be installed with `pip` once `pyproject.toml` is added. Do not introduce uv or Poetry in M1.

## Quality Checks

Expected local checks once the package skeleton exists:

```bash
pytest
ruff check .
mypy src
```

## Scope Discipline

- Keep M1 fixture-first.
- Do not download or commit full Sky130 files in M1.
- Do not add OpenLane, OpenROAD, Docker, LEF/DEF/GDS parsing, timing plots, or a package CLI in M1.
- Keep docs serious and portfolio-focused.
- Ask before scope expansion, commits, tags, GitHub remotes, or Linear changes.
