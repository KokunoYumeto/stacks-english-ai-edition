# R42 build and replay recipe

1. Run `python pipeline_r42.py --materialize` once against the active R42
   lease. This pins the authority, preserves producer evidence, and performs
   exact source replay and structural checks without running TeX.
2. Run `run-builds-with-mutex.ps1` with the pinned upstream source directory,
   two new absent work directories, and two separate private evidence roots.
   It holds `Global\InterlanguageTeXSlotV1` across both sequential candidate
   and authority builds, deterministic PDF comparison, and immediate log checks.
3. Derive source-sensitive PDF pages from the second build's SyncTeX evidence,
   render all pages plus high-resolution sensitive pages, and inspect the actual
   bound images before recording visual PASS.
4. Run `finalize_r42.py mechanical`, `prepare`, independent final validation,
   `finalize_r42.py seal`, and `check-manifest.py`, in that order.

No helper in this candidate admits the overlay, composes generated source, or
publishes an upstream report.
