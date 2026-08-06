# Historical-source mapping tools

These tools adapt the validated FGA conversion method for FAC, Tôhoku, and
GAGA without changing the FGA dossier.

- `intake.py` converts a frozen source scaffold to one common unit schema.
- `scan.py` indexes the current Stacks TeX tree and creates topic candidates.
- `map.py` applies append-only human decisions and validates complete unit
  coverage, source issues, labels, tags, and privacy.

Lexical candidates are triage only. A source unit receives an existing tag
only by joining a reviewed Stacks label that already has that tag. New source
text never assigns a tag.

Each integration checkpoint must validate, build the affected chapter
serially, inspect the changed pages, commit, push, fetch the remote branch, and
prove commit/tree/blob equality.
