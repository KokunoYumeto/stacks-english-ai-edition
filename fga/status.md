# Status

Snapshot: Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`.

The reproducible intake and lexical triage are complete for the bounded FGA
corpus.  They are not yet a completed semantic crosswalk or a source patch.

- 119 Stacks TeX files indexed
- 21,446 labelled TeX objects indexed
- 21,437 objects joined to an existing official tag
- 55 FGA topics searched, producing 3,816 bounded topic candidates
- 1,253 FGA units ingested with no omissions or duplicate IDs
- 276 structural units classified
- 9 correction or historical units awaiting link review
- 968 mathematical units awaiting statement-level review
- 5,485 unit candidates generated
- 553 embedded equations or subitems explicitly have no lexical candidate

Both `check.json` and `mcheck.json` report `PASS` with empty `errors` arrays.
The warnings preserve nine generated book-part labels and nine current TeX
labels that have no entry in upstream's `tags/tags`; no replacement tag has
been invented.

No Stacks mathematical TeX has been changed at this checkpoint.  The next
cursor is the evidence-backed topic map, followed by sequential semantic
review beginning with Expose 149.
