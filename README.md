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
[Current fixed-point build: PASS](validation/stacks-errata-a04446e-r26-build-2026-08-28.json) ·
[Current visual QA: PASS](validation/stacks-errata-a04446e-r26-visual-qa-2026-08-28.json) ·
[Current reproducibility: PASS](validation/stacks-errata-a04446e-r26-reproducibility-2026-08-28.json) ·
[Current published R26 content receipt: PASS](validation/stacks-errata-a04446e-r26-release-2026-08-28.json) ·
[Current preservation release: R26](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r26-2026-08-28) ·
[Current Zenodo version: R26](https://doi.org/10.5281/zenodo.22146844) ·
[R26 cross-host publication receipt: PASS](validation/ai-integrated-stacks-r26-publication-2026-08-28.json) ·
[Historical R24 publication receipt: PASS](validation/ai-integrated-stacks-r24-publication-2026-08-28.json) ·
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
| EGA | Partial root-source composition; direct-source review active | Selected local additions are present in root TeX; the complete English discovery and diplomatic French editions remain separate read-only inputs; review reaches EGA I 6.3.10 and continues at 6.4.1 | [EGA dossier](ega/README.md) |
| Errata and Verdier | Root-composed through R26 | Main contains 27 overlays / 846 stable IDs. Its R1–R26 Stacks errata subset contains 26 batches, 834 correction IDs, and 947 exact v2 operations; R26 contributes 25 IDs and 39 manifest-bound replacements in `smoothing.tex` | [Registry](ai-integrated/registry/overlays.json) · [Verdier release](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json) · [errata evidence](ai-integrated/candidates/commons/stacks/errata/) |

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

The current R26 build is bound to source
`c90a50300dcec156e9ea5fe0c8802c8e36bde81e`, tree
`651fff448fa41a4e7c38970eec169328002ac4f6`. It produced 24 readable PDFs
(2,437 pages; 25,862,999 bytes), reached a global fixed point on sweep four,
and recorded zero fatal, missing-glyph, undefined-reference,
undefined-citation, multiply-defined, rerun-required, or destination-warning
diagnostics. All 37 pages of the affected `smoothing.pdf` were rendered and
reviewed, including 15 correction-locus pages individually inspected at high
resolution. A parallel rebuild in a second linked worktree used the same
source, builder, environment, and sweep, and all 24 PDF identities were exactly
equal. The 134,830-byte cumulative `smoothing.tex` postimage has SHA-256
`85251479BB7D35D73CD5691C194D33B3ADC1BF245BCC248643D969DBBA0E7928`.

The validated R26 state is public as a downloadable source, PDF, and evidence
release on
[GitHub](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r26-2026-08-28)
and [Zenodo](https://doi.org/10.5281/zenodo.22146844), under concept DOI
[`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180). The tag is
bound to public commit `7720e2fd3080c39b02275e34c67421ea9cff31d8`, tree
`cc3b7a21d57d07d70db1323487d125a2f69f98c8`; its exact-head workflow passed.
Anonymous readback matched all six assets and 172,480,328 bytes on each host by
filename, byte count, and SHA-256, for 12 successful downloads and zero
mismatches. The 153,134,447-byte source archive contains a complete
commit-bound projection, 2,169 entries, and an embedded manifest binding six
privacy replacements in four historical provenance files; every unchanged
source member is byte-identical to the bound Git archive. The exact cross-host
evidence is in the
[R26 publication receipt](validation/ai-integrated-stacks-r26-publication-2026-08-28.json).
The EGA integration program in this repository remains explicitly partial and
continues at EGA I §6.4.1. R25 remains preserved as the preceding immutable
version in the same GitHub and Zenodo lineages.

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
