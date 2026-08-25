# R4 independent review: SITES-029 through SITES-033

Review date: 2026-08-22

## Frozen scope and identities

Line references below are one-based references to the frozen authority.

| Item | Frozen identity | Verification |
|---|---|---|
| English authority | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sites.tex`; 424,197 bytes; 11,860 lines; SHA-256 `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D` | Observed byte count, line count, and SHA-256 match the frozen identity exactly. |
| Frozen intake | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\canon\control\ERRATA_R4_SUPPLEMENT_SITES_029_033_20260822.json`; 4,231 bytes; SHA-256 `1D69996094C21526691FD1FEC2B547CB852300DEE17A06CFC6C512B3779F0256` | Observed byte count and SHA-256 match the frozen identity exactly. |
| Producer-ledger anchor carried by the intake | `<LOCAL_WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/00_control/SOURCE_DEFECT_LEDGER.csv`; 67,375 bytes; 164 rows; SHA-256 `C5A2CCF1024527E1BA5318E39365513D8529A7CDFD565EBDB10CA9E19AE25399` | Recorded as intake provenance only. It was not opened or independently rehashed because this review's evidentiary scope is `sites.tex` only. |

The review inspected the five cited loci and only directly relevant definitions and usages in `sites.tex`. It did not modify the authority, translation, intake, producer ledger, Git state, or any shared artifact.

## Verdict table

| ID | Verdict | Defect class | Typed/editorial proof from the frozen authority | Smallest correction |
|---|---|---|---|---|
| SITES-029 | **ACCEPTED** | Index identity / typing | Lines 1694-1698 introduce a covering-indexed family `(s_j)`, project it to `(s_{j, i})`, and state `s_{j, i} = s_i|_{V_j}`. Thus, for `\phi : i \to i'`, the local equality needed at lines 1699-1703 is `\mathcal F(\phi)(s_{j,i}) = s_{j,i'}`. The forms `s_{i,j}` and `s_{i',j}` at line 1702 were never introduced and reverse the already fixed roles of `j` and `i`. | At line 1702 replace `$s_{i, j}$ and $s_{i', j}$` with `$s_{j, i}$ and $s_{j, i'}$`. |
| SITES-030 | **ACCEPTED** | Editorial grammar / quantifier attachment | In lines 1968-1971 the quantified things must be the displayed covering families `\{U_i \to U\}`, because that same family supplies the domain object `U` and factors `U_i` in the following map. The source consistently writes such a family as itself being a covering (for example lines 1693 and 1950). The phrase `coverings of \{U_i \to U\}` instead treats an already displayed covering family as an object being covered and has no defined role in the predicate. | At line 1970 delete `of`, yielding `for all coverings $\{U_i \rightarrow U\}$`. |
| SITES-031 | **ACCEPTED** | Direction of map / colimit typing | Lines 1731-1734 define `\mathcal F^+(U)` as a colimit of the sets `H^0(\mathcal U,\mathcal F)`, so its structure maps run from each `H^0` set into `\mathcal F^+(U)`. Lines 1933-1944 make this direction explicit: every plus-section *arises from* an `H^0` element. At lines 1997-2008, `s,s'` lie in `\mathcal F^+(U)` and the finer covering produces one matching family in `H^0(\{W_{jk}\to U\},\mathcal F)` representing both. There is no constructed reverse map from `\mathcal F^+(U)` to that `H^0` set. | At lines 2009-2010 replace `map to the same element of` with `are the images of the same element of`. |
| SITES-032 | **ACCEPTED** | Domain typing | Lines 1657 and 1673-1675 state the sheaf-condition map with its exact type: `\mathcal F(U) \to H^0(\mathcal U,\mathcal F)`. At line 2037, `\mathcal F` denotes a presheaf while `H^0(\mathcal U,\mathcal F)` is a set, so the printed arrow has mismatched object levels. The object `U` is already bound in line 2038. | At line 2037 replace the domain `$\mathcal F$` with `$\mathcal F(U)$`. |
| SITES-033 | **ACCEPTED** | Functor notation / typing | The arrow `\mathcal F \to \mathcal F^+` denotes the canonical natural map of presheaves (lines 1777-1779), not the endofunctor whose preservation of finite limits the proof needs. The parenthetical at lines 2150-2151 explicitly says the subject is a functor from presheaves to presheaves. The authority itself names that functor as `\mathcal F \mapsto \mathcal F^+` at lines 5349-5352. | At line 2149 replace `\to` with `\mapsto`, yielding `$\mathcal F \mapsto \mathcal F^+$`. |

## Adverse-evidence review

No contrary evidence was strong enough to reject or defer any candidate.

| ID | Strongest plausible contrary reading | Why it does not defeat the verdict |
|---|---|---|
| SITES-029 | The two subscripts might be freely reorderable notation. | They are not free: lines 1695 and 1698 explicitly define and reuse the order `(j,i)`, with `j` the covering index and `i` the diagram index. Both indices remain simultaneously bound at line 1702. |
| SITES-030 | “Coverings of X” is sometimes grammatical. | It is grammatical when `X` is an object or site. Here `X` would be the displayed family that is itself the covering, and no covering-of-a-covering datum enters the definition or the displayed injectivity map. |
| SITES-031 | “Map to” might be informal shorthand for choosing a representative. | The colimit construction provides no canonical choice of representative and no reverse map to a selected `H^0` object. The proof constructs a common representative and sends it forward to both plus-sections. |
| SITES-032 | `\mathcal F` might be shorthand for its sections over the currently understood `U`. | The same local development distinguishes the presheaf `\mathcal F` from its value `\mathcal F(U)` and prints the correctly typed map at lines 1657 and 1675. Suppressing `(U)` here changes the categorical level of the domain. |
| SITES-033 | The arrow might intentionally foreground the natural transformation. | A natural transformation does not itself serve as the stated functor from presheaves to presheaves, and the finite-limit argument concerns the plus endofunctor. Lines 5349-5352 independently use the required `\mapsto` notation for that exact functor. |

## Aggregate disposition

| Disposition | Count |
|---|---:|
| ACCEPTED | 5 |
| REJECTED | 0 |
| DEFERRED | 0 |
| **Total** | **5** |

Defect-class totals are one index-identity defect, one editorial-grammar defect, one map-direction defect, one domain-typing defect, and one functor-notation defect. Every accepted correction is local and preserves the surrounding mathematical argument. This review authorizes no mutation of the frozen English authority; it records corrections for the separate admission workflow only.
