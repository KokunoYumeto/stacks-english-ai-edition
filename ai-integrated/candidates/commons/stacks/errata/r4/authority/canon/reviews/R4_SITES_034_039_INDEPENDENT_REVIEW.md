# Independent canon review: SITES-034--SITES-039

Review date: 2026-08-22  
Scope: the six hypotheses SITES-034 through SITES-039 only.

## Frozen identities

- English authority: `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sites.tex`
  - 424197 bytes
  - 11860 lines
  - SHA-256 `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D`
- Frozen intake: `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\canon\control\ERRATA_R4_SUPPLEMENT_SITES_034_039_20260822.json`
  - 4238 bytes
  - SHA-256 `603D128D491DB35DE9459141EEA481F174EC1BFC7CE18F4C54F74E24973667ED`
- Producer ledger identity declared by the frozen intake (not independently opened in this review): `<LOCAL_WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/00_control/SOURCE_DEFECT_LEDGER.csv`
  - 69475 bytes
  - 170 rows
  - SHA-256 `C9B99053D7A2F4CBA89419A4922E44EF7E64A856513F378125ED6B13379348DC`

The measured authority and intake identities match their frozen expected identities exactly. Substantive review used only the cited passages and relevant same-file definitions/usages in `sites.tex`. No build, Git operation, translation read, authority edit, intake edit, or ledger edit was performed.

## Decision rule

`ACCEPTED` requires a correction forced by the frozen source's grammar, mathematical typing, or asserted relation. A merely nicer register choice, an optional normalization, or TeX-insignificant whitespace does not pass that gate. `REJECTED` means that the proposed change is not forced as a source-defect correction. `DEFERRED` is reserved for a hypothesis that cannot be resolved from the frozen authority.

## Complete verdict table

| ID | Verdict | Proof in frozen `sites.tex` | Strongest adverse evidence considered | Smallest canonical correction |
|---|---|---|---|---|
| SITES-034 | **REJECTED** | Lines 5233--5244 form a complete, valid proof transition. `OK` can operate as a discourse marker and `and` can connect the appeal to the definition with the preceding reduction. Same-file proofs also use `OK, so` at lines 9378 and 11639, so the claimed register exclusion is not supported by this authority. | Replacing `OK, and by` with `By` is shorter and more formal. That is a reasonable copyedit, but no grammar, meaning, type, or TeX output forces it. | None. Preserve the authority. The producer rewrite is optional register polishing only. |
| SITES-035 | **ACCEPTED** | At lines 5358--5363, the subordinate clause `where $j_{U!}^{PSh}\mathcal G$ the presheaf defined by the formula` has a subject and predicate complement but no finite copula. The surrounding sentence requires the definition `j_{U!}^{PSh}\mathcal G` **is** that presheaf. | The intended meaning is recoverable from the formula reference and TeX will compile, but recoverability does not supply the missing verb in the English source. | Insert `is` after `$j_{U!}^{PSh}\mathcal G$`: `where $j_{U!}^{PSh}\mathcal G$ is the presheaf defined by the formula`. |
| SITES-036 | **ACCEPTED** | Lines 5385--5389 read `The value of the presheaf ... is / on $X$ is`. The first `is` prematurely closes the subject, while `on $X$ is` supplies the required predicate. Removing the first occurrence produces the unique ordinary parse and leaves the displayed value as predicate complement. | A reader can recognize the duplicated word and reconstruct the sentence; the formula is mathematically clear. The literal source sentence nevertheless has two incompatible copulas. | Delete the first `is`: `The value of the presheaf $j_{U!}^{PSh}\mathcal{F}_\varphi$ on $X$ is`. |
| SITES-037 | **ACCEPTED** | With `f : V \to U`, lines 5467--5471 define `j : \mathcal C/V \to \mathcal C/U` and identify it with `j_{V/U}`. Hence lines 5500--5513 use `j^{-1} : \Sh(\mathcal C/U) \to \Sh(\mathcal C/V)`. The equality at line 5555 to `j_{U/V}^{-1}` reverses the defining indices. The later square at lines 6191--6202 confirms the convention: `j_{U/V}` denotes the functor `\mathcal C/U \to \mathcal C/V` associated to a morphism `U \to V`, whose inverse-image direction is opposite here. In the local hypotheses only `V \to U` is given. | Because the local symbol `j` was already defined, a reader may treat the bad subscript as an ignorable label. It is not ignorable in an asserted functor equality: under the same-file convention the named right-hand functor has the wrong direction and is not supplied by the local data. | Replace `$j_{U/V}^{-1}$` with `$j_{V/U}^{-1}$` at line 5555. |
| SITES-038 | **ACCEPTED** | Lines 5593--5600 list the functors in the order `j_{U*}, j_{U!}` and then call them `right, left adjoint` to `j_U^{-1}`. Lines 5178--5186 fix the types and explicitly identify `j_{U!}` as left adjoint; line 5535 likewise states that `j^{-1}` is right adjoint to `j_!`. The intended pairwise assignment is correct, but the comma alone neither conjoins the two complements nor marks their distribution over the ordered pair. `respectively ... and ...` states the relation unambiguously. | An expert can infer the pairwise assignment from notation and order, so there is no substantive mathematical error. That inference does not repair the under-coordinated English clause, and the proposed edit changes no mathematics. | Replace `which are right, left adjoint` with `which are respectively right and left adjoint`. |
| SITES-039 | **REJECTED** | Line 5619 contains two ASCII spaces in `\{f_i  : (W_i/V) \to (W/V)\}`. TeX treats the run as ordinary inter-token whitespace, so deleting one space changes neither tokens, typesetting, nor mathematical meaning. Same-file families at lines 6782, 6786, 6835, 6947, 6949, 6957, 10952, 11249, 11272, 11286, and 11324 use one space, establishing a cosmetic inconsistency but not a forced source correction. | The doubled space is the sole `  :` occurrence in this file and normalizing it would improve source consistency. Under the canon gate, uniqueness and neatness do not turn a TeX-insignificant whitespace edit into a defect correction. | None. Preserve the authority. Reducing the run to one space is an optional no-output-change normalization. |

## Aggregate

- ACCEPTED: **4** (SITES-035, SITES-036, SITES-037, SITES-038)
- REJECTED: **2** (SITES-034, SITES-039)
- DEFERRED: **0**
- Total resolved: **6 of 6**

Only the four accepted corrections are eligible for a later, separately authorized overlay. This review itself changes no authority or derived text.
