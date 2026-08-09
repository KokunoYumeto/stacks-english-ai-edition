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
