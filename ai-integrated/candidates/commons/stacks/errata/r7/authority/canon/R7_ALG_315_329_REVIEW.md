# Independent review: ALGEBRA-315–329

Authority: `algebra.tex` at commit
`a04446e57ec1fbc252a871afcec7752fb2807b14`, 1,771,230 bytes, SHA-256
`FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3`.
The producer ledger snapshot has 734 unique rows, 334,819 bytes, SHA-256
`ECE134C64FCB7091B665DF5CBDB31168386C9812F94EAFC0A034F80EFFB16143`.

## Disposition

All fifteen bounded candidates are accepted as `MC-STK-ERR-0660` through
`MC-STK-ERR-0674`. Three independent read-only reviews recomputed the frozen
authority identity and checked the exact loci. No authority, translation, or
upstream repository byte was changed during adjudication.

- `ALGEBRA-315`: the proof forms `kappa(p)` although the lemma binds only
  `q`. Defining `p` as the inverse image of `q` in `R` is the typed repair.
- `ALGEBRA-316`: `overline q` is not the already defined
  `overline{fraktur q}`.
- `ALGEBRA-317`: the polynomial-variable list omits its first comma.
- `ALGEBRA-318`: a prime of the subring `S'` cannot lie over a prime of the
  overring `S`; it is the contraction of `q S_p`.
- `ALGEBRA-319`: a quasi-finite algebra map need not be injective; for example,
  `k[t] -> k`, `t |-> 0`, is quasi-finite. The lemma and its later use require
  a map, not an inclusion.
- `ALGEBRA-320`: the fibre bound `n` and the arbitrary number of presentation
  generators are independent. A fresh `N` repairs both presentation lines.
- `ALGEBRA-321`: generally `k = R/m_R` does not map to `S`; for example take
  `R = Z_(p)` and `S = R`. The defined special-fibre quantity is
  `dim_q(S/R)`.
- `ALGEBRA-322` and `ALGEBRA-323`: the generated algebra and ideal use
  transposed indices different from the elements just bound.
- `ALGEBRA-324`: localizing `S x C` at the `C` idempotent retains `C`; the
  proof needs the idempotent retaining `S`.
- `ALGEBRA-325`: the proof declares `m` variables and then uses undefined `n`
  in three polynomial rings.
- `ALGEBRA-326`: inserting `is` twice is accepted strictly as a grammar and
  parallelism copy-edit. It does not alter the hypotheses' meaning.
- `ALGEBRA-327`: each clause performs two parallel replacements. Naming the old
  polynomial ring and the replacement relation removes the malformed
  coordination without changing the construction.
- `ALGEBRA-328`: the statement leaves its kernel prime unnamed, then the proof
  uses `q'` in two different tensor-product rings. The repair names the kernel
  prime and explicitly takes its inverse image under the canonical localization
  map before the later localizations at `q'`.
- `ALGEBRA-329`: plural `filtered colimits` is required with `commute`.

The candidate is limited to exact, nonoverlapping UTF-8 source operations. The
canonical CJK translations remain source-faithful; these corrections belong
only to the independently maintained Stacks — English AI Edition.
