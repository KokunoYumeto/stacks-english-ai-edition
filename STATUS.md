# Integration status

Status date: **2026-08-30**

Pinned official upstream: `a04446e57ec1fbc252a871afcec7752fb2807b14`

This dashboard summarizes the live integrated tree. Detailed evidence remains
in each corpus dossier and in the machine-readable registry.

## Source integrations

| Workstream | Current state | Bounded claim |
| --- | --- | --- |
| FAC | Root source composed; corpus review closed | The full 661-target review is dispositioned. The dossier records 37 independently written theorem or lemma additions, bounded source corrections, successful validators, builds, and targeted visual inspection. |
| Tôhoku | Dossier-only closure through r71 | The sealed successor records 1,066 decisions, 679 decided units, 33 resolved source issues, and zero remaining gap-class dispositions. It explicitly changed no live TeX, PDF, canonical source, or cursor. |
| GAGA | Root chapter composed through r3; corpus review closed | All 126 source units are classified and all 79 substantive units have reviewed decisions. The live 23-page English chapter and deterministic mapping replay pass. |
| FGA | Root additions composed and notation-normalized; corpus review closed | The combined source contains the normalized FGA additions and post-merge dossier. The closure covers 1,253 units, 1,612 term links, and 579 append-only decisions; the recorded fixed-point Moduli build is 83 pages. |
| EGA | Partial root-source composition; direct-source review active | Selected local additions are present in root TeX. Complete English discovery and diplomatic French edition trees remain separate read-only inputs. Review is public through EGA I §6.6.3 and continues at §6.6.4. |

The current EGA semantic checkpoint is public through §6.6.3 and is
source-bound without changing root TeX or any PDF. GitHub tag
[`ega-i-6.6.3-semantic-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.6.3-semantic-2026-08-30)
and Zenodo version DOI [`10.5281/zenodo.22177421`](https://doi.org/10.5281/zenodo.22177421)
preserve six byte-matched assets totaling 182,415,449 bytes per host. R32 is
the latest errata release; the next EGA cursor is §6.6.4.

## Errata state

The generated [`Changes from Upstream`](CHANGES_FROM_UPSTREAM.md) index and
self-contained [`offline change browser`](ai-integrated/changes/index.html)
place the pinned original and integrated replacement side by side for all
1,023 admitted errata IDs, with direct evidence links and no annotations in
the mathematical TeX.

R31 and R32 are composed and validated in registry order. The live registry has
**33 overlays / 1,035 stable IDs** and the cumulative v2 replay contains **1,159
exact operations**. R31 contributes one operation to `sites-modules.tex`; R32
contributes 125 operations across `fields.tex`, `categories.tex`, and
`algebra.tex`. Two independent 27-PDF builds are byte-identical (2,614 pages;
28,121,719 bytes), and all 700 affected-chapter pages plus 72 mapped loci passed
visual QA.

- Current integrated registry: **33 overlays / 1,035 stable IDs**, frozen at
  the sole R31/R32 append-only successor
  `cdea2e13a447e7cdcf5f6f805d3a767d907fd679`, tree
  `b8466dd73dd960c73faeccb8d2c51fe44ecc4b14`.
- The Stacks errata component is **R1–R32**: 32 batches, 1,023 stable correction
  IDs, and 1,159 exact v2 operations. `MC-STK-ERR-1287` is the highest
  identifier through R32; intentional gaps mean it is not a count of
  corrections.
- The 22nd overlay is the separately admitted historical-source contribution
  `stacks-verdier-a04446e-1-2-13-r1`, containing 12 non-official stable units.
  It inserts the manifest-bound Lemma 4.15 into cumulative `derived.tex` through
  a unique unchanged context. No official Stacks tag or upstream endorsement is
  claimed.
- The prior Stacks-only external registry cutoff is
  `13ca6aaaca454f5930c4885c93f427e30cf21959`; the integrated history preserves
  its byte-for-byte registry import and R1–R21 composition as historical state.
- R20 is composed into `derived.tex`. R21 is operation-replayed onto the
  verified cumulative `simplicial.tex`, preserving earlier AI-integrated
  additions outside its manifest-bound operations.
- The independent `injectives.tex` parenthesis correction is included in the
  live source and retained in Git history.
- R22 and R23 are composed in registry order by replaying their manifest-bound
  operations onto cumulative `more-algebra.tex`; neither isolated payload
  replaces the integrated source. The rejected producer `MORE-ALGEBRA-J-006`
  remains excluded.
- R24 is composed by replaying only its 57 manifest-bound operations onto
  cumulative `spaces-duality.tex`; its isolated payload does not replace the
  integrated source. The committed 80,995-byte postimage has SHA-256
  `3CFCEF73EB9172CF69082FF07B9D84442DD5E545D8AD22917D5A694BAA57298E`.
- R25 is composed by replaying only its 154 manifest-bound operations onto
  cumulative `artin.tex`; its isolated payload does not replace the integrated
  source. The committed 254,488-byte postimage has SHA-256
  `F196752E6D872B3B888E57C7183B326287F1A241286991C075E4896996FD185B`.
  The composition is commit `63dfd5f1499bea1916f64256056a5a37bcfb8f9a`,
  tree `7ab863452c932dd5ef230f65abdfa5bdcd6b5771`.
- R26 is composed by replaying only its 39 manifest-bound operations onto
  cumulative `smoothing.tex`; its isolated payload does not replace the
  integrated source. The committed 134,830-byte postimage has SHA-256
  `85251479BB7D35D73CD5691C194D33B3ADC1BF245BCC248643D969DBBA0E7928`.
  Candidate commit `d1f8c1b4654e8d63ea6380dfb5d2e256a6982121` has tree
  `aca634a2dc857f97f6deb52cf4da5ba0792d6d23` and candidate subtree
  `cc94b817fabf54d21c4914e5b7ebf8f168bac807`; registry import
  `ca00b6023be95e0e928d5c0380e24011756bb0ef` precedes composition commit
  `47c6b78e476e5644f5a7d0ca2ce4816b144a2411`, tree
  `cbad56973a9e594743b596a5fd0fa291b490ae26`.
- R26 adjudication accepted 31 producer identities, aliased
  `SMOOTHING-002/003/004` to their existing R1 corrections, rejected
  `SMOOTHING-010`, and merged four repeated semantic groups before
  materializing 25 new stable units.
- R27 is composed by replaying only its 14 manifest-bound operations onto the
  verified cumulative FAC-expanded `modules.tex`; its isolated authority
  projection does not replace the integrated source. The committed 211,777-byte
  postimage has SHA-256
  `BA34DCC89DCEE1BD5F0B9D3C986B18EE9618F723C10E7C7FD3DBD80E9E0B2300`.
  The append-only topology is lease `1f05772d6f46ab851cdecdf53b70c11ea698cb14`,
  candidate `77fcc9fc2341e72b077224399743f1062e73b228`, admission
  `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, linear import
  `f3bfc1b987ac9defc1b7811650bac0ec84a01373`, and composition
  `5a42b7d2a04c4d08be7861ec91306d8be05d631e`.
- R28 is composed by replaying the one active last-wins replacement onto the
  verified cumulative `smoothing.tex`; its isolated payload is evidence only.
  The registry import is `1c26a825306ba0d14607e8364b49125ed3de39b5`
  and the source composition is `1ed5b9fce0f75dec5ad551d32badd8e99abf058a`,
  tree `28c377be399e04fb75f7568000c62e5cfafa291f`. The 134,835-byte postimage
  has SHA-256 `85A37C95D5591632D11E7BE6775039638B6F5200B44729ABCEA1A644D9F5B056`.
- R29 was admitted at `8b70e94d7d9a1f28041445e52df03bffd2980435`
  and received an append-only transport repair at the R30 cutoff
  `256846d6a4193f21cd6e1af675dc09e6950aa3d6`. Its 31 manifest-bound
  operations produce cumulative `sites-modules.tex` at 312,179 bytes / SHA-256
  `B097799584BD00B3D8046F62A0A56FCFE045516FD04D130C2A4C547CE3BB6C19`.
- R30 contributes 40 stable IDs and 40 operations affecting only
  `injectives.tex`. The 105,225-byte cumulative postimage has SHA-256
  `BDC721593BE0B491334C707B371A2EECD1787787903A71E059721BDB66C5AC04`;
  already-present operation `MC-STK-ERR-1262-OP1` was preserved. The R29/R30
  registry import is `6df0e967030bcf818f3c49584fa5e9a992278d75`; exact source composition is
  `3e57820736a5a57ddb1c9fbaaf2206e455b5ee31`, tree
  `c4ce1faf96257fe11c0123ca649c9c020982aa33`, followed by validation binding
  `c521604343534f94c7a59086c94b99712eb1d754`.
- R31 contributes one stable ID and one operation affecting cumulative
  `sites-modules.tex`; R32 materializes 103 historical IDs as 125 operations
  across `fields.tex`, `categories.tex`, and `algebra.tex`. The repaired
  registry chain is imported at `3f0fa66780213432079c6c3044a6a515508b2576`,
  source composition is `bb81deaa0f922caa8b4b4c1e85d928a03c955b24`, and
  topology binding is `e2c25bc25c6a650f6f4eb4069b4749fdc558163c`.
- R32 is the current public errata preservation checkpoint at content head
  `2af5664a7edcd352ebe5f776c2a190859f1ee071`, tree
  `58f1917e35781ffa028c1de4ed28b9aee232a7d7`, and tag
  [`ai-integrated-stacks-r32-2026-08-30`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r32-2026-08-30).
  Its six current assets total 181,650,621 bytes on each host. All six GitHub
  assets and all nine Zenodo files—including three preserved inherited R30
  ZIPs—passed anonymous byte/hash readback and ZIP reopen checks. The Zenodo
  version DOI is
  [`10.5281/zenodo.22167418`](https://doi.org/10.5281/zenodo.22167418) under
  concept DOI `10.5281/zenodo.22135180`. The current package binds 27 PDFs,
  2,614 pages, and 28,121,719 PDF bytes. See the
  [R32 release receipt](validation/stacks-errata-a04446e-r32-release-2026-08-30.json).
- R28 remains publicly preserved as the preceding historical release at tag
  [`ai-integrated-stacks-r28-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r28-2026-08-28),
  commit `efa46473cf8a73646ef1b6e32354e63ce20fd172`, tree
  `fe139f1aedc35f02dbd10e5471ecb3c7fbed62e1`, and Zenodo version DOI
  [`10.5281/zenodo.22150671`](https://doi.org/10.5281/zenodo.22150671) under
  concept DOI `10.5281/zenodo.22135180`. Workflow run `33212304694`, attempt 1,
  passed. Its six assets total 174,673,433 bytes on each host; anonymous
  readback matched all 12 downloads by filename, byte count, and SHA-256 with
  zero mismatches. The 154,766,484-byte source archive contains 2,312 entries.
- R27 remains published as an earlier historical tag
  [`ai-integrated-stacks-r27-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r27-2026-08-28),
  commit `e624abadfe9e2ac1f311485c44c82d6c53df2df2`, tree
  `a2ba195c47c6cb41dca4e4ee7cb6292372e2e201`, and Zenodo version DOI
  [`10.5281/zenodo.22149250`](https://doi.org/10.5281/zenodo.22149250) under
  concept DOI `10.5281/zenodo.22135180`. Workflow run `33198300432`, attempt 2,
  passed. Its six assets total 174,411,900 bytes on each host; anonymous
  readback matched all 12 downloads by filename, byte count, and SHA-256 with
  zero mismatches. The 154,505,160-byte source archive contains 2,245 entries.
  R26 is the preceding immutable historical release.
- The preceding R22/R23 content release remains public at
  `3c2b49fe0d20519de4ab06951ac2cb5151b68782`; exact-head CI passed and
  anonymous readback matched 138 checked files totaling 25,024,008 bytes.

The authoritative registry is
[`ai-integrated/registry/overlays.json`](ai-integrated/registry/overlays.json).
Candidate manifests, source maps, adjudication, replay evidence, and rejected
proposals remain under
[`ai-integrated/candidates/commons/stacks/errata/`](ai-integrated/candidates/commons/stacks/errata/).

## Validation state

The repository integrity gate checks the pinned authority, protected linear
ancestry, all 33 registry entries and 1,035 stable IDs, the immutable Verdier and
R22–R32 candidates, the retained Verdier insertion, all 1,159 exact v2
operations, exact manifest/source-map/payload/review joins, the independent
source correction, public-document links, JSON registries, and unresolved merge
markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current R32 gate built all 27 required chapters (2,614 pages and
28,121,719 PDF bytes) to a global PDF fixed point on sweep four. It is bound to
source `e2c25bc25c6a650f6f4eb4069b4749fdc558163c`, tree
`6a5a81badb3916956fd4c48378e842c5bde9ed49`, and records zero fatal,
missing-glyph, undefined-reference, undefined-citation, multiply-defined,
rerun-required, or destination-warning diagnostics. Visual QA passed all 700
pages of the four affected chapters, including all 72 unique
manifest-bound locus pages at 180 DPI. The exact artifact inventory is in the
[current fixed-point build receipt](validation/stacks-errata-a04446e-r32-build-2026-08-30.json).

The [parallel linked-worktree reproducibility gate](validation/stacks-errata-a04446e-r32-reproducibility-2026-08-30.json)
is **PASS**. Both builds use the same commit, tree, builder, environment, and
fixed-point sweep; all 27 `{stem, pages, bytes, sha256}` artifact tuples are
exactly equal. Earlier R24, R22/R23, Verdier, and R21 receipts remain preserved
as historical evidence for their exact source identities and scopes.

The [latest public R32 publication receipt](validation/stacks-errata-a04446e-r32-release-2026-08-30.json)
binds the public commit and tree, successful exact-head workflow, identical
six-file current package across GitHub and Zenodo, the three inherited Zenodo
R30 ZIPs, anonymous SHA-256 readback, and archive-member replay. The R30, R28,
and R27 receipts remain historical evidence for their immutable versions.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. Exact anonymous readback of 62
source, registry, candidate, receipt, documentation, tool, and candidate-build
artifact files is recorded in the
[historical Verdier publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json).
