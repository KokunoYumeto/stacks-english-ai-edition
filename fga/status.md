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
- 145 review units now have append-only decisions: all 37 Expose 149 units
  including its erratum all 69 Expose 182 units including its erratum and all
  39 Expose 190 units including its erratum
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
- 151 units remain in `needs_review`: 150 without a final decision and the
  explicitly open Expose 149 proposition
- 6 later correction or comment roots still require item-level link review

Sections remain independent review units.  A provisional rule that treated
every section as a structural container was rejected before publication
because FGA sections contain substantial unboxed mathematics such as the
composition law in Ext.  Equations subitems and diagrams inherit the decision
of their semantic parent.

Three source-hypothesis issues are fail-closed in `issues.csv`.  Expose 149
Proposition 2 remains open.  The confirmed issue is Expose 182 Corollary 6:
the stated invariance under algebraically closed base-field extension needs
properness in arbitrary characteristic; an Artin--Schreier cover of the affine
line supplies a characteristic-p counterexample to the unrestricted claim.
Expose 190 Theorem 3 also remains open at its arbitrary non-Noetherian scope:
the direct current Stacks results require a finite locally free cover whereas
the historical statement assumes finite flat or radicial fpqc descent without
a finite-presentation hypothesis.

Both `check.json` and `mcheck.json` report `PASS` with empty `errors` arrays.
The warnings preserve nine generated book-part labels and nine current TeX
labels that have no entry in upstream's `tags/tags`; no replacement tag has
been invented.

No Stacks mathematical TeX has been changed yet.  The next cursor is Expose
195.  The identified Expose 149 additions are the arbitrary-ideal Ext and Tor
comparison maps the partial-range singular-duality equivalence and the general
Hodge fixed-point statement.  The Expose 182 residuals include the formal
moduli theorem, local-cover descent, projective-bundle automorphisms,
projective-space rigidity and lifting, a product formula for fundamental
groups, finite generation for curves, and the tame specialization package.
The Expose 190 residuals include finite-epimorphism factorization the analytic
Grauert--Remmert passage Cartier p-connection descent the Atiyah--Cartier
rationality criterion descent of abelian models and the non-GL_n torsor
consequences.
