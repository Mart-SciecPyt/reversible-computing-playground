"""Demo script for Reversible Computing Playground.

Run from the project root:
    python examples/demo.py
"""

from pathlib import Path
import sys

# Allow running the example without package installation.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from revcomp.gates import AND, CNOT, FREDKIN, NOT, OR, TOFFOLI, XOR, format_truth_table, truth_table
from revcomp.plots import plot_landauer_curve
from revcomp.simulation import compare_gates
from revcomp.landauer import energy_per_erased_bit


def main() -> None:
    gates = {
        "NOT": (NOT, 1),
        "AND": (AND, 2),
        "OR": (OR, 2),
        "XOR": (XOR, 2),
        "CNOT": (CNOT, 2),
        "TOFFOLI": (TOFFOLI, 3),
        "FREDKIN": (FREDKIN, 3),
    }

    print("Reversible Computing Playground")
    print("================================")
    print()

    print("Landauer energy per erased bit at 300 K:")
    print(f"E_min = {energy_per_erased_bit(300):.3e} J")
    print()

    print("Gate comparison:")
    for result in compare_gates(gates):
        status = "reversible" if result.reversible else "irreversible"
        print(
            f"- {result.name:8s}: {status:12s} | "
            f"lost information ≈ {result.lost_bits:.2f} bit(s)"
        )

    print()
    print("Toffoli truth table:")
    print(format_truth_table(truth_table(TOFFOLI, 3)))

    figure_path = plot_landauer_curve(PROJECT_ROOT / "figures" / "landauer_curve.png")
    print()
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()
