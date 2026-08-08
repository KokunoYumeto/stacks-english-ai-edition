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

`printed_page` names the first printed page on which the generated unit begins.
A separately generated diagram child therefore keeps its own first page even
when its parent statement began earlier. When a frozen discovery witness lacks
a page marker that direct French authority has sealed, `pages.csv` supplies an
append-only evidence overlay. Each active `L` row records the raw parsed page,
the corrected first page, the admitted receipt and page gate, and its decision.
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

Decision, issue, feedback, statement-edge, residual, page-locator, and
agent-run IDs use zero-padded `D`, `I`, `F`, `S`, `R`, `L`, and `A` prefixes.
Rows are append-only. A correction names the earlier row in `supersedes`; it
does not rewrite history.

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
5. bounded build and rendered-page checks for affected output.
