# Status

Snapshot: Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`.

The reproducible intake, topic crosswalk, and statement-level review are
complete for the bounded FGA corpus, apart from one explicitly fail-closed
source hypothesis.  The first four mathematical source patches are implemented
and validated; further source integration remains in progress.

- 119 Stacks TeX files indexed
- 21,455 labelled TeX objects indexed
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
- Expose 182 yields 29 `existing_stronger` decisions 18
  `existing_equivalent` decisions 2 `existing_weaker` decisions 8
  `extend_existing` decisions 8 `new_statement` decisions and 4 historical
  decisions
- Expose 190 yields 19 `existing_equivalent` decisions 8
  `existing_stronger` decisions 1 `existing_weaker` decision 4
  `extend_existing` decisions 2 `new_statement` decisions and 5 historical
  decisions
- Expose 195 yields 2 `existing_equivalent` decisions 6 `existing_stronger`
  decisions 4 `existing_weaker` decisions 4 `extend_existing` decisions 4
  `new_statement` decisions and 1 historical decision
- Expose 212 yields 6 `existing_equivalent` decisions 2 `existing_stronger`
  decisions 1 `existing_weaker` decision 7 `extend_existing` decisions 4
  `new_statement` decisions and 3 historical decisions
- Expose 221 yields 4 `existing_equivalent` decisions 1 `existing_stronger`
  decision 5 `existing_weaker` decisions 6 `extend_existing` decisions 13
  `new_statement` decisions and 4 historical decisions
- Expose 232 yields 2 `existing_equivalent` decisions 7 `existing_weaker`
  decisions 11 `extend_existing` decisions 5 `new_statement` decisions and 8
  historical decisions
- Expose 236 yields 3 `existing_equivalent` decisions 2 `existing_stronger`
  decisions 6 `existing_weaker` decisions 13 `extend_existing` decisions 9
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

Seven source issues are fail-closed in `issues.csv`.  Expose 149
Proposition 2 remains open.  The confirmed issue is Expose 182 Corollary 6:
the stated invariance under algebraically closed base-field extension needs
properness in arbitrary characteristic; an Artin--Schreier cover of the affine
line supplies a characteristic-p counterexample to the unrestricted claim.
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
The warnings preserve nine generated book-part labels and eighteen current TeX
labels that have no entry in upstream's `tags/tags`; nine of these are the new
source labels below.  No replacement tag has been invented.

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
The identified Expose 149
additions are the arbitrary-ideal Ext and Tor
comparison maps the partial-range singular-duality equivalence and the general
Hodge fixed-point statement.  The Expose 182 residuals include the formal
moduli theorem, local-cover descent, projective-bundle automorphisms,
projective-space rigidity and lifting, a product formula for fundamental
groups, finite generation for curves, and the tame specialization package.
The Expose 190 residuals include finite-epimorphism factorization the analytic
Grauert--Remmert passage Cartier p-connection descent the Atiyah--Cartier
rationality criterion descent of abelian models and the non-GL_n torsor
consequences.  The Expose 195 residuals are the general minimal-pair
prorepresentability theorem its Artinian equalizer criterion the narrow
non-flat descent theorem the nonproper formal Hom Picard and scheme-moduli
cases the Witt-smooth abelian deformation result and the generally
non-Noetherian formal parameter object for ramified finite flat coverings.
The Expose 212 residuals are the finite-scheme geometric-fibre exactness
statement the internal Segal nerve theorem the scheme and quasi-projectivity
refinements for proper-flat quotients the saturated generic scheme quotient
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
The Expose 236 residuals are the remaining relative component-locus
properness and universal-openness assertions the reduced-component
specialization refinements the properness smoothness and
torsion loci of the Picard object the general Picard multiplication map the
canonical abelian Picard subscheme the Albanese torsor and universal map the
deformation and local-freeness packages Picard boundedness and projectivity.
Its erratum supplement additionally isolates finite-type pullbacks and power
maps finite type of the torsion-component locus bounded Neron--Severi groups
numerical-equivalence tests and openness-and-closedness of the torsion locus.
