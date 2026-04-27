"""
Quantum Toffoli demo.

Run:
    python examples/quantum_toffoli_demo.py

This example requires Qiskit:
    pip install -r requirements-quantum.txt
"""

from revcomp.quantum import (
    build_quantum_toffoli_circuit,
    quantum_toffoli_truth_table,
    save_quantum_toffoli_figure,
)


def main():
    print("Quantum Toffoli / CCX demo")
    print("===========================")

    circuit = build_quantum_toffoli_circuit(1, 1, 0, include_measurements=False)

    print("\nCircuit:")
    print(circuit.draw(output="text"))

    print("\nTruth table on computational basis states:")
    print("input abc -> output abc | probability")
    print("------------------------------------")

    for input_bits, output_label, probability in quantum_toffoli_truth_table():
        a, b, c = input_bits
        print(f"{a}{b}{c} -> {output_label} | {probability:.1f}")

    saved = save_quantum_toffoli_figure("figures/quantum_toffoli_circuit.png")
    if saved:
        print("\nSaved circuit figure: figures/quantum_toffoli_circuit.png")
    else:
        print("\nCircuit image was not saved. Text output still works.")
        print("Install optional drawing dependency if needed:")
        print("    pip install pylatexenc")


if __name__ == "__main__":
    main()
