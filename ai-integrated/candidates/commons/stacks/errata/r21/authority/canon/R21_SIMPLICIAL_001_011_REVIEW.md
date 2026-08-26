# R21 independent review - `simplicial.tex`

This review binds eleven accepted units directly to the frozen `simplicial.tex` bytes at Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`. The eleven French-producer allegations are locator evidence only; one is rejected. `CANON-SIMPLICIAL-001` was found independently while checking the dual cosimplicial paragraph.

## Mathematical and textual adjudication

- `SIMPLICIAL-001` and `CANON-SIMPLICIAL-001` correct, respectively, the face-map type `U_2 -> U_1` and the dual coface-map type `U_1 -> U_2`.
- `SIMPLICIAL-002`, `SIMPLICIAL-004`, `SIMPLICIAL-005`, and `SIMPLICIAL-011` repair undefined or ill-typed symbols and indices.
- `SIMPLICIAL-003`, `SIMPLICIAL-006`, and `SIMPLICIAL-010` are certain grammar defects.
- `SIMPLICIAL-007` is rejected: line 1715 opens an outer `Mor(`, and the two closing parentheses on line 1716 close the final `Hom(` and that outer `Mor(`. The producer's deletion would unbalance the formula and must be reverted in the French target.
- `SIMPLICIAL-008` removes a genuine unmatched closing parenthesis in the later displayed equality.
- `SIMPLICIAL-009` is mathematically certain: both maps originate at the common `U` term, and the asserted result is `V \amalg_U W`; the construction is a pushout, not a fibre product.

## Replay and deduplication

Every old span occurs exactly once on its declared source line. Operations are applied to frozen half-open byte intervals in descending order. `SIMPLICIAL-004` and `SIMPLICIAL-007` are line-bound because their old text also occurs elsewhere correctly. The line-477 canon-origin unit remains distinct from the producer's line-277 unit.

No accepted unit duplicates R1-R20 or another R21 unit. Rejected allegations consume no stable ID. Stable IDs continue contiguously as `MC-STK-ERR-0904..0914`. The combined eleven-operation payload is expected to be 235,001 bytes with SHA-256 `E4FD6748E65633490F8C48D720BEBF7327505DDF25B578868F6739E15BC96E16`.

The authority, canonical translations, permanent tags, and prior payloads remain immutable. This review authorizes candidate replay and registry admission only; generated-source composition remains a separate task.
