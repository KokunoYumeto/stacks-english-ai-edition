# Unified-build receipts

The current release gate is recorded in
[`unified-build-2026-08-25.json`](unified-build-2026-08-25.json).

It binds the unified source commit and tree to:

- all 15 admitted errata candidate verifiers;
- all R4–R15 immutable manifest checks;
- the complete 460-operation/tag source-composition gate;
- EGA scaffold and pinned-map checks; and
- fresh fixed-point builds of all 16 chapters changed by EGA or R1–R15, plus
  the headline `injectives`, `gaga`, and `moduli` integration chapters.

All 19 PDFs compiled successfully, were readable by `pdfinfo`, and reached a
global fixed point on sweep four. PDF bytes are treated as build artifacts;
the committed receipt records their page counts, byte counts, and SHA-256
identities without placing generated binaries in the source tree.
