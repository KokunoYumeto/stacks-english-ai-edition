# Status

Snapshot: Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`.

The reproducible intake, topic crosswalk, and statement-level review are
complete for the bounded FGA corpus, apart from one explicitly fail-closed
source hypothesis.  The first seventeen mathematical source patches are implemented
and validated; further source integration remains in progress.

- 119 Stacks TeX files indexed
- 21,478 labelled TeX objects indexed
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
- Expose 149 Proposition 2 remains explicitly open pending its higher-Ext
  hypothesis check
- Expose 149 currently yields 20 `existing_stronger` decisions 10
  `existing_equivalent` decisions 2 `extend_existing` decisions 1
  `new_statement` decision 3 historical decisions and 1 open decision
- Expose 182 yields 30 `existing_stronger` decisions 24
  `existing_equivalent` decisions 5 `existing_weaker` decisions 0
  `extend_existing` decisions 6 `new_statement` decisions and 4 historical
  decisions
- Expose 190 yields 19 `existing_equivalent` decisions 8
  `existing_stronger` decisions 1 `existing_weaker` decision 4
  `extend_existing` decisions 2 `new_statement` decisions and 5 historical
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
- exactly 1 unit remains in `needs_review`: the explicitly open Expose 149
  proposition; no correction or comment root remains unreviewed

Sections remain independent review units.  A provisional rule that treated
every section as a structural container was rejected before publication
because FGA sections contain substantial unboxed mathematics such as the
composition law in Ext.  Equations subitems and diagrams inherit the decision
of their semantic parent.

Eight source issues are fail-closed in `issues.csv`.  Expose 149
Proposition 2 remains open.  The confirmed issue is Expose 182 Corollary 6:
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
The warnings preserve nine generated book-part labels and forty-one current
TeX labels that have no entry in upstream's `tags/tags`; thirty-two of these
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
The identified Expose 149
additions are the arbitrary-ideal Ext and Tor
comparison maps the partial-range singular-duality equivalence and the general
Hodge fixed-point statement.  The Expose 182 residuals include the formal
moduli theorem, the non-geometrically-connected branch
of the product injection, finite generation for curves, and the tame
specialization package.
The Expose 190 residuals include finite-epimorphism factorization the analytic
Grauert--Remmert passage Cartier p-connection descent the Atiyah--Cartier
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
