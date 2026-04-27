"""Reversible Computing Playground."""

from .gates import AND, CNOT, FREDKIN, NOT, OR, TOFFOLI, XOR, is_reversible, truth_table
from .landauer import energy_per_erased_bit, total_erasure_energy
from .code_analyzer import analyze_python_file, format_operation_profile
from .runtime import ComputationalProfiler, RuntimeProfile, format_runtime_profile, profiled

__all__ = [
    "AND", "CNOT", "FREDKIN", "NOT", "OR", "TOFFOLI", "XOR",
    "is_reversible", "truth_table", "energy_per_erased_bit", "total_erasure_energy",
    "analyze_python_file", "format_operation_profile",
    "ComputationalProfiler", "RuntimeProfile", "format_runtime_profile", "profiled",
]
