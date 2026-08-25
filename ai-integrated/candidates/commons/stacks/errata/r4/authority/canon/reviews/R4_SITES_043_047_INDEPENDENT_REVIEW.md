# Independent canon review: SITES-043--SITES-047

Review date: 2026-08-22  
Scope: the five frozen hypotheses SITES-043 through SITES-047 only.

## Frozen identities

- English authority: `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sites.tex`
  - 424197 bytes
  - 11860 lines
  - SHA-256 `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D`
- Frozen intake: `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\canon\control\ERRATA_R4_SUPPLEMENT_SITES_043_047_20260822.json`
  - 4219 bytes
  - SHA-256 `4CF58634EA3125494E75C4DB9B4C3CA7456E6295AA357B5FEA42FF9FC6757658`
- Producer ledger identity declared by the intake (the ledger was not opened): `<LOCAL_WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/00_control/SOURCE_DEFECT_LEDGER.csv`
  - 72747 bytes
  - 178 rows
  - SHA-256 `761241716C058F163DD4197F0E40480E7C284A67559CC3188F9D355697EE2360`

The authority's measured byte count, line count, and SHA-256 match the identity declared in the completely read intake. Review evidence is confined to the candidate passages and relevant definitions/usages in that same frozen `sites.tex`. No source, translation, candidate overlay, registry, intake, ledger, or other shared artifact was edited.

## Review gate and SITES-044 provenance

`ACCEPTED` requires a repair forced by grammar, punctuation, terminology, or mathematical typing in the frozen authority. `REJECTED` is used for an optional improvement rather than a defect. `DEFERRED` is used only when the authority does not resolve the claim.

The intake reports that the text now numbered SITES-044 had previously appeared only as an unnumbered observation adjacent to the SITES-040 review. That observation was not treated as a verdict and the prior review was not used as evidence here. SITES-044 receives a fresh, independent, exact disposition below.

## Complete verdict table

| ID | Verdict | Source proof and type check | Strongest adverse reading considered | Smallest exact repair |
|---|---|---|---|---|
| SITES-043 | **ACCEPTED** | Lines 5980--5984 say that the sheaf is constructed by setting `\mathcal F(U)=\mathcal F_U(U)`, followed by the finite `where` clause `where restriction along $f : V \to U$ given by the commutative diagram`. The clause has a subject and passive complement but no finite copula. The diagram at lines 5985--5991 is precisely the definition of that restriction map. | One can recover the intended instruction and TeX compiles; `given by` might visually resemble a reduced passive phrase. After `where`, however, this is a finite defining clause, not a noun modifier, so the omitted `is` is grammatical rather than stylistic. | Insert `is` before `given`: `where restriction along $f : V \to U$ is given by the commutative diagram`. |
| SITES-044 | **ACCEPTED** | Line 6072 has the completed imperative declaration `Let $(s_i, \varphi_i)_{i \in I} \in \prod_i \mathcal H(V_i)$,`; line 6073 begins the independent sentence `This means ...`. A comma cannot terminate the first sentence and join it to the capitalized independent second sentence. Replacing only that punctuation restores the actual sentence boundary. | The explanation is closely related to the declaration, and the comma may have been intended to signal continuity. That relation permits a semicolon or a rewritten dependent clause, but it does not make the present comma splice valid; a period is the smallest repair. | Replace the comma at the end of line 6072 with a period. |
| SITES-045 | **ACCEPTED** | Lines 6171--6173 refer to a property of the localization functor as the noun phrase `the fully faithfulness`. `Fully` is the adverb used inside the adjectival predicate `is fully faithful`; it cannot directly modify the noun `faithfulness`. The same file consistently uses `fully faithful` for functors at lines 4670, 4737, 4756, 4772, 5921, 8712, 9560, 10092, 10223, and 10263. Nominalizing the property requires the adjective `full`: `full faithfulness`. | The intended standard concept is unmistakable, and the malformed phrase was likely produced by mechanically nominalizing `fully faithful`. Clear intent does not make the resulting noun phrase grammatical. | Replace `the fully faithfulness` with `the full faithfulness` at line 6172. |
| SITES-046 | **ACCEPTED** | Lines 6532--6534 declare `u : \mathcal C \to \mathcal D`, take `U \in \mathcal C`, and set `V=u(U)`. An object `U'/U` of `\mathcal C/U` is a morphism `U' \to U`; applying `u` gives `u(U') \to u(U)=V`, hence the object `u(U')/V` of `\mathcal D/V`. The commutative square at lines 6537--6540 forces this object map. In contrast, `V'` at line 6543 is never bound. Same-file analogous slice functors explicitly apply their functor to the numerator, for example `V'/V \mapsto u(V')/U` at lines 6266--6271 and `V/U \mapsto u(V)/u(U)` at lines 8707--8708. | A reader could silently introduce `V':=u(U')`. The lemma does not make that declaration, and silent renaming is especially unsafe inside the formula that defines the functor. The corrected object is uniquely forced by functoriality and the displayed square. | Replace `$V'/V$` with `$u(U')/V$` at line 6543. |
| SITES-047 | **ACCEPTED** | Lines 6562--6567 place the argument in `\mathcal D`: the covering `\{V_j/V \to u(U')/V\}` has underlying maps `V_j \to u(U')`, while applying `u` to `U_i' \to U'` gives `u(U_i') \to u(U')`. A refinement therefore consists of maps `\phi_i : u(U_i') \to V_{\alpha(i)}` whose composites to `u(U')` agree; they are morphisms over `u(U')`. The definition of cocontinuity at lines 4250--4260 states exactly the corresponding refinement `\{u(U_i)\to u(U)\}` of `\{V_j\to u(U)\}`. The written base `U'` belongs to `\mathcal C`, not `\mathcal D`, and no map from either displayed `\mathcal D`-object to `U'` is supplied. | `over $U'$` can be guessed as informal shorthand for “over the image of $U'$.” But the sentence explicitly types a morphism between objects of `\mathcal D`, and the very next lines use those same maps in `\mathcal D/V`; suppressing `u` names the wrong-category base. | Replace `over $U'$` with `over $u(U')$` at line 6569. |

## Aggregate

- ACCEPTED: **5** (SITES-043, SITES-044, SITES-045, SITES-046, SITES-047)
- REJECTED: **0**
- DEFERRED: **0**
- Total resolved: **5 of 5**

The five repairs above are the smallest exact corrections supported by the frozen authority. This review does not apply them to any source or derived artifact.
