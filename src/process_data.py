import argparse
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def load_measurements(path):
    """Load logs and exclude warm-up runs without removing failures."""
    data = pd.read_json(path, lines=True)

    required = {
        "method", "phase", "input_rows",
        "repetition", "duration_ms", "success",
    }

    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    if not data["phase"].isin(["warmup", "measurement"]).all():
        raise ValueError("Unknown phase in the log.")

    measured = data.loc[data["phase"] == "measurement"].copy()

    if measured.empty:
        raise ValueError("No measured runs found.")

    if measured.duplicated(
        ["method", "input_rows", "repetition"]
    ).any():
        raise ValueError("Duplicate measurement records.")

    if not measured["success"].isin([True, False]).all():
        raise ValueError("Invalid success status.")

    durations = measured["duration_ms"]
    if not (np.isfinite(durations) & (durations >= 0)).all():
        raise ValueError("Invalid execution times.")

    return measured


def bootstrap_intervals(values, rng, n_bootstrap=5000):
    """Percentile bootstrap 95% CIs for median, p95 and p99."""
    samples = rng.choice(
        values,
        size=(n_bootstrap, len(values)),
        replace=True,
    )

    estimates = np.quantile(
        samples,
        [0.50, 0.95, 0.99],
        axis=1,
        method="linear",
    )

    intervals = np.quantile(
        estimates,
        [0.025, 0.975],
        axis=1,
        method="linear",
    )

    return {
        "median_ci_low_ms": float(intervals[0, 0]),
        "median_ci_high_ms": float(intervals[1, 0]),
        "p95_ci_low_ms": float(intervals[0, 1]),
        "p95_ci_high_ms": float(intervals[1, 1]),
        "p99_ci_low_ms": float(intervals[0, 2]),
        "p99_ci_high_ms": float(intervals[1, 2]),
    }


def summarize_measurements(data, seed=42, n_bootstrap=5000):
    """Summarize each method and workload separately."""
    if n_bootstrap < 1:
        raise ValueError("n_bootstrap must be positive.")

    rng = np.random.default_rng(seed)
    rows = []

    for (method, input_rows), group in data.groupby(
        ["method", "input_rows"], sort=True
    ):
        successful = group.loc[group["success"] == True]
        values = successful["duration_ms"].to_numpy(dtype=float)

        total = len(group)
        failed = total - len(values)

        row = {
            "method": method,
            "input_rows": int(input_rows),
            "total_runs": total,
            "successful_runs": len(values),
            "failed_runs": failed,
            "error_rate": failed / total,
            "latency_scope": "successful measured runs only",
            "mean_ms": np.nan,
            "sd_ms": np.nan,
            "median_ms": np.nan,
            "p25_ms": np.nan,
            "p75_ms": np.nan,
            "p95_ms": np.nan,
            "p99_ms": np.nan,
            "median_ci_low_ms": np.nan,
            "median_ci_high_ms": np.nan,
            "p95_ci_low_ms": np.nan,
            "p95_ci_high_ms": np.nan,
            "p99_ci_low_ms": np.nan,
            "p99_ci_high_ms": np.nan,
            "bootstrap_seed": seed,
            "bootstrap_resamples": n_bootstrap,
        }

        if len(values):
            p25, median, p75, p95, p99 = np.quantile(
                values,
                [0.25, 0.50, 0.75, 0.95, 0.99],
                method="linear",
            )

            row.update({
                "mean_ms": float(np.mean(values)),
                "sd_ms": (
                    float(np.std(values, ddof=1))
                    if len(values) > 1 else np.nan
                ),
                "median_ms": float(median),
                "p25_ms": float(p25),
                "p75_ms": float(p75),
                "p95_ms": float(p95),
                "p99_ms": float(p99),
            })

            if len(values) > 1:
                row.update(
                    bootstrap_intervals(
                        values, rng, n_bootstrap
                    )
                )

        rows.append(row)

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/raw/comparison_run.jsonl",
    )
    parser.add_argument(
        "--output",
        default="data/processed/metrics_summary.csv",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--bootstrap", type=int, default=5000)
    args = parser.parse_args()

    input_path = ROOT / args.input
    output_path = ROOT / args.output

    measured = load_measurements(input_path)

    summary = summarize_measurements(
        measured,
        seed=args.seed,
        n_bootstrap=args.bootstrap,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)

    columns = [
        "method", "input_rows", "successful_runs",
        "failed_runs", "median_ms",
        "median_ci_low_ms", "median_ci_high_ms",
        "p95_ms", "p99_ms",
    ]

    print(summary[columns].round(4).to_string(index=False))
    print(f"\nSummary saved to: {output_path}")


if __name__ == "__main__":
    main()
