# -*- coding: utf-8 -*-
"""
models.py

Core option pricing models:
- Black-Scholes-Merton (closed-form)
- Monte Carlo simulation
- Binomial Tree (1-step)

Split out from the original Colab notebook
(option_pricing___greeks_calculator.py) with no logic changes.
"""

import numpy as np
from scipy.stats import norm
import yfinance as yf  # NOTE: imported in the original file but never used


def black_scholes_price(S, K, T, r, sigma, option_type="call"):

  """
    Calculates the theoretical price of a European option
    using the Black-Scholes-Merton model.

    Parameters:
    -----------
    S : float
        Spot price of the underlying asset.
    K : float
        Strike price of the option contract.
    T : float
        Time to maturity in years (e.g., 0.5 for 6 months).
    r : float
        Annualized continuously compounded risk-free interest rate.
    sigma : float
        Annualized volatility of the underlying asset's returns.
    option_type : str, optional
        The type of option contract: "call" or "put" (default is "call").

    Raises:
    -------
    ValueError
        If option_type is not 'call' or 'put'.
    """
  # --- 1. Calculate Probability Factors (d1 and d2) ---
  # d1 measures how far in-the-money the option is, adjusted for volatility and time.
  d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
  d2 = d1 - sigma * np.sqrt(T)

  # --- 2. Conditional Pricing and Greeks Calculation ---
  if option_type == "call":
    # Standard Black-Scholes Call Pricing Formula
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

  elif option_type == "put":
      # Standard Black-Scholes Put Pricing Formula
      price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

  else:
      raise ValueError("option_type must be 'call' or 'put'")

  return price


def monte_carlo_price(S_0, K, T, r, sigma, option_type="call"):
    """
    Prices a European option (Call or Put) using the Monte Carlo simulation method.

    This function simulates terminal stock prices under a risk-neutral measure
    based on Geometric Brownian Motion (GBM), evaluates the payoff scenarios,
    and discounts the expected payoff back to present value.

    Parameters:
    -----------
    S_0 : float
        Current asset price (Spot price at t=0).
    K : float
        Strike price of the option contract.
    T : float
        Time to maturity in years (e.g., 0.5 for 6 months).
    r : float
        Annualized continuously compounded risk-free interest rate.
    sigma : float
        Annualized volatility of the underlying asset's returns.
    option_type : str, optional
        The type of option to price. Must be either 'call' or 'put' (default is 'call').

    Returns:
    --------
    float
        The estimated fair value (present value) of the option.

    Raises:
    -------
    ValueError
        If the 'option_type' provided is not 'call' or 'put'.

    Example:
    --------
    >>> price = monte_carlo_price(100, 100, 1, 0.05, 0.2, option_type="call")
    """
    # Number of random paths to simulate for accuracy
    n_sims = 500_000

    # Generate standard normal random variables (Z ~ N(0,1))
    z_independent = np.random.standard_normal(n_sims)

    # --- 1. Simulate Terminal Stock Prices (GBM) ---
    # Calculates the log-returns according to Geometric Brownian Motion
    returns = (r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z_independent
    # Projects the final stock prices at maturity (T)
    S_T = S_0 * np.exp(returns)

    # --- 2. Evaluate Option Payoffs at Maturity ---
    if option_type == "call":
        # Call Payoff = Max(S_T - K, 0)
        payout_scenarios = np.maximum(S_T - K, 0)

    elif option_type == "put":
        # Put Payoff = Max(K - S_T, 0)
        payout_scenarios = np.maximum(K - S_T, 0)

    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # --- 3. Expectation & Discounting ---
    # Find the average payoff across all 500,000 simulated paths
    expected_payout_future = payout_scenarios.mean()

    # Discount the expected future payoff back to present value using e^(-rT)
    price = expected_payout_future * np.exp(-T * r)

    return price


def binomial_tree_price(S_0, K, T, r, sigma, option_type="call"):
    """
    Calculates the theoretical price and replication parameters of a European
    option using a 1-step (single-period) Binomial Tree model.

    This function utilizes the no-arbitrage replicating portfolio method
    (combining stock and bonds) to value the option premium.

    Parameters:
    -----------
    S_0 : float
        Current spot price of the underlying asset.
    K : float
        Strike price of the option contract.
    T : float
        Time to maturity in years (representing the length of the single period).
    r : float
        Annualized continuously compounded risk-free interest rate (used for discounting).
    sigma : float
        Annualized volatility of the underlying asset's returns.
    option_type : str, optional
        The type of option contract: "call" or "put" (default is "call").

    Returns:
    --------
    float
        The theoretical fair price (premium) of the option at time t=0.

    Raises:
    -------
    ValueError
        If option_type is not 'call' or 'put'.
    """

    # --- 1. Calculate Up and Down Return Factors ---
    # Computes percentage movements based on asset volatility and time step.
    u = np.exp(sigma * np.sqrt(T))  - 1  # Percentage increase in the "up" state
    d = np.exp(-sigma * np.sqrt(T)) - 1  # Percentage decrease in the "down" state

    # --- 2. Project Future Stock Prices ---
    # Simulates the two possible asset prices at maturity (T).
    S_u = S_0 * (1 + u)
    S_d = S_0 * (1 + d)

    # --- 3. Compute Intrinsic Option Payoffs at Maturity ---
    if option_type == "call":
        payout_u = np.maximum(S_u - K, 0)
        payout_d = np.maximum(S_d - K, 0)

    elif option_type == "put":
        payout_u = np.maximum(K - S_u, 0)
        payout_d = np.maximum(K - S_d, 0)

    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # --- 4. Portfolio Replication & Pricing ---
    # Delta (Δ): The number of shares required in the replicating portfolio to hedge risk.
    delta = (payout_u - payout_d) / (S_0 * (u - d))

    # Bond Values (B): The amount of money borrowed/lent at the risk-free rate.
    # The term (1 + r*T) acts as the linear discount factor for the single period.
    bond_values = (payout_d * (1 + u) - payout_u * (1 + d)) / ((1 + r * T) * (u - d))

    # Replicating Portfolio Price: V_0 = (Δ * S_0) + B
    # By no-arbitrage principles, the option price must equal the cost of this portfolio.
    price = (S_0 * delta) + bond_values

    return price
