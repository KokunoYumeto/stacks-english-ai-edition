# Deterministic standalone build replay

R31 independently reopens one previously rejected `sites-modules.tex` operation at source line 7967. Eighteen other current handoff operations are exact R29 duplicates and are excluded. Source materialization alone establishes no PDF, render, visual-inspection, manifest, or independent-review PASS.

Use the exact upstream tree bound by `authority/upstream.lock.json`. Run the builder twice with distinct absent work roots and private-evidence roots, then compare and seal the build receipt:

```text
python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_WORK_ROOT_1 --private-evidence-root NEW_ABSENT_PRIVATE_BUILD_ROOT_1
python replay-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_WORK_ROOT_2 --private-evidence-root NEW_ABSENT_PRIVATE_BUILD_ROOT_2
python deterministic-replay.py --first-private-build-root NEW_ABSENT_PRIVATE_BUILD_ROOT_1
python build-receipt.py
```

The runner copies the frozen upstream tree, verifies authority and candidate source hashes, and builds candidate and authority versions of `sites-modules.tex` with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`. Both independent runs use `SOURCE_DATE_EPOCH=1788048000`, `FORCE_SOURCE_DATE=1`, and `TZ=UTC`.

Reproduce the candidate build with SyncTeX in a separate private root, derive and bind the correction-sensitive pages, render the sealed PDF, inspect every contact sheet and every configured high-resolution page, and then seal source/build/visual validation:

```text
python synctex-build.py --upstream-root FROZEN_SOURCE_ROOT --work-root NEW_ABSENT_SYNCTEX_WORK_ROOT
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
