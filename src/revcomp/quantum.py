"""
Quantum Toffoli utilities for the Reversible Computing Playground.

This module is optional: it requires Qiskit.
The classical Toffoli gate is reversible on bits.
The quantum Toffoli gate, also called CCX, is reversible/unitary on qubits.
"""

from __future__ import annotations

from typing import Dict, List, Tuple


def _require_qiskit():
    """Import Qiskit only when quantum features are used."""
    try:
        from qiskit import QuantumCircuit
        from qiskit.quantum_info import Statevector
    except ImportError as exc:
        raise ImportError(
            "Qiskit is required for quantum features. Install it with:\n"
            "    pip install -r requirements-quantum.txt\n"
            "or:\n"
            "    pip install qiskit pylatexenc"
        ) from exc

    return QuantumCircuit, Statevector


def build_quantum_toffoli_circuit(
    a: int = 1,
    b: int = 1,
    c: int = 0,
    include_measurements: bool = False,
):
    """
    Build a 3-qubit quantum Toffoli circuit.

    The Toffoli gate flips the target qubit c only if both control qubits
    a and b are equal to 1.

    Classical reversible rule:
        (a, b, c) -> (a, b, c XOR (a AND b))

    Parameters
    ----------
    a, b, c:
        Initial computational basis values of the three qubits.
    include_measurements:
        If True, add classical bits and measurement operations.

    Returns
    -------
    qiskit.QuantumCircuit
        The quantum circuit containing a CCX gate.
    """
    QuantumCircuit, _ = _require_qiskit()

    if any(bit not in (0, 1) for bit in (a, b, c)):
        raise ValueError("a, b, and c must be classical bit values: 0 or 1.")

    if include_measurements:
        circuit = QuantumCircuit(3, 3)
    else:
        circuit = QuantumCircuit(3)

    if a:
        circuit.x(0)
    if b:
        circuit.x(1)
    if c:
        circuit.x(2)

    circuit.barrier()
    circuit.ccx(0, 1, 2)
    circuit.barrier()

    if include_measurements:
        circuit.measure([0, 1, 2], [0, 1, 2])

    return circuit


def simulate_quantum_toffoli_basis_state(a: int, b: int, c: int) -> Dict[str, float]:
    """
    Simulate a quantum Toffoli circuit on a computational basis input.

    Returns a probability dictionary over output basis states.

    Note about Qiskit bit order:
    Qiskit prints basis labels in little-endian style. For this educational
    utility, the result is converted to the human-readable order abc.
    """
    _, Statevector = _require_qiskit()
    circuit = build_quantum_toffoli_circuit(a, b, c, include_measurements=False)
    state = Statevector.from_instruction(circuit)
    raw_probs = state.probabilities_dict()

    converted: Dict[str, float] = {}
    for qiskit_label, prob in raw_probs.items():
        # Qiskit label order is often cba for qubits [0,1,2], so reverse it.
        human_label = qiskit_label[::-1]
        converted[human_label] = float(prob)

    return converted


def quantum_toffoli_truth_table() -> List[Tuple[Tuple[int, int, int], str, float]]:
    """
    Generate the quantum Toffoli truth table for computational basis inputs.

    Returns
    -------
    list
        Each row contains:
        ((input_a, input_b, input_c), most_likely_output_label, probability)
    """
    rows = []

    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                probs = simulate_quantum_toffoli_basis_state(a, b, c)
                output_label, probability = max(probs.items(), key=lambda item: item[1])
                rows.append(((a, b, c), output_label, probability))

    return rows


def save_quantum_toffoli_figure(path: str = "figures/quantum_toffoli_circuit.png") -> bool:
    """
    Save a circuit diagram of the quantum Toffoli gate if drawing dependencies exist.

    Returns True if the image was saved, otherwise False.
    """
    circuit = build_quantum_toffoli_circuit(1, 1, 0, include_measurements=False)

    try:
        figure = circuit.draw(output="mpl")
        figure.savefig(path, bbox_inches="tight")
        return True
    except Exception:
        return False
