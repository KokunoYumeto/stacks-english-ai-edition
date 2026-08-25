# Deterministic replay

Use the exact source tree bound by `authority/upstream.lock.json` after the R21 materializer has produced the candidate closure.

`python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_TASK_LOCAL_ROOT --private-evidence-root PRIVATE_EVIDENCE_ROOT`

The runner refuses an existing work root, copies the complete frozen tree, verifies authority and payload hashes, fixes `SOURCE_DATE_EPOCH` to the value in `candidate.config.json`, builds candidate and authority versions of the directly modified Simplicial Categories chapter, writes sanitized public evidence under `builds/`, and removes only its marker-bound temporary work root after success. The chapter uses `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.

Run the build twice in distinct fresh work roots. Preserve the first private build root, let the second run produce the current public `builds/` outputs, and run:

`python deterministic-replay.py --first-private-build-root FIRST_PRIVATE_BUILD_ROOT`

Then run `python build-receipt.py`.

The final PDF page mapping is a build result, not an intake guess. Before rendering, `candidate.config.json` must contain sorted, unique, in-range lists at:

- `visual_qa.high_resolution_pages.simplicial`
- `visual_qa.correction_sensitive_pages.simplicial`

The second list must be a subset of the first and must be derived from the final R21 source loci and reader pagination. Invoke `python render-qa.py --render-root NEW_ABSENT_RENDER_ROOT --high-res-pages ...` with exactly the configured high-resolution page list. Inspect every ordered contact sheet and every configured correction-sensitive page, then run `python visual-qa.py --private-render-root PRIVATE_RENDER_ROOT`.

Run `python verify.py`, `python build-manifest.py`, and `python check-manifest.py`. Independent replay is a later nonmutating gate over the sealed pre-review candidate:

`python independent-review.py --private-render-manifest PRIVATE_RENDER_ROOT/render-manifest.json`

Finally rerun `python build-manifest.py` and `python check-manifest.py` so the final manifest binds the replay receipt. The verifier reconstructs the payload from all 11 exact source-map units and 11 operations, verifies that the one rejected allegation consumes no stable ID, and checks source structure, evidence closure, build determinism, visual QA, ledgers, and public hygiene.

The standalone chapter build intentionally retains unresolved cross-chapter references because the cumulative AUX set is absent; candidate and authority warning-target multisets must match exactly apart from explicitly configured candidate-only references. Independent replay, registry admission, and generated-source composition are separate transitions.
