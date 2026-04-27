from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from revcomp import ComputationalProfiler, format_runtime_profile


def test_runtime_profiler_creates_result():
    with ComputationalProfiler("test") as profiler:
        x = 0
        for i in range(10):
            x += i
    assert x == 45
    assert profiler.result is not None
    assert profiler.result.estimated_erased_bits > 0
    assert profiler.result.landauer_energy_joule > 0


def test_runtime_format_contains_warning():
    with ComputationalProfiler("test") as profiler:
        sum(range(5))
    text = format_runtime_profile(profiler.result)
    assert "not a real CPU wattmeter" in text
    assert "Landauer lower bound" in text
