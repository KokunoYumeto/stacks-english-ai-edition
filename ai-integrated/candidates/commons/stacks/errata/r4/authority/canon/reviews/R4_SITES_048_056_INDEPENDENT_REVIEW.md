# R4 independent review: SITES-048--056

## Disposition

All nine hypotheses are **ACCEPTED**.

| ID | Verdict | Smallest exact repair |
|---|---|---|
| SITES-048 | ACCEPTED | At line 8278, change `Then the the category` to `Then the category` (delete one `the `). |
| SITES-049 | ACCEPTED | At line 8397, change `product` to `products` (add `s`). |
| SITES-050 | ACCEPTED | At line 8497, change `Condition (2)` to `Condition (3)`. |
| SITES-051 | ACCEPTED | At line 8498, change `discrete` to `chaotic`. |
| SITES-052 | ACCEPTED | At line 8585, change `The first equality since` to `The first equality holds since` (insert `holds `). |
| SITES-053 | ACCEPTED | At line 8618, change `i_*E(v(u(U)) =` to `i_*E(v(u(U))) =` (insert one `)`). |
| SITES-054 | ACCEPTED | At line 8623, delete `which is equal to `, leaving `the formula for $(v \circ u)^pE$`. |
| SITES-055 | ACCEPTED | At line 8629, change `\mathcal{F}_q` to `\mathcal{F}_p`. |
| SITES-056 | ACCEPTED | At line 8805, change `j^{-1}` to `j_U^{-1}`. |

## Frozen identities and scope

The intake was read completely, and both required identities were recomputed
from the files before review.

| Artifact | Exact path | Bytes | SHA-256 | Additional identity |
|---|---|---:|---|---|
| Frozen authority | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sites.tex` | 424197 | `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D` | 11860 lines; Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14` |
| Frozen intake | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\canon\control\ERRATA_R4_SUPPLEMENT_SITES_048_056_20260822.json` | 6543 | `DB838FCB2CDCF673392E58861458AAA52504AD00439F7EA55A8CCF07C8B634F2` | Schema `stacks-english-ai-errata-intake/v1`; nine hypotheses, SITES-048--056 |

The mathematical and editorial review used only the cited contexts and local
definitions in that exact `sites.tex`. No other authority source was used.

## Per-hypothesis proof and adverse readings

### SITES-048 -- ACCEPTED

Line 8278 literally reads `Then the the category of neighbourhoods of $p$ is
cofiltered`. The adjacent duplicate definite articles have no syntactic or
mathematical role. Deleting either occurrence yields the same byte sequence,
`Then the category ...`, and is the smallest repair.

Adverse reading considered: repeated words can sometimes be deliberate across
a quotation or nested construction. Here both tokens govern the single noun
`category`, with no intervening constituent, so that reading is unavailable.

### SITES-049 -- ACCEPTED

The governing criterion is Proposition `\ref{proposition-point-limits}` at
lines 8310--8317: the site has finite limits (explained there as fibre products
and a final object), and the functor must commute with finite limits. In this
example, `X` is final in `X_{Zar}` and the displayed definition gives
`u(X) = \{*\}`. Products and fibre products are intersections of opens, and
membership of `x` gives the required bijections. Coverings become surjective
families as stated on line 8398. Thus the functor satisfies the criterion.

The wording defect is the anomalous singular count noun in `commutes with
product and fibred products`. The same file's parallel point example at lines
8463--8465 says `commutes with products and fibred products`. Adding the single
letter `s` at line 8397 supplies the exact internally attested wording and is
smaller than expanding the sentence to name the final object separately.

Adverse reading considered: `product` can sometimes denote a named operation
in the singular, as in `tensor product`. That reading would make the phrase
recoverable, but here bare `product` is coordinated with plural `fibred
products`, while the exact parallel construction uses `products`. This is
sufficient evidence of an accidental number error, not a failure of the
underlying example.

### SITES-050 -- ACCEPTED

Definition `\ref{definition-point}`, lines 7895--7903, assigns:

1. covering-surjectivity to condition (1);
2. the covering/fibre-product bijections to condition (2); and
3. left exactness of `\mathcal{F} \mapsto \mathcal{F}_p` to condition (3).

Lines 8495--8497 already discharge conditions (1) and (2) because the only
coverings are identity maps. The following equation
`\mathcal{F}_p = \mathcal{F}(U_0)` and the exactness of evaluation prove the
remaining stalk-exactness condition, hence condition (3). Replacing only the
digit `2` by `3` is exact and minimal.

Adverse reading considered: the second reference cannot restart numbering in
an unstated auxiliary list. Its sentence explicitly continues the immediately
preceding reference to Definition `\ref{definition-point}`, and its proof
content has the type of condition (3), not condition (2).

### SITES-051 -- ACCEPTED

The example begins at line 8492 with `the chaotic topology` and cites Example
`\ref{example-indiscrete}`. That defining example, lines 820--825, says that
the coverings are the isomorphisms and calls the resulting topology `chaotic
or indiscrete`. Line 8496 again describes exactly those identity coverings.
Consequently `since the topology is discrete` on line 8498 contradicts the
authority's own local terminology. Replacing `discrete` with `chaotic` repeats
the term used in the opening sentence and is the smallest unambiguous repair.

Adverse reading considered: terminology for extreme Grothendieck topologies
can vary between authors. That cannot rescue this occurrence because the same
file explicitly fixes both the definition and its accepted names, and
`discrete` is not one of them here. `Indiscrete` would also match the defining
example, but `chaotic` is the exact term already bound at line 8492.

### SITES-052 -- ACCEPTED

Lines 8582--8584 display three equalities. The next text is intended to assign
a reason to each: `The first equality since ...`, `the second equality by ...`,
and `the third by ...`. In a full sentence beginning `The first equality`, the
first clause lacks a predicate. Inserting `holds ` produces `The first equality
holds since $f^{-1} = u_s$` and leaves both the mathematical reference and the
parallel explanation intact.

Adverse reading considered: terse mathematical lists sometimes omit repeated
verbs, but there is no preceding governing verb here from which the first
clause can inherit one; it starts a new sentence after the display. The later
ellipses can inherit `holds`, which is why the one insertion is sufficient.

### SITES-053 -- ACCEPTED

The exact line 8618 is

```tex
g_*i_*E(U) = i_*E(v(u(U)) = \Mor_{\textit{Sets}}(v(u(U)), E)
```

It contains seven opening parentheses and six closing parentheses. More
specifically, `i_*E(` opens evaluation of the sheaf `i_*E`; `v(` and `u(` open
the argument, but the two printed closing parentheses close only `u` and `v`.
One final parenthesis is required to close evaluation by `i_*E` before the
equality sign.

This is also forced by the cited construction at lines 3048--3052,
`i_*E = (U \mapsto \Mor_{\textit{Sets}}(U,E))`. The corrected term is
`i_*E(v(u(U)))`, after which both that term and the whole displayed equality
are delimiter-balanced. Inserting exactly one `)` after `v(u(U))` is minimal.

Adverse reading considered: the missing delimiter cannot be supplied by the
closing parenthesis on the Hom term, because that parenthesis belongs to a
separate expression after an equality sign. Nor is juxtaposition intended:
the same-file definition makes `i_*E` a presheaf being evaluated at the set
`v(u(U))`.

### SITES-054 -- ACCEPTED

After the SITES-053 repair, the display says

```tex
g_*i_*E(U) = \Mor_{\textit{Sets}}(v(u(U)), E).
```

Set `w = v \circ u`, as lines 8515--8518 do. Equation
`\ref{equation-skyscraper}`, lines 7947--7953, defines

```tex
w^pE(U) = \Mor_{\textit{Sets}}(w(U), E)
         = \Mor_{\textit{Sets}}(v(u(U)), E).
```

Thus the displayed Hom expression is exactly the formula for
`(v \circ u)^pE`. The current text, `the formula for which is equal to ...`,
has neither a complement for `for` nor an antecedent for `which`. Deleting
`which is equal to ` binds `formula for` directly to `(v \circ u)^pE`; line
8627 then states the resulting functor equality. This deletion changes no
mathematics and is the smallest complete repair.

Adverse reading considered: one could insert a noun phrase before `which`, for
example another occurrence of `g_*i_*E`. That would say the display is the
formula for the very expression on its left and then repeat the functor
equality on line 8627. The direct binding to the independently identified
skyscraper formula is both shorter and better supported by the cited equation.

### SITES-055 -- ACCEPTED

Lines 8562--8569 fix the types:

```text
u : C -> D,
v : D -> Sets gives the point q of D,
v o u : C -> Sets gives the point p of C.
```

In the second proof, `g : S -> C` and the point morphism `i` produce
`g_*i_* = (v \circ u)^p = (v \circ u)^s`, a functor from sets to sheaves on
`C`. Its left adjoint therefore has domain `Sh(C)` and is the stalk functor
associated to `v \circ u`, namely `\mathcal{F} \mapsto \mathcal{F}_p`.
The printed `\mathcal{F}_q` would instead require `\mathcal{F}` to be a sheaf
on `D`; it is ill-typed in this sentence. Line 8630 immediately confirms the
result by naming the same stalk functor `p^{-1}`. Changing only the subscript
`q` to `p` is minimal.

Adverse reading considered: there is no implicit pullback of `\mathcal{F}` from
`C` to `D` in the adjunction statement, and no notation marking one. Although
`q` is the starting point used to construct `p`, its stalk is the right-hand
factor in the later composite `q^{-1} \circ f^{-1}`, not the left adjoint of
`g_*i_*`.

### SITES-056 -- ACCEPTED

Lemma `\ref{lemma-point-localize}`, lines 8667--8686, defines the localization
morphism

```text
j_U : Sh(C/U) -> Sh(C)
```

and constructs `q : Sh(pt) -> Sh(C/U)` with `j_U \circ q = p`. The proof of
Lemma `\ref{lemma-points-above-point}` repeats that identity at line 8761 and
the diagrams at lines 8780--8782 explicitly use `j_U^{-1}`. Contravariance of
inverse image therefore gives the typed equality

```text
p^{-1} = q^{-1} o j_U^{-1}.
```

The unindexed `j` in `q^{-1} \circ j^{-1} = p^{-1}` at line 8805 is not
defined in the local context. Inserting `_U` identifies the already defined
morphism and makes the equation match both the diagram and the lemma.

Adverse reading considered: a reader can infer that bare `j` abbreviates
`j_U`, but the proof never declares that abbreviation, while every surrounding
formula retains the index. Recoverability does not make the printed morphism
identity exact; the two-character index insertion is the smallest repair.

## Aggregate

| Reviewed | Accepted | Rejected | Deferred |
|---:|---:|---:|---:|
| 9 | 9 | 0 | 0 |

Terminal aggregate: **SITES-048--056: 9 ACCEPTED, 0 REJECTED, 0 DEFERRED**.
