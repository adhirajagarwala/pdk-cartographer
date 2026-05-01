# AGENTS.md

## Project Identity

This repository is `pdk-cartographer`, not CurveCraft.

`pdk-cartographer` is a fixture-first Sky130 PDK exploration project focused on Liberty timing, standard-cell metadata, PDK anatomy, and reproducible engineering reports. CurveCraft is complete through M4 and must not be modified from this repository's work.

## Git Identity — Non-Negotiable

Every commit and push in this repo must be authored as:
  Name:  Adhiraj Agarwala
  Email: adhirajagarwala2007@gmail.com

Before the first commit in any session, run:
  git config user.name "Adhiraj Agarwala"
  git config user.email "adhirajagarwala2007@gmail.com"

Before every commit, verify:
  git config user.name
  git config user.email

Rules:
- Never commit unless git config user.name is exactly Adhiraj Agarwala.
- Never commit unless git config user.email is exactly adhirajagarwala2007@gmail.com.
- Never add Co-Authored-By lines.
- Never add Signed-off-by lines.
- Never add AI/tool/assistant contributor metadata.
- The commit author must be always and only Adhiraj Agarwala.
- If the git identity is wrong, stop and fix it before committing.
- If a commit was already created with the wrong identity, stop and report it. Do not rewrite history unless explicitly approved.

## M1 Scope

M1 is the foundation phase. Keep the work small, inspectable, and reversible.

Allowed M1 scope:
- Repository guardrails and portfolio-facing documentation.
- Python 3.11+ project structure using `src/pdk_cartographer`.
- Standard `venv` plus `pip` setup only.
- Tiny synthetic Liberty fixtures for educational parser development.
- A minimal handwritten parser for those fixtures only.
- Tests, ruff, and mypy configuration.
- Engineering logs and foundation reports.

## Explicit M1 Exclusions

Do not add, install, or create:
- Full Sky130 downloads or copied Sky130 files.
- OpenLane, OpenROAD, Docker, or external PDK toolchains.
- LEF, DEF, or GDS parsing.
- Timing plots, ring oscillator experiments, or silicon experiment claims.
- `silicon-dossier`, `register-city`, or other roadmap projects.
- A package CLI.
- Fake README badges.
- GitHub remotes.
- Commits or tags without explicit owner approval.
- Linear changes unless explicitly instructed.

## Milestone Merge Workflow

- Do not use GitHub PRs for milestone merges.
- Do not use GitHub web merges or GitHub API merges.
- Use local fast-forward merges only.
- Push main directly only after local validation passes.
- Never create merge commits.

## Python Quality Expectations

- Use Python 3.11+.
- Use `src/pdk_cartographer` as the package import path.
- Use standard `venv` and `pip` only for M1.
- Do not introduce uv or Poetry in M1.
- Keep pytest, ruff, and mypy passing once tooling exists.
- Prefer typed dataclasses or simple typed result objects for parsed metadata.
- Keep IO, parsing, fixtures, docs, and tests separated.

## Collaboration Rules

- Keep docs serious, technically honest, and portfolio-focused.
- Make small, clean, reversible choices when details are minor.
- Ask before material changes, especially scope expansion, commits, tags, remotes, or Linear edits.
- Do not modify CurveCraft and do not copy CurveCraft implementation code.
- Do not create `pdk-cartographer` inside CurveCraft.
