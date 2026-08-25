# Deterministic replay

Use the exact source tree bound by `authority/upstream.lock.json`.

`python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_TASK_LOCAL_ROOT --private-evidence-root PRIVATE_EVIDENCE_ROOT`

The runner refuses an existing work root, copies the complete frozen tree, verifies authority and payload hashes, fixes `SOURCE_DATE_EPOCH` to `1785270512`, builds candidate and authority versions of the directly modified Brauer chapter, writes sanitized public evidence under `builds/`, and removes only the marker-bound temporary work root after success. The chapter uses `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.

Run the build twice in fresh work roots and use `python deterministic-replay.py --first-private-build-root FIRST_PRIVATE_BUILD_ROOT` to prove byte-identical PDFs. Then run `python build-receipt.py`, render every candidate page, inspect the ordered contact sheet and all ten high-resolution pages, run `python visual-qa.py`, and run `python verify.py`. The verifier rebuilds the payload from all eight exact source-map units and checks structure, evidence, build, deterministic-PDF, visual, duplicate-rejection-ledger, and public-hygiene gates. Run `python check-manifest.py` only after the manifest is written. Independent replay and overlay admission remain separate transitions.

The standalone chapter build intentionally retains unresolved cross-chapter references because the cumulative AUX set is absent; candidate and authority warning-target multisets must match exactly apart from explicitly configured candidate-only references.
