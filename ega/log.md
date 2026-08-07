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
