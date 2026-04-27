"""Small sample program used by the analyzer demo."""


def kinetic_energy(mass: float, velocity: float) -> float:
    return 0.5 * mass * velocity ** 2


def classify_energy(energy: float) -> str:
    if energy > 1000:
        return "high"
    return "normal"


def main() -> None:
    total = 0.0
    for velocity in range(1, 11):
        total += kinetic_energy(80.0, velocity)
    label = classify_energy(total)
    print(total, label)


if __name__ == "__main__":
    main()
