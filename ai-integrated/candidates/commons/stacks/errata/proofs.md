# Proof dossiers for `stacks-errata-a04446e-r1`

All loci below refer to the byte-identical authority copies in `authority/` and
Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`. These are proofs of
the candidate corrections, not claims of upstream review or endorsement.

## `MC-STK-ERR-0001`

In `smoothing.tex:191-221`, elementary standardness introduces one coefficient
`a'`, while strict standardness instead introduces the family `a_I`. The proof
at lines 261-275 assumes strict standardness, cites that definition, and never
uses or constructs `a'`. Thus “and `a' \in A` be as in Definition …” refers to
data that the cited strict clause does not supply. Deleting only that phrase
restores exact agreement with the hypothesis; no mathematical assertion is
added.

## `MC-STK-ERR-0002`

At `smoothing.tex:469-478`, the chosen presentation is over
`R_0[y_1, …, y_m]`, and each `\bar f_i` is an arbitrary polynomial in those
`m` variables. A lift therefore belongs to `R[y_1, …, y_m]`. Membership in the
smaller ring through `y_c` is not guaranteed: for example, when `m=2,c=1` and
`\bar f_1=y_2`, no element of `R[y_1]` can reduce to `y_2`. The quotient on
line 478 also uses all `m` variables. Replacing `y_c` by `y_m` is therefore the
unique general correction.

## `MC-STK-ERR-0003`, `MC-STK-ERR-0005`, and `MC-STK-ERR-0006`

These are mechanically decidable English defects at exact unique loci:
`exists finite type … map` lacks the singular article; `an enumerations`
disagrees in number; and `correspond a_i/1` lacks `to`. Each replacement occurs
once, changes no mathematical token, and the exact-payload verifier proves
there are no adjacent edits.

## Rejected `MC-STK-ERR-0004`

The inherited proposal would replace “there exists a `g` … that `P(g)`” with
“such that.” Proof review found no defect: the printed construction is
grammatical and has the same mathematical truth conditions. It was therefore
removed from the payload rather than promoted from style preference to errata.

## `MC-STK-ERR-0007`

`crystalline.tex:183-201` declares `T` as the index set for `f_t` and the
divided-power variables `x_t`; `I` is an ideal of `B`. Consequently the term
`x_{t'}` is well-formed only for `t' \in T`, and `f_t` only for `t \in T`.
Quantifying `t',t \in I` is a sort error—elements of the ideal do not index
these variables. The unique well-typed correction is `t',t \in T`.

## `MC-STK-ERR-0008`

An exhaustive label/tag comparison found exactly nine live labels absent from
`authority/tags/tags`, all in the three named source files. The frozen
`scripts/functions.py` allocator, whose hash is bound in the manifest, returned
exactly those nine labels and issued the consecutive records `0HB4` through
`0HBC`; it returned no tenth record. After appending those exact records to a
copy of the full frozen tree, the same allocator returned `[]`. The verifier
also proves that the authority tag file is an unchanged prefix, every new label
exists exactly once in its declared TeX file, and both tag codes and full labels
remain globally unique.

## `MC-STK-ERR-0009`

The lemma at `spaces-cohomology.tex:300-311` declares only a finite morphism
`f:X\to Y`. After the base change at lines 314-319, the renamed objects remain
`X` and `Y`, and the base-changed morphism remains `X\to Y`. No `Z` is declared
anywhere in the lemma or proof. Hence `Z\to X` is undefined and has the wrong
source and target. `X\to Y` is forced by the statement and by the finite-scheme
proposition invoked on the next lines.

## `MC-STK-ERR-0010`

In the projection-formula stalk computation, `\mathcal B` and `\mathcal G`
live on `Y`, so their stalks are at `\bar y`; `\mathcal A` and `\mathcal F`
live on `X`, so their stalks are at the points `\bar x_i` over `\bar y`.
Lines 369-370 already use the base ring `\mathcal B_{\bar y}` on the left.
The right-hand tensor must use that same base to act on
`\mathcal A_{\bar x_i}`. `\mathcal B_{\bar x}` is both undeclared (`\bar x_i`
is the declared notation) and a stalk at a point of the wrong space. Replacing
it by `\mathcal B_{\bar y}` is uniquely type-correct.

## `MC-STK-ERR-0011`

The standing hypothesis is an arbitrary finite morphism. Finite morphisms are
not generally closed immersions—for instance
`Spec(k\times k)\to Spec(k)` is finite but not an immersion. The proof invokes
the immediately preceding lemma specifically proved for finite morphisms.
Therefore “pushforward along a closed immersion” does not follow from the
hypotheses; “pushforward along a finite morphism” states exactly the result
used.

## `MC-STK-ERR-0012`

At `spaces-cohomology.tex:554-564`, the two objects are `U` and `U'`, their
product is `U\times_XU'`, and line 555 already writes `h_{U'}^#`. Lower-case
`u'` is never declared and denotes a different TeX symbol. The product map is
therefore necessarily `h_U^#\times h_{U'}^#`.

## `MC-STK-ERR-0013`

Lines 596-610 define `f_!` as a functor. Lines 613-620 then fix an abelian
sheaf `\mathcal G` and display the presheaf whose values are
`f_!\mathcal G(V)`. A functor alone is not “the sheaf” attached to the fixed
input; its value `f_!\mathcal G` is. The correction inserts precisely the
already fixed argument and agrees with both the displayed formula and the next
sentence.

## `MC-STK-ERR-0014`

At lines 1030-1032, the only opening parenthesis in the tensor factor is the
one in `\underline{\mathbf Z}(\chi_p)`, and it is closed immediately after
`\chi_p`. The printed `))` therefore contains one unmatched extra closing
parenthesis. Removing the second one restores the well-formed functor formula;
the build and exact-diff verifier confirm no delimiter or adjacent expression
was altered.

## `MC-STK-ERR-0015`

Lines 1026-1029 place the restricted injective object in
`Ab(U_{p,\mathrm{\acute etale}})`. Tensoring with the invertible sheaf
`\underline{\mathbf Z}(\chi_p)` is an auto-equivalence of that same category
of abelian sheaves on the small étale site, which is what the subsequent
injectivity and exactness argument requires. Bare `Ab(U_p)` names neither that
site nor the category just introduced. Restoring the explicit small-étale
subscript makes the domain/codomain agree with the preceding restriction and
the later cohomology computation.

## Adverse evidence and residual ambiguity

The frozen source context, current upstream master at verification time,
producer ledgers, dependent notation, and exact build outputs were checked.
No contrary definition or dependent use supporting the printed forms was
found. The retained copyediting items are unambiguous at their unique byte loci; the
mathematical items above have either a type contradiction, an explicit
counterexample, an undefined object, or a forced domain/codomain. No semantic
choice remains open in this candidate. Standalone chapter builds retain the
same unresolved cross-chapter reference targets as their unmodified authority
builds; that limitation is not caused by these corrections.
