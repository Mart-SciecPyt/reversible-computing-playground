## Quantum Toffoli upgrade

The project also includes an optional quantum extension using Qiskit.

The classical Toffoli gate is reversible on bits.  
The quantum Toffoli gate, also called the CCX gate, applies an X operation to the target qubit only when both control qubits are in state `1`.

Install the optional quantum dependencies:

```bash
pip install -r requirements-quantum.txt
```

Run the quantum demo:

```bash
python examples/quantum_toffoli_demo.py
```

Example use:

```python
from revcomp.quantum import build_quantum_toffoli_circuit

qc = build_quantum_toffoli_circuit(1, 1, 0)
print(qc.draw(output="text"))
```

This connects the project to quantum computation, because quantum gates are unitary and therefore reversible.
