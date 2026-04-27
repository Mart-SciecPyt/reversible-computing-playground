# Reversible Computing Playground

A Python-based educational toolkit for exploring the physical limits of computation through reversible logic, Landauer's principle, and runtime computational profiling.

This project connects three ideas:

1. classical computation,
2. information loss,
3. thermodynamic energy limits.

It was developed as a Physics of Computing project, but it is structured as a reusable Python package.

---

## Why this project matters

Modern computation is not only a mathematical process. It is also a physical process.

Whenever information is irreversibly erased, a minimum amount of energy must be dissipated as heat. This lower bound is described by Landauer's principle:

E_min = k_B * T * ln(2)

This project demonstrates that idea using Python.

---

## Main features

- Classical logic gates: AND, OR, XOR, NOT
- Reversible logic gate: Toffoli gate
- Automatic reversibility checking
- Truth table generation
- Landauer energy calculations
- Energy vs temperature visualization
- Runtime computational profiler
- Simple examples and tests
- Markdown report for academic submission

---

## Runtime profiler

Example:

from revcomp import ComputationalProfiler, format_runtime_profile

with ComputationalProfiler("example computation") as profiler:
    result = sum(i * i for i in range(100_000))

print(format_runtime_profile(profiler.result))

---

## Installation

git clone https://github.com/Mart-SciecPyt/reversible-computing-playground.git
cd reversible-computing-playground

pip install -r requirements.txt

---

## Usage

python examples/demo.py
python examples/runtime_usage.py

---

## Author

Martin Trancsik
