# R44 finalization order

1. Materialize and independently replay the 24-unit, 32-operation source stage.
2. Build candidate and authority twice under the machine-wide TeX mutex using
   `-recorder`; bind deterministic PDFs, sanitized logs, and `.fls` closure.
3. Render every candidate page, inspect complete contact-sheet coverage and all
   correction-sensitive pages at high resolution, and preserve adverse evidence.
4. Freeze `replay/FINAL_STAGE.json`.
5. Obtain a separate independent `replay/FINAL_INDEPENDENT_REVIEW.json` that
   binds the frozen stage.
6. Seal `candidate.manifest.json` last, then commit the candidate separately
   from registry admission.

No step composes or pushes generated Stacks source.
