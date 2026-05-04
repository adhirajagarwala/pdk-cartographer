# Real PDK Read-Only Ingestion

M5 is the first milestone that points `pdk-cartographer` at a real external
Sky130 PDK installation. The important boundary is that the PDK remains source
material outside the repository. The project discovers file layout, records
small metadata summaries, and probes parser compatibility without copying raw
PDK files.

## External Root Strategy

The preferred environment variable is:

```bash
export PDK_CARTOGRAPHER_PDK_ROOT="$HOME/pdks/ciel"
```

If that variable is not set, the discovery helpers fall back to `PDK_ROOT`.
This keeps machine-specific paths out of source code and generated artifacts.

The M5 scripts support roots that directly point at `sky130A` or `sky130B`, and
roots that contain those variants deeper inside a Ciel-style directory tree.
Discovery is bounded so the project does not scan the full filesystem.

## Why Raw PDK Files Stay Out Of Git

Real PDKs are large source distributions with licensing, provenance, and
versioning concerns. Committing raw Liberty, LEF, GDS, SPICE, or database files
would make the repository noisy and harder to review. It would also blur the
line between this project's code and upstream PDK source material.

M5 commits only small generated summaries:

- discovered Liberty file paths relative to the configured PDK root
- file sizes
- inferred Sky130 variant names
- inferred standard-cell family names
- inferred corner names
- the selected parser-probe subset
- compact parser compatibility results

Generated summaries are reviewable project artifacts. Raw PDK source files are
not.

## Selected Real Liberty Subset

The first real target subset is intentionally small:

- prefer `sky130A`
- prefer `sky130_fd_sc_hd`
- include one typical-like corner when present
- include one fast-like corner when obvious
- include one slow-like corner when obvious
- cap the subset at three Liberty files

For the current Ciel Sky130 install, this selects one TT file plus one FF and
one SS file from `sky130_fd_sc_hd`. This is enough to test the M2-M4 parser
against real Liberty syntax while keeping M5 bounded.

## Parser Compatibility Boundary

The parser remains a fixture-first educational Liberty subset parser. M5 uses
real Liberty files to answer a narrower question: can the current parser read
the selected files well enough to report library name, cell count, and timing
table count?

That is not full Liberty compliance. It is not static timing analysis. It is
not timing interpolation. It is not production timing signoff.

Compatibility failures should be recorded honestly with compact diagnostics.
Large parser rewrites belong in a separately scoped milestone if the selected
files expose unsupported syntax that cannot be handled safely.

## M6 Handoff

M6 should use the M5 manifest and compatibility report as its baseline. Good
next steps are broader report polish, clearer corner comparison, and better
portfolio-facing explanation of what Liberty metadata contains. Raw PDK files
should remain external.
