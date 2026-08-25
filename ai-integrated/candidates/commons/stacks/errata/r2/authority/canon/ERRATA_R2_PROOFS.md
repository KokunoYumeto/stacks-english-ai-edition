# Stacks errata R2 proof intake

Authority commit: `a04446e57ec1fbc252a871afcec7752fb2807b14`

This is a proof record for the next derived-fork batch. It does not alter the
frozen source or either canonical Chinese translation, and it is not itself an
admitted overlay. Producer reports were treated as hypotheses. Every outcome
below was reopened against the exact source bytes; the Chapter 102 set was also
replayed by a separate bounded read-only reviewer.

## `MC-STK-ERR-0016` — `P02-E0001`

Authority: `brauer.tex`, 28,201 bytes, SHA-256
`B2504820D769EBE4E9E33B8ADD78753FB30ACA6E8A7F75C8D54DDA885EDCD682`.

At line 626 the source defines “splitting field”; lines 681 and 692 use the
same term, Proposition `proposition-separable-splitting-field` at lines
705–712 proves existence of one, and line 718 invokes
`lemma-maximal-subfield-splits`. Line 711 alone says “spitting field.” A
bounded corpus search found that spelling only at this locus and found the
defined term throughout. This is a mechanically certain spelling defect.

Smallest correction: `spitting field` → `splitting field` at line 711.

## `MC-STK-ERR-0017` — `P02-E0002`

Authority: the same `brauer.tex` bytes.

Lines 724–726 reduce the proof to finding an `x` satisfying all three
conditions `x in K`, `x not in k`, and `x` separable over `k`. The logical
negation used for contradiction is therefore that no element of `K \setminus
k` is separable. Line 733 instead assumes that no element of all of `K` is
separable. The printed assumption is false before the argument begins: each
`a in k` has minimal polynomial `T-a`, hence is separable over `k`.

The narrower correction still supports lines 736–740. An element outside `k`
has the asserted purely inseparable minimal polynomial under the corrected
assumption; an element of `k` has the same displayed form with the power
`q=1`. Thus the later common-power conclusion is not weakened.

Smallest correction: “assume no element of `K` is separable over `k`” →
“assume no element of `K` outside `k` is separable over `k`.”

## Chapter 102 authority

The following units use `stacks-limits.tex`, 42,110 bytes, SHA-256
`F4F5EBF02BB5922A8DFF70EA507ED6F821F992C697D9C9A984B9513C39FEC57A`.
The producer receipt binds the first 7,048 bytes of its append-only errata
ledger at SHA-256
`7B0EA21585CAF451E47B6C2AF320836C5FE4D917DF514CD986138DE3307B24AC`.
Later Chapter 103 rows in the live ledger are outside this proof intake.

## `MC-STK-ERR-0018` — `P12-ERR-0001`

Definition `definition-limit-preserving`, lines 60–70, fixes the base `S` and
quantifies directed systems of affine schemes `U_i` over `S`, with limit `U`.
Line 83 says “affine schemes over `U`,” but the limit projections are
`U -> U_i`; no structure maps `U_i -> U` have been supplied. The definition
being invoked forces the base `S`.

Smallest and unique well-typed correction: `over $U$` → `over $S$`.

## `MC-STK-ERR-0019` — `P12-ERR-0002`

The lemma declares `p : \mathcal{X} \to \mathcal{Y}` at line 157. Lines 188–201
use `p(x_i)` and set `y_i=p(x_i)`. The functor at line 208 alone requires an
isomorphism `phi : f(x) -> y_i|V`, but no `f` is declared in this proof.

Smallest and unique typed correction: `f(x)` → `p(x)`.

## `MC-STK-ERR-0020` — `P12-ERR-0003`

Lines 374–382 define the presenting groupoid with relation object `R` and
quotient `[U/R]`. The same quotient appears at lines 398, 401–406, and
433–437. Consequently the morphism description cited at line 440 is the fibre
category of `[U/R]`, not `[U/T]`.

Adverse evidence corrected from the producer report: `T` is not undefined; it
is the limit affine scheme introduced at line 395. It is nevertheless not the
relation object of the groupoid and cannot replace `R` in the quotient.

Smallest correction: `[U/T]` → `[U/R]`.

## `MC-STK-ERR-0021` — `P12-ERR-0004`

Situation `situation-descent`, lines 525–529, defines only
`Y=\lim Y_i`. Line 527 then attributes quasi-compactness and
quasi-separatedness to undeclared `X_i`, while the dependent lemma at lines
533–568 uses `Y_i` throughout.

Smallest and unique correction: `X_i` → `Y_i` at line 527.

## `MC-STK-ERR-0022` — first locus of `P12-ERR-0005`

Line 702 announces “two morpisms `s,t`.” The numeral and the two displayed
maps fix the plural noun; the spelling is not an alternate technical term.

Smallest correction: `morpisms` → `morphisms`.

## `MC-STK-ERR-0023` — second locus of `P12-ERR-0005`

Lines 872–877 compose the proper map `R_i \to V_i` with the closed immersion
`V_i \to U_i \times_{Y_i} U_i`, producing a proper map for each sufficiently
large `i`. Line 876 says “a proper morphisms.” Both deleting the article to
make a plural and deleting the final `s` to retain the singular are
mathematically possible; the latter is the one-character correction and the
frozen corpus independently uses “we obtain a proper morphism” in
`artin.tex:6085`.

Smallest corpus-consistent correction: `a proper morphisms` →
`a proper morphism`.

## `MC-STK-ERR-0024` — third locus of `P12-ERR-0005`

Line 881 says “this is the morphism is the same as `(s_i,t_i)`.” The previous
sentence has just constructed the composite morphism, so the demonstrative
modifies that morphism. Removing the duplicated copular phrase gives “this
morphism is the same as `(s_i,t_i)`.” The exact frozen corpus independently
uses that construction in `divisors.tex:8834`, and also uses “this morphism
is” in `curves.tex:5073` and `etale-cohomology.tex:14628`.

Adverse evidence: “this is the same as …” and the more redundant “this is the
morphism and is the same as …” can also be made grammatical. The selected
repair preserves the explicit referent and matches house usage; it is not
claimed to be the only grammatical paraphrase.

Smallest context-preserving correction: delete ` is the` after `this`, yielding
`this morphism is the same as`.

## `MC-STK-ERR-0025` — `P12-ERR-0006`

The lemma declares `f : \mathcal{X} \to Y` at line 900 and uses
`\mathcal{X}` in the source space at lines 901 and 916–917. Plain `X` is not
declared in the lemma. The ambient space at line 912 must carry the same stack.

Smallest and unique typed correction:
`|X \times_Y Z'|` → `|\mathcal{X} \times_Y Z'|`.

## `MC-STK-ERR-0026` — `P12-ERR-0007`

Lines 976 and 980 declare `\mathcal{X} \to \mathcal{Y}` and
`Z \to \mathcal{Y}`.
Line 982 forms their fibre product over undeclared plain `Y`; item (3), lines
983–986, correctly uses `\mathcal{Y}` as the base.

Smallest and unique typed correction:
`\mathcal{X} \times_Y Z` → `\mathcal{X} \times_{\mathcal{Y}} Z`.

## `MC-STK-ERR-0027` — `P12-ERR-0008`

The new implication at line 1053 fixes `V \to \mathcal{Y}`. Therefore its base
change at line 1054 is `\mathcal{X} \times_{\mathcal{Y}} V`. Only at lines
1059–1060 does the proof reduce to the special case `\mathcal{Y}=Y`.

Adverse evidence corrected from the producer report: plain `Y` occurs earlier
at lines 1002 and 1005, but inside the already completed `(2) => (1)`
reduction. It is outside the logical scope of the implication beginning at
line 1053 and does not type the line 1054 base change.

Smallest and unique correction:
`\mathcal{X} \times_Y V` → `\mathcal{X} \times_{\mathcal{Y}} V`.

## `MC-STK-ERR-0028` — `P12-ERR-0009`

The two cartesian diagrams at lines 1073–1088 identify the spaces exactly:

- top left: `|\mathcal{X} \times_Y Z|`;
- top right: `|\mathbf{A}^n \times \mathcal{X}|`;
- bottom right: `|\mathbf{A}^n \times Y|`.

Thus the closed subset `T` at line 1096 belongs to the top-left space. Its
closed extension `T'` at line 1097 belongs to the top-right space, and the
closedness hypothesis from line 1061 applies to its image in the bottom-right
space at line 1098. The three printed expressions respectively drop
`mathcal`, put `T'` in the bottom-right space, and put its image in an
undeclared plain-`X` space.

This is one linked diagram-typing unit. Corrections:

1. line 1096: `|X \times_Y Z|` → `|\mathcal{X} \times_Y Z|`;
2. line 1097: `|\mathbf{A}^n \times Y|` →
   `|\mathbf{A}^n \times \mathcal{X}|`;
3. line 1098: `|\mathbf{A}^n \times X|` →
   `|\mathbf{A}^n \times Y|`.

## Boundary and next gate

All thirteen units are proved against exact frozen bytes and may enter an R2
candidate. They remain unapplied here. R2 still requires its own exact payload,
source map, structural checks, authority/candidate builds, visual QA,
manifest, independent replay, separate admission commit, and public-byte
readback. Chapter 103 hypotheses remain a separate unproved queue.
