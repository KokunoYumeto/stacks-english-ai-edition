# Integration status

Status date: **2026-08-28**

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
| EGA | Partial root-source composition; direct-source review active | Selected local additions are present in root TeX. Complete English discovery and diplomatic French edition trees remain separate read-only inputs. Review reaches EGA I 6.3.10 and continues at 6.4.1. |

## Errata state

- Current integrated registry: **28 overlays / 860 stable IDs**, frozen at R27
  admission commit `8c0539a6a7aa001cc6152daee92d5c7a49bf6a93`, tree
  `110a3006fcbb27b94c4170639aab56db507f9a89`.
- The Stacks errata component is **R1–R27**: 27 batches, 848 stable correction
  IDs, and 961 exact v2 operations. `MC-STK-ERR-1215` is the highest identifier
  through R27; intentional gaps mean it is not a count of corrections. R27
  adds 14 IDs and 14 operations affecting only `modules.tex`.
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
- R27 is validated and pre-publication; no R27 GitHub release or Zenodo version
  is claimed here. R26 remains the latest published preservation release at tag commit
  `7720e2fd3080c39b02275e34c67421ea9cff31d8`, tree
  `cc3b7a21d57d07d70db1323487d125a2f69f98c8`; exact-head CI passed. Its
  six assets total 172,480,328 bytes on each of GitHub and Zenodo, at version
  DOI `10.5281/zenodo.22146844` under concept DOI
  `10.5281/zenodo.22135180`. Anonymous readback matched all 12 downloads by
  filename, byte count, and SHA-256, with zero mismatches. The source projection
  records six privacy replacements in four historical provenance files and
  preserves every unchanged source payload byte-exactly.
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
ancestry, all 28 registry entries and 860 stable IDs, the immutable Verdier and
R22–R27 candidates, the retained Verdier insertion, all 961 exact v2
operations, exact manifest/source-map/payload/review joins, the independent
source correction, public-document links, JSON registries, and unresolved merge
markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current R27 gate built all 25 required chapters (2,492 pages and
26,609,586 PDF bytes) to a global PDF fixed point on sweep four. It is bound to
source `dc849731c9768048b993eb5a9df218118b817f40`, tree
`b3462d130dedb3b3c0625cab0d7a2d406114e17f`, and records zero fatal,
missing-glyph, undefined-reference, undefined-citation, multiply-defined,
rerun-required, or destination-warning diagnostics. Visual QA passed for all 55
affected `modules.pdf` pages, including individual high-resolution review of
10 correction-locus pages. The exact artifact inventory is in the
[current fixed-point build receipt](validation/stacks-errata-a04446e-r27-build-2026-08-28.json).

The [parallel linked-worktree reproducibility gate](validation/stacks-errata-a04446e-r27-reproducibility-2026-08-28.json)
is **PASS**. Both builds use the same commit, tree, builder, environment, and
fixed-point sweep; all 25 `{stem, pages, bytes, sha256}` artifact tuples are
exactly equal. Earlier R24, R22/R23, Verdier, and R21 receipts remain preserved
as historical evidence for their exact source identities and scopes.

The [latest published R26 release receipt](validation/stacks-errata-a04446e-r26-release-2026-08-28.json)
binds the content composition and exact-head validation evidence. The
[cross-host receipt](validation/ai-integrated-stacks-r26-publication-2026-08-28.json)
binds the identical public six-file package on GitHub and Zenodo, including
anonymous SHA-256 readback and ZIP replay.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. Exact anonymous readback of 62
source, registry, candidate, receipt, documentation, tool, and candidate-build
artifact files is recorded in the
[historical Verdier publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json).
