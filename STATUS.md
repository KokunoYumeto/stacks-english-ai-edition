# Integration status

Status date: **2026-08-29**

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
| EGA | Partial root-source composition; direct-source review active | Selected local additions are present in root TeX. Complete English discovery and diplomatic French edition trees remain separate read-only inputs. Review is complete through EGA I §6.4.13 and continues at §6.5.1. |

The current EGA semantic checkpoint is public: §6.4.1–§6.4.13 were source-bound
and routed without changing root TeX or any PDF. GitHub tag
[`ega-i-6.4-semantic-2026-08-29`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ega-i-6.4-semantic-2026-08-29)
and Zenodo version DOI [`10.5281/zenodo.22161051`](https://doi.org/10.5281/zenodo.22161051)
preserve six byte-matched assets totaling 174,783,585 bytes per host. R28 remains
the latest errata release; the next EGA cursor is §6.5.1.

## Errata state

- Current integrated registry: **29 overlays / 861 stable IDs**, frozen at R28
  admission commit `655c8e0e1fe9e7b350244a0ef0230fb6c38e0026`, tree
  `5eddd7d6db54d25eccf09cf21d5d7ab30c3ec1d3`.
- The Stacks errata component is **R1–R28**: 28 batches, 849 stable correction
  IDs, and 962 exact v2 operations. `MC-STK-ERR-1216` is the highest identifier
  through R28; intentional gaps mean it is not a count of corrections. R28
  adds one operation affecting only `smoothing.tex` and explicitly superseding
  R26 operation `MC-STK-ERR-1183-OP1`.
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
- R28 is the current public preservation release at tag
  [`ai-integrated-stacks-r28-2026-08-28`](https://github.com/KokunoYumeto/unofficial-ai-integrated-stacks-project/releases/tag/ai-integrated-stacks-r28-2026-08-28),
  commit `efa46473cf8a73646ef1b6e32354e63ce20fd172`, tree
  `fe139f1aedc35f02dbd10e5471ecb3c7fbed62e1`, and Zenodo version DOI
  [`10.5281/zenodo.22150671`](https://doi.org/10.5281/zenodo.22150671) under
  concept DOI `10.5281/zenodo.22135180`. Workflow run `33212304694`, attempt 1,
  passed. Its six assets total 174,673,433 bytes on each host; anonymous
  readback matched all 12 downloads by filename, byte count, and SHA-256 with
  zero mismatches. The 154,766,484-byte source archive contains 2,312 entries.
- R27 remains published as the preceding historical tag
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
ancestry, all 29 registry entries and 861 stable IDs, the immutable Verdier and
R22–R28 candidates, the retained Verdier insertion, all 962 exact v2
operations, exact manifest/source-map/payload/review joins, the independent
source correction, public-document links, JSON registries, and unresolved merge
markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current R28 gate built all 25 required chapters (2,492 pages and
26,612,367 PDF bytes) to a global PDF fixed point on sweep four. It is bound to
source `9a68186b09bfd9ac66c51359d94b22074d43ebbf`, tree
`fa91f3313576065f7ffa8a3c131435e5b764b162`, and records zero fatal,
missing-glyph, undefined-reference, undefined-citation, multiply-defined,
rerun-required, or destination-warning diagnostics. Visual QA passed for all 37
affected `smoothing.pdf` pages, including individual high-resolution review of
correction-locus page 16. The exact artifact inventory is in the
[current fixed-point build receipt](validation/stacks-errata-a04446e-r28-build-2026-08-28.json).

The [parallel linked-worktree reproducibility gate](validation/stacks-errata-a04446e-r28-reproducibility-2026-08-28.json)
is **PASS**. Both builds use the same commit, tree, builder, environment, and
fixed-point sweep; all 25 `{stem, pages, bytes, sha256}` artifact tuples are
exactly equal. Earlier R24, R22/R23, Verdier, and R21 receipts remain preserved
as historical evidence for their exact source identities and scopes.

The [current R28 publication receipt](validation/stacks-errata-a04446e-r28-release-2026-08-28.json)
binds the public commit and tree, successful exact-head workflow, identical
six-file package on GitHub and Zenodo, anonymous SHA-256 readback, and archive
member replay. The R27 receipt remains historical evidence for the preceding
immutable version.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. Exact anonymous readback of 62
source, registry, candidate, receipt, documentation, tool, and candidate-build
artifact files is recorded in the
[historical Verdier publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json).
