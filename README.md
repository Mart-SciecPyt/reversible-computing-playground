# Reversible Computing Playground

A small Python toolkit for studying the physical limits of computation through
reversible logic, Landauer's principle, runtime profiling, and an optional
quantum Toffoli gate example.

The project was created for a Physics of Computing assignment, but it is written
as a reusable Python package. It can be imported into other Python scripts and
used to estimate the computational effort of a code block.

---

## Purpose

Computation is a physical process. When information is irreversibly erased, a
minimum amount of energy must be dissipated as heat. This theoretical lower
bound is described by Landauer's principle:

```text
E_min = k_B * T * ln(2)
```

This project demonstrates this idea in three ways:

1. by implementing irreversible and reversible logic gates,
2. by calculating the Landauer lower bound for bit erasure,
3. by providing a lightweight runtime profiler that estimates the computational
   effort of Python code and connects it to a theoretical Landauer energy limit.

The profiler is educational. It does not measure real CPU power consumption.
Instead, it gives a theoretical and comparative estimate based on runtime,
CPU time, memory usage, and an approximate number of computational events.

---

## Main features

- Classical logic gates: AND, OR, XOR, NOT
- Reversible logic: Toffoli gate
- Truth table generation
- Reversibility checking
- Landauer energy calculation
- Energy vs temperature plotting
- Runtime computational profiler
- Heavy-computation demo
- Optional Qiskit-based quantum Toffoli gate demo
- Unit tests
- Short theoretical documentation and assignment report

---

## Project structure

```text
reversible-computing-playground/
│
├── src/
│   └── revcomp/
│       ├── gates.py          # classical and reversible gate functions
│       ├── landauer.py       # Landauer energy calculations
│       ├── plots.py          # plotting utilities
│       ├── profiler.py       # runtime computational profiler
│       ├── quantum.py        # optional Qiskit-based quantum Toffoli tools
│       └── simulation.py     # truth table and simulation helpers
│
├── examples/
│   ├── demo.py                   # basic gate and Landauer demo
│   ├── runtime_usage.py           # minimal runtime profiler example
│   ├── heavy_demo.py              # heavier runtime profiling demo
│   └── quantum_toffoli_demo.py    # optional quantum Toffoli demo
│
├── docs/
│   └── theory.md              # theoretical background
│
├── figures/                   # generated plots and screenshots
├── tests/                     # unit tests
├── report.md                  # assignment-style report
├── requirements.txt           # base dependencies
├── requirements-quantum.txt   # optional quantum dependencies
├── pyproject.toml
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Mart-SciecPyt/reversible-computing-playground.git
cd reversible-computing-playground
```

Install the base dependencies:

```bash
pip install -r requirements.txt
```

Install the package in editable mode:

```bash
pip install -e .
```

The editable installation is recommended because it allows the package to be
imported from any script while still keeping the source files editable.

After installation, this should work in Python:

```python
import revcomp
```

---

## Quick test

Run the basic demo:

```bash
python examples/demo.py
```

Run the runtime profiler demo:

```bash
python examples/runtime_usage.py
```

Run the heavier computational demo:

```bash
python examples/heavy_demo.py
```

Run unit tests:

```bash
pytest
```

---

## Using the profiler in your own Python code

The runtime profiler can be used with a `with` block.

Example:

```python
from revcomp import ComputationalProfiler, format_runtime_profile

with ComputationalProfiler("my computation") as profiler:
    result = sum(i * i for i in range(100_000))

print(format_runtime_profile(profiler.result))
```

This allows any Python code placed inside the `with` block to be profiled.

---

## What the profiler reports

The profiler returns a computational-effort report. A typical output looks like:

```text
Runtime Computational-Effort Report
===================================
Label: heavy computation demo
Wall time:              0.897551 s
CPU time:               0.828125 s
Peak traced memory:     12.253 MB

Educational Landauer estimate:
Temperature:            300.00 K
Bits per event:         64
Estimated events:       840671
Estimated erased bits:  53802944
Landauer lower bound:   1.545e-13 J

Important notes:
- This is an educational computational-effort estimate, not a real CPU wattmeter.
- The Landauer value is a theoretical lower bound and is far below real hardware energy use.
- The event estimate is based on CPU time and traced peak memory, not actual machine instructions.
```

### Meaning of the reported values

#### Wall time

The real elapsed time between the start and end of the profiled code block.

This includes the time observed by the user, including interpreter overhead and
possible waiting time.

#### CPU time

The amount of processor time used by the Python process during the profiled
section.

This is useful for estimating how much active computation was performed.

#### Peak traced memory

The maximum amount of memory traced during the profiled block.

This does not necessarily equal the full system memory usage, but it is useful
for comparing different Python code blocks.

#### Estimated events

A rough educational estimate of how many computational events occurred.

This is not the real number of CPU instructions. It is a model-based estimate
derived from runtime and memory behavior.

#### Estimated erased bits

An approximate number of bits treated as irreversibly processed or erased by the
model.

This value is used to connect the runtime behavior to Landauer's principle.

#### Landauer lower bound

The theoretical minimum energy required to erase the estimated number of bits at
the selected temperature.

This is not the real energy used by the CPU. Real hardware consumes many orders
of magnitude more energy.

---

## Changing the temperature

By default, the profiler uses approximately room temperature:

```text
T = 300 K
```

If the profiler implementation in your version exposes a temperature parameter,
it can be used to compare different physical temperature assumptions.

Conceptually:

```python
with ComputationalProfiler("cold system", temperature=77) as profiler:
    result = sum(i * i for i in range(100_000))
```

A lower temperature decreases the theoretical Landauer energy per erased bit.

---

## Landauer calculation example

The package can also calculate the Landauer energy directly:

```python
from revcomp import landauer_energy

energy = landauer_energy(temperature=300)
print(energy)
```

This returns the minimum energy required to erase one bit at 300 K.

For multiple bits:

```python
from revcomp import landauer_energy_for_bits

energy = landauer_energy_for_bits(bits=1_000_000, temperature=300)
print(energy)
```

---

## Reversible logic example

The Toffoli gate is a reversible three-bit gate. It flips the third bit only if
the first two bits are both 1.

```python
from revcomp import toffoli_gate

print(toffoli_gate(1, 1, 0))
```

Expected behavior:

```text
(1, 1, 1)
```

The Toffoli gate is important because it shows how universal classical
computation can be represented using reversible operations.

---

## Optional quantum extension

The project also includes an optional quantum Toffoli example using Qiskit.

The quantum Toffoli gate is also called the CCX gate. It applies an X operation
to the target qubit only when both control qubits are in state `1`.

Install the optional quantum dependencies:

```bash
pip install -r requirements-quantum.txt
```

Run the quantum demo:

```bash
python examples/quantum_toffoli_demo.py
```

Minimal example:

```python
from revcomp.quantum import build_quantum_toffoli_circuit

qc = build_quantum_toffoli_circuit(1, 1, 0)
print(qc.draw(output="text"))
```

This connects reversible classical computation to quantum computation, where
valid quantum gates are unitary and therefore reversible.

---

## Interpreting the project correctly

This package is not a CPU power meter.

It does not answer:

```text
How many watts did my laptop use?
```

Instead, it answers a theoretical Physics of Computing question:

```text
Given an estimated amount of information processing, what is the theoretical
minimum energy required by Landauer's principle?
```

The project is therefore best used for:

- educational demonstrations,
- comparing simple code blocks,
- showing the relation between computation and thermodynamics,
- explaining why irreversible information erasure has a physical energy cost,
- connecting classical reversible logic to quantum computation.

---

## Limitations

The runtime profiler is intentionally simple.

Important limitations:

- It does not count real CPU instructions.
- It does not measure electrical power.
- It does not account for processor architecture.
- It does not include cache behavior, voltage scaling, or operating system effects.
- It should not be used for hardware benchmarking.
- The Landauer energy is a theoretical lower bound, not a practical energy estimate.

Real computers consume much more energy than the Landauer limit.

---

## Example use cases

### 1. Compare two algorithms

You can wrap two different code blocks with the profiler and compare their wall
time, CPU time, peak memory, estimated erased bits, and Landauer lower bound.

### 2. Demonstrate Landauer's principle

You can calculate the energy required to erase a given number of bits at a given
temperature.

### 3. Study reversible gates

You can compare irreversible gates such as AND and OR with reversible gates such
as Toffoli.

### 4. Connect to quantum computing

You can run the optional Qiskit demo to see the quantum version of the Toffoli
gate.

---

## Future work

Possible extensions:

- Fredkin gate implementation
- Reversible full adder
- More accurate static Python code analysis
- More advanced runtime event estimation
- Streamlit-based interactive dashboard
- More Qiskit examples
- Classical vs quantum reversible circuit comparison

---

## Author

Martin Trancsik

Physics of Computing / Quantum Engineering project.
