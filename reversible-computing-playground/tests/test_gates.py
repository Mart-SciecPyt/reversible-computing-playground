from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from revcomp.gates import AND, CNOT, FREDKIN, NOT, OR, TOFFOLI, is_reversible


def test_irreversible_gates():
    assert not is_reversible(AND, 2)
    assert not is_reversible(OR, 2)


def test_reversible_gates():
    assert is_reversible(NOT, 1)
    assert is_reversible(CNOT, 2)
    assert is_reversible(TOFFOLI, 3)
    assert is_reversible(FREDKIN, 3)
