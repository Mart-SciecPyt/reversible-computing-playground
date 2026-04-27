"""Static Python code analyzer for educational Landauer-limit estimates.

This module does NOT predict real CPU power consumption. It parses Python code
with the built-in ``ast`` module, counts selected operations, estimates an
educational bit-erasure count, and converts that into a Landauer lower bound.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path

from .landauer import total_erasure_energy


@dataclass(frozen=True)
class OperationProfile:
    """Summary of counted Python operations."""

    file_path: str
    additions: int = 0
    subtractions: int = 0
    multiplications: int = 0
    divisions: int = 0
    modulo_ops: int = 0
    powers: int = 0
    comparisons: int = 0
    boolean_operations: int = 0
    assignments: int = 0
    function_calls: int = 0
    loops: int = 0
    conditionals: int = 0
    estimated_operations: int = 0
    estimated_erased_bits: int = 0
    temperature_kelvin: float = 300.0
    landauer_energy_joule: float = 0.0
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, int | float | str | list[str]]:
        """Return a dictionary representation useful for JSON export later."""
        return self.__dict__.copy()


class PythonOperationCounter(ast.NodeVisitor):
    """Count selected operation types in a Python abstract syntax tree."""

    def __init__(self) -> None:
        self.additions = 0
        self.subtractions = 0
        self.multiplications = 0
        self.divisions = 0
        self.modulo_ops = 0
        self.powers = 0
        self.comparisons = 0
        self.boolean_operations = 0
        self.assignments = 0
        self.function_calls = 0
        self.loops = 0
        self.conditionals = 0

    def visit_BinOp(self, node: ast.BinOp) -> None:  # noqa: N802 - ast naming convention
        op = node.op
        if isinstance(op, ast.Add):
            self.additions += 1
        elif isinstance(op, ast.Sub):
            self.subtractions += 1
        elif isinstance(op, ast.Mult):
            self.multiplications += 1
        elif isinstance(op, (ast.Div, ast.FloorDiv)):
            self.divisions += 1
        elif isinstance(op, ast.Mod):
            self.modulo_ops += 1
        elif isinstance(op, ast.Pow):
            self.powers += 1
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:  # noqa: N802
        self.comparisons += len(node.ops)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:  # noqa: N802
        # a and b and c contains two boolean operations
        self.boolean_operations += max(1, len(node.values) - 1)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:  # noqa: N802
        self.assignments += len(node.targets)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:  # noqa: N802
        self.assignments += 1
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:  # noqa: N802
        self.assignments += 1
        # x += 1 also contains an arithmetic update
        if isinstance(node.op, ast.Add):
            self.additions += 1
        elif isinstance(node.op, ast.Sub):
            self.subtractions += 1
        elif isinstance(node.op, ast.Mult):
            self.multiplications += 1
        elif isinstance(node.op, (ast.Div, ast.FloorDiv)):
            self.divisions += 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        self.function_calls += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:  # noqa: N802
        self.loops += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:  # noqa: N802
        self.loops += 1
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:  # noqa: N802
        self.conditionals += 1
        self.generic_visit(node)


def _weighted_operation_estimate(counter: PythonOperationCounter) -> int:
    """Return a simple weighted operation estimate.

    The weights are intentionally coarse and educational. Multiplication,
    division, powers, and function calls are weighted higher than addition.
    """
    return (
        counter.additions
        + counter.subtractions
        + 3 * counter.multiplications
        + 6 * counter.divisions
        + 6 * counter.modulo_ops
        + 10 * counter.powers
        + counter.comparisons
        + counter.boolean_operations
        + counter.assignments
        + 5 * counter.function_calls
        + 4 * counter.loops
        + 2 * counter.conditionals
    )


def analyze_python_file(
    file_path: str | Path,
    temperature_kelvin: float = 300.0,
    bits_per_operation: int = 64,
) -> OperationProfile:
    """Analyze a Python file and estimate its Landauer lower-bound energy.

    Parameters
    ----------
    file_path:
        Path to a Python source file.
    temperature_kelvin:
        Absolute temperature used in the Landauer formula.
    bits_per_operation:
        Educational assumption for erased bits per counted operation.

    Returns
    -------
    OperationProfile
        Counted operations and estimated Landauer lower-bound energy.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix != ".py":
        raise ValueError("Only .py files are supported.")
    if bits_per_operation <= 0:
        raise ValueError("bits_per_operation must be positive.")

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    counter = PythonOperationCounter()
    counter.visit(tree)

    estimated_operations = _weighted_operation_estimate(counter)
    estimated_erased_bits = estimated_operations * bits_per_operation
    energy = total_erasure_energy(estimated_erased_bits, temperature_kelvin)

    notes = [
        "This is a static educational estimate, not a real CPU power measurement.",
        "Loops are counted structurally, not by runtime iteration count.",
        "Python interpreter overhead and hardware effects are not included.",
        "The result is a theoretical Landauer lower bound, usually far below real energy use.",
    ]

    return OperationProfile(
        file_path=str(path),
        additions=counter.additions,
        subtractions=counter.subtractions,
        multiplications=counter.multiplications,
        divisions=counter.divisions,
        modulo_ops=counter.modulo_ops,
        powers=counter.powers,
        comparisons=counter.comparisons,
        boolean_operations=counter.boolean_operations,
        assignments=counter.assignments,
        function_calls=counter.function_calls,
        loops=counter.loops,
        conditionals=counter.conditionals,
        estimated_operations=estimated_operations,
        estimated_erased_bits=estimated_erased_bits,
        temperature_kelvin=temperature_kelvin,
        landauer_energy_joule=energy,
        notes=notes,
    )


def format_operation_profile(profile: OperationProfile) -> str:
    """Format an operation profile as readable text."""
    lines = [
        "Python Code Energy-Limit Analysis",
        "=================================",
        f"File: {profile.file_path}",
        f"Temperature: {profile.temperature_kelvin:.2f} K",
        "",
        "Static operation counts:",
        f"- additions:            {profile.additions}",
        f"- subtractions:         {profile.subtractions}",
        f"- multiplications:      {profile.multiplications}",
        f"- divisions:            {profile.divisions}",
        f"- modulo operations:    {profile.modulo_ops}",
        f"- powers:               {profile.powers}",
        f"- comparisons:          {profile.comparisons}",
        f"- boolean operations:   {profile.boolean_operations}",
        f"- assignments:          {profile.assignments}",
        f"- function calls:       {profile.function_calls}",
        f"- loops:                {profile.loops}",
        f"- conditionals:         {profile.conditionals}",
        "",
        "Educational estimate:",
        f"- weighted operations:  {profile.estimated_operations}",
        f"- erased bits:          {profile.estimated_erased_bits}",
        f"- Landauer lower bound: {profile.landauer_energy_joule:.3e} J",
        "",
        "Important notes:",
    ]
    lines.extend(f"- {note}" for note in profile.notes)
    return "\n".join(lines)
