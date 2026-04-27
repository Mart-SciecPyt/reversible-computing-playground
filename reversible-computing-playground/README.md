# Reversible Computing Playground

A small educational Python project for the **Physics of Computing** course.

The project compares ordinary irreversible logic gates with reversible gates and connects this to the physical cost of information erasure through **Landauer's principle**.

## Main idea

Classical logic gates such as `AND` and `OR` lose information because several different inputs can produce the same output. According to Landauer's principle, irreversible information erasure has a minimum thermodynamic energy cost:

```math
E_{min} = k_B T \ln 2
```

Reversible gates such as `NOT`, `CNOT`, `Toffoli`, and `Fredkin` preserve enough information to reconstruct the input from the output. This makes reversible computing an important bridge between classical thermodynamics of computation and quantum computing, where ideal quantum gates are unitary and therefore reversible.

## Features

- Classical gates: `NOT`, `AND`, `OR`, `XOR`
- Reversible gates: `CNOT`, `Toffoli`, `Fredkin`
- Truth table generation
- Automatic reversibility check
- Simple lost-information estimate
- Landauer limit calculation
- Temperature vs energy plot
- Demo script and basic tests

## Project structure

```text
reversible-computing-playground/
├── src/revcomp/
│   ├── gates.py
│   ├── landauer.py
│   ├── plots.py
│   └── simulation.py
├── examples/
│   └── demo.py
├── docs/
│   └── theory.md
├── tests/
│   └── test_gates.py
├── figures/
├── README.md
├── report.md
├── requirements.txt
└── pyproject.toml
```

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/reversible-computing-playground.git
cd reversible-computing-playground
pip install -r requirements.txt
```

## Run the demo

```bash
python examples/demo.py
```

The demo prints a comparison of reversible and irreversible gates and saves a figure to:

```text
figures/landauer_curve.png
```

## Run tests

```bash
pytest
```

## Possible extensions

- Add more reversible gates
- Build a reversible full adder
- Add Qiskit implementation of the Toffoli gate
- Compare classical reversible gates with quantum unitary gates
- Create a Streamlit web demo

## Course relevance

This project demonstrates a core idea of the physics of computation: information processing is not only mathematical, but physical. If a computational operation erases information, thermodynamics imposes a minimum energy cost.
