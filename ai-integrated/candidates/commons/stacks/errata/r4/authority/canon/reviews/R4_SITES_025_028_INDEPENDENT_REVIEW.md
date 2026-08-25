# R4 independent review: SITES-025 through SITES-028

Review date: 2026-08-22

## Scope and frozen identities

This review is limited to SITES-025, SITES-026, SITES-027, and SITES-028. It uses only the frozen intake and the exact local source contexts and definitions in the frozen <code>sites.tex</code> authority. No authority, translation, intake, ledger, Git state, or other shared file was modified.

- Frozen authority: <code><LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sites.tex</code>
  - Bytes: 424197
  - Lines: 11860
  - SHA-256: <code>07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D</code>
- Frozen intake: <code><LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\canon\control\ERRATA_R4_SUPPLEMENT_SITES_025_028_20260822.json</code>
  - Bytes: 3459
  - SHA-256: <code>6E0CCE25A4C4D921CEA70875D3C22E204C9649C4F7BD20B56E51B9C430B8FAE5</code>
- Producer-ledger snapshot declared by the frozen intake (not independently opened under this review's source boundary):
  - Path: <code><LOCAL_WORKSPACE>/03_projects/language_management/romance/03_working_translations/stacks_fr_20260821/00_control/SOURCE_DEFECT_LEDGER.csv</code>
  - Bytes: 65495
  - Rows: 159
  - SHA-256: <code>96C203A7AF6C2908EC9687E112330A7CD25219566E4F6164C20F42B0BB8C8A91</code>

## Complete verdict table

| ID | Locus and exact source | Verdict | Proof from the frozen authority | Adverse evidence considered | Smallest correction |
|---|---|---|---|---|---|
| SITES-025 | <code>sites.tex:4479</code>: “Let <code>$\{E_i \to v(u(U))\}$</code> be a covering of <code>$U$</code> in <code>$\mathcal{E}$</code>.” | **ACCEPTED — ambient-object/target typing defect** | Lines 4468-4469 declare <code>$u:\mathcal C\to\mathcal D$</code> and <code>$v:\mathcal D\to\mathcal E$</code>; line 4478 declares <code>$U\in\operatorname{Ob}(\mathcal C)$</code>. Definition 4251-4260 says that the cover used to test cocontinuity has the image object as its target. The displayed arrows at line 4479 all target <code>$v(u(U))\in\mathcal E$</code>, and lines 4480-4481 apply cocontinuity of <code>$v$</code> to exactly that cover. Thus it must be a covering of <code>$v(u(U))$</code>, not of <code>$U$</code>. | Even if the underlying categories happened to share an object denoted <code>$U$</code>, no equality <code>$U=v(u(U))$</code> is declared. More decisively, a family said to cover <code>$U$</code> would have target <code>$U$</code>, while the written family has target <code>$v(u(U))$</code>. This does not defeat the defect finding. | Replace only “of <code>$U$</code>” by “of <code>$v(u(U))$</code>”: “Let <code>$\{E_i \to v(u(U))\}$</code> be a covering of <code>$v(u(U))$</code> in <code>$\mathcal{E}$</code>.” |
| SITES-026 | <code>sites.tex:4801</code>: “shouldn't any covering of <code>$U\cap Z$</code> it come from a covering” | **ACCEPTED — editorial duplicate subject** | The interrogative already has the subject noun phrase “any covering of <code>$U\cap Z$</code>”. The later “it” supplies a second subject before “come”. Deleting “it” produces the grammatical “shouldn't any covering of <code>$U\cap Z$</code> come from a covering”, which connects directly to “of <code>$U$</code> in <code>$X$</code>?” on line 4802. | The intended meaning is recoverable and the mathematics in lines 4802-4814 is unaffected. That limits the defect to prose editing; it does not make the duplicate pronoun correct. | Delete the single word “it” (and its following space). |
| SITES-027 | <code>sites.tex:4935</code>: <code>$\{v(V_j) \to v(u(U))\}_{i \in I}$</code> | **ACCEPTED — mathematical index-binding defect** | Line 4934 introduces <code>$\{V_j\to u(U)\}_{j\in J}$</code>. Definition 2524-2535 states that a continuous functor sends a covering family to the image family with the same index set. Hence applying continuous <code>$v$</code> yields <code>$\{v(V_j)\to v(u(U))\}_{j\in J}$</code>. In the printed subscript, <code>$i$</code> and <code>$I$</code> are unintroduced while the member index <code>$j$</code> is not bound. Lines 4937-4944 continue consistently with <code>$W_j$</code>, <code>$p_j$</code>, and <code>$V_j$</code>. | A deliberate reindexing could in principle introduce <code>$i\in I$</code>, but the source declares no reindexing or map between index sets, and it leaves <code>$j$</code> in every family member. There is therefore no source-supported reading that binds the displayed family as written. | Replace only the subscript <code>$_{i \in I}$</code> by <code>$_{j \in J}$</code>. |
| SITES-028 | <code>sites.tex:4956</code>: “then <code>$u$</code> is cocontinous.” | **ACCEPTED — editorial terminology misspelling** | The term is defined as “cocontinuous” at lines 4251-4255. The same adjoint implication is stated with that spelling at line 4830, and the lemma invoked at lines 4955-4956 concludes “<code>$u$</code> is cocontinuous” at line 4925. The form “cocontinous” at line 4956 is therefore a local misspelling of the defined adjective. | TeX accepts the prose token and the intended term remains obvious, so there is no formal or mathematical ambiguity. That makes the correction editorial only, not unnecessary. | Replace “cocontinous” by “cocontinuous”. |

## Aggregate disposition

- ACCEPTED: 4
- REJECTED: 0
- DEFERRED: 0
- Accepted defect classes: 2 mathematical typing/index-binding defects (SITES-025, SITES-027); 2 editorial prose/terminology defects (SITES-026, SITES-028).

All four verdicts are independently determined from the frozen <code>sites.tex</code> source. None depends on producer-ledger contents beyond the intake's frozen provenance statement.
