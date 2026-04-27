# Theory Notes

## 1. Irreversible computation

A logic operation is irreversible if the original input cannot be reconstructed from the output.

Example: the `AND` gate maps four possible inputs to only two possible outputs:

```text
(0, 0) -> 0
(0, 1) -> 0
(1, 0) -> 0
(1, 1) -> 1
```

Because three different inputs collapse into the same output `0`, information is lost.

## 2. Landauer's principle

Landauer's principle states that erasing one bit of information has a minimum energy cost:

```math
E_{min} = k_B T \ln 2
```

where:

- `k_B` is the Boltzmann constant,
- `T` is the absolute temperature in kelvin,
- `ln 2` appears because one binary bit has two possible states.

At room temperature, around 300 K, this energy is extremely small for one bit, but it becomes relevant when billions or trillions of operations are performed.

## 3. Reversible computation

A reversible gate has a one-to-one mapping between input and output states. Therefore, the input can always be reconstructed from the output.

Examples:

- `NOT`: reversible
- `CNOT`: reversible
- `Toffoli`: reversible
- `Fredkin`: reversible

## 4. Toffoli gate

The Toffoli gate has three bits: two control bits and one target bit.

```text
(a, b, c) -> (a, b, c XOR (a AND b))
```

It is important because it is universal for reversible classical computation.

## 5. Connection to quantum computing

Ideal quantum gates are represented by unitary matrices. Unitary transformations are reversible, because their inverse also exists. This is why reversible computing is a natural conceptual bridge between classical computation, thermodynamics, and quantum computation.
