# Unified-build receipts

The current release build gate is recorded in
[`unified-fixed-point-2026-08-25-r19.json`](unified-fixed-point-2026-08-25-r19.json).
The earlier [`R1–R15 receipt`](unified-build-2026-08-25.json) remains preserved
as historical evidence for its exact source tree.

It binds the unified source commit and tree to:

- admitted errata replay through R19;
- all R4–R19 immutable manifest checks;
- the complete 548-operation source-composition gate, 69 earlier replacements,
  nine R1 tag additions, and 21,819 unique permanent tags;
- EGA scaffold and pinned-map checks; and
- fresh fixed-point builds of all 18 chapters changed by EGA or R1–R19, plus
  the headline `injectives`, `gaga`, and `moduli` integration chapters.

All 21 PDFs (2,269 pages; 23,549,238 bytes) compiled successfully, were readable
by `pdfinfo`, and reached a global fixed point on sweep four. PDF bytes are build artifacts;
the committed receipt records their page counts, byte counts, and SHA-256
identities without placing generated binaries in the source tree.
