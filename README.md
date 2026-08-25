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
[Current build receipt](validation/unified-build-2026-08-25.json) ·
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
| GAGA | Integrated through r3 | All 126 units classified, all 79 substantive units decided, and a validated 22-page English chapter | [r3 status](gaga_r3/STATUS.md) · [chapter source](gaga.tex) |
| FGA | Integrated and notation-normalized | 1,253 source units and 1,612 term links closed; fixed-point 83-page Moduli build recorded | [Overview](fga/README.md) · [status](fga/status.md) |
| EGA | Active integration | Direct-French review through EGA I 6.1.13; 1,059 active edges across 355 generated units; next cursor EGA I 6.2.1 | [EGA dossier](ega/README.md) |
| Errata | Composed into this source tree | 15 admitted batches containing 385 stable correction IDs; R16 remains preserved as a candidate, not silently admitted | [Registry](ai-integrated/registry/overlays.json) · [candidate evidence](ai-integrated/candidates/commons/stacks/errata/) |

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
| [`PROVENANCE.md`](PROVENANCE.md) | Upstream identity, merge architecture, and frozen pre-unification histories |

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
python tools/validate_unified_repository.py
```

See [VALIDATION.md](VALIDATION.md) for scope, receipts, and interpretation.

## Attribution and licensing

This repository derives from the Stacks Project. The pinned upstream source
and modified source are distributed under the GNU Free Documentation License
1.2; see [COPYING](COPYING). Registry metadata and schemas have the separate,
narrow rights statement recorded in
[`ai-integrated/RIGHTS.md`](ai-integrated/RIGHTS.md). Attribution does not imply
upstream endorsement.
