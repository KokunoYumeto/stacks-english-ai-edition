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
[Changes from Upstream](CHANGES_FROM_UPSTREAM.md) ·
[Offline change browser](ai-integrated/changes/index.html) ·
[Errata registry](ai-integrated/registry/overlays.json) ·
[Validation](VALIDATION.md) ·
[Current composition receipt](validation/composition-current.json) ·
[Current R33 fixed-point build: PASS](validation/stacks-errata-a04446e-r33-build-2026-08-30.json) ·
[Current R33 visual QA: PASS](validation/stacks-errata-a04446e-r33-visual-qa-2026-08-30.json) ·
[Current R33 reproducibility: PASS](validation/stacks-errata-a04446e-r33-reproducibility-2026-08-30.json) ·
[Latest errata public readback: PASS](validation/stacks-errata-a04446e-r33-public-readback-2026-08-30.json) ·
[Latest errata release receipt: R33 PASS](validation/stacks-errata-a04446e-r33-release-2026-08-30.json) ·
[Latest errata preservation release: R33](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r33-2026-08-30) ·
[Latest errata Zenodo version: R33](https://doi.org/10.5281/zenodo.22182175) ·
[Latest EGA semantic checkpoint receipt: PASS](validation/ega-i-6.6.3-semantic-checkpoint-2026-08-30.json) ·
[Latest EGA semantic GitHub release: I §6.6.3](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.6.3-semantic-2026-08-30) ·
[Latest EGA semantic Zenodo version: I §6.6.3](https://doi.org/10.5281/zenodo.22177421) ·
[Historical R28 release receipt: PASS](validation/stacks-errata-a04446e-r28-release-2026-08-28.json) ·
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

## See exactly what changed

[`CHANGES_FROM_UPSTREAM.md`](CHANGES_FROM_UPSTREAM.md) is the readable,
clickable correction index. The self-contained
[`ai-integrated/changes/index.html`](ai-integrated/changes/index.html) adds
offline full-text, chapter, overlay, and evidence-fidelity filters. Every
entry places the pinned original beside the integrated replacement and links
to the immutable upstream source, cumulative source, admitted manifest,
source map, stable unit, and independent review. The mathematical TeX remains
unmarked; the comparison is a generated sidecar that fails closed on evidence
or replay drift.

## Integration dashboard

| Area | State | Verified scope | Evidence |
| --- | --- | --- | --- |
| FAC | Root source composed; corpus review closed | All 661 targets are dispositioned; 37 independently written theorem or lemma additions and bounded corrections are present in the root TeX tree; maintenance remains open | [Status](fac/STATUS.md) |
| Tôhoku | Dossier-only mapping and adjudication closed through sealed r71 | 1,066 decisions, 679 decided units, and zero remaining gap-class dispositions; r71 explicitly changed no live TeX, PDF, canonical source, or cursor | [Sealed r71 dossier](tohoku_r71/STATUS.md) · [historical working dossier](tohoku/STATUS.md) |
| GAGA | Root chapter composed through r3; corpus review closed | All 126 units are classified and all 79 substantive units decided; the current unified `gaga.pdf` is 23 pages, while the sealed r3 dossier records its historical 22-page build | [r3 dossier](gaga_r3/STATUS.md) · [live chapter source](gaga.tex) |
| FGA | Root additions composed and notation-normalized; corpus review closed | All 1,253 units and 1,612 term links are dispositioned; selected independently written additions are in the combined source; the fixed-point Moduli build is 83 pages | [Overview](fga/README.md) · [status](fga/status.md) |
| EGA | Partial root-source composition; direct-source review active | Selected local additions are present in root TeX; the complete English discovery and diplomatic French editions remain separate read-only inputs; review is public through EGA I §6.6.3 and continues at §6.6.4 | [EGA dossier](ega/README.md) |
| Errata and Verdier | Root-composed and deterministically validated through R33 | The integrated tree contains 34 overlays / 1,042 stable IDs. Its R1–R33 Stacks errata subset contains 33 batches, 1,030 correction IDs, and 1,166 exact v2 operations; R33 updates `spaces-morphisms.tex` with seven manifest-bound operations | [Registry](ai-integrated/registry/overlays.json) · [R33 build](validation/stacks-errata-a04446e-r33-build-2026-08-30.json) · [R33 release receipt](validation/stacks-errata-a04446e-r33-release-2026-08-30.json) · [errata evidence](ai-integrated/candidates/commons/stacks/errata/) |

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
| [`CHANGES_FROM_UPSTREAM.md`](CHANGES_FROM_UPSTREAM.md) and [`ai-integrated/changes/index.html`](ai-integrated/changes/index.html) | Generated pinned-original versus integrated correction views |
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

The current validated R33 build is bound to source
`1c90a67eb42de28884be05abd8fb58f781aed7db`, tree
`3c292f9a4b94162ede69d2633b1272b057a498c3`. It produced 28 readable PDFs
(2,730 pages; 29,277,302 bytes), reached a global fixed point on sweep four,
and recorded zero fatal, missing-glyph, undefined-reference,
undefined-citation, multiply-defined, rerun-required, or destination-warning
diagnostics. All 116 pages of `spaces-morphisms.pdf` were rendered and
reviewed, including five correction-locus pages at 180 DPI. A second
linked-worktree build used the same source, builder, environment, and sweep,
and all 28 PDF identities were exactly equal.

R33 is the current manifest-bound registry successor: cutoff
`acb48c7edaf9595b542b003ed360399870188b7f`, tree
`8356ae1652ae4ce6a22a457855072c5a3e7b3ad4`, with 34 overlays and 1,042
stable IDs (R1–R33 contain 1,030 Stacks errata IDs and 1,166 exact operations).
The R33 linear registry import is `b2ffa008fc27bfdb8b93c431f4df0c3e197d3440`;
its seven operations were replayed onto cumulative `spaces-morphisms.tex`,
whose postimage is 398,512 bytes / SHA-256
`048BC16D80E71DBAA9C5CF11B109B69B481D920B278CBCB379C3BC9B8BBFC252`.
No isolated payload replaced a cumulative source.

The R33 public content head is
`a52883a83081348d0ea4927a03d5fd8aa036890b`, tagged
[`ai-integrated-stacks-r33-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r33-2026-08-30).
Its six current assets total 184,010,318 bytes on each host and are preserved
as Zenodo version DOI
[`10.5281/zenodo.22182175`](https://doi.org/10.5281/zenodo.22182175) under
concept DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
The Zenodo successor contains the six R33 assets plus three inherited EGA
semantic archives. Anonymous readback matched all six GitHub files and all
nine Zenodo files; every ZIP reopened with complete listings and valid CRCs.
See the [R33 release receipt](validation/stacks-errata-a04446e-r33-release-2026-08-30.json)
and [public readback](validation/stacks-errata-a04446e-r33-public-readback-2026-08-30.json).

R28 remains publicly preserved as a historical release at tag
[`ai-integrated-stacks-r28-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r28-2026-08-28)
at commit `efa46473cf8a73646ef1b6e32354e63ce20fd172`, tree
`fe139f1aedc35f02dbd10e5471ecb3c7fbed62e1`, and as Zenodo version DOI
[`10.5281/zenodo.22150671`](https://doi.org/10.5281/zenodo.22150671) under
concept DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
GitHub Actions run `33212304694`, attempt 1, completed successfully. Anonymous
readback matched the six assets and 174,673,433 bytes on each host by filename,
byte count, and SHA-256: 12 exact downloads and zero mismatches. The
154,766,484-byte source archive contains 2,312 entries. The exact publication
and public-byte evidence is in the
[R28 release receipt](validation/stacks-errata-a04446e-r28-release-2026-08-28.json).

R27 remains public as the preceding historical tag
[`ai-integrated-stacks-r27-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r27-2026-08-28)
at commit `e624abadfe9e2ac1f311485c44c82d6c53df2df2`, tree
`a2ba195c47c6cb41dca4e4ee7cb6292372e2e201`, and as Zenodo version DOI
[`10.5281/zenodo.22149250`](https://doi.org/10.5281/zenodo.22149250) under
concept DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
GitHub Actions run `33198300432`, attempt 2, completed successfully. Anonymous
readback matched the six assets and 174,411,900 bytes on each host by filename,
byte count, and SHA-256: 12 exact downloads and zero mismatches. The
154,505,160-byte source archive contains 2,245 entries. The exact publication
and public-byte evidence is in the
[R27 release receipt](validation/stacks-errata-a04446e-r27-release-2026-08-28.json).
Its registry cutoff remains `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`,
tree `110a3006fcbb27b94c4170639aab56db507f9a89`; its manifest-bound
composition is commit `5a42b7d2a04c4d08be7861ec91306d8be05d631e`, tree
`ecbad57ee36b4fb290c80cb4d1f83eab50a47460`. R26 remains preserved as the
preceding immutable historical version in the same GitHub and Zenodo lineages.
The current public EGA semantic checkpoint covers EGA I through §6.6.3 and
advances the next cursor to §6.6.4. It is preserved at GitHub tag
[`ega-i-6.6.3-semantic-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.6.3-semantic-2026-08-30),
content commit `f1b8d56b5f3c9999010455a38a289bce76735070`, and Zenodo version
DOI [`10.5281/zenodo.22177421`](https://doi.org/10.5281/zenodo.22177421) in the
existing concept lineage. Its six assets total 182,415,449 bytes per host and
passed 12-file cross-host readback. This semantic-only checkpoint changes no
root TeX or PDF; R33 remains the latest errata release.

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
