# FAC status

- Frozen surface: 661 source targets through printed page 278.
- Stage: sequential source review and statement-level Stacks integration.
- Completed checkpoint: Chapter III, Section 3, no. 61, printed pages 199--254.
- Reviewed decisions: 335 (103 equivalent, 131 stronger, 46 extensions,
  20 new-statement decisions, 33 historical references, 2 outside scope).
- Current Stacks references added: 227 across `topology.tex`, `sheaves.tex`,
  `modules.tex`, `homology.tex`, `coherent.tex`, `cohomology.tex`,
  `divisors.tex`, `constructions.tex`, `schemes.tex`, `morphisms.tex`,
  `derham.tex`, `algebra.tex`, `properties.tex`, `varieties.tex`,
  `simplicial.tex`, and `more-algebra.tex`.
- New Stacks theorem/lemma statements: 14, plus the paracompactness and
  locally-constant-sheaf definitions and the graded-conventions remark;
  each new theorem/lemma has a complete proof and no assigned tag.
- Source/proof issues or convention boundaries: 471 found by direct
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
- Historical notes added: 66, preserving the source's operator calculus,
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
  English; transcription repair `T0034` remains separately classified.
- Next unit: `fac:III:3:no:62`.
- No statement is mapped by lexical similarity alone.
