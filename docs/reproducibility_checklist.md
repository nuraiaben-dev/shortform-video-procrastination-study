# Reproducibility & Audit Checklist

**Project:** The Impact of Short-Form Video Content on Student Procrastination and Academic Deadline Adherence  
**Repository:** https://github.com/nuraiaben-dev/shortform-video-procrastination-study  
**Reviewer time to complete this checklist:** ≤ 2 minutes

---

## How to use this checklist

Open the repository in a browser. Tick each box. If **all 7 items** are checked, the repository is considered **fully reproducible**.

---

## ✅ 1. Environment is pinned with exact versions

- [ ] `environment.yml` (or `requirements.txt`) exists in the repository root.
- [ ] Every package has an **exact version** (e.g. `pandas=2.2.2`, not `pandas>=2.0`).
- [ ] Python version is pinned (e.g. `python=3.11.9`).
- [ ] Optionally, a `Dockerfile` is present and builds with `docker build -t shortform-study .`

**Where to look:** [`environment.yml`](../environment.yml), [`Dockerfile`](../Dockerfile)

---

## ✅ 2. Experiment parameters are externalised in a config file

- [ ] A `config.yaml` (or `config.json`) exists.
- [ ] All tunable parameters — observation window, minimum valid days, alpha, seed, paths — are in the config, **not hard-coded** in the script.
- [ ] The config is committed to the repository.

**Where to look:** [`configs/config.yaml`](../configs/config.yaml)

---

## ✅ 3. Entry-point script runs end-to-end on the sample data

- [ ] An executable script exists under `src/` (e.g. `src/analyze.py`).
- [ ] Running the three Quickstart commands from `README.md` completes **without errors**.
- [ ] The script produces a log file in `results/` and prints a summary to the console.

**Where to look:** [`src/analyze.py`](../src/analyze.py), [`README.md` → Quickstart](../README.md#quickstart--reproducibility-guide)

---

## ✅ 4. Sample data is included for pipeline testing

- [ ] A small synthetic sample (5–10 rows) exists under `data/sample/`.
- [ ] The sample schema matches the columns the analysis script expects.
- [ ] **No real participant data are committed** — only synthetic data.

**Where to look:** [`data/sample/sample_data.csv`](../data/sample/sample_data.csv)

---

## ✅ 5. Randomness is controlled

- [ ] Random seeds are explicitly set in the config (e.g. `random_seed: 42`).
- [ ] The script calls `np.random.seed(...)` (or the equivalent) before any stochastic operation.
- [ ] Re-running the pipeline yields identical results.

**Where to look:** [`configs/config.yaml` → reproducibility](../configs/config.yaml), [`src/analyze.py`](../src/analyze.py)

---

## ✅ 6. README enables a 5-minute reproduction

- [ ] README contains: **Title, Authors, Research Question, Repository Structure, Quickstart Guide, Expected Results table, Citation (BibTeX), License**.
- [ ] Quickstart section lists **three or fewer commands** to reproduce the analysis.
- [ ] System requirements (OS, Python version, RAM) are documented.

**Where to look:** [`README.md`](../README.md)

---

## ✅ 7. Repository hygiene is clean

- [ ] `.gitignore` excludes `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, `*.log`, real data, and model weights.
- [ ] No large binaries, no secrets, no `.env` files, no virtual environments committed.
- [ ] `LICENSE` is present (MIT, Apache 2.0, or CC-BY 4.0).
- [ ] Commit history is informative (each commit message describes the change).

**Where to look:** [`.gitignore`](../.gitignore), [`LICENSE`](../LICENSE), [commit history](https://github.com/nuraiaben-dev/shortform-video-procrastination-study/commits/main)

---

## Verdict

| Items checked | Status |
|---|---|
| 7 / 7 | ✅ Fully reproducible |
| 5–6 / 7 | 🟡 Minor gaps — fix before submission |
| < 5 / 7 | 🔴 Not reproducible — needs rework |

---

## Related documents

- [Methodology Passport Card](methodology.md)
- [Main README](../README.md)
