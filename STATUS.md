# Integration status

Status date: **2026-08-26**

Pinned official upstream: `a04446e57ec1fbc252a871afcec7752fb2807b14`

This dashboard summarizes the live integrated tree. Detailed evidence remains
in each corpus dossier and in the machine-readable registry.

## Source integrations

| Workstream | Current state | Bounded claim |
| --- | --- | --- |
| FAC | Integrated | The full 661-target review is dispositioned. The dossier records 37 new theorem or lemma statements, seven source corrections, 27 corrected Stacks defects, successful validators, builds, and targeted visual inspection. |
| Tôhoku | Integrated through r71 | The sealed successor records 1,066 decisions, 679 decided units, 33 resolved source issues, and zero remaining gap-class dispositions. This does not convert the dossier's explicit nonclaims into a claim of upstream acceptance or an official release. |
| GAGA | Integrated through r3 | All 126 source units are classified; all 79 substantive units have reviewed decisions. The 23-page English chapter and deterministic mapping replay pass. The three previously dangling cross-reference targets are closed. |
| FGA | Integrated and normalized | The combined source contains the normalized FGA chapter and its post-merge dossier. The closure covers 1,253 units, 1,612 term links, and 579 append-only decisions; the recorded fixed-point Moduli build is 83 pages. |
| EGA | Active | Direct-French semantic review reaches EGA I 6.1.13. The active graph contains 1,059 edges across 355 generated units; the next semantic cursor is EGA I 6.2.1. |

## Errata state

- Current integrated registry: **22 overlays / 559 stable IDs**, frozen at
  Verdier admission commit
  `60f1d97ecbd376ff7a91298d17e1f162b9996c3a`.
- The Stacks errata component remains **R1–R21**: 21 batches, 547 stable
  correction IDs, and 591 exact v2 operations. `MC-STK-ERR-0914` is the highest
  Stacks correction identifier through R21; intentional gaps mean it is not a
  count of corrections. R20–R21 add 43 operations, while the bounded R18–R21
  replay contains 120.
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
- R22 and R23 are later admitted, source-disjoint-from-Verdier composer inputs
  for `more-algebra.tex`. They remain queued in registry order and are not
  included in the current 22-overlay / 559-ID cutoff.

The authoritative registry is
[`ai-integrated/registry/overlays.json`](ai-integrated/registry/overlays.json).
Candidate manifests, source maps, adjudication, replay evidence, and rejected
proposals remain under
[`ai-integrated/candidates/commons/stacks/errata/`](ai-integrated/candidates/commons/stacks/errata/).

## Validation state

The repository integrity gate checks the pinned authority, protected linear
ancestry, all 22 registry entries and 559 stable IDs, the immutable Verdier
candidate and exact insertion, the historical R1–R21 validator and all 591 v2
operations, exact manifest/source-map/payload/review joins, the independent
source correction, public-document links, JSON registries, and unresolved merge
markers. See [VALIDATION.md](VALIDATION.md).

Per-corpus build and visual receipts remain linked from the detailed dossiers;
they are not silently generalized beyond their recorded source identity.

The current Verdier v4 gate built all 22 required chapters (2,343 pages and
24,390,066 PDF bytes) to a global PDF fixed point on sweep four. It is bound to
source `7ee4b3a46e995e9e36b259bbc9300828c3c6988b`, tree
`5b3349e5944ecf9d0718c6a31728a457adcd1c69`, and records zero fatal,
missing-glyph, undefined-reference, undefined-citation, multiply-defined,
rerun-required, or destination-warning diagnostics. Visual QA passed for all
130 affected chapter pages and high-resolution pages 9–11. The exact artifact
inventory is in the [current fixed-point build receipt](validation/stacks-verdier-a04446e-1-2-13-r1-build-2026-08-26.json).

The [parallel linked-worktree reproducibility gate](validation/stacks-verdier-a04446e-1-2-13-r1-reproducibility-2026-08-26.json)
is **PASS**. Both builds use the same commit, tree, builder, environment, and
fixed-point sweep; all 22 `{stem, pages, bytes, sha256}` artifact tuples are
exactly equal. The earlier R21 content fixed point at
`780f48fafbb46dc1057bf8fdcd339693fb44d6bf` and its successful anonymous
readback remain preserved as historical evidence for their exact scope.

The Verdier content release is public at
`4947e4a6d22971ea793e4b4bc2b09d8ab8cc04d0`. Exact anonymous readback of 62
source, registry, candidate, receipt, documentation, tool, and candidate-build
artifact files is recorded in the
[current publication receipt](validation/stacks-verdier-a04446e-1-2-13-r1-release-2026-08-26.json).
