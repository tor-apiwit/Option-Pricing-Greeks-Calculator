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

## Critical Known Issues
1. **Binomial Tree Formula **: `binomial_tree_price()` calculates Up/Down factors incorrectly by subtracting 1 (`u = np.exp(...) - 1`). This violates standard no-arbitrage models and severely distorts Gamma and Vega results.
