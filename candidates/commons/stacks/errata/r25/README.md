# Stacks errata candidate R25

R25 is the source-materialized candidate for independently adjudicated corrections to `artin.tex` at Stacks Project commit `a04446e57ec1fbc252a871afcec7752fb2807b14`. The frozen authority is 254,362 bytes with SHA-256 `EBA90A897B08EEBFF451E80925D13381B1A7F6AB883A34118733CD24CF061F47`.

The frozen intake contains the contiguous producer packet `P11-E0200` through `P11-E0339`. Independent adjudication accepts 137 producer identities, rejects `P11-E0202`, `P11-E0215`, and `P11-E0217`, merges six linked pairs, and materializes 131 semantic units with contiguous IDs `MC-STK-ERR-1046` through `MC-STK-ERR-1176`. The packet seals 154 non-overlapping exact operations in first-locus physical source order.

`prepare-inputs.py` verifies the frozen authority and producer ledger, recovers exact source locators, and derives the intake ledgers. `materialize.py` creates the authority closure and corrected payload. `verify-source.py` independently reconstructs the payload, checks identifier and producer closure, verifies the requested semantic refinements, and writes `source-validation.json`.

The source-only payload is 254,488 bytes with SHA-256 `F196752E6D872B3B888E57C7183B326287F1A241286991C075E4896996FD185B`. Source verification passes. No TeX/PDF build, render, admission, registry mutation, Git operation, publication, or generated-source composition has been performed.

The lease remains bound to registrar-issued `stacks-lease-000029-errata-r25`. The Stacks Project authors and maintainers have not requested, reviewed, approved, or endorsed this independently maintained AI-produced candidate. Upstream content remains under GNU Free Documentation License 1.2.
