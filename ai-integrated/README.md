# Errata and integration registry

This directory contains machine-readable provenance, correction overlays,
candidate contracts, replay evidence, schemas, and release records for the
[Unofficial AI-Integrated Stacks Project](../README.md). It is part of the
unified repository, not a separate edition.

> [!IMPORTANT]
> This is independently maintained, AI-produced work. The Stacks Project
> authors and maintainers have not requested, reviewed, approved, or endorsed
> this edition or its overlays.

## Bound upstream

- Official upstream repository:
  <https://github.com/stacks/stacks-project>
- Commit: `a04446e57ec1fbc252a871afcec7752fb2807b14`
- Tree: `3feeb703b931a6e7259782c10e7d1575adc83e5e`
- Upstream lock: [`upstream/stacks.lock.json`](upstream/stacks.lock.json)
- Upstream license boundary: [`RIGHTS.md`](RIGHTS.md)

## Integrated registry cutoff

- Current integrated overlays: **31**, containing **931 stable IDs**.
- Current cutoff: R30 admission commit
  `256846d6a4193f21cd6e1af675dc09e6950aa3d6`, tree
  `9a4f0ba1bd342cde5bf3f8f36a2d68cd7792aef3`.
- The Stacks errata subset is **R1–R30**: 30 batches, 919 correction IDs, and
  1,033 exact v2 operations. Its highest identifier is `MC-STK-ERR-1286`; gaps
  are intentional.
- The 22nd overlay is `stacks-verdier-a04446e-1-2-13-r1`, an independently
  written historical-source insertion with 12 non-official stable units. It
  claims no official Stacks tag, upstream review, approval, or endorsement.

The authoritative overlay list is
[`registry/overlays.json`](registry/overlays.json). The integrated root source
contains the admitted R1–R21 composition, the separately composed Verdier
insertion, the R22-before-R23 `more-algebra.tex` composition, the R24
`spaces-duality.tex` composition, the R25 `artin.tex` composition, the R26
`smoothing.tex` composition, the R27 `modules.tex` composition, and the R28
supersession-aware `smoothing.tex` composition, followed by the R29
`sites-modules.tex` and R30 `injectives.tex` compositions;
registry admission and source composition remain separately testable states.
R21 is replayed as exact manifest-bound operations over cumulative
`simplicial.tex`, and Verdier is inserted into cumulative `derived.tex` through
one unique unchanged context with exact prefix/suffix invariance.

R22 and R23 add 93 IDs and 106 operations affecting only `more-algebra.tex`.
R24 adds 38 IDs and 57 operations affecting only `spaces-duality.tex`. R25 adds
131 IDs and 154 manifest-bound operations affecting only `artin.tex`. R26 adds
25 IDs and 39 operations affecting only `smoothing.tex`. R27 adds 14 IDs and
14 operations affecting only `modules.tex`. R28 adds one ID and one operation
affecting only `smoothing.tex`, superseding `MC-STK-ERR-1183-OP1`.
R29 adds 30 IDs and 31 operations affecting only `sites-modules.tex`; R30 adds
40 IDs and 40 operations affecting only `injectives.tex`. Every round is
composed in registry order from manifest operations; no isolated payload
replaces cumulative source wholesale. The R29/R30 registry import is
`6df0e967030bcf818f3c49584fa5e9a992278d75`; exact source composition is
`3e57820736a5a57ddb1c9fbaaf2206e455b5ee31`, tree
`c4ce1faf96257fe11c0123ca649c9c020982aa33`, followed by validation binding
`c521604343534f94c7a59086c94b99712eb1d754`. The cumulative postimages are
312,179-byte `sites-modules.tex` / SHA-256
`B097799584BD00B3D8046F62A0A56FCFE045516FD04D130C2A4C547CE3BB6C19`
and 105,225-byte `injectives.tex` / SHA-256
`BDC721593BE0B491334C707B371A2EECD1787787903A71E059721BDB66C5AC04`.

R27 is bound by lease `1f05772d6f46ab851cdecdf53b70c11ea698cb14`,
candidate `77fcc9fc2341e72b077224399743f1062e73b228`, and admission
`8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`. The candidate tree is
`6183d66d4f907b7b83f1b69dc799dcfe92a0f4d0`, its candidate subtree is
`fe8a24fb2c4e0279a22d9839364fb3ffd12367d8`, and the admitted registry was
imported at `f3bfc1b987ac9defc1b7811650bac0ec84a01373`. The exact R27 manifest
SHA-256 is `A4D03B8B47A1005B6DAC8B0EE4B9D0F4361E065E51D324B9634F38B51053DE3C`.

The current R30 fixed-point receipts cover 26 PDFs, 2,572 pages, and 27,531,529
PDF bytes at source `c521604343534f94c7a59086c94b99712eb1d754`, tree
`4fe26c45da3edc493b8406824f90db06ef3df28c`. Both linked-worktree builds are
byte-for-byte reproducible. All 111 pages of affected `sites-modules.pdf` and
`injectives.pdf` passed review, including all 42 correction-locus pages
inspected individually at high resolution. R30 is the latest public errata
preservation checkpoint at source head
`e3def48650c66c0d65978a04f67dea88bd8b42ac`, tree
`62bee382516e4a06df6746c5aa61a54b2fe6622f`, and tag
[`ai-integrated-stacks-r30-2026-08-29`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r30-2026-08-29).
The six assets total 178,510,756 bytes on each host; all 12 anonymous GitHub and
Zenodo downloads matched by filename, byte count, and SHA-256. Zenodo version
DOI [`10.5281/zenodo.22166456`](https://doi.org/10.5281/zenodo.22166456) remains
under concept DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
The release preserves the exact 26-PDF, 2,572-page, 27,531,529-byte build
inventory. See the
[R30 release receipt](../validation/stacks-errata-a04446e-r30-release-2026-08-29.json).
R28 remains available as the
[preceding historical release](../validation/stacks-errata-a04446e-r28-release-2026-08-28.json).

## Directory map

| Path | Role |
| --- | --- |
| [`registry/`](registry/) | Admitted overlays, namespace leases, locales, and releases |
| [`candidates/`](candidates/) | Immutable candidates, adjudication, exact source maps, replay, and rejected proposals |
| [`schemas/`](schemas/) | Machine-readable registry and candidate contracts |
| [`upstream/`](upstream/) | Pinned upstream identity and license hashes |
| [`RIGHTS.md`](RIGHTS.md) | Rights and attribution boundary |

Detailed dossiers for FAC, Tôhoku, GAGA, FGA, and EGA remain at the repository
root so that mathematical source, mapping evidence, and build records can be
browsed together. FAC, GAGA, and FGA have root-source additions; the sealed
Tôhoku r71 result is dossier-only and changes no live TeX; EGA has only bounded
partial root-source additions, while its complete English discovery and French
diplomatic editions remain separate read-only inputs. See the project
[status dashboard](../STATUS.md).
