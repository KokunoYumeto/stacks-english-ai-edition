# Illusie integration r2

This bounded integration proposes one source-bound Stacks-style example: two
differential graded presentations that become isomorphic after a common base
change give the same derived-Hom groups against every module over the common
algebra.

## Scope and authority

- Source: *Complexe cotangent et deformations II*, Section 11.5.1,
  equation (11.5.1.7), printed page 175 (physical PDF page 181).
- Authority PDF: 3,525,502 bytes; SHA-256
  `3ECAD82EBF13C74AC02CA452CF56FE1330BF5BF6F1CF00D2656AE7118AA44E13`.
- Corrected French source: 5,009 bytes; SHA-256
  `6510B883F35E9D3E509B91A030F6E8D4BCD0AFB2A1ED1CEFE6E8F7978B107DF2`.
- English witness: 4,943 bytes; SHA-256
  `BBE1F78C5B41FE022EFD9932CF40DC0C6EEE14760C5A1B3A4F12E9963B831F7A`.
- Admitted replacement receipt: 12,700 bytes; SHA-256
  `B72C0C1228B7B9671F212A11C625E97C19CCF8695688D2E598FEF0350C407039`.
- The rejected English generation and its receipt are superseded and excluded.
  Proposition 11.5.2.4 and every adjacent unit are outside this integration.

## Stacks disposition

DGA Lemma 33.5 (Tag 09LT) and Example 33.6 (Tag 0BYX) already supply the
tensor--Hom adjunction and restriction-of-scalars specialization. They do not
record the two-presentation consequence. This integration therefore proposes
one `example`, not a duplicate theorem, in `dga.tex` under the internal label
`example-two-presentations-derived-hom`.

The example is independently worded. It assumes an isomorphism after the two
derived base changes, applies extension--restriction adjunction on both sides,
and obtains functorial shifted Hom-group isomorphisms by composition with the
inverse comparison. It does not import Illusie's stable-normalization
machinery, copy source prose, or claim an official Stacks tag or upstream
endorsement.

## Coordination and validation

- Public issue: https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/issues/2
- Branch: `codex/illusie-derived-hom-r2`.
- Base: public `main` commit
  `4cf4242c1daf5cc49e092a0d347246fc501bb257`, tree
  `d5464f63f28477975749115050fe4750f49d56b3`.
- Write boundary: `dga.tex` and new `illusie_r2/**` only. EGA, FAC, Tôhoku,
  GAGA, `illusie_r1`, and every other root source are read-only.

The candidate must pass an independent mathematical and deduplication replay,
a targeted serial fixed-point `dga.tex` build, affected-page visual QA,
repository validation, exact-head CI, integration on public `main`, and
anonymous public byte/hash readback. `check.json` will bind those results.
