# The Impact of Short-Form Video Content on Student Procrastination and Academic Deadline Adherence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![Status: Completed](https://img.shields.io/badge/status-completed-brightgreen.svg)](#)
[![Reproducible](https://img.shields.io/badge/reproducibility-100%25-brightgreen.svg)](#reproducibility)

**Authors:** Nuray Aben (nuraiaben-dev) & Akniet Abish (aknietabish-cpu)

**Course:** Research Methods — Task 2 & Task 3: Methodology Passport Card, Data Analysis & Visualization  

**Institution:** [Narxoz]  

**Date:** November 2026

---

## Overview & Research Aim

This repository contains the research protocol, methodology passport card, and reproducible analysis pipeline for an observational study examining whether short-form video consumption (TikTok, Instagram Reels, YouTube Shorts) is associated with increased procrastination and reduced academic deadline adherence among university students.

**Research Question(s):**

- **RQ1** (descriptive): What are students' average daily short-form video viewing time and baseline procrastination scores?
- **RQ2** (associational): Is daily viewing time positively associated with procrastination?
- **RQ3** (associational): Are viewing during academic tasks and viewing before bedtime associated with a higher proportion of missed academic deadlines?

**Core hypothesis (H1 for RQ2):** There is a positive association (Spearman ρ > 0) between daily short-form video viewing time and procrastination scores.

**Study Design:** Mixed-Methods — primary quantitative observational design (14-day diary + questionnaire + device screen-time evidence), with optional qualitative follow-up interviews.

This repository now includes the empirical analysis of real survey data (`data/raw/real_data.csv`) investigating the relationship between short-form video viewing habits and procrastination levels. The pipeline includes data cleaning, bootstrapped statistical aggregation, and scientific visualization.

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

```text
shortform-video-procrastination-study/
│
├── README.md
├── LICENSE
├── .gitignore
├── environment.yml
│
├── configs/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   │   └── real_data.csv
│   └── processed/
│       └── metrics_summary.csv
│
├── docs/
│   ├── methodology.md
│   ├── domain_model.md
│   └── reproducibility_checklist.md
│
├── notebooks/
│   └── 01_data_analysis.ipynb
│
├── reports/
│   ├── figures/
│   │   ├── fig1_procrastination_vs_viewing.png
│   │   ├── fig1_procrastination_vs_viewing.pdf
│   │   ├── fig2_viewing_vs_procrastination.png
│   │   └── fig2_viewing_vs_procrastination.pdf
│   ├── paper_section_4.md
│   └── task3_report.md
│
└── src/
    ├── process_data.py
    └── visualize.py


# The Impact of Short-Form Video Content on Student Procrastination and Academic Deadline Adherence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![Status: Completed](https://img.shields.io/badge/status-completed-brightgreen.svg)](#)
[![Reproducible](https://img.shields.io/badge/reproducibility-100%25-brightgreen.svg)](#reproducibility)

**Authors:** Nuray Aben (nuraiaben-dev) & Akniet Abish (aknietabish-cpu)

**Course:** Research Methods — Task 2 & Task 3: Methodology Passport Card, Data Analysis & Visualization  

**Institution:** [Narxoz]  

**Date:** November 2026

---

## Overview & Research Aim

This repository contains the research protocol, methodology passport card, and reproducible analysis pipeline for an observational study examining whether short-form video consumption (TikTok, Instagram Reels, YouTube Shorts) is associated with increased procrastination and reduced academic deadline adherence among university students.

**Research Question(s):**

- **RQ1** (descriptive): What are students' average daily short-form video viewing time and baseline procrastination scores?
- **RQ2** (associational): Is daily viewing time positively associated with procrastination?
- **RQ3** (associational): Are viewing during academic tasks and viewing before bedtime associated with a higher proportion of missed academic deadlines?

**Core hypothesis (H1 for RQ2):** There is a positive association (Spearman ρ > 0) between daily short-form video viewing time and procrastination scores.

**Study Design:** Mixed-Methods — primary quantitative observational design (14-day diary + questionnaire + device screen-time evidence), with optional qualitative follow-up interviews.

This repository now includes the empirical analysis of real survey data (`data/raw/real_data.csv`) investigating the relationship between short-form video viewing habits and procrastination levels. The pipeline includes data cleaning, bootstrapped statistical aggregation, and scientific visualization.

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

```text
shortform-video-procrastination-study/
│
├── README.md
├── LICENSE
├── .gitignore
├── environment.yml
│
├── configs/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   │   └── real_data.csv
│   └── processed/
│       └── metrics_summary.csv
│
├── docs/
│   ├── methodology.md
│   ├── domain_model.md
│   └── reproducibility_checklist.md
│
├── notebooks/
│   └── 01_data_analysis.ipynb
│
├── reports/
│   ├── figures/
│   │   ├── fig1_procrastination_vs_viewing.png
│   │   ├── fig1_procrastination_vs_viewing.pdf
│   │   ├── fig2_viewing_vs_procrastination.png
│   │   └── fig2_viewing_vs_procrastination.pdf
│   ├── paper_section_4.md
│   └── task3_report.md
│
└── src/
    ├── process_data.py
    └── visualize.py

## Quickstart & Reproducibility Guide

### Option A — Conda (Recommended)

Run the full analysis pipeline on the real data in **three commands**:

    # 1. Clone the repository and enter directory
    git clone https://github.com/nuraiaben-dev/shortform-video-procrastination-study.git
    cd shortform-video-procrastination-study

    # 2. Create and activate environment
    conda env create -f environment.yml
    conda activate shortform-study

    # 3. Execute sample analysis pipeline
    jupyter notebook notebooks/01_data_analysis.ipynb

---

## Methodology Passport Card

The full **Methodology Passport Card** (Task 2 submission document) is available at:

📄 [docs/methodology.md](docs/methodology.md)

It contains: research type, hypotheses H0/H1, variable matrix (independent / dependent / controlled), primary and guardrail metrics, and the baseline definition.

---

## Reproducibility

- Exact dependency versions are pinned in `environment.yml`.
- All experiment parameters live in `configs/config.yaml`.
- Random seeds for resampling are fixed in the config.
- The analysis script is deterministic given the same inputs.
- A reviewer-facing audit checklist is at [docs/reproducibility_checklist.md](docs/reproducibility_checklist.md).

---

## Data & Privacy

- The real participant data (`data/raw/real_data.csv`) has been anonymized and pseudonymized via study IDs prior to analysis. The repository includes the processed aggregate metrics (`data/processed/metrics_summary.csv`) and generated figures, but does not contain any personally identifiable information (PII).
- Participant records are pseudonymised via study IDs; contact information is stored separately.

---

## Citation

If you reference this protocol, please cite:

    @misc{akniet2026shortform,
      author       = {Akniet, Nuray},
      title        = {The Impact of Short-Form Video Content on Student Procrastination
                      and Academic Deadline Adherence: Research Protocol and Reproducible Pipeline},
      year         = {2026},
      publisher    = {GitHub},
      howpublished = {\url{https://github.com/nuraiaben-dev/shortform-video-procrastination-study}},
      note         = {Research protocol and empirical analysis of real survey data}
    }

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## References

1. Tuckman, B. W. (1991). The Development and Concurrent Validity of the Procrastination Scale. *Educational and Psychological Measurement*, 51(2), 473–480. https://doi.org/10.1177/0013164491512022
2. Microsoft Learn. Microsoft Threat Modeling Tool threats. https://learn.microsoft.com/azure/security/develop/threat-modeling-tool-threats
3. FIRST. CVSS v4.0 User Guide. https://www.first.org/cvss/user-guide.html

---

## Task 3 Results and Discussion

### Experimental setup

We analyzed real survey data (`data/raw/real_data.csv`) containing 2,360 records of student behaviour. Data processing included cleaning missing values and dividing participants into two groups based on daily viewing time (`< 60 mins` and `>= 60 mins`). We calculated robust statistics (mean, median) and bootstrapped 95% confidence intervals (2,000 resamples, seed = 42). We also tracked a guardrail metric: the percentage of participants with a high procrastination score (> 50).

### Results

The table below summarises the findings:

| Viewing Time Group | N (records) | Mean Score | Median Score | 95% CI (Bootstrap) | High Procrastination Rate (Guardrail) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **< 60 mins** | 854 | 24.80 | 23.0 | [24.32, 25.29] | 0.35% |
| **>= 60 mins** | 1506 | 43.10 | 44.0 | [42.55, 43.70] | 29.22% |

**Key Findings:**

1. Participants watching short-form videos for **60 minutes or more per day** show significantly higher procrastination scores. The non-overlapping confidence intervals confirm this difference is statistically robust.
2. The guardrail metric reveals a dramatic difference: the rate of high procrastination is ~83 times higher in the `>= 60 mins` group.

### Scientific figures

The plots strictly follow scientific visualization standards (explicit axis units, 95% CI error bars, colorblind-safe palette, distinct markers):

* ![Procrastination vs Viewing Time](reports/figures/fig1_procrastination_vs_viewing.png)
* ![Correlation Plot](reports/figures/fig2_viewing_vs_procrastination.png)

Vector exports: [Figure 1 PDF](reports/figures/fig1_procrastination_vs_viewing.pdf) | [Figure 2 PDF](reports/figures/fig2_viewing_vs_procrastination.pdf)

### Domain model

The component diagram and measurement boundaries are documented in [docs/domain_model.md](docs/domain_model.md).

### Limitations

The analysis is based on observational self-reported data. While a significant association exists, it does not imply causation. The dataset is limited to the survey sample and does not capture long-term behavioural changes.
