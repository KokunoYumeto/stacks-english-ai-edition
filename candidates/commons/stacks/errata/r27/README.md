# Stacks errata candidate R27

R27 is the source-materialized candidate for independently adjudicated corrections to `modules.tex` at Stacks Project commit `a04446e57ec1fbc252a871afcec7752fb2807b14`. The frozen authority is 204,133 bytes with SHA-256 `7BD3E9E096717EF6FD458492D8AD91FC9FFE428CFD7DD80E386FAE377BB7CB0D`.

The intake contains exactly `MODULES-001` through `MODULES-014`. Three independent reviews accept all 14 as new semantic units, find no aliases or rejections, and assign contiguous IDs `MC-STK-ERR-1202` through `MC-STK-ERR-1215` in first-locus source order. Each unit has one exact bounded operation. `MODULES-014` uses the narrower forced article correction rather than the producer's broader number rewrite.

`prepare-inputs.py` verifies the frozen authority and producer evidence, performs predecessor deduplication, recovers exact source locators, and derives the intake ledgers. `materialize.py` creates the authority closure and corrected payload. `verify-source.py` independently reconstructs the payload, checks identifier and producer closure, and writes `source-validation.json`.

The lease is bound to registrar-issued `stacks-lease-000031-errata-r27`. The Stacks Project authors and maintainers have not requested, reviewed, approved, or endorsed this independently maintained AI-produced candidate. Upstream and modified payload content remains under GNU Free Documentation License 1.2.
