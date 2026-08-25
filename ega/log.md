# EGA integration log

## 2026-08-07

- [x] Correct the active scope from EGA II to the full EGA 0--IV corpus.
- [x] Create the durable 3,995-character EGA-to-Stacks goal.
- [x] Bind the read-only edition interface to sealed French printed p.19 and
  corrected English discovery manifest R184.
- [x] Repair the validator so a newer live French cursor does not invalidate
  earlier mappings bound to exact historical authority receipts.
- [x] At the first useful mechanical opportunity, launch a nonconservative
  Spark batch. Prefer independent candidate, label, manifest, schema,
  reference, inverse, or build-log shards; scale the batch rather than leaving
  the separate Spark pool idle, but never invent useless work to consume it.
- [x] For the first agent batch, record task IDs/model, exact bounded scope,
  inputs, requested output, runtime/status, returned findings, false positives,
  unexpected writes, independent verification, accepted/rejected disposition,
  visible usage when available, and the exact net effect on owner work. See
  `agent.csv`; the archived task ID is the durable pointer to its verbatim
  prompt and full result.

### Spark batch A000001--A000016

- Five disjoint manifest shards replayed all 127 R184 entries. Every path,
  byte count, and SHA-256 matched. This independently corroborates the owner
  intake replay.
- Receipt, interface, validator, ID, candidate, privacy, inverse, and diff
  audits were consumed. Accepted and rejected findings are separated in
  `agent.csv`; no agent finding was promoted without an owner check.
- Three false-discrepancy patterns were learned and bound for later prompts:
  external authority payloads must be named by exact external path; Stacks
  source labels must be normalized from `file-label` to local `label`; and
  official tags must be checked against `tags/tags`, never `cand.csv`.
- All sixteen tasks reported no filesystem writes. A fresh owner `git status`
  remains mandatory because read-only claims are not self-certifying.
- All sixteen completed Spark tasks were archived only after their results and
  owner dispositions were written to `agent.csv`.

### Statement review A000017--A000019

- Three non-overlapping read-only reviewers covered EGA I 1.1.1--1.1.15.
  Their exact task names, scopes, findings, owner checks, and dispositions are
  recorded in `agent.csv`; runtime telemetry was not exposed.
- The review produced 22 statement edges across 14 source units, eight
  explicit residuals, two exact existing-tag equivalences, and one exact
  locally integrated lemma. The local lemma has deliberately no official tag.
- The 1.1.15 reviewer also detected the printed proof's missing
  `a != A` qualification. The diplomatic French remains untouched; the
  correction is routed through `reports/findings.jsonl`.

Agents may improve throughput or independent checking; they may not decide
source authority, theorem equivalence, mathematical correctness, translation,
visual fidelity, publication, or ownership. The owner verifies every result.

### Spark batch A000020--A000027

- Eight independent audits attacked the new lemma from mathematical edge cases,
  bounded duplicate search, source conventions, use-site logic, provenance,
  statement-map semantics, validator completeness, and bounded build evidence.
- The mathematical and use-site reviews confirmed the implication chain. The
  duplicate audit found no exact named target already present in the Stacks
  source. The source-convention audit found no new formatting defect.
- The provenance review confirmed that F8 is the direct French source receipt
  for the new statement edge and `LOCAL_WORKTREE` describes only the target
  integration state. One reviewer conflated those axes; that detail was
  rejected and is retained explicitly in `agent.csv`.
- The adversarial validator review found genuine blind spots in coverage-value
  validation and relation-to-residual closure. `check.py` now fail-closes on
  those fields and on incomplete or duplicated agent records.
- Bounded serial builds of `algebra.tex` and `more-algebra.tex` completed
  without fatal errors. The new citation and local label resolve. Generated
  build logs remain ignored artifacts and are not part of the public scaffold.
- Every task result was consumed and owner-checked before archival. Exact task
  IDs, runtimes, findings, checks, dispositions, and write claims are recorded
  in `agent.csv`.

### Canonical-source correction referral

- The EGA I 1.1.15 proper-ideal proof qualification was recorded append-only
  as `EGA-I-1.1.15-PROOF-PROPER-IDEAL` in
  `reports/findings.jsonl` and sent to the bounded French-canon task.
- The dispatched file was 777 bytes with SHA-256
  `01B2E4D9AB60A6CAF880DE8EF6D38282ACD80389A4BDEE92C02F700F8AC4E993`.
  This referral proposes a corrected-layer disposition and does not alter the
  diplomatic French authority.

### Statement review A000028--A000029

- Two read-only reviewers covered every numbered unit in EGA I 1.2.1--1.2.7
  over three bounded turns. A requested third child could not be created
  because the collaboration thread limit was reached; no task or duplicate
  work was created. The completed first reviewer was reused for the remaining
  disjoint slice.
- Existing Stacks coverage is exact for the quotient-spectrum and localization
  corollaries and strictly stronger for the dense-image criterion. Spectrum
  functoriality merges continuity and the standard-open inverse-image formula.
- The residue-field naturality package and the closure-of-image formula are
  present only as prose or proof-level derivations at EGA's granularity; both
  remain explicit residuals rather than fabricated theorem equivalences.
- EGA I 1.2.4 exposed a reusable gap. The new cited but untagged Algebra lemma
  states the general unit-times-image embedding criterion and now supplies the
  common topology argument in the quotient and localization proofs.
- Direct comparison exposed two printed-source defects: the 1.2.5 reference
  to 1.1.12 must be 1.1.11 in corrected layers; and the 1.2.7 proof must use
  `X'` and `A'` in three linked places. Both were added append-only to
  `reports/findings.jsonl`; diplomatic French was not changed.
- The correction referral was delivered to the bounded canon task as a
  2,465-byte file with SHA-256
  `8C665633918EE9CC7DCAC9C4D56E63E692C56AFFEC353BF4AD89F4E5A308C1F2`.

### EGA I 1.2 integration gate

- A follow-on adversarial review under A000029 passed the new lemma and both
  refactored uses. It explicitly checked injectivity and the subspace topology;
  zero rings; localization with zero in the multiplicative set; quotient by
  the unit ideal; citation accuracy; style; and absence of circular dependence.
- Two serial `algebra.tex` passes exited zero. The new label is present in
  `algebra.aux`; neither it nor the EGA I citation is unresolved. Existing
  standalone-chapter external-reference warnings are outside this delta.
- The hardened scaffold validator passes with 9,155 units; 34 statement edges
  across 21 source units; 13 residuals; three correction findings; 29 recorded
  agent runs; and no errors.

### Spark batch A000030--A000036

- Seven read-only Spark shards covered the fourteen numbered units of EGA I
  1.3.1--1.3.14 in non-overlapping pairs. Exact task IDs runtimes returned
  findings owner checks dispositions and write claims are in `agent.csv`.
- Useful results located the compact Stacks core 01HS 01HU 01HV 01I7--01I9
  01IB--01ID 01PB and 01SA--01SB. The owner rechecked every official tag and
  direct French locus before admission.
- Three systematic false-positive classes were rejected: a larger target was
  repeatedly called partial despite full source coverage; an aggregate unit
  was called unmatched despite exact split components; and the final shard
  supplied nonexistent French source paths and overbroad sheafification tags.
- The relation rule is now explicit in `schema.md`: classify coverage from the
  source toward the target and reserve partial for an actual source remainder.
- The slice produced 22 new statement edges and 11 residuals. No printed-source
  correction and no genuine mathematical gap requiring new exposition was
  found. EGA-local saturation notation and unlabelled coherence formulas remain
  visible rather than being forced into invented tags.

### EGA I 1.4 review A000037--A000048

- Three bounded reviewers and one nested source extractor separated Theorem
  1.4.1 into exact existing ingredients. Tags 0EHM and 01P7 cover the canonical
  quasi-coherent and localization directions, but no official label packages
  the ambient-module, finite-standard-cover, quasi-coherent, and converse
  localization criterion as one statement.
- A cited local Properties lemma now records that reusable four-way
  characterization. It assigns no official tag. Two serial chapter passes exit
  zero, the local label resolves, and standalone missing-external-aux warnings
  remain outside the delta.
- EGA I Lemma 1.4.1.1 has no exact named target under its arbitrary-sheaf
  hypotheses. Its conclusion is absorbed by 01P7 in the quasi-coherent
  application and its finite gluing maneuver already appears inside existing
  proofs. It remains an explicit proof-device residual rather than a redundant
  new lemma.
- The closer target for Corollary 1.4.2 is 01PE, which works for any
  quasi-compact open immersion. Corollary 1.4.3 splits across 01SA and 01SB,
  with 01IB, 01I8, and 0H88 recorded as proof dependencies.
- Eight read-only Spark audits attacked proof logic, duplicates, source
  equivalence, Stacks conventions, map design, build evidence, source
  corrections, and validator closure. Exact task IDs, runtimes, findings,
  owner checks, accepted and rejected dispositions, and write claims are in
  `agent.csv`.
- Three Spark failures were retained rather than silently discarded: one
  conflated the new worktree label with official tag 0EHM; one could not open
  the real diff and changed the nonnegative exponent quantifier; and one
  proposed unrelated tags 01P8 and 01P9. Pinned-base `git show`, exact
  label-to-tag joins, and owner source reading closed all three.
- A proposed new correction for the printed tilde on `N` was rejected as a
  duplicate. Direct page-90 validation R13 already records the visible source
  oddity, its diplomatic preservation, and the corrected English disposition.
  No new finding row was added.
- Every completed Spark task was consumed before archival. The live French
  interface now records F19 and the E2P20 gate; the immutable F8 receipt remains
  the authority for all EGA I statement edges in this slice.

### EGA I 1.5 review A000049--A000052

- Four bounded numbered units were checked against direct French F8 and the
  pinned Stacks base. The cumulative statement map now has 72 edges across 41
  source units with 31 explicit residuals.
- Theorem 1.5.1 is fully covered but not by one tag. Tag 01XZ gives coherent if
  and only if finite type plus quasi-coherent; 0EHM 01PF 01IA and 01PB give the
  finite ambient A-module clause. The split packaging remains explicit instead
  of adding a redundant omnibus lemma.
- Corollary 1.5.2 is an affine special case of the explicit structure-sheaf
  conclusion in 01XZ. Corollary 1.5.3 is exactly derived from 01PE 01PF and
  01XZ; 0FD0 is excluded because it extends a morphism between sheaves already
  present on X. Corollary 1.5.4 is exactly tag 0GN6.
- The review exposed a genuine upstream cross-reference error in the proof of
  01PI. After the proof has established only finite type it cited 01PC to infer
  a finitely generated affine module. Pinned base and current upstream HEAD are
  identical at this locus. The branch now cites the exact finite-type criterion
  01PB; no surrounding wording changed.
- One nested source extractor claimed that printed p.93 duplicated corollary
  number 1.5.3. The owner rendered the exact NUMDAM page once at 1100 dpi and
  visibly confirmed the sequence 1.5.2 1.5.3 1.5.4; the sealed R16 receipt says
  the same. The extraction was retained and the numbering claim was rejected;
  no correction referral was created.
- The bundled `pdftoppm` wrapper failed before producing an authority image as
  it had in the predecessor workflow. One serial MiKTeX `pdftocairo` render of
  the same page succeeded. This was a read-only check and changed no edition
  file.
- Two serial `properties.tex` PDF passes exited zero. On rendered output page
  29 the repaired proof now links visibly to Lemma 17.1 rather than the
  inapplicable finite-presentation criterion. A serial 1100-dpi page review
  found no clipping overlap or changed-page layout defect; remaining undefined
  references are the ordinary standalone external-chapter references.

### EGA I 1.6 review A000053--A000055

- Eleven stable source units were checked against direct French F8: the ten
  numbered units 1.6.1--1.6.10 and displayed formula 1.6.5.1. The cumulative
  statement map now has 99 edges across 52 source units with 41 residuals.
- The exact existing core is 00E2 00E3 008H 0096 0098 01AJ 01HV 01I1 01I2
  01I8 01I9 01SB 02C6 05DQ and 0H7H. These targets distribute the spectrum
  morphism construction arbitrary localization affine pullback and pushforward
  adjunction maps tensor identities ideal and quotient base change and
  functoriality. No reusable mathematical gap or new Stacks lemma was found.
- EGA 1.6.8 only identifies the canonical internal-Hom base-change map with
  the sheaf associated to its module counterpart. It does not claim an
  isomorphism and assumes no flatness. Tag 0C6I was therefore excluded rather
  than used as an overstrong match.
- The arbitrary localization of 1.6.2 was kept distinct from the principal
  localization open-immersion result 01I3: with an infinite multiplicative set
  its image need not be open. Its induced-sheaf assertion is instead recorded
  through exact topology local-ring and stalkwise-sheaf components.
- Direct p.95--96 validation and owner reading found no source correction.
  The historical phrase `pour chaque fibre` names the stalk maps in context;
  it is not a geometric-fibre assertion. No TeX chapter changed in this slice,
  so a Stacks build or visual render would test no substantive delta and was
  intentionally omitted. The structural validator and remote identity gate
  remain mandatory before the checkpoint is reported.

### EGA I 1.7 review A000056--A000060

- Five numbered units and the labelled proof square were checked against
  direct French F8. The cumulative map has 112 edges across 58 admitted source
  units and 46 residuals. Tags 01HW 01HB 01HV 01HY 01I1 and 01I2 cover the
  affine definition recognition criterion Hom bijection and opposite-category
  equivalence. Tag 01IG is a stronger closed-immersion form of 1.7.5 and 01L6
  records its point-and-stalk proof criterion in the scheme category.
- The labelled square `I.1.7.3.diagram-fr` exposed a registry defect: intake
  recognized 15 tikz-cd environments but none of 430 active native Xy-pic
  commands. Intake v3 now registers both forms in disjoint typed namespaces
  without renumbering any old ID. Exact R184 replay passes with 9,585 units
  including 445 diagrams and copies no source prose.
- Literal presentation-independent canonicity in 1.7.1 is false: on
  `Spec(k[t])` the identity and `t -> t + 1` presentations give different
  identifications with the witness ring. Context supports the harmless
  intended meaning relative to a chosen affine presentation. The lowest-
  severity clarification was referred append-only; diplomatic French was not
  changed and the canon task owns disposition.
- The correction channel was delivered directly to the canon task as
  `reports/findings.jsonl`, 3,509 bytes, SHA-256
  `F29BF107D0A7100A6E63AFEF0E89D9C9E4D63A428F75B214A08E6689FCF3D786`.
  No source tree was mutated.
- Two exact intake replays produced identical `units.csv` SHA-256
  `7EC7BAB365BAC48101FA8C107D814CD26017A9AC728A99C1F90BD5B6908166CF`
  and `intake.json` SHA-256
  `E5C9609AD505DFDF51AE20AB50E25E44C4748B0CC67F2DCE5D479D1C8030C565`.
  The Xy-pic namespace is disjoint so all old diagram rows remain
  byte-identical; a unified diagram counter was rejected because it would have
  reassigned one previously published tikz-cd ID.
- The same audit found a pre-existing section-parser state leak. Exact R184 has
  567 legitimate labelled headings with a maximum four-line label gap; an
  unlabelled starred errata heading had remained pending for 107 lines. Intake
  now expires that state after four lines. Stable IDs are unchanged while one
  remark kind and eleven later parent links are repaired deterministically.
- No Stacks TeX changed in this slice. A chapter build or visual render would
  therefore test no substantive delta; exact intake replay structural
  validation and remote identity are the applicable gates.

### EGA I 2.1 review A000062--A000064

- Eight numbered units were checked against direct French F8 and the pinned
  Stacks base. The cumulative statement map now has 130 edges across 66 source
  units with 51 explicit residuals. No Stacks TeX changed.
- EGA's historical `prescheme` is exactly the modern unrestricted scheme in
  01IJ; no separatedness enters. Tags 00A1 and 01HW split the affine-open
  definition while 01IT exactly states that affine opens form a basis.
- Tag 01IS deliberately serves twice: it is stronger than the Kolmogorov
  assertion in 2.1.4 and exactly states the generic-point result in 2.1.5.
  Reusing one target avoids manufacturing duplicate semantic nodes.
- For irreducible X the modern rational-function ring is the generic stalk by
  01RU and the one-component specialization of 01RV. Tag 01RW was excluded:
  EGA assumes no reducedness and says ring rather than field. The historical
  notation for the ambient stalk along an irreducible closed subset remains a
  migration residual because the only nearby tagged uses are narrower.
- The locally-integral clause is exactly reconstructed from 01OQ instantiated
  with integral domains and 01OK. It was not weakened to the false criterion
  that all local rings are domains; the pinned Properties chapter itself
  records a connected affine counterexample to that shortcut.
- The proof of 2.1.5 prints X where the referent is Y. Canonical control P98
  already catalogues and diplomatically preserves the typo. The existing
  correction record was reused and no duplicate finding was created.
- No chapter build or visual render is applicable because this slice changes
  only the machine-readable comparison graph. Pinned-label replay structural
  validation privacy checks and exact remote identity remain the checkpoint
  gates.

### EGA I 2.2 review A000065--A000074

- Ten numbered units and independently labelled formula 2.2.4.1 were checked
  against direct French F8. The cumulative map has 168 edges across 77 admitted
  source units with 67 residuals. No Stacks TeX changed.
- Tags 01HB and 01IJ identify EGA prescheme morphisms with modern locally
  ringed scheme morphisms. The induced residue-field injection remains an
  explicit proof-level consequence of 07BI rather than an invented theorem.
- Tag 01I1 gives the affine-target Hom bijection for the stronger case of an
  arbitrary locally ringed source. Its proof contains formula 2.2.4.1 exactly.
  Tags 01IB 01I7 01BH and 0096 reconstruct the module mapping formula without an
  affine quasi-compact or quasi-separated hypothesis on the morphism; the
  Stacks construction does not need the source hypothesis that G is
  quasi-coherent.
- Ordinary closedness is the underlying-topological definition 005O. It was
  not conflated with a closed immersion properness or universal closedness.
  For composition the ordinary clause of 0515 gives a stronger algebraic-stack
  target; open and surjective composition use 02V2 and 01S0 while the remaining
  cancellation clauses stay explicitly derived.
- Surjectivity and dominance are local for stronger fpqc and fppf target
  topologies by 02KV and 0H8J. The arbitrary Zariski-cover specialization adds
  no finiteness condition. Tag 0H8H was excluded because it packages
  quasi-compactness with dominance.
- Tags 01RO 0BAB and 01RP give the complete birational package for schemes with
  finitely many components and no reducedness or integrality assumption. The
  graph uses the invariant bijection on component generic points; the printed
  paired indexing is retained as historical formulation rather than silently
  made ordering-dependent.
- Eight bounded Spark audits were read consumed and archived. Their useful
  target evidence was retained; an invented source label a false dense-open
  isomorphism paraphrase an unrelated topology target and a missed ordinary-
  closed clause remain append-only in A000065--A000072 and I000019--I000021.
  Two inherited-parent audits then supplied whole-section source and adversarial
  checks. Every accepted target was replayed at pinned base a04446e5.
- The live edition interface advanced independently to EGA II printed p.23
  under E2P23 and F22. Historical §2.2 evidence remains bound to immutable F8.
  No chapter build or render is applicable to this graph-only checkpoint;
  structural validation privacy checks and exact remote identity are mandatory.

### EGA I 2.3 review A000075

- Two numbered units were checked against direct French F8 and the p.101
  diplomatic gate. The cumulative map has 178 edges across 79 admitted source
  units with 71 residuals. No source diagram occurs in the bounded section and
  no Stacks TeX changed.
- Tags 01JB and 01JC split the general locally ringed gluing construction from
  the assertion that gluing schemes produces a scheme. Tag 01IT supplies the
  stronger affine-open basis used to reconstruct every scheme from its affine
  overlap data. No finiteness quasi-compactness or separatedness was imported.
- EGA 2.3.2 is exactly the projective-line example 01JE: two affine lines are
  glued along their principal punctured opens by coordinate inversion global
  functions are the ground field and the result is not affine. EGA names the
  inverse overlap direction from Stacks but the gluing datum is identical.
- The nearby doubled-origin example 01JD was rejected. It uses the identity
  transition and produces a nonseparated scheme. Confusing it with the source
  would corrupt both the semantic target and later property dependencies.
- The forward reference to the later projective-space construction is recorded
  through 01NF and 01NG as a derived documentary comparison: the pinned text
  defines Proj projective one-space and its two standard charts but has no
  separately tagged comparison with the earlier glued object.
- One exact inherited-parent audit was accepted after owner replay. A parallel
  adversarial attempt was interrupted after exceeding its bounded utility and
  returned no evidence; it produced no write and therefore receives no
  completed-run A-row. Canonical p.101 controls record no source correction.
- No chapter build or visual render is applicable to this graph-only slice.
  Pinned-label replay structural validation privacy checks and exact remote
  identity remain the checkpoint gates.

### EGA I 2.4 review A000076--A000078

- Eight numbered units and the native affine-chart triangle were checked
  against direct French F8 and the p.101--p.103 diplomatic gates. The
  cumulative map has 219 edges across 88 admitted source units with 82
  residuals. No Stacks TeX changed.
- The exact page-ledger SHA-256 identities are p.101
  `F7329A53C494396C09C8C6DED894FB40E40254977C66E25172CF50B19A3C297A`;
  p.102 `7325833EC8890A9A8A0A627E14902F5DD3160A7CD019F880A41ABAB31EA3BD7E`;
  and p.103 `B520493D1CA931E46505DACB158597147EAC7DC84B9F53EF5AFAB21771AF13A7`.
  Their R24--R26 validation SHA-256 identities are respectively
  `2B8A9A673EC9DE56E26E13566CF11568F8DD5F3474A602B95F6F7EDE6410781B`;
  `8DDC1F5216FE7D1E210C6F6AE57393F677BCDBAE965D948E5890846C59C66CF4`;
  and `E12D1BAFBF55F86BA7DC24349E7439E518A82397C649E51CA3186B13383BB78A`.
- Tags 01HW 07BI and 00E9 split the historical local-scheme definition and its
  unique closed point. Tags 01J6 and 02NA give the canonical local-spectrum
  morphism in stronger universal form. The source triangle has no identical
  tagged diagram and remains an exact derived diagram edge.
- Tags 01J7 and 00E3 separate the generalization image from its induced-
  topology homeomorphism. Tags 01HV and 02C6 prove the stalk isomorphisms.
  Tag 01L6 formally states monicity only among schemes; its proof applies
  verbatim to arbitrary ringed-space test objects and that category difference
  remains explicit rather than being silently erased.
- The component and dimension-zero criterion in 2.4.3 is reconstructed from
  00ET 00ES 00E3 00KE 04MG and locality. No Noetherian or reduced hypothesis
  is introduced and a zero-dimensional local ring is not strengthened to a
  field.
- Tag 01J6 exactly matches the local-source mapping property in 2.4.4. The
  fixed-field classification in 2.4.6 is exact prose under section tag 01J5;
  tag 01J9 was excluded because it quotients field-valued points by
  equivalence and forgets distinct embeddings for fixed K.
- EGA I 2.4.5 contains a material source error. For
  `A = k[t]_(t)` and `K = k(t)` the inclusion defines a point of `Spec(A)` at
  the generic prime rather than the closed point and does not factor through
  `A/(t)`. The valid local-map clause is mapped; the false unrestricted
  sentence is an open residual and was referred to the canonical edition in
  `reports/findings.jsonl` at 4,986 bytes and SHA-256
  `7AE91F0A80471A3D3CBA63B94DEF6C9A259644E8E1D234DB89632F1061210291`.
  The edition task acknowledged the queue and owns corrected-layer
  adjudication; no authority file was mutated here.
- The quotient and local-spectrum factors of 2.4.7 map separately to 01IG and
  01L9; the full composite need not be a closed immersion. For 2.4.8 the local
  triviality argument is 0B8M plus the unique-closed-point open-neighbourhood
  fact in the proof of 01J6. Tag 02AH supplies an explicit affine
  counterexample and 0BDA plus 0BCH supply the stronger UFD conclusion;
  factoriality already entails normality.
- Three bounded inherited-parent audits were consumed and owner-replayed.
  Their exact scopes findings corrections and no-write claims are recorded in
  A000076--A000078. No chapter build or visual render is applicable to this
  graph-only slice; pinned-label replay structural validation privacy checks
  and exact remote identity remain the checkpoint gates.

### EGA I 2.5 review A000079--A000081

- Five numbered units and the native scheme-over-base triangle were checked
  against direct French F8 and the p.103--p.104 diplomatic gates. The
  cumulative map has 242 edges across 94 admitted source units with 93
  residuals. No Stacks TeX changed.
- The admitted French source `ega1-2-fr.tex` is 27,463 bytes with SHA-256
  `AE6B128092ACBB8C1AFB4899EEA003FB966B6FF6669A264B59FD5F095AF4F029`.
  The p.103 ledger and R26 validation SHA-256 identities are respectively
  `B520493D1CA931E46505DACB158597147EAC7DC84B9F53EF5AFAB21771AF13A7`
  and `E12D1BAFBF55F86BA7DC24349E7439E518A82397C649E51CA3186B13383BB78A`.
  The p.104 ledger and R27 validation identities are respectively
  `C997C1D70DD5C6F32E67538657AB7DDE820ADF495BEF7EA8AF9BD3309F74769F`
  and `D21A97F27507F42FC20848B422599877D5F04F4653E8A799DD1A5266B5FD49EF`.
- Tag 01JX supplies the exact scheme-over-base structure morphism morphism-
  over-base and Mor-over-base clauses. Tag 01I1 supplies the equivalent affine
  target and sheaf-of-A-algebras reformulation. Tag 01JM records the stronger
  final-object fact with Spec Z identified in its proof and 01RJ gives
  dominance without adding irreducibility or surjectivity.
- Tag 001G identifies the category as the slice category Sch over S and gives
  postcomposition along a base arrow. The source triangle remains a native
  diagram unit because no identical labelled Stacks diagram exists. Its
  mathematical equality is exactly 01JX item three; pointwise fibre
  preservation is recorded only as a consequence and never as a replacement
  definition for a morphism over S.
- For 2.5.3 source restriction is composition with the open inclusion 01HF
  after 01IK ensures the open is a scheme. Tag 01JB glues the underlying local
  morphisms and uniqueness proves that the result remains over S. Tag 01HI
  handles factorization through an open target. No finiteness compactness or
  separation hypothesis is introduced.
- The heading change of base in 2.5.4 is historical terminology for
  postcomposition and restriction through an ambient open base. It is not the
  fibre-product construction in 01JX items five through seven and 01JY was
  excluded. The automatic S-prime-linearity clause follows by cancelling the
  open immersion through 01L7 and is not generalized to arbitrary base maps.
- The p.104 authority prints `Si X est un S-morphisme` in 2.5.5. The
  diplomatic layer remains unchanged and the graph uses the separately
  corrected S-prescheme reading already catalogued as
  `EG-EGA-I-P104-FR-255-SOURCE-TYPO-001`; no duplicate finding was emitted.
  Tag 01KT gives the section identity while 01JX reconstructs the section set
  as Mor_S from S to X. EGA's Gamma notation remains explicit migration
  metadata so it cannot be confused with global functions or cohomology.
- Three bounded inherited-parent audits were consumed and owner-replayed.
  Their scopes outputs and no-write claims are recorded in A000079--A000081.
  No chapter build or visual render is applicable to this graph-only slice;
  pinned-label replay structural validation privacy checks and exact remote
  identity remain the checkpoint gates.

### EGA I 3.1 review A000082--A000084

- The single direct-French semantic unit 3.1.1 was checked through its final
  binary affine sentence on printed p.104. The cumulative map has 253 edges
  across 95 admitted source units with 100 residuals. No Stacks TeX changed.
- The admitted French source `ega1-3-fr.tex` is 59,766 bytes with SHA-256
  `DB4F986C9FDC1B66FF2D627C5E9121BCE0490563B7C14415320B5DDD7424B851`.
  Its F8 manifest remains 5,784 bytes with SHA-256
  `2137BF64B9BD210176B58075DBDB58E7C8A5669F9EFAD61410510A01D32D0BC0`.
  The p.104 ledger is 4,498 bytes with SHA-256
  `C997C1D70DD5C6F32E67538657AB7DDE820ADF495BEF7EA8AF9BD3309F74769F`;
  R27 is 8,883 bytes with SHA-256
  `D21A97F27507F42FC20848B422599877D5F04F4653E8A799DD1A5266B5FD49EF`
  and PASS/errors empty.
- Tag 0B1X supplies the arbitrary topological coproduct. Tag 01JB specializes
  to the source construction by taking every off-diagonal overlap empty; its
  construction and first mapping property yield the transported components
  and exact product-of-Hom-sets bijection. Tags 00AL and 00AM retain the sheaf
  and ring-structure layers and 01JC upgrades the result to a scheme. No
  finiteness quasi-compactness separation or nonemptiness condition is added.
- Tag 002J identifies the resulting universal property as a set-indexed
  coproduct. Applying the 01JB mapping property with target S gives the unique
  structural map and in fact the coproduct in the slice category Sch over S;
  01JX records only the scheme-over-S terminology. Tag 04AO records the binary
  coproduct while retaining the notation migration from EGA sqcup to Stacks
  amalg.
- Tag 00ED gives the underlying disjoint-union homeomorphism for Spec of the
  binary product ring. The ring projections A times B to A and B induce the
  scheme coprojections in the contravariant direction. The proof of 01I5
  constructs the canonical locally ringed-space isomorphism and supplies the
  structure-sheaf layer absent from 00ED alone.
- The affine formula is deliberately binary. An infinite disjoint union of
  nonempty affine schemes need not be quasi-compact whereas every affine
  spectrum is quasi-compact; Spec of an infinite ring product may also have
  extra ultrafilter primes. Tag 000R was excluded because it only guarantees
  at-most-countable coproducts inside a chosen universe-controlled category.
  Tag 01I4 was excluded because it concerns products of schemes and tensor
  products of rings.
- The English discovery wrapper contains synthetic label I.3.1 in addition to
  I.3.1.1 while direct French has only the subsection label and semantic label
  I.3.1.1. The wrapper alias stays unreviewed and all admitted edges use
  `ega:I.3.1.1`; stable discovery IDs and authority files remain unchanged.
- Three bounded inherited-parent audits were consumed and owner-replayed.
  Their scopes outputs and no-write claims are recorded in A000082--A000084.
  No chapter build or visual render is applicable to this graph-only slice;
  pinned-label replay structural validation privacy checks and exact remote
  identity remain the checkpoint gates.

### EGA I 3.2.1--3.2.5 review A000085--A000087

- The product definition, affine construction, pairing formula,
  monomorphic-base comparison, and open-base corollary were checked against
  direct French F8 across printed pp.104--106. The cumulative map has 274
  edges across 100 admitted source units with 115 residuals. No Stacks TeX
  changed.
- The admitted French source `ega1-3-fr.tex` remains 59,766 bytes with SHA-256
  `DB4F986C9FDC1B66FF2D627C5E9121BCE0490563B7C14415320B5DDD7424B851`.
  The p.104 ledger/R27 identities are
  `C997C1D70DD5C6F32E67538657AB7DDE820ADF495BEF7EA8AF9BD3309F74769F`
  and `D21A97F27507F42FC20848B422599877D5F04F4653E8A799DD1A5266B5FD49EF`.
  The p.105 ledger/R28 identities are
  `4F85769E94A2E8EF7C3B4A6C7A8400D062313CC218BD5C97596C0109C947D8DB`
  and `E09FD9270B63CA943059DDEDCA557FB420C4C65D60DCF2D46FC68AA51ECCE022`.
  The p.106 ledger/R29 identities are
  `E6757586AB33B973673E229E307EE9914AF5836EEC815643968DBD8F1C2A8F5D`
  and `FA89227CD8E5CCBBA1EE733B93BE9C87782A39ADA29234C1F316646C942BBAD1`.
  All three validations are PASS/errors empty and record no scoped source
  correction, ambiguity, or mathematical defect.
- EGA's product of S-schemes is the categorical product in the slice Sch over
  S through 001G and 001S and exactly the ordinary scheme fibre product in
  01JP. The unique isomorphism statement is projection-compatible rather than
  literal equality. Pairing notation and the map u times_S v are reconstructed
  from the universal property and general limit functoriality 002L. The source
  remains definition-only here; existence in 01JM belongs to 3.2.6.
- Tag 01I4 exactly gives Spec of B tensor_A C and proves the product even among
  locally ringed spaces. Its canonical projection data reverse the ring maps
  into the tensor product. Its proof gives the A-algebra Hom bijection; 00CX
  supplies only the balanced module tensor dependency and is not mislabeled as
  the full algebra theorem.
- In 3.2.3 the compatible maps rho and sigma determine tau by tau of b tensor c
  equal to rho of b times sigma of c. Compatibility on A is essential: two
  unrelated evaluations of k[t] at zero and one cannot arise from one map out
  of the tensor product. Tag 01I1 retains the affine morphism contravariance.
- In 3.2.4 categorical cancellation is exactly 003B. Tag 01L3 turns monicity
  into an isomorphic diagonal and the 01KR comparison is its base change, so
  products over S prime and S agree. Neither point injectivity nor
  separatedness suffices: Frobenius can be point-bijective with a nonreduced
  self-fibre product and separatedness yields only a closed comparison.
- For 3.2.5 tag 01HI uniquely factors both structure maps through the open base
  and 01L7 makes that open immersion monic. This reduces the corollary to the
  preceding proposition and remains conditional on chosen product objects.
- Three bounded inherited-parent audits were consumed and owner-replayed.
  Their scopes, outputs, and no-write claims are recorded in A000085--A000087.
  No chapter build or visual render is applicable to this graph-only slice;
  pinned-label replay, structural validation, privacy checks, and exact remote
  identity remain the checkpoint gates.

### EGA I 3.2.6--3.2.8 review A000088--A000090

- The global existence theorem, its five-step proof, the open-product
  corollary, and the product-of-sums decomposition were checked against direct
  French F8 across printed pp.106--108. The cumulative map has 299 edges
  across 108 admitted source units with 136 residuals. No Stacks TeX changed.
- The admitted French source `ega1-3-fr.tex` remains 59,766 bytes with SHA-256
  `DB4F986C9FDC1B66FF2D627C5E9121BCE0490563B7C14415320B5DDD7424B851`;
  F8 remains 5,784 bytes with SHA-256
  `2137BF64B9BD210176B58075DBDB58E7C8A5669F9EFAD61410510A01D32D0BC0`.
  The p.106 ledger/R29 identities are
  `E6757586AB33B973673E229E307EE9914AF5836EEC815643968DBD8F1C2A8F5D`
  and `FA89227CD8E5CCBBA1EE733B93BE9C87782A39ADA29234C1F316646C942BBAD1`.
  The p.107 ledger/R30 identities are
  `0BBB806A5B6AE6AB72327A3BA47D222AFAD5DFA5C1FFCCFF711CA928660498AF`
  and `15657B56D2904F07954F47CC0414038EB9C5D1A24CA41E53EB214EBEBE6BC713`.
  The p.108 ledger/R31 identities are
  `61815DBE2CE8BA37209E8FB59DDAF7C7B718E79061993C8277098D5E8420EC6F`
  and `C2990F06616057C1051F1CA6B4ED3A68BB04BA9B966E7D05B22738A657394282`.
  All validations are PASS/errors empty and record zero scoped authorial
  corrections, source typos, or unresolved readings.
- Tag 01JM strictly strengthens Theorem 3.2.6 by proving all finite limits in
  schemes. Its proof represents the compatible-pair functor and uses 01JJ with
  affine input 01I4. This is full theorem coverage but an alternative package
  for EGA's numbered local construction rather than a line-for-line proof.
- Lemma 3.2.6.1 is the whole-base specialization of 01JR. The same tag must not
  be cited as a dependency of 01JM because it occurs downstream and assumes
  existence. Tag 01JS is likewise excluded from existence coverage because it
  only describes an affine cover of an already-existing product.
- Lemma 3.2.6.2 has no standalone target. Its exact candidate-cone conclusion
  follows from 01JP universal arrows, 01JB morphism gluing, and the 01JR open
  overlap calculation. The condition that every chart is the simultaneous
  inverse image under p and q is essential; arbitrary product-copy charts do
  not verify a preassigned cone.
- Lemma 3.2.6.3 is entailed by unconditional 01JM and its source construction
  is recovered by 01JJ, canonical fibre-product uniqueness, and 01JB plus
  01JC. Universality forces both the overlap isomorphisms and their cocycle.
  Lemma 3.2.6.4 is likewise entailed globally while 01HI and 01JJ retain the
  synchronized-base-cover argument. Unit 3.2.6.5 is proof closure rather than
  a second theorem; 01I4 is its exact affine ingredient and the 01JM proof is
  only partial line-level absorption.
- The main open-product identification in 3.2.7 is exactly 01JR after renaming
  its base and factor opens. The pairing compatibility is derived from 01HI
  and 01JP uniqueness. Both image-containment hypotheses remain mandatory.
- No single pinned tag states the two-family formula in 3.2.8. Tags 01JR, 01JB,
  and 01JC give complete derived coverage by decomposing the global product
  into disjoint open pairwise products. Tag 023X contains only the self-family
  formula in an unlabelled descent proof and is retained as corroboration rather
  than an equivalent target. Arbitrary and empty families remain allowed.
- English discovery unit I.3.2.9 is not a synthetic body paragraph: its own
  footnote identifies it as a translator augmentation from the EGA II errata
  on printed p.221. The French producer's p.108 continuation control expressly
  leaves that insertion pending separate authority replay. Issue I000036 keeps
  it unpromoted until the exact French erratum witness is admitted.
- Three bounded inherited-parent audits were consumed and owner-replayed.
  Their scopes, outputs, rehashes, and no-write claims are recorded in
  A000088--A000090. No diagram occurs in these units and no chapter build or
  visual render is applicable to this graph-only slice; pinned-label replay,
  structural validation, privacy checks, and exact remote identity remain the
  checkpoint gates.
- Final no-write audit A000091 adversarially checked every new edge, residual,
  decision, issue, agent row, count, target join, authority-pending statement,
  and circularity guard and returned PASS before staging.

### EGA I 3.3.1--3.3.5 review and R184 page-scope repair A000092--A000094

- The first 3.3 intake exposed a deterministic provenance defect rather than a
  mathematical mapping problem. Discovery unit I.3.2.9 contains an inline
  EGA II p.221 erratum marker after its label. The old parser left that unit at
  I:108 and leaked II:221 into subsection 3.3 and units through 3.3.5.
- Intake now distinguishes a whole appended foreign-witness section from a
  foreign marker entered from an ordinary body page inside one statement. The
  latter binds retroactively to the statement and restores the body page at
  the matching environment end. Exact checks cover both the persistent I.1.8
  errata section and the isolated I.3.2.9 insertion.
- The exact frozen R184 tree was replayed rather than the advanced live English
  tree. Three later English corrections were inverted only in a temporary
  reconstruction from their producer-authored exact inverses. R184 replay is
  PASS with 127 files, 7,283,321 bytes, tree SHA-256
  `3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D`,
  9,585 units, and 445 diagrams. Exactly nine printed-page fields changed;
  every stable ID and every other generated field is unchanged.
- Direct French F8 admits 3.3.1--3.3.5 across printed pp.108--109. The source
  `ega1-3-fr.tex` remains 59,766 bytes with SHA-256
  `DB4F986C9FDC1B66FF2D627C5E9121BCE0490563B7C14415320B5DDD7424B851`.
  The p.108 ledger/validation identities are
  `61815DBE2CE8BA37209E8FB59DDAF7C7B718E79061993C8277098D5E8420EC6F`
  and `C2990F06616057C1051F1CA6B4ED3A68BB04BA9B966E7D05B22738A657394282`;
  the p.109 identities are
  `0936AEE282CBEF59C4C613DC3AB891BDEEE7BFDB086DAE6E16521D61DB0F19E1`
  and `188004628018FCA04FD5FE31A8A8E690908FA57195DE2B6A33042A81CAF1CFCD`.
- Unit 3.3.1 is only partial. Its slice-category explanation is exactly 001G,
  but its claim that every non-excluded property is categorical includes the
  final 3.3.10 assertion that base change preserves sums. In Grp with S the
  trivial group and nontrivial H mapping to S, base change of the coproduct of
  two terminal groups is id_H while the coproduct of their base changes in
  Grp over H is the nonisomorphic fold H free-product H to H. Issue I000038
  and residual R000137 remain open at the source layer; the append-only
  referral is `EGA-I-3.3.1-ARBITRARY-CATEGORY-SUM-BASE-CHANGE`. The six-row
  `reports/findings.jsonl` is 6,469 bytes with SHA-256
  `EF81768A542B2DC883907C3C61DE4A671CC7A3D981CA649668A49B029F0AA3D6`.
- Units 3.3.2--3.3.4 are completely covered at categorical or proof level by
  slice categories, fibre-product uniqueness, functorial limits, and the
  terminal object in a slice. There is no separate ordinary-product unitor or
  projection-formula tag. The native 3.3.2 diagram remains an independent
  stable unit and records first-projection naturality.
- Unit 3.3.5 is split across 002I, 01JM, 002O, 002E, 002L, and 01JP. The source
  does not spell out n=0 or n=1; the empty product is S in the slice and the
  singleton product is X as implicit conventions. Associativity and
  commutativity are canonical projection-compatible isomorphisms rather than
  literal equalities or arbitrary identifications.
- The cumulative scaffold now has 316 statement edges across 115 admitted
  source units, 150 residuals, 313 official-target rows, 139 distinct existing
  tags, three local untagged rows, 18 full exact equivalences, 38 issues, six
  correction referrals, and 95 agent records. No Stacks chapter TeX changed.
- Final no-write audit A000095 returned PASS on the exact nine-field page
  migration, all new graph rows and target joins, count reconciliation,
  authority identities, counterexample, privacy, and deterministic validators.
- Direct-French review now covers EGA I 3.3.6--3.3.10 and leaves 3.3.11 as the
  next sequential unit. The authority remains `ega1-3-fr.tex`, 59,766 bytes,
  SHA-256 `DB4F986C9FDC1B66FF2D627C5E9121BCE0490563B7C14415320B5DDD7424B851`,
  under F8 SHA-256
  `2137BF64B9BD210176B58075DBDB58E7C8A5669F9EFAD61410510A01D32D0BC0`.
  Printed-p.109 controls are ledger
  `0936AEE282CBEF59C4C613DC3AB891BDEEE7BFDB086DAE6E16521D61DB0F19E1`
  and validation
  `188004628018FCA04FD5FE31A8A8E690908FA57195DE2B6A33042A81CAF1CFCD`;
  printed-p.110 controls are ledger
  `92EBEF4E44D3821B4D2F4320ADFB5A1C9890A63873BC6C7AEB9F74338CB62CEA`
  and PASS validation
  `66E00BE78EEB8B6B4E8E470C2DAFEC901274DC24B6E845FBE477BE2DB5034B76`.
- Unit 3.3.6 is the exact base-change construction 01JX after canonical factor
  symmetry; its diagram is covered by the stronger cartesian square 01JP.
  Unit 3.3.7 uses the explicit base-changed morphism from 01JX and derives
  functor laws from fibre-product uniqueness after representatives are chosen.
- Unit 3.3.8 is the exact 01JP Hom bijection and identifies postcomposition as
  left adjoint to pullback. The printed `f` where the construction requires
  `g` is already catalogued as
  `EG-EGA-I-P109-FR-338-F-VS-G-SRCTYPO-001`; I000039 reuses that authority
  record and creates neither a second correction referral nor a source edit.
- Unit 3.3.9 specializes the stronger fibred-category coherence theorem 02XO.
  Its proof and formula 3.3.9.1 occur at proof level in 001Y; formula 3.3.9.2
  is naturality of the pullback comparison. Every equality is only under the
  specified canonical identifications.
- Unit 3.3.10 is implied by the stronger right-adjoint limit theorem 0038.
  The pairing formula is derived from 002L and projection uniqueness. Its
  scheme coproduct clause is valid through 01JR plus 01JB and 01JC; it is not
  promoted to an arbitrary-category law. Existing I000038 and R000137 retain
  the counterexample to the earlier 3.3.1 omnibus claim without duplication.
- Agent records A000096--A000099 preserve the three disjoint read-only audits
  and the final adversarial pass. That pass caught and closed a semantic
  ordinal typo in D000097 which structural validation alone could not detect.
  The cumulative draft now has 335 statement edges
  across 127 admitted units, 171 residuals, 332 official-target rows, 142
  distinct existing tags, three local untagged rows, 20 full exact
  equivalences, 39 issues, six correction referrals, and 99 agent records.
  No Stacks chapter TeX changed.
- Immediate post-push review found that the final product and sum prose at
  English discovery lines 466--476 and French authority lines 520--530 follows
  the closed 3.3.10 proof rather than belonging to it. D000103 and I000040
  therefore move exactly S000331--S000334 and R000165--R000167 from
  `ega:I.3.3.10:proof` to `ega:I.3.3.10`. S000330 remains the sole proof edge;
  `ega:I.3.3.10.1` remains an independent labelled-formula unit. This is an
  attribution correction only: tags, mathematical dispositions, stable edge
  IDs, residual IDs, row counts, and the six-item correction-referral file do
  not change. The append-only correction raises the current issue count to 40
  and the decision count to 103.
- Governance review then established that the first correction mechanism was
  itself invalid: published S/R rows are append-only, but their tables lacked
  an explicit supersession field. D000104 and I000041 restore the exact
  f2195bb forms of S000331--S000334 and R000165--R000167 and append corrected
  successors S000336--S000339 and R000172--R000174. `smap.csv` now has 339
  physical rows with 335 active and four superseded; `resid.csv` has 174
  physical rows with 171 active and three superseded. The validator rejects
  missing forward or multiply claimed supersessions and calculates all review
  closure from the active view while still validating historical rows. The
  append-only physical registers now contain 104 decisions and 41 issues.
  It also pins the reconstructed legacy prefixes at 144,616 bytes / SHA-256
  `86DB212E45E51F7F7CB8613E4A205A9A07E68A82E173BBD2C5DD8167E350819C`
  for S000001--S000335 and 46,075 bytes / SHA-256
  `704D957786F45FE1F280C3303C59883DC50AAC9809CD2071FBB8C20369147303`
  for R000001--R000171. Exact row arity and attribution-only field equality
  are fail-closed regressions. Synthetic unknown-target, forward-reference,
  whitespace, branching, and valid-chain supersession tests all passed.
  Contiguous physical S/R ID order closes the low-ID omission bypass, while
  exact D000104-to-D000103 and I000041-to-I000040 regressions make the
  governance repair itself non-optional. The legacy issue-link column is
  validated as an explicit mixed namespace: historical `D` links resolve to
  decisions and new `I` links obey prior-row nonbranching supersession.
- Agent records A000100--A000102 preserve the registry/control audit and both
  disjoint mathematical audits for the next 3.3.11--3.3.15 slice. Their work
  also supplied the exact supersession invariants and independently confirmed
  the corrected 3.3.10 attribution. The physical agent register now has 102
  rows; all three runs were read-only and owner-replayed.
- Final no-write audit A000103 returned PASS on the restored legacy bytes,
  explicit successors, mixed issue-link namespace, physical and active counts,
  row arity, contiguous identifiers, failure cases, and privacy. The agent
  register now has 103 rows.
- Direct-French review now covers EGA I 3.3.11--3.3.15 and closes subsection
  3.3; EGA I 3.4.1 is next. The p.110 controls remain ledger
  `92EBEF4E44D3821B4D2F4320ADFB5A1C9890A63873BC6C7AEB9F74338CB62CEA`
  and validation
  `66E00BE78EEB8B6B4E8E470C2DAFEC901274DC24B6E845FBE477BE2DB5034B76`.
  P.111 is bound by ledger
  `1CEDDC361F0EC9409C888F6D3CF6442E8E671FD9465F06F96244FDF81D3CBA5E`
  and PASS validation
  `7FBFDD83E08BC65055A19F18FEB29EED152777414894DBE6A4A6844668AA3AE3`;
  the latter records direct 1100-dpi inspection and one 5000-dpi formula crop.
- Unit 3.3.11 is the exact proof-level pullback identity in 01JY; its labelled
  immersion hypothesis is not imported. The statement proof and native diagram
  remain separate stable units and every comparison is canonical rather than
  literal equality.
- Unit 3.3.12 is split across categorical cancellation fibre-product
  uniqueness the product-factorization formula 02YC and 01L5. Its printed
  codomain `Y_(S')` must be `X'_(S')`; I000042 reuses
  `EG-EGA-I-P111-FR-3312-BASECHANGE-TARGET-Y-VS-XPRIME-SRCTYPO-001` without a
  second referral or any diplomatic-source edit.
- Unit 3.3.13 is exactly affine duality plus the affine fibre-product tensor
  formula. `X tensor_A A'` is retained only as an EGA alias for base change.
  Unit 3.3.14 is the universal pullback map `(f 1)` and its specialized Hom
  bijection; Stacks has no separate graph-terminology tag.
- Unit 3.3.15 is covered by the final object `Spec Z`, affine one-space 01M0,
  the global-section representation 01JH, affine-target maps 01I1, and sheaf
  gluing 006T. Its printed scheme arrow is reversed; I000043 reuses
  `EG-EGA-I-P111-FR-3315-MORPHISM-DIRECTION-SRCTYPO-001` and maps only the
  corrected `X -> Spec Z[T]` reading.
- The two French-labelled plain displays in 3.3.12 and 3.3.14 remain explicit
  parent `source_part` records. R184 leaves them unlabelled; inventing child IDs
  would violate the English-discovery identity scheme and a generic display
  parser would add 1,560 unrelated statement children.
- The active scaffold now has 355 statement edges across 134 admitted units,
  352 official-target rows, 149 distinct official tags, three local untagged
  rows, 20 full exact equivalences, and 190 active residuals. Physical history
  contains 359 edge rows with four superseded and 193 residual rows with three
  superseded. There are 110 decisions, 43 issues, six correction referrals,
  and 104 agent records. No Stacks chapter TeX changed.
- A000104 independently audited the complete release diff against direct French,
  the P110/P111 controls, and pinned target commit `a04446e5`. It returned PASS
  on all twenty new edge rows, nineteen residual rows, six decisions, two
  already-catalogued source-defect issues, target joins, semantic
  classifications, append-only history, snapshots, privacy, and the validator;
  it made no writes and found no new defect.
- Public checkpoint `6b141b040991fa0583ca8873f9dcdda7bb524e1e` closed
  EGA I 3.3 through 3.3.15. Local HEAD, fetched fork, `ls-remote`, and the
  GitHub commit API all returned that commit and tree
  `ea7b173f1cf3a545ae0fca697f6aed006a3d7a8d`; the post-push worktree was
  clean.
- Direct-French review now covers all eighteen generated units in EGA I
  3.4.1--3.4.9 and closes subsection 3.4; EGA I 3.5.1 is next. Authority is
  still F8 `2137BF64B9BD210176B58075DBDB58E7C8A5669F9EFAD61410510A01D32D0BC0`.
  P111 through P114 validation hashes are respectively
  `7FBFDD83E08BC65055A19F18FEB29EED152777414894DBE6A4A6844668AA3AE3`,
  `2024E09325ECB75B7398699C954856DA99CC13DB130E242357CF870C31110B9F`,
  `06D68E902E48B278C0AB683D1992FFE739104AE7B670D55FD316EDF22046FA30`,
  and `C0575FC4F2215613939BC4657407D123370967A385B83E11229333D005CCFAE1`;
  every receipt is PASS with direct NUMDAM inspection and no OCR.
- Units 3.4.1--3.4.4 are the representable point functor and its pointwise
  product identities in the slice category. They map to 001O, 0020, 001G,
  001S, 001V, 01I2, and 01JX. Ring-valued covariance is recorded as two
  contravariance reversals rather than an unexplained change of variance.
- Unit 3.4.5 maps local spectra to 01J6 and fixed-field points to the exact
  prose under 01J5. Its historical term `point geometrique` includes every
  field-valued point; modern 03PO requires an algebraically closed value field.
  The final `X(K)` is explicitly retained as relative over `Spec K`, since an
  absolute reading can be false when K has nontrivial endomorphisms.
- Units 3.4.6--3.4.7 combine the common-extension lemma 0H7K with the product
  universal property and the exact binary point criterion 0495. The map of
  underlying sets is only surjective: 0496 supplies a concrete two-point
  counterexample and 01JT classifies every fibre by primes of the residue-field
  tensor product.
- Unit 3.4.8 occurs verbatim in the proof of 01S1 including the arbitrary
  subset identity and the native Cartesian square. It is set-theoretic and is
  not a statement about scheme-theoretic images. Unit 3.4.9 is exactly 01JT
  after migrating Bourbaki composite-extension types to tensor-product primes;
  01KR, 01L3, and 01I4 supply the proof's base replacement and affine formula.
- French 3.4.9 calls the induced tensor-product map to `kappa(z)` a
  `monomorphisme`. It may have a nonzero prime kernel. I000044 reuses
  `EG-EGA-I-P114-FR-349-TENSOR-MONOMORPHISM-SRCTYPO-001`; diplomatic French is
  untouched and the mapped mathematical reading is `homomorphisme`. The three
  French-only plain-display labels remain parent source parts because frozen
  R184 supplies no corresponding child IDs. Repeated placeholder proof hashes
  are never used for identity or deduplication.
- A000105 and its bounded nested contribution A000106 audited 3.4.1--3.4.5;
  A000107 audited 3.4.6--3.4.9. All work was read-only. The owner replayed all
  target joins, control hashes, variance and field hypotheses, unit boundaries,
  terminology, and correction status before integration. No new gap or new
  correction referral was created.
- The active scaffold now has 390 statement edges across 152 admitted units,
  387 official-target rows, 157 distinct official tags, three local untagged
  rows, 23 full exact equivalences, and 232 active residuals. Physical history
  contains 394 edge rows with four superseded and 235 residual rows with three
  superseded. There are 120 decisions, 44 issues, six correction referrals,
  and 108 agent records. No Stacks chapter TeX changed.
- A000108 independently audited the complete 3.4 release diff and returned
  PASS on all eighteen unit attributions, thirty-five edges, forty-two new
  residual rows, ten decisions, the single already-catalogued P114 issue,
  agent records, target joins, active snapshots, append-only history, privacy,
  and the validator. It included the owner repair of S000382 and explicit
  parent-label and partial-terminology closure in R000233--R000235; it made no
  writes and found no new defect.

## 2026-08-08

- Direct-French review now covers EGA I 3.5.1--3.5.11 and closes subsection
  3.5; EGA I 3.6.1 is next. The authority is F8
  `2137BF64B9BD210176B58075DBDB58E7C8A5669F9EFAD61410510A01D32D0BC0`;
  canonical `ega1-3-fr.tex` is 59,766 bytes with SHA-256
  `DB4F986C9FDC1B66FF2D627C5E9121BCE0490563B7C14415320B5DDD7424B851`.
  P114--P117 are PASS and no scoped French source defect or unresolved reading
  was found.
- The admitted slice has 21 generated units and 49 new statement/component
  edges S000395--S000443. Exact full-statement matches are 01S4 for 3.5.4 and
  3.5.8 and 01S4 with 01S3 for 3.5.11. The remaining claims are explicitly
  split among 01JX 01KU 01S0 01S1 01RZ 01J9 0H7K 03H5 003B 001O 0CPN 02V1
  0472 01JP 04VS 04VW and 01I2. R000236--R000271 record every derived,
  unlabelled, stronger-category, terminology, point-set, and parent-display
  boundary. No new open mathematical gap and no new correction referral were
  created.
- Frozen R184 omits printed-page markers I:115 and I:116 from `ega1-3.tex`.
  D000121 and I000045 therefore add `pages.csv` rather than altering the
  frozen discovery tree. Its 18 active L rows are 5,483 bytes with SHA-256
  `6EED824C60BC56AB07996FDA2D70B962E3225898DA90CEA232006A2A52AF16F7`;
  P115 gate `8D0C007424BBFAECD5F59CE33A25567EE6923C4A88D461BB87CE86ADA2496E1B`
  and P116 gate `083D997689E74C8E7610C0894F978E643753D73DCCA4D8BB61B1FBA17A72339A`
  bind all corrections. Exactly 18 `printed_page` fields changed and every
  other field and all 9,585 stable IDs remained byte-semantically identical.
- Two independent full R184 replays reconstructed the 127-file 7,283,321-byte
  tree at `3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D`
  by applying the four recorded live-tree inverses. Both produced byte-identical
  `files.csv` `A1BB4950FE27D813FD79BCC4604607994D38E3F1E5A2C1D52EC21E01EC5C7E5F`,
  `units.csv` `E72220BBBC714B20F4386F5CF91695A46CAF194F077430E747F545504C556FBE`,
  and `intake.json` `DA75F2DBA40E7BB19844B771E084118DAFC67E857B8DEBA8347312DAA3BCD86A`.
  A deliberately stale raw-page guard applied zero rows and left all units
  unchanged. The overlay is therefore deterministic and atomic.
- A000109--A000114 record the control/unit audit, the bounded 3.5.1--3.5.6
  parent audit and its two exact nested contributions, the 3.5.7--3.5.11
  audit, and the independent page-overlay design. All contributions were
  read-only and were owner-replayed before integration. No Stacks chapter TeX
  changed.
- The active scaffold now has 439 statement edges across 173 admitted units,
  436 official-target rows, 166 distinct official tags, three local untagged
  rows, 26 full exact equivalences, and 268 active residuals. Physical history
  contains 443 edge rows with four superseded and 271 residual rows with three
  superseded. There are 133 decisions, 45 issues, six correction referrals,
  and 114 consumed agent records.
- A000115 independently audited the complete release diff and returned PASS
  on all 21 attributions, 49 edges, 36 residuals, 13 decisions, the page issue,
  all 19 pinned target joins, the 18-row page overlay, deterministic replay,
  adverse atomicity, append-only history, snapshots, privacy, and validator.
  It made no writes and found no defect. The consumed agent total is now 115.

## 2026-08-09

- Direct-French review now covers EGA I 3.6.1--3.6.5 and closes subsection
  3.6; EGA I 3.7.1 is next. Authority remains F8
  `2137BF64B9BD210176B58075DBDB58E7C8A5669F9EFAD61410510A01D32D0BC0`;
  canonical `ega1-3-fr.tex` is 59,766 bytes with SHA-256
  `DB4F986C9FDC1B66FF2D627C5E9121BCE0490563B7C14415320B5DDD7424B851`.
  P117 and P118 validation hashes are
  `F35A37B89CB1DEE40A79D0C4E7AA708A006B608C166B153E241E2FB662A6464E`
  and `40CE9BF9A4180940D00ACA2E0A69BA3D3F51CF059F9BFD037D26B4A7D83AEF7A`;
  both are PASS with no scoped French correction or unresolved reading.
- Unit 3.6.1 splits the topology of the ordinary residue-field fibre in 01K1
  from the nilpotent thickening comparison in stronger 0BR6. Its affine proof
  uses 01I4 and 00DK and ends with the already integrated untagged EGA I 1.2.4
  criterion. Reusing that local dependency adds no new mathematical gap and
  assigns no official tag.
- Unit 3.6.2 maps the canonical fibre and general base-change convention to
  01K0 01K1 and 01JX. Its field-valued point clause is an instance of 01JP
  only relative to the fixed map through y; an absolute X(K) reading is
  explicitly excluded. Historical tensor notation and structure transported
  onto the underlying subset remain terminology and model residuals.
- Unit 3.6.3 is the proof-level pullback associativity identity in 001Y with
  01JP for the identity pullback and 01JR plus 01K1 for the induced open
  fibre. Unit 3.6.4 uses the unrestricted proof-level base-change identity in
  001Z; 001Y and 02XO preserve its canonical coherence and 01HH supplies the
  open-neighbourhood specialization. The same displayed identity occurs in
  the proof of 02V3 but that labelled lemma assumes locally finite type so it
  is not accepted as the unrestricted target.
- Unit 3.6.5 is the second local-spectrum square of 01K1. Tag 01J7 identifies
  its image as the generalization locus; 01I4 00DK and 00E3 give the affine
  localization model; and 01HV with 02C6 proves that corresponding stalks are
  unchanged. Tag 0HA1 is deliberately rejected as a near-match because it
  instead computes the quotient local ring of the residue-field fibre. No
  scheme isomorphism onto a globally defined subscheme is claimed.
- The two direct-French labelled displays in 3.6.1 and 3.6.3 remain exact
  parent source parts because frozen R184 has no formula children. All eight
  generated units keep their stable IDs and correct I:117--I:118 first-page
  locators; no page overlay row is needed.
- D000134--D000138 add 31 statement/component edges S000444--S000474 and 27
  explicit residual rows R000272--R000298. The active scaffold now has 470
  edges across 181 admitted units and 295 residuals; physical history has 474
  edges with four superseded and 298 residuals with three superseded. There
  are 466 official-target rows resolving to 170 distinct tags plus four local
  untagged rows. The four earlier open gaps remain unchanged.
- A000116--A000118 preserve two disjoint mathematical audits and the exact
  control unit page and duplicate audit. The owner replayed every accepted
  target and caught both a hypothesis-bearing target overclaim and a
  report-only false-near-match tag typo before integration. All contributions
  were read-only. No Stacks chapter TeX changed.
- A000119 independently audited the repaired complete release diff and
  returned PASS on F8 P117 P118 all eight generated units both parent-only
  displays D000134--D000138 S000444--S000474 R000272--R000298 A000116--A000118
  every pinned label and tag the local dependency append-only prefixes exact
  snapshots privacy and graph-only scope. Its sole adverse finding was the
  02V3 hypothesis overclaim which was repaired and re-audited before release.
- Public checkpoint `d0b21e3f4f5af04c207a72a28681498796e2f573` closed EGA I
  3.6 through 3.6.5 with tree
  `de4a42dca6d08987269e611e94ad4fec2730d87b`. Local HEAD fetched fork
  `ls-remote` and GitHub's commit API all returned that identity and tree.
  Every one of the seven changed public files was read back from the immutable
  commit with equal byte length and SHA-256; mismatch count was zero.
- Direct-French review now covers EGA I 3.7.1--3.7.3 and closes section 3;
  EGA I 4.1.1 is next. Authority remains F8
  `2137BF64B9BD210176B58075DBDB58E7C8A5669F9EFAD61410510A01D32D0BC0`
  and canonical `ega1-3-fr.tex` remains 59,766 bytes with SHA-256
  `DB4F986C9FDC1B66FF2D627C5E9121BCE0490563B7C14415320B5DDD7424B851`.
  P118 and P119 gates are PASS at hashes
  `40CE9BF9A4180940D00ACA2E0A69BA3D3F51CF059F9BFD037D26B4A7D83AEF7A`
  and `B82C5D63AF34111BBE4D94700582770A36CFF1A005E76C8C088E960421DE83CC`.
  Their recorded 1100-dpi context derivatives are absent from the current
  bounded authority root but the exact NUMDAM PDF remains live and rehashed;
  this creates no source-reading uncertainty.
- Unit 3.7.1 is the quotient base change 01JX. Historical reduction modulo an
  ideal is not nilreduction 01J4 and can produce a nonreduced special fibre.
  Unit 3.7.2 combines 07BI 01K0 and 01JX for local special and generic fibres.
  The two-point spectrum and open generic singleton are derived from 00KE
  07BI and 01I3 and require all three local domain dimension-one hypotheses.
- The generic fibre is the induced open by 01JR. A closed subscheme of that
  open is a locally closed immersion by 01IO; 01T6 and 01OX make it
  quasi-compact in the source Noetherian setting. Tags 01R6 and 01R7 give the
  minimal closed scheme-theoretic image while 01R8 and the proof of 01QV give
  exact recovery on the generic open. Existence itself does not require
  Noetherianity and the model is canonical only relative to the chosen
  immersion and ambient P.
- Unit 3.7.3 is the valuative criterion 0BX5 specialized to the DVR A. Tag
  01JP identifies K-points of the generic fibre with compatible maps to X;
  01KF and 01KZ split existence from uniqueness; and 01W1 plus 01WC covers
  the proper closed-projective parenthetical. The target strengthens DVR to
  arbitrary valuation rings but not to arbitrary local domains.
- I000046 and finding
  `EGA-I-3.7.3-P119-CONTROL-DIMENSION-ONE-SCOPE` refer a control-level scope
  overstatement. For A equal `k[x,y]_(x,y)` and X equal projective one-space
  over A the K-point `[x:y]` has no A-valued extension. Thus the final French
  sentence removes dimension one only for the model-level assertions about X;
  it does not generalize the point bijection. Diplomatic French is untouched.
- D000139--D000141 add 26 edges S000475--S000500 and 22 residuals
  R000299--R000320. The active graph now has 496 edges across 184 admitted
  units and 317 residuals; physical history contains 500 edge rows with four
  superseded and 320 residual rows with three superseded. There are 492
  official-target rows resolving to 182 distinct tags and four local untagged
  rows. The four earlier open gaps remain unchanged.
- A000120 and A000121 preserve the disjoint 3.7.1--3.7.2 semantic audit and
  the 3.7.3 mathematical plus complete-section control audit. Both were
  read-only. The owner replayed every accepted target both counterexamples
  the I:118--I:119 seam and the correction-referral scope. No Stacks chapter
  TeX changed.
- A000122 records the independent final release audit. It caught the masked
  absence of a target-specific strength residual for the 01JP universal
  property; R000320 now closes that link. The same audit tightened the two
  counterexample descriptions and then returned hard PASS after replaying all
  twenty-six edges twenty-two residuals visual authority append-only privacy
  and graph-only gates.

### EGA I 4.1.1--4.1.10 review and blank-locator intake repair A000123--A000125

- Direct-French review now covers all of subsection 4.1 and stops before
  4.2.1. The original F8 receipt remains historical page evidence. The current
  semantic authority is F33 at 14,944 bytes and SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`.
  Its `ega1-4-fr.tex` row is 34,792 bytes with SHA-256
  `A5F5CDAC81E654E9ABA75BBFEAD24F3010B122452C689B9EBAB5A7711B454EC1`.
- Direct p.121 inspection exposed one diplomatic transcription error: the
  canonical text and R44 had `g'=(psi',omega^b)` although the print has
  unprimed `g` and p.122 consistently concludes `f=j` composed with `g`.
  The correction was referred without a cross-tree write. The French owner
  returned P121S at 5,600 bytes / SHA-256
  `E78CA53480FC3F577786FCB643E63116A1DEC118EDB99C5629B52D6E5E9B411C`
  and F33 removes only that one prime byte with an exact inverse. The English
  already had the printed reading and remains unchanged. I000048 and the
  append-only referral plus closure records preserve the complete history.
- Frozen R184 has genuinely blank first-page locators for the section 4 and
  subsection 4.1 headings plus 4.1.1 4.1.2 and the 4.1.2 proof. D000142 and
  I000047 add L000019--L000023 to bind them respectively to I:119 I:119
  I:119 I:119 and I:120. The parser now permits an empty `parsed_page` only
  as an exact guard; `printed_page` remains mandatory. Positive double replay
  and adverse tests reject a blank guard against a nonblank unit a wrong
  nonblank guard a blank target and a partly bad multirow application. The
  latter applies zero rows and mutates no unit.
- The short `r184.py` replay reconstructs the exact 127-file 7,283,321-byte
  R184 tree from the current six-file English successor using the producer's
  byte-precise inverses. Two serial no-overwrite reconstructions and full
  intakes independently produced byte-identical `files.csv` at
  `A1BB4950FE27D813FD79BCC4604607994D38E3F1E5A2C1D52EC21E01EC5C7E5F`,
  `units.csv` at
  `132E2BC14F9C04C0B71CF5B46588770613509318D1FEEB2EBD20C68E9BB8EAD3`,
  and `intake.json` at
  `B5056E38C8716B28B9AD1952C809C5F6B83D19C707E28340ACE495B40D801A45`.
  All 9,585 IDs and every field except the five intended page locators are
  unchanged from the public predecessor.
- D000143--D000152 add S000501--S000554 and R000321--R000353. The slice
  decomposes quasi-coherent closure into 01BE 01IA 01I7 01IC 01ID and 01LA;
  closed-subscheme construction and classification into 01AV 01HM 01IN 01IB
  01IG 01I9 0F2L 01QP and 01QQ; restriction and gluing into 01BG 01JU 01JV 0FCZ
  00AL 00AM and 00AN; and canonical inclusion containment and factorization into
  02V0 01IM 01IO 01IQ 0H7H 01L6 01L7 003B 01HI and 01HP.
- The graph keeps every important boundary explicit. Generic support of a
  quasi-coherent module is not substituted for quotient-ring support;
  identity of closed subschemes is identity over X; local ideal kernels must
  agree on overlaps; scheme monicity is not silently promoted to ringed-space
  monicity; and set-theoretic image containment cannot replace annihilation of
  the defining ideal. For example the identity of the dual-number point does
  not factor through its reduced closed subscheme.
- The active scaffold now has 550 statement edges across 198 admitted units
  and 350 residuals. Physical history contains 554 edge rows and 353 residual
  rows. There are 546 official-target rows resolving to 199 distinct tags and
  four local untagged rows. Twenty-six exact full-statement equivalences and
  the four earlier open gaps are unchanged. No Stacks chapter TeX changed.
- A000123--A000126 preserve two disjoint semantic audits the inverse audit of
  4.1.6--4.1.10 and the complete control unit page and collision audit. All
  were read-only. Their findings caused the exact blank-guard repair and the
  direct-authority referral before any release claim.
- A000127 then failed the first inverse audit of 4.1.1--4.1.6: affine-only
  01IC and 01ID had been allowed to carry global source claims the exact
  unlabelled 01LA enumeration was missing and the ideal-gluing proof lacked
  the map-gluing and quasi-coherence-locality steps. The repair retargets the
  global claims to 01LA keeps the affine lemmas only as dependencies adds
  00AN and records every stronger-target remainder. A000128 independently
  replayed the repaired graph and returned hard PASS with zero duplicate
  semantic keys.

### Diagram graph-certification gate D000153 / I000049

- The direct user warning reported a concrete cross-corpus false certification in which
  insufficient authority detail produced a nonexistent edge and a separate
  accepted render placed a label on the wrong side. The controlling lesson is
  graph completeness including absent edges rather than mere legibility.
- This EGA scaffold has 445 registered native diagram units and earlier mapped
  slices sometimes record only 1,100-dpi whole-page review. No false EGA edge
  is inferred from that fact but the earlier evidence is below the new floor.
  Production after 4.1 therefore stops for a bounded inventory and every
  already mapped diagram is re-audited from its own tightly bounded
  direct-authority and final-output crops at no less than 5,000 dpi-equivalent
  detail. Full-page shared and grouped crops do not qualify.
- The gate separately checks objects directed edges absent edges direction
  hook and equality style label text primes bars subscripts geometry and label
  side then checks the rendered native output. Discovery-only units remain
  unreviewed rather than receiving retroactive fidelity claims.
- The threshold addendum applies the same individual 5,000-dpi minimum to
  intricate standalone mathematical blocks such as dense arrays compatibility
  chains exact-sequence grids and unusual-symbol constructions.
- A000129 independently replayed the complete 4.1 release diff after the
  semantic repairs and the diagram-gate addition. It returned hard PASS on
  all fifty-four edges thirty-three residual rows F33 and P121S authority five
  blank-locator overlays exact R184 reconstruction append-only prefixes
  privacy and graph-only scope. No Stacks chapter TeX or edition authority was
  written by this checkpoint.
- The direct threshold addendum arrived after that replay and raised the floor
  from 3,000 to 5,000 dpi-equivalent detail. D000153 I000049 the schema and
  README now require individual tightly bounded authority and final-output
  crops and extend the gate to intricate standalone mathematical blocks. The
  owner reran the validator syntax target and diff gates after this control-only
  strengthening; no 4.1 mapping or authority byte changed.

### First individual visual batch D000154 / I000050 / V000001--V000014

- A000130 inventories 445 typed diagram units and 483 deterministic
  intricate-mathematics candidates. The diagram-ID digest is
  `92837AD5EDCF2F9EE0BEED3623E4BFC260D9B5977731B11F00D1E98451E00F08`;
  the intricate-block locator digest is
  `F9D6156800B48F681A4115B165AA62C2C5812F44A7EC1979412559526C95B4F4`.
  The first queue consists of every diagram already used by the active
  statement graph, twelve items, plus two exact-sequence blocks at the reviewed
  frontier. The remaining 433 diagrams and 481 unselected block candidates
  retain no visual-certification claim.
- The three parent surfaces are exact and distinct: NUMDAM authority
  `EGA_I_PMIHES_1960_4.pdf`, 31,680,717 bytes, SHA-256
  `9ABA23020217535977E279BDD06A0413F48DA703086865BA4C00766C85DF4AE6`;
  public cumulative French `zenodo:21859616/00_FR.pdf`, 1,974,323 bytes,
  SHA-256
  `1D4332295C2F572B7D555B05E9A5786632BA9DCB9F329CEAF448CAFC2BDEC6C7`;
  and public cumulative English `zenodo:21859616/00_EN.pdf`, 14,589,396
  bytes, SHA-256
  `C70C13635EC53C10A2E1866EAB3BC9CA1B6F6601DCA8B344342DA901A70A0257`.
  A provisional check against the shorter standalone English EGA I reader was
  rejected before freeze because the controlling output is the cumulative
  reader. Every English crop was regenerated from the exact public cumulative
  byte stream.
- Full-page 5,000-dpi rendering exceeded practical memory, so every item was
  rendered by applying the 5,000/72 matrix only to its tight PDF-point clip.
  This preserves the required effective detail without a heavy page-wide
  allocation. The owner inspected all 42 crops individually at original
  detail. Twelve complete directed graphs and two exact sequences passed the
  object/term, edge, non-edge, direction, style, label, glyph, geometry, and
  label-side masks. The only differences are recorded English terminal
  punctuation on the two sequences and one diagram; no source-graph,
  mathematical, or final-render defect was found.
- `vqa.csv` is 13,674 bytes with SHA-256
  `DD25067C21EE816D5243AA55846B667C3A1E075E331FEBB4A568EDD2FD2A81D3`.
  V000001--V000014 bind 42 unique crop files totalling 12,625,106 bytes to
  exact filename-qualified record keys, one-based physical pages, top-left
  PDF-point boxes, crop bytes and hashes, effective scale, masks, signatures,
  and D000154. I000050 closes only this bounded queue and deliberately does not
  supersede the open corpus-wide I000049 gate.
- The validator pins the immutable first-batch prefix while permitting later
  append-only V successors under new QA-ID-derived paths. It rejects stale or
  duplicate active items, paths, bytes, locators, symlink/root escapes,
  unmanifested evidence, malformed or CRC-invalid PNGs, wrong parent records,
  page overflow, nonfinite boxes, and any effective scale below 5,000 dpi.
  Future mapped diagrams and selected intricate blocks cannot be promoted
  without an active certified V row.
- A000131 independently replayed every parent-PDF identity, page count,
  one-based locator, CropBox bound, TeX locus, crop byte and hash, PNG structure,
  effective scale, and nonclipping margin. It returned hard PASS within its
  read-only locator, integrity, and governance scope; graph and mathematical
  certification remained the owner's direct responsibility.
- A000132 then adversarially audited append-only successor semantics and the
  fail-closed validator. It caused four forward-history repairs: later rows use
  new QA-ID paths, supersession cannot change the stable item, decisions must
  be active visual-QA admissions, and active locator uniqueness uses canonical
  parsed page and box values rather than lexical CSV spellings. After repair it
  replayed the complete prefix, active-map closure, crop identities, source
  joins, snapshots, controls, privacy, compile, validator, and diff gates and
  returned hard PASS. It did not substitute for the owner's visual-content
  judgment.

### EGA I 4.2.1--4.2.5 and individual diagram V000015

- Direct-French review advances through 4.2.5 and stops before 4.3.1. The
  governing corrected source is `ega1-4-fr.tex`, 34,792 bytes, SHA-256
  `A5F5CDAC81E654E9ABA75BBFEAD24F3010B122452C689B9EBAB5A7711B454EC1`,
  admitted by F33, 14,944 bytes, SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`.
  P122/R45, P123/R46, and P124/R47 replay at respectively 10,598, 10,743,
  and 10,336 bytes with SHA-256 `B188DC15970531829D52CDC27BEC574A7DC056E05C5BCB9814F326657C680B14`,
  `859AE56FAFA479F12F68B1080E61100CD9B0F2C750DFA9041774516BC3CDF20C`,
  and `49BAFE90DBC08F35258F8C1AB4C3B476971B3B9B5359667B8C9D0564CC4E6A54`.
  Nine frozen units have exact I:122--I:124 locators; no page overlay was
  required.
- D000155--D000159 admit 36 edges S000555--S000590. D000160 admits the
  individual visual receipt and D000161 records the later direct-source
  referral. The slice adds 20 residuals R000354--R000373. The active scaffold
  now has 586 edges across 207 source units and 370 residuals; physical history
  has 590 edge rows and 373 residual
  rows. Of the active edges 582 resolve to 211 distinct official tags and four
  remain explicit local untagged integrations. There are 27 exact
  full-statement equivalences and the four earlier bounded open gaps remain.
- For 4.2.1, 01IO supplies the immersion definition, 01IM the exact unlabelled
  canonical factorization, 01HH and 01HO its open and closed cases, and 01L7
  plus 01S4 the mono and radicial consequences. For 4.2.2, 01HE and 0H7H split
  the open criterion while 00AE and 01QO split the closed one; 01HI and 0FCZ
  localize the locally closed case. The proof-level map and stalk ingredients
  remain explicit rather than being promoted to a false single-tag theorem.
- The printed 4.2.2 proof reverses the prose type of `theta_y^sharp`. I000051
  binds the existing authority defect
  `EG-EGA-I-P122-FR-422-THETA-DIRECTION-ERROR-001`; the proposition, the
  four-edge square, the following argument, and the English correction all use
  the correct direction from the pulled-back structure sheaf to `O_Y`.
- Direct 5,000-dpi authority inspection also exposed a previously uncatalogued
  4.2.3 defect: for `f=(psi,theta)` printed p.123 and the inherited English both
  write `Gamma(psi)` for the induced global-sections homomorphism. EGA I 1.7.3
  types that map as `Gamma(theta)`; the same one-point map on `Spec(C)` can
  underlie both identity and conjugation, so the printed notation is not
  recoverable from `psi`. I000052 and R000373 keep this canon-owned correction
  explicit, and finding `EGA-I-4.2.3-P123-GAMMA-PSI-TYPE` was sent to the
  French/English producer without writing its authority tree.
- For 4.2.3 the affine closed-immersion criterion is honestly split between
  01QO, affine duality 01I2, and quotient construction 01IG. For 4.2.4, 01JY
  supplies necessity, 0FCZ the immersion sufficiency, 02L3 the stronger open
  descent result, and 02L6 plus 01HL the closed case. The full composition
  result 4.2.5 is exactly 02V0; 01QS is retained only as its closed subclaim.
  Counterexamples preserve the affine-target and image-cover boundaries.
- V000015 individually certifies `ega:I.4.2.2:diagram:xymatrix:1` from the
  exact NUMDAM authority PDF page 122 box `238;178;128;72`, cumulative French
  page 84 box `231;198;162;73`, and cumulative English page 314 box
  `226;603;159;77`. The three grayscale 5,000-dpi crops are respectively
  177,353, 388,385, and 409,414 bytes with SHA-256
  `4F7AF7FC771985F3553AE1B310FB7883CCD9BC791B05084961662CE9A0E1444F`,
  `ED8B2BFD003DD64A2D24B26746E6E5FF91BEC85991C9929F1702F0AD28E37FA2`,
  and `F7B0885D7BA488272E2B787342592974EF5BA31B8F31C240568E70AA4E26B2FF`.
  The owner inspected each at original detail: four objects, four ordinary
  directed edges, all labels and subscripts, commutativity, geometry and label
  sides match; no hook, equality, reverse, diagonal, or additional edge exists.
  The corpus-wide I000049 gate remains open.
- A000133--A000135 independently audited the pinned targets, direct French,
  controls, generated-unit inventory, diagram graph, false near matches, and
  collision surface. No authority tree, English or French edition source, or
  Stacks chapter TeX was written by this graph-and-evidence checkpoint.
- A000136 inverse-audited every semantic edge and residual after the
  source-part and hypothesis-boundary repairs. A000137 independently replayed
  the expanded correction referral, all three parent PDFs and V000015 crops,
  append-only prefixes, snapshots, privacy, and no-TeX-write scope. Both
  returned hard PASS without substituting for the owner's direct mathematical
  or visual judgment.

### EGA I 4.3.1--4.3.2 product and base-change stability

- Direct-French review closes subsection 4.3 and stops before 4.4.1. The
  governing corrected source remains `ega1-4-fr.tex`, 34,792 bytes, SHA-256
  `A5F5CDAC81E654E9ABA75BBFEAD24F3010B122452C689B9EBAB5A7711B454EC1`,
  under F33 SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`.
  Printed-p.124 R47 is 10,336 bytes SHA-256
  `49BAFE90DBC08F35258F8C1AB4C3B476971B3B9B5359667B8C9D0564CC4E6A54`;
  printed-p.125 R48 is 10,341 bytes SHA-256
  `0B5B2C235F4E2166F5A15F084A4B8FC9592EA7426D2CB663EB916DBDAD9CA1F0`.
  The three generated units are 4.3.1 and its proof at I:124 continuing onto
  I:125 plus 4.3.2 at I:125. No page overlay or diagram unit is required.
- D000163--D000164 admit 18 edges S000591--S000608 and nine residuals
  R000374--R000382. The active scaffold now has 604 edges across 210 source
  units and 379 residuals; physical history has 608 edge rows and 382 residual
  rows. Six hundred active edges resolve to 213 distinct official tags and
  four remain explicit local untagged integrations. There are 28 exact
  full-statement equivalences and the four earlier open gaps remain unchanged.
- For 4.3.1, 01JY supplies each base-changed factor and 02V0 their composition.
  The open image is the exact inverse-image intersection of 01JR; 01JU gives
  closed pullbacks and their ideals; and 01IO reduces the general immersion
  case to the open and closed cases. The historical proof retains 01JS and
  0FCZ or 01HL for localization, 01I4 and 01I2 for affine tensor products, and
  01IH plus 01IG for quotient spectra. The closed-set calculation uses 00E5
  and 00E0. No single target is falsely described as the whole proposition.
- The affine proof contains a newly exposed author-level notation error.
  Printed p.125 unmistakably states `ker(rho tensor sigma)=u(b)+v(c)` with
  ordinary images. For `A=k`, `B=k[x]`, `C=k[y]`, `b=(x)`, and `c=0`, the
  kernel `(x)` contains `xy` but the ordinary image `u(b)` does not. The correct
  expression is `Im(b tensor_A C)+Im(B tensor_A c)`, exactly the extension-ideal
  form EGA 0 I 7.7.7 itself uses and 00DF proves by right exactness. D000162,
  I000053, R000377, and finding
  `EGA-I-4.3.1-P125-KERNEL-IMAGE-IDEALS-001` preserve print while referring the
  correction and R48 supersession to the canon owner.
- D000165 closes the source-error evidence-provenance gap without rewriting
  the published 4.2 finding. `reports/qsrc.csv` is 768 bytes with SHA-256
  `47688723470C409C20B3E0F7F0B0A95937A43BB7793E6FF49053ED5CDC0288EA`.
  Q000001 binds authority PDF
  page 122, box `88;572;182;49`, to `reports/qa/423g.png`: 274,034 bytes,
  SHA-256
  `AD6EECAD5060C23A5F73C1FC3EF900ED98E4C5426AD522DA6F47FB28773234D5`,
  dimensions 12,639 by 3,403. Q000002 binds page 124, box
  `86;335;429;37`, to `reports/qa/431k.png`: 490,151 bytes, SHA-256
  `9D799B065380ACBEA0217C3E7F50B48EE5367E2A0FF70DA216785FBF7DC811C6`,
  dimensions 29,792 by 2,571. Both are individual tight grayscale
  5,000-dpi-equivalent direct-authority receipts; they neither admit the
  corrections nor substitute for the three-surface V gate.
- Corollary 4.3.2 is exactly 01JY after the base-change definition 01JX; 01JU
  strengthens only its closed clause by supplying the pulled-back ideal.
  Neither immersion hypothesis nor the same-type refinements were weakened.
  The one three-term equality display in the proof is ordinary rather than a
  dense array or intricate standalone block and was not promoted into the
  visual-QA inventory.
- A000138 independently rehashed F33 R47 R48 and the direct source, enumerated
  all three units, replayed the pinned target bundle and false near matches,
  found the kernel error, and confirmed zero graph collisions. That read-only
  audit changed no authority source, edition source, Stacks chapter TeX,
  diagram registry, or visual receipt. The owner subsequently added
  Q000001--Q000002 and their two crop files under the separate source-error
  evidence gate described above.
- A000139 inverse-audited all 18 §4.3 edges and nine residuals against the
  pinned labels and direct French, then adversarially checked the Q schema,
  active-admission boundary, path uniqueness, append-only extension rule,
  snapshots, privacy, and duplicate closure. Its successive concrete failures
  caused the S000608 source-attribution repair and the strict Q-ID-boundary
  gate; the final live tree returned HARD PASS with no write claim and no
  visual-content certification.
- A000140 independently replayed F33, R47, R48, all three source units,
  D000162--D000165, I000053, S000591--S000608, R000374--R000382, and both Q
  receipts. It also rerendered each recorded authority page/box and found the
  committed PNG bytes pixel-identical, while retaining the owner's exclusive
  visual judgment. Its final release verdict was HARD PASS with no file write.

### EGA I 4.4.1--4.4.6 inverse images and binary infima

- Direct authority is the 34,792-byte corrected diplomatic
  `ega1-4-fr.tex`, SHA-256
  `A5F5CDAC81E654E9ABA75BBFEAD24F3010B122452C689B9EBAB5A7711B454EC1`,
  admitted by 14,944-byte F33 SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`.
  The bounded French lines 498--601 are 4,724 UTF-8/LF bytes with SHA-256
  `F05DEFC561F2212E6C0E47A25201FF9DDE3332FF7E6BA012E425DC1114017211`.
  Printed-p.125 R48 is 10,341 bytes SHA-256
  `0B5B2C235F4E2166F5A15F084A4B8FC9592EA7426D2CB663EB916DBDAD9CA1F0`;
  printed-p.126 R49 is 12,000 bytes SHA-256
  `98501091AB4641EEAFB20F2FFC7E25225189C2A2784E3EDE0AEA7773F1E19DE9`.
- The frozen inventory contains the subsection plus six statement/proof pairs:
  4.4.1 and its proof first occur on I:125; 4.4.2--4.4.6 and their proofs on
  I:126. There are no generated diagrams or equation children and no page
  overlays. The sole standalone display is the ordinary binary-meet equality
  in 4.4.4; it is not an intricate mathematical block and creates no V row.
- D000166--D000172 admit S000609--S000644 and R000383--R000414. Proposition
  4.4.1 splits over 01JU, proof-level 01S1, 001V, 01JV, 01K0, and 01J3.
  Corollary 4.4.2 uses the exact iterated-pullback identity in the proof of
  001Y. Corollaries 4.4.3--4.4.4 derive arbitrary locally closed binary meets
  from 001Y, 001V, 01JU, 02V0, 01L7, and 01IM; 0C4I remains closed-only. Proposition
  4.4.5 is the exact 01JU ideal formula with 01HQ and 00DF proof dependencies.
  Corollary 4.4.6 combines 001V, 01JU, 01HP, and 01QP.
- I000054 and R000397 carry but do not duplicate the official p.126 correction
  `EG-EGA-I-P126-FR-445-PRINTED-ALGEBRA-DIRECTION-ERROR-001`: line 586 must
  read A as a B-algebra for `A tensor_B (B/K)`. Diplomatic French remains
  untouched and the proposition itself is unaffected.
- A000141 independently audited the direct French target bundle source error
  counterexamples and collision surface. A000142 independently replayed F33,
  R48, R49, all six page ledgers, the twelve generated statement/proof units,
  and the no-diagram/no-intricate classification. Both were read-only and
  their candidate inventories were accepted only after owner target and
  authority replay.
- A000143 rejected an overstrong direct use of 001Y for the 4.4.4 proof and
  two target-side proof descriptions that had been attributed to the French.
  After S000633, S000636, S000638, R000407, R000409, and D000166 were repaired,
  it replayed the live graph and returned HARD PASS without a write or visual
  certification claim.
- A000144 independently replayed the complete repaired authority and graph
  surface including target-specific R000410--R000414. It returned HARD PASS
  on target joins, append-only history, snapshots, privacy, no-TeX-write scope,
  and the no-diagram/no-intricate classification without substituting for
  owner mathematical or visual judgment.
- A000145 exposed five cases where a stronger or partial edge was mechanically
  accepted because an unrelated residual shared its source unit. The owner
  added target-specific R000410--R000414 and tightened the repeated-001Y
  derivation. A000146 then replayed those exact repairs and returned HARD PASS
  with zero active semantic duplicates and strict binary scope preserved.

### EGA I 4.5.1--4.5.5 local immersions and permanence

- Direct authority is the 34,792-byte corrected diplomatic
  `ega1-4-fr.tex`, SHA-256
  `A5F5CDAC81E654E9ABA75BBFEAD24F3010B122452C689B9EBAB5A7711B454EC1`,
  admitted by 14,944-byte F33 SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`.
  The bounded French lines 603--682 are 3,784 UTF-8/LF bytes with SHA-256
  `253F12D3194BFF1A4374D3F939074404D675B39CDCB5ACED75C609C455791520`.
  Printed-p.126 R49 is 12,000 bytes SHA-256
  `98501091AB4641EEAFB20F2FFC7E25225189C2A2784E3EDE0AEA7773F1E19DE9`;
  printed-p.127 R50 is 11,010 bytes SHA-256
  `D631DC20C4EF98C822AA61FF29A02176382A23E40077C1D36338FE359E80EA25`.
- The frozen inventory contains the subsection and seven substantive units:
  4.5.1 and 4.5.2 begin on I:126 with 4.5.2 crossing the exact page seam;
  4.5.3--4.5.5 and the two proposition proofs are on I:127. There is no
  diagram display equation or intricate standalone block and no new V row.
- D000173--D000177 admit S000645--S000677 and R000415--R000442. Historical
  local immersion splits over 01HK and 01IO. Historical local isomorphism uses
  01HE with affine-only 096E. The 4.5.3 recognition clauses use 0FCZ only after
  the source topology produces full inverse-image charts and use 01IQ for the
  closed specialization. Proposition 4.5.4 combines 004V 01RJ 01HK and 0FCZ
  with explicit counterexamples showing that irreducibility dominance
  injectivity and local immersion are all essential. Proposition 4.5.5 uses
  02V0 01JR 01JY and 01JX; 096F and 096G remain affine-only while the exact
  product factorization in the proof of 01KU is retained as unlabelled.
- R50 already catalogued two source-proof defects and this checkpoint closes
  their high-detail evidence. Q000003 binds authority PDF page 126 and box
  `112;365;390;15` to `reports/qa/455c.png`: 180,658 bytes, SHA-256
  `D9CADDC12DFF68562DA64F2E8FAAE6408B406AB052DACF452F4BB7775E07EB13`,
  dimensions 27,085 by 1,042. It shows the printed transitivity citation
  `4.2.4`, whose unique correction is `4.2.5`. Q000004 binds the same parent
  page and box `82;420;420;44` to `reports/qa/455z.png`: 530,790 bytes,
  SHA-256
  `F7942DE4BA93153FE778DE68020331063ACE2CC6EB6F0CB691C36B3DBB6C0E3E`,
  dimensions 29,168 by 3,057. It shows the proof using `z` and `z'` before
  choosing them. D000178--D000180 and I000055--I000056 preserve diplomatic
  print and refer the corrected readings through append-only findings.
- The live English tree is exact sealed R215: 127 files and 7,283,691 bytes
  with tree SHA-256
  `FB74DC982C560AD5E154C8300D93FB0FFA9EE4754342ACE1DC7D9612A1172BB4`.
  Six files differ from R184. `r184.py` now gates the whole R215 tree before
  applying the exact producer inverses including four label-side repairs in
  `ega0-1.tex` and the two-step `ega1-4.tex` correction chain. Two serial
  no-overwrite runs reconstructed all 127 R184 files and 7,283,321 bytes with
  exact tree SHA-256
  `3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D`
  without mutating the edition source.
- `interface.json` and `scope.json` retain R184 and each historical French
  receipt as claim authority while truthfully exposing sealed R215 and F37T
  as the latest comparison markers. No unsealed live byte is admitted and no
  authority source edition source Stacks chapter TeX diagram registry or V
  receipt is changed by this checkpoint.
- A000147 replayed 4.5.1--4.5.3 against direct French and pinned 01HK 01IO
  01HE 096E 0FCZ and 01IQ. It returned HARD PASS with exact relation scopes
  and zero duplicate semantic keys. A000148 supplied the independent 4.5.4--
  4.5.5 candidate and source-defect inventory.
- A000149 correctly HARD-FAILED the first release candidate because the live
  sealed R215 tree could no longer be reconstructed by the stale five-file
  script and the new source-error crops were not yet bound. The owner added
  the sixth exact inverse chain the whole-R215 tree gate current sealed
  interface markers Q000003--Q000004 and their active admissions rather than
  suppressing that failure history.
- A000150 found and closed the remaining aggregate residual link from
  R000442 to the citation-only decision by binding it to combined admission
  D000180. It then returned HARD PASS over all 4.5.4--4.5.5 semantic and
  source-error-QA rows without making a visual-content certification.
- A000151 independently replayed F33 F37T R49 R50 the sealed R215 tree two
  serial exact R184 reconstructions both 5000-dpi report receipts every new
  append-only prefix and the privacy and no-TeX scope. It returned final HARD
  PASS after the interface wording was made exact.

### EGA I 5.1.1--5.1.4 nilradicals reduction and local integrality

- Direct authority is the 50,232-byte F33-bound `ega1-5-fr.tex` at SHA-256
  `4610C5F9E732D99948AA809ED64C85D236423990C2750A06F0DC7A805D317701`.
  Lines 1--100 are 4,990 UTF-8/LF bytes at SHA-256
  `C4C473DFA1FA795033E696AA638D19BF0B7F628B8FFA9030C57A41864AF3FB1A`.
  F33 is 14,944 bytes at SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`.
  R50 is 11,010 bytes at SHA-256
  `D631DC20C4EF98C822AA61FF29A02176382A23E40077C1D36338FE359E80EA25`;
  R51 is 10,926 bytes at SHA-256
  `94F833E316F3726489EEF9254871BB55B12EBA691B7BFEAF918F76C285A7DE41`.
  Both are PASS with empty error arrays.
- D000181 and L000024--L000027 bind four raw blank locators. Section I.5
  subsection I.5.1 and the complete 5.1.1 statement begin on I:127; all proof
  text begins on I:128 despite the frozen `begin{proof}` preceding that page
  marker. Two deterministic intakes applied all 27 active page rows and were
  byte-identical: `files.csv` remains
  `A1BB4950FE27D813FD79BCC4604607994D38E3F1E5A2C1D52EC21E01EC5C7E5F`;
  `units.csv` is
  `5E4E7E92155A1B081DC1909198632D75EA39996BE598FC37D578E3C79D91C361`;
  and `intake.json` is
  `82B07554EF81287EDC8BA70BAAA465F6991586AB4171C51C8AF69BF0EEBB2677`.
  All 9,585 stable IDs are preserved and exactly four printed-page fields
  change.
- D000182--D000187 admit S000678--S000712 and R000443--R000467. Proposition
  5.1.1 uses 01I7 01LA and 0544 only as existing ingredients. R000443 and
  R000444 retain genuine labelled gaps for the arbitrary quasi-coherent
  algebra nilradical package and the reverse localization equality. They are
  not collapsed into the structure-sheaf reduction result 01J3.
- Corollary 5.1.2 and Definition 5.1.3 split over 01IQ 01J3 01J4 0BR6 0356
  01QQ 01J2 00E0 and 01J0. Proposition 5.1.4 combines 01J2 01ON 00ES 00E0
  and 01OK. Its following unnumbered paragraph uses 01OQ 01HV 0052 01J0
  00ET 0BX3 and 01ON while preserving the distinction between locally
  Noetherian topology and a locally Noetherian scheme. Tag 0568 supplies the
  failure when the topological hypothesis is removed.
- I000057 reuses R51's catalogued French `defined Y by` word-order defect as
  a resolved grammatical issue. The two already-present English repairs on
  p.128 remain comparison-layer facts and do not alter French authority. The
  slice contains no diagram display equation grid or intricate standalone
  block. No V row is created; the next source unit 5.1.5 contains the first
  display and diagram and remains closed under I000049 until individual
  authority French and English 5,000-dpi receipts are complete.
- A000152 independently identified the thirteen 5.1.1--5.1.2 candidate edges
  and the two real labelled gaps. A000153 independently established the
  strict 5.1.3--5.1.4 mapping and the topological hypothesis boundaries.
  A000154 replayed authority controls frozen units and page seams and required
  the four exact overlays before semantic admission. All three were read-only
  and made no visual certification.

### EGA I 5.1.1--5.1.4 inverse failures and exact release repairs

- A000155 rejected the initial 5.1.2 mapping because S000689 attributed both
  the full-support containment and the intersection-of-primes identity to
  00E0. S000713 preserves the old row and supersedes it with `split` scope:
  00E0 supplies only the intersection identity. A000158 independently replayed
  the active successor and returned HARD PASS; the historical failure remains
  in A000155.
- A000156 rejected S000704 because the paragraph after 5.1.4 uses a notion
  defined earlier in 2.1.8 rather than defining local integrality anew.
  S000714 preserves and supersedes S000704, records the prior-definition
  dependency, and limits 01OQ to derived affine-neighbourhood coverage.
- The same audit exposed a new printed cross-reference defect. Proposition
  5.1.4 visibly cites `2.1.7`, but 2.1.7 concerns open restrictions; 2.1.8 is
  the definition of integral and locally integral schemes. The owner generated
  and personally inspected the tight authority-only Q000005 crop at exactly
  5,000 dpi from printed p.128, point box `90;433;417;32`. The immutable
  `reports/qa/514r.png` is 377,678 bytes, SHA-256
  `C00A8CC1A6126220003816FAE76678E00C134CA83D6C8B2F8DF8787976205277`,
  and 28,959 by 2,223 pixels. D000188--D000189, I000058, R000468, Q000005,
  and the append-only finding preserve diplomatic print and refer the corrected
  `2.1.8` reading to the edition owner. This source-error receipt is not a
  diagram or edition-output visual certification.
- A000157 then fail-closed the release because the live English comparison
  tree had advanced from sealed R215 to sealed R218 and because the four new
  I.5 page locators lacked fixed unit/page regressions. R218 is 127 files and
  7,283,691 bytes with tree SHA-256
  `35D0D86A689FCC39F074FD49EE5AE89ED7B5FCBFCF25D3943D26402C06CA0FDE`;
  its manifest is 166,531 bytes with SHA-256
  `8B83763939CB804605ED4FDD1FB3A40F7C151F1DF754EE59A491354D2D297C61`.
  The new seventh inverse path restores the two sealed label-side changes in
  `ega0/ega0-3.tex`. Two serial no-overwrite runs of the 9,848-byte
  `r184.py` at SHA-256
  `E5108DF5AC34A0327E121900E90B62B80410EB2CB7EBA15A7C41C3DD29FCFE5A`
  each reconstructed exact R184: 127 files, 7,283,321 bytes, tree SHA-256
  `3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D`.
  The checker now joins the interface and scope latest-successor triples and pins section
  I.5, subsection I.5.1, 5.1.1, and its proof to I:127/I:128 exactly.
- The final serial replay then observed sealed R219 rather than accepting the
  now-stale R218 marker. R219 is the edition task's direct propagation of this
  checkpoint's Q000005 correction: only `ega1/ega1-5.tex` changes, replacing
  the inherited 2.1.7 reference by 2.1.8. Its manifest is 168,856 bytes at
  SHA-256
  `92AED9B4880DBB958004F727DC1185BB48529A78EDC95DB5D3FF94D4316355C5`;
  the sealed 127-file tree remains 7,283,691 bytes and has SHA-256
  `AD9F9A8A17882E5DF5EE4D1CFB1EAC03EBF5E22826B97A98207A2C220D106D22`.
  The 10,274-byte `r184.py` at SHA-256
  `659EBF52943674465A6775F612FCE6BA41B43D0AEBF3338FD74CD4080765E70E`
  adds an eighth exact inverse path and fail-closes on the whole R219 tree.
  Two fresh serial R219-to-R184 reconstructions and intakes each reproduced
  tracked `files.csv`, `units.csv`, and `intake.json` byte-for-byte. Interface
  and scope expose R219 while all graph claims remain bound to their exact
  historical French receipts and frozen R184 discovery IDs.
- After both append-only semantic repairs the active graph remains 708 edges
  over 236 source units; physical history is 714 rows with six superseded.
  Residual history is 468 rows with 465 active and six open gaps. The slice
  still has no diagram or intricate standalone mathematics block; I000049
  continues to hard-gate the first display and diagram in 5.1.5.
- A000159 returned HARD PASS on the S000714 and Q000005 repair chain while
  preserving A000156 as the historical source-attribution failure. A000160
  records the second fail-closed successor drift from R218 to R219. A000161
  then independently replayed R219, both deterministic intakes, every new
  append-only row, exact page changes, privacy, and the no-TeX/no-V boundary
  and returned final HARD PASS. No agent wrote files or claimed independent
  visual-content certification.

### EGA I 5.1.5--5.1.10 reduction functoriality products and thickenings

- Direct authority remains the 50,232-byte F33-bound `ega1-5-fr.tex` at
  SHA-256
  `4610C5F9E732D99948AA809ED64C85D236423990C2750A06F0DC7A805D317701`.
  Lines 101--304 are 9,279 UTF-8/LF bytes with SHA-256
  `39A8328C323D5140A47D12437CC78B672CE63931B0AB0A77914C7CE4369804EA`.
  The exact page controls are R52 for I:129 (10,074 bytes SHA-256
  `2A69BDB7C8D978A1BC2864A66A738A5C7450A3DE567EB7A67A937817EB1E2902`),
  R53 for I:130 (10,676 bytes SHA-256
  `BDD7227EE137F2B61A57438AB84D3B564131AD214C9A1F8AFD918CE7A2472F8F`),
  and R54 for I:131 (11,936 bytes SHA-256
  `4B51F8C9B847D1D4A3C8C759CAEE6E09DD1F5EA00D5291E9623A44AF69990AA4`).
- D000190 and L000028 correct only the frozen `ega:I.5.1.9` locator from
  I:129 to I:130. The raw locator guard, F33, R53, and evidence
  `EG-EGA-I-P130-FR-ADMISSION-001` are exact; all 9,585 stable IDs remain
  unchanged.
- D000191--D000197 admit S000715--S000767 and R000469--R000498. The 53 new
  statement edges comprise 50 exact official-label references plus three
  explicit local untagged labels. The 30 residuals keep all stronger,
  derived, unlabelled, terminology, counterexample, and upstream-pending
  differences separate. The active graph is 761 of 767 physical rows over
  251 source units with six superseded; 754 active edges resolve to 241
  distinct official tags, seven are local untagged integrations, and 31 are
  exact full-statement equivalences. Residual history is 495 of 498 active
  rows with three superseded, six open gaps, and seven local-pending rows.
- `schemes-lemma-reduction-functorial` cites EGA I 5.1.5 and gives the unique
  reduction morphism, its natural square, identity, and composition.
  `morphisms-lemma-reduction-morphism-properties` cites Proposition 5.1.6 and
  gives surjective and universally-injective reflection plus forward
  preservation of immersion, closed immersion, and open immersion.
  `morphisms-lemma-reductions-fibre-product` cites Proposition 5.1.7 and gives
  the canonical product comparison and its closed universal-homeomorphism
  map into the unreduced product. No official tag is assigned.
- The first local proof audit A000162 rejected an unnecessary forward
  reference, a false target-local argument for arbitrary immersions, and an
  incomplete two-arrow fibre-product citation. The owner used the earlier
  closed-subspace uniqueness lemma, proved closed and open cases before
  factoring a general immersion, and proved both base-change arrows plus
  their composition. A000163 then returned HARD PASS; fresh two-pass isolated
  `schemes.tex`, `morphisms.tex`, and `more-morphisms.tex` builds exit zero and
  the three new labels are present in their chapter aux files.
- D000200--D000201 and I000060--I000061 record two local 04EX repairs. The
  fourth thickening condition now says closed subscheme of `X'`, not the
  tautological repeated `X`, and the explanatory paragraph says `nth order
  thickening`, not `nth order thinking`. The definitions and downstream
  mathematics are unchanged.
- A000166 supplied the deterministic 53-edge and 30-residual decomposition.
  A000169 independently replayed every direct-French attribution, official
  file, label, tag, relation, residual, hypothesis boundary, counterexample,
  and all three local statements and proofs at pinned commit a04446e5. It
  returned HARD PASS with zero active semantic duplicates and made no visual
  certification.

### EGA I 5.1 visual evidence source referral and fail-closed governance

- V000016 independently certifies the 5.1.5 reduction square against one
  tight authority, sealed B37AA French, and sealed B231 English crop at 5,000
  dpi. V000017--V000020 do the same for the 5.1.9 A/A0 block, labelled exact
  sequence, ring square, and scheme square. The owner inspected each of the
  fifteen final crops individually for complete terms, objects, edges,
  nonedges, directions, styles, labels, subscripts, punctuation, geometry,
  and label sides. The only edition differences are the recorded English
  ideal-letter normalization, two-line reflow, trailing punctuation, and
  French equation-number placement.
- J000001--J000009 preserve every rejected or nonfinal crop: clipped graph
  content, adjacent prose, an obsolete English crop, an obsolete French crop,
  and four below-floor locator candidates. D000202 covers J000001--J000005;
  append-only D000204 covers J000006--J000009. No rejected path or bytes can
  satisfy an active V receipt.
- D000198--D000199, I000059, Q000006, and finding
  `EGA-I-5.1.9.2-P131-RESTRICTION-Y-V-001` bind the exact printed defect in
  the 5.1.9.2 proof. The sentence introduces a neighbourhood V but prints
  `F|Y`; the uniquely typed local splitting is `F|V`. Q000006 binds NUMDAM
  page 130, box `86;188;425;30`, to `reports/qa/519y.png`: 348,419 bytes,
  SHA-256
  `63CA3C2A27119D40DFEB3213A6906BD8072F2FEF8E4E0214576ADEB2DBCD7A3B`,
  dimensions 29,515 by 2,084 at 5,000 dpi. The EGA Canon accepted the referral
  under REF10 while preserving diplomatic French; English was already
  corrected and footnoted, so neither reader was rebuilt or republished.
- R243 is the exact metadata-only successor that closes the EGA interface:
  35,095-byte manifest SHA-256
  `E8A3C98FA2A8950B74F89A778AB695E7CDFF9AD08966EA0BB9A28A462B46826E`,
  preserving 127 files, 7,283,701 bytes, and tree SHA-256
  `EB6A5465B872682311DD0DA7E6B633071A220C7FB957FCFB601795D5CBA1E39C`.
  `r184.py` now applies 28 exact inverse operations across 12 files and
  validates the complete sealed tree twice, including immediately before
  atomic promotion. This closes the concurrent producer-drift race reproduced
  by A000164 without mutating the edition tree.
- A000167 rejected a superficially green governance snapshot because malformed
  V/J IDs could crash, page-129 geometry was wrong, J000006--J000009 lacked an
  exact decision join, source-error tokens could be spliced across findings,
  and current evidence prefixes were mutable. A000168 materialized the narrow
  repair: structured failures, exact authority geometry and active evidence
  contracts, immutable checkpoint prefixes, flat nonsymlink crop trees, an
  explicit Q000001 companion-finding rule, and adverse mutation regressions.
  Agent writes are recorded exactly as four repository-relative paths rather
  than falsely claimed as `none`. The owner reran compilation, the complete
  checker, and diff-check after inspecting those paths.
- A000170 then replayed the complete publication surface read-only. It found
  exactly 21 tracked modifications and 26 intended new evidence files, exact
  append-only registry prefixes apart from the governed I:129 to I:130 unit
  locator overlay, unique untagged local labels, green TeX and Python gates,
  no private paths or secrets, and no remaining release blocker. This audit
  does not substitute for the owner's visual comparison recorded by V000016
  through V000020.

### EGA I 5.2.1--5.2.4 reduced locally closed subspaces and closures

- Direct authority remains the 50,232-byte F33-bound `ega1-5-fr.tex` at
  SHA-256
  `4610C5F9E732D99948AA809ED64C85D236423990C2750A06F0DC7A805D317701`.
  Exact page controls are R54 for I:131 (11,936 bytes SHA-256
  `4B51F8C9B847D1D4A3C8C759CAEE6E09DD1F5EA00D5291E9623A44AF69990AA4`)
  and R55 for I:132 (12,290 bytes SHA-256
  `C97366E68C0A41EF8D55E74D17F01A661A274F7850BB9EE24C897D1F67996C7A`).
  Nine frozen units cover 5.2.1--5.2.4 and their proofs. The slice contains no
  diagram, display, equation, or intricate standalone block. Two context-image
  paths named by the historical controls are no longer live, but the exact
  authority PDF and page receipts remain available; this is recorded as QA
  derivative attrition rather than a source defect.
- D000205 and L000029 correct only `ega:I.5.2.3:proof` from I:131 to I:132
  under F33, R55, and evidence `EG-EGA-I-P132-FR-523-PROOF-001`. Both
  deterministic intakes preserve all 9,585 IDs and change no unit field except
  that one `printed_page` value.
- D000206--D000209 admit S000768--S000788 and R000499--R000519. The 21 new
  statement edges all resolve to existing official labels; the 21 residuals
  retain every stronger, derived, proof-level, terminology, and counterexample
  boundary. The active graph is 782 of 788 physical rows over 259 source units
  with six superseded; 775 edges resolve to 243 distinct official tags and
  seven remain explicit local integrations. Residual history is 516 of 519
  active rows with three superseded, six open gaps, and seven local-pending
  rows. R000517--R000519 bind the distinct extra strength of 01J3, 01QP, and
  01HP rather than allowing nearby 0356 or composite residuals to mask those
  targets.
- The 5.2.1 statement splits exactly across 0F2L and 01J3; 00E0 and 01J2
  absorb its affine construction. The stronger 0356 criterion covers 5.2.2,
  with 01JU, proof-level 01S1, 00E0, 01J1, and 001V accounting for its proof.
  Tag 03DQ exactly matches 5.2.3. The 5.2.4 ideal inclusion is composite-
  covered by 0356, 01JU, 01QP, and 01HP and reuses the D000172 bundle. No
  genuine labelled gap, source defect, Stacks defect, or new local TeX was
  found.
- A000171 checked authority, page seams, unit inventory, visual classification,
  and collision surface. A000172 and A000173 independently checked the exact
  pinned labels, tags, relations, proof dependencies, and essential
  locally-closedness, reducedness, and image-ideal counterexamples before the
  rows were materialized.
- A000175 then rejected the first materialization because the distinct extra
  strength of 01J3, 01QP, and 01HP was masked by neighbouring 0356 or derived
  residuals. The owner appended R000517--R000519 without rewriting any prior
  row. A000176 replayed all 21 edges and 21 residuals and returned HARD PASS;
  it also found no exact disagreement with the independent sealed zh-Hans EGA
  I 1.1.14 baseline. A000177 refreshed the complete release audit after that
  repair and returned HARD PASS.
- During the release replay the standalone-English producer advanced from
  R243 to sealed R247. R247 is a 53,306-byte manifest at SHA-256
  `9A3652BA4E9A762DB0F9EA89A2B84FE26CE0DAD0BC97D3B9B3F7343C17CE4DB5`;
  its 127 files total 7,283,701 bytes with tree SHA-256
  `F152BFBC3AC3102DCE41975C27EEB373D01770F325639DF9AD01EFB6AD4F36D8`.
  The sole source delta beyond R243 is `_` to `^` at byte 78,592 of
  `ega1/ega1-10.tex` in the inverse direction. The 29-operation replay now
  gates exact R243 and R219 trees before reconstructing R184 and rereads all
  live sealed bytes immediately before promotion. The 17,617-byte `r184.py`
  has SHA-256
  `B4C2D79409012AEE4FAC0C933949D38A9BCB83C9E2A7F0D638645EEA3713527A`.
  Two fresh serial no-overwrite reconstructions and intakes each reproduced
  tracked `files.csv`
  (`A1BB4950FE27D813FD79BCC4604607994D38E3F1E5A2C1D52EC21E01EC5C7E5F`),
  `units.csv`
  (`5C73182F07F749F03C0B0F92BBA0D37884873FFF096C93AE2E1A3CDB599EDA4C`),
  and `intake.json`
  (`6252CE94351C297E9BBBACA7527FD79688D0F3B2917A0B1F82F3D87D64130C7D`)
  byte-for-byte. A000174 independently
  replayed every layer and current F37ZH, B37AB, and B232 interface identity;
  historical V and J rows remain bound to their immutable B37AA/B231 parents.

### EGA I 5.3.1--5.3.4 diagonal identities

- Direct authority is the 50,232-byte F33-bound `ega1-5-fr.tex` at SHA-256
  `4610C5F9E732D99948AA809ED64C85D236423990C2750A06F0DC7A805D317701`.
  F33 is 14,944 bytes at SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`;
  R55 is 12,290 bytes at SHA-256
  `C97366E68C0A41EF8D55E74D17F01A661A274F7850BB9EE24C897D1F67996C7A`.
  Direct-French lines 372--425 are 2,004 UTF-8/LF bytes at SHA-256
  `FAAB19CF315D64E2F48C3872648C1447FBB72CBFAF1DBFAF581320877F94390F`.
  Ten frozen statement, subitem, proof, and compatibility-anchor units all
  lie on I:132. The scope contains three ordinary displays, no diagram, and no
  intricate standalone mathematics block, so it adds no V receipt.
- D000210--D000213 admit S000789--S000803 and R000520--R000537. Unlabelled
  01KH prose supplies the exact diagonal and projection identities. Tags 001S,
  001V, and 002L provide their categorical derivation; proof-level 02X0 gives
  the product identity for algebraic spaces; proofs under 01KU and 04YR give
  stronger base-change forms; and 0038 plus 001Y reuse the D000102 pullback-
  product bundle. All official labels and tags are bound to pinned commit
  `a04446e57ec1fbc252a871afcec7752fb2807b14`.
- The new untagged `schemes-lemma-diagonal-identities` packages exactly three
  reusable scheme statements: the pairing formula, the diagonal of a product,
  and compatibility of the diagonal with arbitrary base change. Its proof is
  the universal-property comparison of the relevant projections. It is
  `LOCAL_WORKTREE`, receives no official tag, and makes no upstream-acceptance
  claim.
- R55 and stable evidence `EG-EGA-I-P132-FR-532-NUMBERING-001` preserve the
  printed jump from 5.3.2 directly to 5.3.4. `ega:I.5.3.3` is only a
  non-rendering English navigation anchor; D000212 and R000527 give it no
  mathematical edge, issue, or source-correction referral. R000523 leaves the
  source remark's forward claim through 5.3.8 open until those units are
  reviewed. No bounded source or Stacks mathematical defect was found.
- A000178--A000187 record ten visible, projectless, disposable Spark tasks.
  Two schema canaries failed closed; three later tasks were rejected for an
  underspecified nested path or incorrect tag-line results; the remaining
  bounded hash, manifest, registry, and locator shards were independently
  replayed and accepted. Every task was archived and its disappearance was
  verified. The ledger retains the actual `low` effort, and the checker now
  accepts exposed `low`, `medium`, `high`, or `xhigh` Spark effort while
  rejecting inherited Spark effort and exposed effort on inherited agents.
- A000188 independently closed the direct-French authority, page, unit,
  formula, visual-classification, and collision surface. A000189 independently
  closed the target, categorical-scope, local-gap, hypothesis, and numbering
  audit. The materialized graph has 797 active of 803 physical statement
  edges over 266 source units and 534 active of 537 physical residuals. There
  are 787 official rows using 246 distinct tags, ten local rows, 35 exact full-
  statement equivalences, seven open gaps, and ten local-pending residuals.
- A000190 adversarially replayed every source part, official label and tag,
  relation, residual, decision, and the local lemma and returned HARD PASS.
  A000191 nevertheless rejected release because the live producer had advanced
  from F37ZH/R247/B37AB/B232 to F37ZI/R248/B37AC/B233. A000192 then rejected
  the first refreshed interface because D38 was absent and the alleged DIA38
  was still the byte-identical DIA37 preimage with p.211 pending. Both failures
  remain append-only evidence; neither was masked by the green local checker.
- The owner added a distinct R248-to-R247 inverse before the existing layers:
  at zero-based UTF-8 offset 133,729 of `ega1/ega1-10.tex`, exact postimage
  `^` is restored to `_`, giving the sealed R247 file SHA-256
  `06D95A924F724193D419A6CEA9FC590381D408A3B03D724177BCD61DD238D54A`.
  R248 is a 58,687-byte manifest at SHA-256
  `C771CF817202DF1B0BC47C02DBACE0CA8AF0D27608A4E69FB4B5B31A320F6135`;
  its 127 files total 7,283,701 bytes with tree SHA-256
  `DDBF5FF8FD0D3A74ED43A06B3F9011855540BBD9D3F029256822CB68E872EE49`.
  The reconstruction now applies 30 operations across 12 paths and separately
  gates the exact R247, R243, and R219 trees.
- The producer subsequently sealed D38 (14,072 bytes, SHA-256
  `85457FA2DA4799DA1D86CBE3BB96050EDD31C8F71CC15053E33649D7F50DFA32`)
  and a true DIA38 successor (114,926 bytes, SHA-256
  `72CEEEF2435A785F1034E03860C2AB69EB089FEBF4990F0CAF9397C86A29619C`).
  They bind F37ZI, R248, B37AC, and B233, close the p.211 diagram, and record
  39 verified / 45 pending items. The current standalone reader identities are
  French 2,004,725 bytes / 168 pages / SHA-256
  `16789110240CD4ED7255D4E5802E65D1E87CD8BD416DBCE9A9EA32AD8065842F`
  and English 14,590,635 bytes / 1,346 pages / SHA-256
  `C06C6F10634ABDE5BDC6DC652F4D12725800397BE42D503D9ACC96E992B5C0C6`.
- Two fresh serial R248-to-R184 reconstructions and intakes each returned PASS
  and reproduced tracked `files.csv`, `units.csv`, and `intake.json` byte-for-
  byte. The checkpoint remained fail-closed until the producer sealed the D38
  temporary-workspace receipts. Q37BU is 12,737 bytes at SHA-256
  `1AF4F42283792825FE814E2ABA2CB4129F36B72D49A974351AFF4931F6D7670F`;
  final Q37BV is 5,585 bytes at SHA-256
  `C5D2FDEF6BDE7235CC3B78AEA1DA81BC70D019078E4F2202A06A064EDDF36707`.
  Q37BV binds F37ZI/R248/B37AC/B233/D38/DIA38/Q37BU, records two zero-error
  201-row post-cleanup replays at state fingerprint
  `9962DA981F1D81B207802E13000CA1509252DDB8CF51CC3B5C1B7A7E4F4F7C4E`,
  and verifies that `C:/tmp/EGA-d38` is absent without touching permanent
  accepted or rejected evidence. The external interface-drift gate is closed.
- A000193 then reran the repaired whole checkpoint from the current sealed
  surfaces and returned HARD PASS: exact append-only prefixes, the unique local
  label, all nine official joins, a fresh isolated Schemes build, Python and
  scaffold validators, tag and privacy gates, both serial R248-to-R184 replays,
  and fork readiness all passed. A000191 and A000192 remain preserved as the
  two historical fail-closed release findings that caused the repairs.

### EGA I 5.3.5--5.3.8 fibre squares and monomorphism criterion

- Exact authority remains F33 (14,944 bytes, SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`)
  with the 50,232-byte diplomatic `ega1-5-fr.tex` at SHA-256
  `4610C5F9E732D99948AA809ED64C85D236423990C2750A06F0DC7A805D317701`.
  Its lines 426--495 are 2,557 LF bytes at SHA-256
  `47C866A2565FC437884317C4B72F33BA5C77304E252B5BE45E28FBE1C7B166D7`.
  Page controls R55 and R56 are respectively 12,290 bytes /
  `C97366E68C0A41EF8D55E74D17F01A661A274F7850BB9EE24C897D1F67996C7A`
  and 11,033 bytes /
  `025D9BB49D0B2305199EBE54D56822E6CE7E4E38E4AAA93819EC67A560CCB091`.
- D000214--D000221 admit S000804--S000816 and R000538--R000558. S000809
  supersedes the earlier partial S000793, and R000556 closes the forward
  categorical gap R000523. The exact target bundle is 01KR, 001V, 01JX,
  01KS, 01L3, 08LR, and 003B; no new local theorem was required. A000194
  independently replayed the direct source, every label/tag join, relation,
  residual, correction, counterexample, decision, and duplicate key and
  returned HARD PASS while the visual R000552 gate was still deliberately
  open.
- Q000007 binds the printed missing `g` in 5.3.5 to EGA II Errata p.221.
  Q000008 binds the 5.3.8 proof's printed “one element” to the correct “at
  most one”; the empty-scheme monomorphism is the exact existence
  counterexample. Both findings preserve diplomatic French and carry their
  own individual 5,000-dpi authority receipts under D000216/D000219 and
  admission D000221.
- V000021 closes the 5.3.5 diagram against authority, B37AC French, and B233
  English. The first 5.3.7 authority and B234 crops were visually exact but
  their integer dimensions measured fractionally below the strict effective
  5,000-dpi floor. The checker rejected that state. J000015--J000016 preserve
  those exact rasters and D000224 records the failure; V000022 uses a complete
  floor/ceiling pixel envelope instead, while J000010--J000014 preserve the
  clipped, stale-output, and nonfinal lineage. D000222/I000064 record the
  `Delta_Y` label-side referral; D000223/I000065 and R000559 close it after
  corrected B37AD/B234 three-surface inspection. No failed artifact was
  overwritten or silently normalized.
- The producer closure is F37ZL 6,159 bytes /
  `9356CB6B4F40E72488BB1E4D8E08E34AA0965C8F96B6D880AC190C423DCB8E4C`,
  R251 25,277 bytes /
  `250A00CB2846004B788E542D0AEA0A31CB00AF2B1864ABD8C153116E97087F55`,
  B37AD 7,129 bytes /
  `B8736E90D2465E36F2DDC00499EFA2234A42B96046B79044370C87D2733A566F`,
  and B234 7,753 bytes /
  `DAC7E77E922D3142B7541142B3501E2E8507EA140A21233D3AD33491369A69BB`.
  D41R/DIA41R/REF11 are sealed, and Q37CD records two zero-error 186-row
  post-cleanup replays at fingerprint
  `31379A4907EEA1FCAEE0BFF3F4D3F9E15E8BCB9519CCD03BAAC240532DD1D55D`
  with `C:/tmp/EGA-ref11` absent.
- `r184.py` now applies 31 hash-guarded operations across 12 paths from the
  exact R251 tree through separately gated R248, R247, R243, and R219 trees to
  R184. Two fresh serial no-overwrite runs each reconstructed 127 files /
  7,283,321 bytes / tree
  `3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D`.
  Both intakes returned PASS and reproduced tracked `files.csv`
  (`A1BB4950FE27D813FD79BCC4604607994D38E3F1E5A2C1D52EC21E01EC5C7E5F`),
  `units.csv`
  (`5C73182F07F749F03C0B0F92BBA0D37884873FFF096C93AE2E1A3CDB599EDA4C`),
  and `intake.json`
  (`6252CE94351C297E9BBBACA7527FD79688D0F3B2917A0B1F82F3D87D64130C7D`)
  byte-for-byte without mutating the sealed source.
- A000195 returned the final semantic HARD PASS after the corrected F33 slice
  hash and V000022 closure. A000196 then found and closed the only remaining
  governance weakness by pinning the exact active R000559-to-R000552 visual-gap
  successor contract; its targeted decision-switch replay now fails closed.
  A000197 finally replayed the stable 16-modified/15-new-file checkpoint,
  including both serial R251-to-R184 reconstructions and intakes, append-only
  prefixes, sealed interfaces, privacy, Python, scaffold, and diff gates, and
  returned HARD PASS with zero staged or tag-tree changes.

### Mathematical Commons local-mirror policy transition

- On 2026-08-11 the user directed that upstream Stacks submission packaging
  stop after the maintainer stated that AI-assisted contributions would not be
  accepted for the foreseeable future. This does not stop source transcription,
  translation, visual QA, semantic mapping, local theorem integration, or the
  documentation of naturally encountered Stacks defects. The pinned official
  Stacks tree remains the comparison and dependency authority; the independent
  Mathematical Commons fork is the production destination.
- Upstream PRs 198, 199, and 200 were closed, and their three disposable remote
  branches (`codex/fix-picard-base-change-direction`,
  `codex/fix-generator-proof-parenthesis`, and
  `codex/fix-01kr-duplicate-arrow`) were deleted. A fresh readback found no open
  Stacks PR from the account. The high-throughput Commons branches and all local
  worktrees, audit evidence, corrections, and corpus history remain intact.
- D000234 records the independent-mirror policy. R000578--R000588 supersede the
  eleven formerly active `integrated_local_pending_upstream` residuals without
  rewriting them; every successor is active `integrated_local_mirror`. The
  active residual view is 572 rows from 588 physical rows, with 16 superseded,
  six open gaps, and eleven local-mirror integrations. No active legacy
  upstream-pending residual remains.
- The validator pins D000234 and the complete semantic tuple of every old/new
  residual pair, including source unit, kind, evidence, disposition, status,
  decision, supersession, and active state. Adverse replays that substituted an
  upstream-submission disposition or changed a predecessor and successor in
  tandem both failed closed. The active local statement-unit set and active
  local-mirror residual-unit set are exactly equal at eleven.
- A000203 independently enumerated the migration surface and returned HARD
  PASS. A first inverse audit then exposed the missing independent tuple pins;
  after repair its exact contradictory-disposition and paired-history tests
  returned HARD PASS. Historical schema vocabulary remains readable, but the
  active production path now terminates at a remotely verified Commons
  checkpoint rather than an upstream-acceptance state.

### EGA I 5.3.9--5.3.14 source-only checkpoint

- Exact authority is F33 (14,944 bytes / SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`)
  with the direct-French lines 497--594 slice at 4,033 LF bytes / SHA-256
  `649D95D1023FD47B7C6C0BE6B98D3C0D7BDEEB8582C53988FA5C7982C6D9581E`.
  Page controls R56 and R57 are 11,033 bytes /
  `025D9BB49D0B2305199EBE54D56822E6CE7E4E38E4AAA93819EC67A560CCB091`
  and 12,367 bytes /
  `AA264ADF86D4AF5B1A1BE075DC5293920009B08E57C8218993865E958BF9EC18`.
- S000817--S000836 add twenty scoped semantic edges for the diagonal
  immersion, fibre-product comparison, graph criteria and base change,
  immersion cancellation, and the pairing criterion. R000560--R000577 retain
  eighteen proof, terminology, stronger-target, and derived boundaries. The
  corrected source directions are `X times_S Y -> X times_T Y` and the
  pullback of `Delta_{S/T}`. Independent compact-versus-full dependency and
  local-lemma audits found no missing required edge or residual.
- Q000009 binds the insufficient printed proof of 5.3.9; primary EGA III.2
  Err_III,10 supplies the missing affine-local closed-image argument. Q000010
  binds the printed 5.3.13 citation `4.2.4`; the primary list-2 erratum directs
  replacement by `4.2.5`. Both exact 5,000-dpi authority crops reproduce
  byte-for-byte and diplomatic French remains unchanged. I000066 and I000067
  stay `referred_to_canon` at the reader-closure layer.
- Item four of the local untagged `schemes-lemma-diagonal-identities` records
  that arbitrary base change carries a graph morphism to the graph of the
  base-changed map under the canonical product identification. Its proof is
  the exact two-projection argument. Three isolated Schemes passes produced a
  50-page PDF of 651,288 bytes / SHA-256
  `C991E0B6E0D18E23BAE8356B2091CED0626A6B533B3661C0FE5F71CF4792FD39`;
  changed pages were inspected without a layout defect.
- The producer source seals are F37ZP 5,886 bytes /
  `FACB20FE64825D69C092D26F8546EDD0ACCEE2664B5714F17A03AC2F8CA504A5`
  and R255 26,255 bytes /
  `072A5D6251553188D86A869A9252A6A84A613B7638CAEEDD4C42B3DDD4A7A4E9`.
  F37ZP preserves the exact 18-file French tree. R255 changes only
  `ega1/ega1-5.tex` and has 127 files / 7,284,367 bytes / tree
  `B6B0A39094F1E7799C8F6C032FC1C38840597CD66075202D11F4926C8668DB4C`.
  `r184.py` now reverses the 5.3.13 citation first, gates the exact
  7,284,191-byte intermediate tree, reverses the 5.3.9 proof second, gates the
  exact R254/R251 tree, and continues through the existing lower layers. The
  complete replay is 33 exact operations across twelve paths and returns the
  frozen R184 tree without runtime dependence on temporary producer files.
- Two fresh serial R255-to-R184 reconstructions each returned 127 files /
  7,283,321 bytes / tree
  `3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D`.
  Their independent intakes returned PASS and matched tracked `files.csv`
  (`A1BB4950FE27D813FD79BCC4604607994D38E3F1E5A2C1D52EC21E01EC5C7E5F`),
  `units.csv`
  (`5C73182F07F749F03C0B0F92BBA0D37884873FFF096C93AE2E1A3CDB599EDA4C`),
  and `intake.json`
  (`6252CE94351C297E9BBBACA7527FD79688D0F3B2917A0B1F82F3D87D64130C7D`)
  byte-for-byte. Both runs reread the full sealed R255 source immediately
  before atomic promotion.
- This is deliberately a source-only successor checkpoint. The last admitted
  reader interface remains F37ZL/R251 with B37AD/B234 and the
  D41R/DIA41R/REF11/Q37CC/Q37CD closure. French B37AD remains source-compatible
  because the French successors are identity-only; English B234 is explicitly
  predecessor-only because R255 changes bytes and adds a page.
- B235 43,066 bytes /
  `BDCBF4BDB3ED548A194ABA75AF684348799610D04B00541FA31517031EFCF052`,
  RF14, DIA42R, REF14, and q37ckgen are retained only in an exact quarantine
  object. B235 falsely records zero total bytes for three rejected trees whose
  listed files sum to 13,522,363, 1,039,408, and 15,953,997 bytes. The cleanup
  generator pins four stale identities, Q37CK/Q37CL are absent, and
  `C:/tmp/EGA-ref14` remains present. None of these objects confers reader,
  closure, visual, or publication admission.
- A000204 and A000205 independently verified the source seals and rejected the
  reader closure. A000206 preserves the initial local-mirror contract failure;
  A000207 records its repaired HARD PASS. A000208 independently proved the
  citation-first/proof-second inverse order and both whole-tree gates. A000209
  then made six source/reader/quarantine mutations and every case failed
  closed. A000210 independently repeated both exact reconstruction/intake runs
  plus block-order, manifest, tree, no-overwrite, and final-reread drift tests
  and returned HARD PASS. A000211 independently replayed the French source,
  both primary errata, all twenty edges and eighteen residuals, both exact
  5,000-dpi Q crops, the local lemma and current Schemes build, append-only
  prefixes, mirror-only policy, privacy, and remote-readiness surface and
  returned the final HARD PASS.

### EGA I 5.3.5.1 visual fail-close referral

- On 2026-08-12 a fresh personal exact-5,000-dpi review found that active
  V000021 had accepted an incorrect bottom-arrow label-side signature. The
  NUMDAM authority crop on PDF page 131 at `86;574;260;70` places
  `Delta_{S|T}` below the arrow `S -> S times_T S`; the B37AIR French reader
  crop on page 90 at `240;410;299;65` and the B238R English reader crop on
  page 322 at `86;575;275;65` both place it above. The graph, all other labels,
  directions, geometry, and the already recorded equation-number placement
  remain unchanged.
- The exact live source defect is one byte in each language. French
  `ega1-5-fr.tex:437` has the caret at zero-based byte 19,828 and English
  `ega1-5.tex:316` has it at byte 18,692; both require `^` to `_`, with the
  inverse `_` to `^`. No producer source was mutated from this repository.
- D000242 supersedes D000220 and records the correction referral. I000076 is
  the active canon issue. R000606 supersedes R000548 as an open visual gap.
  V000021 remains immutable adverse history but is not an admissible current
  witness while the issue is active, and all downstream current-reader
  promotion remains fail closed.
- The failed current-reader crops are preserved as `qa/r/j31.png` (583,569
  bytes / SHA-256
  `2ED884790C7A378F54CECB3BD6B2A8C58EE4F3171825BD472EBDD8E602CCDCFA`)
  and `qa/r/j32.png` (613,948 bytes / SHA-256
  `BBAF3173A548DEDA55241CCE3D14FB997D504D33AE122C27DCAF74DAA5342962`).
  Their J rows are deliberately deferred until a corrected accepted V
  successor exists. The exact authority crop remains reusable and is not
  rejected.
- The canonical French/English producer task was notified with the precise
  line and byte loci and asked for append-only source manifests, rebuilt
  readers, direct visual closure, cleanup receipts, and deterministic inverse
  metadata. This remains Mathematical Commons work only; no upstream Stacks
  packaging or submission is involved.

### EGA I 5.1.5 and 5.1.9 visual fail-close referrals

- The same bounded exact-5,000-dpi sweep found two earlier bottom-arrow
  label-side defects. In the 5.1.5 reduction square, NUMDAM page 128 box
  `258;214;76;64` places the bottom `f` below, while B37AIR French page 88 box
  `254;126;84;68` and B238R English page 319 box `258;682;96;67` place it
  above. In the second 5.1.9 square, NUMDAM page 129 box `258;421;70;69`
  places the leftward bottom `f_0` below, while B37AIR French page 89 box
  `263;83;69;64` and B238R English page 321 box `273;68;66;67` place it above.
  Every object, edge, direction, other label, and geometric association agrees.
- The source repairs are six length-preserving one-byte edits across the three
  defects. For 5.1.5, French line 127 byte 6,169 and English line 83 byte 5,590
  require `^` to `_`; only the first occurrence is in scope. For 5.1.9,
  French line 246 byte 11,369 and English line 169 byte 10,214 require `_` to
  `^` on the unique leftward `f_0` arrow. Together with the 5.3.5 edits at
  bytes 19,828 and 18,692, the exact in-memory postimages are French
  `B4B58D0664ECAC315942727082B2999A23AEB6EF11BDB80B40E9857E37447F04`
  and English
  `B5323F253347AFAF0489059C0B6E02C850176473EBD4551DA5AA533F217AF574`.
  The Commons repository did not mutate either producer source.
- D000243 and I000077 refer the 5.1.5 defect. D000244 supersedes the mixed
  D000203 batch and I000078 refers the 5.1.9 defect; V000017--V000019 remain
  content-correct historical evidence. R000607 and R000608 retain the exact
  mathematical derivations while replacing R000471 and R000491 with active
  visual gaps. The mathematical S rows remain present, but visual and
  current-reader promotion is blocked until repaired readers and fresh
  downstream certification exist.
- Failed B37AIR/B238R crops are preserved without premature J ledger rows as
  `qa/r/j33.png` (249,144 bytes /
  `4C0DAF5CF1806A8768C9E17BFE8DBAA8C343947D26492405E72AB9B88A8C6809`),
  `qa/r/j34.png` (270,555 bytes /
  `34667D72E1A4C055BF21D3E7BEF82A1C47DF3063C692299CB56E726E84752B02`),
  `qa/r/j35.png` (228,378 bytes /
  `F8D713DA575E70B5FB90F7764300D53773F0323E9A77FE318C344CDEA1A9776A`),
  and `qa/r/j36.png` (231,635 bytes /
  `A0674180FE13DD600251D916200BD537008C19A1CFFB39AE646B3088E1CB16D0`).
  J000033--J000036 remain reserved until corrected active V successors exist.
- Independent original-detail review of every V000008--V000025 surface found
  no fourth defect. The producer was told that the final correction batch is
  exactly 5.1.5, 5.1.9 diagram 2, and 5.3.5, in addition to the already
  corrected p.109 `pi''` side. Commons keeps V000008--V000025 operationally
  quarantined until the canonical producer seals a repaired final lineage.

### D48 final current-reader closure

- The canonical producer subsequently sealed the exact three-repair source
  manifests F37ZW (13,345 bytes / SHA-256
  `0A56D886058B8203C34A9CDAA52B2CBF4EF4E6ED871C053CB7ADAA0F766690A0`)
  and R261 (32,444 bytes / SHA-256
  `A87DC2EDD0BDA5CE6828A2759095B1F4F3278E993DC5661EBA2E345C33BEEF18`).
  Their exact live trees replay as 18 files / 1,014,921 bytes / tree
  `5A2A1BC407D5B0395C5E0D10103E0813C4EC9EDE37668D4DCA1091D1D280A841`
  and 127 files / 7,284,367 bytes / tree
  `3FF379C715F99D2A28F231A54D55996E9CDA27153E5DBBFB14BA6F7F70766CB0`.
  The three inverse markers in each source restore the exact F37ZUR/R259R
  trees without changing any other row.
- B37AJ and B239 seal the corresponding 168-page French and 1,347-page
  English readers. D48 binds the three repaired diagrams. DIA48T is the
  admitted 84-item inventory with 53 verified / 31 pending and next cursor
  `DIA:ega1/ega1-3-fr.tex:699`. Q37CY binds the exact 12-row pre-cleanup tree;
  Q37DB binds Q37CZ, retains Q37CU/Q37CV as adverse evidence, supersedes the
  malformed Q37CX correction, proves `C:/tmp/EGA-d48x` absent, and closes the
  admitted cleanup lineage. Publication remains quarantined.
- DIA48, DIA48R, DIA48S, Q37CU, Q37CV, Q37CW, and Q37CX remain immutable
  rejected control history. They contain stale inventory pointers or malformed
  comma-bound permanent/supersession arrays and are forbidden from every
  admitted interface field. The interface and scope mirror this exact adverse
  object rather than erasing the failed attempts.
- V000027--V000044 are fresh exact-5,000-dpi current-reader successors for
  every affected or downstream witness. V000027 was independently rerendered
  from its declared B37AJ/B239 boxes after the checker rejected mismatched
  raster dimensions: the corrected French crop is 10,000 x 5,333 pixels,
  407,228 bytes, SHA-256
  `3AC6EE495DD99E4C23177295382CD58CF9811688488BC74000D94DC18CEDA748`;
  the English crop is 10,667 x 5,667 pixels, 445,513 bytes, SHA-256
  `184C73331F676B71E02B23624DA1D492E4BA815CD3659F476CF85FB915D1C15E`.
  Personal original-detail comparison confirms the complete two-by-three
  graph, all arrows and labels, and the corrected left-side `pi''` placement.
  No scale exception was introduced.
- J000031--J000036 now bind the six predecessor-reader adverse crops to their
  exact active successors. D000245 admits the full D48 interface; D000246
  admits the current visual successor set; D000247--D000249 close the three
  label-side referrals. I000079--I000087 and R000611--R000616 preserve the
  corresponding append-only issue and residual successor chains.
- The deterministic R261-to-R184 replay is 41 operations across twelve paths.
  Both reconstructed outputs contain 127 files / 7,283,321 bytes / tree
  `3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D`.
  All source and intermediate manifest, file, block, tree, ordering,
  no-overwrite, and final-reread gates remain fail closed.
- A later D49 producer line is not consumed by this checkpoint. Independent
  replay found DIA49R3 internally split between 53/31 and 54/30 counts,
  Q37DA recording zero temporary bytes for a 1,336,647-byte tree, a disconnected
  cleanup predecessor, and incomplete rejected lineage. D49 therefore confers
  no source, reader, inventory, cleanup, visual, interface, or publication
  admission in the Commons mirror.
- Immediately before staging, two fresh no-overwrite R261-to-R184 runs and two
  independent intakes again returned byte-identical outputs. Tracked and both
  regenerated copies of `files.csv` (13,987 bytes /
  `A1BB4950FE27D813FD79BCC4604607994D38E3F1E5A2C1D52EC21E01EC5C7E5F`),
  `units.csv` (1,864,094 bytes /
  `5C73182F07F749F03C0B0F92BBA0D37884873FFF096C93AE2E1A3CDB599EDA4C`),
  and `intake.json` (1,132 bytes /
  `6252CE94351C297E9BBBACA7527FD79688D0F3B2917A0B1F82F3D87D64130C7D`)
  match exactly. A fresh two-pass standalone Schemes build produced a clean
  50-page 651,424-byte PDF at SHA-256
  `FC78EE27D50D6C2C53458C53EE642AB089ED29FD0993026DAAA293906C16B336`;
  personal inspection of pages 39--41 found the five-part diagonal lemma and
  its projection proof unclipped and legible, with no changed-line overfull
  box or duplicate-label warning.

### EGA I 5.4.1--5.4.8 semantic checkpoint

- Direct French lines 670--772 on printed pp.135--136 were replayed from the
  canonical source. The LF-inclusive slice is 4,208 bytes / SHA-256
  `AE4ED884CE3E0F16B9854CABCBA9D5F184B7AB2EBD8B2B33AC344E43EDAA07BE`.
  Every new statement edge remains bound to the admitted semantic receipt
  F33.json, 14,944 bytes / SHA-256
  `2652207F96F697935BC81C5D63B292DE4D956905D69CB92572225E320BB27F4C`.
- D000250--D000257, S000853--S000879, and R000617--R000634 admit the eight
  numbered results and all six proof units without inventing a source unit,
  official tag, issue, or local theorem. The final statement snapshot is 872
  active / 879 physical / seven superseded rows across 307 source units, with
  859 official-tag rows, 252 distinct tags, thirteen local-mirror rows, and
  forty exact full-statement equivalences. The residual snapshot is 609 active
  / 634 physical / 25 superseded, with six open gaps and thirteen local-mirror
  rows.
- Exact joins are 01KK for separatedness; 01KJ plus 01IQ for the topological
  diagonal criterion; 01KR and 01KS for comparison and graph clauses; item
  three of 07RK with 01QR/01QS for cancellation; 01KU, 07RK, and 001V for
  closed pairings; and 01KT for sections. The generic-point theorem retains
  the composite 01J5/01KM/004X/0356/001V route and explicitly rejects 01RH as
  a direct match because a generic point need not be open.
- The middle converse in 5.4.8 is typed with base Y, structural map p1 on
  Y times_Z Y, j equal to id_Y, and g equal to Delta_Y_over_Z. The doubled
  origin, dual-number base, and reducible base counterexamples keep
  separatedness, reducedness, and irreducibility distinct. No mathematical or
  source defect was found.
- The slice contains no registered diagram, equation child, or selected
  intricate standalone block. It adds no V/J/Q/page row and changes no TeX,
  PDF, reader, producer source, or publication surface. A000218--A000224
  record the schema, semantic, producer-frontier, adversarial, and
  checker-hardening audits.
- A fresh read-only producer replay found F38L/R276/B37AL/B241/D63/DIA63 and
  Q37ED/Q37EE byte-coherent at their own payload level, but admission remains
  closed. Every final inventory from DIA49R3 through DIA63 retains stale
  top-level aggregate counts 53/31 while its actual and publication-gate
  totals advance; DIA63 is actually 68/16. D59 onward also records character
  indexes as UTF-8 byte offsets for the 5.5.12 repair: the declared French and
  English offsets are 47,778 and 46,893 while the actual marker bytes are
  48,651 and 46,901. The admitted Commons interface therefore remains D48 and
  publication stays disabled.

### EGA I 5.5.1--5.5.13 semantic and source-error checkpoint

- Direct-French review now covers the whole separatedness subsection through
  5.5.13. D000258--D000271, S000880--S000986, and R000635--R000695 bind every
  actual statement, proof, labelled identity, and registered diagram unit to
  exact labels at pinned Stacks commit
  `a04446e57ec1fbc252a871afcec7752fb2807b14`. The final graph contains 979
  active / 986 physical statement rows across 333 source units, 966 existing-
  tag rows using 269 distinct official tags, thirteen local-mirror rows, and
  42 exact full-statement equivalences. Residual history contains 670 active /
  695 physical rows, 25 superseded rows, ten open gaps, and thirteen active
  local-mirror rows. The next semantic cursor is EGA I 6.1.1.
- The theorem audit retains the finite closed-family hypothesis in 5.5.4,
  separates the two directions and quantifiers in 5.5.8--5.5.9, reads the
  historical `scheme` target in 5.5.10 as separated, and treats the arbitrary-
  property package in 5.5.12--5.5.13 as formal composite coverage. Reduction
  arrows are closed by 01J4, factor through 0356, and are separated for
  cancellation by 01L7; no one-tag theorem is invented.
- D000272--D000276, I000088--I000091, Q000011--Q000014, and four new findings
  preserve three wrong 5.5.4 references and both 5.5.11 mathematical defects.
  Each wrong reference uniquely requires target-locality Proposition 5.5.5.
  The doubled-line exceptional fibre is over `(s)`, not `(0)`. For the doubled
  plane, the punctured overlap is nonaffine but has global ring `k[s,t]` and
  full identity restriction images, so only the first separation criterion
  fails. The fourteen-row source-QA manifest is 4,416 bytes / SHA-256
  `91EAAF72648ACDDE00F6D20D014DB60F0071C8BDEDDA2027D2E07FE4C2182086`;
  its fourteen immutable authority crops total 5,763,117 bytes. Diplomatic
  source is unchanged.
- The first Q000011--Q000014 render attempt was rejected before admission:
  bundled `pdftoppm` returned correctly sized but pure-white PNGs after a
  high-resolution allocation failure. The accepted replacements were rendered
  in grayscale by Poppler `pdftocairo` 24.04.0 (binary SHA-256
  `433369ECCDC3FDC640A0970075E05221EF954B84119AB6551EEEF5EC10BB8D69`),
  personally inspected, and checked for nonwhite pixels. `check.py` now rejects
  blank source-error crops, including dimension- and hash-valid ones.
- S000908--S000910 and S000982--S000983 remain valid semantic mappings for
  three diagram units. Their visual status is independently fail closed under
  I000092, I000093, I000095 and R000659, R000660, R000682. The unallocated
  intricate block remains under I000094/R000661 without inventing a unit.
  D56--D59/D65 are nonadmitted producer discovery only; no V or J row is added
  and the current interface remains F37ZW/R261/B37AJ/B239/D48/DIA48T/Q37CY/
  Q37DB. The ordered active referral set is exactly I000088, I000089,
  I000091--I000095; I000090 is resolved.
- A000225--A000230 record the two bounded semantic audits, the adversarial
  hypothesis/source-defect audit, the checker-hardening plan, the independent
  post-write mathematical audit, and the independent final release audit. One
  redundant provisional residual for the two 5.5.9 citations was removed before
  sealing, leaving one canonical append-only record. Prefix replay, exact
  source-QA joins, LF-only files, semantic-only diagram isolation, adversarial
  mutations, compilation, privacy, diff, and remote verification remain release
  gates.

### EGA I 6.1.1--6.1.13 Noetherian and local-topology checkpoint

- Direct-French review covers all thirteen numbered units and nine registered
  proof units in the subsection. D000278--D000290, S000987--S001066, and
  R000696--R000741 bind 80 semantic edges and 46 residual contracts to the
  admitted F33 receipt and pinned Stacks commit
  `a04446e57ec1fbc252a871afcec7752fb2807b14`. Unnumbered French lines 15--34
  and 81--83 are explicitly routed as source parts. No formula or diagram child
  exists and no V, J, or page row is added.
- The final graph contains 1,059 active / 1,066 physical statement rows across
  355 source units, 1,046 existing-tag rows using 289 distinct official tags,
  thirteen local-mirror rows, and 49 exact full-statement equivalences.
  Residual history contains 716 active / 741 physical rows, 25 superseded rows,
  ten open gaps, and thirteen active local-mirror rows. M000024 adds one
  explicitly topical-only bridge from EGA I 6.1 to Stacks section 01OU. The next
  semantic cursor is EGA I 6.2.1.
- The 6.1.5 non-Noetherian product warning is fully derived without inventing
  a tag. For `K=k(x_1,x_2,...)`, 01JQ and 01OW reduce the scheme claim to
  `K tensor_k K`; 00RW identifies the diagonal conormal module with
  `Omega_(K/k)`, while 00RX, 00RT, and 031G make that module infinitely
  generated. The local-component and neighbourhood results retain every
  finite-component, nonempty, connected, reduced, irreducible, and local
  Noetherianity hypothesis at its exact proof boundary.
- Two source findings are admitted append only. In the 6.1.8 proof the claimed
  complement in all of X is missing intersection with U; the generic point of
  `Spec(k[t])` with `U=D(t)` is a bounded counterexample. In 6.1.12 the printed
  integrality criterion omits nonemptiness under EGA's convention. D000291--
  D000293, I000096--I000097, Q000015--Q000016, and findings 25--26 bind the
  exact evidence while leaving diplomatic French untouched. The sixteen-row
  source-QA manifest is 5,012 bytes / SHA-256
  `167BA57EBD509192C90823DAE4FB9DB928EC2EF35DFC85668293E8298AD9144A`;
  its sixteen crops total 6,022,269 bytes.
- Candidate generation no longer reads mutable live Stacks TeX or a CRLF
  worktree tag registry. `map.py` replays the root TeX and tags blobs at the
  pinned commit and `--check` verifies the generated outputs without writing.
  The deterministic snapshot is 21,446 labels, 21,437 tag joins, 36 topics,
  and 2,749 candidates. The Noetherian topic is split from approximation.
- A000231--A000235 record the combined schema/provenance plan, the two bounded
  semantic audits, the independent live post-write audit, and the independent
  final release audit. The checker, privacy, deterministic-map, compilation,
  and diff gates all pass before staging; Git and remote replay remain the
  release gates for this checkpoint.
