# Unofficial AI-Integrated Stacks Project

[![Unified repository validation](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/actions/workflows/validate.yml/badge.svg)](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/actions/workflows/validate.yml)

A single Stacks-derived source tree combining a pinned official upstream
baseline with AI-produced corrections, historical-source integrations, and
machine-readable validation evidence.

> [!IMPORTANT]
> This is an unofficial, independently maintained derivative of the
> [Stacks Project](https://github.com/stacks/stacks-project). All additions and
> integration work beyond the pinned upstream source are produced by
> cooperating AI agents. The original Stacks source remains the work of the
> Stacks Project authors. This repository is not affiliated with, reviewed by,
> approved by, or endorsed by the Stacks Project or its maintainers.

[Current status](STATUS.md) ·
[Browse the source](chapters.tex) ·
[Errata registry](ai-integrated/registry/overlays.json) ·
[Validation](VALIDATION.md) ·
[Current composition receipt](validation/composition-current.json) ·
[Current fixed-point build: PASS](validation/stacks-errata-a04446e-r24-build-2026-08-27.json) ·
[Current visual QA: PASS](validation/stacks-errata-a04446e-r24-visual-qa-2026-08-27.json) ·
[Current reproducibility: PASS](validation/stacks-errata-a04446e-r24-reproducibility-2026-08-27.json) ·
[Current R24 publication receipt: PASS](validation/stacks-errata-a04446e-r24-release-2026-08-27.json) ·
[Current preservation release](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r24-2026-08-28) ·
[Zenodo DOI 10.5281/zenodo.22135181](https://doi.org/10.5281/zenodo.22135181) ·
[Cross-host publication receipt: PASS](validation/ai-integrated-stacks-r24-publication-2026-08-28.json) ·
[Historical R22/R23 publication receipt: PASS](validation/stacks-errata-a04446e-r22-r23-release-2026-08-27.json) ·
[Historical Verdier publication receipt: PASS](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json) ·
[Historical R21 publication receipt: PASS](validation/errata-r18-r19-release-2026-08-25.json) ·
[R17 historical receipt](validation/unification-release-2026-08-25.json) ·
[Roadmap](ROADMAP.md) ·
[Provenance and frozen histories](PROVENANCE.md) ·
[License](COPYING)

## One integrated edition

The official Stacks Project is the canonical upstream. This repository is one
unofficial integrated derivative: the upstream source, admitted errata, and
independently written integrations of classical mathematical sources live in
one versioned tree. The evidence registry is part of this repository under
[`ai-integrated/`](ai-integrated/README.md); it is not a second edition.

The pinned upstream baseline is
[`a04446e57ec1fbc252a871afcec7752fb2807b14`](https://github.com/stacks/stacks-project/commit/a04446e57ec1fbc252a871afcec7752fb2807b14).

## Integration dashboard

| Area | State | Verified scope | Evidence |
| --- | --- | --- | --- |
| FAC | Root source composed; corpus review closed | All 661 targets are dispositioned; 37 independently written theorem or lemma additions and bounded corrections are present in the root TeX tree; maintenance remains open | [Status](fac/STATUS.md) |
| Tôhoku | Dossier-only mapping and adjudication closed through sealed r71 | 1,066 decisions, 679 decided units, and zero remaining gap-class dispositions; r71 explicitly changed no live TeX, PDF, canonical source, or cursor | [Sealed r71 dossier](tohoku_r71/STATUS.md) · [historical working dossier](tohoku/STATUS.md) |
| GAGA | Root chapter composed through r3; corpus review closed | All 126 units are classified and all 79 substantive units decided; the current unified `gaga.pdf` is 23 pages, while the sealed r3 dossier records its historical 22-page build | [r3 dossier](gaga_r3/STATUS.md) · [live chapter source](gaga.tex) |
| FGA | Root additions composed and notation-normalized; corpus review closed | All 1,253 units and 1,612 term links are dispositioned; selected independently written additions are in the combined source; the fixed-point Moduli build is 83 pages | [Overview](fga/README.md) · [status](fga/status.md) |
| EGA | Partial root-source composition; direct-source review active | Selected local additions are present in root TeX; the complete English discovery and diplomatic French editions remain separate read-only inputs; review reaches EGA I 6.2.2 and continues at 6.3.1 | [EGA dossier](ega/README.md) |
| Errata and Verdier | Root-composed through R24 in registry order | 25 admitted overlays and 690 stable IDs at cutoff `6df734ec`; Stacks errata R1–R24 comprise 24 batches, 678 IDs, and 754 exact v2 operations; Verdier contributes 12 separately admitted units | [Registry](ai-integrated/registry/overlays.json) · [Verdier release](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json) · [errata evidence](ai-integrated/candidates/commons/stacks/errata/) |

“Root-composed” means that the live top-level TeX tree changed and participates
in the unified build. “Dossier-only” means that mappings, decisions, and
evidence were added without changing live TeX. “Partial” means that only the
specifically recorded local additions are root-composed. Full translation,
discovery, or separately maintained editions are not part of this tree unless
a bounded import and composition receipt explicitly says otherwise. No local
label is represented as an official Stacks tag.

## Repository map

| Path | Contents |
| --- | --- |
| [`*.tex`](chapters.tex) | The integrated Stacks-derived source tree |
| [`fac/`](fac/STATUS.md) | FAC statement mapping, source issues, decisions, and validation |
| [`tohoku/`](tohoku/STATUS.md) and [`tohoku_r71/`](tohoku_r71/STATUS.md) | Tôhoku mapping and adjudication dossiers; sealed r71 is dossier-only and made no live-TeX change |
| [`gaga/`](gaga/STATUS.md) and [`gaga_r3/`](gaga_r3/STATUS.md) | Historical GAGA mapping files and sealed r3 evidence supporting the live root chapter |
| [`fga/`](fga/README.md) | Closed FGA corpus review, composed additions, notation normalization, and build receipts |
| [`ega/`](ega/README.md) | Partial root integration, source-bound mappings, residuals, and separate-edition input boundaries |
| [`reports/`](reports/README.md) | Exact source findings and visual evidence |
| [`ai-integrated/`](ai-integrated/README.md) | Admitted errata, candidates, schemas, provenance, and release records |
| [`VALIDATION.md`](VALIDATION.md) | Reproducible checks and build guidance |
| [`validation/`](validation/README.md) | Machine-readable unified-build receipts |
| [`PROVENANCE.md`](PROVENANCE.md) | Upstream identity, linear publication architecture, and frozen pre-unification histories |

## Build

The source retains the upstream build interface. With a compatible TeX and
Python environment:

```sh
make pdfs
```

Targeted chapters can also be built directly, for example:

```sh
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error moduli.tex
bibtex moduli
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error moduli.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error moduli.tex
```

Run the fast repository-level integrity gate with:

```sh
python tools/validate_unified_repository.py --pre-publication
```

The current R24 build is bound to source
`c3bc402b03dea3c5ac92c9e226645b5895a78887`, tree
`626b67a2c32f4b2bc1b8ad7b4586cdb036b25a21`. It produced 23 readable PDFs
(2,368 pages; 24,949,361 bytes), reached a global fixed point on sweep four,
and recorded zero fatal, missing-glyph, undefined-reference,
undefined-citation, multiply-defined, rerun-required, or destination-warning
diagnostics. All 25 pages of the affected `spaces-duality.pdf` were rendered
and inspected individually at high resolution. A
parallel rebuild in a second linked worktree used the same source, builder,
environment, and sweep, and all 23 PDF identities were exactly equal.

The R24 content release is public at
`50438757de89ec6e67385084d4a2d578707f5a37`, tree
`d1d4b9385d0b67fb2e70220bad8c4fe9c2a2fcd5`. Its exact-head content workflow
passed, and anonymous HTTPS readback matched all 86 checked files (5,155,955
bytes), including both candidate PDFs, by filename, byte count, SHA-256, and
Git blob.

The same validated R24 state is preserved as a downloadable source, PDF, and
evidence release on
[GitHub](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r24-2026-08-28)
and [Zenodo](https://doi.org/10.5281/zenodo.22135181), under concept DOI
[`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180). Anonymous
readback matched all six assets across both hosts by filename, byte count, and
SHA-256. The source archive is bound to public commit `9fb327dd32e18f612ece06e213299f869e9fb11d`;
the EGA program remains explicitly partial and continues at EGA I 6.3.1.

The preceding R22/R23 content release remains public at
`3c2b49fe0d20519de4ab06951ac2cb5151b68782`, tree
`eeb92e6723554f9b8465bee9eac3de58d4a69705`. Its exact-head GitHub Actions
run passed, and anonymous HTTPS readback matched all 138 checked files
(25,024,008 bytes) by filename, byte count, SHA-256, and Git blob.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. Its exact source, candidate,
registry, build, QA, documentation, tooling, and candidate-PDF bytes were read
back anonymously and remain bound in its historical publication receipt.

The preceding R21 Stacks-only fixed point remains historical evidence at
content head `780f48fafbb46dc1057bf8fdcd339693fb44d6bf`. Its receipts and anonymous
readback remain preserved, but they are not presented as evidence for the later
Verdier insertion.

The receipt filenames are stable automation interfaces retained for
compatibility; the JSON schema, source identities, and recorded scope are
authoritative. See [VALIDATION.md](VALIDATION.md) for details.

## Attribution and licensing

This repository derives from the Stacks Project. The pinned upstream source
and modified source are distributed under the GNU Free Documentation License
1.2; see [COPYING](COPYING). Registry metadata and schemas have the separate,
narrow rights statement recorded in
[`ai-integrated/RIGHTS.md`](ai-integrated/RIGHTS.md). Attribution does not imply
upstream endorsement.
