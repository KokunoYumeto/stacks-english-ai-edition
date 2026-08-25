# R4 independent review: SITES-065--072

## Disposition

All eight hypotheses are **ACCEPTED**.

| ID | Verdict | Smallest exact repair |
|---|---|---|
| SITES-065 | ACCEPTED | At line 7013, change `may look be a bit confusing` to `may look a bit confusing` (delete `be `). |
| SITES-066 | ACCEPTED | At lines 7213, 7215, 7217, and 7219, change each bare `Sh` in the subscript of `\Mor` to `\Sh`. |
| SITES-067 | ACCEPTED | At line 7244, change `Lemmas` to `Lemma`. |
| SITES-068 | ACCEPTED | At line 7379, change `is the one associates to` to `is the one that associates to` (insert `that `). |
| SITES-069 | ACCEPTED | At line 7930, change `determine the same object` to `determine the same element`. |
| SITES-070 | ACCEPTED | At line 7933, change `chains of identities like this` to `chains of identifications like this`. |
| SITES-071 | ACCEPTED | Across lines 7959--7960, change the sentence boundary `. The functor` to `, the functor`. |
| SITES-072 | ACCEPTED | At line 8025, insert `to be ` before `the sheaf`. |

## Frozen identities and scope

Both intakes were read completely, and the byte counts and SHA-256 identities
below were independently recomputed from the live files before review. The
authority identity agrees exactly with the identity recorded in both intakes.

| Artifact | Exact path | Bytes | SHA-256 | Additional identity |
|---|---|---:|---|---|
| Frozen authority | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sites.tex` | 424197 | `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D` | 11860 lines; Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14` |
| Frozen intake, SITES-065--067 | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\canon\control\ERRATA_R4_SUPPLEMENT_SITES_065_067_20260822.json` | 3043 | `2B4D72C1F06C2717FA02691E5661332ECC979CF28AAF6B35D37DB36B082F6E24` | 61 lines; three hypotheses |
| Frozen intake, SITES-068--072 | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\canon\control\ERRATA_R4_SUPPLEMENT_SITES_068_072_20260822.json` | 4092 | `0A8282FF73C5A301439013584E8A4F600F78CA6A9089468355069F47C07496EA` | 77 lines; five hypotheses |

The review reopened the cited contexts in that exact `sites.tex` and the local
`preamble.tex` definition which `sites.tex` inputs on line 1. It did not use a
translation, overlay, registry, or mutable upstream checkout as authority.

## Per-hypothesis proof and adverse readings

### SITES-065 -- ACCEPTED

Line 7013 reads `Some of the statements above may look be a bit confusing at
first`. After modal `may`, `look` already supplies the bare infinitive and
takes the predicative complement `a bit confusing`; the additional bare verb
`be` cannot occupy a grammatical position. Deleting `be ` yields the standard
construction `may look a bit confusing` and changes no mathematical content.

Adverse reading considered: deleting `look ` would also produce grammatical
prose, `may be a bit confusing`. It removes a meaningful perception verb and
is a larger deletion. Removing only `be ` is therefore the smallest exact
repair.

### SITES-066 -- ACCEPTED

`sites.tex` line 1 inputs `preamble.tex`, whose line 185 defines

```tex
\def\Sh{\mathop{\mathit{Sh}}\nolimits}
```

Thus `\Sh` is the project's explicit sheaf-category operator: it groups `Sh`
typographically and assigns operator math class. Bare `Sh` instead consists of
two ordinary math-letter atoms and conventionally reads as their
juxtaposition. A complete scan of the frozen `sites.tex` found 531 occurrences
of `\Sh(` and exactly four occurrences of unescaped `Sh(`; the latter are
precisely lines 7213, 7215, 7217, and 7219 in the one aligned calculation.
The surrounding statement and every adjacent category occurrence use `\Sh`.
Changing those four tokens to `\Sh` restores both the intended operator
semantics and the established typography without altering any arguments or
delimiters.

Adverse reading considered: a reader can infer that bare `Sh` informally means
the category of sheaves, so the displayed adjunction remains recoverable.
Recoverability does not make it TeX-equivalent to the defined operator: the
math atom classes and glyph grouping differ, and the four isolated spellings
are contradicted by 531 locally attested macro uses.

### SITES-067 -- ACCEPTED

The conditional at lines 7243--7249 says to first apply exactly one cited
result, `\ref{lemma-topos-good-site}`, and then exactly one separately cited
result, `\ref{lemma-morphism-topoi-comes-from-morphism-sites}`. The plural
`Lemmas` at line 7244 governs only the first, singular reference. Replacing it
with `Lemma` gives number agreement while preserving the reference and the
sequence of applications.

Adverse reading considered: the sentence ultimately invokes two lemmas, but
they occur in separately governed phrases (`first apply ...` and `then
Lemma ...`). The first plural cannot grammatically range across the intervening
`to ... and then` construction, and the second citation already has its own
singular label.

### SITES-068 -- ACCEPTED

Lines 7378--7385 identify the action of the functor
`j_{\mathcal{F}, *}` on a morphism `\varphi`. In `is the one associates to`,
the finite verb `associates` needs a relative marker after `the one`. Inserting
`that ` produces the complete predicate `is the one that associates to
\varphi ...`. The same file attests the exact construction `the functor that
associates to` at lines 379 and 4073.

Adverse reading considered: deleting `is the one ` would also leave the direct
predicate `associates to`. That rewrite is idiomatic, but it deletes a larger
constituent. Inserting `that ` is the smallest repair and retains the sentence's
original information structure.

### SITES-069 -- ACCEPTED

Equation `\ref{equation-stalk}` at line 7864 defines `\mathcal{F}_p` as a
colimit in sets. Lines 7867--7871 then state explicitly that an **element** is
represented by a triple and that equality of triples is the equivalence
relation generated by the displayed elementary relation. The proof under
review specializes this to `(h_U)_p`: line 7927 again begins `An element of
(h_U)_p is given by a triple`. Consequently two such triples represent, or
`determine`, the same **element** of that colimit set. They do not determine an
object of the indexing category; those objects are the neighbourhood pairs
`(V,y)`. Replacing only `object` by `element` makes the referent exact.

Adverse reading considered: `object` can be used informally for any
mathematical entity, so a charitable reader can recover the intended quotient
class. In this category-theoretic paragraph, however, `object` already has the
distinct technical possibility of an indexing-category object, while the
target is explicitly a set and the local definition consistently calls its
members elements. The more precise noun is therefore a correction, not a
change to the proof.

### SITES-070 -- ACCEPTED

The condition at lines 7931--7932 gives one generating identification between
representatives: an arbitrary morphism `\phi : V \to V'` relates the two
triples when the two compatibility equations hold. As lines 7869--7871 already
state, equality in the colimit is the equivalence relation **generated** by
these pairs. A general equality can therefore require a zigzag, or chain, of
such identifications. It is not a chain of identity morphisms; `\phi` is
arbitrary. Replacing `identities` with `identifications` names exactly the
steps whose equivalence closure is being taken.

Adverse reading considered: `identity` can loosely mean an equality. No
identity is displayed here, however; the prose gives a conditional relation
between representatives, and the immediately preceding local definition
calls it an equivalence relation. `Identifications` is the exact term and is a
one-word repair.

### SITES-071 -- ACCEPTED

`For any functor $u : \mathcal{C} \to \textit{Sets}$.` at line 7959 is a
prepositional introductory phrase with no main clause. The following sentence
supplies precisely the missing clause. Replacing the period by a comma and
lowercasing `The` yields one grammatical lemma statement: `For any functor
..., the functor $u^p$ is a right adjoint ...`.

Adverse reading considered: terse theorem prose sometimes uses labels or
headings without predicates, but this text is neither marked nor formatted as
one, and it sits inside a `lemma` environment as ordinary prose. Joining the
two fragments changes only the erroneous sentence boundary and preserves the
quantifier's intended scope.

### SITES-072 -- ACCEPTED

The definition at lines 8024--8026 intends to identify `p_*E = u^sE` with the
sheaf already constructed in Lemma `\ref{lemma-point-pushforward-sheaf}`. In
`we define $p_*E = u^sE$ the sheaf described ...`, the noun phrase `the sheaf`
has no syntactic link to `define`. Inserting `to be ` supplies the predicative
complement: `we define $p_*E = u^sE$ to be the sheaf described ...`. It leaves
the notation and cited construction unchanged.

Adverse reading considered: inserting only a comma before `the sheaf` could
invite an appositive reading and is fewer characters. Its attachment to an
entire displayed equality is syntactically loose and can suggest that the
equation, rather than its denoted value, is a sheaf. `To be` is the smallest
unambiguous verbal repair of the missing link asserted by the definition.

## Aggregate

| Reviewed | Accepted | Rejected | Deferred |
|---:|---:|---:|---:|
| 8 | 8 | 0 | 0 |

Terminal aggregate: **SITES-065--072: 8 ACCEPTED, 0 REJECTED, 0 DEFERRED**.
