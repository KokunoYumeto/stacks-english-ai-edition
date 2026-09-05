# Deterministic build contract

Build the candidate and frozen authority sequentially in a fresh isolated copy
of the pinned Stacks source tree. Run `pdflatex -recorder`, BibTeX, then two more
`pdflatex -recorder` passes for each phase. Repeat the full build in a second
fresh root with the same `SOURCE_DATE_EPOCH`, compare PDFs byte-for-byte, and
retain sanitized logs plus exact `.fls` dependency inventories. Every TeX and
BibTeX process must run while holding `Global\InterlanguageTeXSlotV1`.
