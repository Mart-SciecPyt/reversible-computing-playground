# Reversible Computing and the Landauer Limit

## 1. Introduction

This project studies the connection between logic operations and physical energy cost. In ordinary digital computation, many logical operations are irreversible: after seeing the output, the original input cannot always be reconstructed. This loss of information is not only a mathematical issue, but also a physical one. According to Landauer's principle, erasing information has a minimum thermodynamic energy cost.

The goal of the project is to implement a small Python playground that compares irreversible and reversible logic gates and calculates the Landauer limit for bit erasure.

## 2. Physical background

Landauer's principle states that the minimum energy required to erase one bit of information at temperature `T` is:

```math
E_{min} = k_B T \ln 2
```

Here `k_B` is the Boltzmann constant and `T` is the absolute temperature in kelvin. The formula shows that computation is connected to thermodynamics: information erasure produces a physical cost.

At room temperature, `T = 300 K`, the minimum energy per erased bit is approximately:

```text
2.87 × 10^-21 J
```

This value is very small for a single bit, but modern computers process enormous numbers of bits, which makes the physical limits of computation important.

## 3. Irreversible gates

The project implements basic gates such as `AND`, `OR`, and `XOR`. These gates are usually irreversible because several inputs can produce the same output. For example, in the `AND` gate, the inputs `(0,0)`, `(0,1)`, and `(1,0)` all produce output `0`. Therefore, the output alone does not contain enough information to reconstruct the input.

## 4. Reversible gates

The project also implements reversible gates such as `NOT`, `CNOT`, `Toffoli`, and `Fredkin`. These gates preserve information because every input state maps to a unique output state. The Toffoli gate is especially important because it is universal for reversible classical computation.

The Toffoli gate acts as:

```text
(a, b, c) -> (a, b, c XOR (a AND b))
```

This means the third bit is flipped only when both control bits are equal to one.

## 5. Python implementation

The implementation contains separate modules for:

- logic gates,
- Landauer energy calculations,
- gate analysis,
- plotting.

The program automatically generates truth tables, checks whether a gate is reversible, estimates lost information, and plots the dependence of the Landauer energy on temperature.

## 6. Results

The demo script shows that `AND`, `OR`, and `XOR` are irreversible in their simple two-input, one-output form, while `NOT`, `CNOT`, `Toffoli`, and `Fredkin` are reversible.

The generated Landauer plot shows a linear relationship between temperature and the minimum energy required to erase one bit. This agrees with the formula `E_min = k_B T ln 2`.

## 7. Connection to quantum computing

Reversible computation is closely related to quantum computing. Ideal quantum gates are unitary transformations, and unitary transformations are reversible. Therefore, reversible classical gates such as the Toffoli gate provide a useful conceptual bridge between classical information theory, thermodynamics, and quantum information processing.

## 8. Conclusion

This project demonstrates that computation has physical consequences. Irreversible logical operations destroy information, and information erasure has a minimum energy cost. Reversible computing avoids this information loss at the logical level and is therefore an important concept in the physics of computation and quantum engineering.

The project can be extended by adding a reversible full adder, Qiskit circuits, and comparisons between classical reversible gates and quantum gates.
