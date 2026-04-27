"""Small simulation helpers for the reversible computing playground."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .gates import Gate, is_reversible, lost_information_bits, truth_table
from .landauer import total_erasure_energy


@dataclass(frozen=True)
class GateAnalysis:
    name: str
    input_size: int
    reversible: bool
    lost_bits: float
    landauer_energy_at_300K: float


def analyze_gate(name: str, gate: Gate, input_size: int, temperature_kelvin: float = 300.0) -> GateAnalysis:
    """Analyze reversibility and approximate erasure cost of a gate."""
    lost_bits = lost_information_bits(gate, input_size)
    energy = total_erasure_energy(round(lost_bits), temperature_kelvin)
    return GateAnalysis(
        name=name,
        input_size=input_size,
        reversible=is_reversible(gate, input_size),
        lost_bits=lost_bits,
        landauer_energy_at_300K=energy,
    )


def compare_gates(gates: dict[str, tuple[Callable, int]], temperature_kelvin: float = 300.0) -> list[GateAnalysis]:
    """Analyze several gates and return the results as a list."""
    return [analyze_gate(name, gate, n, temperature_kelvin) for name, (gate, n) in gates.items()]
