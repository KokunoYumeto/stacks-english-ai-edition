# Verdier candidate: Proposition 1.2.13

This directory is a bounded, metadata-first candidate for one possible addition
to the unofficial AI-integrated Stacks source. It covers exactly the twelve
semantic units from Proposition 1.2.13 in Jean-Louis Verdier's Astérisque 239,
beginning at anchor ch2-1-2-13 on physical authority page 121 and ending at
ch2-1-2-13-proof-complete on physical authority page 122.

The mathematical candidate is the obstruction created by a functorial choice
of cone triangle: if every arrow of a triangulated category is assigned a
distinguished triangle functorially, then the existence of countable products
or countable coproducts forces every arrow to have the split
projection-then-inclusion form. The proposed Stacks label is
lemma-functorial-triangles-decomposable.

## Exact evidence boundary

The controlling authority is AST_1996__239__R1_0.pdf, 19,188,423 bytes,
270 physical pages, SHA-256
6214C252BACEBA5584E3C4AEB564C129851941C1A9250BABAB45B79A3939B0AE.
The authority lock also binds the current four-edition semantic anchor map and
the two English source-page files by byte count and SHA-256. The public source
lineage is the Verdier Zenodo concept DOI 10.5281/zenodo.21792163.

The proposed composition base is published unified Stacks main commit
6bdfac7e39a8419dd765b1c78e1b10d7310726f0. Its pinned official Stacks
upstream is commit a04446e57ec1fbc252a871afcec7752fb2807b14, tree
3feeb703b931a6e7259782c10e7d1575adc83e5e.

## Deduplication

Ten units are mapped to the proposed new lemma. Two terminal proof steps are
already supplied by existing Stacks results and are excluded from any new
payload:

- Tag 05QW supplies the countable-product/countable-coproduct
  idempotent-splitting step.
- Tag 05QU supplies the final equivalence between representable kernel data and
  the split projection-then-inclusion form.

Neither existing tag states the functorial-triangle obstruction itself. The
packet therefore records partial overlap rather than claiming either full
duplication or full novelty without qualification.

## Rights and status

No thesis prose is copied into this candidate. The ledgers contain only exact
locators, hashes, structural descriptions, and independently written
mathematical paraphrases. The source work's provenance and release terms remain
controlling; this packet neither relicenses the source nor asserts that the
source is in the public domain. The authored Stacks fragment is independently
worded, and its incorporation into the upstream-derived source remains governed
by the upstream GNU Free Documentation License 1.2.

One independently worded Stacks fragment has now been authored and is bound to
composition operation VDR-STK-COMP-0001. Its bounded fixed-point build and
mechanical validation pass with zero new diagnostics. The resulting 130-page
derived PDF is 1,244,620 bytes with SHA-256
EDB4BED1F5A166B34562B63D44EEEE70C3F421AAFDD91F31C142E1B0EEAEF96A.
Visual QA passes on the complete printed Lemma 4.15 on PDF page 10 and its two
neighbor pages, with no reported issue.

Independent review and replay now pass. The receipt at
replay/independent-review.json is 14,754 bytes with SHA-256
5FE1320F22A25385EB548B4AD6223B1F1C47B77E0A0D275E76EA2E38ABB4B359.
It independently reconstructs the exact insertion, verifies all twelve source
units and both existing-tag dispositions, checks the proof and its signs,
confirms the build and rendered pages, and reports zero unresolved defects.

The candidate remains not admitted. The proposed label is not an official
Stacks tag; there is no upstream endorsement, review, or acceptance.

## Files

- authority/authority.lock.json binds source, local evidence, public archive,
  and composition identities.
- stable-units.json enumerates all twelve typed units.
- source-map.jsonl maps every unit to the proposed lemma or an existing-tag
  duplicate disposition.
- decisions.jsonl records bounded design decisions.
- rejections.jsonl preserves excluded alternatives and rights exclusions.
- formula-diagram-inventory.json classifies all formula- and diagram-sensitive
  units before payload construction.
- candidate.config.json records the closed scope and truthful gate states.
- payload/fragments/derived-functorial-triangles.tex is the authored and
  fixed-point-build-validated one-lemma fragment.
- composition.jsonl binds the single insertion-only composition operation.
- builds/build-receipt.json, builds/validation.json, and builds/visual-qa.json
  bind the successful bounded build, mechanical validation, and visual QA.
- replay/independent-review.json binds the successful independent mathematical
  review and byte replay.
