# Independent review: ALGEBRA-314

Authority: `algebra.tex` at commit
`a04446e57ec1fbc252a871afcec7752fb2807b14`, SHA-256
`FA8BB92E58A4F78A2BD01B3B6A4A87DE0A0D279F5DD90641B574DD5FBFFFA4F3`.

## Disposition

Accepted as `MC-STK-ERR-0659`.

The printed lemma permits the exact example
`A = k[t]_(t)` and `B = k(t) = A[1/t]`.  Here `A` is a one-dimensional
Noetherian local domain, `B` is a finite-type `A`-domain, and the fraction-field
extension is finite (indeed, the identity).  Nevertheless, the sole maximal
ideal of `B` is `(0)`, so `B_(0)` has dimension zero.  The order function cited
in the conclusion is defined only for one-dimensional Noetherian local rings,
and the displayed residue-field degree need not be finite.  In the proof,
`C cap (0) = (0)` is likewise not a maximal ideal of the finite `A`-algebra
`C`.

Adding that `B` is not a field closes the counterexample.  Indeed, any maximal
ideal of `B` contracting to `(0)` has height zero by the dimension formula;
because `B` is a domain it must then be `(0)`, which can be maximal only when
`B` is a field.  Thus every maximal ideal of a nonfield `B` lies over the
maximal ideal of `A`, and the local orders and the proof's maximal-ideal
partition are well typed.

The bounded rendered correction is a single prose hypothesis immediately
after the existing enumeration.  No authority or translation bytes were
mutated by this review.
