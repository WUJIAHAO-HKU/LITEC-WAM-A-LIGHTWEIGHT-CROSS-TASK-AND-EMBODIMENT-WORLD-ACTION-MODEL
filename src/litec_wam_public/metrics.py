"""Statistics used by the reported LiteC-WAM evaluations.

The paired exact test follows the experiment's aggregation code. The public
version removes machine-specific paths and validates counts before computing.
All calculations use the Python standard library.
"""

from __future__ import annotations

import math
from statistics import NormalDist
from typing import Iterable


def _count(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")


def success_rate(successes: int, trials: int) -> float:
    _count(successes, "successes")
    _count(trials, "trials")
    if trials == 0 or successes > trials:
        raise ValueError("Require 0 <= successes <= trials and trials > 0")
    return successes / trials


def wilson_interval(successes: int, trials: int, confidence: float = 0.95) -> tuple[float, float]:
    """Return a two-sided Wilson score interval, as proportions."""
    p = success_rate(successes, trials)
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one")
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    denominator = 1 + z * z / trials
    center = (p + z * z / (2 * trials)) / denominator
    half = z * math.sqrt(p * (1 - p) / trials + z * z / (4 * trials * trials)) / denominator
    return max(0.0, center - half), min(1.0, center + half)


def exact_paired_test(condition_only: int, reference_only: int) -> float:
    """Two-sided exact McNemar test using discordant paired outcomes.

    The same binomial test can be used on counts of positive/negative seed
    differences. Ties do not contribute to the seed-level sign test.
    """
    _count(condition_only, "condition_only")
    _count(reference_only, "reference_only")
    n = condition_only + reference_only
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, k) for k in range(min(condition_only, reference_only) + 1))
    return min(1.0, (2 * tail) / (1 << n))


def task_macro_rate(tasks: Iterable[tuple[int, int]]) -> float:
    """Average task-level rates with equal task weight, not pooled trials."""
    rates = [success_rate(successes, trials) for successes, trials in tasks]
    if not rates:
        raise ValueError("At least one task is required")
    return sum(rates) / len(rates)
