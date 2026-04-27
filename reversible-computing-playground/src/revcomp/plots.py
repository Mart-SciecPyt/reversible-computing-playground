"""Plotting functions for the project."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from .landauer import energy_curve


def plot_landauer_curve(output_path: str | Path = "figures/landauer_curve.png") -> Path:
    """Create a temperature vs Landauer energy plot."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    temperatures = list(range(1, 501))
    energies = energy_curve(temperatures)

    plt.figure()
    plt.plot(temperatures, energies)
    plt.xlabel("Temperature [K]")
    plt.ylabel("Minimum energy per erased bit [J]")
    plt.title("Landauer Limit")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    return output_path
