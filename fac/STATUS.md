# FAC status

- Frozen surface: 661 source targets through printed page 278.
- Stage: complete source review and statement-level Stacks integration;
  maintenance remains open for later corrections.
- Completed checkpoint: full FAC article, introduction through terminal
  bibliography, printed pages 197--278.
- Reviewed source units: all 661 through 668 append-only decision rows
  (189 equivalent, 179 stronger, 81 extensions, 118 new-statement decisions,
  72 historical references, 3 outside scope, and 19 structural anchors).
- Current distinct active Stacks comparison labels: 356 across `topology.tex`, `sheaves.tex`,
  `modules.tex`, `homology.tex`, `coherent.tex`, `cohomology.tex`,
  `divisors.tex`, `constructions.tex`, `schemes.tex`, `morphisms.tex`,
  `derham.tex`, `algebra.tex`, `properties.tex`, `varieties.tex`,
  `simplicial.tex`, `more-algebra.tex`, `dualizing.tex`, `local-cohomology.tex`,
  `duality.tex`, `spaces-over-fields.tex`, and `curves.tex`.
- New Stacks theorem/lemma statements: 37, plus the paracompactness and
  locally-constant-sheaf definitions, the graded-conventions remark, and
  the internal graded Ext and degreewise graded dual definitions, together
  with the dimension-zero complete-intersection remark;
  each new theorem/lemma has a complete proof and no assigned tag.
- Source/proof issues or convention boundaries: 991 found by direct
  authority-page and TeX inspection, all resolved and
  retained in `issues.csv`.
- Source corrections: 7, including the no. 74 repeated resolution index
  restored from printed `L_p` to quantified `L_i` as correction `C0040`
  and the no. 75 conflict between the general and degree-one Koszul signs
  resolved as correction `C0041`, plus the no. 78 selected-basis degree
  repaired as `C0042` (external edition correction `FAC-FR-C0041`) and its
  repeated sign occurrence recorded separately as `C0043` linked to `C0041`,
  and the omitted French subject in no. 80 restored as `C0044` linked to
  external correction `FAC-FR-C0042`.
- Existing Stacks defects corrected: 27, comprising the refinement-homotopy
  sign, repeated coefficient sheaves, wrong boundary domain, wrong boundary
  degree, incomplete low-degree citation, and multiplication by a negative
  power before localization in the Proj shift proof, plus the wrong
  projective-space dimension, reversed vertical exponents, and wrong ambient
  local-ring subscript in the Enriques--Severi--Zariski proof, plus the missing
  closing parenthesis, wrong inverse-prime membership, and false arbitrary
  Veronese tensor isomorphism in the d-uple proof, and the ambient-scheme
  switch, undefined signed-degree notation, and nearby infinitive typo in the
  negative-twist proof, plus the omitted rank-zero case and wrong derived
  sheaf-Hom base ring in tag `0BQZ`, and the missing word `space` in the
  proper-algebraic-space hypothesis at tag `0DN1`, plus the omitted twist on
  basis sections in tag `08A8` and the invalid negative lower binomial index
  in the reciprocal-module rank preceding tag `01XT`, plus the zero-support
  wording in tag `0AYT`, the missing cokernel identification in tag `08A0`,
  the zero-polynomial wording in tag `08AC`, the grammar in tag `0B52`, the
  missing zero branches in tags `0BEM`/`0DN4` and `0BEN`/`0EDE`, and the false
  zero-support degree bound in tag `0F27`.
- Validation: `intake.json`, `check.json`, and `mcheck.json` all PASS.
- Builds: `topology.pdf`, `sheaves.pdf`, `modules.pdf`, `homology.pdf`,
  `coherent.pdf`, `cohomology.pdf`, `divisors.pdf`, `constructions.pdf`,
  `schemes.pdf`, `morphisms.pdf`, `derham.pdf`, `algebra.pdf`,
  `properties.pdf`, `varieties.pdf`, `simplicial.pdf`, `more-algebra.pdf`,
  `dualizing.pdf`, `local-cohomology.pdf`, `duality.pdf`,
  `spaces-over-fields.pdf`, `curves.pdf`, and `algebraization.pdf`
  completed; every
  affected statement page passed direct 1100 dpi visual inspection. See
  `qa.json`.
- History blocks: 128 present, of which 124 are added relative to upstream
  base `a04446e57ec1fbc252a871afcec7752fb2807b14`, preserving the source's
  operator calculus,
  image-complex construction, two-covering double complex, and unproved
  cofinal-vanishing question, together with the classical closed-point to
  reduced-scheme bridge, the classical-map to scheme-morphism bridge, and the
  classical-product topology and empty-factor boundary, and the precise
  classical-variety to reduced finite-type separated-scheme correspondence,
  the induced-subvariety terminology and reduced-source boundary, and the
  classical fraction-field sheaf to generic-point function-field bridge,
  the classical coherence proof's locally Noetherian scheme bridge, and the
  closed-subvariety extension-by-zero to closed-immersion direct-image bridge,
  the historical sheaf-of-fractional-ideals terminology, the classical
  section-sheaf versus relative-spectrum dual convention, and the precise
  complex Hodge-decomposition boundary behind the classical Betti-number sum,
  together with the classical affine-variety convention, the principal-open
  graph construction, the standard-open basis, the affine-refinement
  corollary, and the exact closed-diagonal role in affine intersections,
  plus the corrected logical order in the printed affine-global-sections
  proof and the two principal-open denominator-clearing arguments,
  and the corrected alternating sign in the explicit affine Cech contraction,
  together with the affine global-generation theorem and the finite-type
  module route to a finite free quotient, while the existing localization and
  affine-equivalence histories now record no. 45's patching and exactness use,
  and the no. 46 histories now distinguish standard-cover Cech vanishing,
  affine sheaf-cohomology vanishing, and kernel-only global-section lifting,
  while no. 47 records the affine-intersection comparison and the historical
  image-complex route to the long exact sequence without claiming false modern
  theorem matches, and no. 48 now records the character-space versus prime-
  spectrum boundary, the sheafification of the tensor construction, the
  fraction proof of localization exactness, and the essential Noetherian
  hypothesis behind coherence of a finite module's associated sheaf; no. 49
  now records the finite-free proof of the affine unit and counit, separates
  affine right-exactness from general global sections, and resolves the
  projective warning into the graded-module quotient by high-degree torsion;
  no. 50 now distinguishes the direct-summand and Hom-exact definitions,
  strengthens the classical closed-point projectivity criterion to the
  all-prime/all-maximal modern formulation, records the locally constant rank
  boundary and relative-spectrum dual convention, and dates the printed
  polynomial-ring question while refusing to invent a Quillen--Suslin tag;
  no. 51 now records the classical scalar-orbit model of projective space,
  identifies its standard affine charts and same-degree fraction sheaf with
  their modern Proj counterparts, and distinguishes closed projective
  subvarieties from intrinsic projective morphisms and closed subschemes;
  no. 52 now separates the finite standard-cover and support-adapted Cech
  arguments from Grothendieck vanishing on Noetherian spaces, records the
  homogeneous-principal-open construction and its precise index bound, and
  distinguishes the classical Veronese proof from direct Proj localization;
  no. 53 now records the cofinal finite-complement covers of an irreducible
  classical curve and the finite-simplex contraction, preserves the fact that
  the source is using direct-limit Cech groups, distinguishes the modern
  derived-functor vanishing theorem from an unproved comparison of theories,
  and closes the empty-index-set defect by the harmless choice of one closed
  point without altering the authority text; no. 54 now identifies the
  transition-function construction of twists with shifted graded modules,
  records the homogeneous-function and tensor descriptions, preserves the
  grading-sign and degree-one-generation boundaries, retains the two printed
  source corrections, and separates the positive-dimensional global-section
  claim from projective zero-space and arbitrary Proj; no. 55 now records the
  affine denominator-clearing lemma, the two-stage chart and overlap
  uniformization, eventual global generation by high twists, and the finite
  twist-quotient corollary, while matching them to localization at an
  invertible section and the modern ample-sheaf characterization; no. 56 now
  fixes the exact graded-module and shift conventions, identifies Serre's
  class-C arrows with the morphisms inverted in the Serre quotient, preserves
  the distinction between a finite high-degree tail and ordinary finite
  generation, and records the homogeneous-basis sign convention. Its visual
  gate also caught and closed the initially empty reader remark before push;
  no. 57 now identifies the same-degree fraction, restriction, stalk, and
  functoriality formulas with the standard-open Proj construction, records
  the printed singleton typo, and corrects the false claim that the raw
  single-denominator assignment on every open is already a sheaf by using
  the existing global-sections counterexample and the proved basis extension;
  no. 58 now records exactness by stalkwise localization, the all-integer
  shift comparison, the high-degree-tail criterion, and the Serre-quotient
  interpretation of relative injectivity and surjectivity. It also corrects
  the printed negative-shift formula by moving negative powers into the
  localization and closes the matching pre-localization defect in the existing
  Stacks proof; no. 59 now identifies the integer-graded twisted-section
  module, its canonical action, and the comparison maps with their modern
  counterparts, while the new complete standard-open proof records both
  triangle identities without promoting them to an unjustified adjunction.
  The source's no. 65 sentence remains a forecast rather than a proof at this
  cursor; no. 60 now records high-tail finiteness and recovery for finite
  sums of twists, the projective zero-space exception to whole-module finite
  generation, and the historical essential-surjectivity proof by a graded
  cokernel presentation. It keeps that chosen representative distinct from
  the later direct twisted-section comparison, and it records correction
  `FAC-FR-C0035` only after direct 5000 dpi-equivalent inspection confirmed
  the two type-inconsistent upper-row roman-L glyphs; no. 61 now records the
  graded, internal-degree-zero positive truncation of the module
  Koszul-to-extended-alternating-Cech colimit, including its subset-product
  transition maps, exact filtered-colimit cohomology, functoriality, and long
  exact sequence. The history explicitly retains the absent augmentation and
  one-degree shift, while the no. 69 Ext sentence remains a forecast. Direct
  5000 dpi-equivalent inspection confirmed the printed terminal `i_i` defect
  before correction `FAC-FR-C0036` was admitted in corrected French and
  English; transcription repair `T0034` remains separately classified;
  no. 62 now matches its finite power-Koszul computation to regularity,
  module-valued extended alternating-Cech vanishing, and projective-space
  cohomology. It records stabilization of the finite systems and repairs four
  membership signs through transcription entry `T0035`. The source's genuine
  projective-zero-space boundary is retained explicitly: when `r = 0`, the
  positive complex has no incoming top differential, Proposition 2(c) and
  Corollary 1 do not apply for nonnegative twists, and the final dimension
  formula must be replaced by rank one in degree zero. Direct 1100 dpi review
  of physical pages 59--61 and all three affected output pages passed; the
  visual gate caught and closed one compound-term hyphenation error before
  admission, with no high-detail crop needed; no. 63 now preserves the
  finite-graded-free-resolution proof of stabilization, finite-dimensionality,
  eventual higher vanishing, and recovery of high graded pieces, while
  distinguishing its algebraic colimit groups from the cover comparison that
  begins only at no. 64. Its modern destinations are tags 0913, 01YS, 0AG7,
  0BXD, 05QB, and 0117; no tag was invented for the source-specific
  finite-stage stabilization or its resolution-dimension convention. The
  corrected projective-zero-space computation from no. 62 is propagated into
  the free base case, and source correction `C0037` restores the missing
  superscript on the upper middle free-module term. Authority physical pages
  61--62 and output pages coherent 34 and 37 and more-algebra 74 passed direct
  1100 dpi inspection after two serial builds, with no high-detail crop needed;
  no. 64 now identifies the internal-degree-zero Koszul colimit with alternating
  cochains on the finite standard Proj cover by its explicit localization
  fractions, including transition compatibility, a uniform denominator
  exponent, and inverse identities at the colimit level. It preserves the
  source's type-TF finite-presentation and cokernel proof while recording that
  tags 0913 and 01M7 give the complex comparison for every graded module.
  The corollary is routed through tags 01FM, 01XD, and 01XB, with the
  alternating-to-usual and affine-intersection acyclicity steps explicit; no
  new theorem or tag was created. Transcription repair `T0036` remains separate
  from source correction. Authority physical pages 62--63 and output pages
  coherent 3, constructions 12, and more-algebra 74 passed direct 1100 dpi
  inspection after two serial builds, with no high-detail crop needed; no. 65
  now completes the promised projective module--sheaf comparison through the
  eventual unit, the sheaf counit, and their exact triangle identity. Tags
  0AG7 and 0BXD supply the modern eventual-recovery and quotient-equivalence
  forms, while tag 01YS gives the stronger Noetherian-base finiteness and
  Serre-vanishing result. Proposition 8 and both displayed basis formulas map
  to tag 01XT, including the reciprocal-monomial generator in twist
  `-r-1`; the projective-zero-space exception discovered at no. 62 is
  propagated rather than lost. Authority physical pages 63--64 and output
  pages coherent 16, 34, 37, and 38 and constructions 20 passed direct
  1100 dpi inspection after two serial builds, with no high-detail crop
  needed; no. 66 now routes closed-subvariety extension by zero, proper
  coherent cohomology, the Noetherian dimension bound, eventual global
  generation and vanishing, projective twists, and very ample line bundles
  to tags 087T, 089W, 02O6, 02UZ, 01Q3, 0B5T, 01MN, and 01VM. It preserves
  the printed conjectural status of the extension from projective to complete
  varieties and the principal-bundle construction as historical lineage,
  without inventing a direct tag for either presentation. Authority physical
  pages 64--65 and output pages coherent 24, 42, and 50, cohomology 39,
  properties 44, constructions 17, and morphisms 86 passed direct 1100 dpi
  inspection after two serial builds, with an exact hard stop before no. 67
  on printed page 260 and no high-detail crop needed; no. 67 now identifies
  the all-integer twisted-section module and its canonical comparison map,
  and adds the exact common-annihilator and compatible-family criterion for
  that map to be injective or bijective. The reusable criterion is a new
  completely proved lemma with no assigned tag; tags 01MT and 0AG7 retain the
  construction and eventual-recovery inputs, while tag 0913 records only the
  finite-stage-to-colimit lineage and is not conflated with the source's
  stage-one notation. Authority physical pages 65--66 and output pages
  constructions 18, 21, and 22, coherent 37, and more-algebra 74 passed
  direct 1100 dpi inspection after two serial builds, with an exact hard stop
  before Section 4 and no. 68 on printed page 261 and no high-detail crop
  needed; no. 68 now distinguishes internal graded Hom and Ext from their
  ordinary ungraded counterparts, preserving the exact nonfinite boundary
  in the source's footnote. Two new completely proved lemmas establish
  graded free resolutions and the full internal Ext package, while a new
  definition records the homogeneous cochain complexes, graded module
  action, shifts, finiteness, polynomial-ring vanishing, and both long exact
  sequences. Tags 00JL, 00LT, 00LU, 065P, 08YR, 065R, and 00OQ remain the
  exact existing inputs and comparison targets; no tag was invented for the
  new labels. Transcription entry `T0039` remains separate from any source
  correction. Authority physical pages 66--67 and algebra output pages
  129--131, 171--172, and 272 passed direct 1100 dpi inspection after two
  serial builds, with an exact hard stop before no. 69 on printed page 262
  and no high-detail crop needed; no. 69 now identifies the positive graded
  Koszul truncation as a free resolution of
  `J_k=(t_0^k,...,t_r^k)` and computes its internal graded Ext. A new
  completely proved equal-degree Koszul-ideal lemma records that reusable
  bridge without an assigned tag. Tags 062F and 0913 retain regularity and
  the finite-Koszul-to-extended-Cech colimit; tags 0954, 0DWR, 01YB, and
  0G2H give the exact local-cohomology, punctured-open, and section forms,
  with the `q+1` shift, low-degree exact sequence, cofinal ideals, and Ext
  variance explicit. The `k=0` contractible stage and source condition-(TF)
  boundary remain recorded rather than normalized away. Transcription entry
  `T0040` remains separate from source correction. Authority physical pages
  67--68 and output pages more-algebra 74--76, dualizing 12,
  local-cohomology 2, coherent 25, and duality 80 passed direct 1100 dpi
  inspection after two direct serial builds, with an exact hard stop before
  no. 70 on printed page 263 and no high-detail crop needed. The aggregate
  Makefile dependency path was rejected after its bounded attempt exposed an
  unrelated marker cascade; direct named-master compilation is now the
  recorded fail-closed build route; no. 70 now defines the degreewise
  direct-sum graded dual, proves exact contravariance and componentwise
  biduality, and records the exact sequence obtained by applying an exact
  contravariant functor to a cohomological delta functor. It distinguishes
  Macaulay's apolar terminology from a categorical inverse system and keeps
  the internal-degree sign in the definition of `T^q`. Direct 5000
  dpi-equivalent inspection confirmed that the printed formula really has
  subscript `S`; the integration records this as an authorial defect and uses
  internal `GrHom_K(M,K)`, since `GrHom_S(S,K)=K` cannot equal the displayed
  degreewise dual of `S`. Tags 010Q, 0117, 01YS, 0913, and 0DWR remain the
  exact existing inputs; the new graded-dual definition and two completely
  proved lemmas remain untagged. Authority physical pages 68--69 and output
  pages algebra 130--132, homology 27--29, local-cohomology 2, more-algebra
  74, and coherent 34 passed direct visual inspection after two direct serial
  builds, with an exact hard stop before no. 71 on printed page 264; no. 71
  now proves the exact functorial top-degree pairing for every graded module:
  internal graded Hom into `S(-r-1)` is the degreewise dual of top positive
  Cech cohomology. The new completely proved lemma retains the source's
  single shifted free summand, arbitrary direct-sum/product, and graded free
  presentation arguments. Lead review made the factorization through the
  image and kernel of the free presentation explicit before the final build.
  The comparison diagram is delivered as native TeX with no assigned tag.
  It keeps the essential `r >= 1` boundary and all
  internal-degree signs. Tag 01XT supplies the reciprocal-monomial basis used
  in the free calculation, while tag 0A9W is recorded only as the stronger
  relative derived comparison sharing the twist `-r-1`; neither is presented
  as identical to the source proposition. Transcription entry `T0042`
  remains separate from source correction, and direct authority review found
  no new authorial defect. Authority physical pages 69--70 and output pages
  more-algebra 76--78, coherent 16--17, and duality 35 passed direct 1100
  dpi-equivalent inspection after two direct serial builds, with an exact hard
  stop before no. 72 on printed page 265 and no high-detail crop needed;
  no. 72 now realizes the source's piecewise functors `E^q` as the
  cohomology of the reversed graded dual augmented Cech complex and proves
  their functorial identification with internal graded Ext for every graded
  module. The single new completely proved lemma retains the exact
  five-term sequence, both exceptional connecting maps, and the native
  `T^1`/`T^0` comparison diagram. It proves free acyclicity for arbitrary
  direct sums, applies tags 010T and 010U on the opposite graded-module
  category, and records the finite degree-zero perfect pairing and the exact
  finite-tail conclusion for `T^0`. The printed theorem omits the exceptional
  degree `r+1`; direct authority review and the immediately following
  definition force its restoration, now recorded as source correction
  `C0039` rather than a silent normalization. Tag 01YS supplies projective
  cohomology finiteness and tag 0FVX remains only the stronger proper-scheme
  comparison. No official tag is assigned to the new theorem. Transcription
  entry `T0043` remains separate. Authority physical pages 70--72 and output
  pages algebra 130, homology 29, coherent 34, duality 70, and more-algebra
  78--80 passed direct 1100 dpi-equivalent inspection after two serial direct
  builds, with an exact hard stop before Section 5 and no. 73 on printed page
  267 and no high-detail crop needed; no. 73 now identifies internal graded
  Hom and Ext after degree-zero homogeneous localization at every point of
  Proj. Two new completely proved untagged lemmas retain the exact fraction
  map, the finite-in-each-degree graded free resolution, both cocycle and
  coboundary exact sequences before and after localization, and the
  degree-one unit that trivializes every localized twist. The associated-
  sheaf Hom isomorphism and local Ext comparison remain separate, with their
  degree-zero compatibility explicit and the second module arbitrary. Tags
  01CP, 01M7, and 087R supply the finite-presentation stalk comparison,
  associated-sheaf stalks and exactness, and ordinary flat-base-change input;
  none replaces the source's degree-zero graded step. Direct authority review
  found no new source correction. Authority physical pages 72--73 and output
  pages algebra 135--137, constructions 13--14, modules 32, and more-algebra
  172 passed direct 1100 dpi-equivalent inspection after two serial builds,
  with an exact hard stop before no. 74 on printed page 268 and no high-detail
  crop needed; no. 74 now characterizes eventual cohomology vanishing under
  increasingly negative twists by local Ext vanishing, and then by a bound
  on stalkwise projective dimension. Three new completely proved untagged
  lemmas retain the internal-degree sign, the exceptional `q=0` five-term
  step, finite-tail detection through the associated sheaf, the local
  trivialization of `O(-r-1)`, every scheme point, the `r`-variable affine
  chart bound, and the exact reversal from `0 <= q < p` to
  `r-p < i <= r`. Tags 01XD, 0AG7, and 0BXD supply standard-cover
  cohomology, finite-tail recovery, and the coherent Proj equivalence; tags
  00O4, 0CXF, 00O8, and 00OQ supply projective dimension, finite free local
  resolutions, localization of global dimension, and the polynomial-ring
  bound. None replaces the three new criteria. Direct authority review
  confirms that the printed phrase “each `L_p`” leaves the displayed
  `L_p,...,L_0` terms unquantified; correction `C0040` restores “each
  `L_i`” and preserves the printed form in provenance. Authority physical
  pages 73--74 and output pages algebra 263--266 and 274--275 and coherent
  38--40 passed direct 1100 dpi-equivalent inspection after two serial
  builds, with an exact hard stop before no. 75 on printed page 269 and no
  high-detail crop needed; no. 75 now derives increasingly negative-twist
  vanishing for finite locally free sheaves on closed subschemes locally
  cut out by a regular sequence of fixed length. One new completely proved
  untagged lemma retains the regular-local quotient, the exterior-basis
  Koszul resolution, the pushed-forward stalk, the exact projective-
  dimension bound, finite pushforward coherence, the projection formula,
  higher-direct-image vanishing, and the Leray comparison back to the
  closed subscheme. Tags 00NR and 00NQ supply the regular local quotient and
  regular sequence; tags 0622, 0623, and 062F supply the Koszul complex and
  its exactness; tag 0E9J supplies the regular-immersion specialization;
  tags 01Y6, 01E8, and 01F4 supply coherent finite pushforward, twisting,
  and cohomology transfer. None replaces the assembled vanishing theorem.
  Direct authority review finds that the printed general differential sign
  `(-1)^j` contradicts the immediately following formula
  `d(e<i>)=f_i` at `q=1`; correction `C0041` uses the standard
  `(-1)^(j+1)` sign, preserves both printed forms, and records the
  degreewise chain isomorphism for the uniformly opposite convention.
  Authority physical pages 74--75 and output pages algebra 255,
  more-algebra 76, divisors 50, and coherent 39--40 passed direct 1100
  dpi-equivalent inspection after two serial builds, with an exact hard stop
  before no. 76 on printed page 270 and no high-detail crop needed; no. 76
  now isolates the exact projective-dimension shift modulo a module
  nonzerodivisor in one completely proved untagged algebra lemma. Its history
  makes the printed lemma's implicit nonzero-module hypothesis explicit.
  Tag 0FD8 supplies the stronger intrinsic vanishing theorem; tags 01WC and
  01PU close properness and ampleness, while tags 0345, 0B18, and 0B19 close
  the depth-two specialization. The classical ambient proof remains
  separately traceable through tags 031T, 00LL, 00OQ, and 00O8, and tag 08YR
  supplies the finite top Ext module required before Nakayama. A bounded
  independent read-only review checked the exact component, authority
  renders, twelve source units, and supporting chapters against base
  `244d41fef29d7df2d2753d3bc816f9d918aa7b41`; it made no edits and used no
  further agents. Lead recheck accepted its hard findings, replaced seven
  earlier decisions append-only, and corrected the source-aligned English
  interpretation from arbitrary primes containing `(f)` to the associated
  primes of the principal quotient. The same review exposed three global
  defects in the pre-existing proof of tag 0FD8: `P^1` instead of `P^n`,
  exponent `m'-m` instead of `m-m'` on both downward arrows, and ambient
  local-ring subscript `x` instead of `y=i(x)`. All three are now repaired and
  documented. Authority physical pages 75--76 and output pages algebra
  270--271 and varieties 109--111 passed direct 1100 dpi-equivalent
  inspection after two final serial builds, with no high-detail crop needed
  and an exact hard stop before no. 77 on printed page 271; no. 77 now proves
  the global top-Ext test for projective dimension, the exact all-integer-twist
  criterion through graded local duality, the high-Veronese projective-
  dimension theorem, and its smooth-projective embedding corollary in four
  completely proved untagged lemmas. The historical first-kind terminology is
  retained without being promoted to a general definition. The high-Veronese
  proof makes `P_d`, `N_d`, the saturated coordinate ideal, algebraically
  closed base, reducedness, connectedness, component dimensions, and the
  positive/zero/negative twist split explicit. Tags 0AG7, 01YS, 0FD7, 0BUG,
  0B5J, and 067U provide the exact existing recovery, positive and negative
  section vanishing, global-functions, Veronese, and regular-immersion inputs;
  the untagged negative-twist criterion supplies the local-to-negative
  direction. No official tag is invented for any assembled statement. A
  bounded independent read-only
  review checked the exact component and the four affected chapters against
  base `2fb2edc6e7bb82c0aeab78342fef45fd3c28ef8a`; it made zero edits, used no
  further agents, and its three concrete findings were independently verified
  and closed by lead review. That review also propagated six global target
  repairs: the d-uple statement parenthesis, inverse-prime membership, false
  tensor isomorphism, the negative-twist proof's ambient-scheme switch and
  signed tensor-power notation, and its nearby infinitive typo. Authority
  physical pages 76--78 and output pages algebra 130 and 265--266, coherent
  38--42, constructions 25--26, and varieties 109--110 passed direct 1100
  dpi-equivalent inspection after two final serial builds. Every native TeX
  diagram is intact, no edited line creates an overfull box or unresolved
  reference, no high-detail crop was needed, and the scope stops exactly before
  no. 78 on printed page 273. No. 78 now gives the heterogeneous graded Koszul
  resolution of a complete-intersection quotient and its full graded Ext
  calculation, followed by the section, intermediate-vanishing, and top-duality
  formulas for positive-dimensional projective complete intersections. Two new
  completely proved untagged lemmas and one untagged dimension-zero remark retain
  every selected degree, graded shift, differential sign, exceptional local-
  duality term, and orientation dependence. Direct authority review confirms two
  printed defects on p. 273: the degree of `e_(i_1...i_q)` omits the selected
  indices, and the one-based sign `(-1)^j` again conflicts with `d(e_i)=P_i`.
  Corrections `C0042` and `C0043` preserve the print, keep external identifier
  `FAC-FR-C0041` in its own namespace, and link the repeated sign intervention to
  global correction `C0041`. The printed all-degree section assertion is false in
  dimension zero: `K[t_0,t_1]/(t_1)` has `A_(-1)=0` while its Proj point has a
  nonzero section of `O(-1)`. The modern theorem therefore requires `p>=1`; the
  following remark supplies the exact dimension-zero sequence and separately
  retains part (c) through the intrinsic dualizing module and tag `0FVZ`. Three
  bounded independent read-only audits checked the exact component, target gaps,
  signs, shifts, source boundary, and zero-dimensional case against committed base
  `4496ca9b56f104e360143b804020b373f020888c`; all made zero edits and spawned no
  downstream agents. Lead recheck reproduced every accepted finding and also
  repaired two pre-existing defects in tag `0BQZ`: rank zero is now admitted for
  the identity immersion, and the final derived sheaf Hom is correctly taken over
  `O_Y`. Authority physical pp. 78--79 and output pages More on Algebra 76--77,
  Coherent 42--43, and Duality 37--38 passed direct 1100 dpi-equivalent inspection
  after two final serial builds. All edited references resolve, no edited line
  creates an overfull box, and only inherited end-matter phantom hyperlinks remain
  undefined. The scope stops exactly before Section 6/no. 79 on printed p. 274.
  The previously unsupported status count of 143 history notes was also reconciled
  to 106 added history blocks and 110 total, with the correction retained as
  issue `I000916`; no. 79 now defines the Euler--Poincare characteristic and
  closes both additivity propositions. Tags `0BEJ` and `08AA` already supply
  the proper-scheme definition and the module-linear short-exact formula, but
  direct authority review exposed a deliberate stronger arrow class in
  Proposition 1: its homomorphisms are only linear over the ground field,
  whereas no. 38 reserves “algebraic homomorphism” for module-linear maps and
  Proposition 2 returns to that narrower hypothesis. One new completely proved
  untagged lemma therefore retains the exact ground-field-linear statement by
  using tag `03FD` to pass to underlying abelian-sheaf cohomology. Proposition 2
  remains the exact finite-sequence consequence of tag `08AA` and coherent
  kernels from tag `01Y0`; no redundant theorem or official tag was created.
  Three bounded read-only audits checked the 12 source units, both authority
  pages, the arrow-class boundary, signs, finite truncation, target surface,
  and exact stop against committed base
  `f535adfc9001b4782eb5acffa3c046236ea1bc52`; all made zero edits and spawned
  zero downstream agents. Lead review reproduced the strictness witness and
  closed every accepted finding. The duplicate target audit also exposed and
  repaired the pre-existing missing word `space` in tag `0DN1`. Authority
  physical pp. 79--80 and output pages Varieties 61--62 and Algebraic Spaces
  over Fields 28 passed direct 1100 dpi-equivalent inspection after two final
  serial builds. Every edited reference resolves, no edited line creates an
  overfull box, and the scope stops exactly after Proposition 2 on printed
  p. 275, before no. 80. No tensor-product statement was attributed to this
  checkpoint. The cumulative provenance surface is now 109 added history
  blocks and 113 total. No. 80 now closes the Hilbert-polynomial,
  characteristic-function, and arithmetic-genus comparison. Tag `08AC`
  states the exact degree-at-most-ambient-dimension bound, while tag `0BEM`
  remains explicitly stronger by support dimension. The finite graded
  resolution is retained as historical proof machinery through the branch
  graded-resolution lemma and tag `00OQ`, without pretending that one target
  statement packages both finiteness properties. Tags `0AG7`, `01YS`, and
  `08AE` preserve the finite-tail and eventual-recovery boundary: for
  `M=K=S/S_+`, the eventual polynomial is zero although the degree-zero
  Hilbert function is one, so the all-integer identity is polynomial identity
  rather than low-degree recovery. Tag `01XT` gives
  `chi(O(n))=binom(n+r,r)` with the generalized-binomial convention for every
  integer, including negative twists and `r=0`. The new untagged arithmetic-
  genus remark identifies only the value at zero with `chi(V,O_V)` through
  the closed-immersion pushforward and tag `089W`; it warns that the remaining
  Hilbert polynomial depends on the embedding and keeps FAC's adopted
  `chi(V,O_V)` convention separate from classical `p_a`. External correction
  `FAC-FR-C0042` is recorded locally as `C0044` and restores only the omitted
  French subject. Three bounded read-only audits checked all 16 units against
  committed base `539c415ce13e7532b4c8c12a90f3576529da457c`; all made zero
  edits and spawned zero downstream agents. Lead review reproduced every
  accepted finding and repaired two pre-existing target defects: the missing
  `F(m)` twist in tag `08A8` and the reciprocal-module rank preceding tag
  `01XT`. Authority physical pp. 80--81 and output pages Varieties 67--68,
  Coherent 16, and Algebraic Curves 23 passed direct 1100 dpi-equivalent
  inspection after two final serial builds. Every introduced reference
  resolves, no edited line creates an overfull box, both validators report
  PASS with empty error arrays, and the scope stops exactly before no. 81 on
  printed p. 276. The cumulative provenance surface is now 115 added history
  blocks and 119 total. No. 81 now closes the body of FAC with the exact
  support-dimension degree theorem. Tags `01AT` and `01BA` give the stalkwise
  support definition and closedness, while tags `00L4`, `00L7`, and `01YF`
  replace the source's homogeneous primary-decomposition machinery by prime
  filtrations and coherent devissage. The irrelevant homogeneous prime is
  retained as an affine module possibility and excluded only after passing to
  projective degree-zero localizations. Tags `08A0` and `0EGK` preserve the
  regular-hyperplane sequence and first-difference proof, with all associated
  primes rather than only minimal components and with the quotient written as
  `i_*i^*F` on the ambient projective space. A new completely proved untagged
  lemma states that the Hilbert polynomial of a nonzero coherent sheaf has
  degree exactly the dimension of its support; the zero sheaf is stated
  separately. Its generic-length and ample-positivity proof works over every
  field and avoids silently importing the source's infinite-field hyperplane
  choice into finite fields. Tag `0BEM` remains only an upper bound for
  arbitrary invertible twists, since the trivial twist on a positive-
  dimensional proper scheme is a counterexample to equality. Three bounded
  read-only audits checked all 16 units, both authority pages, the exact target
  gap, embedded-prime and finite-field counterexamples, zero conventions, and
  the hard stop against committed base
  `b3f7e318fc2a9bf268a54d5bf96eb48cf28cc2a8`; all made zero edits and spawned
  zero downstream agents. Lead review reproduced every accepted finding and
  propagated seven directly exposed target repairs: tags `0AYT`, `08A0`,
  `08AC`, and `0B52`, the scheme/algebraic-space pairs `0BEM`/`0DN4` and
  `0BEN`/`0EDE`, and formal-triple tag `0F27`. Authority physical pp. 81--82
  and fourteen output pages across Modules, Algebra, Varieties, Algebraic
  Spaces over Fields, and Algebraic and Formal Geometry passed direct 1100
  dpi-equivalent inspection after repeated serial builds. Every introduced
  reference resolves, no edited line creates an overfull box, both validators
  report PASS with empty errors, and the scope stops exactly after Remark 2 on
  printed p. 277, before Paris and the bibliography. No new printed-source
  correction was needed; external `FAC-FR-T0044` remains only transcription
  provenance. The cumulative provenance surface is now 124 added history
  blocks and 128 total.
- The terminal end-matter and global residual audit close the frozen corpus.
  Component `080_paris_and_bibliography.tex` is 3,164 bytes, SHA-256
  `B8DC16C1FCB919118372646FD0A702DA1EB30521567F43198979CEC8DF430F89`;
  it covers physical pp. 82--83 / printed pp. 277--278 through article EOF.
  The frozen `fac:bibliography` locator begins at the heading on component
  line 10; the adjacent `Paris` signature on line 7 is recorded as exact
  terminal paratext outside the 661-unit inventory, not silently folded into
  the bibliography unit.
  Direct 1100 dpi-equivalent renders have SHA-256
  `1B7102B52AD87C8CF831E73FB1F0F23BBDB6E213AD96D12B1FD8C9A42ECFA98F`
  and
  `D33DF4DBF368BEA1A342F5BE8D2CA21015C4CE8E6B4B91BBCEC27C26D891AE71`.
  Physical pp. 2--3 were also replayed at the same scale, with hashes
  `74A481462D0757BC3D98546B668A5182D2E957D0E20C512F9E41928D9D094EAE`
  and
  `E540905B5A72A2E60C752D465D0D932CA18BD7D042A3EB1D72FE6B9663065595`,
  closing the introduction-to-body seam. All 19 bibliography entries occur
  in the article, for 92 in-text uses; only items 6, 7, and 14 have exact
  local `my.bib` identities, and sixteen same-author or nearby records were
  deliberately not substituted. Two optional footnote numbers, `[3]` and
  `[4]` in component 039, are excluded from those counts; the predecessor
  reader reference graph had falsely classified them as external citations.
  That graph has 1,376 structurally adjudicated residuals but 983 still marked
  `rule_classified_pending_lead_residual_replay`; its zero-open-residual count
  proves partition closure, not full lead semantic review. This limitation is
  retained separately and is not used to certify the direct FAC-to-Stacks
  unit map. All 661 predecessor target rows and 596 edge rows also retain
  stale `source_declared_pending_final_pdf_replay` status despite the
  aggregate three-pass PDF receipt, so row-level compiled status is not
  claimed. The final residual sweep separates 18 true
  hierarchy anchors from 17 embedded mathematical, proof, diagram, and
  terminology units. It maps the latter explicitly and rejects the
  terminology footnote's false Ext candidates. A 21-row append-only
  `corr.csv` overlay corrects the generated parents of that footnote, the
  affine finite-presentation diagram, and all nineteen bibliography entries
  while preserving the byte-identical frozen `units.csv`; the generator
  validates contiguous IDs, sequential and distinct old/new values, new
  parents, action and supersession chains, one active terminal per corrected
  field, completeness, privacy, and parent cycles. Corrections apply to a
  working copy and generated CSVs are promoted only after a full PASS, so a
  rejected ledger preserves both the input graph and last known-good outputs.
  A short three-target recovery journal binds `map.csv`, `ucand.csv`, and
  `mcheck.json`; interruption either proves the full new hash set or restores
  all prior bytes from verified backups before the next validation run.
  If the journal itself is lost while recovery artifacts remain, cleanup is
  allowed only when the current receipt independently matches both generated
  CSV hashes; mixed, stale, invalid, or missing receipts fail closed and keep
  every target and recovery artifact byte for inspection or restoration.
  Fault injection at all three promotion positions and restart replay after
  zero, one, two, and three completed promotions passed without a split state.
  Three bounded
  read-only audits used committed HEAD
  `33513352b39f4dbb984f5138846bf526a25cd5ee`, tree
  `6f8a1d2b54c7b5e0ca62fbc5089c593196d9e259`, made zero edits, and spawned
  zero downstream agents; lead review reproduced every accepted finding.
  Both validators report PASS with empty errors: 661 decided units, 668
  append-only decisions, zero review or candidate units, zero inherited
  defaults, and zero active issues. No Stacks TeX or `my.bib` file changes at
  this terminal checkpoint, so the previously admitted serial builds remain
  the exact mathematical-output gate.
- FAC is complete at printed page 278. The next corpus in the durable goal is
  Tohoku; FAC remains open only for append-only maintenance corrections.
- No statement is mapped by lexical similarity alone.
