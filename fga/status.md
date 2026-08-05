# Status

Snapshot: Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`.

The reproducible intake, topic crosswalk, and statement-level review are
complete for the bounded FGA corpus.  Every review unit has an append-only
decision and source problems remain explicit.  Twenty-nine mathematical
source patches are implemented and validated; further source integration
remains in progress.

- 119 Stacks TeX files indexed
- 21,504 labelled TeX objects indexed
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
- Expose 195 yields 2 `existing_equivalent` decisions 6 `existing_stronger`
  decisions 4 `existing_weaker` decisions 4 `extend_existing` decisions 4
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

Eight source issues are recorded in `issues.csv`; seven remain active.
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
The Expose 190 residuals include the arbitrary finite-coequalizer extension
of flat-object full faithfulness and effectivity beyond the pure case the
finite-flat quasi-projective descent branch without a finite-presentation
hypothesis the Atiyah--Cartier
rationality criterion descent of abelian models and the non-GL_n torsor
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
