# Stacks errata candidate R22 intake skeleton

R22 is the bounded, non-build intake skeleton for 83 independently replayed corrections to `more-algebra.tex` at Stacks Project commit `a04446e57ec1fbc252a871afcec7752fb2807b14` (tree `3feeb703b931a6e7259782c10e7d1575adc83e5e`). It preserves provisional IDs `MC-STK-ERR-0915..0966` and extends them through `MC-STK-ERR-0997` in physical authority-source order.

Repeated P02 discoveries are collapsed as aliases on one semantic unit. The two unresolved editorial-reference placeholders are deleted without inventing destinations. The operation set repairs all three `M_b` loci in `MORE-ALGEBRA-G-001`, only the malformed `I^{c2c3}` occurrence on line 22705 for `G-015`, and changes `of` to `if` for `G-018`.

Lease I contributes 31 accepted semantic units and 37 operations. Five linked producer groups are merged, `MORE-ALGEBRA-I-027` is rejected without consuming an ID, and `MORE-ALGEBRA-I-009` is intentionally absent rather than rejected. The accepted I-004, I-025, and I-035 operations use the fully normalized wording and bounds required by the independent audit. Every accepted Lease-I unit is deduplicated to its exact P02 alias.

Run `python prepare-intake.py` to deterministically regenerate and validate the machine-readable intake inputs. `materialize.py` is adapted from the R21 workflow but has deliberately not been run. No authority copy, payload, TeX build, render, registry admission, Git mutation, push, or publication belongs to this skeleton stage.

The Stacks Project authors and maintainers have not requested, reviewed, approved, or endorsed this independently maintained AI-produced candidate. Upstream content remains under GNU Free Documentation License 1.2.
