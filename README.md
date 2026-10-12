# The Impact of Short-Form Video Content on Student Procrastination and Academic Deadline Adherence

**Authors:** Nuray Akniet (nuraiaben-dev)  
**Course:** Research Methods — Task 2: Methodology Passport Card & Research Repository  
**Institution:** [University Name]  
**Date:** October 2026

---

## Overview

This repository contains the research protocol, methodology passport card, and reproducible analysis pipeline for an observational study examining whether short-form video consumption (TikTok, Instagram Reels, YouTube Shorts) is associated with increased procrastination and reduced academic deadline adherence among university students.

**Research Question(s):**

- **RQ1** (descriptive): What are students' average daily short-form video viewing time and baseline procrastination scores?
- **RQ2** (associational): Is daily viewing time positively associated with procrastination?
- **RQ3** (associational): Are viewing during academic tasks and viewing before bedtime associated with a higher proportion of missed academic deadlines?

**Study Design:** Mixed-Methods — primary quantitative observational design (14-day diary + questionnaire + device screen-time evidence), with optional qualitative follow-up interviews.

**No empirical findings are claimed at this stage.** This is a protocol and reproducible pipeline.

---

## Hypotheses

**RQ2:**
- H0: The population Spearman correlation between daily viewing time and procrastination is zero (ρs = 0).
- H1: The correlation is positive (ρs > 0).

**RQ3a (study-time viewing):**
- H0: The adjusted incidence-rate ratio for late submissions is 1.
- H1: The adjusted incidence-rate ratio exceeds 1.

**RQ3b (bedtime viewing):**
- H0: The adjusted incidence-rate ratio for late submissions is 1.
- H1: The adjusted incidence-rate ratio exceeds 1.

---

## Repository Structure

```
shortform-video-procrastination-study/
│
├── README.md                  # This file — overview and Quickstart
├── LICENSE                    # MIT License
├── .gitignore                 # Python / data-science gitignore
├── environment.yml            # Pinned dependencies (conda)
│
├── configs/
│   └── config.yaml            # Experiment parameters (window, thresholds, paths)
│
├── data/
│   └── sample/
│       └── sample_data.csv    # 10-row synthetic sample for pipeline testing
│
├── docs/
│   └── methodology.md         # Methodology Passport Card (Task 2 submission)
│
├── notebooks/
│   └── .gitkeep               # Placeholder for exploratory notebooks
│
└── src/
    └── analyze.py             # Main analysis pipeline (Spearman + IRR model)
```

---

## Planned Benchmarks & Metrics

| Metric | Role | Formula / Definition | Collection Source |
|---|---|---|---|
| Procrastination score **P** | Primary (RQ2 outcome) | Sum of 16-item Tuckman scale (reverse-coded) | Baseline questionnaire |
| Mean daily viewing **X** | Primary (RQ2 predictor) | Total valid viewing minutes / valid diary days | 14-day diary + device evidence |
| Late-submission rate **R** | Primary (RQ3 outcome) | 100 × L / A, for A > 0 | Deadline log |
| Spearman correlation **ρs** | Primary (RQ2 effect) | Correlation of ranked X and P | Derived |
| Adjusted IRR | Primary (RQ3 effect) | exp(β) from Poisson/NegBinom with log(A) offset | Derived |
| Diary completeness | Guardrail | 100 × valid days / 14 (require ≥ 10) | Diary |
| Proxy discrepancy | Guardrail | Diary minutes vs. app minutes | Diary vs. device |
| On-time rate | Guardrail (secondary) | 100 × (A − L) / A | Deadline log |

**Baseline / Reference group:** Students reporting *neither* study-time viewing *nor* bedtime viewing (the "neither" pattern group). Continuous predictors X, S, B are the primary adjusted predictors.

---

## Quickstart Guide

Run the full analysis pipeline on the synthetic sample in **three commands**.

### Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/) installed.

### 1. Create the environment

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate shortform-study
```

### 3. Run the analysis on the sample data

```bash
python src/analyze.py --config configs/config.yaml --input data/sample/sample_data.csv
```

**Expected output:** the script prints summary statistics, Spearman ρ with a directional p-value, and the incidence-rate-ratio model fit, and writes a log file to `results/run.log`.

### Alternative (Docker)

If Docker is preferred, a `Dockerfile` may be added in a future revision. The current pinned `environment.yml` guarantees reproducibility.

---

## Methodology Passport Card

The full **Methodology Passport Card** (Task 2 submission document) is available at:

📄 [`docs/methodology.md`](docs/methodology.md)

It contains: research type, hypotheses H0/H1, variable matrix (independent / dependent / controlled), primary and guardrail metrics, and the baseline definition.

---

## Data & Privacy

- **No real participant data are stored in this repository.** Only a synthetic `data/sample/sample_data.csv` (10 rows) is committed for pipeline testing.
- Real data (if collected in the future) will be stored under `data/raw/` and `data/processed/`, both of which are excluded via `.gitignore`.
- Participant records are pseudonymised via study IDs; contact information is stored separately.

---

## Reproducibility

- Exact dependency versions are pinned in `environment.yml`.
- All experiment parameters live in `configs/config.yaml`.
- Random seeds for resampling are fixed in the config.
- The analysis script is deterministic given the same inputs.

---

## Citation

If you reference this protocol, please cite:

```
Akniet, N. (2026). The Impact of Short-Form Video Content on Student Procrastination
and Academic Deadline Adherence: Research Protocol and Reproducible Pipeline.
GitHub: https://github.com/nuraiaben-dev/shortform-video-procrastination-study
```

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## References

1. Tuckman, B. W. (1991). The Development and Concurrent Validity of the Procrastination Scale. *Educational and Psychological Measurement*, 51(2), 473–480. https://doi.org/10.1177/0013164491512022
2. Microsoft Learn. Microsoft Threat Modeling Tool threats. https://learn.microsoft.com/azure/security/develop/threat-modeling-tool-threats
3. FIRST. CVSS v4.0 User Guide. https://www.first.org/cvss/user-guide.html

