# Integration status

Status date: **2026-08-27**

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
| EGA | Partial root-source composition; direct-source review active | Selected local additions are present in root TeX. Complete English discovery and diplomatic French edition trees remain separate read-only inputs. Review reaches EGA I 6.2.2 and continues at 6.3.1. |

## Errata state

- Current integrated registry: **25 overlays / 690 stable IDs**, frozen at R24
  admission commit `6df734ecb3bef8f35770819d17a8d3e267b8e07a`, tree
  `49b8e57e91f0bf04669b2ee93e3586cfb6919088`.
- The Stacks errata component is **R1–R24**: 24 batches, 678 stable correction
  IDs, and 754 exact v2 operations. `MC-STK-ERR-1045` is the highest
  identifier through R24; intentional gaps mean it is not a count of
  corrections. R24 adds 38 IDs and 57 operations affecting only
  `spaces-duality.tex`.
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
- Registry successor `53c517215ef542cfc987e2445a07bb23c7b120fb`
  only materializes the active R25 lease. R25 is not admitted or composed.
  The French `MORE-ALGEBRA-L-001..029` and `SMOOTHING-001..035` packets
  remain unadmitted intake evidence and are not part of this fixed point.
- The current R24 content release is public at
  `50438757de89ec6e67385084d4a2d578707f5a37`; exact-head CI passed and
  anonymous readback matched 86 checked files totaling 5,155,955 bytes,
  including both candidate PDFs.
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
ancestry, all 25 registry entries and 690 stable IDs, the immutable Verdier and
R22–R24 candidates, the retained Verdier insertion, all 754 exact v2
operations, exact manifest/source-map/payload/review joins, the independent
source correction, public-document links, JSON registries, and unresolved merge
markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current R24 gate built all 23 required chapters (2,368 pages and
24,949,361 PDF bytes) to a global PDF fixed point on sweep four. It is bound to
source `c3bc402b03dea3c5ac92c9e226645b5895a78887`, tree
`626b67a2c32f4b2bc1b8ad7b4586cdb036b25a21`, and records zero fatal,
missing-glyph, undefined-reference, undefined-citation, multiply-defined,
rerun-required, or destination-warning diagnostics. Visual QA passed for all 25
affected `spaces-duality.pdf` pages at both contact-sheet and individual
high-resolution review. The exact artifact inventory is in the
[current fixed-point build receipt](validation/stacks-errata-a04446e-r24-build-2026-08-27.json).

The [parallel linked-worktree reproducibility gate](validation/stacks-errata-a04446e-r24-reproducibility-2026-08-27.json)
is **PASS**. Both builds use the same commit, tree, builder, environment, and
fixed-point sweep; all 23 `{stem, pages, bytes, sha256}` artifact tuples are
exactly equal. The earlier Verdier and R21 fixed points remain preserved as
historical evidence for their exact source identities and scopes.

The [current R24 publication receipt](validation/stacks-errata-a04446e-r24-release-2026-08-27.json)
binds the public content head, exact-head workflow, and anonymous byte/hash/blob
readback inventory.

The preceding Verdier content release remains public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. Exact anonymous readback of 62
source, registry, candidate, receipt, documentation, tool, and candidate-build
artifact files is recorded in the
[historical Verdier publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json).
