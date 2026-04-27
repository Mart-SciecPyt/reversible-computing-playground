"""Runtime profiler for educational Physics of Computing estimates.

This is not a hardware-accurate CPU power meter. It measures Python-level
runtime signals and converts them into a coarse Landauer lower-bound estimate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
import time
import tracemalloc
from typing import Callable, ParamSpec, TypeVar

from .landauer import total_erasure_energy

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True)
class RuntimeProfile:
    label: str
    wall_time_seconds: float
    cpu_time_seconds: float
    peak_memory_bytes: int
    temperature_kelvin: float
    bits_per_event: int
    estimated_events: int
    estimated_erased_bits: int
    landauer_energy_joule: float
    notes: list[str] = field(default_factory=list)

    @property
    def peak_memory_megabytes(self) -> float:
        return self.peak_memory_bytes / (1024 * 1024)

    def as_dict(self) -> dict[str, int | float | str | list[str]]:
        return self.__dict__.copy()


class ComputationalProfiler:
    """Context manager for lightweight runtime profiling."""

    def __init__(self, label: str = "profiled block", temperature_kelvin: float = 300.0, bits_per_event: int = 64) -> None:
        if temperature_kelvin <= 0:
            raise ValueError("temperature_kelvin must be positive.")
        if bits_per_event <= 0:
            raise ValueError("bits_per_event must be positive.")
        self.label = label
        self.temperature_kelvin = temperature_kelvin
        self.bits_per_event = bits_per_event
        self.result: RuntimeProfile | None = None
        self._start_wall = 0.0
        self._start_cpu = 0.0

    def __enter__(self) -> "ComputationalProfiler":
        self.result = None
        tracemalloc.start()
        self._start_wall = time.perf_counter()
        self._start_cpu = time.process_time()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        cpu_time = time.process_time() - self._start_cpu
        wall_time = time.perf_counter() - self._start_wall
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Educational score, not real instruction count.
        # CPU time dominates, memory contributes weakly.
        time_events = max(1, int(cpu_time * 1_000_000))
        memory_events = max(0, int(peak / 1024))
        estimated_events = time_events + memory_events
        estimated_erased_bits = estimated_events * self.bits_per_event
        landauer_energy = total_erasure_energy(estimated_erased_bits, self.temperature_kelvin)

        self.result = RuntimeProfile(
            label=self.label,
            wall_time_seconds=wall_time,
            cpu_time_seconds=cpu_time,
            peak_memory_bytes=peak,
            temperature_kelvin=self.temperature_kelvin,
            bits_per_event=self.bits_per_event,
            estimated_events=estimated_events,
            estimated_erased_bits=estimated_erased_bits,
            landauer_energy_joule=landauer_energy,
            notes=[
                "This is an educational computational-effort estimate, not a real CPU wattmeter.",
                "The Landauer value is a theoretical lower bound and is far below real hardware energy use.",
                "The event estimate is based on CPU time and traced peak memory, not actual machine instructions.",
            ],
        )
        return False


def format_runtime_profile(profile: RuntimeProfile) -> str:
    lines = [
        "Runtime Computational-Effort Report",
        "===================================",
        f"Label: {profile.label}",
        f"Wall time:              {profile.wall_time_seconds:.6f} s",
        f"CPU time:               {profile.cpu_time_seconds:.6f} s",
        f"Peak traced memory:     {profile.peak_memory_megabytes:.3f} MB",
        "",
        "Educational Landauer estimate:",
        f"Temperature:            {profile.temperature_kelvin:.2f} K",
        f"Bits per event:         {profile.bits_per_event}",
        f"Estimated events:       {profile.estimated_events}",
        f"Estimated erased bits:  {profile.estimated_erased_bits}",
        f"Landauer lower bound:   {profile.landauer_energy_joule:.3e} J",
        "",
        "Important notes:",
    ]
    lines.extend(f"- {note}" for note in profile.notes)
    return "\n".join(lines)


def profiled(label: str | None = None, temperature_kelvin: float = 300.0, bits_per_event: int = 64) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            profile_label = label or func.__name__
            with ComputationalProfiler(profile_label, temperature_kelvin=temperature_kelvin, bits_per_event=bits_per_event) as profiler:
                output = func(*args, **kwargs)
            if profiler.result is not None:
                print(format_runtime_profile(profiler.result))
            return output
        return wrapper
    return decorator
