# Option Pricing & Structuring Package

Split from the original single-file Colab export (`option_pricing___greeks_calculator.py`) into a proper package structure.

## Structure
```text
option_pricing_pkg/
├── __init__.py       # Re-exports all public functions
├── models.py         # Option pricing models (Black-Scholes, Monte Carlo, Binomial Tree)
├── greeks.py         # Greeks calculation (Numerical FDM & Closed-form)
├── reports.py        # Comparative reporting utilities
├── structuring.py    # Principal-protected structured note builders
└── main.py           # Entry point / Execution script
```

## Installation
Ensure you have the required dependencies installed:
```bash
pip install -r requirements.txt
```

## Usage
Run the predefined example script:
```bash
python -m option_pricing_pkg.main
```

Or import specific functions into your project:
```python
from option_pricing_pkg import black_scholes_price
price = black_scholes_price(S=100, K=99, T=1, r=0.03, sigma=0.25, option_type="call")
```

## Critical Known Issues (Technical Debt)
*Please be aware of the following unresolved issues from the original code before utilizing this package in production:*

1. **Binomial Tree Formula Error**: `binomial_tree_price()` calculates Up/Down factors incorrectly by subtracting 1 (`u = np.exp(...) - 1`). This violates standard no-arbitrage models and severely distorts Gamma and Vega results.
2. **Environment Dependency**: `price_report_with_vanilla()` utilizes the `display()` function, which will raise a `NameError` outside of Jupyter/IPython environments.
3. **Unit Mismatch**: In `main.py`, the time horizon $T=10$ is strictly annualized, but the interest rate and volatility are divided by 12, implying a monthly basis. This mismatch skews calculations.
4. **Unused Dependency**: `yfinance` is imported as a hard dependency in `models.py` but is never executed.
