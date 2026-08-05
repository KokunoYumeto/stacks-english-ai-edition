# Status

Snapshot: Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`.

The reproducible intake and topic crosswalk are complete for the bounded FGA
corpus.  Statement-level review is in progress and is not yet a completed
source patch.

- 119 Stacks TeX files indexed
- 21,446 labelled TeX objects indexed
- 21,437 objects joined to an existing official tag
- 55 FGA topics reviewed: 30 direct and 14 broad coverage decisions plus 6
  partial and 5 no-direct decisions
- 1,253 FGA units ingested with no omissions or duplicate IDs
- 952 structural or embedded units classified
- 9 item-level correction or historical units preserved
- 292 independent mathematical or expository units identified for review
- 255 review units now have append-only decisions: all 37 Expose 149 units
  including its erratum all 69 Expose 182 units including its erratum all 39
  Expose 190 units including its erratum all 21 Expose 195 units including its
  erratum all 23 Expose 212 units including its erratum all 33 Expose 221
  units including its erratum and all 33 Expose 232 units including its erratum
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
- 45 units remain in `needs_review`: 44 without a final decision and the
  explicitly open Expose 149 proposition
- 2 later correction or comment roots still require item-level link review

Sections remain independent review units.  A provisional rule that treated
every section as a structural container was rejected before publication
because FGA sections contain substantial unboxed mathematics such as the
composition law in Ext.  Equations subitems and diagrams inherit the decision
of their semantic parent.

Six source-hypothesis issues are fail-closed in `issues.csv`.  Expose 149
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

The broad later conjecture that finite maps should always give effective
descent for flat modules was disproved by Venken.  This does not by itself
refute Expose 195 Theorem 2 because that theorem adds an Artinian maximal-ideal
condition and an Amitsur equalizer condition.  The current Stacks chapter gives
the exact general criterion of universal injectivity but does not prove that
the historical hypotheses imply it or otherwise recover the flat-module-only
claim.  The unit therefore remains an explicit extension target rather than
being silently identified with fpqc descent.

Both `check.json` and `mcheck.json` report `PASS` with empty `errors` arrays.
The warnings preserve nine generated book-part labels and nine current TeX
labels that have no entry in upstream's `tags/tags`; no replacement tag has
been invented.

No Stacks mathematical TeX has been changed yet.  The next cursor is Expose
236.  The identified Expose 149 additions are the arbitrary-ideal Ext and Tor
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
