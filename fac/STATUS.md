# FAC status

- Frozen surface: 661 source targets through printed page 278.
- Stage: sequential source review and statement-level Stacks integration.
- Completed checkpoint: Chapter III, Section 4, no. 68, printed pages 199--262.
- Reviewed decisions: 413 (128 equivalent, 155 stronger, 56 extensions,
  32 new-statement decisions, 40 historical references, 2 outside scope).
- Current Stacks references added: 261 across `topology.tex`, `sheaves.tex`,
  `modules.tex`, `homology.tex`, `coherent.tex`, `cohomology.tex`,
  `divisors.tex`, `constructions.tex`, `schemes.tex`, `morphisms.tex`,
  `derham.tex`, `algebra.tex`, `properties.tex`, `varieties.tex`,
  `simplicial.tex`, and `more-algebra.tex`.
- New Stacks theorem/lemma statements: 17, plus the paracompactness and
  locally-constant-sheaf definitions, the graded-conventions remark, and
  the internal graded Ext definition;
  each new theorem/lemma has a complete proof and no assigned tag.
- Source/proof issues or convention boundaries: 676 found by direct
  authority-page and TeX inspection, all resolved and
  retained in `issues.csv`.
- Existing Stacks defects corrected: 6, comprising the refinement-homotopy
  sign, repeated coefficient sheaves, wrong boundary domain, wrong boundary
  degree, incomplete low-degree citation, and multiplication by a negative
  power before localization in the Proj shift proof.
- Validation: `intake.json`, `check.json`, and `mcheck.json` all PASS.
- Builds: `topology.pdf`, `sheaves.pdf`, `modules.pdf`, `homology.pdf`,
  `coherent.pdf`, `cohomology.pdf`, `divisors.pdf`, `constructions.pdf`,
  `schemes.pdf`, `morphisms.pdf`, `derham.pdf`, `algebra.pdf`,
  `properties.pdf`, `varieties.pdf`, `simplicial.pdf`, and
  `more-algebra.pdf`
  completed; every
  affected statement page passed direct 1100 dpi visual inspection. See
  `qa.json`.
- Historical notes added: 100, preserving the source's operator calculus,
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
  and no high-detail crop needed.
- Next unit: `fac:III:4:no:69`.
- No statement is mapped by lexical similarity alone.
