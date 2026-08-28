# R28 deterministic gate sequence

1. Run `python prepare-inputs.py` and `python verify-source.py`.
2. Build the standalone candidate and frozen official authority twice with `replay-build.py` in new isolated roots.
3. Compare the two private builds with `deterministic-replay.py`.
4. Create `build-receipt.json`, derive the SyncTeX source-page map, and freeze the exact visual-page inventory in `candidate.config.json`.
5. Render every page and the correction-sensitive pages with `render-qa.py`; inspect the contact sheets and high-resolution pages; then record `visual-qa.json`.
6. Run `verify.py`, build the pre-review manifest, and check complete hash closure.
7. Run `independent-review.py` against the sealed private render manifest.
8. Rebuild and recheck the final manifest. Admission and cumulative composition are separate append-only transitions.

The cumulative composer must apply only the bound fragment replacement against the exact public-base blob. It must not copy the isolated payload wholesale.
