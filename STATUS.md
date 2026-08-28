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

- Current integrated registry: **26 overlays / 821 stable IDs**, frozen at R25
  admission commit `001f36d41504aecfa77201a04fedff16d37b00f0`, tree
  `f8e3a8ea8d7e95190b3cb4d21eb701a6709f90c7`.
- The Stacks errata component is **R1–R25**: 25 batches, 809 stable correction
  IDs, and 908 exact v2 operations. `MC-STK-ERR-1176` is the highest identifier
  through R25; intentional gaps mean it is not a count of corrections. R25
  adds 131 IDs and 154 operations affecting only `artin.tex`.
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
- The French `MORE-ALGEBRA-L-001..029` and `SMOOTHING-001..035` packets remain
  separate intake evidence and are not silently included in this fixed point.
- The current R25 content release is public at
  `fb3e4cb4d834c4e28d84b6df41466ad8aaa71b42`; exact-head CI passed and
  anonymous readback matched 78 R25-changed paths totaling 4,746,502 bytes.
  The six-asset GitHub/Zenodo preservation package contains 171,723,585
  cross-host byte-identical public bytes at version DOI
  `10.5281/zenodo.22143740`.
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
ancestry, all 26 registry entries and 821 stable IDs, the immutable Verdier and
R22–R25 candidates, the retained Verdier insertion, all 908 exact v2
operations, exact manifest/source-map/payload/review joins, the independent
source correction, public-document links, JSON registries, and unresolved merge
markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current R25 gate built all 24 required chapters (2,437 pages and
25,862,634 PDF bytes) to a global PDF fixed point on sweep four. It is bound to
source `a13d609ba9b146eac0a72f593bcf8aff5c5a6a33`, tree
`fbf8d6341b22298d05fdc1f72d547907bc164077`, and records zero fatal,
missing-glyph, undefined-reference, undefined-citation, multiply-defined,
rerun-required, or destination-warning diagnostics. Visual QA passed for all 69
affected `artin.pdf` pages, including individual high-resolution review of all
63 correction-locus pages. The exact artifact inventory is in the
[current fixed-point build receipt](validation/stacks-errata-a04446e-r25-build-2026-08-28.json).

The [parallel linked-worktree reproducibility gate](validation/stacks-errata-a04446e-r25-reproducibility-2026-08-28.json)
is **PASS**. Both builds use the same commit, tree, builder, environment, and
fixed-point sweep; all 24 `{stem, pages, bytes, sha256}` artifact tuples are
exactly equal. Earlier R24, R22/R23, Verdier, and R21 receipts remain preserved
as historical evidence for their exact source identities and scopes.

The [current R25 release receipt](validation/stacks-errata-a04446e-r25-release-2026-08-28.json)
binds the public content head, exact-head workflow, and anonymous byte/hash/blob
readback inventory. The
[cross-host receipt](validation/ai-integrated-stacks-r25-publication-2026-08-28.json)
binds the identical six-file package on GitHub and Zenodo.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. Exact anonymous readback of 62
source, registry, candidate, receipt, documentation, tool, and candidate-build
artifact files is recorded in the
[historical Verdier publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json).
