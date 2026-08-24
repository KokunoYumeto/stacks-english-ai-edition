# GAGA–Stacks R3 release

This successor release preserves the complete 69-file inventory of Zenodo record
`22074492` and adds 25 non-colliding files (`60_` through `84_`), for a final
94-file inventory on the existing concept lineage.

## Formalization result

The R3 bridge maps the GAGA source into the Stacks Project at statement level.
Its terminal receipt records:

- 126 audited source units;
- 79 explicit mapping decisions;
- 0 review units;
- 0 candidate units; and
- 0 remaining substantive statement gaps.

`77_GAGA_Stacks_R3_terminal_receipt.json` binds the final English integration,
mapping tables, deterministic checks, build products, and page-render identities.
The accompanying unit, mapping, decision, issue, and check files are numbered
`72_` through `76_`.

## Editions

The release contains three synchronized editions:

- `60_GAGA_Stacks_R3_English.pdf` — 22 pages;
- `61_GAGA_Stacks_R3_Japanese.pdf` — 21 pages; and
- `62_GAGA_Stacks_R3_Simplified_Chinese.pdf` — 19 pages.

The Japanese and Simplified-Chinese sources preserve the English edition's
labels, references, citations, environment topology, formulas, and chapter
targets. Their theorem and proof captions are localized. The English source,
both localized source pairs, shared preamble, chapter file, bibliography, and
document class are included as files `63_` through `71_`.

All three PDFs were built through XeLaTeX/BibTeX fixed points. Deterministic log,
font, source-structure, extracted-text, and render-identity checks passed. Every
one of the 62 final PDF pages was visually inspected for clipping, overlap,
missing glyphs, broken formulas, and layout defects. The localized build receipt
is `81_GAGA_Stacks_R3_localized_build_validation.json`.

## Reproduction and verification

The release includes the integration builder, edition validator, localized
edition builder, and restart-safe Zenodo publisher as files `78_` through `80_`
and `84_`. In the source tree, the principal deterministic checks are:

```text
python srcmap/build_gaga_r3.py
python srcmap/validate_gaga_editions.py --language all
python srcmap/build_gaga_localized_editions.py --language all
python srcmap/publish_gaga_r3_zenodo.py
```

The last command performs local identity checks and anonymous lineage preflight
without accessing a credential or mutating Zenodo. Publication requires the
explicit `--execute` option. The transaction state is written before any draft
mutation, exact partial uploads are resumable, and every newly public file is
downloaded anonymously and checked against its local byte count and SHA-256.

`83_GAGA_Stacks_R3_MANIFEST.csv` records the local path, remote filename, byte
count, MD5, and SHA-256 of the other 24 new files. The manifest deliberately
omits its own row because a file cannot contain its own final cryptographic hash.

## Rights and provenance

This version inherits the predecessor's citation, rights, and source-provenance
metadata without alteration. Inclusion of formalization sources and validation
artifacts does not grant additional rights in the underlying Serre source
material.
