# option_pricing_pkg

Split from the original single-file Colab export
(`option_pricing___greeks_calculator.py`) into a proper package.
**No pricing/Greeks logic was changed** — every formula, variable name,
comment, and hardcoded input is copied verbatim from the source file.

## Structure

```
option_pricing_pkg/
├── __init__.py       # re-exports all public functions
├── models.py         # black_scholes_price, monte_carlo_price, binomial_tree_price
├── greeks.py         # greeks_fdm (numerical), greeks_fdm_cf (closed-form)
├── reports.py        # price_report_with_vanilla, greek_report_with_vanilla
├── structuring.py    # structuring_note_*, print_note_summary
└── main.py           # the hardcoded example block from the bottom of the
                       # original notebook, now behind `if __name__ == "__main__"`
```

## Usage

```bash
python -m option_pricing_pkg.main
```

or import individual functions:

```python
from option_pricing_pkg import black_scholes_price
black_scholes_price(S=100, K=99, T=1, r=0.03, sigma=0.25, option_type="call")
```

## Two mandatory, non-optional changes made during the split

These were not "logic fixes" — the file would not run as a multi-file
package without them:

1. **`structuring.py` now imports `numpy as np`.** In the original
   single-file script `np` was imported once at the top and shared by
   every function via one global scope. `_bond_and_budget()` calls
   `np.exp(...)` but lives in its own module now, so it needs its own
   import or it throws `NameError` on first call.
2. **`main.py` wraps the execution block in `if __name__ == "__main__":`.**
   The original script ran its example calculations immediately on
   being loaded. If any other file does
   `from option_pricing_pkg import black_scholes_price`, that must not
   also fire off five structuring-note print blocks. This guard is
   standard practice for any importable Python package.

## Known issues — intentionally NOT fixed (per user instruction)

These were flagged before the split and left untouched at the user's
explicit request. Anyone building on this package should be aware of
them before trusting the output:

1. **`binomial_tree_price()` uses the wrong up/down factors.**
   `u = np.exp(sigma * np.sqrt(T)) - 1` and
   `d = np.exp(-sigma * np.sqrt(T)) - 1` are not the standard
   Cox-Ross-Rubinstein (or any standard no-arbitrage) up/down factors —
   the `- 1` should not be there. This measurably distorts delta,
   gamma, and vega for the binomial model versus the closed-form
   Black-Scholes benchmark, especially at long maturities (the sample
   input in `main.py` uses `T = 10` years). Run
   `greek_report_with_vanilla` and compare the `Binomial Tree` row to
   `Closed-Form (Analytical)` — Gamma comes out ~0 and Vega is off by
   ~25%.
2. **`import yfinance as yf` in `models.py` is unused.** No function in
   this package calls it. It's a leftover from an earlier draft that
   pulled live market data. Kept as-is; means `yfinance` is a hard
   dependency of this package for no functional reason.
3. **`price_report_with_vanilla()` calls a bare `display()`.** That
   function only exists in Jupyter/Colab/IPython. Calling it from a
   plain `python` script or `main.py` raises
   `NameError: name 'display' is not defined`. Not called from
   `main.py`, so the package runs fine — but this function will break
   for anyone who imports and calls it outside a notebook.
4. **Input assumption worth double-checking**: in `main.py`,
   `r = 0.015/12` and `sigma = 0.32/np.sqrt(12)` alongside `T = 10`
   (years, per every docstring). If `0.015` and `0.32` are already
   *annualized* figures, dividing by `12`/`sqrt(12)` converts them to a
   *monthly* basis while `T` is still expressed in years — that's a
   unit mismatch between rate/vol and time horizon. Worth confirming
   against wherever these numbers originally came from.
