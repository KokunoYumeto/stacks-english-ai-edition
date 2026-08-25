# Independent canon review: R4 SITES-057--064

Review date: 2026-08-22 (Europe/Berlin)

## Scope and frozen identities

This review is limited to the eight hypotheses SITES-057 through SITES-064. I read the supplement in full and reopened the cited loci and controlling local definitions in the exact frozen `sites.tex`. No source, translation, overlay, registry, or other control file was changed.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `ERRATA_R4_SUPPLEMENT_SITES_057_064_20260822.json` | 5,904 | `94ef2aedbf70f27a595139eb965254289e880953d831c6efd8562c37b5ac3bb3` |
| frozen `sites.tex` at commit `a04446e57ec1fbc252a871afcec7752fb2807b14` | 424,197 | `07ae4690c2d8eb6873837d3d14a37f07408bb14f9e0be6077ed570c220b1845d` |

The recomputed `sites.tex` byte count and digest agree with the authority identity embedded in the supplement.

## Aggregate decision

| Decision | Count | Candidates |
|---|---:|---|
| **ACCEPTED** | 7 | SITES-057, SITES-058, SITES-059, SITES-060, SITES-061, SITES-062, SITES-064 |
| **REJECTED** | 1 | SITES-063 |
| **DEFERRED** | 0 | none |

SITES-063 is a harmless source-style inconsistency: `\mathcal{C'}` and `\mathcal{C}'` produce the same mathematical notation. It does not warrant an erratum overlay. Every accepted item has a local one-token, one-expression, or one-sentence repair and requires no broader rewrite.

## Candidate findings

### SITES-057 — ACCEPTED

**Frozen locus:** lines 6818--6867, especially 6820--6825 and 6864--6866.

The limit is indexed by pairs `(U', \psi)` with `\psi : u(U') \to u(U)`. The proof itself identifies the distinguished final object as `(U, \text{id})` at line 6822 and says that a compatible family is determined by its `(U, \text{id})` component at line 6825. Therefore the prescribed value at the end of the existence argument must be

```tex
s_{(U, \text{id})} = s.
```

The frozen `s_{(U, \psi)} = s` is not rescued by the generic `\psi` introduced earlier: that map has domain `u(U')`, so it does not in general even index a pair whose first component is `U`. When `U'=U`, a nonidentity endomorphism `\psi` still denotes a different component and need not evaluate to `s`.

**Smallest repair:** replace only `\psi` by `\text{id}` in line 6866.

### SITES-058 — ACCEPTED

**Frozen locus:** lines 7652--7673, controlled by `lemma-localize-morphism` at lines 6265--6289 and `lemma-localize-compare` at lines 7517--7529.

Here `u : \mathcal{D} \to \mathcal{C}`, `V` is an object of `\mathcal{D}`, and line 7657 identifies `\mathcal{F}` with `h_{u(V)}`. Consequently the object at which the site `\mathcal{C}` is localized is `u(V)`. Yet the proof uses `\mathcal{C}/U`, `j_U`, and `j_U^{-1}` without ever binding `U` in this proof.

The cited localization lemma explicitly makes the binding `U=u(V)` before forming `\mathcal{C}/U`. A variable local to that lemma is not silently bound merely by citing it. Replacing all three uses by `u(V)` would type-check, but is a larger and less readable repair.

**Smallest repair:** insert `Set $U = u(V)$.` immediately after line 7658.

### SITES-059 — ACCEPTED

**Frozen locus:** lines 7706--7727, controlled directly by `lemma-localize-morphism-topoi` at lines 7625--7646.

The declarations give

```tex
\mathcal{G} \in \Sh(\mathcal{D}),
\qquad
\mathcal{F} \in \Sh(\mathcal{C}).
```

The localized morphism from the controlling lemma has type

```tex
f' : \Sh(\mathcal{C})/f^{-1}\mathcal{G}
     \longrightarrow \Sh(\mathcal{D})/\mathcal{G}.
```

Thus the frozen codomain `\Sh(\mathcal{D})/\mathcal{F}` is not merely the wrong slice: it is ill-typed because `\mathcal{F}` is not an object of `\Sh(\mathcal{D})`. The displayed square at lines 7714--7718 and the phrase “as in” the controlling lemma eliminate any alternative directional reading.

**Smallest repair:** replace `\mathcal{F}` by `\mathcal{G}` at line 7725.

### SITES-060 — ACCEPTED

**Frozen locus:** lines 7788--7801, controlled by `lemma-pullback-representable-sheaf` at lines 2618--2629.

For `u : \mathcal{D} \to \mathcal{C}`, the controlling lemma gives

```tex
f^{-1}h_V^\# = h_{u(V)}^\#.
```

The hypothesis in the reviewed lemma is only a morphism `c : U \to u(V)`. By Yoneda followed by sheafification, it induces the map

```tex
h_U^\# \longrightarrow h_{u(V)}^\# = f^{-1}h_V^\#
```

used correctly on the following line; it does not identify its source and target.

There is a direct counterexample to the asserted equality. Give the arrow category `0 \to 1` the trivial topology, take the identity morphism of sites, and let `c:0\to1`. All presheaves are sheaves, while `h_0(1)=\varnothing` and `h_1(1)=\{\mathrm{id}_1\}`. Hence `h_0` and `h_1` are not equal or isomorphic. The adverse reading that the equals sign means “identified via `c`” fails: an arbitrary map supplies a morphism, not an identification, and no isomorphism hypothesis is present.

**Smallest repair:** delete only `= f^{-1}h_V^\#` from line 7793. The map `s` in line 7794 then states exactly the needed relationship.

### SITES-061 — ACCEPTED

**Frozen locus:** lines 6768--6772.

No primary SGA 4 file was present in the bounded local project search, so I checked the cited proposition against the read-only combined primary text: [M. Artin, A. Grothendieck, and J.-L. Verdier, *Théorie des topos et cohomologie étale des schémas*, Tomes 1 à 3](https://www.normalesup.org/~forgogozo/SGA4/tomes/SGA4.pdf). Its table of contents and the internal page 153 heading identify **Exposé IV, Topos**; Proposition 4.9.4 appears in that exposé on internal page 180 (PDF pages 160 and 187 respectively in the combined file).

This is primary-text evidence for Exposé IV, not Exposé III. The later frozen reference at lines 7142--7146 independently agrees, citing Proposition 4.9.4 and Remarque 4.7.4 in Exposé IV. A loose “compare with” reading does not save the numeral III because the proposition number names a definite locus in the cited work.

**Smallest repair:** replace `Expos\'e III` by `Expos\'e IV` at line 6771.

### SITES-062 — ACCEPTED

**Frozen locus:** lines 7111--7126.

The proof announces an inductively defined chain and immediately defines `\mathcal{C}_{n+1}` from `\mathcal{C}_n`. Its first displayed terms must therefore be

```tex
\mathcal{C}_1 \subset \mathcal{C}_2 \subset \mathcal{C}_3 \subset \ldots
```

Repeating `\mathcal{C}_2` can be read as a vacuously true redundant inclusion if `\subset` is non-strict, but that adverse reading defeats the displayed enumeration and is incompatible with the indexed recurrence which follows. The issue is visible in output and is not merely source style.

**Smallest repair:** replace the second `\mathcal{C}_2` by `\mathcal{C}_3` at line 7119.

### SITES-063 — REJECTED

**Frozen loci:** lines 7132 and 7187--7189.

The canonical category name is written `\mathcal{C}'` elsewhere, whereas two functor codomains use `\mathcal{C'}`. This is a source-spelling inconsistency, but not a mathematical or rendered-output defect. In TeX math mode, the prime inside `\mathcal{C'}` is parsed as the superscript prime on the calligraphic `C`; moving it just outside the math-alphabet argument leaves the same calligraphic-C-with-prime output. The prime glyph is not changed into a calligraphic character.

A source-normalization or parser-consistency policy could prefer `\mathcal{C}'`, but no such preference makes the frozen statement false, ambiguous, ill-typed, or visually different. Under the frozen-authority/erratum standard, admitting an overlay would create change without a material correction.

**Repair decision:** none. Retain the frozen source. The proposed two replacements are harmless optional style normalization only, not an accepted R4 erratum.

### SITES-064 — ACCEPTED

**Frozen locus:** lines 6953--6968.

The exact domains are:

```tex
c       : u(U'')       \longrightarrow u(U'),
f_i     : U_i''        \longrightarrow U'',
f_{ik}  : U_{ik}''     \longrightarrow U_i'',
c_{ik}  = c_i \circ f_{ik} : U_{ik}'' \longrightarrow U'.
```

Line 6958 gives `u(c_i)=c\circ u(f_i)`. Functoriality therefore forces

```tex
u(c_{ik})
= u(c_i) \circ u(f_{ik})
= c \circ u(f_i) \circ u(f_{ik})
= c \circ u(f_i \circ f_{ik}).
```

The frozen `c \circ u(f_{ik})` is ill-typed: `u(f_{ik})` lands in `u(U_i'')`, whereas the domain of `c` is `u(U'')`. There is no suppressed redefinition of `f_{ik}`; line 6963 fixes its codomain as `U_i''`, and line 6965 explicitly uses the composite `f_i\circ f_{ik}` for the covering of `U''`.

**Smallest repair:** replace `u(f_{ik})` by `u(f_i \circ f_{ik})` at line 6966.

## Closure

The eight hypotheses are fully decided: seven are established from the frozen local definitions (with SITES-061 additionally established from the cited primary work), one is defeated as an output-no-op, and none requires deferral. The accepted repairs above are the smallest semantically complete changes; this review does not itself authorize or apply them to any source or overlay.
