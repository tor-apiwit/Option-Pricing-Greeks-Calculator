# -*- coding: utf-8 -*-
"""
main.py

Entry-point script. Runs the same hardcoded example that sat at the
bottom of the original notebook export.

Split out from the original Colab notebook
(option_pricing___greeks_calculator.py) with no logic changes, other
than wrapping it in `if __name__ == "__main__":` so importing this
package does not immediately execute this block.

Run with:
    python -m option_pricing_pkg.main
"""

import numpy as np

from .reports import greek_report_with_vanilla
from .structuring import (
    structuring_note_with_vanilla,
    structuring_note_bull_call_spread,
    structuring_note_straddle,
    structuring_note_bull_strangle,
    print_note_summary,
)


def main():
    # --- Core Inputs (Standard Annualized Basis) ---
    notional = 10000
    PR = 0.8
    S = 100
    K = 99
    T = 10
    r = 0.015 / 12
    sigma = 0.32 / np.sqrt(12)
    option_type = "call"

    for opt in ["call", "put"]:
        greek_report_with_vanilla(S, K, T, r, sigma, opt)

    # 1. Vanilla Options (Call & Put)
    for opt in ["call", "put"]:
        data = structuring_note_with_vanilla(notional, PR, S, K, T, r, sigma, opt)
        print_note_summary(f"Structuring note with {opt.capitalize()} Option", data)

    # 2. Bull Call Spread
    s1_data = structuring_note_bull_call_spread(notional, PR, S, S * 0.90, S * 1.10, T, r, sigma)
    print_note_summary("Structuring note bull call spread", s1_data)

    # 3. Straddle
    s2_data = structuring_note_straddle(notional, PR, S, K, T, r, sigma)
    print_note_summary("Structuring note straddle", s2_data)

    # 4. Bull Strangle
    s3_data = structuring_note_bull_strangle(notional, PR, S, S * 0.90, S * 1.10, T, r, sigma)
    print_note_summary("Structuring note bull strangle", s3_data)


if __name__ == "__main__":
    main()
