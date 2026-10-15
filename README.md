# The Impact of Short-Form Video Content on Student Procrastination and Academic Deadline Adherence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![Status: Protocol](https://img.shields.io/badge/status-protocol-orange.svg)](#)
[![Reproducible](https://img.shields.io/badge/reproducibility-100%25-brightgreen.svg)](#reproducibility)

**Authors:** Nuray Aben (nuraiaben-dev) & Akniet Abish 

**Course:** Research Methods — Task 2: Methodology Passport Card & Research Repository  

**Institution:** [Narxoz]  

**Date:** October 2026

---

## Overview & Research Aim

This repository contains the research protocol, methodology passport card, and reproducible analysis pipeline for an observational study examining whether short-form video consumption (TikTok, Instagram Reels, YouTube Shorts) is associated with increased procrastination and reduced academic deadline adherence among university students.

**Research Question(s):**

- **RQ1** (descriptive): What are students' average daily short-form video viewing time and baseline procrastination scores?
- **RQ2** (associational): Is daily viewing time positively associated with procrastination?
- **RQ3** (associational): Are viewing during academic tasks and viewing before bedtime associated with a higher proportion of missed academic deadlines?

**Core hypothesis (H1 for RQ2):** There is a positive association (Spearman ρ > 0) between daily short-form video viewing time and procrastination scores.

**Study Design:** Mixed-Methods — primary quantitative observational design (14-day diary + questionnaire + device screen-time evidence), with optional qualitative follow-up interviews.

**No empirical findings are claimed at this stage.** This is a protocol and reproducible pipeline.

---

## System Requirements & Prerequisites

**Hardware:**

- Any modern CPU (no GPU required — this is a behavioural study, not a deep-learning workload)
- ≥ 4 GB RAM (8 GB recommended)
- ≥ 500 MB free disk space

**Operating System:**

- macOS 12+, Ubuntu 20.04+, or Windows 10+ (via WSL2 or Anaconda Prompt)

**Software:**

- [Miniconda 23.x+](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda 2023.x+](https://www.anaconda.com/)
- Python 3.11.9 (installed automatically via `environment.yml`)
- Git 2.30+
- Optional: [Docker Desktop 4.x+](https://www.docker.com/products/docker-desktop/) (see `Dockerfile`)

---

## Repository Structure

```
shortform-video-procrastination-study/
│
├── README.md                          # This file — overview and Quickstart
├── LICENSE                            # MIT License
├── .gitignore                         # Python / data-science gitignore
├── .dockerignore                      # Docker build context exclusions
├── environment.yml                    # Pinned dependencies (conda)
├── Dockerfile                         # Optional containerised environment
│
├── configs/
│   └── config.yaml                    # Experiment parameters (window, thresholds, paths)
│
├── data/
│   └── sample/
│       └── sample_data.csv            # 10-row synthetic sample for pipeline testing
│
├── docs/
│   ├── methodology.md                 # Methodology Passport Card (Task 2 submission)
│   └── reproducibility_checklist.md   # 7-point reviewer audit checklist
│
├── notebooks/
│   └── .gitkeep                       # Placeholder for exploratory notebooks
│
└── src/
    └── analyze.py                     # Main analysis pipeline (Spearman + IRR model)
```

---

## Quickstart & Reproducibility Guide

Run the full analysis pipeline on the synthetic sample in **three commands**.

### Option A — Conda (recommended)

```bash
# 1. Create the environment from pinned dependencies
conda env create -f environment.yml

# 2. Activate it
conda activate shortform-study

# 3. Run the analysis on the sample data
python src/analyze.py --config configs/config.yaml --input data/sample/sample_data.csv
```

### Option B — Docker

```bash
# 1. Build the image
docker build -t shortform-study .

# 2. Run the pipeline inside the container
docker run --rm -v "$PWD":/work shortform-study \
    python src/analyze.py --config configs/config.yaml --input data/sample/sample_data.csv
```

**Expected output:** the script prints summary statistics, Spearman ρ with a directional p-value, and the incidence-rate-ratio model fit, and writes a log file to `results/run.log`.

---

## Expected Results / Benchmark Table

The table below summarises the **planned** metrics for the study. Actual values are placeholders — no empirical results are claimed at protocol stage.

| Metric | Role | Formula / Definition | Collection Source | Expected Direction |
|---|---|---|---|---|
| Procrastination score **P** | Primary (RQ2 outcome) | Sum of 16-item Tuckman scale (reverse-coded) | Baseline questionnaire | — |
| Mean daily viewing **X** | Primary (RQ2 predictor) | Total valid viewing minutes / valid diary days | 14-day diary + device | — |
| Late-submission rate **R** | Primary (RQ3 outcome) | 100 × L / A, for A > 0 | Deadline log | — |
| Spearman **ρs** | Primary (RQ2 effect) | Rank correlation between X and P | Derived | ρs > 0 (H1) |
| Adjusted **IRR** | Primary (RQ3 effect) | exp(β) from Poisson/NegBinom with log(A) offset | Derived | IRR > 1 (H1) |
| Diary completeness | Guardrail | 100 × valid days / 14 (≥ 10 required) | Diary | ≥ 71% |
| Proxy discrepancy | Guardrail | Diary minutes vs. app minutes | Diary vs. device | Report only |
| On-time rate | Guardrail (secondary) | 100 × (A − L) / A | Deadline log | — |

**Baseline / Reference group:** Students reporting *neither* study-time viewing *nor* bedtime viewing (the "neither" pattern group). Continuous predictors X, S, B are the primary adjusted predictors.

---

## Methodology Passport Card

The full **Methodology Passport Card** (Task 2 submission document) is available at:

📄 [`docs/methodology.md`](docs/methodology.md)

It contains: research type, hypotheses H0/H1, variable matrix (independent / dependent / controlled), primary and guardrail metrics, and the baseline definition.

---

## Reproducibility

- Exact dependency versions are pinned in `environment.yml`.
- All experiment parameters live in `configs/config.yaml`.
- Random seeds for resampling are fixed in the config.
- The analysis script is deterministic given the same inputs.
- A reviewer-facing audit checklist is at [`docs/reproducibility_checklist.md`](docs/reproducibility_checklist.md).

---

## Data & Privacy

- **No real participant data are stored in this repository.** Only a synthetic `data/sample/sample_data.csv` (10 rows) is committed for pipeline testing.
- Real data (if collected in the future) will be stored under `data/raw/` and `data/processed/`, both excluded via `.gitignore`.
- Participant records are pseudonymised via study IDs; contact information is stored separately.

---

## Citation

If you reference this protocol, please cite:

```bibtex
@misc{akniet2026shortform,
  author       = {Akniet, Nuray},
  title        = {The Impact of Short-Form Video Content on Student Procrastination
                  and Academic Deadline Adherence: Research Protocol and Reproducible Pipeline},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/nuraiaben-dev/shortform-video-procrastination-study}},
  note         = {Research protocol, no empirical findings claimed}
}
```

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## References

1. Tuckman, B. W. (1991). The Development and Concurrent Validity of the Procrastination Scale. *Educational and Psychological Measurement*, 51(2), 473–480. https://doi.org/10.1177/0013164491512022
2. Microsoft Learn. Microsoft Threat Modeling Tool threats. https://learn.microsoft.com/azure/security/develop/threat-modeling-tool-threats
3. FIRST. CVSS v4.0 User Guide. https://www.first.org/cvss/user-guide.html

## Week 7 Benchmark

The benchmark measures the execution time of
`derive_participant_level` on the 10-row synthetic sample.
CSV reading, file writing and console output are outside
the timed section.

### Run

With the project environment installed:

```bash
conda activate shortform-study
python src/benchmark.py --config configs/config.yaml
```

Settings are stored in `configs/config.yaml`.

### Test results

10 warm-up runs were excluded from summary statistics.
All 100 measured runs completed successfully.

| Metric | Value |
|---|---:|
| Successful runs | 100 |
| Failed runs | 0 |
| Mean | 3.520 ms |
| Median | 3.516 ms |
| p95 | 3.552 ms |
| p99 | 3.566 ms |

These timings describe one local test on synthetic data.
They are not findings about student behaviour.
Timings may differ across machines and runs.

### Output files

- `data/raw/test_run.jsonl`: individual measurements,
  labelled as warm-up or measurement.
- `data/raw/test_run_metadata.json`: environment and configuration.
- `data/raw/test_run_summary.json`: summary statistics.

Only synthetic benchmark outputs are committed.
Real participant data must remain excluded from Git.

## Task 3 Results and Discussion

### Experimental setup

We compared two implementations of participant-level diary aggregation:

- **Baseline:** separate grouped aggregations followed by table merges.
- **Proposed:** one grouped aggregation producing the same variables.

Both methods were tested on 10, 100, 1,000 and 10,000 synthetic rows.
Outputs matched for every workload before timing.

Each method completed 10 warm-up and 100 measured runs per workload.
Warm-up runs were excluded from final statistics. Method order was
randomized within paired repetitions. All 800 measured runs succeeded.

### Results

The table below shows rounded median execution times.
The executed notebook and CSV also report quartiles, mean, sample SD,
p95, p99 and bootstrap 95% confidence intervals.

| Input size (rows) | Baseline median (p25–p75), ms | Proposed median (p25–p75), ms | Speedup |
|---:|---:|---:|---:|
| 10 | 3.537 (3.517–3.571) | 1.910 (1.903–1.920) | 1.85× |
| 100 | 3.635 (3.622–3.658) | 1.929 (1.921–1.938) | 1.88× |
| 1,000 | 5.016 (4.991–5.171) | 2.193 (2.176–2.291) | 2.29× |
| 10,000 | 20.647 (20.481–21.025) | 4.852 (4.797–4.975) | 4.26× |

Speedup is the baseline median divided by the proposed median.

The proposed method had lower median execution time at every tested
input size. Its relative advantage was largest at 10,000 rows.
Both methods had an observed error rate of 0% in this experiment.

### Scientific figures

![Median execution time and bootstrap 95% confidence intervals](reports/figures/fig1_latency_vs_load.png)

![Execution-time distributions and median confidence intervals](reports/figures/fig2_distribution_boxplot.png)

Vector exports:
[Figure 1 PDF](reports/figures/fig1_latency_vs_load.pdf) |
[Figure 2 PDF](reports/figures/fig2_distribution_boxplot.pdf)

### Reproduce the analysis

After installing and activating the project environment:

```bash
python src/process_data.py
python src/visualize.py
jupyter notebook notebooks/01_data_analysis.ipynb
```

The notebook is saved with sequentially executed cells and visible outputs.

To collect a new comparison log:

```bash
python src/compare_benchmark.py --config configs/config.yaml
```

This command overwrites the comparison log. Re-run processing and
visualization afterwards; numerical results may differ.

### Domain model

See the [component diagram and measurement boundaries](docs/domain_model.md).

### Limitations

The experiment used one computer and repeated synthetic sample data.
Increasing workload size increased both row count and participant-group
count. Their effects were not isolated.

Bootstrap intervals use 5,000 resamples with seed 42 and describe
within-session uncertainty under an independent-run assumption.
They do not capture differences across machines or separate sessions.
With 100 measurements per group, p99 estimates are approximate.

These results evaluate software performance. They do not test the
behavioural hypotheses about short-form videos and student procrastination.

### Analysis artifacts

- [Executed notebook](notebooks/01_data_analysis.ipynb)
- [Full statistical summary](data/processed/metrics_summary.csv)
- [Comparison measurements](data/raw/comparison_run.jsonl)
- [Experiment metadata](data/raw/comparison_run_metadata.json)
