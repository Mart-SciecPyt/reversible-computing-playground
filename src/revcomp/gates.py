"""Classical irreversible and reversible logic gates.

The main idea is simple: a gate is reversible if every output corresponds to
exactly one input. In other words, the input-output mapping is one-to-one.
"""

from __future__ import annotations

from itertools import product
from typing import Callable, Iterable, Sequence, Tuple

Bit = int
BitTuple = Tuple[Bit, ...]
Gate = Callable[..., BitTuple]


def _validate_bits(bits: Iterable[int]) -> None:
    for bit in bits:
        if bit not in (0, 1):
            raise ValueError("All inputs must be binary bits: 0 or 1.")


def NOT(a: Bit) -> BitTuple:
    _validate_bits((a,))
    return (1 - a,)


def AND(a: Bit, b: Bit) -> BitTuple:
    _validate_bits((a, b))
    return (a & b,)


def OR(a: Bit, b: Bit) -> BitTuple:
    _validate_bits((a, b))
    return (a | b,)


def XOR(a: Bit, b: Bit) -> BitTuple:
    _validate_bits((a, b))
    return (a ^ b,)


def CNOT(control: Bit, target: Bit) -> BitTuple:
    """Controlled-NOT gate: maps (c, t) -> (c, t XOR c)."""
    _validate_bits((control, target))
    return (control, target ^ control)


def TOFFOLI(a: Bit, b: Bit, c: Bit) -> BitTuple:
    """Toffoli gate: maps (a, b, c) -> (a, b, c XOR (a AND b))."""
    _validate_bits((a, b, c))
    return (a, b, c ^ (a & b))


def FREDKIN(control: Bit, a: Bit, b: Bit) -> BitTuple:
    """Fredkin gate: swaps a and b if control is 1."""
    _validate_bits((control, a, b))
    if control == 1:
        return (control, b, a)
    return (control, a, b)


def truth_table(gate: Gate, input_size: int) -> list[tuple[BitTuple, BitTuple]]:
    """Generate the truth table of a binary gate."""
    rows = []
    for input_bits in product((0, 1), repeat=input_size):
        output_bits = gate(*input_bits)
        rows.append((input_bits, output_bits))
    return rows


def is_reversible(gate: Gate, input_size: int) -> bool:
    """Check whether a gate has a one-to-one input-output mapping."""
    outputs = [output for _, output in truth_table(gate, input_size)]
    return len(outputs) == len(set(outputs))


def lost_information_bits(gate: Gate, input_size: int) -> float:
    """Estimate lost information in bits from input/output state counts.

    This is a coarse educational estimate: if N inputs collapse into M unique
    outputs, then log2(N/M) bits are lost on average at the mapping level.
    """
    import math

    rows = truth_table(gate, input_size)
    unique_outputs = {output for _, output in rows}
    return math.log2(len(rows) / len(unique_outputs))


def format_truth_table(rows: Sequence[tuple[BitTuple, BitTuple]]) -> str:
    """Return a human-readable truth table string."""
    lines = ["input -> output"]
    lines.append("-" * 17)
    for input_bits, output_bits in rows:
        lines.append(f"{input_bits} -> {output_bits}")
    return "\n".join(lines)
