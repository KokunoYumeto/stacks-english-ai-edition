# Illusie integration r1

This bounded integration adds one source-bound Stacks-style example: the
relative bar resolution and its acyclicity after restriction of scalars.

## Scope and authority

- Source: *Complexe cotangent et deformations II*, Section 11.4.4,
  printed pages 172--173 (physical PDF pages 178--179).
- Authority PDF: 3,525,502 bytes; SHA-256
  `3ECAD82EBF13C74AC02CA452CF56FE1330BF5BF6F1CF00D2656AE7118AA44E13`.
- The source unit is independently sealed by the accepted page receipts
  recorded in `check.json`.
- Rejected printed page 175 and all later unaccepted Volume II material are
  outside this integration.

## Stacks disposition

The abstract homotopy theorem already exists as Stacks Lemma 14.34.3,
Tag 08ND. The exact relative-bar specialization was not present in the pinned
source. This integration therefore adds an `example`, not a duplicate theorem,
to `simplicial.tex` under the internal label
`example-relative-bar-resolution`.

The example records the terms, faces, degeneracies, augmentation, and the
associated and normalized augmented resolutions. It deliberately stops before
the following flatness sentence in the source, which needs a separate
hypothesis audit.

No official Stacks tag or upstream endorsement is claimed. This is
AI-authored work in an unofficial derivative, coordinated publicly in
repository issue 1.

## Validation

`check.json` records the frozen source identities, deduplication result,
source preimage and postimage, targeted serial build, diagnostics, affected
rendered pages, and public GitHub readback.
