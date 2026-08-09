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
- French authority: production is active; the latest sealed interface marker
  is F37T through EGA II printed p.37, with printed p.38 next. This graph still
  binds every reviewed EGA I claim to its exact historical page receipt;
  receipt F33 also repairs 4.1.9 from `g'` to the directly verified printed
  `g` without changing the already-correct English.
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
- Tenth statement-level slice: EGA I 2.3.1--2.3.2 now have direct-French
  dispositions. The cumulative map has 178 edges across 79 source units and
  71 explicit residuals. Tags 01JB 01JC and 01IT cover unrestricted scheme
  gluing and affine reconstruction. Tag 01JE is the exact projective-line
  inversion example; the nearby doubled-origin example 01JD is explicitly
  excluded. No new Stacks lemma was needed.
- Eleventh statement-level slice: EGA I 2.4.1--2.4.8 and the labelled
  affine-chart diagram now have direct-French dispositions. The cumulative map
  has 219 edges across 88 source units and 82 explicit residuals. Tags 01J6
  and 01J7 organize local-spectrum mapping and generalizations; 00E3 and 02C6
  supply topology and stalks; 0B8M and 0BDA cover invertible modules and the
  factorial comparison. The unrestricted field-point sentence in 2.4.5 is
  false without a closed-image hypothesis and has been referred append-only
  to the canonical edition rather than silently normalized. No Stacks TeX
  change was needed.
- Twelfth statement-level slice: EGA I 2.5.1--2.5.5 and the native commuting
  triangle now have direct-French dispositions. The cumulative map has 242
  edges across 94 source units and 93 explicit residuals. Tags 01JX and 001G
  give the scheme-over-base and slice-category language; 01JB and 01HI cover
  gluing and open factorization; 01KT supplies the section definition. The
  historical change-of-base operation is explicitly distinguished from
  Cartesian base change. The printed S-morphisme type error in 2.5.5 reuses
  the canonical producer's existing correction record and is not silently
  changed or duplicated here. No Stacks TeX change was needed.
- Thirteenth statement-level slice: EGA I 3.1.1 now has a direct-French
  disposition. The cumulative map has 253 edges across 95 source units and
  100 explicit residuals. The arbitrary sum is the empty-overlap specialization
  of 01JB and 01JC with 00AL and 00AM retaining its transported sheaf layers;
  002J records the coproduct property. Tags 00ED and 01I5 cover the binary
  affine formula. The graph explicitly prevents its false extension to
  infinite ring products and leaves the English-only I.3.1 wrapper alias
  unpromoted. No Stacks TeX change was needed.
- Fourteenth statement-level slice part one: EGA I 3.2.1--3.2.5 now have
  direct-French dispositions. The cumulative map has 274 edges across 100
  source units and 115 explicit residuals. Tags 01JP and 01I4 give the exact
  fibre-product definition and affine tensor construction; 003B, 01L3, and
  01KR give invariance under a monomorphic base; 01HI and 01L7 give the
  open-base corollary. Product-in-the-slice terminology,
  tensor-versus-direct-ring-product variance, and categorical monicity remain
  explicit. No Stacks TeX change was needed.
- Fourteenth statement-level slice part two: EGA I 3.2.6--3.2.8 now have
  direct-French dispositions. The cumulative map has 299 edges across 108
  source units and 136 explicit residuals. Tag 01JM supplies global existence;
  01JR gives the open-product identification; 01JJ, 01JB, and 01JC retain the
  local gluing proof; and the two-family disjoint-sum formula remains a derived
  scheme-specific result rather than a generic categorical law. The discovery
  unit 3.2.9 is a translator augmentation citing the EGA II errata and remains
  fail-closed pending that exact French authority. No Stacks TeX change was
  needed.
- The intake registry now recognizes all 430 native Xy-pic commands as well
  as 15 tikz-cd environments. Synthetic diagram IDs are deterministic within
  their semantic parent. This repairs an actual pre-Stacks graph omission;
  source prose and diagram artwork remain uncopied.
- EGA I 3.6.1--3.6.5 now has direct-French statement and proof dispositions.
  Nilpotent thickening is separated from ordinary fibre topology; relative
  field-valued points are distinguished from absolute points; and fibre
  transitivity and local-spectrum stalk preservation retain their exact
  proof-level dependencies. The two French-labelled plain displays remain
  parent components because frozen R184 supplies no child IDs. No new gap or
  Stacks chapter edit was needed.
- EGA I 3.7.1--3.7.3 now closes section 3. Quotient-base reduction is kept
  distinct from nilreduction; the generic/special fibre model construction is
  decomposed into open base change and quasi-compact scheme-theoretic image;
  and the proper DVR point bijection is identified with the valuative
  criterion. A p.119 control phrase that could wrongly extend that bijection
  to higher-dimensional local domains is referred append-only with an exact
  projective-line counterexample. The French source itself is correct.
- EGA I 4.1.1--4.1.10 now has direct-French statement and proof
  dispositions. Quasi-coherent closure properties match the exact global
  enumeration under 01LA while retaining the affine proof dependencies;
  ideal quotients and locally closed subschemes are
  split into their sheaf and scheme layers; and factorization through a
  subscheme is separated from set-theoretic image containment. F33 and its
  P121S superseder correct the one diplomatic error found in this slice:
  printed p.121 has unprimed `g` throughout the 4.1.9 proof. The English was
  already correct. Five genuinely blank frozen page locators are now guarded
  and overlaid append-only; an empty parsed guard is never a wildcard.
- EGA I 4.2.1--4.2.5 now has direct-French statement proof and diagram
  dispositions. Immersions are separated from their canonical locally closed
  factorization; the open and closed criteria are split into topology and
  stalk or sheaf conditions; and affine closed immersions and local-on-target
  criteria retain their exact hypothesis boundaries. The printed 4.2.2 proof
  contains the already catalogued reversal in the prose type of
  `theta_y^sharp`; the proposition, diagram, continuation, and English
  correction are mathematically coherent. No Stacks TeX change or new
  mathematical gap was needed. Direct 5,000-dpi review additionally found that
  4.2.3 prints the induced global map as `Gamma(psi)` although the typed sheaf
  component is `theta`; diplomatic text stays untouched and D000161/I000052
  refer `Gamma(theta)` to the owning corrected French and English layers.
- EGA I 4.3.1--4.3.2 now has direct-French statement and proof dispositions.
  The product of two immersions is decomposed into two base changes followed by
  composition; open and closed pullbacks recover the stated inverse-image
  intersection; and 4.3.2 is exactly the base-change theorem 01JY. Direct
  5,000-dpi review found that the historical affine proof writes the kernel as
  the sum of the plain images `u(b)+v(c)`, which is false without taking the
  generated extension ideals. D000162/I000053 preserve diplomatic French and
  refer the correct tensor-extension formula to the corrected French and
  English layers. The theorem itself and its modern proof are unaffected.
- D000165 and `../reports/qsrc.csv` make the two direct-authority source-error
  witnesses exact and replayable. Q000001 binds the earlier p.123
  `Gamma(psi)` witness at 274,034 bytes, SHA-256
  `AD6EECAD5060C23A5F73C1FC3EF900ED98E4C5426AD522DA6F47FB28773234D5`,
  dimensions 12,639 by 3,403. Q000002 binds the p.125 kernel-formula witness
  at 490,151 bytes, SHA-256
  `9D799B065380ACBEA0217C3E7F50B48EE5367E2A0FF70DA216785FBF7DC811C6`,
  dimensions 29,792 by 2,571. Both are individual tight
  5,000-dpi-equivalent grayscale authority-only receipts. They do not admit
  either correction and do not replace authority/French/English visual QA.
- D000153 and I000049 bind the strengthened diagram gate. The deterministic
  inventory contains 445 registered diagrams and 483 intricate-block
  candidates. D000154, I000050, and V000001--V000014 certify the first bounded
  queue: all twelve diagrams already carrying statement-map claims and two
  exact-sequence blocks at the reviewed frontier. Each item has a separate
  tightly bounded crop from direct authority, cumulative French, and cumulative
  English at an effective scale of at least 5,000 dpi, for 42 committed crop
  files. Complete graph or mathematical-chain masks passed and no EGA source or
  render defect was found. D000160 and V000015 separately certify the newly
  mapped 4.2.2 stalk square on all three surfaces. The remaining 432 discovery
  diagrams and 481
  unselected block candidates remain explicitly uncertified; each future
  promotion requires its own active V row. Shared, full-page, and grouped crops
  do not qualify.
- Current statement-level frontier: direct-French review is complete through
  EGA I 4.3.2. The active graph has 604 edges across 210 generated units and
  379 residual records; 600 edges resolve to 213 distinct existing official
  tags and four resolve to explicitly untagged local integrations. Twenty-six
  prior exact full-statement equivalences plus 4.2.5 and 4.3.2 make
  twenty-eight. Four bounded mathematical gaps remain open from earlier
  slices; subsection 4.3 adds no Stacks gap. The next cursor is EGA I 4.4.1.

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
- `r184.py`: exact no-overwrite reconstruction of the frozen R184 discovery
  tree from the sealed six-file R215 English successor using hash-guarded inverse
  operations; it never mutates the edition source.
- `files.csv`, `units.csv`, and `intake.json`: generated exact-file inventory,
  stable unit registry, and fail-closed intake receipt.
- `pages.csv`: append-only direct-authority page evidence for frozen discovery
  files whose printed-page markers are absent; raw-page guards make replay
  atomic and preserve every stable unit ID.
- `vqa.csv` and `qa/{a,f,e}`: append-only per-item visual certifications and
  their separate authority, cumulative-French, and cumulative-English crops.
  Rows bind exact public parent-PDF keys, bytes, hashes, one-based physical
  pages, bounded PDF-point boxes, effective scale, comparison mask, and
  complete normalized signature. Historical V rows and crop bytes are never
  overwritten when a later correction supersedes them.
- `map.py`, `cand.csv`, and `map.json`: lexical candidate generation against
  the exact upstream Stacks snapshot. Candidates are not reviewed mappings.
- `tmap.csv`: French-admitted topic-level bridges to existing Stacks sections;
  granularity and non-coverage claims are explicit in every row.
- `smap.csv`: French-admitted statement and statement-component edges to
  exact existing labels or explicitly untagged local labels; published
  corrections append explicit same-table successors instead of rewriting.
- `resid.csv`: noncoverage, partial coverage, terminology migration,
  stronger-target, derived, and upstream-pending residuals with the same
  append-only supersession rule.
- `agent.csv`: exact task IDs, bounded scopes, runtimes when exposed, returned
  findings, owner checks, accepted/rejected dispositions, and write claims.
- `interface.json`: hash-bound read-only contract with the active French and
  English EGA edition task.
- `log.md`: concise operating log, agent/Spark TODOs, and exact outcome
  records.
- `../reports/findings.jsonl`: append-only suspected-correction referrals;
  the edition task alone decides and mutates canonical source.
- `../reports/qsrc.csv` and `../reports/qa`: short flat manifest and immutable
  direct-authority crops for source-error evidence; these are not edition
  outputs or three-surface visual certifications.

### Current reviewed frontier: EGA I 4.5.1--4.5.5

The historical local-immersion subsection through Proposition 4.5.5 is now
admitted from F33 and direct printed pp.126--127. Thirty-three active edges
S000645--S000677 cover all seven statement/proof units; residuals
R000415--R000442 keep the missing modern terminology packages, affine-only
specializations, derived chart arguments, source corrections, and hypothesis
counterexamples explicit. The active statement graph has 673 edges across
229 source units and 439 residuals; physical append-only history has 677 edge
rows and 442 residual rows. Of the active edges, 669 resolve to 220 distinct
official tags and four remain explicit local untagged integrations. Exact
full-statement equivalences remain 29.

Tags 01HK and 01IO split the source-point definition of local immersion;
01HE supplies the local open charts for historical local isomorphisms while
096E remains only its affine ring-map specialization. The global
characterizations in 4.5.3 use 0FCZ only after the homeomorphism or injectivity
hypotheses turn source-local charts into full inverse-image charts; 01IQ gives
the closed-image specialization. Proposition 4.5.4 is a genuinely composite
004V--01RJ--01HK--0FCZ argument and is not strengthened to an open immersion.
Proposition 4.5.5 uses 02V0, 01JR, 01JY, and 01JX; affine tags 096F and 096G
remain partial witnesses and the proof-level two-factor decomposition under
01KU remains explicitly unlabelled.

Printed p.127 contains two already catalogued proof defects. Q000003 confirms
the transitivity citation `4.2.4`, which must read `4.2.5`; Q000004 confirms
that `z` and `z'` are used before being introduced. D000178--D000180,
I000055--I000056, the append-only findings, and individual tight
5,000-dpi-equivalent receipts `455c.png` and `455z.png` preserve diplomatic
print while binding the corrected readings. The subsection has no diagram,
display, equation, or intricate standalone block and therefore creates no V
item; the corpus-wide I000049 visual gate remains open.

The immediate work is sequential statement-level comparison across EGA 0--IV,
continuing in the direct-French body after EGA I 4.5.5 at EGA I 5.1.1. The
latest sealed French interface marker is F37T through EGA II printed p.37;
every reviewed EGA I claim remains bound to its own exact historical receipt.
Discovery unit I.3.2.9 remains in a separate authority-pending queue for its
cited EGA II erratum witness.
The complete English discovery surface drives provisional candidates only.
Mathematical Stacks chapter edits occur only after a bounded unit has direct
French evidence, a reviewed disposition, explicit residual accounting, and
owner verification.
