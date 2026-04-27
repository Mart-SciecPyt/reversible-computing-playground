from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from revcomp.code_analyzer import analyze_python_file, format_operation_profile


def test_analyze_sample_program():
    profile = analyze_python_file(PROJECT_ROOT / "examples" / "sample_program.py")
    assert profile.estimated_operations > 0
    assert profile.estimated_erased_bits > 0
    assert profile.landauer_energy_joule > 0
    assert profile.function_calls >= 1


def test_format_operation_profile_contains_warning():
    profile = analyze_python_file(PROJECT_ROOT / "examples" / "sample_program.py")
    text = format_operation_profile(profile)
    assert "not a real CPU power measurement" in text
    assert "Landauer lower bound" in text
