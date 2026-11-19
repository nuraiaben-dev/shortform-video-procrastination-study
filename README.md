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
