from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

from process_data import load_measurements


ROOT = Path(__file__).resolve().parents[1]

STYLES = {
    "baseline": {
        "color": "#0072B2",
        "marker": "o",
        "linestyle": "-",
        "label": "Baseline",
    },
    "proposed": {
        "color": "#D55E00",
        "marker": "s",
        "linestyle": "--",
        "label": "Proposed",
    },
}


def save_figure(fig, folder, name):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        folder / f"{name}.pdf",
        bbox_inches="tight",
    )
    fig.savefig(
        folder / f"{name}.png",
        dpi=300,
        bbox_inches="tight",
    )


def plot_latency_vs_load(summary):
    fig, ax = plt.subplots(figsize=(7, 4.5))

    for method, style in STYLES.items():
        group = (
            summary.loc[summary["method"] == method]
            .sort_values("input_rows")
        )

        x = group["input_rows"].to_numpy()
        median = group["median_ms"].to_numpy()
        low = group["median_ci_low_ms"].to_numpy()
        high = group["median_ci_high_ms"].to_numpy()

        ax.plot(
            x, median,
            color=style["color"],
            marker=style["marker"],
            linestyle=style["linestyle"],
            label=style["label"],
        )

        # Draw the actual CI endpoints, including asymmetric intervals.
        ax.vlines(x, low, high, color=style["color"])
        ax.scatter(
            x, low, marker="_",
            color=style["color"], s=70,
        )
        ax.scatter(
            x, high, marker="_",
            color=style["color"], s=70,
        )

    ax.set_xscale("log")
    ax.set_xlabel("Input size (rows, logarithmic scale)")
    ax.set_ylabel("Execution time (ms)")
    ax.set_title("Median execution time with bootstrap 95% CI")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()

    return fig


def plot_distribution(measured, summary):
    sizes = sorted(measured["input_rows"].unique())

    fig, axes = plt.subplots(
        1, len(sizes),
        figsize=(3.3 * len(sizes), 4.5),
        squeeze=False,
    )

    for ax, size in zip(axes[0], sizes):
        for position, (method, style) in enumerate(
            STYLES.items(), start=1
        ):
            values = measured.loc[
                (measured["input_rows"] == size)
                & (measured["method"] == method)
                & (measured["success"] == True),
                "duration_ms",
            ].to_numpy()

            if len(values) == 0:
                raise ValueError(
                    f"No successful runs: {method}, {size} rows."
                )

            boxes = ax.boxplot(
                [values],
                positions=[position],
                widths=0.5,
                patch_artist=True,
                showfliers=True,
                medianprops={"color": "black"},
                flierprops={
                    "marker": style["marker"],
                    "markersize": 3,
                    "markeredgecolor": style["color"],
                    "markerfacecolor": "none",
                },
            )

            boxes["boxes"][0].set_facecolor(style["color"])
            boxes["boxes"][0].set_alpha(0.3)
            boxes["boxes"][0].set_linestyle(style["linestyle"])

            row = summary.loc[
                (summary["input_rows"] == size)
                & (summary["method"] == method)
            ].iloc[0]

            # CI is offset slightly from the box for visibility.
            ci_x = position + 0.32
            ax.vlines(
                ci_x,
                row["median_ci_low_ms"],
                row["median_ci_high_ms"],
                color=style["color"],
                linewidth=2,
            )
            ax.scatter(
                [ci_x],
                [row["median_ms"]],
                marker=style["marker"],
                color=style["color"],
                s=25,
                zorder=3,
            )

        ax.set_xticks([1, 2])
        ax.set_xticklabels(["Baseline", "Proposed"])
        ax.set_xlim(0.5, 2.7)
        ax.set_title(f"{int(size):,} input rows")
        ax.set_ylabel("Execution time (ms)")
        ax.grid(axis="y", alpha=0.25)

    fig.suptitle(
        "Execution-time distributions\n"
        "Boxes: IQR; whiskers: 1.5 × IQR; "
        "offset points and bars: median and bootstrap 95% CI",
        fontsize=11,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.88])

    return fig


def create_figures(measured, summary, output_dir):
    plt.rcParams.update({
        "font.size": 10,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    figures = [
        (
            plot_latency_vs_load(summary),
            "fig1_latency_vs_load",
        ),
        (
            plot_distribution(measured, summary),
            "fig2_distribution_boxplot",
        ),
    ]

    for fig, name in figures:
        save_figure(fig, output_dir, name)

    return [fig for fig, name in figures]


def main():
    measured = load_measurements(
        ROOT / "data/raw/comparison_run.jsonl"
    )
    summary = pd.read_csv(
        ROOT / "data/processed/metrics_summary.csv"
    )

    output_dir = ROOT / "reports/figures"
    figures = create_figures(measured, summary, output_dir)

    for fig in figures:
        plt.close(fig)

    print(f"Four figure files saved to: {output_dir}")


if __name__ == "__main__":
    main()
