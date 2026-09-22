"""Recompute reported statistics without running policy evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .metrics import exact_paired_test, success_rate, task_macro_rate, wilson_interval


def summarize_counts(row: dict) -> dict:
    successes, trials = row["successes"], row["trials"]
    low, high = wilson_interval(successes, trials)
    return {"successes": successes, "trials": trials,
            "rate_percent": 100 * success_rate(successes, trials),
            "wilson_95_percent": [100 * low, 100 * high]}


def compute_report(data: dict) -> dict:
    if data.get("schema") != "litec-wam.public-reported-counts.v1":
        raise ValueError("Unsupported input schema")
    f = data["feedback"]
    n, world, zero = f["paired_trials"], f["with_feedback"], f["zeroed"]
    success_rate(world, n)
    success_rate(zero, n)
    p = exact_paired_test(f["feedback_only"], f["zeroed_only"])
    both = world - f["feedback_only"]
    neither = n - both - f["feedback_only"] - f["zeroed_only"]
    if both < 0 or neither < 0 or both + f["zeroed_only"] != zero:
        raise ValueError("Discordant pairs are inconsistent with total success counts")
    seeds = f["per_seed"]
    if len({row["seed"] for row in seeds}) != len(seeds):
        raise ValueError("Seed identifiers must be unique")
    for row in seeds:
        success_rate(row["with_feedback"], row["trials"])
        success_rate(row["zeroed"], row["trials"])
    if (sum(r["trials"] for r in seeds), sum(r["with_feedback"] for r in seeds), sum(r["zeroed"] for r in seeds)) != (n, world, zero):
        raise ValueError("Per-seed counts are inconsistent with aggregate counts")
    positive = sum(r["with_feedback"] > r["zeroed"] for r in seeds)
    negative = sum(r["with_feedback"] < r["zeroed"] for r in seeds)
    return {
        "scope": "Statistics from reported aggregate counts; no new policy rollouts",
        "libero": summarize_counts(data["libero"]),
        "rlbench": summarize_counts(data["rlbench"]),
        "real_robot": [{"task": r["task"], **summarize_counts(r)} for r in data["real_robot"]],
        "arx5_macro_percent": 100 * task_macro_rate((r["successes"], r["trials"]) for r in data["arx5"]["tasks"]),
        "feedback": {
            "gain_percentage_points": 100 * (world - zero) / n,
            "paired_exact_mcnemar_p": p,
            "positive_seeds": positive, "negative_seeds": negative,
            "seed_sign_test_p": exact_paired_test(positive, negative),
            "with_feedback": summarize_counts({"successes": world, "trials": n}),
            "zeroed": summarize_counts({"successes": zero, "trials": n}),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()
    report = compute_report(json.loads(args.results.read_text(encoding="utf-8")))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
