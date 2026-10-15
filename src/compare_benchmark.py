import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from analyze import derive_participant_level
from aggregation import derive_participant_level_proposed


ROOT = Path(__file__).resolve().parents[1]

METHODS = {
    "baseline": derive_participant_level,
    "proposed": derive_participant_level_proposed,
}


def timestamp():
    return datetime.now(timezone.utc).isoformat(
        timespec="microseconds"
    )


def project_path(value):
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def command_output(command):
    try:
        return subprocess.check_output(
            command,
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def make_workload(sample, copies, id_column):
    """Repeat the synthetic sample with unique participant IDs."""
    parts = []

    for copy_number in range(copies):
        part = sample.copy()
        part[id_column] = (
            part[id_column].astype(str)
            + f"_copy{copy_number}"
        )
        parts.append(part)

    return pd.concat(parts, ignore_index=True)


def check_equivalence(data, cfg):
    """Check outputs before benchmarking, outside timing."""
    id_column = cfg["columns"]["id"]

    baseline = METHODS["baseline"](data, cfg)
    proposed = METHODS["proposed"](data, cfg)

    baseline = (
        baseline.sort_values(id_column)
        .reset_index(drop=True)
    )
    proposed = (
        proposed.sort_values(id_column)
        .reset_index(drop=True)
    )
    proposed = proposed[baseline.columns]

    pd.testing.assert_frame_equal(baseline, proposed)

    return len(baseline)


def measure(function, data, cfg, expected_rows):
    started_at = timestamp()
    error = None
    result = None

    start = time.perf_counter_ns()

    try:
        result = function(data, cfg)
    except Exception as exc:
        elapsed_ns = time.perf_counter_ns() - start
        error = {
            "type": type(exc).__name__,
            "message": str(exc),
        }
    else:
        elapsed_ns = time.perf_counter_ns() - start

    # Output validation is outside the timed section.
    if error is None:
        if (
            not isinstance(result, pd.DataFrame)
            or len(result) != expected_rows
        ):
            error = {
                "type": "InvalidOutput",
                "message": "Unexpected output type or row count.",
            }

    return {
        "timestamp_utc": started_at,
        "duration_ms": elapsed_ns / 1_000_000,
        "success": error is None,
        "error": error,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="configs/config.yaml",
    )
    args = parser.parse_args()

    config_path = project_path(args.config)

    with config_path.open(encoding="utf-8") as file:
        cfg = yaml.safe_load(file)

    settings = cfg["comparison"]

    warmup_runs = int(settings["warmup_runs"])
    measured_runs = int(settings["measured_runs"])
    copies_list = [int(x) for x in settings["sample_copies"]]
    seed = int(cfg["reproducibility"]["random_seed"])

    if warmup_runs < 1 or measured_runs < 100:
        raise ValueError(
            "Use at least 1 warm-up and 100 measured runs."
        )

    if (
        not copies_list
        or any(x < 1 for x in copies_list)
        or len(set(copies_list)) != len(copies_list)
    ):
        raise ValueError("sample_copies must be unique positive integers.")

    rng = np.random.default_rng(seed)

    input_path = project_path(settings["input_path"])
    output_path = project_path(settings["output_path"])

    # File reading and workload generation are outside timing.
    sample = pd.read_csv(input_path)

    if sample.empty:
        raise ValueError("The synthetic sample is empty.")

    id_column = cfg["columns"]["id"]

    # Randomise workload order to reduce systematic order effects.
    workload_order = list(rng.permutation(copies_list))
    records = []

    for copies in workload_order:
        copies = int(copies)
        data = make_workload(sample, copies, id_column)

        expected_rows = check_equivalence(data, cfg)

        print(
            f"Outputs match: {len(data)} input rows, "
            f"{expected_rows} participants.",
            flush=True,
        )

        for phase, count in [
            ("warmup", warmup_runs),
            ("measurement", measured_runs),
        ]:
            for repetition in range(1, count + 1):
                # Both methods run once in each paired repetition.
                # Their order changes randomly.
                method_order = rng.permutation(list(METHODS))

                for position, method in enumerate(method_order, start=1):
                    method = str(method)

                    record = measure(
                        METHODS[method],
                        data,
                        cfg,
                        expected_rows,
                    )

                    record.update({
                        "method": method,
                        "phase": phase,
                        "repetition": repetition,
                        "order_in_pair": position,
                        "sample_copies": copies,
                        "input_rows": len(data),
                        "expected_output_rows": expected_rows,
                    })

                    records.append(record)

        print(
            f"Finished both methods for {len(data)} rows.",
            flush=True,
        )

    # Logs are written after all timed runs.
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                    allow_nan=False,
                ) + "\n"
            )

    ram_bytes = command_output(["sysctl", "-n", "hw.memsize"])

    metadata = {
        "timestamp_utc": timestamp(),
        "experiment": "baseline_vs_proposed_aggregation",
        "data_type": "repeated synthetic sample",
        "workload_note": (
            "Sample copies have unique participant IDs. "
            "This tests input size and group-count scaling, "
            "not real student behaviour."
        ),
        "methods": {
            "baseline": "analyze.derive_participant_level",
            "proposed": "aggregation.derive_participant_level_proposed",
        },
        "equivalence_check": "passed for all workloads",
        "python": sys.version,
        "os": platform.platform(),
        "cpu_model": (
            command_output(["sysctl", "-n", "machdep.cpu.brand_string"])
            or platform.processor()
            or "not reported"
        ),
        "ram_gib": (
            round(int(ram_bytes) / (1024 ** 3), 2)
            if ram_bytes and ram_bytes.isdigit()
            else None
        ),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "pyyaml": yaml.__version__,
        "random_seed": seed,
        "workload_order": [int(x) for x in workload_order],
        "input_sha256": hashlib.sha256(
            input_path.read_bytes()
        ).hexdigest(),
        "git_commit": command_output(["git", "rev-parse", "HEAD"]),
        "config": cfg,
    }

    metadata_path = output_path.with_name(
        output_path.stem + "_metadata.json"
    )

    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )

    measured = [
        record for record in records
        if record["phase"] == "measurement"
    ]

    print("\nMeasured runs by method and input size:")

    for copies in sorted(copies_list):
        for method in METHODS:
            group = [
                record for record in measured
                if record["sample_copies"] == copies
                and record["method"] == method
            ]
            times = [
                record["duration_ms"]
                for record in group
                if record["success"]
            ]
            failures = sum(not record["success"] for record in group)

            median_text = (
                f"{np.median(times):.3f} ms"
                if times else "unavailable"
            )

            print(
                f"{method}: rows={len(sample) * copies}, "
                f"successful={len(times)}, failed={failures}, "
                f"median={median_text}"
            )

    print(f"\nLog saved to: {output_path}")

    if any(not record["success"] for record in records):
        raise SystemExit(
            "Some runs failed. Inspect the log before analysis."
        )


if __name__ == "__main__":
    main()
