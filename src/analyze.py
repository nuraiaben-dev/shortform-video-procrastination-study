#!/usr/bin/env python3
"""
Main analysis pipeline for the short-form video / procrastination study.

Unit of analysis: the PARTICIPANT. The raw file has one row per
participant-day, but the procrastination score P is measured once per
participant, so every inferential step works on the participant-level
table (one row per participant) and the bootstrap resamples participants,
never rows.

Pipeline
    1. validate_diary            - cleaning rules and data-quality report
    2. derive_participant_level  - X, S, B, P, L, A per participant
    3. RQ1  descriptive estimates with bootstrap 95% CI
    4. RQ2  one-sided Spearman correlation between X and P
    5. RQ3  Poisson model for late tasks L with offset log(A)
    6. guardrails: diary completeness and proxy discrepancy

Usage:
    python src/analyze.py --config configs/config.yaml \
                          --input data/raw/real_data.csv
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy import stats

from common import add_late_tasks


# ----------------------------------------------------------------------
# Config and logging
# ----------------------------------------------------------------------
def load_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_logging(log_file: str | Path) -> logging.Logger:
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("analyze")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    fh = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger


# ----------------------------------------------------------------------
# 1. Validation and cleaning (day level)
# ----------------------------------------------------------------------
def validate_diary(df: pd.DataFrame, cfg: dict) -> tuple[pd.DataFrame, dict]:
    """Apply the predefined cleaning rules and report what was removed.

    Rules (each row is dropped at the first rule it fails):
      1. missing value in a required column
      2. diary day not completed (diary_completed != 1)
      3. negative viewing minutes
      4. more tasks completed than planned
      5. duplicate participant-date record (first kept)
    Participant-level exclusion (< min_valid_days) is applied later.
    """
    col = cfg["columns"]
    required = [col[k] for k in (
        "id", "date", "viewing_minutes", "study_time_viewing",
        "bedtime_viewing", "tuckman_score", "tasks_due",
        "tasks_completed", "diary_completed",
    )]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise KeyError(f"Input is missing required columns: {missing_cols}")

    report = {"rows_input": int(len(df)),
              "participants_input": int(df[col["id"]].nunique())}
    data = df.copy()

    def drop(mask, key):
        nonlocal data
        report[key] = int(mask.sum())
        data = data[~mask]

    drop(data[required].isna().any(axis=1), "dropped_missing_values")
    drop(data[col["diary_completed"]] != 1, "dropped_diary_not_completed")
    drop(data[col["viewing_minutes"]] < 0, "dropped_negative_viewing")
    drop(data[col["tasks_completed"]] > data[col["tasks_due"]],
         "dropped_completed_gt_planned")
    drop(data.duplicated([col["id"], col["date"]]), "dropped_duplicates")

    # Consistency checks that are reported but do not remove rows.
    if col["deadline_status"] in data.columns:
        status = data[col["deadline_status"]]
        done = data[col["tasks_completed"]]
        planned = data[col["tasks_due"]]
        report["check_on_time_but_unfinished"] = int(
            ((status == "on_time") & (done < planned)).sum())
        report["check_missed_but_completed"] = int(
            ((status == "missed") & (done > 0)).sum())
    if col["screen_time_minutes"] in data.columns:
        report["days_screen_lt_viewing"] = int(
            (data[col["screen_time_minutes"]]
             < data[col["viewing_minutes"]]).sum())

    # P must be constant within a participant.
    nun = data.groupby(col["id"])[col["tuckman_score"]].nunique()
    report["participants_with_changing_P"] = int((nun > 1).sum())

    report["rows_clean"] = int(len(data))
    report["participants_clean"] = int(data[col["id"]].nunique())
    return data.reset_index(drop=True), report


# ----------------------------------------------------------------------
# 2. Participant-level derivation (also the timed baseline in benchmark)
# ----------------------------------------------------------------------
def derive_participant_level(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Collapse per-day rows into one row per participant (baseline).

    Separate grouped aggregations followed by merges; the proposed
    one-pass version lives in aggregation.py and must give the same table.
    """
    col = cfg["columns"]

    df = df[df[col["viewing_minutes"]] >= 0]
    df = add_late_tasks(df, cfg)

    valid = df.groupby(col["id"]).size().rename("valid_days").reset_index()
    x = (df.groupby(col["id"])[col["viewing_minutes"]].sum()
         .rename("sum_viewing").reset_index())
    s = (df.groupby(col["id"])[col["study_time_viewing"]].sum()
         .rename("sum_study").reset_index())
    b = (df.groupby(col["id"])[col["bedtime_viewing"]].sum()
         .rename("sum_bedtime").reset_index())
    p = (df.groupby(col["id"])[col["tuckman_score"]].first()
         .rename("P").reset_index())
    l = (df.groupby(col["id"])[col["late_tasks"]].sum()
         .rename("L").reset_index())
    a = (df.groupby(col["id"])[col["tasks_due"]].sum()
         .rename("A").reset_index())

    merged = valid.merge(x, on=col["id"]).merge(s, on=col["id"])
    merged = merged.merge(b, on=col["id"]).merge(p, on=col["id"])
    merged = merged.merge(l, on=col["id"]).merge(a, on=col["id"])

    merged["X"] = merged["sum_viewing"] / merged["valid_days"]
    merged["S"] = merged["sum_study"] / merged["valid_days"]
    merged["B"] = merged["sum_bedtime"] / merged["valid_days"]
    return merged


def add_participant_covariates(part: pd.DataFrame, diary: pd.DataFrame,
                               cfg: dict) -> pd.DataFrame:
    """Attach age, gender and mean device screen time to the participant table."""
    col = cfg["columns"]
    extra = {}
    if col["age"] in diary.columns:
        extra["age"] = (col["age"], "first")
    if col["gender"] in diary.columns:
        extra["gender"] = (col["gender"], "first")
    if col["screen_time_minutes"] in diary.columns:
        extra["screen_mean"] = (col["screen_time_minutes"], "mean")
    if not extra:
        return part
    cov = diary.groupby(col["id"]).agg(**extra).reset_index()
    return part.merge(cov, on=col["id"], how="left")


def apply_completeness_guardrail(part: pd.DataFrame, cfg: dict):
    """Keep participants with at least min_valid_days valid diary days."""
    min_days = cfg["observation"]["min_valid_days"]
    keep = part["valid_days"] >= min_days
    info = {
        "min_valid_days": int(min_days),
        "participants_before": int(len(part)),
        "participants_excluded": int((~keep).sum()),
        "participants_analysed": int(keep.sum()),
        "valid_days_min": int(part["valid_days"].min()),
        "valid_days_median": float(part["valid_days"].median()),
        "valid_days_max": int(part["valid_days"].max()),
        "completeness_mean_pct": float(
            100 * part["valid_days"].mean() / cfg["observation"]["total_days"]),
    }
    return part[keep].reset_index(drop=True), info


# ----------------------------------------------------------------------
# Statistical helpers
# ----------------------------------------------------------------------
def bootstrap_ci(values: np.ndarray, stat=np.mean, n_boot: int = 2000,
                 seed: int = 42, level: float = 95.0):
    """Percentile bootstrap CI; `values` must be one value per participant."""
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(values), size=(n_boot, len(values)))
    boot = np.array([stat(values[i]) for i in idx])
    lo, hi = np.percentile(boot, [(100 - level) / 2, 100 - (100 - level) / 2])
    return float(lo), float(hi)


def bootstrap_ratio_ci(num: np.ndarray, den: np.ndarray, n_boot: int = 2000,
                       seed: int = 42, scale: float = 100.0):
    """Bootstrap CI for a pooled rate scale * sum(num) / sum(den)."""
    num = np.asarray(num, dtype=float)
    den = np.asarray(den, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(num), size=(n_boot, len(num)))
    boot = scale * num[idx].sum(axis=1) / den[idx].sum(axis=1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return float(scale * num.sum() / den.sum()), float(lo), float(hi)


def holm_adjust(pvalues):
    """Holm step-down adjusted p-values (same order as input)."""
    p = np.asarray(pvalues, dtype=float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj


def poisson_glm(X: np.ndarray, y: np.ndarray, offset: np.ndarray,
                max_iter: int = 100, tol: float = 1e-10) -> dict:
    """Poisson GLM (log link, offset) fitted by IRLS, with robust SEs.

    Standard errors are the HC1 sandwich estimator, which stays valid under
    mild over-dispersion. Returns coefficients, SEs and Pearson dispersion.
    """
    n, k = X.shape
    beta = np.zeros(k)
    beta[0] = np.log(y.sum() / np.exp(offset).sum())  # intercept start
    for _ in range(max_iter):
        mu = np.exp(X @ beta + offset)
        z = X @ beta + (y - mu) / mu
        new = np.linalg.solve(X.T @ (mu[:, None] * X), X.T @ (mu * z))
        done = np.max(np.abs(new - beta)) < tol
        beta = new
        if done:
            break
    else:
        raise RuntimeError("Poisson IRLS did not converge")

    mu = np.exp(X @ beta + offset)
    bread = np.linalg.inv(X.T @ (mu[:, None] * X))
    resid = y - mu
    meat = X.T @ ((resid ** 2)[:, None] * X)
    cov = (n / (n - k)) * bread @ meat @ bread
    return {
        "beta": beta,
        "se": np.sqrt(np.diag(cov)),
        "dispersion": float(np.sum(resid ** 2 / mu) / (n - k)),
        "n": int(n),
    }


# ----------------------------------------------------------------------
# RQ1 - descriptive
# ----------------------------------------------------------------------
def run_rq1(part: pd.DataFrame, cfg: dict, logger=None) -> pd.DataFrame:
    n_boot = cfg["reproducibility"]["n_bootstrap"]
    seed = cfg["reproducibility"]["random_seed"]
    rows = []
    for name, series, unit in (
        ("X: mean daily viewing", part["X"], "min/day"),
        ("P: Tuckman score", part["P"], "points"),
        ("S: study-time viewing", part["S"], "share of days"),
        ("B: bedtime viewing", part["B"], "share of days"),
    ):
        lo, hi = bootstrap_ci(series.to_numpy(), np.mean, n_boot, seed)
        rows.append({
            "Variable": name, "Unit": unit, "N": len(series),
            "Mean": series.mean(), "SD": series.std(ddof=1),
            "Median": series.median(), "CI95_Lower": lo, "CI95_Upper": hi,
        })
    r, lo, hi = bootstrap_ratio_ci(part["L"], part["A"], n_boot, seed)
    rows.append({
        "Variable": "R: late-task rate (pooled)", "Unit": "%", "N": len(part),
        "Mean": r, "SD": np.nan, "Median": np.nan,
        "CI95_Lower": lo, "CI95_Upper": hi,
    })
    out = pd.DataFrame(rows)
    if logger:
        logger.info("RQ1 descriptive estimates (participant level, "
                    "bootstrap of participants):\n%s",
                    out.round(2).to_string(index=False))
    return out


# ----------------------------------------------------------------------
# RQ2 - Spearman
# ----------------------------------------------------------------------
def run_rq2(part: pd.DataFrame, cfg: dict, logger=None) -> dict:
    alt = cfg["analysis"]["spearman"].get("alternative", "greater")
    n_boot = cfg["reproducibility"]["n_bootstrap"]
    seed = cfg["reproducibility"]["random_seed"]
    x, p = part["X"].to_numpy(), part["P"].to_numpy()
    if len(x) < 3:
        return {"rho": np.nan, "p_value": np.nan, "n": len(x),
                "ci_lower": np.nan, "ci_upper": np.nan}

    rho, pval = stats.spearmanr(x, p, alternative=alt)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    boot = np.array([stats.spearmanr(x[i], p[i])[0] for i in idx])
    lo, hi = np.percentile(boot, [2.5, 97.5])

    res = {"rho": float(rho), "p_value": float(pval), "n": int(len(x)),
           "ci_lower": float(lo), "ci_upper": float(hi),
           "alternative": alt}
    if logger:
        logger.info("RQ2: Spearman rho = %.3f, 95%% bootstrap CI [%.3f, %.3f], "
                    "p = %.3g (alternative: %s), n = %d participants",
                    rho, lo, hi, pval, alt, len(x))
        if pval < cfg["analysis"]["alpha"]:
            logger.info("RQ2 -> reject H0 at alpha=%.2f", cfg["analysis"]["alpha"])
        else:
            logger.info("RQ2 -> fail to reject H0")
    return res


# ----------------------------------------------------------------------
# RQ3 - count model
# ----------------------------------------------------------------------
def _design(part: pd.DataFrame, covariates: list[str]):
    cols = {"Intercept": np.ones(len(part)), "S": part["S"].to_numpy(),
            "B": part["B"].to_numpy(), "X per 100 min": part["X"].to_numpy() / 100}
    for c in covariates:
        if c not in part.columns:
            continue
        if part[c].dtype == object or str(part[c].dtype) in ("str", "category"):
            dummies = pd.get_dummies(part[c], prefix=c, drop_first=True)
            for name in dummies.columns:
                cols[name] = dummies[name].astype(float).to_numpy()
        else:
            cols[c] = part[c].to_numpy(dtype=float)
    names = list(cols)
    return np.column_stack([cols[n] for n in names]), names


def run_rq3(part: pd.DataFrame, cfg: dict, logger=None,
            covariates: list[str] | None = None) -> pd.DataFrame:
    """Poisson GLM  log E(L) = log A + b0 + bS*S + bB*B + bX*X/100 (+ covariates).

    One-sided Wald tests (H1: IRR > 1) for S and B with Holm correction.
    """
    covariates = covariates or []
    d = part[part["A"] > 0].reset_index(drop=True)
    X, names = _design(d, covariates)
    try:
        fit = poisson_glm(X, d["L"].to_numpy(dtype=float),
                          np.log(d["A"].to_numpy(dtype=float)))
    except (np.linalg.LinAlgError, RuntimeError) as exc:
        if logger:
            logger.warning("RQ3 model could not be fitted (%s); the data are "
                           "too small or the predictors are degenerate.", exc)
        empty = pd.DataFrame(columns=["Term", "IRR", "CI95_Lower", "CI95_Upper",
                                      "p_one_sided", "p_holm"])
        empty.attrs.update(dispersion=np.nan, n=len(d))
        return empty

    beta, se = fit["beta"], fit["se"]
    z = beta / se
    rows = []
    for i, name in enumerate(names):
        if name == "Intercept":
            continue
        rows.append({
            "Term": name,
            "IRR": np.exp(beta[i]),
            "CI95_Lower": np.exp(beta[i] - 1.96 * se[i]),
            "CI95_Upper": np.exp(beta[i] + 1.96 * se[i]),
            "p_one_sided": float(stats.norm.sf(z[i])),
        })
    out = pd.DataFrame(rows)
    primary = out["Term"].isin(["S", "B"])
    out["p_holm"] = np.nan
    out.loc[primary, "p_holm"] = holm_adjust(out.loc[primary, "p_one_sided"])
    out.attrs["dispersion"] = fit["dispersion"]
    out.attrs["n"] = fit["n"]

    if logger:
        label = "with covariates " + str(covariates) if covariates else "primary"
        logger.info("RQ3 Poisson model (%s), n = %d, Pearson dispersion = %.2f",
                    label, fit["n"], fit["dispersion"])
        if fit["dispersion"] > cfg["analysis"]["rq3_model"]["dispersion_warning"]:
            logger.warning("Over-dispersion above threshold; robust SEs used, "
                           "consider a negative binomial sensitivity check.")
        logger.info("\n%s", out.round(4).to_string(index=False))
    return out


# ----------------------------------------------------------------------
# Descriptive viewing-pattern groups (RQ3 descriptive comparison)
# ----------------------------------------------------------------------
def viewing_pattern_groups(part: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """Four groups by frequent study-time / bedtime viewing.

    The protocol's reference group ("neither pattern") is empty in practice
    when almost everyone views before bed at least once, so a participant is
    labelled as a *frequent* viewer when the pattern occurs on at least
    `descriptive_groups.threshold` of valid days. Descriptive only.
    """
    thr = cfg["analysis"]["descriptive_groups"]["threshold"]
    n_boot = cfg["reproducibility"]["n_bootstrap"]
    seed = cfg["reproducibility"]["random_seed"]
    study = part["S"] >= thr
    bed = part["B"] >= thr
    labels = np.select(
        [~study & ~bed, study & ~bed, ~study & bed, study & bed],
        ["Neither (reference)", "Study-time only", "Bedtime only", "Both"],
        default="",
    )
    rows = []
    for g in ["Neither (reference)", "Study-time only", "Bedtime only", "Both"]:
        sub = part[labels == g]
        if len(sub) == 0:
            continue
        r, lo, hi = bootstrap_ratio_ci(sub["L"], sub["A"], n_boot, seed)
        rows.append({"Group": g, "N": len(sub),
                     "Mean_X": sub["X"].mean(), "Mean_P": sub["P"].mean(),
                     "Late_rate_%": r, "CI95_Lower": lo, "CI95_Upper": hi})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------
# Guardrail: proxy discrepancy
# ----------------------------------------------------------------------
def proxy_discrepancy(part: pd.DataFrame, cfg: dict, logger=None) -> dict:
    """Diary minutes vs device minutes (reported, not used to exclude)."""
    if "screen_mean" not in part.columns:
        return {}
    diff = part["screen_mean"] - part["X"]
    lo, hi = bootstrap_ci(diff.to_numpy(), np.mean,
                          cfg["reproducibility"]["n_bootstrap"],
                          cfg["reproducibility"]["random_seed"])
    rho = stats.spearmanr(part["X"], part["screen_mean"])[0]
    res = {"mean_diff_min": float(diff.mean()), "ci_lower": lo, "ci_upper": hi,
           "spearman_diary_vs_device": float(rho),
           "mean_ratio_device_to_diary":
               float((part["screen_mean"] / part["X"]).mean())}
    if logger:
        logger.info("Proxy discrepancy (device - diary), participant means: "
                    "%.1f min/day [95%% CI %.1f, %.1f]; Spearman = %.2f",
                    res["mean_diff_min"], lo, hi, rho)
    return res


# ----------------------------------------------------------------------
# Assemble flat results table
# ----------------------------------------------------------------------
def results_table(rq1, rq2, rq3, rq3_cov, groups, proxy, completeness) -> pd.DataFrame:
    rows = []
    for _, r in rq1.iterrows():
        rows.append(("RQ1", r["Variable"], r["Mean"], r["CI95_Lower"], r["CI95_Upper"], np.nan, r["Unit"]))
    rows.append(("RQ2", "Spearman rho (X vs P)", rq2["rho"], rq2["ci_lower"],
                 rq2["ci_upper"], rq2["p_value"], f"n={rq2['n']}"))
    for _, r in rq3.iterrows():
        rows.append(("RQ3", f"IRR {r['Term']}", r["IRR"], r["CI95_Lower"],
                     r["CI95_Upper"], r["p_holm"] if not np.isnan(r["p_holm"]) else r["p_one_sided"],
                     "Holm p" if not np.isnan(r["p_holm"]) else "one-sided p"))
    for _, r in rq3_cov.iterrows():
        rows.append(("RQ3 sensitivity", f"IRR {r['Term']}", r["IRR"], r["CI95_Lower"],
                     r["CI95_Upper"], r["p_one_sided"], "adjusted for age, gender"))
    for _, r in groups.iterrows():
        rows.append(("RQ3 descriptive", f"Late rate: {r['Group']}", r["Late_rate_%"],
                     r["CI95_Lower"], r["CI95_Upper"], np.nan, f"n={int(r['N'])}, %"))
    if proxy:
        rows.append(("Guardrail", "Device minus diary (min/day)", proxy["mean_diff_min"],
                     proxy["ci_lower"], proxy["ci_upper"], np.nan, "participant means"))
    rows.append(("Guardrail", "Participants analysed", completeness["participants_analysed"],
                 np.nan, np.nan, np.nan, f"excluded: {completeness['participants_excluded']}"))
    return pd.DataFrame(rows, columns=["Question", "Quantity", "Estimate",
                                       "CI95_Lower", "CI95_Upper", "p", "Note"])


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def run_pipeline(diary_raw: pd.DataFrame, cfg: dict, logger=None) -> dict:
    """Run every step and return all intermediate and final tables."""
    diary, report = validate_diary(diary_raw, cfg)
    part = derive_participant_level(diary, cfg)
    part = add_participant_covariates(part, diary, cfg)
    part, completeness = apply_completeness_guardrail(part, cfg)
    if len(part) < 4:
        raise ValueError(
            f"Only {len(part)} participant(s) have at least "
            f"{cfg['observation']['min_valid_days']} valid diary days; "
            "too few to fit the models. For the 2-day synthetic sample use "
            "--min-valid-days 1.")

    if logger:
        logger.info("Validation report: %s", report)
        logger.info("Completeness guardrail: %s", completeness)
        logger.info("Participant-level table: %d participants", len(part))

    rq1 = run_rq1(part, cfg, logger)
    rq2 = run_rq2(part, cfg, logger)
    rq3 = run_rq3(part, cfg, logger)
    rq3_cov = run_rq3(part, cfg, logger,
                      cfg["analysis"]["rq3_model"]["sensitivity_covariates"])
    groups = viewing_pattern_groups(part, cfg)
    proxy = proxy_discrepancy(part, cfg, logger)
    if logger:
        logger.info("Descriptive viewing-pattern groups:\n%s",
                    groups.round(2).to_string(index=False))
    table = results_table(rq1, rq2, rq3, rq3_cov, groups, proxy, completeness)
    return {"diary": diary, "validation": report, "participants": part,
            "completeness": completeness, "rq1": rq1, "rq2": rq2,
            "rq3": rq3, "rq3_cov": rq3_cov, "groups": groups,
            "proxy": proxy, "results": table}


def main() -> int:
    parser = argparse.ArgumentParser(description="Analysis pipeline for the short-form video study.")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--input", required=True, help="Path to diary CSV")
    parser.add_argument("--min-valid-days", type=int, default=None,
                        help="Override observation.min_valid_days (use 1 for the 2-day synthetic sample)")
    parser.add_argument("--save", action="store_true",
                        help="Write participant-level and results tables to data/processed/")
    args = parser.parse_args()

    cfg = load_config(args.config)
    if args.min_valid_days is not None:
        cfg["observation"]["min_valid_days"] = args.min_valid_days
    root = Path(args.config).resolve().parent.parent
    logger = setup_logging(root / cfg["reproducibility"].get("log_file", "results/run.log"))
    logger.info("Config: %s | input: %s", args.config, args.input)

    diary_raw = pd.read_csv(args.input)
    out = run_pipeline(diary_raw, cfg, logger)

    if args.save:
        for key, name in (("participants", "participant_table"),
                          ("results", "results_table")):
            path = root / cfg["output"][name]
            path.parent.mkdir(parents=True, exist_ok=True)
            out[key].to_csv(path, index=False)
            logger.info("Saved %s", path)
    logger.info("Analysis complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
