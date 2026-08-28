# R28 Smoothing supersession proof

This candidate corrects the already-admitted R26 unit `MC-STK-ERR-1183`. It does not mutate R26 and does not re-admit producer row `SMOOTHING-026`.

Put

\[
S=(R/\pi^2R)[x_1,\ldots,x_n],\qquad
M=\bar I/\bar I_k,\qquad a=a_k,
\qquad c=a^N+b_k.
\]

The printed proof chooses (b_k/a^N\in\bar I_a) so that

\[
u=1+\frac{b_k}{a^N}=\frac{c}{a^N}
\]

annihilates (M_a). R26 replaced (a) by (c). That only preserves the principal open after passage to \(\operatorname{Spec}(\bar C)\), because (c\equiv a^N\pmod{\bar I}). It does not prove (M_c=0) in the ambient polynomial ring.

A counterexample is

\[
S=k[a,x],\qquad f_1=a(a+x)x,\qquad f_2=x,
\qquad I=(f_1,f_2)=(x),\qquad I_k=(f_1).
\]

On (D(a)), the class of (f_1) freely generates (I/I^2). Taking (N=1) and (b=x), the element (1+x/a) annihilates ((I/I_k)_a). But for (c=a+x), localization at the prime ((a)) gives (I_{(a)}=S_{(a)}) and ((I_k)_{(a)}=aS_{(a)}), while (c) is a unit. Thus (M_c\ne0).

The minimal robust replacement is

```tex
After replacing $a_k$ by $a_k((a_k)^N + b_k)$ we get
```

Indeed, with (d=ac), localization at (d) makes both (a) and (c) invertible. Hence (u=c/a^N) is an annihilating unit on (M_d), so (M_d=0) and

\[
(\bar I_k)_d=(\bar I)_d.
\]

Since (b_k\in I), the image of (d) in \(\bar C\) is (a^{N+1}). Therefore (D_{\operatorname{Spec}(\bar C)}(d)=D_{\operatorname{Spec}(\bar C)}(a)), so the smooth-locus cover remains unchanged.

Composition must replace the exact R26 effective fragment `$(a_k)^N + b_k$` in the bound cumulative source. The isolated R28 payload is a projection from the official frozen authority and must not be copied wholesale into the cumulative English tree.
