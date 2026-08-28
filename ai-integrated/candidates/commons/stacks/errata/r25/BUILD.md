# Deterministic build and QA replay

R25 source adjudication and materialization are sealed for `artin.tex`: 131 semantic units and 154 exact operations produce the payload identified in `candidate.config.json`. Source materialization alone establishes no PDF, render, visual-inspection, manifest, or independent-review PASS.

Use the exact upstream tree bound by `authority/upstream.lock.json`. Run the builder twice with distinct absent work roots and distinct absent private-evidence roots:

```text
python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_WORK_ROOT_1 --private-evidence-root NEW_ABSENT_PRIVATE_BUILD_ROOT_1
python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_WORK_ROOT_2 --private-evidence-root NEW_ABSENT_PRIVATE_BUILD_ROOT_2
python deterministic-replay.py --first-private-build-root NEW_ABSENT_PRIVATE_BUILD_ROOT_1
python build-receipt.py
```

The runner refuses either pre-existing output root, copies the full frozen upstream tree, verifies the authority and candidate source hashes, reads `SOURCE_DATE_EPOCH` from `candidate.config.json`, builds candidate and authority versions of `artin.tex`, writes sanitized public evidence under `builds/`, and removes only its marker-bound temporary work root after success. The exact chapter recipe is `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.

Final reader-page mapping is a build result. In a separate private SyncTeX work root, reproduce the candidate build with `-synctex=1`; its `artin.tex` source must equal the sealed payload and its `artin.pdf` must be byte-identical to `builds/artin.pdf`. Then run:

```text
python derive-visual-pages.py --synctex-work-root PRIVATE_SYNCTEX_WORK_ROOT
```

Freeze the resulting `builds/source-page-map.json` into `candidate.config.json` as follows:

- `visual_qa.correction_sensitive_pages.artin` must equal `source-page-map.json`'s sorted `unique_pages` exactly.
- `visual_qa.high_resolution_pages.artin` must be a sorted unique superset of those pages; using the same list is sufficient.
- `visual_qa.source_page_map` must record path `builds/source-page-map.json`, its byte count, and SHA-256.
- `private_render_logical_path` must identify the durable sanitized private render location without exposing a machine-local path.

Render only after those bindings are sealed:

```text
python render-qa.py --render-root NEW_ABSENT_PRIVATE_RENDER_ROOT
```

The main agent must inspect every ordered contact sheet and every configured high-resolution correction-sensitive page before recording visual PASS. `visual-qa.py` will refuse to claim that inspection unless the post-inspection attestation flag is supplied:

```text
python visual-qa.py --private-render-root PRIVATE_RENDER_ROOT --manual-review-complete
python verify.py
python build-manifest.py
python check-manifest.py
```

The first manifest is the sealed pre-review manifest. Run the later independent adverse replay against the exact private render manifest, then rebind and recheck the final manifest:

```text
python independent-review.py --private-render-manifest PRIVATE_RENDER_ROOT/render-manifest.json
python build-manifest.py
python check-manifest.py
```

The standalone chapter build may retain cross-chapter unresolved references because the cumulative AUX set is absent; candidate and authority warning-target multisets must match apart from explicitly configured, source-grounded exceptions. Registry admission, generated-source composition, Git operations, and publication remain separate transitions.
