# -*- coding: utf-8 -*-
"""
option_pricing_pkg

Split from the original single-file Colab export
(option_pricing___greeks_calculator.py) with no logic changes.

Modules:
    models      - black_scholes_price, monte_carlo_price, binomial_tree_price
    greeks      - greeks_fdm, greeks_fdm_cf
    reports     - price_report_with_vanilla, greek_report_with_vanilla
    structuring - structuring_note_*, print_note_summary
"""

from .models import (
    black_scholes_price,
    monte_carlo_price,
    binomial_tree_price,
)
from .greeks import (
    greeks_fdm,
    greeks_fdm_cf,
)
from .reports import (
    price_report_with_vanilla,
    greek_report_with_vanilla,
)
from .structuring import (
    structuring_note_with_vanilla,
    structuring_note_bull_call_spread,
    structuring_note_straddle,
    structuring_note_bull_strangle,
    print_note_summary,
)

__all__ = [
    "black_scholes_price",
    "monte_carlo_price",
    "binomial_tree_price",
    "greeks_fdm",
    "greeks_fdm_cf",
    "price_report_with_vanilla",
    "greek_report_with_vanilla",
    "structuring_note_with_vanilla",
    "structuring_note_bull_call_spread",
    "structuring_note_straddle",
    "structuring_note_bull_strangle",
    "print_note_summary",
]
