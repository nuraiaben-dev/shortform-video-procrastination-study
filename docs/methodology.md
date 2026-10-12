# Methodology Passport Card

**Project:** The Impact of Short-Form Video Content on Student Procrastination and Academic Deadline Adherence

**Authors:** Nuray Aben (nuraiaben-dev) & Akniet Abish

**Repository:** https://github.com/nuraiaben-dev/shortform-video-procrastination-study

**Date:** October 2026

---

## 1. Research Type

**Mixed-Methods** — with a **primary quantitative observational design**, complemented by optional qualitative interviews.

**Justification:**
- The core research questions (RQ2, RQ3) are **associational and quantitative**: they require numerical measurement of viewing time, procrastination scores, and late-submission counts.
- **RQ1** is purely descriptive (mean viewing time, baseline procrastination).
- Optional **qualitative interviews** (8–12 participants) provide contextual explanations of *why* students open short-form video feeds during study sessions — they do not establish causal mechanisms.

The study is **observational**, not experimental. No exposure is manipulated in the primary design. An optional A/B extension (app-limit intervention) is proposed for a future study but is not part of this protocol.

---

## 2. Hypotheses

### RQ2 — Association between viewing time and procrastination

- **H0:** The population Spearman correlation between daily viewing time (X) and procrastination score (P) is zero (ρs = 0).
- **H1:** The correlation is positive (ρs > 0).

*Directional hypothesis, specified before inspecting data.*

### RQ3a — Study-time viewing and late submissions

- **H0:** The adjusted incidence-rate ratio for late submissions associated with study-time viewing (S) is 1.
- **H1:** It exceeds 1.

### RQ3b — Bedtime viewing and late submissions

- **H0:** The adjusted incidence-rate ratio for late submissions associated with bedtime viewing (B) is 1.
- **H1:** It exceeds 1.

*RQ3a and RQ3b are separate contrasts, adjusted for the other viewing pattern and predefined covariates. Holm correction is applied across the two tests at α = 0.05.*

### RQ1 — Descriptive

Answered by estimates and 95% confidence intervals; no hypothesis test (no unsupported normative threshold).

---

## 3. Variable Matrix

| Class | Variable & Operational Definition | Role / Type |
|---|---|---|
| **Independent predictor** | **X** — Daily short-form viewing time: mean minutes/day from a 14-day diary. Device app minutes are a corroborating proxy. | Continuous exposure (RQ2); covariate for RQ3 |
| **Independent predictor** | **S** — Study-time viewing: days with ≥ 1 short-video session during an intended academic work session / valid diary days. | Proportion (0–1) |
| **Independent predictor** | **B** — Bedtime viewing: days with short videos in the 60 minutes before intended bedtime / valid diary days. | Proportion (0–1) |
| **Dependent outcome** | **P** — Baseline procrastination: total score from a documented 16-item Tuckman scale version. | Questionnaire outcome (RQ2) |
| **Dependent outcome** | **L** — Late tasks: tasks submitted after original deadline or still unsubmitted at observation endpoint. | Count outcome (RQ3) |
| **Exposure denominator** | **A** — Tasks due: eligible academic tasks with deadlines during the same 14-day window. | Opportunity denominator; RQ3 includes A > 0 |
| **Measured covariates** | Academic workload (h/week), study year, mean sleep hours, non-short-video phone time. | Potential confounders; measured, not held constant |
| **Controlled procedures** | Same 14-day duration, same questionnaire version and scoring, same diary prompts, same deadline definition and cleaning rules. | Procedural standardisation |
| **Recorded context** | University/course context, exam-period status, device OS, screen-time source. | Assess comparability and measurement differences |

**Note on "independent variable":** Since no exposure is manipulated, "independent variable" here means a **measured predictor**, not a randomly assigned treatment. The two viewing-pattern predictors (S, B) are retained separately.

---

## 4. Metrics and Baseline

### Primary Metrics

| Metric | Definition / Formula | Hypothesis |
|---|---|---|
| **Spearman ρs** | Correlation of ranked X and P values; average ranks for ties | RQ2 effect estimate, with interval and directional test |
| **Adjusted IRR** | exp(β) from log E(L) = log A + β₀ + βS·S + βB·B + βX·X + γ′C | RQ3 effect estimate, with control for opportunity and covariates |
| **Procrastination score P** | Sum of correctly scored items on the 16-item Tuckman scale, per scoring key | RQ2 outcome |
| **Late-submission rate R** | 100 × L / A, for A > 0 | RQ3 outcome |
| **Mean daily viewing X** | Σ valid daily viewing minutes / number of valid diary days | RQ2 predictor |

### Guardrail Metrics

| Guardrail | Threshold / Rule | Purpose |
|---|---|---|
| **Diary completeness** | Require ≥ 10 valid diary days out of 14 for primary exposure analysis | Data-quality guardrail |
| **Proxy discrepancy** | Compare diary short-video minutes vs. corresponding app minutes; report discrepancy and context | Measurement guardrail; not proof of dishonesty |
| **On-time rate** | 100 × (A − L) / A | Secondary; equivalent complement of late rate, not a separate confirmatory test |

### Baseline / Reference Group

- **Primary RQ2 analysis:** continuous viewing time across the sample — no arbitrary high/low split.
- **RQ3 descriptive comparison:** four naturally occurring groups —
  1. **Neither** viewing pattern (reference group)
  2. Study-time viewing only
  3. Bedtime viewing only
  4. Both patterns
- **Continuous S and B** remain the primary adjusted predictors, avoiding loss of information.
- These are **naturally occurring comparison groups**, not randomised control groups. Adjusted comparisons reduce measured confounding but do not eliminate it.

### Excluded Metrics

CPU/GPU usage, memory, FLOPs, and API latency are **excluded** — they are unrelated to the behavioural hypotheses.

---

## 5. Threats to Validity (summary)

| Threat | Consequence | Mitigation |
|---|---|---|
| **Internal validity** — reverse direction & confounding | Students may watch videos because they already procrastinate; workload can affect both | Cautious association wording; measured covariates; later randomised extension |
| **Construct validity** — app time & self-report error | Whole-app minutes do not isolate short videos; diaries and deadlines may be inaccurate | Keep proxy and diary variables separate; corroborate redacted evidence; pilot definitions |
| **External validity** — convenience sample | One university and willing volunteers may not represent all students | Recruit across study years/courses; report context and selection limits |
| **Statistical validity** — few events & multiple tests | Unstable regression and false positives | Power/event feasibility check; parsimonious models; Holm correction; intervals |
| **Qualitative credibility** | Interpretations may reflect interviewer's assumptions | Codebook; reflexive notes; contrasting cases; review coding disagreements |

---

## 6. Data Collection Procedure (outline)

1. **Pilot** the questionnaire and diary with 5–10 students (excluded from main analysis if protocol changes).
2. **Recruit** volunteers, obtain informed consent, assign random study IDs.
3. **Collect** baseline questionnaire + 14-day diary + redacted app-usage evidence + deadline log.
4. **Clean** data using predefined rules; derive X, S, B, L, A; lock the cleaned dataset and analysis plan.
5. **Analyse** associations with uncertainty intervals; integrate optional interview themes.

---

## 7. Reproducibility

- Questionnaire version, codebook, blank diary, preprocessing rules, and analysis script are preserved.
- Software environment and random seeds are pinned in `environment.yml` and `configs/config.yaml`.
- Only disclosure-checked aggregate outputs or authorised deidentified datasets are shared.

---

## References

1. Tuckman, B. W. (1991). The Development and Concurrent Validity of the Procrastination Scale. *Educational and Psychological Measurement*, 51(2), 473–480. https://doi.org/10.1177/0013164491512022
2. Microsoft Learn. Microsoft Threat Modeling Tool threats. https://learn.microsoft.com/azure/security/develop/threat-modeling-tool-threats
3. FIRST. CVSS v4.0 User Guide. https://www.first.org/cvss/user-guide.html
