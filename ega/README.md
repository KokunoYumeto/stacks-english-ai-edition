# EGA discovery and integration scaffold

This branch is a public, machine-readable working scaffold for comparing
*Éléments de géométrie algébrique* (EGA 0--IV) with the current Stacks
Project. It is **not** a claim that EGA has been fully rewritten in Stacks
form, accepted upstream, or formally verified.

The complete standalone English EGA source is admitted only as discovery
text. Canonical source claims remain gated by the separately maintained
diplomatic French edition and its page-level authority receipts. The edition
trees are read-only inputs to this branch and are never copied, edited, built,
or published here.

## Current snapshot

- Stacks upstream base: `a04446e57ec1fbc252a871afcec7752fb2807b14`.
- English discovery manifest: R172, 88,062 bytes, SHA-256
  `01D0226BD1A31B14A250C29C18F3DBAE0C7537B245AB1C119422EBBEAF0C133E`;
  127 files, 7,283,317 bytes, tree SHA-256
  `F5EBDCAAA7C5B4A426085B1C696E821B2F74B9E5E58582664955AD37E8C2BC59`.
- French authority: production is active; the current interface snapshot has
  EGA II printed p.9 sealed locally and printed p.10 as the next cursor.
- Existing incremental pre-Stacks notes: 340,356 bytes, SHA-256
  `8C4E31D85658F6A8D82A809FB7FC4D6B89B7A02B9F9FBF5B7C0480FDD32D78FF`.
  They are evidence to normalize into the new schema, not a completed
  deliverable or an upstream mapping.
- Verified discovery inventory: 127 exact source files and 9,155
  metadata-only semantic units. No source prose is copied into the branch.
- Current Stacks snapshot: 21,446 chapter labels, 21,437 exact official-tag
  joins, and 2,670 lexical candidates across all 35 discovery topics. Reviewed
  mappings remain exactly zero at this scaffold stage.

## State model

Every source unit and topic advances independently through:

`discovery` -> `candidate` -> `reviewed_existing` or `reviewed_gap` ->
`integrated_local` -> `built` -> `remote_checkpoint` ->
`upstream_feedback` -> `upstream_accepted`.

No state is inferred from a successful build alone. No new label is an
official Stacks tag unless upstream assigns it. Historical source defects,
English corrections, mapping reversals, and maintainer feedback are recorded
append-only.

## Files

- `scope.json`: exact claims, exclusions, inputs, and upstream base.
- `src.csv`: source surfaces and authority state.
- `topics.csv`: corpus-wide discovery topics; initially unreviewed.
- `dec.csv`: append-only mapping and policy decisions.
- `issues.csv`: source, mathematical, and integration issues.
- `fb.csv`: upstream feedback and its disposition.
- `schema.md`: stable IDs, evidence rules, and promotion gates.
- `check.py`: local structural validator.
- `intake.py`: deterministic manifest verification and metadata-only unit
  extraction; it does not copy source prose.
- `files.csv`, `units.csv`, and `intake.json`: generated exact-file inventory,
  stable unit registry, and fail-closed intake receipt.
- `map.py`, `cand.csv`, and `map.json`: lexical candidate generation against
  the exact upstream Stacks snapshot. Candidates are not reviewed mappings.

The immediate work is corpus-wide source-unit extraction and topic
classification. Mathematical Stacks chapter edits begin only after a bounded
unit has direct evidence and an explicit reviewed disposition.
