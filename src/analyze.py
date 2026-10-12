#!/usr/bin/env python3
"""
Main analysis pipeline for the short-form video / procrastination study.

Reads a config file and a per-day diary CSV, derives participant-level
exposure variables (X, S, B) and outcomes (P, L, A), then runs:

  - RQ2: Spearman correlation between X (mean daily viewing) and
         P (Tuckman procrastination score), one-sided (H1: rho > 0).
  - RQ3: Poisson / Negative-Binomial count model of late tasks (L)
         with log(A) offset, predictors S and B (and X as covariate).

Writes a log file to results/run.log.

Usage:
    python src/analyze.py --config configs/config.yaml \
                          --input data/sample/sample_data.csv
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy import stats

try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    HAVE_STATSMODELS = True
except ImportError:
    HAVE_STATSMODELS = False


# ----------------------------------------------------------------------
# Config loading
# ----------------------------------------------------------------------
def load_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
def setup_logging(log_file: str | Path) -> logging.Logger:
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("analyze")
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger


# ----------------------------------------------------------------------
# Variable derivation
# ----------------------------------------------------------------------
def derive_participant_level(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Collapse per-day rows into one row per participant."""
    col = cfg["columns"]
    var = cfg["variables"]

    df = df.copy()

    # Drop rows with impossible values (defensive check)
    df = df[df[col["viewing_minutes"]] >= 0]

    # Count valid diary days per participant
    valid = (
        df.groupby(col["id"])
        .size()
        .rename("valid_days")
        .reset_index()
    )

    # Mean daily viewing X
    x = (
        df.groupby(col["id"])[col["viewing_minutes"]]
        .sum()
        .rename("sum_viewing")
        .reset_index()
    )
    # Study-time viewing proportion S
    s = (
        df.groupby(col["id"])[col["study_time_viewing"]]
        .sum()
        .rename("sum_study")
        .reset_index()
    )
    # Bedtime viewing proportion B
    b = (
        df.groupby(col["id"])[col["bedtime_viewing"]]
        .sum()
        .rename("sum_bedtime")
        .reset_index()
    )
    # Tuckman score P (one value per participant — take first)
    p = (
        df.groupby(col["id"])[col["tuckman_score"]]
        .first()
        .rename("P")
        .reset_index()
    )
    # Late tasks L and tasks due A (sum over the window)
    l = (
        df.groupby(col["id"])[col["late_tasks"]]
        .sum()
        .rename("L")
        .reset_index()
    )
    a = (
        df.groupby(col["id"])[col["tasks_due"]]
        .sum()
        .rename("A")
        .reset_index()
    )

    merged = valid.merge(x, on=col["id"]).merge(s, on=col["id"])
    merged = merged.merge(b, on=col["id"]).merge(p, on=col["id"])
    merged = merged.merge(l, on=col["id"]).merge(a, on=col["id"])

    merged["X"] = merged["sum_viewing"] / merged["valid_days"]
    merged["S"] = merged["sum_study"] / merged["valid_days"]
    merged["B"] = merged["sum_bedtime"] / merged["valid_days"]

    return merged


# ----------------------------------------------------------------------
# RQ2 — Spearman correlation
# ----------------------------------------------------------------------
def run_rq2(df: pd.DataFrame, cfg: dict, logger: logging.Logger) -> dict:
    logger.info("=" * 70)
    logger.info("RQ2: Spearman correlation between X (viewing) and P (procrastination)")
    logger.info("=" * 70)

    x = df["X"].to_numpy()
    p = df["P"].to_numpy()

    if len(x) < 3:
        logger.warning("Not enough participants for a stable correlation (n=%d).", len(x))
        return {"rho": np.nan, "p_value": np.nan, "n": len(x)}

    alternative = cfg["analysis"]["spearman"].get("alternative", "greater")
    rho, pval = stats.spearmanr(x, p, alternative=alternative)

    logger.info("n          = %d", len(x))
    logger.info("Spearman ρ = %.4f", rho)
    logger.info("p-value    = %.4f  (alternative: %s)", pval, alternative)

    if pval < cfg["analysis"]["alpha"]:
        logger.info("→ Result: REJECT H0 (ρ > 0 is supported at α=%.2f).", cfg["analysis"]["alpha"])
    else:
        logger.info("→ Result: FAIL TO REJECT H0 (no significant positive association).")

    return {"rho": float(rho), "p_value": float(pval), "n": int(len(x))}


# ----------------------------------------------------------------------
# RQ3 — Count model with offset
# ----------------------------------------------------------------------
def run_rq3(df: pd.DataFrame, cfg: dict, logger: logging.Logger) -> dict:
    logger.info("=" * 70)
    logger.info("RQ3: Count model for late tasks L ~ S + B (+ X), offset = log(A)")
    logger.info("=" * 70)

    if not HAVE_STATSMODELS:
        logger.warning("statsmodels not installed — skipping RQ3 model.")
        return {"irr_S": np.nan, "irr_B": np.nan, "model": None}

    # Only participants with at least one eligible deadline
    d = df[df["A"] > 0].copy()

    if len(d) < 3:
        logger.warning("Fewer than 3 participants with A > 0 (n=%d). Skipping model.", len(d))
        return {"irr_S": np.nan, "irr_B": np.nan, "model": None}

    # Scale X down so the coefficient isn't microscopic (per 100 minutes)
    d["X100"] = d["X"] / 100.0

    formula = "L ~ S + B + X100"
    logger.info("Formula: %s", formula)
    logger.info("n participants with A > 0: %d", len(d))

    try:
        model = smf.glm(
            formula=formula,
            data=d,
            family=sm.families.Poisson(),
            offset=np.log(d["A"].to_numpy()),
        ).fit()
        logger.info("Fitted model: Poisson GLM")
        logger.info("\n%s", model.summary().as_text())
    except Exception as exc:
        logger.warning("Poisson fit failed (%s). Trying Negative Binomial…", exc)
        try:
            model = smf.glm(
                formula=formula,
                data=d,
                family=sm.families.NegativeBinomial(),
                offset=np.log(d["A"].to_numpy()),
            ).fit()
            logger.info("Fitted model: Negative Binomial GLM")
            logger.info("\n%s", model.summary().as_text())
        except Exception as exc2:
            logger.error("Both models failed: %s", exc2)
            return {"irr_S": np.nan, "irr_B": np.nan, "model": None}

    irr_S = float(np.exp(model.params.get("S", np.nan)))
    irr_B = float(np.exp(model.params.get("B", np.nan)))

    logger.info("IRR for S (study-time viewing): %.4f", irr_S)
    logger.info("IRR for B (bedtime viewing):    %.4f", irr_B)
    logger.info("Interpretation: IRR > 1 → more late tasks associated with the pattern.")

    return {"irr_S": irr_S, "irr_B": irr_B, "model": model}


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Analysis pipeline for the short-form video study.")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--input", required=True, help="Path to diary CSV")
    args = parser.parse_args()

    cfg = load_config(args.config)
    log_path = cfg["reproducibility"].get("log_file", "results/run.log")
    logger = setup_logging(log_path)

    logger.info("Config loaded from %s", args.config)
    logger.info("Input data: %s", args.input)

    np.random.seed(cfg["reproducibility"].get("random_seed", 42))

    df_raw = pd.read_csv(args.input)
    logger.info("Loaded %d raw rows from %s", len(df_raw), args.input)

    df = derive_participant_level(df_raw, cfg)
    logger.info("Derived participant-level table with %d participants", len(df))
    logger.info("\n%s", df.to_string(index=False))

    rq2 = run_rq2(df, cfg, logger)
    rq3 = run_rq3(df, cfg, logger)

    logger.info("=" * 70)
    logger.info("SUMMARY")
    logger.info("=" * 70)
    logger.info("RQ2: ρ = %.4f, p = %.4f, n = %d", rq2["rho"], rq2["p_value"], rq2["n"])
    logger.info("RQ3: IRR(S) = %.4f, IRR(B) = %.4f", rq3["irr_S"], rq3["irr_B"])
    logger.info("Log saved to: %s", log_path)
    logger.info("Analysis complete.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
