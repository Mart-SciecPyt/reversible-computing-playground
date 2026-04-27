"""Analyze a Python file and estimate its Landauer lower-bound energy.

Usage from project root:
    python examples/analyze_python_file.py examples/sample_program.py
    python examples/analyze_python_file.py examples/sample_program.py --temperature 300 --bits-per-operation 64
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from revcomp.code_analyzer import analyze_python_file, format_operation_profile


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Static Python-code analyzer for educational Landauer-limit estimates."
    )
    parser.add_argument("file", help="Path to the Python file to analyze.")
    parser.add_argument(
        "--temperature",
        type=float,
        default=300.0,
        help="Temperature in kelvin. Default: 300 K.",
    )
    parser.add_argument(
        "--bits-per-operation",
        type=int,
        default=64,
        help="Educational erased-bit assumption per weighted operation. Default: 64.",
    )
    args = parser.parse_args()

    profile = analyze_python_file(
        args.file,
        temperature_kelvin=args.temperature,
        bits_per_operation=args.bits_per_operation,
    )
    print(format_operation_profile(profile))


if __name__ == "__main__":
    main()
