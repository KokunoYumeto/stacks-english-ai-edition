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
- all 36 Expose 149 review units have append-only decisions except that
  Proposition 2 remains explicitly open pending its higher-Ext hypothesis
  check
- Expose 149 currently yields 20 `existing_stronger` decisions 10
  `existing_equivalent` decisions 2 `extend_existing` decisions 1
  `new_statement` decision and 2 historical decisions

Sections remain independent review units.  A provisional rule that treated
every section as a structural container was rejected before publication
because FGA sections contain substantial unboxed mathematics such as the
composition law in Ext.  Equations subitems and diagrams inherit the decision
of their semantic parent.

Both `check.json` and `mcheck.json` report `PASS` with empty `errors` arrays.
The warnings preserve nine generated book-part labels and nine current TeX
labels that have no entry in upstream's `tags/tags`; no replacement tag has
been invented.

No Stacks mathematical TeX has been changed yet.  The next cursor is Expose
182 after resolving the open hypothesis in Expose 149 Proposition 2.  The
identified Expose 149 additions are the arbitrary-ideal Ext and Tor comparison
maps the partial-range singular-duality equivalence and the general Hodge
fixed-point statement.
