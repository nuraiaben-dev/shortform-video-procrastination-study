import argparse
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from analyze import derive_participant_level


ROOT = Path(__file__).resolve().parents[1]


def project_path(value):
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def timestamp():
    return datetime.now(timezone.utc).isoformat(
        timespec="microseconds"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="configs/config.yaml",
    )
    args = parser.parse_args()

    with project_path(args.config).open(
        encoding="utf-8"
    ) as file:
        cfg = yaml.safe_load(file)

    settings = cfg.get("benchmark", {})
    warmup_runs = int(settings.get("warmup_runs", 10))
    measured_runs = int(settings.get("measured_runs", 100))
    seed = int(cfg["reproducibility"].get("random_seed", 42))

    if warmup_runs < 0 or measured_runs < 100:
        raise ValueError(
            "Use warmup_runs >= 0 and measured_runs >= 100."
        )

    np.random.seed(seed)

    input_path = project_path(
        settings.get("input_path", cfg["data"]["sample_path"])
    )
    output_path = project_path(
        settings.get("output_path", "data/raw/test_run.jsonl")
    )

    # Reading the CSV is outside the timed function.
    data = pd.read_csv(input_path)
    records = []

    for run in range(warmup_runs + measured_runs):
        phase = "warmup" if run < warmup_runs else "measurement"
        started_at = timestamp()
        error = None
        result = None

        # Only the target function is timed.
        start = time.perf_counter_ns()

        try:
            result = derive_participant_level(data, cfg)
        except Exception as exc:
            elapsed_ns = time.perf_counter_ns() - start
            error = {
                "type": type(exc).__name__,
                "message": str(exc),
            }
        else:
            elapsed_ns = time.perf_counter_ns() - start

        # Validation and logging preparation are outside timing.
        if error is None:
            if not isinstance(result, pd.DataFrame) or result.empty:
                error = {
                    "type": "InvalidOutput",
                    "message": "Expected a non-empty DataFrame.",
                }

        records.append({
            "run": run + 1,
            "phase": phase,
            "timestamp_utc": started_at,
            "duration_ms": elapsed_ns / 1_000_000,
            "success": error is None,
            "error": error,
            "input_rows": len(data),
            "output_rows": (
                len(result)
                if isinstance(result, pd.DataFrame)
                else None
            ),
        })

    measured = [
        record for record in records
        if record["phase"] == "measurement"
    ]
    successful_times = [
        record["duration_ms"]
        for record in measured
        if record["success"]
    ]
    failed_runs = sum(
        not record["success"] for record in measured
    )

    summary = {
        "measured_runs": measured_runs,
        "successful_runs": len(successful_times),
        "failed_runs": failed_runs,
        "error_rate": failed_runs / measured_runs,
        "latency_scope": "successful measured runs only",
        "mean_ms": None,
        "median_ms": None,
        "p95_ms": None,
        "p99_ms": None,
    }

    if successful_times:
        summary.update({
            "mean_ms": float(np.mean(successful_times)),
            "median_ms": float(np.median(successful_times)),
            "p95_ms": float(np.percentile(
                successful_times, 95, method="linear"
            )),
            "p99_ms": float(np.percentile(
                successful_times, 99, method="linear"
            )),
        })

    metadata = {
        "timestamp_utc": timestamp(),
        "target_function": "derive_participant_level",
        "python": sys.version,
        "os": platform.platform(),
        "cpu": platform.processor() or "not reported",
        "logical_cpu_count": __import__("os").cpu_count(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "pyyaml": yaml.__version__,
        "input_path": str(input_path),
        "input_rows": len(data),
        "warmup_runs": warmup_runs,
        "measured_runs": measured_runs,
        "random_seed": seed,
        "config": cfg,
    }

    # All file writes happen after the timed runs.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(
                record, ensure_ascii=False, allow_nan=False
            ) + "\n")

    metadata_path = output_path.with_name(
        output_path.stem + "_metadata.json"
    )
    summary_path = output_path.with_name(
        output_path.stem + "_summary.json"
    )

    for path, content in [
        (metadata_path, metadata),
        (summary_path, summary),
    ]:
        with path.open("w", encoding="utf-8") as file:
            json.dump(
                content, file, indent=2,
                ensure_ascii=False, allow_nan=False
            )

    print(json.dumps(summary, indent=2))
    print(f"Measurements saved to: {output_path}")

    if failed_runs:
        raise SystemExit(
            "Some measured runs failed. Check the JSONL log."
        )


if __name__ == "__main__":
    main()
