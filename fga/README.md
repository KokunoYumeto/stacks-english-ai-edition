# FGA integration record

This directory records the conversion of the eight FGA exposés, their eight
item-linked errata, and the 1962 comments into the conventions and dependency
structure of the Stacks Project.

The source edition is the independently produced FGA corpus published at
<https://doi.org/10.5281/zenodo.21802810>.  No French source prose is copied
here.  New mathematical prose intended for the Stacks Project will be written
independently in English and will follow `coding.tex` and
`documentation/rules`.

The files in this directory are an integration dossier on the working branch.
They are not official Stacks tags and do not assert that upstream has accepted
any proposed text.

## Generated index

Run

```text
python fga/mkidx.py
```

from the repository root.  The script produces:

- `stx.csv`: every labelled object in the current TeX tree, joined to its
  existing official tag when one exists;
- `tcand.csv`: bounded lexical candidates for each FGA topic; and
- `tmap.csv`: reviewed topic-level scope decisions joined to exact labels and
  tags; and
- `check.json`: counts, hashes, and fail-closed validation results.

`topics.csv` contains search vocabulary and the human-reviewed topic scope.
A lexical hit or topic-level decision is never treated as proof that two
mathematical statements are equivalent.

Run

```text
python fga/mkmap.py PATH/TO/units.csv PATH/TO/terms.csv
```

with `units.csv` and `terms.csv` from the cited FGA source package.  This
produces:

- `map.csv`: one controlled-disposition row for every FGA semantic unit;
- `ucand.csv`: ranked lexical candidates for units requiring comparison; and
- `mcheck.json`: source identity, coverage counts, hashes, and validation.

The generator is locked to the published 1,253-unit inventory and 1,612 topic
links.  It records no private source path.  Topic evidence and candidate
rankings are triage aids only.

Validation records the exact `origin/master` commit as the upstream baseline
and hashes every indexed TeX file.  It does not record the moving branch HEAD
as a source identity because doing so would make a generated manifest stale as
soon as that manifest itself was committed.

## Semantic dispositions

The unit-level crosswalk uses the following controlled dispositions:

- `existing_equivalent`
- `existing_stronger`
- `existing_weaker`
- `extend_existing`
- `new_statement`
- `new_section`
- `example_or_remark`
- `historical_reference`
- `outside_scope`
- `structural_only`
- `needs_review`

Every non-structural FGA unit must ultimately have source evidence, a Stacks
label or an explicit residual, a rationale, and a review state.  Generated
candidates remain `needs_review` until the underlying mathematics has been
compared.

Human decisions are append-only in `dec.csv`.  A later correction uses a new
`replace` row naming the exact earlier decision in `supersedes`; the generator
rejects silent replacement, unknown Stacks labels, and duplicate decision IDs.

Source claims whose exact hypotheses are open or demonstrably too broad are
recorded in `issues.csv`.  The validator checks each issue ID, FGA unit,
current Stacks evidence label, status, and corrective control.  This keeps a
source problem distinct from a missing Stacks result and prevents a historical
claim from being imported silently.
