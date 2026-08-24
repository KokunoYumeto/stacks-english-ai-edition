# Independent review: ALGEBRA-330–341

Authority: `algebra.tex` at commit
`a04446e57ec1fbc252a871afcec7752fb2807b14`, 1,771,230 bytes, SHA-256
`FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3`.
The producer ledger snapshot has 746 unique rows, 341,079 bytes, SHA-256
`71C77AD80E68F10107D1295E4DEF985954B315FBAC246F2910AFDECBECE48798`.

## Disposition

Eleven bounded candidates are accepted as `MC-STK-ERR-0675` through
`MC-STK-ERR-0685`; `ALGEBRA-338` is rejected. Three independent read-only
reviews and the canon review recomputed the frozen identities and checked the
exact loci. No authority, translation, or upstream repository byte was changed
during adjudication.

- `ALGEBRA-330` is an omitted-verification gap, not a counterexample. The proof
  must separate the trivial `x in R` case and verify the nonisomorphism,
  kernel, target, and associated-prime hypotheses before invoking alternative
  (4) of the cited lemma.
- `ALGEBRA-331` and `ALGEBRA-332` repair associated-prime terminology and a
  missing sentence terminator.
- `ALGEBRA-333` is circular as printed: `K` cannot be introduced as the
  fraction field of `K[X_1,...,X_{r+1}]/(G)`. The polynomial was declared over
  `k`, so the domain is `k[X_1,...,X_{r+1}]/(G)`; the broken sentence is joined.
- `ALGEBRA-334` replaces both undefined `Omega_k` shorthands by the explicitly
  relative modules `Omega_{k/F_p}` used throughout the lemma.
- `ALGEBRA-335` replaces an unlocalized codomain `Omega_{S/F_p}` by
  `Omega_{K/F_p}`, matching the preceding localization and the lemma statement.
- `ALGEBRA-336` repairs a real proof-scope gap. In characteristic zero the
  extension is separable directly. In characteristic `p`, applying the
  formal-smoothness exact-sequence lemma with base `F_p` gives exactly the
  differential injection required by the cited positive-characteristic
  separability criterion.
- `ALGEBRA-337` repairs singular agreement.
- `ALGEBRA-338` is not a defect. The enumeration is the grammatical complement
  of “If the characteristic of k is zero then” and asserts that all five
  statements hold. Recasting it as an equivalence would change the claim.
- `ALGEBRA-339` adds the omitted lemma connecting formal smoothness with
  `H_1(L_{K/k}) = 0`, and repairs the citation-list comma.
- `ALGEBRA-340` uses the standard term “minimal polynomial.”
- `ALGEBRA-341` repairs plural agreement and replaces two `x_r` endpoints by
  `x_d`: `d` indexes the transcendence basis while `r` indexes the algebraic
  generators.

The candidate is limited to fifteen exact, nonoverlapping UTF-8 operations.
Canonical CJK translations remain source-faithful; these corrections belong
only to the independently maintained Stacks — English AI Edition.
