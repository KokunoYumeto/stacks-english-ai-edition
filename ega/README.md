# EGA discovery and integration scaffold

This branch is a public, machine-readable working scaffold for comparing
*Éléments de géométrie algébrique* (EGA 0--IV) with the current Stacks
Project. It is **not** a claim that EGA has been fully rewritten in Stacks
form, accepted upstream, or formally verified.

The complete standalone English EGA source is admitted only as discovery
text. Canonical source claims remain gated by the separately maintained
diplomatic French edition and its page-level authority receipts. The edition
trees are read-only inputs to this branch and are never copied, edited, built,
or published here.

## Current snapshot

- Stacks upstream base: `a04446e57ec1fbc252a871afcec7752fb2807b14`.
- English discovery manifest: R184, 92,445 bytes, SHA-256
  `5C64ECD32FD7C5458D2599D70ED667D2CF06D95517EFFA9C6D6DCEF7626913A0`;
  127 files, 7,283,321 bytes, tree SHA-256
  `3BFB1C5103093481246EF4A6365E08544F6D5E19ACC0EA63E717F3F3643F064D`.
- French authority: production is active; the current interface snapshot has
  EGA II printed p.20 sealed and printed p.21 as the next cursor.
- Existing incremental pre-Stacks notes: 399,689 bytes, SHA-256
  `4B4811B6F24F139020E15CF27D7BFA82C3872F0A549DCFF4F64B28F4454737D6`.
  They are evidence to normalize into the new schema, not a completed
  deliverable or an upstream mapping.
- Verified discovery inventory: 127 exact source files and 9,585
  metadata-only semantic units including 445 native diagram units. No source
  prose is copied into the branch.
- Current Stacks snapshot: 21,446 chapter labels, 21,437 exact official-tag
  joins, and 2,670 lexical candidates across all 35 discovery topics. Reviewed
  lexical candidates remain exactly zero in `map.json`.
- First bounded review slice: 23 source-subsection-to-Stacks-section bridges
  across 22 EGA I subsections and eight topics. These are explicitly
  topic-level split correspondences; they claim zero theorem equivalences and
  zero complete source-subsection coverage.
- First statement-level slice: all fifteen numbered units in EGA I 1.1.1--1.1.15
  were checked directly against admitted French and the pinned Stacks base.
  `smap.csv` records 22 exact edges across fourteen units; `resid.csv` records
  every partial, derived, unlabelled, terminology, or missing-tag remainder.
  EGA I 1.1.3 has no direct tagged target.
- First local integration: EGA I Proposition 1.1.15 is now a cited Algebra
  lemma with an explicit use in `more-algebra.tex`. It fills a fact previously
  used there without a named target. Its label is local and has no official
  tag or upstream-acceptance claim.
- Second statement-level slice: all seven numbered units in EGA I 1.2.1--1.2.7
  were checked against the same direct French authority. The cumulative map
  now has 34 edges across 21 source units and 13 explicit residuals. Exact
  existing targets include 00E2, 00E3, 00E5, and 00FL.
- Second local integration: EGA I Corollary 1.2.4 supplies a general
  unit-times-image criterion for a spectrum map to be a homeomorphism onto its
  image. The new untagged lemma now supplies the common topology step in the
  quotient and localization proofs.
- Third statement-level slice: all fourteen numbered units in EGA I
  1.3.1--1.3.14 now have direct-French dispositions. The cumulative map has 56
  edges across 34 source units and 24 explicit residuals. This slice required
  no new Stacks lemma: the apparent remainders are notation or consequences of
  the affine equivalence and its exact tensor and colimit behavior.
- Fourth statement-level slice: EGA I 1.4.1--1.4.3 now have direct-French
  dispositions. The cumulative map has 62 edges across 37 source units and 28
  explicit residuals. The exact four-way quasi-coherent characterization is a
  cited local Properties lemma with no official tag. Lemma 1.4.1.1 remains a
  proof-device residual; 01PE covers 1.4.2 more generally; and 01SA--01SB split
  the algebra and module clauses of 1.4.3.
- Fifth statement-level slice: EGA I 1.5.1--1.5.4 now have direct-French
  dispositions. The cumulative map has 72 edges across 41 source units and 31
  explicit residuals. Tags 01XZ and 0GN6 contain the coherent-sheaf results;
  0EHM 01PE 01PF 01IA and 01PB give the two extension packages without a new
  omnibus lemma. This review also repaired one wrong internal reference in the
  proof of 01PI from the finite-presentation criterion to the finite-type
  criterion.
- Sixth statement-level slice: EGA I 1.6.1--1.6.10 and displayed formula
  1.6.5.1 now have direct-French dispositions. The cumulative map has 99 edges
  across 52 source units and 41 explicit residuals. Existing affine-spectrum,
  associated-sheaf, adjunction, localization, tensor, internal-Hom, and
  categorical functoriality results cover the whole slice; no new lemma or
  source correction was needed. The map-identification statement in 1.6.8 is
  deliberately not promoted to flat base-change isomorphism tag 0C6I.
- Seventh statement-level slice: EGA I 1.7.1--1.7.5 and its labelled
  global-to-local square now have direct-French dispositions. The cumulative
  map has 112 edges across 58 source units and 46 explicit residuals. Tags
  01HW 01HB 01I1 and 01I2 exactly split affine recognition and the opposite-
  rings equivalence; 01IG gives a stronger closed-immersion form of the final
  quotient monomorphism. No new Stacks lemma was needed.
- Eighth statement-level slice: EGA I 2.1.1--2.1.8 now have direct-French
  dispositions. The cumulative map has 130 edges across 66 source units and
  51 explicit residuals. Modern scheme terminology exactly absorbs EGA's
  `prescheme`; sobriety merges the Kolmogorov and generic-point results; and
  the rational-function and locally-integral clauses remain split so neither
  fieldhood nor a false stalkwise criterion is introduced. No new Stacks
  lemma was needed.
- Ninth statement-level slice: EGA I 2.2.1--2.2.10 and numbered formula
  2.2.4.1 now have direct-French dispositions. The cumulative map has 168
  edges across 77 source units and 67 explicit residuals. Existing definitions
  and lemmas cover locally ringed morphisms affine targets module mappings
  permanence locality and componentwise birationality; ordinary closedness is
  kept rigorously separate from closed immersions and universal closedness.
  No new Stacks lemma was needed.
- The intake registry now recognizes all 430 native Xy-pic commands as well
  as 15 tikz-cd environments. Synthetic diagram IDs are deterministic within
  their semantic parent. This repairs an actual pre-Stacks graph omission;
  source prose and diagram artwork remain uncopied.

## State model

Every source unit and topic advances independently through:

`discovery` -> `candidate` -> `reviewed_existing` or `reviewed_gap` ->
`integrated_local` -> `built` -> `remote_checkpoint` ->
`upstream_feedback` -> `upstream_accepted`.

No state is inferred from a successful build alone. No new label is an
official Stacks tag unless upstream assigns it. Historical source defects,
English corrections, mapping reversals, and maintainer feedback are recorded
append-only.

## Files

- `scope.json`: exact claims, exclusions, inputs, and upstream base.
- `src.csv`: source surfaces and authority state.
- `topics.csv`: corpus-wide discovery topics; initially unreviewed.
- `dec.csv`: append-only mapping and policy decisions.
- `issues.csv`: source, mathematical, and integration issues.
- `fb.csv`: upstream feedback and its disposition.
- `schema.md`: stable IDs, evidence rules, and promotion gates.
- `check.py`: local structural validator.
- `intake.py`: deterministic manifest verification and metadata-only unit
  extraction; it does not copy source prose.
- `files.csv`, `units.csv`, and `intake.json`: generated exact-file inventory,
  stable unit registry, and fail-closed intake receipt.
- `map.py`, `cand.csv`, and `map.json`: lexical candidate generation against
  the exact upstream Stacks snapshot. Candidates are not reviewed mappings.
- `tmap.csv`: French-admitted topic-level bridges to existing Stacks sections;
  granularity and non-coverage claims are explicit in every row.
- `smap.csv`: French-admitted statement and statement-component edges to
  exact existing labels or explicitly untagged local labels.
- `resid.csv`: noncoverage, partial coverage, terminology migration,
  stronger-target, derived, and upstream-pending residuals.
- `agent.csv`: exact task IDs, bounded scopes, runtimes when exposed, returned
  findings, owner checks, accepted/rejected dispositions, and write claims.
- `interface.json`: hash-bound read-only contract with the active French and
  English EGA edition task.
- `log.md`: concise operating log, agent/Spark TODOs, and exact outcome
  records.
- `../reports/findings.jsonl`: append-only suspected-correction referrals;
  the edition task alone decides and mutates canonical source.

The immediate work is sequential statement-level comparison across EGA 0--IV,
continuing after EGA I 2.2.10 while EGA II is admitted through printed p.23.
The complete English discovery surface drives provisional candidates only.
Mathematical Stacks chapter edits occur only after a bounded unit has direct
French evidence, a reviewed disposition, explicit residual accounting, and
owner verification.
