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
- `check.json`: counts, hashes, and fail-closed validation results.

`topics.csv` contains search vocabulary only.  A lexical hit is never treated
as proof that two mathematical statements are equivalent.

Run

```text
python fga/mkmap.py PATH/TO/units.csv
```

with `units.csv` from the cited FGA source package.  This produces:

- `map.csv`: one controlled-disposition row for every FGA semantic unit;
- `ucand.csv`: ranked lexical candidates for units requiring comparison; and
- `mcheck.json`: source identity, coverage counts, hashes, and validation.

The generator is locked to the published 1,253-unit inventory.  It records no
private source path.  Its candidate rankings are triage aids only.

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
