# R4 independent review: SITES-040

## Verdict

**ACCEPTED.** The four printed composites on `sites.tex` lines 6077, 6080,
and 6083 are ill-typed in the order printed. Reversing each composite is the
smallest correction and gives exactly the restriction maps required by the
sheaf compatibility argument.

## Frozen evidence identities

All three identities below were checked directly before review.

| Artifact | Exact path / identity | Bytes | SHA-256 | Additional identity |
|---|---|---:|---|---|
| Frozen English authority | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\upstream\src\stacks-project-a04446e57ec1fbc252a871afcec7752fb2807b14\sites.tex` | 424197 | `07AE4690C2D8EB6873837D3D14A37F07408BB14F9E0BE6077ED570C220B1845D` | Stacks commit `a04446e57ec1fbc252a871afcec7752fb2807b14`; 11860 lines as recorded by the frozen intake |
| Frozen SITES-040 intake | `<LOCAL_WORKSPACE>/03_projects\language_management\cjk\03_working_translations\stacks_cjk_20260821\canon\control\ERRATA_R4_SUPPLEMENT_SITES_040_20260822.json` | 2319 | `66AA87B72F024CCB281A4CA123DAB77EE70C5D818CB0A1FD490121298F242A5C` | Schema `stacks-english-ai-errata-intake/v1`; one hypothesis, `SITES-040` |
| Producer ledger at intake | `<LOCAL_WORKSPACE>/03_projects\language_management\romance\03_working_translations\stacks_fr_20260821\00_control\SOURCE_DEFECT_LEDGER.csv` | 70068 | `B652420336D6A50634A54FBF6535A2C455AC14AA29434BD32BC41CC5725B943D` | 171 CSV data rows (172 physical lines including the header); the directly checked live identity equals the intake-recorded identity |

The reviewed locus is `sites.tex:6072-6083`. No other source file was used to
establish the mathematical verdict.

## Exact source evidence

The local setup says that `\{V_i \to V\}` is a covering (lines 6068-6069), and
then states (lines 6072-6074)

```tex
Let $(s_i, \varphi_i)_{i \in I} \in \prod_i \mathcal{H}(V_i)$,
This means $\varphi_i : V_i \to U$ is a morphism in $\mathcal{C}$, and
$s_i \in \mathcal{G}(V_i \xrightarrow{\varphi_i} U)$.
```

For `P_{ij} = V_i \times_V V_j`, the notation in lines 6075-6083 necessarily
uses the fiber-product projections

```text
pr_1 : P_{ij} -> V_i,       pr_2 : P_{ij} -> V_j.
```

The relevant presheaf was defined in the same file at lines 5219-5226 by

```tex
V \longmapsto
\coprod\nolimits_{\varphi \in \Mor_\mathcal{C}(V, U)}
\mathcal{G}(V \xrightarrow{\varphi} U)
```

with restriction mappings. Thus restricting the summand indexed by
`\varphi_i : V_i -> U` along `pr_1 : P_{ij} -> V_i` must land in the summand
indexed by a map `P_{ij} -> U`.

The composition convention is not ambiguous. In `sites.tex:5256-5264`, the
file declares `p : X -> U` and uses `\psi : V -> X` in the typed equation
`p \circ \psi = \varphi`, where `\varphi : V -> U`. Hence `f \circ g` means
first `g`, then `f`. The local prose at lines 6086-6087 agrees: `\varphi_i` is
the composition of `V_i -> V` with `\varphi : V -> U`, i.e.
`\varphi_i = \varphi \circ (V_i -> V)`.

## Typed proof

Let `P_{ij} = V_i \times_V V_j`. The declared and canonical types are

```text
varphi_i : V_i -> U          pr_1 : P_{ij} -> V_i
varphi_j : V_j -> U          pr_2 : P_{ij} -> V_j.
```

Under the source's convention, the expressions printed at lines 6077 and 6080
would require the following interfaces:

```text
pr_1 o varphi_i : V_i -> ?   requires cod(varphi_i) = dom(pr_1), i.e. U = P_{ij}
pr_2 o varphi_j : V_j -> ?   requires cod(varphi_j) = dom(pr_2), i.e. U = P_{ij}
```

No such object identities are assumed; the lemma is for an arbitrary site,
object `U`, object `V`, and covering. Therefore these composites are not
defined in general. Consequently, the equality printed at line 6083 is also
an equality between undefined expressions and cannot express Cech
compatibility.

Reversing the factors produces the required maps:

```text
varphi_i o pr_1 : P_{ij} -> V_i -> U,
varphi_j o pr_2 : P_{ij} -> V_j -> U.
```

They have a common domain and codomain, so their equality is well-typed and is
precisely the descent condition used in lines 6084-6087 to obtain the unique
`\varphi : V -> U`.

## Adverse-evidence check

The strongest reading against admission is that the intended maps are obvious
from the prose and the lemma remains mathematically recoverable. That makes
the defect a readily repaired notation error, but it does not make the printed
formulas valid. A reversed convention for `\circ` would rescue the four local
strings, but is ruled out by the typed `p \circ \psi = \varphi` example in the
same file and by lines 6086-6087. Nor can `\text{pr}_1` and `\text{pr}_2` be
maps out of `V_i` and `V_j`: in the stated restriction to
`V_i \times_V V_j`, they are the two canonical projections from that fiber
product. No adverse evidence defeats the source-defect claim.

## Smallest correction

Change only the four composite expressions on the three cited lines:

```text
sites.tex:6077  \text{pr}_1 \circ \varphi_i  ->  \varphi_i \circ \text{pr}_1
sites.tex:6080  \text{pr}_2 \circ \varphi_j  ->  \varphi_j \circ \text{pr}_2
sites.tex:6083  \text{pr}_1 \circ \varphi_i  ->  \varphi_i \circ \text{pr}_1
sites.tex:6083  \text{pr}_2 \circ \varphi_j  ->  \varphi_j \circ \text{pr}_2
```

No surrounding prose, notation, or mathematical structure needs to change.

## Adjacent punctuation notice (unnumbered)

At `sites.tex:6072`, the sentence ending after
`\prod_i \mathcal{H}(V_i)$` has a comma immediately before the new sentence
`This means ...`. The comma should be a period. This is noted without assigning
an erratum ID and is excluded from the SITES-040 verdict and aggregate.

## Aggregate

| Reviewed | Accepted | Rejected | Deferred |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 |

Aggregate terminal disposition: **SITES-040 ACCEPTED**. The one unnumbered
adjacent punctuation notice is not counted as a reviewed candidate.
