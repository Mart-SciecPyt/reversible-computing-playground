"""Example: use revcomp inside your own code.

Run from project root:
    python examples/runtime_usage.py
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from revcomp import ComputationalProfiler, format_runtime_profile, profiled


def heavy_calculation(n: int = 100_000) -> float:
    total = 0.0
    for i in range(1, n):
        total += (i ** 2 + 3 * i) / (i + 1)
    return total


def main() -> None:
    with ComputationalProfiler("heavy_calculation") as profiler:
        result = heavy_calculation()

    print(f"Calculation result: {result:.3f}")
    print()
    print(format_runtime_profile(profiler.result))


@profiled("decorated small task")
def small_task() -> int:
    return sum(i * i for i in range(1000))


if __name__ == "__main__":
    main()
    print("\nDecorator example:\n")
    small_task()
