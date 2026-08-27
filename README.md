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
[Current fixed-point build: PASS](validation/stacks-errata-a04446e-r22-r23-build-2026-08-27.json) ·
[Current visual QA: PASS](validation/stacks-errata-a04446e-r22-r23-visual-qa-2026-08-27.json) ·
[Current reproducibility: PASS](validation/stacks-errata-a04446e-r22-r23-reproducibility-2026-08-27.json) ·
[Current R22/R23 publication receipt: PASS](validation/stacks-errata-a04446e-r22-r23-release-2026-08-27.json) ·
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
| FAC | Integrated | Complete review of 661 source targets; 37 new theorem or lemma statements; deterministic validators pass | [Status](fac/STATUS.md) |
| Tôhoku | Integrated through sealed r71 | 1,066 decisions, 679 decided units, and no remaining gap-class dispositions | [r71 status](tohoku_r71/STATUS.md) · [working dossier](tohoku/STATUS.md) |
| GAGA | Integrated through r3 | All 126 units classified, all 79 substantive units decided, and a validated 23-page English chapter | [r3 status](gaga_r3/STATUS.md) · [chapter source](gaga.tex) |
| FGA | Integrated and notation-normalized | 1,253 source units and 1,612 term links closed; fixed-point 83-page Moduli build recorded | [Overview](fga/README.md) · [status](fga/status.md) |
| EGA | Active integration | Direct-French review through EGA I 6.1.13; 1,059 active edges across 355 generated units; next cursor EGA I 6.2.1 | [EGA dossier](ega/README.md) |
| Registry and source overlays | R1–R23 errata and Verdier integrated in registry order | 24 admitted overlays and 652 stable IDs at cutoff `49fc23ab`; the Stacks errata component is 23 batches, 640 IDs, and 697 exact v2 operations through R23 | [Registry](ai-integrated/registry/overlays.json) · [Verdier evidence](ai-integrated/candidates/commons/stacks/verdier/) · [errata evidence](ai-integrated/candidates/commons/stacks/errata/) |

These labels are deliberately precise. “Integrated,” “active,” “admitted,” and
“candidate” are not interchangeable, and no local label is represented as an
official Stacks tag.

## Repository map

| Path | Contents |
| --- | --- |
| [`*.tex`](chapters.tex) | The integrated Stacks-derived source tree |
| [`fac/`](fac/STATUS.md) | FAC statement mapping, source issues, decisions, and validation |
| [`tohoku/`](tohoku/STATUS.md) and [`tohoku_r71/`](tohoku_r71/STATUS.md) | Tôhoku integration dossiers and sealed closure evidence |
| [`gaga/`](gaga/STATUS.md) and [`gaga_r3/`](gaga_r3/STATUS.md) | GAGA mapping history and completed r3 evidence |
| [`fga/`](fga/README.md) | FGA integration, normalization, and build receipts |
| [`ega/`](ega/README.md) | EGA discovery, source-bound mappings, residuals, and active integration |
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

The current R22/R23 build is bound to source
`1e9771352840bd70224027d13e9b32546838ccd2`, tree
`4a3b7398f7607b73ee5596d359e5cf7a401c2256`. It produced 22 readable PDFs
(2,343 pages; 24,389,773 bytes), reached a global fixed point on sweep four,
and recorded zero fatal, missing-glyph, undefined-reference,
undefined-citation, multiply-defined, rerun-required, or destination-warning
diagnostics. All 406 pages of the affected `more-algebra.pdf` were rendered and
reviewed; 63 correction-locus pages were also inspected at high resolution. A
parallel rebuild in a second linked worktree used the same source, builder,
environment, and sweep, and all 22 PDF identities were exactly equal.

The R22/R23 content release is public at
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
