# Scaffold schema

## Stable identity

Source IDs use `ega.<volume>.<source-number>[.<subitem>]`. They identify the
mathematical source unit, not a mutable line or PDF coordinate. Page, TeX,
hash, and language locators attach as versioned evidence.

Native diagrams receive deterministic typed child IDs. Existing `tikzcd`
units retain `ega:<parent>:diagram:<ordinal>`; Xy-pic units use the append-only
namespace `ega:<parent>:diagram:xymatrix:<ordinal>`, including commands with
`@` layout options. The type split prevents newly discovered earlier Xy-pic
commands from renumbering published tikz-cd IDs. A diplomatic-French diagram
label may be bound as an evidence alias without replacing the stable child ID.

The `volume` field is the logical EGA volume determined from the stable label
or source-file role. `printed_page` is an independent witness locator and may
name another volume when a later erratum supplies text for an earlier volume.
It must never reclassify the semantic unit.

Every mapped diagram requires its own tightly bounded direct-authority crop
at no less than 5,000 dpi-equivalent detail and its own tightly bounded
final-output crop at the same floor; higher detail remains appropriate for
genuinely ambiguous tiny marks. Full pages shared page crops grouped diagrams
and grouped output crops do not qualify. Admission separately records all objects all directed edges and
the absence of non-edges plus direction hook/equality style label text every
prime bar and subscript geometry and label side. Page legibility or a clean
render is not graph certification. The final native diagram is rendered and
checked independently after source-graph admission. Discovery-only diagram
units remain explicitly unreviewed until this evidence exists.
The identical per-item gate applies to intricate standalone mathematical
blocks including dense arrays compatibility chains exact-sequence grids and
unusual-symbol constructions.

`vqa.csv` is the append-only visual-evidence ledger. A `V` row binds one
stable diagram or selected mathematical-block ID to three separate evidence
surfaces: direct authority, the cumulative French output, and the cumulative
English output. These are three surfaces, not three languages. Each surface
records the exact parent PDF record key, filename-bound byte count and SHA-256,
one-based physical PDF page, top-left crop box in PDF points, committed
individual PNG path, PNG bytes and SHA-256, and dpi-equivalent scale. The
validator recomputes every PNG identity and checks its dimensions against the
box and scale. It rejects shared paths, grouped crops, pages, stale parent-PDF
identities, and scales below 5,000 dpi-equivalent. Profiles and masks state the
required comparison dimensions; normalized signatures record the admitted
complete graph or mathematical chain and explicitly include absent edges.
Harmless punctuation differences between output and authority are named rather
than silently normalized. Discovery units without an active certified `V` row
remain visually unreviewed.
At the 5,000-dpi boundary the committed raster must cover the complete declared
point box: the upper-left pixel is rounded down and the lower-right pixel is
rounded up. A renderer invocation at nominal 5,000 dpi whose integer envelope
still measures fractionally below the floor is preserved in `rej.csv`, not
admitted by rounding the computed scale or weakening the validator.
The immutable first batch keeps its short `bNN` and `dNN` crop names. Every
later V row, including a correction that supersedes one of those rows, uses a
new QA-ID-derived crop path under each surface directory; the historical PNGs
remain present and hash-checked. Only the active successor participates in
item, locator, and crop-byte uniqueness and promotion closure. Its decision
must be an active append-only visual-QA admission D row rather than reusing the
first-batch decision by fiat, and every superseding V row must retain the exact
same stable item ID as its predecessor.

`../reports/qsrc.csv` is the separate append-only source-error crop ledger.
A `Q` row binds one already-recorded correction finding and its controlling
decision plus an active source-error-QA admission decision to one tightly
bounded direct-authority receipt. It records the exact
authority PDF key, bytes and SHA-256; one-based page and page geometry; top-left
PDF-point box; effective scale; short flat crop path; and exact PNG bytes,
SHA-256 and dimensions. These authority-only witnesses prove what the printed
source says; they do not admit a correction and do not substitute for the
three-surface `V` gate. Historical Q rows and crop bytes are immutable. A later
evidence correction appends a new Q row and an append-only finding/decision
closure rather than overwriting either receipt. Q identifiers are contiguous
in append order, crop paths are unique, and every later admission must name
its Q identifier explicitly.
The nested `reports/.gitattributes` pins `qsrc.csv` to LF so its byte receipt is
stable across Windows and Unix checkouts.

`printed_page` names the first printed page on which the generated unit begins.
A separately generated diagram child therefore keeps its own first page even
when its parent statement began earlier. When a frozen discovery witness lacks
a page marker that direct French authority has sealed, `pages.csv` supplies an
append-only evidence overlay. Each active `L` row records the raw parsed page,
the corrected first page, the admitted receipt and page gate, and its decision.
The raw `parsed_page` guard may be empty only when the frozen unit genuinely
has no locator; the authoritative `printed_page` must always be nonempty and
valid. An empty guard never acts as a wildcard and therefore rejects a unit
whose frozen locator is nonempty.
Intake validates the complete active overlay before applying any row; a stale
raw-page guard or invalid evidence makes the application atomic and fail-closed.
The overlay changes neither the frozen manifest bytes nor any stable unit ID.

A foreign-volume page marker that begins an appended errata section remains
the active witness locator for that section. A foreign-volume marker entered
from the body page inside one statement is instead statement-scoped: it binds
retroactively to that whole statement and the enclosing body page is restored
at the matching environment end. Exact regression rows prevent either form
from contaminating the other.

Topic IDs use `ega-topic-<slug>`. Local Stacks labels may be recorded as
evidence, but this branch never writes or claims an official Stacks tag.

Decision, issue, feedback, statement-edge, residual, page-locator, visual-QA,
source-error-receipt, and agent-run IDs use zero-padded `D`, `I`, `F`, `S`,
`R`, `L`, `V`, `Q`, and `A` prefixes.
Rows are append-only. A correction names the earlier row in `supersedes`; it
does not rewrite history.

`rej.csv` retains failed or obsolete per-item visual crops under stable `J`
identifiers. Every row binds one exact parent PDF page and point box to a
CRC-clean crop and names the active same-item `V` successor. A below-5000-dpi
locator artifact is admissible only as `rejected` evidence with an explicit
below-floor reason; it can never satisfy the active `V` gate. Rejected and
accepted evidence may share neither a path nor bytes. The validator requires
manifest-directory closure so later success cannot erase a clipped or
nonfinal witness from the audit history.

Governance ledgers are parsed fail-closed: an unexpected CSV header yields no
admitted rows, and `V` and `J` identifiers must pass their exact structured
zero-padded grammar before any numeric operation. Accepted crop directories,
like the rejected and source-error directories, must be nonempty flat
directories containing only regular nonsymlink files. Parent-page dimensions
are authority metadata, not values a row may declare for itself.

The current complete `V`, `J`, `L`, and `Q` ledgers and the sealed prefixes of
the decision, issue, and findings ledgers have exact LF-normalized byte and
SHA-256 pins in `scope.json`. These pins freeze the stated historical rows but
do not freeze each file: later rows remain append-only successors after the
pinned prefix. Evidence promotion requires an exact active decision contract
(subject, action, state, and evidence), and each `Q` receipt must join one
specific finding object whose own evidence contains that receipt ID, crop
path, and crop hash; tokens split across findings never satisfy the join.
The sole immutable legacy exception is `Q000001`: its named original finding
must remain present, while the separately published append-only companion
`EGA-I-4.2.3-P123-GAMMA-PSI-CROP-RECEIPT` alone must carry all three exact
receipt tokens. This explicit two-object lineage cannot be inferred for later
rows.

For `smap.csv` and `resid.csv`, `supersedes` is the final column so legacy
rows without a serialized trailing field remain byte-stable and are read as
blank. A successor must point to one strictly earlier row in the same table;
one row may have at most one direct successor. Validation checks every
historical row but computes review and residual snapshots from the
unsuperseded active view. The snapshot records active rows, physical file
rows, and superseded rows separately. New rows must serialize the final field
even when blank; legacy rows may omit only that final blank. The validator
rejects overflow fields and whitespace-normalized identifiers. For a pure
source-unit attribution correction, every field other than stable row ID,
source unit, decision, and supersession link remains byte-semantically equal.
The published legacy prefixes are hash-pinned before successors are read.
Stable S/R identifiers are contiguous in physical append order, so a newly
appended low or reused identifier cannot evade the explicit-final-field gate.
Decision supersession links use the same prior-row and single-successor rules.
The historical `issues.csv` field is a mixed namespace: a `D` value names the
linked controlling decision while an `I` value supersedes one strictly prior
issue and may not branch. Named governance repairs have exact regressions.

## Authority states

- `english_discovery`: complete English text supports search and candidates.
- `french_admitted`: the diplomatic French unit has a sealed authority receipt.
- `source_corrected`: a separate justified correction exists.
- `source_disputed`: the source claim or reading remains fail-closed.

English discovery may create candidates at any point. Only `french_admitted`
or an exact published authority can support a canonical source claim.

## Review states

- `unreviewed`: search topic or source unit only.
- `candidate`: plausible Stacks correspondence with recorded evidence.
- `reviewed_existing`: equivalent, stronger, weaker, or split treatment found.
- `reviewed_gap`: bounded gap established by mathematical review.
- `integrated_local`: independent Stacks-convention exposition exists locally.
- `built`: every affected chapter passes its bounded build gate.
- `remote_checkpoint`: exact branch bytes are pushed and remotely verified.
- `upstream_feedback`: upstream comment is recorded and dispositioned.
- `upstream_accepted`: upstream merged or explicitly accepted the material.

Build success never promotes mathematical review state by itself.

`tmap.csv` records bounded reviewed correspondences. Its granularity and
coverage columns are part of the claim: a `source_subsection_to_stacks_section`
row with `topical_overlap_only` establishes only a topic-level bridge. It does
not establish theorem equivalence or complete coverage of the source
subsection. Existing official tags in that table are read back from the fixed
upstream `tags/tags`; the scaffold assigns no tags.

`smap.csv` records statement or statement-component edges. Existing targets
must resolve to the fixed upstream commit and exact `tags/tags` join. A local
integration uses `LOCAL_WORKTREE`, must leave `official_tag` empty, and cannot
be reported as upstream acceptance. Multiple edges may share a source unit;
`resid.csv` records every known remainder that prevents a misleading
single-edge completeness claim.

Relations are measured from the source unit toward the target. Extra clauses
in a target do not make the source only `partial`: use `merged` when Stacks
absorbs the whole source with neighboring material and `entailed_by_stronger`
when a genuinely stronger target implies the whole source. Use `partial` only
when some mathematical part of the source remains uncovered by that edge.

`agent.csv` records the task identity, model/effort when exposed, exact bounded
scope, status/runtime, returned result, owner verification, accepted or
rejected disposition, and write claim. Agent output is evidence only; it
cannot promote authority or mathematical review state.

An exposed Spark run records its actual effort as `low`, `medium`, `high`, or
`xhigh`; it may not use `inherited`. A task run by an inherited parent model
records both `inherited-parent` and `inherited`. These enums describe observed
execution provenance and must never be upgraded after the run merely to pass a
validator.

The write claim is either the literal `none` or a sorted pipe-delimited list
of repository-relative paths actually changed by that bounded task. The owner
must inspect every claimed path; a write claim never expands task authority or
substitutes for review of the resulting bytes.

One task path may appear in more than one row when a later follow-up receives
a genuinely different bounded scope. The task-path and scope pair is unique.
Nested agent paths are retained exactly. Official-target claims from an agent
must be replayed against `git show` at the pinned upstream commit and the exact
full-label join in `tags/tags`; an uncommitted worktree label is never evidence
that the target already exists upstream.

## Feedback integration

`fb.csv` records the immutable URL, source, date, affected stable ID, and
disposition of each upstream comment. Any resulting change receives a new
decision row. Rejected or deferred feedback remains visible. This lets the
scaffold absorb maintainer guidance without rekeying the corpus graph.

## Promotion gate

A source unit can modify a Stacks chapter only when it has:

1. stable source identity and exact authority evidence;
2. an explicit correspondence state (existing, stronger, weaker, split, gap,
   historical, false, or unsupported);
3. a reviewed mathematical rationale and dependencies;
4. append-only issue and correction closure;
5. an active certified `V` row when the claim involves a diagram or selected
   intricate standalone mathematical block;
6. bounded build and rendered-page checks for affected output.
