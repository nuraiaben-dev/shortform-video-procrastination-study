# ============================================================
# Dockerfile — reproducible environment for the short-form
# video / procrastination study analysis pipeline.
#
# Build:  docker build -t shortform-study .
# Run:    docker run --rm -v "$PWD":/work shortform-study \
#             python src/analyze.py --config configs/config.yaml \
#                                   --input data/sample/sample_data.csv
# ============================================================

# ---- Base image (pinned) ----
FROM continuumio/miniconda3:24.1.2-0

# ---- Metadata ----
LABEL maintainer="Nuray Akniet <nuraiaben-dev@users.noreply.github.com>"
LABEL description="Analysis pipeline: short-form video & procrastination study"
LABEL version="0.1.0"

# ---- Working directory ----
WORKDIR /work

# ---- Install environment from pinned environment.yml ----
# Copy only the environment file first so that this layer is cached
# and only re-runs when environment.yml changes.
COPY environment.yml /work/environment.yml
RUN conda env create -f /work/environment.yml && \
    conda clean -afy

# ---- Make 'conda run' the default entrypoint ----
# This ensures all commands use the 'shortform-study' environment
# without requiring 'conda activate' (which does not work in non-interactive
# 'docker run' shells by default).
SHELL ["conda", "run", "-n", "shortform-study", "/bin/bash", "-c"]

# ---- Copy the rest of the project ----
COPY . /work

# ---- Default command: run the analysis on the sample data ----
CMD ["python", "src/analyze.py", \
     "--config", "configs/config.yaml", \
     "--input", "data/sample/sample_data.csv"]
