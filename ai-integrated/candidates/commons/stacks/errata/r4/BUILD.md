# Deterministic replay

Use the exact source tree bound by `authority/upstream.lock.json`.

`python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_TASK_LOCAL_ROOT --private-evidence-root PRIVATE_EVIDENCE_ROOT`

The runner refuses an existing work root, copies the complete frozen tree,
verifies all three authority and payload hashes, fixes `SOURCE_DATE_EPOCH` to
`1785270512`, builds candidate and authority versions of the three
modified chapters, writes sanitized public evidence under `builds/`, and
removes only the marker-bound temporary work root after success. Each chapter
uses `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.

Then run `python build-receipt.py` and `python verify.py`. The verifier rebuilds
all payloads from the 154 exact source-map units and checks structure, evidence,
build, visual, and public-hygiene gates. Run `python check-manifest.py` only
after the manifest is written. Independent replay and overlay admission remain
separate transitions.

Standalone chapter builds intentionally retain unresolved cross-chapter
references because the cumulative AUX set is absent; candidate and authority
warning-target multisets must match exactly.
