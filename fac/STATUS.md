# FAC status

- Frozen surface: 661 source targets through printed page 278.
- Stage: sequential source review and statement-level Stacks integration.
- Completed checkpoint: Chapter III, Section 5, no. 77, printed pages 199--273.
- Reviewed source units: 548 through 555 append-only decision rows
  (167 equivalent, 164 stronger, 70 extensions, 101 new-statement decisions,
  44 historical references, 2 outside scope).
- Current Stacks references added: 308 across `topology.tex`, `sheaves.tex`,
  `modules.tex`, `homology.tex`, `coherent.tex`, `cohomology.tex`,
  `divisors.tex`, `constructions.tex`, `schemes.tex`, `morphisms.tex`,
  `derham.tex`, `algebra.tex`, `properties.tex`, `varieties.tex`,
  `simplicial.tex`, `more-algebra.tex`, `dualizing.tex`, `local-cohomology.tex`,
  and `duality.tex`.
- New Stacks theorem/lemma statements: 33, plus the paracompactness and
  locally-constant-sheaf definitions, the graded-conventions remark, and
  the internal graded Ext and degreewise graded dual definitions;
  each new theorem/lemma has a complete proof and no assigned tag.
- Source/proof issues or convention boundaries: 890 found by direct
  authority-page and TeX inspection, all resolved and
  retained in `issues.csv`.
- Source corrections: 4, including the no. 74 repeated resolution index
  restored from printed `L_p` to quantified `L_i` as correction `C0040`
  and the no. 75 conflict between the general and degree-one Koszul signs
  resolved as correction `C0041`.
- Existing Stacks defects corrected: 15, comprising the refinement-homotopy
  sign, repeated coefficient sheaves, wrong boundary domain, wrong boundary
  degree, incomplete low-degree citation, and multiplication by a negative
  power before localization in the Proj shift proof, plus the wrong
  projective-space dimension, reversed vertical exponents, and wrong ambient
  local-ring subscript in the Enriques--Severi--Zariski proof, plus the missing
  closing parenthesis, wrong inverse-prime membership, and false arbitrary
  Veronese tensor isomorphism in the d-uple proof, and the ambient-scheme
  switch, undefined signed-degree notation, and nearby infinitive typo in the
  negative-twist proof.
- Validation: `intake.json`, `check.json`, and `mcheck.json` all PASS.
- Builds: `topology.pdf`, `sheaves.pdf`, `modules.pdf`, `homology.pdf`,
  `coherent.pdf`, `cohomology.pdf`, `divisors.pdf`, `constructions.pdf`,
  `schemes.pdf`, `morphisms.pdf`, `derham.pdf`, `algebra.pdf`,
  `properties.pdf`, `varieties.pdf`, `simplicial.pdf`, `more-algebra.pdf`,
  `dualizing.pdf`, `local-cohomology.pdf`, and `duality.pdf`
  completed; every
  affected statement page passed direct 1100 dpi visual inspection. See
  `qa.json`.
- Historical notes added: 143, preserving the source's operator calculus,
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
  no. 78 on printed page 273.
- Next unit: `fac:III:5:no:78`.
- No statement is mapped by lexical similarity alone.
