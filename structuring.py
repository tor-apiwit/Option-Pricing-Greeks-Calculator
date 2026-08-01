# -*- coding: utf-8 -*-
"""
structuring.py

Principal-protected structured note builders (vanilla option, bull call
spread, straddle, bull strangle) plus the shared bond/option-budget split
and a print helper.

Split out from the original Colab notebook
(option_pricing___greeks_calculator.py) with no logic changes.
"""

import numpy as np

from .models import black_scholes_price


def _bond_and_budget(notional, PR, r, T):
    """Shared bond-leg / option-budget split, with the solvency check the
    original code was missing."""
    bond_leg = notional * PR * np.exp(-r * T)
    option_budget = notional - bond_leg

    return bond_leg, option_budget


def structuring_note_with_vanilla(notional, PR, S, K, T, r, sigma, option_type):
  bond_leg, option_budget = _bond_and_budget(notional, PR, r, T)
  option_price = black_scholes_price(S, K, T, r, sigma, option_type)
  uints_of_options = option_budget/option_price
  return {
        "Bond Value": bond_leg,
        "Option Budget": option_budget,
        "Fixed PR": PR,
        "Option Price": option_price,
        "Units of option": uints_of_options,
        "Time" : T
    }


def structuring_note_bull_call_spread(notional, PR, S, K_low, K_high, T, r, sigma):

  if K_high > K_low:
    bond_leg, option_budget = _bond_and_budget(notional, PR, r, T)

    call_K_low = black_scholes_price(S, K_low, T, r, sigma, "call")
    call_K_high = black_scholes_price(S, K_high, T, r, sigma, "call")
    option_price = call_K_low - call_K_high

    uints_of_options = option_budget/option_price

  else:
    raise ValueError("Exercise price in this function must be K_high > K_low")

  return {
        "Bond Value": bond_leg,
        "Option Budget": option_budget,
        "Fixed PR": PR,
        "Option Price": option_price,
        "Units of option": uints_of_options,
        "Time" : T
    }


def structuring_note_straddle(notional, PR, S, K, T, r, sigma):
  bond_leg, option_budget = _bond_and_budget(notional, PR, r, T)
  call = black_scholes_price(S, K, T, r, sigma, "call")
  put = black_scholes_price(S, K, T, r, sigma, "put")
  option_price = call + put
  uints_of_options = option_budget/option_price
  return {
        "Bond Value": bond_leg,
        "Option Budget": option_budget,
        "Fixed PR": PR,
        "Option Price": option_price,
        "Units of option": uints_of_options,
        "Time" : T
    }


def structuring_note_bull_strangle(notional, PR, S, K_call, K_put, T, r, sigma):

  if K_put > K_call:
    bond_leg, option_budget = _bond_and_budget(notional, PR, r, T)

    call = black_scholes_price(S, K_call, T, r, sigma, "call")
    put  = black_scholes_price(S, K_put, T, r, sigma, "put")
    option_price = call - put

    uints_of_options = option_budget/option_price

  else:
    raise ValueError("Exercise price in this function must be K_high > K_low")

  return {
        "Bond Value": bond_leg,
        "Option Budget": option_budget,
        "Fixed PR": PR,
        "Option Price": option_price,
        "Units of option": uints_of_options,
        "Time" : T
    }


def print_note_summary(title: str, note_data: dict):
    print(title)
    # ใช้การวนลูปผ่าน key ของ Dictionary แทนการเขียนระบุทีละตัว
    # กำหนดความกว้างของตัวอักษรเป็น 16 ตัวอักษร (:<16) เพื่อให้เครื่องหมาย : ตรงกัน
    for key, value in note_data.items():
        print(f"{key:<16}: {value:.2f}")
    print("-" * 40)
