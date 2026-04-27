from revcomp import ComputationalProfiler, format_runtime_profile
import random

def heavy_computation(n):
    data = [random.random() for _ in range(n)]

    # többféle művelet (CPU + memória)
    for _ in range(5):
        data = [x**2 + 3*x + 1 for x in data]
        data.sort()

    return sum(data)


if __name__ == "__main__":
    with ComputationalProfiler("heavy computation demo") as profiler:
        result = heavy_computation(200_000)

    print("\n=== RESULT ===")
    print(result)

    print("\n=== PROFILER OUTPUT ===")
    print(format_runtime_profile(profiler.result))