# Stacks errata candidate R26

R26 is the source-materialized candidate for independently adjudicated corrections to `smoothing.tex` at Stacks Project commit `a04446e57ec1fbc252a871afcec7752fb2807b14`. The frozen authority is 134,660 bytes with SHA-256 `FD28CF874BB7DAD3C5C5FF03314D1C83701613A8A98730A99B9CA7A4BCFE6068`.

The intake contains exactly `SMOOTHING-001` through `SMOOTHING-035`. Independent adjudication accepts 31 new producer identities, binds `SMOOTHING-002`, `SMOOTHING-003`, and `SMOOTHING-004` as exact aliases of admitted R1 units `MC-STK-ERR-0002`, `MC-STK-ERR-0005`, and `MC-STK-ERR-0006`, rejects `SMOOTHING-010`, merges four repeated defect groups, and materializes 25 new semantic units with contiguous IDs `MC-STK-ERR-1177` through `MC-STK-ERR-1201`. The packet seals 39 non-overlapping operations in first-locus physical source order.

`prepare-inputs.py` verifies the frozen authority and producer evidence, performs predecessor deduplication, recovers exact source locators, and derives the intake ledgers. `materialize.py` creates the authority closure and corrected payload. `verify-source.py` independently reconstructs the payload, checks identifier and producer closure, verifies the refined operations, and writes `source-validation.json`.

The source-only payload is 134,839 bytes with SHA-256 `D5C5F0A6099ED011122BC90E836F8563E4F1496A30700CEBC1928E37812B08F0`. Source verification passes. Build, render, admission, registry publication, and generated-source composition remain later deterministic transitions.

The lease is bound to registrar-issued `stacks-lease-000030-errata-r26`. The Stacks Project authors and maintainers have not requested, reviewed, approved, or endorsed this independently maintained AI-produced candidate. Upstream and modified payload content remains under GNU Free Documentation License 1.2.
