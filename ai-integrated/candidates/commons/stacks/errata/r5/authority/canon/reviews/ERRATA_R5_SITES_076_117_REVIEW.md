# R5 Sites proof and deduplication review

Date: 2026-08-22

Frozen authority: `sites.tex`, 424,197 bytes, SHA-256
`07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D`,
Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`.

This is a canon-side, read-only proof review of producer hypotheses
`SITES-076`--`SITES-117`. It is outside the frozen R4 candidate. The review was
independently repeated in two bounded passes for `SITES-099`--`SITES-117`.
No upstream source, canonical translation, or admitted overlay was changed.

Disposition: 38 new accepted units, 42 nonoverlapping operations; three
rejections (`SITES-085`, `SITES-095`, `SITES-116`); one exact prior-R4 alias
(`SITES-077` = `SITES-047` / `MC-STK-ERR-0189`); and one repeated incoming
packet for `SITES-097`, counted once. Diagnostic replay of only the 42 accepted
operations produces 424,291 bytes, SHA-256
`9B11C7525C7A23CD8732FDC204E5F62B66892969B08087CE26EC194F85073499`.
The stable IDs below are the source-order R5 allocation after admitted R4 ends
at `MC-STK-ERR-0216`; they become final only after the R5 lease transition.

## Accepted units

| Stable ID | Producer ID | Locus | Exact correction | Proof / adverse evidence |
|---|---|---|---|---|
| MC-STK-ERR-0217 | SITES-076 | 6513 | `\times_{h_{u(V'), c'}^#}` -> `\times_{h_{u(V')}^#, c'}` | Line 6515 identifies `h_{u(V')}^#` as the fibre-product base; `c'` is its structure map, not part of the representable subscript. |
| MC-STK-ERR-0218 | SITES-078 | 6821--6822 | `has a final object, namely` -> `has an object, namely` | Objects allow arbitrary `psi:u(U')->u(U)`, which need not lift as `u(alpha)`; `(U,id)` therefore need not be final. The limit projection uses only that it is an indexed object. |
| MC-STK-ERR-0219 | SITES-084 | 7054 | `Denote $g` -> `Denote by $g` | Required English construction. |
| MC-STK-ERR-0220 | SITES-079 | 9140 | sentence-initial `let` -> `Let` | Capitalization repair. |
| MC-STK-ERR-0221 | SITES-080 | 9224 | `The first equality since` -> `The first equality holds since` | Restores the missing predicate; distinct from the analogous R4 defect at line 8585. |
| MC-STK-ERR-0222 | SITES-082 | 9316, 9324, 9418 | all three `distinct image` -> `distinct images` | Each occurrence has plural objects; correcting only the reported last occurrence would leave two identical defects. |
| MC-STK-ERR-0223 | SITES-081 | 9349 | `g_{ii'}` -> `f_{ii'}` | The refining system is introduced and used with transition maps `f_{ii'}`; `g` is undefined here. |
| MC-STK-ERR-0224 | SITES-083 | 9443 | `\coprod h_{U_i}` -> `\coprod h_{U_i}^#` | The coproduct is asserted in `Sh(C)`, but representables need not be sheaves on a general site; line 9170 supplies the exact sheafified analogue. |
| MC-STK-ERR-0225 | SITES-086 | 9533 | `enough contractible objects` -> `enough weakly contractible objects` | Only weakly contractible objects are defined and proved sufficient in the section. |
| MC-STK-ERR-0226 | SITES-087 | 9841 | `be maps of sheaves` -> `be a map of sheaves` | Singular morphism `alpha` requires a singular predicate complement. |
| MC-STK-ERR-0227 | SITES-088 | 9864--9866 | `and coverings countable families` -> `, with coverings the countable families` | Repairs the malformed site definition while preserving jointly-surjective countable families. |
| MC-STK-ERR-0228 | SITES-089 | 9949 | `applied the empty covering` -> `applied to the empty covering` | Missing preposition. |
| MC-STK-ERR-0229 | SITES-090 | 10015 | `is still a covering of` -> `is still a covering of $u(U)$` | The sentence lacks its covered object; every displayed composite targets `u(U)`. |
| MC-STK-ERR-0230 | SITES-091 | 10042 | `by a diagram` -> `be a diagram` | Required infinitive after `Let`. |
| MC-STK-ERR-0231 | SITES-092 | 10057 | `\colim^{PSh}` -> `\colim^{Psh}` | Line 10046 and adjacent uses establish the case-sensitive `Psh` notation; only line 10057 is wrong. |
| MC-STK-ERR-0232 | SITES-110 | 10285 | `two morphism of` -> `two morphisms of` | Number agreement. |
| MC-STK-ERR-0233 | SITES-111 | 10326 | `which agrees` -> `which agree` | The antecedent is the plural pair of pushforward and pullback functors. |
| MC-STK-ERR-0234 | SITES-112 | 10329 | `of a space, works` -> `of a space works` | The comma incorrectly separates subject from predicate. |
| MC-STK-ERR-0235 | SITES-113 | 10384 | `trying the define` -> `trying to define` | Lexical typo. |
| MC-STK-ERR-0236 | SITES-093 | 10462 | `the structure` -> `de structure` inside the quoted French phrase | Primary French grammar is `espece de structure algebrique`; English `the` corrupts the quotation. |
| MC-STK-ERR-0237 | SITES-094 | 10463 | `projectives finie` -> `projectives finies` | The adjective agrees with plural `limites`. |
| MC-STK-ERR-0238 | SITES-114 | 10478--10479 | `from $\Sh(\mathcal D) \to \Sh(\mathcal C)$` -> `$\Sh(\mathcal D) \to \Sh(\mathcal C)$` | Removes the duplicated direction syntax while retaining the typed arrow. |
| MC-STK-ERR-0239 | SITES-099 | 10545--10546 | `pair $(\mathcal F,\cdot)$` -> `triple $(\mathcal F,\cdot,1)$`; `with suitable axiom` -> `with suitable axioms` | Multiplication alone gives at most a semigroup object. A monoid object requires a unit and associativity/unit laws; the adjacent group and unital-ring descriptions confirm this convention. The adverse reading that the unit is hidden inside one existential axiom conflicts with the finite-limit equational presentation used here. |
| MC-STK-ERR-0240 | SITES-096 | 10549 | `An sheaf` -> `A sheaf` | Article agreement. |
| MC-STK-ERR-0241 | SITES-115 | 10605--10606 | `is the set` -> `are the set` | Smallest subject-verb repair for plural `The global sections ...`; recasting to `The set of global sections ... is` is equivalent but larger. |
| MC-STK-ERR-0242 | SITES-098 | 10622 | `be objects of` -> `be morphisms of` | `a,b:V->U` are parallel arrows, and the coequalizer plus pullbacks `a^*,b^*` require morphisms. |
| MC-STK-ERR-0243 | SITES-097 | 10761 | `of ringed topoi` -> `of topoi` | This base-change diagram uses only ordinary topoi and `f_*`,`g^{-1}`; the parallel remark at 10735 says `topoi`. The genuinely ringed-topoi occurrence at 10859 remains unchanged. |
| MC-STK-ERR-0244 | SITES-104 | 11272--11274 | `such that $S$ the image of $h_{U_i}\to h_U$ is contained` -> `such that the sieve generated by the $f_i$ is contained` | Removes malformed/shadowed `S` and uses the exact preceding definition of the sieve generated by a covering family. |
| MC-STK-ERR-0245 | SITES-105 | 11276, 11278 | insert `the image of` before both `h_{U_{ij}}\to h_{U_i}` and `h_{U_{ij}}\to h_U` containment clauses | A morphism is not literally a subpresheaf; its image is. “Factors through” is an equivalent reading, but image wording is the smallest typed local correction. |
| MC-STK-ERR-0246 | SITES-106 | 11293 | `In stead` -> `Instead` | Spelling. |
| MC-STK-ERR-0247 | SITES-107 | 11299 | `$T\in\mathcal U$` -> `$T\in\mathcal C$` | `C` is the ambient category in which the sieve is evaluated; `mathcal U` is undefined as a category here. |
| MC-STK-ERR-0248 | SITES-108 | 11303--11304 | `f_i\circ\alpha_{i'}'` -> `f_{i'}\circ\alpha_{i'}'` | The second factorization is indexed by `i'`; the printed `f_i` defeats and mistypes the comparison. |
| MC-STK-ERR-0249 | SITES-117 | 11343--11351 | `be two coverings defining` -> `be two sets of coverings defining` | Each `Cov_k(C)` is a set/system of covering families, as stated at 11224--11230 and 11354--11356, not one covering. |
| MC-STK-ERR-0250 | SITES-109 | 11363 | `add to $\mathcal C$ any set of families` -> `add to $\text{Cov}(\mathcal C)$ any set of families` | Covering families enlarge the coverage, not the objects/morphisms of `C`. |
| MC-STK-ERR-0251 | SITES-100 | 11503 | `{categories-lemma-functorial-colimit}` -> `\ref{categories-lemma-functorial-colimit}` | The exact label exists in `categories.tex`; without `ref` TeX prints the key literally and creates no cross-reference. |
| MC-STK-ERR-0252 | SITES-101 | 11598 | codomain `L\mathcal F` -> `\mathcal F` in `Mor_{PSh(C)}(S'',-)` | The representatives are maps into `F`; equality after refinement must hold before applying `L`. Equality in `LF` is already the assumption and would not prove separatedness. |
| MC-STK-ERR-0253 | SITES-102 | 11606 | `\Mor_\mathcal C(S,L\mathcal F)` -> `\Mor_{\textit{PSh}(\mathcal C)}(S,L\mathcal F)` | Both arguments are presheaves, not objects of `C`. |
| MC-STK-ERR-0254 | SITES-103 | 11626 | `choice$ V'` -> `choice $V'` | Missing text/math boundary space. |

## Exclusions and aliases

- `SITES-077`: exact alias of admitted R4 `SITES-047` /
  `MC-STK-ERR-0189`, same line-6569 `over $U'$` -> `over $u(U')$` operation.
- `SITES-085`: rejected. `V_j` versus `V_i` is an unbound dummy-index rename;
  it changes neither the family, type, proof, nor rendering.
- `SITES-095`: rejected. Types already force the unique composite
  `+ o (lambda_r x lambda_r') o Delta`; added parentheses are optional clarity,
  not a proved defect.
- `SITES-116`: rejected. `J` is fixed immediately before the clause, so
  `Sh(C)` is unambiguous contextual shorthand. Explicit `Sh(C,J)` is needed
  only where `J` and `J'` are compared simultaneously.
- The second delivery of `SITES-097` is a packet-level alias of the same exact
  line-10761 operation, not another unit.

## Boundary

This review does not admit R5, mutate the upstream mirror, alter any canonical
translation, or contact Stacks maintainers. R5 candidate construction begins
only after R4 admission releases its lease and a separate R5 lease is issued.
