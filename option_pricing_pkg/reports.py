# -*- coding: utf-8 -*-
"""
reports.py

Comparative reporting utilities that benchmark the three pricing models
against each other, and analytical Greeks against FDM-estimated Greeks.

Split out from the original Colab notebook
(option_pricing___greeks_calculator.py) with no logic changes.

NOTE: price_report_with_vanilla() calls the bare display() function, which
only exists in Jupyter/Colab/IPython environments. Running this in a plain
Python interpreter or terminal will raise NameError: name 'display' is not
defined. This is preserved as-is from the original notebook.
"""

import pandas as pd

from .models import black_scholes_price, monte_carlo_price, binomial_tree_price
from .greeks import greeks_fdm, greeks_fdm_cf


def price_report_with_vanilla(S, K, T, r, sigma, option_type):
    """
    Generates a comparative pricing report for a vanilla European option
    across three different quantitative models: Black-Scholes, Monte Carlo,
    and the Binomial Tree.

    Outputs a formatted Pandas DataFrame to the display environment.

    Parameters:
    -----------
    S : float
        Current spot price of the underlying asset.
    K : float
        Strike price of the option contract.
    T : float
        Time to maturity in years.
    r : float
        Annualized continuously compounded risk-free interest rate.
    sigma : float
        Annualized volatility of the underlying asset's returns.
    option_type : str
        The type of option contract: "call" or "put".

    Dependencies:
    -------------
    Requires `pandas` as `pd` and a Jupyter notebook/IPython environment for `display()`.
    """
    # 1. Execute pricing routines across all engines
    price_bs = black_scholes_price(S, K, T, r, sigma, option_type)
    price_mc = monte_carlo_price(S, K, T, r, sigma, option_type)
    price_bt = binomial_tree_price(S, K, T, r, sigma, option_type)

    # 2. Consolidate premiums into a comparative DataFrame
    model = ["Black-Scholes", "Monte Carlo", "Binomial Tree"]
    price_table = pd.DataFrame({
        "Price": [price_bs, price_mc, price_bt]
    }, index=model).round(2)

    # 3. Output results
    print(f"The Price of {option_type.capitalize()} option")
    print(price_table)


def greek_report_with_vanilla(S, K, T, r, sigma, option_type):
    """
    Generates a comprehensive benchmarking report comparing option Greeks
    calculated analytically via Closed-Form solutions against numerical
    Finite Difference Method (FDM) implementations.

    CRITICAL NOTE FOR CODE REVIEWERS:
    ---------------------------------
    - The 'Monte Carlo (FDM)' outputs will exhibit massive variance/noise
      unless the underlying engine locks paths using Common Random Numbers (CRN).
    - The 'Binomial Tree' row reflects FDM shocks on a single-period model,
      causing visible tracking errors against the analytical benchmark.

    Parameters:
    -----------
    S : float
        Current spot price of the underlying asset.
    K : float
        Strike price of the option contract.
    T : float
        Time to maturity in years.
    r : float
        Annualized continuously compounded risk-free interest rate.
    sigma : float
        Annualized volatility of the underlying asset's returns.
    option_type : str
        The type of option contract: "call" or "put".
    """
    # 1. Extract exact analytical Greeks from the Closed-Form Black-Scholes solution
    delta_cf, gamma_cf, vega_cf, theta_cf, rho_cf = greeks_fdm_cf(S, K, T, r, sigma, option_type)

    # 2. Extract numerical Greeks via analytical Black-Scholes FDM
    delta_fdm_bs, gamma_fdm_bs, vega_fdm_bs, theta_fdm_bs, rho_fdm_bs = greeks_fdm(black_scholes_price, S, K, T, r, sigma, option_type)

    # 3. Extract numerical Greeks via Monte Carlo Simulation FDM
    delta_fdm_mc, gamma_fdm_mc, vega_fdm_mc, theta_fdm_mc, rho_fdm_mc = greeks_fdm(monte_carlo_price, S, K, T, r, sigma, option_type)

    # 4. Extract numerical Greeks via Binomial Tree FDM
    delta_fdm_bt, gamma_fdm_bt, vega_fdm_bt, theta_fdm_bt, rho_fdm_bt = greeks_fdm(binomial_tree_price, S, K, T, r, sigma, option_type)

    # 5. Build structured comparative matrix using Pandas
    methods = ["Closed-Form (Analytical)", "FDM (Black-Scholes)", "Monte Carlo (FDM)", "Binomial Tree"]
    greek_table = pd.DataFrame({
        "Delta": [delta_cf, delta_fdm_bs, delta_fdm_mc, delta_fdm_bt],
        "Gamma": [gamma_cf, gamma_fdm_bs, gamma_fdm_mc, gamma_fdm_bt],
        "Vega":  [vega_cf,  vega_fdm_bs,  vega_fdm_mc,  vega_fdm_bt],
        "Theta": [theta_cf, theta_fdm_bs, theta_fdm_mc, theta_fdm_bt],
        "Rho":   [rho_cf,   rho_fdm_bs,   rho_fdm_mc,   rho_fdm_bt],
    }, index=methods).round(6)

    # 6. Output formatted analysis report
    print(f"The Greeks of {option_type.capitalize()} option")
    print(greek_table)
    print("-" * 80)
