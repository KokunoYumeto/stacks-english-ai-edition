# Deterministic replay

Use the exact source tree bound by `authority/upstream.lock.json`. Both frozen
source files must reproduce the hashes in `verify.py` before applying payloads.

Run:

`python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_EMPTY_TEMP_ROOT --private-evidence-root PRIVATE_EVIDENCE_ROOT`

The runner refuses an existing work directory, copies the complete frozen tree,
verifies authority and payload hashes, fixes `SOURCE_DATE_EPOCH`, builds only
`brauer.tex` and `stacks-limits.tex`, restores the authority bytes, repeats both
builds, writes sanitized public evidence under `builds/`, and removes the fresh
work tree after success. For each stem the command sequence is `pdflatex`,
`bibtex`, `pdflatex`, `pdflatex` with nonstop and halt-on-error flags.

Then run `python build-receipt.py` and `python verify.py`. The first binds source,
log, PDF, command, and warning multisets. The second reconstructs each payload
from the thirteen mapped units, proves structural invariants, validates all
evidence hashes, and requires the rendered-page QA receipt. Independent replay
and overlay admission are later, separate receipt-bound transitions.

Standalone chapter builds intentionally retain unresolved cross-chapter
references because the cumulative AUX set is absent. This limitation must match
the authority builds exactly.
