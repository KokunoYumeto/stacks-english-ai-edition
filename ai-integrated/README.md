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

- Current integrated overlays: **34**, containing **1,042 stable IDs**.
- Current cutoff: R33 append-only successor
  `acb48c7edaf9595b542b003ed360399870188b7f`, tree
  `8356ae1652ae4ce6a22a457855072c5a3e7b3ad4`.
- The Stacks errata subset is **R1–R33**: 33 batches, 1,030 correction IDs, and
  1,166 exact v2 operations. Its highest identifier is `MC-STK-ERR-1294`; gaps
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
supersession-aware `smoothing.tex` composition, the R29 `sites-modules.tex`
and R30 `injectives.tex` compositions, and then the R31 `sites-modules.tex`
  and R32 `fields.tex`, `categories.tex`, and `algebra.tex` compositions, and
  the R33 `spaces-morphisms.tex` composition;
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
40 IDs and 40 operations affecting only `injectives.tex`; R31 adds one ID and
  one operation affecting `sites-modules.tex`; R32 materializes 103 historical
  IDs as 125 operations across `fields.tex`, `categories.tex`, and `algebra.tex`;
  and R33 adds seven operations to `spaces-morphisms.tex`. Every round is
composed in registry order from manifest operations; no isolated payload
replaces cumulative source wholesale. The R29/R30 registry import is
`6df0e967030bcf818f3c49584fa5e9a992278d75`; exact source composition is
`3e57820736a5a57ddb1c9fbaaf2206e455b5ee31`, tree
`c4ce1faf96257fe11c0123ca649c9c020982aa33`, followed by validation binding
  `c521604343534f94c7a59086c94b99712eb1d754`. R33 was imported at
  `b2ffa008fc27bfdb8b93c431f4df0c3e197d3440` and composed at
  `9100eefe0819f9632c6129e6d6f19a4101d223d1`, tree
  `d786a8604e7c0be79fab77c380247bd971555520`; its seven operations yield
  398,512-byte `spaces-morphisms.tex` / SHA-256
  `048BC16D80E71DBAA9C5CF11B109B69B481D920B278CBCB379C3BC9B8BBFC252`.
  The cumulative postimages are
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

The current R33 fixed-point receipts cover 28 PDFs, 2,730 pages, and 29,277,302
PDF bytes at source `1c90a67eb42de28884be05abd8fb58f781aed7db`, tree
`3c292f9a4b94162ede69d2633b1272b057a498c3`. Both linked-worktree builds are
byte-for-byte reproducible. All 116 pages of `spaces-morphisms.pdf` passed
review, including all five correction-locus pages inspected individually at high
resolution. R33 is the latest public errata preservation checkpoint at content
head `a52883a83081348d0ea4927a03d5fd8aa036890b`, tree
`2d686e92dacdc8e01d6c6950bf81f250e657cd8f`, and tag
[`ai-integrated-stacks-r33-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r33-2026-08-30).
The six current assets total 184,010,318 bytes on each host; all six GitHub
assets and all nine Zenodo files passed anonymous byte/hash readback. Zenodo
version DOI [`10.5281/zenodo.22182175`](https://doi.org/10.5281/zenodo.22182175) is
under concept DOI [`10.5281/zenodo.22135180`](https://doi.org/10.5281/zenodo.22135180).
The release preserves the exact 28-PDF, 2,730-page, 29,277,302-byte build
inventory. See the
[R33 release receipt](../validation/stacks-errata-a04446e-r33-release-2026-08-30.json)
and [public readback](../validation/stacks-errata-a04446e-r33-public-readback-2026-08-30.json).
R30 remains available as the preceding historical release, and R28 remains an
[earlier historical release](../validation/stacks-errata-a04446e-r28-release-2026-08-28.json).

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
