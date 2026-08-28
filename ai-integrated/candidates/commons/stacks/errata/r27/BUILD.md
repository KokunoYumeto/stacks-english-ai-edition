# Deterministic build and QA replay

R27 source adjudication and materialization are sealed for `modules.tex`: 14 semantic units and 14 exact operations produce the payload identified in `candidate.config.json`. Source materialization alone establishes no PDF, render, visual-inspection, manifest, or independent-review PASS.

Use the exact upstream tree bound by `authority/upstream.lock.json`. Run the builder twice with distinct absent work roots and private-evidence roots, then compare and seal the build receipt:

```text
python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_WORK_ROOT_1 --private-evidence-root NEW_ABSENT_PRIVATE_BUILD_ROOT_1
python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_WORK_ROOT_2 --private-evidence-root NEW_ABSENT_PRIVATE_BUILD_ROOT_2
python deterministic-replay.py --first-private-build-root NEW_ABSENT_PRIVATE_BUILD_ROOT_1
python build-receipt.py
```

The runner copies the frozen upstream tree, verifies authority and candidate source hashes, and builds candidate and authority versions of `modules.tex` with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.

Reproduce the candidate build with SyncTeX in a separate private root, derive and bind the correction-sensitive pages, render the sealed PDF, inspect every contact sheet and every configured high-resolution page, and then seal source/build/visual validation:

```text
python derive-visual-pages.py --synctex-work-root PRIVATE_SYNCTEX_WORK_ROOT
python render-qa.py --render-root NEW_ABSENT_PRIVATE_RENDER_ROOT
python visual-qa.py --private-render-root PRIVATE_RENDER_ROOT --manual-review-complete
python verify.py
python build-manifest.py
python check-manifest.py
python independent-review.py --private-render-manifest PRIVATE_RENDER_ROOT/render-manifest.json
python build-manifest.py
python check-manifest.py
```

Cross-chapter unresolved references may remain in the isolated build only when their target multiset matches the frozen authority build. Registry admission, generated-source composition, Git operations, and publication are separate transitions.
