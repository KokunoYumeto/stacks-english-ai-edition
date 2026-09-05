# R43 additive finalization order

1. Preserve the source-only artifacts and their independent validation receipt.
2. Run two fresh TeX builds under the required machine-wide mutex, prove PDF
   byte identity, and bind the final mutex receipt and build diagnostics.
3. Map all seven operations across seven stable units to the sealed candidate PDF, render every page,
   inspect every rendered page at the stated resolution, and preserve explicit
   visual limitations and any adverse evidence.
4. `python finalize_r43.py mechanical` rehashes source, build, PDF, link,
   source-page-map, mutex, and render evidence without asserting visual review.
5. `python finalize_r43.py prepare` freezes every completed artifact except the
   future independent review and top manifest in immutable
   `replay/FINAL_STAGE.json`.
6. An independent replay reads that snapshot, replays all operations from the
   pinned authority, checks the build and visual receipts, and writes
   `replay/FINAL_INDEPENDENT_REVIEW.json` binding the snapshot hash.
7. `python finalize_r43.py seal` writes the top manifest last; then
   `python check-manifest.py` proves strict schema and owned-file closure.

Registry admission is a later append-only registrar transition. The frozen
authority, generated-source repositories, and official upstream remain outside
this candidate's write boundary.
