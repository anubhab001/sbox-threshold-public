
This repository contains the accompanying codes for the paper: **"From Substitution Box To Threshold"** ([IACR ePrint](https://eprint.iacr.org/2023/633)/[Indocrypt 2023](https://crsind.in/indocrypt2023/)).

# Contents

<!--## Directory Structure-->
```
.
│   README.md
│
├───with-decomposition
│       decomposition.py
│       README.md
│       sample_decomp_log.txt
│
└───without-decomposition
        default-ls.txt
        no-decomposition.py
        README.md
        sample_wo_decomp_log.txt
        uniformity-table-generator.py

```
<!--
## README Files

* [Threshold with SBox Decomposition](./with-decomposition/README.md)
* [Threshold without SBox Decomposition](./without-decomposition/README.md)
-->
# Dependency
All the codes are written for/tested with [Sage 9.3](https://www.sagemath.org/), no other library is used. It (`.py` extension) can be run from the terminal from inside REPL ("`load(<filename>)`") or outside REPL (`"sage <filename>"`).

<!--
# Example of distribution of monomials (no decomposition) with DEFAULT-LS SBox
An example with the quadratic DEFAULT-LS SBox (`037ED4A9CF18B265`) is given below for first threshold order (i.e., 3-sharing). Each $y_{\cdot,j}$ variable is missing $x_{\cdot, j}$ for $j=0,1,2$; thereby satisfying the non-completeness condition.
```
y0_0 = x0_1 + x1_2 + x2_2
y0_1 = x0_2 + x1_0 + x2_0
y0_2 = x0_0 + x1_1 + x2_1

y1_0 = x0_1*x1_2 + x0_1*x2_1 + x0_1*x2_2 + x0_2*x1_1 + x0_2*x1_2 + x0_2*x2_1 + x0_2 + x1_1*x3_2 + x1_2*x3_1 + x2_1*x3_2 + x2_2*x3_1 + x2_2*x3_2
y1_1 = x0_0*x1_0 + x0_0*x1_2 + x0_0*x2_2 + x0_2*x1_0 + x0_2*x2_0 + x0_2*x2_2 + x1_0*x3_2 + x1_0 + x1_2*x3_0 + x1_2*x3_2 + x1_2 + x2_0*x3_2 + x2_2*x3_0
y1_2 = x0_0*x1_1 + x0_0*x2_0 + x0_0*x2_1 + x0_0 + x0_1*x1_0 + x0_1*x1_1 + x0_1*x2_0 + x0_1 + x1_0*x3_0 + x1_0*x3_1 + x1_1*x3_0 + x1_1*x3_1 + x1_1 + x2_0*x3_0 + x2_0*x3_1 + x2_1*x3_0 + x2_1*x3_1

y2_0 = x1_1 + x2_1 + x2_2
y2_1 = x1_2 + x2_0 + x3_2
y2_2 = x1_0 + x3_0 + x3_1

y3_0 = x0_1*x1_1 + x0_1*x1_2 + x0_1*x2_2 + x0_2*x1_1 + x0_2*x1_2 + x0_2*x2_1 + x0_2*x2_2 + x1_1*x3_1 + x1_1*x3_2 + x1_2*x3_1 + x2_1*x3_2 + x2_1 + x2_2*x3_1 + x2_2
y3_1 = x0_0*x1_2 + x0_0*x2_2 + x0_2*x1_0 + x0_2*x2_0 + x1_0*x3_0 + x1_0*x3_2 + x1_2*x3_0 + x1_2*x3_2 + x2_0*x3_2 + x2_0 + x2_2*x3_0 + x2_2*x3_2 + x3_2
y3_2 = x0_0*x1_0 + x0_0*x1_1 + x0_0*x2_0 + x0_0*x2_1 + x0_1*x1_0 + x0_1*x2_0 + x0_1*x2_1 + x1_0*x3_1 + x1_1*x3_0 + x2_0*x3_0 + x2_0*x3_1 + x2_1*x3_0 + x2_1*x3_1 + x3_0 + x3_1

```
-->