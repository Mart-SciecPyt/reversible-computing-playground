"""Landauer limit utilities.

This module contains small helper functions for estimating the minimum
energy cost of irreversible bit erasure according to Landauer's principle.
"""

from __future__ import annotations

import math
from typing import Iterable

# Boltzmann constant in joule per kelvin
K_B = 1.380649e-23


def energy_per_erased_bit(temperature_kelvin: float) -> float:
    """Return the Landauer minimum energy for erasing one bit.

    Parameters
    ----------
    temperature_kelvin:
        Absolute temperature in kelvin.

    Returns
    -------
    float
        Minimum energy in joule: k_B * T * ln(2).
    """
    if temperature_kelvin < 0:
        raise ValueError("Temperature must be non-negative in kelvin.")
    return K_B * temperature_kelvin * math.log(2)


def total_erasure_energy(number_of_bits: int, temperature_kelvin: float) -> float:
    """Return the minimum energy for erasing multiple bits."""
    if number_of_bits < 0:
        raise ValueError("Number of bits must be non-negative.")
    return number_of_bits * energy_per_erased_bit(temperature_kelvin)


def energy_curve(temperatures_kelvin: Iterable[float]) -> list[float]:
    """Compute Landauer energy values for an iterable of temperatures."""
    return [energy_per_erased_bit(temp) for temp in temperatures_kelvin]
