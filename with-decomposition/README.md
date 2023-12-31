# Decomposition
* [`decomposition.py`](./with-decomposition/decomposition.py): Code to find decomposition of a given 4-bit (cubic) SBox into 2 or more (quadratic) SBoxes.

    Options/Parameters: 

    * `target_sbx` (at or near line 128, default: `SKINNY_SBOX`): Target SBox in [`sage.crypto.sbox.SBox`](https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/sbox.html) format; currently `PRESENT_SBOX` (defined at or near line 123), `SKINNY_SBOX` (defined at or near line 124) and `GIFT_SBOX` (defined at or near line 125) are included from [`sage.crypto.sboxes`](https://doc.sagemath.org/html/en/reference/cryptography/sage/crypto/sboxes.html).
    * `count` (at or near line 132, default: `1`): Number of decompositions requested. 
    * `order` (at or near line 132, default: `2`): Order of decomposition (e.g., setting it to `3` would find $F_2, F_1, F_0$).
    * `ineq_type` (at or near line 132, default: `"<"`, non-default option: `"<="`): Constraint that the algebraic degree of the SBoxes in the composition is to satisfy. 
    * `base_in` (at or near line 132, default: `None`): Any other base class from which affine equivalent SBoxes can be supplied; when set to default `None`, the 6 quadratic classes are used: 4 (`0123456789ABDCFE`), 12 (`0123456789CDEFAB`), 293 (`0123457689CDEFBA`), 294 (`0123456789BAEFDC`), 299 (`012345678ACEB9FD`) and 300 (`0123458967CDEFAB`).
    * `log` (at or near line 132, default: `"decomp_log.txt"` in `"a+"` mode): File used for logging.

* [`sample_decomp_log.txt`](./with-decomposition/sample_decomp_log.txt): Sample log file generated by [`decomposition.py`](./with-decomposition/decomposition.py).
