# Status

Snapshot: Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`.

The reproducible intake, topic crosswalk, and statement-level review are
complete for the bounded FGA corpus.  Every review unit has an append-only
decision and source problems remain explicit.  Forty-one mathematical
source patches are implemented and validated; further source integration
remains in progress.

- 119 Stacks TeX files indexed
- 21,537 labelled TeX objects indexed
- 21,437 objects joined to an existing official tag
- 55 FGA topics reviewed: 30 direct and 14 broad coverage decisions plus 6
  partial and 5 no-direct decisions
- 1,253 FGA units ingested with no omissions or duplicate IDs
- 952 structural or embedded units classified
- 9 item-level correction or historical units preserved
- 301 non-structural mathematical, expository, correction, or historical
  units identified for review
- all 301 review units now have append-only decisions: all 37 Expose 149 units
  including its erratum all 69 Expose 182 units including its erratum all 39
  Expose 190 units including its erratum all 21 Expose 195 units including its
  erratum all 23 Expose 212 units including its erratum all 33 Expose 221
  units including its erratum all 33 Expose 232 units including its erratum all
  43 Expose 236 units including its erratum and all 3 Commentaires units
- Expose 149 currently yields 20 `existing_stronger` decisions 12
  `existing_equivalent` decisions 1 `existing_weaker` decision 0
  `extend_existing` decisions 1 `new_statement` decision and 3 historical
  decisions
- Expose 182 yields 30 `existing_stronger` decisions 30
  `existing_equivalent` decisions 5 `existing_weaker` decisions 0
  `extend_existing` decisions 0 `new_statement` decisions and 4 historical
  decisions
- Expose 190 yields 19 `existing_equivalent` decisions 10
  `existing_stronger` decisions 2 `existing_weaker` decisions 2
  `extend_existing` decisions 1 `new_statement` decision and 5 historical
  decisions
- Expose 195 yields 5 `existing_equivalent` decisions 6 `existing_stronger`
  decisions 4 `existing_weaker` decisions 3 `extend_existing` decisions 2
  `new_statement` decisions and 1 historical decision
- Expose 212 yields 8 `existing_equivalent` decisions 2 `existing_stronger`
  decisions 1 `existing_weaker` decision 7 `extend_existing` decisions 2
  `new_statement` decisions and 3 historical decisions
- Expose 221 yields 4 `existing_equivalent` decisions 1 `existing_stronger`
  decision 5 `existing_weaker` decisions 6 `extend_existing` decisions 13
  `new_statement` decisions and 4 historical decisions
- Expose 232 yields 2 `existing_equivalent` decisions 7 `existing_weaker`
  decisions 11 `extend_existing` decisions 5 `new_statement` decisions and 8
  historical decisions
- Expose 236 yields 4 `existing_equivalent` decisions 2 `existing_stronger`
  decisions 7 `existing_weaker` decisions 11 `extend_existing` decisions 9
  `new_statement` decisions 4 `new_section` decisions 1 example-or-remark
  decision and 5 historical decisions
- the 3 Commentaires units are preserved as historical editorial provenance
- no unit remains in `needs_review`; no correction or comment root remains
  unreviewed

Sections remain independent review units.  A provisional rule that treated
every section as a structural container was rejected before publication
because FGA sections contain substantial unboxed mathematics such as the
composition law in Ext.  Equations subitems and diagrams inherit the decision
of their semantic parent.

Eight source issues are recorded in `issues.csv`; six remain active.
Expose 149 Proposition 2 is resolved by a narrowed hypothesis.  The direct
scan states the all-degree stalk comparison from one finite presentation and
its linked erratum does not alter the claim.  A finite presentation supplies
the degree-zero comparison; degree $q$ requires a finite free partial
resolution through degree $q+1$, while pseudo-coherence supplies all degrees.
This covers the intended coherent case on a Noetherian scheme without
importing the unrestricted historical wording.  The confirmed issue in
Expose 182 Corollary 6 is that
the stated invariance under algebraically closed base-field extension needs
properness in arbitrary characteristic; an Artin--Schreier cover of the affine
line supplies a characteristic-p counterexample to the unrestricted claim.
Expose 182 Proposition 2 omits a necessary rank-at-least-two hypothesis:
for a line bundle $E$ the projective bundle $\mathbf P(E)$ is the base and
$\mathcal O(1)$ is pulled back from $E$, so the claimed integer is not unique.
The projective-bundle Picard and automorphism results are integrated only in
the corrected rank range and `I000008` retains the literal counterexample.
Expose 190 Theorem 3 also remains open at its arbitrary non-Noetherian scope:
the direct current Stacks results require a finite locally free cover whereas
the historical statement assumes finite flat or radicial fpqc descent without
a finite-presentation hypothesis.  Expose 195 Proposition 2.1 has a confirmed
cohomological-degree error: infinitesimal lifts of a fixed morphism form a
torsor under global derivations in degree zero while degree one contains the
obstruction.  The affine-line map from a point is an immediate counterexample
to the printed tangent formula.  Expose 212's projective-linear-group quotient
conjecture is also confirmed false by its linked erratum: current Stacks gives
an algebraic-space torsor quotient for a free flat action but neither scheme
representability nor the asserted descended pre-ample polarization.  Expose
232 Remark 5.2 is likewise fail-closed: its linked erratum retracts the
scheme-level Picard existence conjecture while current Stacks proves only
algebraic-space representability under the universal constant-functions
hypothesis.

Expose 236 Remark on catalog page 223 contains a confirmed notation reversal:
the displayed definitions make `sigma` prime-to-characteristic and `rho`
primary while the following parenthetical prose assigns those descriptions in
the opposite order.  The integration follows the displayed definitions and
their intersection and product identities; `I000007` preserves the direct
NUMDAM authority hash and prevents the reversed prose from being imported
silently.

The broad later conjecture that finite maps should always give effective
descent for flat modules was disproved by Venken.  This does not by itself
refute Expose 195 Theorem 2 because that theorem adds an Artinian maximal-ideal
condition and an Amitsur equalizer condition.  The current Stacks chapter gives
the exact general criterion of universal injectivity but does not prove that
the historical hypotheses imply it or otherwise recover the flat-module-only
claim.  The unit therefore remains an explicit extension target rather than
being silently identified with fpqc descent.

Both `check.json` and `mcheck.json` report `PASS` with empty `errors` arrays.
The warnings preserve nine generated book-part labels and fifty-two current
TeX labels that have no entry in upstream's `tags/tags`; forty-three of these
are the new source labels below.  No replacement tag has been invented.

The first source patch adds
`more-morphisms-lemma-pic-roots-first-order-thickening`, a cartesian
root-lifting square for Picard groups, and
`moduli-lemma-pic-functor-multiplication-etale`, the resulting prime-to-$n$
etaleness theorem for the current Picard algebraic space when $X$ is a scheme.
Decision `D000304` append-only supersedes the earlier gap classification
`D000278`; the narrower current section hypotheses remain explicit.  Both
affected chapters compile to DVI and PDF without TeX errors, and the inserted
diagram and theorem page passed rendered inspection.  The next cursor is the
relative group-locus package in Expose 236.  The second source patch adds
`groupoids-lemma-smooth-flat-locus-group-scheme`, which makes the smooth or
flat locus an open subgroup over the identity-locus open and proves that it
contains every section, and
`groupoids-lemma-smooth-flat-along-identity-component`, which propagates the
property to every section and fibrewise identity component.  Decisions
`D000305` and `D000306` supersede the earlier ingredient-only records.  The
Groupoid Schemes chapter compiles to PDF without TeX errors and the complete
inserted page passed rendered inspection.  The next cursor remains the other
relative group-locus results in Expose 236.  The third source patch adds
`bootstrap-lemma-component-group-scheme-over-field`, which represents the
etale component quotient as a commutative group scheme and an fppf torsor,
`bootstrap-lemma-torsion-component-subgroups`, which constructs its torsion,
prime-to-characteristic, and primary open-and-closed subgroups, and
`bootstrap-remark-component-group-picard-scheme`, which records the Picard
terminology and the reduced-identity quotient without claiming an unproved
specialization theorem.  Decision `D000307` supersedes the earlier gap record
but deliberately retains `existing_weaker` for the historical perfect-or-
proper criterion and specialization claim.  The Bootstrap chapter compiles to
PDF without TeX errors and both inserted pages passed rendered inspection.
The fourth source patch adds
`more-morphisms-lemma-torsion-component-locus-open`, which makes the
fibrewise torsion-component locus a base-change-compatible open subgroup, and
`more-morphisms-lemma-order-in-component-group-constructible`, which proves
local finite-image constructibility of the component-order function and the
equal-characteristic sigma and rho loci.  Decisions `D000308` and `D000309`
replace the former gap records while retaining the unproved properness and
universal-openness clauses as residuals.  The More on Morphisms chapter
compiles to PDF without TeX errors and the two inserted pages and transition
passed rendered inspection.
The fifth source patch adds
`more-morphisms-lemma-connected-along-section-proper`, which proves that the
component selected by a section is closed in a proper family, and
`more-morphisms-lemma-proper-connected-component-neighbourhood`, which spreads
a single proper fibre component over a Zariski neighbourhood using the
existing henselian splitting theorem and fpqc descent.  Decision `D000310`
upgrades FGA 236, Lemma 1.3 to direct equivalent coverage and `D000311`
propagates the result into Theorem 1.1 without erasing its remaining clauses.
Both affected page ranges in More on Morphisms passed compilation and rendered
inspection.
The sixth source patch adds
`more-morphisms-lemma-characteristic-zero-component-loci`, which records the
characteristic-zero identifications of the torsion-component subgroups and,
under separatedness and properness of the fibrewise identity components,
proves that the identity-component locus is closed and proper with its reduced
structure and that the torsion locus is open and closed.  Decision `D000312`
supersedes the former extension classification while retaining
`existing_weaker`, since the historical universal-openness and
reduced-base-smoothness assertions remain unproved.  The More on Morphisms
chapter passed two PDF builds and the complete inserted lemma and transition
passed rendered inspection.
The seventh source patch adds the ordinary nerve of a category and proves that
the nerve functor is fully faithful with essential image characterized by the
Segal bijections.  It also proves that a category is a groupoid exactly when
its nerve is a Kan complex and records the finite-limit internal category and
groupoid versions.  Decisions `D000313` and `D000314` replace the two former
gap records for FGA 212, Proposition 4.1 and Corollary 4.2 with direct modern
equivalents.  The Simplicial Methods chapter passed two PDF builds and all
four affected pages passed rendered inspection.
The eighth source patch proves the Picard decomposition of a projective bundle
over a connected base and the exact scalar-linear-projective-twisting sequence
for its automorphism group.  It also proves that every twisting class is
annihilated by the rank.  Decisions `D000315` and `D000316` replace the two
former gaps with integrated results under the necessary rank-at-least-two
hypothesis recorded in `I000008`.  Both inserted More on Morphisms pages passed
two PDF builds and rendered inspection.
The ninth source patch adds
`derham-lemma-H1-tangent-projective-space`, deriving the vanishing of the
first cohomology of the tangent sheaf from the Euler sequence, and
`defos-lemma-projective-space-rigid-complete-local`, which uses that vanishing
to construct compatible infinitesimal isomorphisms and then algebraizes them.
Decision `D000317` replaces the former ingredient-only record for FGA 182,
Corollary 2 on catalog page 206 with a direct modern equivalent, including
the dimension-zero case.  Both affected chapters passed two PDF builds and
the complete inserted pages passed rendered inspection.
The tenth source patch adds
`defos-lemma-projective-lift-complete-local`, which combines cotangent-complex
obstructions, the Picard exact sequence for first-order thickenings, and
Grothendieck algebraization to lift a smooth projective scheme when the second
cohomology of its structure and tangent sheaves vanishes.  It also adds
`defos-lemma-smooth-proper-curve-lift-complete-local`, using dimension-one
projectivity and cohomological vanishing.  Decisions `D000318` and `D000319`
replace the two former ingredient-only records for FGA 182, Corollaries 3 and
4 on catalog page 206 with direct modern equivalents.  The Deformation Theory
chapter passed two PDF builds and both complete inserted statements passed
rendered inspection.
The eleventh source patch adds
`coherent-lemma-algebraize-flat-formal-scheme-H2`, which algebraizes a flat
formal system over a complete Noetherian local ring when its special fibre is
projective and has vanishing second structure-sheaf cohomology.  The proof
lifts an ample invertible sheaf through every first-order thickening, applies
Grothendieck algebraization, and verifies flatness of the algebraized scheme.
Decision `D000320` replaces the former ingredient-only record for FGA 182,
Theorem 4 on catalog pages 198--199 with a direct modern equivalent.  The
Deformation Theory lifting criterion now reuses this theorem.  Both affected
chapters passed two PDF builds and the complete changed pages passed rendered
inspection.
The twelfth source patch adds
`pione-lemma-pi1-surjective-pushforward-structure-sheaf`, which proves that a
quasi-compact and quasi-separated morphism of connected schemes inducing an
isomorphism on the pushforward of the structure sheaf induces a surjection on
fundamental groups.  Flat base change shows that connected finite etale covers
of the base remain connected after pullback, so the result strengthens the
proper-morphism criterion in FGA 182, Lemma 4 on catalog page 212.  Decision
`D000321` supersedes its former ingredient-only record.  The Fundamental
Groups chapter passed two PDF builds and the complete inserted statement and
proof passed rendered inspection.  The next cursor is the sharper local
finite-etale descent package later in the same section.
The thirteenth source patch adds
`pione-lemma-fundamental-group-product-one-proper`.  For geometrically
connected finite-type schemes over a field, one of which is proper, it
identifies the fundamental group of the product with the fibre product of the
two fundamental groups over the absolute Galois group.  Over an algebraically
closed field this is the direct-product isomorphism in FGA 182, Corollary 5 on
catalog page 215, including the properness condition restored by the 1962
erratum.  Decision `D000322` records the remaining historical generality for
connected but not geometrically connected factors rather than silently
claiming it.  The Fundamental Groups chapter passed two PDF builds and both
affected pages, including the exact-sequence diagram, passed rendered
inspection.  The next cursor returns to the local finite-etale descent
package.
The fourteenth source patch adds
`pione-lemma-finite-etale-descends-if-trivial-on-fibre`.  Under the modern
flat proper finite-presentation hypotheses with geometrically connected and
reduced fibres, a finite-etale cover descends uniquely from the base exactly
when its restriction to one geometric fibre is trivial.  The proof makes the
Galois-category content of the homotopy exact sequence reusable.  Decision
`D000323` replaces the former ingredient-only record for FGA 182, Corollary 1
on catalog page 214 while retaining `existing_weaker` for the historical
criterion under only properness and the structure-sheaf pushforward identity.
The Fundamental Groups chapter passed two PDF builds and the complete lemma
page passed rendered inspection.  The next cursor is the broader local
finite-etale descent theorem from which the historical generality follows.
The fifteenth source patch, in its initially published form, adds
`pione-lemma-local-Stein-trivial-component`, a modern form of FGA 182,
Theorem 11 on catalog pages 213--214.  For a proper morphism whose
structure-sheaf pushforward is the base structure sheaf, it proves that a
geometrically trivial connected component of a finite cover, unramified along
that component, spreads through Stein factorization to an unramified
neighbourhood over which the cover is pulled back from the base.  The proof
uses the finite-map isomorphism locus, properness, and relative differentials.
Decision `D000324` replaces the former gap record with a
direct modern equivalent.  The Fundamental Groups chapter passed two PDF
builds and both the full statement and proof pages passed rendered inspection.
The next cursor is the global finite-etale descent corollary under the
historical properness and structure-sheaf pushforward hypotheses.
The sixteenth source patch adds
`pione-lemma-finite-unramified-etale-after-pullback` and
`pione-lemma-finite-etale-descends-trivial-all-fibres`.  The first proves that
a finite unramified morphism becomes etale when its pullback does along a
proper morphism whose structure-sheaf pushforward is the base structure
sheaf.  The second uses this descent step and the local Stein theorem to prove
the exact FGA 182, Corollary 1 criterion on catalog page 214: a finite-etale
cover descends uniquely from the base exactly when it is geometrically trivial
on every fibre.  Decision `D000325` supersedes the narrower modern-hypothesis
record `D000323` with direct equivalent coverage.  The Fundamental Groups
chapter passed two PDF builds and both inserted lemmas and their proofs passed
rendered inspection.  The next cursor is the function-field consequence of
the local Stein theorem.
The seventeenth source patch is an append-only semantic correction to the
fifteenth and sixteenth patches.  FGA explicitly defines an ``unramified
covering'' as finite locally free with separable fibres, which is modern finite
etale; the immediately following function-field corollary also requires the
resulting generic extension to be separable.  The corrected
`pione-lemma-local-Stein-trivial-component` therefore assumes that the finite
map is etale along the selected component and produces an etale Stein
neighbourhood.  The pointwise form of
`pione-lemma-finite-unramified-etale-after-pullback` supplies the flatness
descent step.  Decisions `D000326` and `D000327` supersede `D000324` and
`D000325` without erasing the earlier interpretation.  The Fundamental Groups
chapter again passed two PDF builds, and all three corrected pages passed
rendered inspection.  The next cursor remains the function-field consequence
of the local Stein theorem.
The eighteenth source patch adds
`pione-lemma-function-fields-local-Stein-trivial-component`, the exact
function-field consequence in FGA 182, Corollary 2 on catalog page 214.  The
function field of the integral Stein factor is finite separable over the base
field because its generic point lies in the etale neighbourhood.  The generic
fibre-product isomorphism makes its tensor product with the function field of
the total space a field, proving linear disjointness and identifying the
compositum with the function field of the finite cover.  Decision `D000328`
supersedes the former gap record `D000087` with direct equivalent coverage.
The Fundamental Groups chapter passed two PDF builds and the complete lemma
and proof passed rendered inspection.  The next cursor is the fibrewise
function-field criterion later in the same FGA section.
The nineteenth source patch adds
`examples-defos-lemma-proper-smooth-formal-moduli-unobstructed`, the formal
moduli theorem of FGA 182, Theorem 10 on catalog page 209.  Vanishing of
zeroth tangent-sheaf cohomology removes infinitesimal automorphisms and makes
the deformation functor prorepresentable; vanishing of second cohomology
kills every cotangent obstruction across small extensions.  Smoothness of the
represented functor then identifies the universal ring with a formal
power-series ring whose number of variables is the dimension of first
tangent-sheaf cohomology.  Decision `D000329` supersedes gap record `D000076`
with direct equivalent coverage.  The Deformation Problems chapter passed two
PDF builds and the complete statement and proof page passed rendered
inspection.  The next cursor is the finite-generation theorem for fundamental
groups of smooth proper varieties.
The twentieth source patch adds
`pione-lemma-fundamental-group-smooth-proper-curve-generators` and
`pione-proposition-fundamental-group-smooth-projective-finitely-generated`.
The curve lemma proves the exact FGA surface-group quotient statement in
arbitrary characteristic: Riemann existence gives the characteristic-zero
presentation while a Cohen-ring lift and surjective specialization supply the
same generators and relation in positive characteristic.  Successive smooth
irreducible hyperplane sections and Lefschetz full faithfulness then give a
surjection from a curve fundamental group to that of every connected smooth
projective scheme.  Decisions `D000330` and `D000331` supersede gap records
`D000097` and `D000098` with direct equivalent coverage.  The Fundamental
Groups chapter passed two PDF builds and both complete statements and proofs
on catalog pages 217--218 passed rendered inspection.  The next cursor is the
tame-specialization package later in the same FGA section.
The twenty-first source patch adds
`pione-definition-tame-fundamental-group`,
`pione-theorem-tame-specialization`, and
`pione-proposition-tame-fundamental-group-punctured-curve`.  The new Galois
subcategory makes the tame fundamental group relative to its compactification
machine-usable.  The specialization theorem gives the full tame surjection and
the prime-to-residue-characteristic isomorphism for a smooth proper family with
a smooth relative divisor.  The curve proposition supplies the exact $2g+n$
generators, surface-and-inertia relation, tame inertia generators, and
prime-to-characteristic realization theorem.  Decisions `D000332` and
`D000333` supersede gap records `D000102` and `D000103`; Expose 182 now has no
remaining `new_statement` or `extend_existing` disposition.  The Fundamental
Groups chapter passed three PDF builds and all four affected pages passed
rendered inspection.  The next cursor returns to the unresolved higher-Ext
hypothesis in Expose 149, Proposition 2.
The twenty-second source patch adds
`cohomology-lemma-stalk-ext-finite-resolution` and
`cohomology-remark-stalk-ext-finite-presentation`.  The lemma proves that a
finite free partial resolution through degree $q+1$ identifies internal Ext
and module Ext at a stalk through degree $q$.  The remark relates this exact
finite-range statement to the existing pseudo-coherent derived theorem and
to the Noetherian coherent case intended in Expose 149.  Decision `D000334`
supersedes open record `D000004`, and issue `I000001` is resolved without
silently strengthening the historical hypothesis.  The authority page and
linked erratum page were inspected at 1200 dpi-equivalent.  The Cohomology of
Sheaves chapter passed two PDF builds and both affected pages passed rendered
inspection.  The next cursor is Expose 149 Section 3's arbitrary-ideal Ext and
Tor comparison maps.
The twenty-third source patch adds
`cotangent-lemma-conormal-ext-tor-maps`.  For an arbitrary quotient $A\to B$
it constructs the functorial map from $\operatorname{Ext}^p_A(B,M)$ to the
dual of $\bigwedge^p(I/I^2)$ and the companion map from that exterior power
and $\operatorname{Hom}_A(B,M)$ to $\operatorname{Tor}_p^A(B,M)$.  The proof
combines the canonical conormal-to-Tor edge map with an explicit Ext--Tor
pairing on a projective resolution.  Decision `D000335` supersedes gap record
`D000007`; together with the existing regular-Koszul calculation this closes
Expose 149 Section 3's general construction.  The Cotangent Complex chapter
passed two PDF builds and all three affected pages passed rendered inspection.
The next cursor is Expose 149 Theorem 3 bis and its partial-range singular
duality equivalence.
The twenty-fourth source patch adds
`duality-lemma-duality-proper-over-field-in-range`.  It packages the exact
partial-duality criterion intrinsically: duality against the lowest
cohomology module of the normalized dualizing complex in the top $c+1$
cohomological degrees is equivalent to eventual negative-twist vanishing,
co-effaceability under coherent surjections, and vanishing of the next $c$
cohomology modules of the dualizing complex.  Its spectral-sequence argument
also recovers the historical asymptotic criterion without retaining a chosen
embedding in projective space.  Decision `D000336` supersedes gap record
`D000028` with direct equivalent coverage.  The Duality chapter passed the
final two bibliography-complete PDF builds at 98 pages with no new overfull
boxes, and the complete inserted lemma on pages 71--72 passed rendered
inspection.  The next cursor is Expose 149 Theorem 5 and its general Hodge
fixed-point statement.
The twenty-fifth source patch adds
`derham-lemma-hodge-classes-points-diagonal-graph` and
`derham-lemma-hodge-fixed-point-formula`.  The normalization lemma proves
that rational points have one common nonzero top Hodge Gysin class and that
the diagonal and every graph send this class to its exterior square.  The
fixed-point lemma then computes a transverse graph--diagonal intersection in
two ways: as the degree of the finite etale fixed scheme and as the total
Hodge supertrace.  Decision `D000337` supersedes gap record `D000033` with
direct equivalent coverage of Expose 149, Theorem 5.  The De Rham chapter
passed two final PDF builds at 70 pages with no new overfull boxes, and the
complete additions on pages 59--61 passed rendered inspection.  Expose 149
now has no remaining `new_statement` or `extend_existing` disposition.  The
next cursor is Expose 182's non-geometrically-connected product injection.
The twenty-sixth source patch adds
`pione-lemma-ses-field-component` and strengthens
`pione-lemma-fundamental-group-product-one-proper`.  The new exact sequence
identifies the image of a connected scheme's fundamental group in the
absolute Galois group with the stabilizer of its chosen geometric component.
Intersecting the two stabilizers then identifies the fundamental group of the
chosen product component with the arithmetic fibre product over the absolute
Galois group.  It follows that the map to the direct product is injective for
arbitrary connected finite-type factors when one is proper and is an
isomorphism over an algebraically closed field; the historical separability
hypothesis is unnecessary.  Decision `D000338` supersedes residual record
`D000322` with stronger coverage.  The Fundamental Groups chapter passed two
final PDF builds at 89 pages with no new overfull boxes, and the complete
additions on pages 39 and 44--45 passed rendered inspection.  The product
residual in Expose 182 is closed.  The next cursor is Expose 190's
finite-epimorphism factorization.
The twenty-seventh source patch adds
`descent-lemma-finite-epimorphism-injective-functions`,
`descent-lemma-finite-effective-epimorphism-functions`, and
`descent-theorem-finite-epimorphism-canonical-factorization`.  The first two
lemmas identify finite scheme epimorphisms with injectivity on functions and
finite effective epimorphisms with the exact function equalizer.  The theorem
constructs the canonical sequence of finite effective epimorphisms over a
Noetherian target, proves termination and flat-base-change compatibility, and
proves minimality among all such factorizations.  Decision `D000339`
supersedes gap record `D000121` with stronger coverage.  The Descent chapter
passed its final two bibliography-complete PDF builds at 95 pages with no new
overfull boxes, and the complete addition on pages 19--21 passed rendered
inspection.  Both semantic validators pass with no errors: 21,496 labels and
339 append-only decisions.  The next cursor is Expose 190's exact flat
base-change and flat-object descent package on source pages 306--307.
The twenty-eighth source patch adds
`descent-lemma-equalizer-flat-module-descent`,
`descent-lemma-effective-descent-flat-modules`,
`descent-lemma-finite-effective-epimorphism-flat-schemes`, and
`descent-lemma-finite-effective-epimorphism-flat-quasi-coherent`.  It proves
full faithfulness on flat modules from the exact ring equalizer and packages
the corresponding flat-scheme and flat-quasi-coherent results for a finite
effective epimorphism.  It separately records the modern stronger conclusion:
a universally injective ring map gives effective descent for flat modules.
Decision `D000340` supersedes gap record `D000122` as `existing_weaker`, since
the arbitrary finite coequalizer diagram and effectivity for every finite
effective epimorphism remain explicit residuals.  The next cursor is Expose
190's analytic Grauert--Remmert passage on source pages 307--312.
The twenty-ninth source patch adds
`etale-lemma-etale-analytification-local-isomorphism`,
`pione-theorem-riemann-existence`, and
`pione-lemma-fundamental-group-complex`.  It turns the existing unlabelled
analytic criterion for etaleness into a cited result and states the full
Riemann-existence equivalence for every finite-type complex scheme without a
normality hypothesis together with the profinite fundamental-group comparison.
The already present universal-homeomorphism theorem and modern Cech and stack
formalism cover the remaining algebraic and descent assertions in greater
generality.  Decision `D000341` supersedes gap record `D000123` with stronger
coverage.  The Etale Morphisms chapter passed two final bibliography-complete
builds at 31 pages and the Fundamental Groups chapter passed two at 90 pages;
neither addition introduced an overfull box.  The complete additions on pages
22 and 19 respectively passed rendered inspection.  Both semantic validators
pass with no errors: 21,504 labels and 341 append-only decisions.  The next
cursor is Expose 190 Theorem 3 and the subsequent Cartier descent package on
source pages 318--324.
The thirtieth source patch adds
`groupoids-lemma-descend-along-fpqc-radicial`.  It proves that every descent
datum on a scheme is effective along an arbitrary surjective quasi-compact
flat radicial morphism, with no finite-presentation hypothesis.  Surjectivity
of the diagonal makes affine opens invariant after first descending an affine
open neighbourhood of the base point; affine fpqc descent and the existing
local effectivity criterion then finish the proof.  Decision `D000342`
supersedes `D000138` and closes the radicial half of Expose 190, Theorem 3.
Issue `I000003` is narrowed rather than erased: the finite branch still lacks
coverage for finite faithfully flat morphisms that are not finite locally
free.  The next cursor is the Cartier descent package on source pages
318--324.
The thirty-first source patch adds
`descent-lemma-finite-locally-free-endomorphism-descent`,
`descent-lemma-height-one-differential-operators`,
`descent-proposition-cartier-descent-modules`, and
`descent-lemma-cartier-descent-algebras`.  It first gives the Morita form of
finite locally free module descent.  For a height-one p-basis presentation it
then proves that the endomorphism algebra is generated by multiplication and
the commuting p-nilpotent partial derivations.  This yields effective Cartier
descent for modules, algebras, and affine schemes, with the descended object
recovered as horizontal sections; equivalently these are flat connections
with zero p-curvature.  Decision `D000343` supersedes `D000139` but remains
`extend_existing`, because the precise Atiyah--Cartier line-bundle
rationality criterion is the next residual.  The Descent chapter passed two
final bibliography-complete builds at 99 pages with no new overfull boxes,
and the complete addition on pages 9--11 passed rendered inspection.  Both
semantic validators pass with no errors: 21,510 labels and 343 append-only
decisions.  The next cursor is Expose 190, Section 4 on source page 323.
The thirty-second source patch adds
`descent-lemma-rigidified-invertible-fpqc-descent` and
`descent-proposition-atiyah-cartier-invertible`.  Rigidification along a
section removes all automorphisms when universal global functions come from
the base, so any comparison isomorphism is unique and its cocycle condition
is automatic.  The Atiyah--Cartier proposition then normalizes a line bundle,
identifies vanishing of its ordinary first principal-parts class with a
connection, normalizes that connection along the section, and forces both its
curvature and p-curvature to vanish.  Cartier descent recovers the descended
line bundle from horizontal sections.  Decision `D000344` supersedes
`D000343` as `existing_stronger`; Expose 190, Section 4 no longer has a
semantic residual.  The Descent chapter passed two final
bibliography-complete builds at 100 pages with no new overfull boxes, and the
complete addition on pages 11--13 passed rendered inspection.  Both semantic
validators pass with no errors: 21,512 labels and 344 append-only decisions.
The next cursor is Expose 190, Proposition 5.1 on source page 324.
The Expose 190 residuals include the arbitrary finite-coequalizer extension
of flat-object full faithfulness and effectivity beyond the pure case the
finite-flat quasi-projective descent branch without a finite-presentation
hypothesis descent of abelian models and the non-GL_n torsor
consequences.  The Expose 195 residuals are the general minimal-pair
prorepresentability theorem its Artinian equalizer criterion the narrow
non-flat descent theorem the nonproper formal Hom Picard and scheme-moduli
cases the Witt-smooth abelian deformation result and the generally
non-Noetherian formal parameter object for ramified finite flat coverings.
The Expose 212 residuals are the finite-scheme geometric-fibre exactness
statement the scheme and quasi-projectivity refinements for proper-flat
quotients the saturated generic scheme quotient
the abelian good-reduction application and the Artinian and field-valued
group-scheme quotient theorems.
The Expose 221 residuals are the general bounded-family calculus the
dimension-filtration and partial-Hilbert-coefficient boundedness the classical
Grassmann construction and projective-scheme conclusion the eventual very
ample determinant line the local-to-global normal-sheaf smoothness package
smooth Weil restriction along finite flat morphisms the norm morphism from
finite-length Hilbert spaces to symmetric products and the scheme-level
positive and negative Weil-restriction refinements.
The Expose 232 residuals are the classical Picard-scheme and
quasi-projective-translate existence theorem the general relative-divisor
open Hilbert scheme the projective-bundle fibres and projectivity of the
divisor-to-Picard morphism the degeneration counterexamples the affine
component-gluing and nilpotent-thickening comparisons the arbitrary
projective-scheme Picard theorem over a field and the Lefschetz and
pro-algebraic class-group refinements.
The Expose 236 residuals are the remaining relative component-locus global
quasi-compactness and universal-openness assertions the reduced-component
specialization refinements the properness smoothness and
torsion loci of the Picard object the general Picard multiplication map the
canonical abelian Picard subscheme the Albanese torsor and universal map the
deformation and local-freeness packages Picard boundedness and projectivity.
Its erratum supplement additionally isolates finite-type pullbacks and power
maps finite type of the torsion-component locus bounded Neron--Severi groups
numerical-equivalence tests and openness-and-closedness of the torsion locus.
The thirty-third source patch adds
`groupoids-lemma-projective-after-finite-locally-free-base-change`,
`examples-definition-abelian-scheme`, and
`examples-proposition-abelian-model-finite-etale-descent`.  The norm of an
ample invertible sheaf proves that projectivity descends once the underlying
scheme has descended through a finite locally free cover; this does not make
the false claim that projectivity is fpqc-local for arbitrary descent data.
The abelian-model proposition extends the generic comparison isomorphism over
the regular double overlap using rational-section extension, obtains the
cocycle by uniqueness, descends the scheme and group law, recovers
projectivity by the norm lemma, and proves uniqueness of the resulting model.
Decision `D000345` supersedes gap record `D000140` with exact coverage of
Expose 190, Proposition 5.1.  The Groupoid Schemes chapter passed two final
bibliography-complete builds at 57 pages and the Examples chapter passed two
at 80 pages; the additions on pages 54--55 and 65--67 respectively introduce
no overfull box and passed rendered inspection.  Both semantic validators
pass with no errors: 21,515 labels and 345 append-only decisions.  The next
cursor is Expose 190, Section 6 on source pages 325--327.
The thirty-fourth source patch adds
`groupoids-lemma-smooth-torsor-etale`,
`groupoids-lemma-torsors-special-linear-symplectic`,
`groupoids-lemma-subgroup-torsor-local-triviality`, and
`groupoids-remark-linear-subgroup-torsors`.  It states explicitly that every
torsor under a smooth group scheme is etale locally trivial, proves Zariski
local triviality for special-linear and symplectic torsors and their finite
products, and packages the reduction-of-structure-group argument for both
finite faithfully flat and etale trivializations.  Decision `D000346`
supersedes `D000142` with stronger coverage of Expose 190, Proposition 6.1
and its consequences.  The Groupoid Schemes chapter passed two final
bibliography-complete builds at 58 pages with no new overfull box, and the
complete addition on pages 24--26 passed rendered inspection.  Both semantic
validators pass with no errors: 21,519 labels and 346 append-only decisions.
The next cursor returns to the two remaining Expose 190 theorem-level
residuals: finite-coequalizer flat descent on source pages 305--307 and the
finite-flat quasi-projective branch on source pages 318--319.
The thirty-fifth source patch adds
`descent-lemma-finite-coequalizer-flat-base-change` and
`descent-example-finite-effective-epimorphism-not-pure`.  It proves the full
arbitrary finite-coequalizer flat-base-change and Hom-equalizer statement of
Expose 190, Section 2(c), separates full faithfulness from effectivity, and
demonstrates that a finite effective epimorphism need not be pure.  Decision
`D000347` supersedes `D000340` with stronger modern coverage while preserving
the narrower flat-data effectivity question as historical rather than
claiming an unsupported answer.  The finite faithfully flat
quasi-projective branch remains `I000003`, because direct authority contains
no finite-presentation or local-freeness hypothesis.  The Descent chapter
passed two final bibliography-complete builds at 102 pages with no new
overfull box, and the complete addition on pages 24--27 passed rendered
inspection.  Both semantic validators pass with no errors: 21,521 labels and
347 append-only decisions.  Expose 190 is complete as classified, with
`I000003` explicit; the next cursor is Expose 195.
The thirty-sixth source patch adds the general minimal-pair criterion for
strict prorepresentability to Categories.  It defines strict monomorphisms,
strict proobjects, pointed objects, domination, and minimality; proves that a
functor on a small finite-limit category is strictly prorepresentable exactly
when it is left exact and every pointed object is dominated by a minimal one;
and derives the Artinian-subobject corollary that every proobject then admits
a strict presentation.  Decisions `D000348` and `D000349` supersede
`D000149` and `D000150` with exact integrated coverage of Expose 195,
Proposition A.3.1 and its corollary.  The Categories chapter passed two final
bibliography-complete builds at 105 pages with no new overfull box, and the
complete addition on pages 34--35 passed rendered inspection.  Both semantic
validators pass with no errors: 21,525 labels and 349 append-only decisions.
The next cursor is Expose 195, Theorem B.1.
The thirty-seventh source patch adds
`descent-lemma-artinian-small-effective-descent-flat-modules` and
`descent-remark-finite-artinian-flat-descent-counterexample`.  The theorem
recovers the exact narrow non-flat descent result of Expose 195, Theorem B.2:
the maximal-ideal hypothesis identifies the base ring with a fibre product
over its residue field, faithfully flat descent handles the reduced datum,
and the existing flat-module patching theorem reconstructs the module.  A
cocycle argument in the embedded nilpotent maximal ideal proves that the
reconstructed datum is the original one.  Venken's finite local Artinian
counterexample is retained beside the theorem to show that the ring
equalizer alone gives full faithfulness but not effectivity.  Decision
`D000350` supersedes `D000155` with exact integrated coverage.  Validation,
build, and rendered inspection all pass: the two semantic validators report
no errors at 21,527 labels and 350 append-only decisions; a complete
bibliography pass followed by two final TeX passes produces a 103-page
Descent chapter; no overfull box occurs in the added source block; and pages
17--19, containing the full theorem, proof, counterexample warning, and both
joins to the surrounding chapter, pass rendered inspection.  The next cursor
is Expose 195, Theorem B.1.
The thirty-eighth source patch adds the Grothendieck--Levelt criterion to
Formal Deformation Theory.  It distinguishes finite-length algebras with
varying residue fields from the fixed-residue-field deformation category,
defines the required Cech equalizer property, proves the ring equalizer for
minimal local extensions of length one, and states the exact equivalence
between strict prorepresentability, preservation of all applicable Cech
equalizers, and the traditional local tests `(P)`, `(L)`, and `(M)`.  The
proof records the finite normal residue-field extension and finite free local
base-change step rather than suppressing it.  Direct inspection of Levelt's
1969 paper and his 1970 correction established that the criterion is valid
but the last assertion of the original Section 3, Lemma 5 is false; the
replacement proof is therefore cited explicitly and the invalid shortcut is
preserved as a warning in
`formal-defos-remark-levelt-correction`.  Decision `D000351` supersedes
`D000154` with exact integrated coverage.  The Formal Deformation Theory
chapter passed a bibliography-complete build followed by two final TeX passes
at 77 pages; both Levelt records are registered in `my.bib`, no overfull box
occurs in the added source block, and pages 74--76 containing the full
insertion and both joins pass rendered inspection.  Both semantic validators
report no errors:
21,532 labels and 351 append-only decisions.  The next cursor is Expose 195,
Proposition C.2.1.
The thirty-ninth source patch proves the valid part of Expose 195,
Proposition C.2.1 and repairs its invalid tangent formula.  For schemes $X$
and $Y$ over a Noetherian ring with $X$ flat, the formal Hom functor commutes
with products; its finite-free local test is fpqc descent, and its length-one
test follows from the finite-effective-epimorphism equalizer for morphisms
with flat source.  The corrected Grothendieck--Levelt criterion therefore
gives strict prorepresentability without adding properness or finite-type
hypotheses.  The fibre over dual numbers has a distinguished base-change
lift, and the existing derivation action identifies all lifts with global
sections of the pulled-back tangent sheaf, in degree zero.  The printed
$H^1$ formula is disproved explicitly by $X=\Spec(A)$ and
$Y=\mathbf{A}^1_A$: its lift set is $A$ while the asserted first cohomology
vanishes.  Decision `D000352` supersedes `D000157`; issue `I000004` is now
resolved by an integrated correction rather than a silent normalization.
The Formal Deformation Theory chapter passed a bibliography-complete build
followed by two final TeX passes at 78 pages, no overfull box occurs in the
added block, and page 76 containing the complete proposition, proof,
correction, and both joins passes rendered inspection.  Both semantic
validators report no errors: 21,534 labels and 352 append-only decisions.
The next cursor is the corollary following Expose 195, Proposition C.2.1.
The fortieth source patch proves the full Noetherianity corollary following
Expose 195, Proposition C.2.1, without the narrower separatedness and finite
presentation assumptions in the previously mapped global Mor-space theorem.
For a field-valued morphism $\xi:X_K\to Y_K$, local finite type of $Y$
makes $\Omega_{Y_K/K}$ coherent; its pullback-Hom into
$\mathcal O_{X_K}$ remains coherent, and properness of $X_K$ makes its
global sections finite dimensional.  The corrected degree-zero tangent
formula from the preceding patch therefore meets the local-component
finite-tangent criterion of Expose 195, Proposition A.5.1, expressed in the
current chapter by the bounded-cotangent-space inverse-limit argument.  Thus
every local prorepresenting component is Noetherian for the source's full
locally-finite-type target scope.  Decision `D000353` supersedes `D000158`
with exact integrated coverage.  After the class-native lemma environment
replaced an invalid draft `corollary` environment, the Formal Deformation
Theory chapter passed a bibliography-complete build followed by two final TeX
passes at 78 pages; no overfull box occurs in the added block, and pages
76--77 containing the complete result and both joins pass rendered
inspection.  Both semantic validators report no errors: 21,535 labels and
353 append-only decisions.  The next cursor is Expose 195, Proposition C.3.1.
The forty-first source patch integrates Expose 195, Proposition C.3.1 in the
modern form required by the expos\'e's own warning about the naive Picard
rule: the functor is the fppf sheafification of relative Picard classes, not
the nonlocal assignment $A\mapsto\Pic(X_A)$.  For a flat $X$ over a
Noetherian affine base satisfying the stated universal global-functions
hypothesis, finite-free Cech equalizers are the fppf sheaf condition.  For a
minimal injective extension $A\to B$, the equality
$A=B\times_{B/\mathfrak m}A/\mathfrak m$ reduces the datum modulo the maximal
ideal, uses faithfully flat descent there, and patches finite flat rank-one
modules across the fibre-product square.  The global-functions hypothesis
identifies all line-bundle automorphisms with base units, so passage from the
Picard groupoid to the sheaf of isomorphism classes preserves the equalizer.
The corrected Grothendieck--Levelt criterion then gives strict
prorepresentability without a properness hypothesis.  The first-order
Picard exact sequence and surjectivity on global units identify the tangent
fibre canonically with $H^1(X_A,\mathcal O_{X_A})$; this degree one is valid
and is deliberately distinct from the erroneous degree-one formal-Hom
formula corrected two patches earlier.  An adjacent remark records the 1962
erratum that the source's parenthetical reduction must say ``proper and
separable'', not merely ``proper''.  Decision `D000354` supersedes
`D000161` with exact integrated coverage.  The Quot and Hilbert Spaces
chapter passed a bibliography-complete build followed by two final TeX
passes at 60 pages; a targeted draft dependency build resolved the two
initially missing fibre-product references, no overfull box occurs in the
added block, and pages 28--29 containing the whole proposition, proof, and
erratum remark pass 400 dpi rendered inspection.  Both semantic validators
report no errors: 21,537 labels and 354 append-only decisions.  The next
cursor is the corollary following Expose 195, Proposition C.3.1.
The forty-second source patch integrates Expose 195, Proposition C.4.1 for
the full nonproper scope stated in the source.  A deformation over an
Artinian local algebra is marked by an identification of its special fibre
with the corresponding residue-field extension of the fixed scheme.  The
vanishing of global derivations persists under every finite residue-field
extension and eliminates all automorphisms of marked deformations, so an
isomorphism between the two pullbacks of a class is unique and automatically
satisfies the cocycle condition.  For the finite-free Grothendieck--Levelt
test, fppf descent first produces an algebraic space; its marked special
fibre is a scheme and the result is a nilpotent thickening of that fibre, so
it is again a scheme.  For the length-one test, the exact maximal-ideal and
ring-equalizer identities allow effective descent of every flat affine
coordinate module; multiplication, units, principal localizations, and
gluing descend by full faithfulness.  The corrected Grothendieck--Levelt
criterion therefore gives strict prorepresentability without properness.
The same lemma identifies the tangent space with
$\operatorname{Ext}^1(\mathrm{NL}_{X/k},\mathcal O_X)$, hence with
$H^1(X,\mathcal T_{X/k})$ when $X$ is smooth, and proves that the local
prorepresenting algebra is Noetherian when $X$ is proper by the finite-tangent
bounded-cotangent argument.  Decision `D000355` supersedes `D000164` with
exact integrated coverage.  A bibliography-complete build followed by final
TeX passes produces a 36-page Deformation Problems chapter; the added block
has no undefined reference or overfull box, and pages 14--15 have no visible
placeholder and pass 600 dpi rendered inspection.  Both semantic validators
report no errors: 21,538 labels and 355 append-only decisions.  The next
cursor is the remarks following Expose 195, Proposition C.4.1.
The forty-third source patch resolves three of the four mathematical layers
in the compound remarks following Expose 195, Proposition C.4.1.  The
cotangent-complex formalism already supersedes the source's diagonal-Ext
description for a nonsmooth scheme.  A new characteristic-free theorem proves
that the marked deformation functor of a dimension-$g$ abelian variety over a
complete Noetherian coefficient ring is strictly prorepresented by
$\Lambda[[t_{ij}\mid 1\leq i,j\leq g]]$ and is formally smooth of relative
dimension $g^2$.  Its proof combines rigidity, the Grothendieck--Levelt
equalizer tests, and Oort's product-obstruction calculation; in characteristic
two the automorphism $(x,y)\mapsto(x+y,y)$ changes
$i_1(\omega)+i_2(\omega)$ into $2i_1(\omega)+i_2(\omega)$, so invariance still
forces $\omega=0$.  A second theorem gives the exact smooth-proper-curve rings
$\Lambda$, $\Lambda[[t]]$, and
$\Lambda[[t_1,\ldots,t_{3g-3}]]$ in genera zero, one, and at least two.
Decision `D000356` supersedes `D000165` but deliberately remains
`extend_existing`: the covering-extension setup on printed pages 387--389 is
the unresolved fourth layer and belongs with the following proposition.
The exact Oort 1971 authority is registered in `my.bib`.  The Deformation
Problems chapter passed a bibliography-complete build followed by two final
TeX passes at 38 pages and 672,836 bytes; the added block has no unresolved
reference or overfull box, pages 16--18 contain no `??`, pages 16--17 pass
1,200 dpi rendered inspection, and an independent 300 dpi render confirms
that the apparent page-18 running-header clipping was only a large-raster
viewer artifact.  Both semantic validators report no errors: 21,540 labels
and 356 append-only decisions.  The next cursor is the formal-covering setup
in this same compound unit, followed by Expose 195, Proposition C.5.1.
The forty-fourth source patch integrates the formal-covering setup and the
valid corrected form of Expose 195, Proposition C.5.1.  It constructs the
Zariski sheaf of rigid marked finite locally free coverings, proves the
erratum-corrected injection from a local class set into its completion,
identifies compatible infinitesimal systems, and algebraizes them uniquely
over a proper scheme.  The prorepresentability proof applies the corrected
Grothendieck--Levelt criterion: finite-free extensions use fpqc descent, while
minimal injective extensions use effective descent of flat modules followed
by descent of the algebra structure and the reduced-fibre marking.

Two independent defects in the printed proposition are now fail-closed
rather than silently inherited.  First, the literal marking over
$A/\mathfrak mA$ is not cartesian enough on the category of all finite-length
coefficient algebras.  The explicit length-one inclusion
$A\subset B$ with $a=\epsilon b$ makes a flat-family quadratic covering
correctly marked over $B$ although its discriminant prevents the required
marking over $A$; the integrated functor therefore uses the functorial
reduced fibre, which agrees with $X_0$ on every $\Lambda_n$.  Second, the
source omits coefficient-flatness, and the two quadratic coverings over
$k[y,z]/(y^2)$ with discriminants $(4z)$ and $(4(z+y))$ become identical
after an injective length-one base extension.  This disproves the
unconditional assertion, and the linked 1962 erratum does not repair either
gap.  Issues I000009 and I000010 retain both counterexamples; decision
D000358 supersedes D000166, while D000357 records the completed setup and
leaves only the subsequent one-dimensional local-product and smoothness
claims open.

Both semantic validators pass with no errors at 21,549 labels, 358
append-only decisions, 1,253 source units, 1,612 term links, and 10 recorded
source issues.  Sequential draft builds of only the eight exact dependency
chapters followed by two final TeX passes produce a 42-page Deformation
Problems chapter of 712,186 bytes with SHA-256
720BE41CE339819C59FC216FACF2E2725B3A18429A753ADFA935948E29CF2ADC.
The added block has no undefined reference or overfull box; extracted pages
19--23 contain no placeholder, and all five pages and both joins pass
1,200-dpi rendered inspection.  The next cursor is the claimed product of
arbitrary completed-local extension classes in dimension one and the claimed
smoothness when the closed fibre is normal.

The forty-fifth source patch closes the two remaining mathematical claims in
Expose 195.  For a finite ramification set the covering sheaf is exactly the
product of its ordinary local stalks.  In the one dimensional
principal-complement case tensor-compatible formal gluing separately proves
that every completed-local covering class algebraizes to the local ring and
hence recovers the source's product of arbitrary completed-local classes.  The
separate argument is necessary: the 1962 erratum changes the general
stalk-to-completion equality to an inclusion so the printed invocation of
parts (a) and (b) no longer proves surjectivity by itself.

The final normal-fibre smoothness assertion is false without further
hypotheses on the fixed covering.  Over the normal DVR $k[t]_{(t)}$ a
rank-four covering which is split after inverting $t$ has an explicit
associative deformation modulo $\epsilon^2$.  Associativity for the triple
$(x_1,x_2,x_2)$ forces an impossible coefficient of $x_3$ in every proposed
lift modulo $\epsilon^3$.  Issue `I000011` records this nonlifting example and
issue `I000012` records the proof gap repaired by formal gluing.  Decisions
`D000359` and `D000360` supersede the two open covering decisions and close
the Expose 195 mathematical cursor.

Both semantic validators pass with no errors at 21,551 labels, 360
append-only decisions, 1,253 source units, 1,612 term links, and 12 recorded
source issues.  Eight exact dependency chapters were built serially before a
bibliography-complete draft and two final TeX passes.  The resulting
Deformation Problems chapter has 43 pages and 726,407 bytes with SHA-256
B71E3AEDB8F00B325B561271C4844883A22B8397194FC2382FD27FCA0C1647F1.
The added block has no new undefined reference or overfull box; pages 23--24
contain no placeholder and pass 1,200-dpi rendered inspection.  The next
substantive cursor is Expose 212.

The forty-sixth source patch integrates Expose 212, Proposition 2.1 and its
kernel-pair consequence for arbitrary finite schemes, rather than only the
finite-locally-free quotient cases already present.  Over a locally
Noetherian base, finite colimits are constructed by taking equalizers of the
corresponding finite algebras.  At a geometric point, flat passage to the
strict henselization preserves those equalizers.  Every finite algebra over
the resulting strictly henselian local ring is a product of local algebras,
each with exactly one point over the chosen algebraically closed field.
Consequently the geometric-point functor is left adjoint to the constant
finite-scheme functor and preserves finite colimits.  Applied to a finite
equivalence relation, this proves that its map to the quotient kernel pair is
a surjective closed immersion, hence is surjective and radicial exactly as
the source asserts.

Decision D000361 supersedes the former gap decision D000169.  Both semantic
validators pass with no errors at 21,553 labels, 361 append-only decisions,
1,253 source units, 1,612 term links, and 12 recorded source issues.  Two
final TeX passes produce a 105-page Descent chapter of 1,179,762 bytes with
SHA-256 B7A039B04D7BA3B861D2B29BE151E37A90BC8D9005A5945BE7000D316EE13568.
The added proposition and consequence have no unresolved reference or
overfull box; their complete pages 26--27 pass 1,200-dpi rendered inspection.
The next substantive cursor is Expose 212, Section 5 and Theorem 5.1.

The forty-seventh source patch closes Expose 212, Section 5.  Exact FGA
references now accompany the invariant-ring integrality theorem, the affine
orbit-space theorem, finite-flat effectivity, the invariant-affine
neighbourhood construction, the global quotient theorem, and the modern
uniform categorical-moduli strengthening.  The affine orbit-space lemma now
also states Corollary 5.2 explicitly: the canonical arrow-scheme morphism to
the quotient kernel pair is surjective.  Its proof lifts an arbitrary point of
the kernel pair to an algebraically closed residue-field extension and applies
the geometric-orbit equality.

A separate lemma in Properties of Algebraic Spaces integrates Corollary 5.5.
For the global finite locally free quotient it proves that the quotient degree
is exactly the degree of either kernel-pair projection and that flatness over
every further base is equivalent on the quotient and its finite locally free
surjective cover.  Decisions D000362--D000368 supersede the seven former
Section 5 decisions without changing any historical row.

Both semantic validators pass with no errors at 21,554 labels, 368 append-only
decisions, 1,253 source units, 1,612 term links, and 12 recorded source issues.
Serial bibliography-complete builds followed by two final TeX passes produce
Groupoid Schemes at 58 pages and 791,125 bytes with SHA-256
75CFE5FC16FDC678832EF369071E55C09B5A5A729133010C160AC6DF9C18AA84;
Properties of Algebraic Spaces at 63 pages and 823,689 bytes with SHA-256
ED49741C270EC825AC4A4AD7E8C0E1ABEBFF4EF0A28F592CCE8C1CAE27D419E1;
and More on Morphisms of Stacks at 51 pages and 712,885 bytes with SHA-256
EE9A1C8CC3AE2BAD25D260C70D48F519DEF7C306B27736AE397397124BBB6EE9.
The changed line ranges add no unresolved reference or overfull box;
Groupoids pages 49--50 and Properties of Algebraic Spaces page 19 contain no
placeholder and pass 1,200-dpi rendered inspection.  The next substantive
cursor is Expose 212, Section 6 and Theorem 6.1 together with its linked
erratum.

The forty-eighth source patch integrates Expose 212, Section 6 at the exact
point justified by the current Stacks machinery.  A new proper-flat groupoid
proposition constructs the finite-inertia Keel--Mori algebraic-space quotient
and proves that its presentation map is surjective, proper, and open, that its
geometric-point fibres are precisely the orbits, and that the arrow scheme
surjects onto the quotient kernel pair.  For an actual equivalence relation it
also proves faithful flatness and effectivity.  The adjacent source-linked
remark records, without conflation, that the historical theorem additionally
asserts a scheme quotient and corrected quasi-projectivity, and that those two
scheme-theoretic refinements do not follow from this argument.

A second new proposition closes Theorem 6.2.  It takes the largest invariant
dense open on which the quasi-finite stabilizer is finite, forms its
finite-inertia moduli space, and passes to a dense scheme open in that
quasi-separated Noetherian algebraic space.  This supplies the exact
finite-type scheme quotient, openness, orbit fibres, quotient topology, and
kernel-pair surjectivity of the source; for an equivalence relation the chosen
quotient is faithfully flat, finitely presented, and effective.  Decisions
`D000369`--`D000372` supersede the four former Section 6 decisions while
retaining the unresolved scheme/quasi-projectivity refinement explicitly.

Both semantic validators pass with no errors at 21,557 labels, 372 append-only
decisions, 1,253 source units, 1,612 term links, and 12 recorded source issues.
Serial dependency builds and two final TeX passes produce a 53-page More on
Morphisms of Stacks chapter of 746,808 bytes with SHA-256
`39BB958A982ED3C64BEB8789903857596AA3E3632591EFF65F7CB4489BDD9D62`.
The added source occupies lines 4093--4267 and rendered pages 44--46; it adds
no unresolved reference or overfull box, contains no placeholder, and passes
1,200-dpi inspection.  The next substantive cursor remains Expose 212,
Theorem 6.1: audit and, if valid, independently reconstruct the residual
scheme and corrected quasi-projectivity argument before moving to Section 7.

The forty-ninth source patch completes that direct-source audit and fails
closed on the residual rather than manufacturing the omitted proof.  Printed
page 113 gives no quasi-section construction: it only says that suitable
quasi-sections reduce Theorem 6.1 to the finite-flat case.  The linked erratum
narrows quasi-projectivity to actual equivalence relations but supplies no
argument.  As an independent later check, Lieblich's 2006 Remark 3.3.2 calls
the corresponding general relative quasi-projective-scheme conclusion a
tempting expectation and gives the argument only over a field or when a finite
flat quasi-projective cover is already available.  The public Stacks remark now
cites that comparison explicitly.

Open source issue `I000013` records the diplomatic source and erratum hashes,
the missing quasi-section step, the later comparison evidence, and the exact
fail-close condition.  Decisions `D000373`--`D000375` supersede the affected
Theorem 6.1, scholium, and section decisions: the proper open algebraic-space
quotient and all effectivity conclusions remain proved; the global scheme and
relative quasi-projectivity claims remain unasserted pending a theorem under
the exact relative hypotheses.  No historical row was changed or removed.

Both semantic validators pass with no errors at 21,557 labels, 375 append-only
decisions, 1,253 source units, 1,612 term links, and 13 recorded source issues,
of which seven remain active.  A bibliography-complete build and two final TeX
passes produce a 53-page More on Morphisms of Stacks chapter of 747,776 bytes
with SHA-256
`D8187426A0B6C71B8811B37A42AAA5CE3D3D25DCCD66475552F8DD0AE80D9106`.
The changed reader paragraph has no unresolved citation or new box warning and
passes 1,200-dpi inspection on page 45.  The next substantive cursor is Expose
212, Section 7 and Proposition 7.1; issue `I000013` remains an explicit global
residual rather than an implicit completion claim.

The fiftieth source patch completes the sequential Section 7 pass without
silently extending any source beyond its proof.  Examples now contains an
independent proof of Proposition 7.1: take the flat schematic closure of the
generic kernel in the abelian model, form its proper fppf algebraic-space
quotient, apply Raynaud's dimension-one representability theorem to obtain a
scheme, and descend flatness and geometric regularity to prove that the
quotient is an abelian scheme.  More on Groupoids in Spaces records the exact
Raynaud theorem.  The inspected Raynaud PDF is 6,849,906 bytes with SHA-256
`FDBA4B96E9F3FA3EEB158868217B95FFD4172F128148A70013115666CF04CF92`.

More on Morphisms of Stacks now records the exact quotient theorem supplied by
SGA 3 over a local Artinian base in its two proved branches: a flat target, or
a monomorphic source homomorphism.  It also proves the flat closed-subgroup
corollary and the quotient-by-kernel/closed-image factorization over a field,
thereby integrating Corollary 7.4.  The checked SGA 3 re-edition PDFs are
Expose V, 549,877 bytes, SHA-256
`9DFB1CE933FF4D1C29710185433AADC99650A06934167C18A630D053730918D7`;
Expose VI_A, 412,401 bytes, SHA-256
`692D61E19DD522B36E87F4918CC7D7420A336ADB28D981A2217F0549C0CEB4CF`;
and Expose VI_B, 862,924 bytes, SHA-256
`981F2AC055F5359A80CEB5E48AEAC85F6B2102F0389446452D033EBFD02B10C9`.
The Expose V editorial note cites VI_A 3.2 and 3.3, but those passages assume
respectively that the target is flat or that the homomorphism is a
monomorphism.  Open issue `I000014` therefore retains the remaining
nonflat-target, nonmonomorphic corner of FGA Theorem 7.2 instead of converting
that citation gap into a false theorem.  Decisions `D000377`--`D000382` are
append-only replacements for the former Section 7 classifications.

Both semantic validators pass with no errors at 21,564 labels, 3,839 topic
candidates, 382 append-only decisions, 1,253 source units, 1,612 term links,
and 14 recorded source issues, of which eight remain active.  The decision and
issue ledgers have SHA-256
`96368B888EC31F7A6A3D253707ABB59C2EBBB73B246F57EFE9C6DD94930F073E`
and `2B72A51905C003F2B863DC400A2642D4029767FCB3009CD0BD27B1E361BCC43C`.
Serial bibliography-complete builds and final TeX passes produce More on
Morphisms of Stacks at 55 pages and 760,913 bytes, SHA-256
`1D8354B56AD1540D1C7A35F7E462465D8354F442AEC6F17B0EB6A86DD819AB3D`;
More on Groupoids in Spaces at 29 pages and 564,709 bytes, SHA-256
`084EDF9E3CB6F73F9996EFB0D6BCFADEED7C67D91E3E4A58442A70B78CBD3DB8`;
and Examples at 81 pages and 1,002,109 bytes, SHA-256
`7ABD7C28A29F1875427E8929D65310EE036FF162638BE496E03C793DBF7B4DEA`.
The new material adds no unresolved reference or overfull horizontal box and
passes 1,200-dpi inspection on More on Morphisms pages 46--47, More on
Groupoids in Spaces page 12, and Examples pages 67--69.  Expose 212 has now
received its complete sequential pass, with issues `I000013` and `I000014`
still visibly open.  The next source cursor is Expose 221, beginning at its
first substantive unit.

The fifty-first source patch begins Expose 221 from authority SHA-256
`ABBF37780FDC514BEBD2F1811BFC94E706E44FA8751402CE171510A3F1520968`.
Moduli Stacks now defines a fibrewise coherent sheaf as a coherent module
over a residue-field extension modulo isomorphism after passage to a common
field, and defines boundedness by one coherent family over a finite-type
parameter scheme.  The adjacent lemma proves directly that bounded families
are closed under finite unions, arbitrary base change, and tensor products.
It also uses generic flatness stratification to replace every bounding family
by finitely many finite-type strata on which its coherent module is flat.
This is the exact infrastructure needed for the harder Hom, extension, and
support constructions that follow; it does not yet claim Propositions 1.2 or
1.3.  Decisions `D000383` and `D000384` supersede the former definition and
partial-section classifications.

Both semantic validators pass with no errors at 21,567 labels, 3,842 topic
candidates, 384 append-only decisions, 1,253 source units, 1,612 term links,
and 14 source issues, of which eight remain active.  The decision ledger has
SHA-256
`3FD34AE025925147C29DEAD86983C4D483E70FB641DE66ACEAD08B3B605F1DA2`.
A bibliography-complete build and two final TeX passes produce a 23-page
Moduli Stacks chapter of 522,606 bytes with SHA-256
`DFFECB9CC00DE875E7B405ED6D3147B83C61F5B115E124DBAB3B0D19D1332FBF`.
The new source adds no unresolved reference or overfull horizontal box and
passes 1,200-dpi inspection on pages 8--10.  The next sequential cursor is
Expose 221, Proposition 1.2.
