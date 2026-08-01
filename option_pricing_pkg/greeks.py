# -*- coding: utf-8 -*-
"""
greeks.py

Option Greeks calculation:
- greeks_fdm     : Finite Difference Method (works with any pricing model function)
- greeks_fdm_cf  : Closed-form analytical Greeks (Black-Scholes only)

Split out from the original Colab notebook
(option_pricing___greeks_calculator.py) with no logic changes.
"""

import numpy as np
from scipy.stats import norm


def greeks_fdm(model, S_0, K, T, r, sigma, option_type):
    """
    Estimates the option Greeks using the Finite Difference Method (FDM)
    by perturbing inputs via the Model pricing function.

    This function applies numerical differentiation (Central and Central-Second
    Difference schemes) to approximate partial derivatives, serving as a
    validation tool or alternative to exact analytical solutions.

    Parameters:
    -----------
    S_0 : float
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

    Returns:
    --------
    tuple of floats
        (delta, gamma, vega, theta, rho) calculated via numerical approximations.
    """

    # --- Define Perturbation Steps (Shocks) ---
    h_S = 0.01 * S_0   # 1% shift in underlying asset price
    h_sigma = 0.01     # 1% absolute shift in volatility (0.01 = 1 percentage point)
    h_r = 0.001        # 0.1% absolute shift in interest rate (10 basis points)

    # =========================================================================
    # 1. Delta & Gamma (Asset Price Sensitivities)
    # =========================================================================
    # Shift stock price up, down, and capture baseline price
    V_S_plus = model(S_0 + h_S, K, T, r, sigma, option_type)
    V_S_minus = model(S_0 - h_S, K, T, r, sigma, option_type)
    V_base = model(S_0, K, T, r, sigma, option_type)

    # Delta (First Derivative): Central Difference Scheme
    delta = (V_S_plus - V_S_minus) / (2 * h_S)

    # Gamma (Second Derivative): Central Second Difference Scheme
    gamma = (V_S_plus - 2 * V_base + V_S_minus) / (h_S ** 2)

    # =========================================================================
    # 2. Vega (Volatility Sensitivity)
    # =========================================================================
    # Shift volatility up and down
    V_sigma_plus = model(S_0, K, T, r, sigma + h_sigma, option_type)
    V_sigma_minus = model(S_0, K, T, r, sigma - h_sigma, option_type)

    # Vega (First Derivative): Central Difference Scheme
    vega = (V_sigma_plus - V_sigma_minus) / (2 * h_sigma)

    # =========================================================================
    # 3. Theta (Time Decay Sensitivity)
    # =========================================================================
    dt = 1 / 252  # Time step representing exactly 1 trading day

    # Ensure there is enough time remaining to step backward and forward
    if T - dt > 0:
        V_t_plus = model(S_0, K, T + dt, r, sigma, option_type)
        V_t_minus = model(S_0, K, T - dt, r, sigma, option_type)

        # Theta (Central Difference): Corrected to accurately capture time decay
        # as maturity decreases (T - dt is later in calendar time than T + dt).
        theta = (V_t_minus - V_t_plus) / (2 * dt)
    else:
        theta = np.nan  # Avoid calculating negative or zero time to maturity

    # =========================================================================
    # 4. Rho (Interest Rate Sensitivity)
    # =========================================================================
    # Shift interest rate up and down
    V_r_plus = model(S_0, K, T, r + h_r, sigma, option_type)
    V_r_minus = model(S_0, K, T, r - h_r, sigma, option_type)

    # Rho (First Derivative): Central Difference Scheme
    rho = (V_r_plus - V_r_minus) / (2 * h_r)

    return delta, gamma, vega, theta, rho


def greeks_fdm_cf(S, K, T, r, sigma, option_type="call"):

  """
    Calculates the theoretical price and the risk sensitivities (Greeks)
    of a European option using the Black-Scholes-Merton model.

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
    # Call-specific Greeks
    delta = norm.cdf(d1)
    theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    rho   = K * T * np.exp(-r * T) * norm.cdf(d2)

  elif option_type == "put":
      # Put-specific Greeks
      delta = norm.cdf(d1) - 1
      theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
      rho   = -K * T * np.exp(-r * T) * norm.cdf(-d2)

  else:
      raise ValueError("option_type must be 'call' or 'put'")


  # --- 3. Shared Greeks Calculation ---
  # Gamma and Vega are identical for both Call and Put options,
  # so they are calculated outside the conditional blocks.
  gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
  vega = S * np.sqrt(T) * norm.pdf(d1)

  return delta, gamma, vega, theta, rho
