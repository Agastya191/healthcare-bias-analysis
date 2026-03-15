"""
visualize.py
------------
Generates and saves all figures for the healthcare bias analysis.
All plots use a consistent style and save to outputs/.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns

# ── Style ─────────────────────────────────────────────────────────────────────

PALETTE    = "Blues_d"
ACCENT     = "#C0392B"   # red for worst-off group highlight
GOOD       = "#27AE60"   # green for best-off group
FIG_SIZE   = (10, 5)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")

def _save(fig: plt.Figure, name: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def set_style() -> None:
    sns.set_theme(style="whitegrid", font_scale=1.1)
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor":   "white",
        "axes.edgecolor":   "#CCCCCC",
    })


# ── Individual plots ──────────────────────────────────────────────────────────

def plot_insurance_by_income(income_summary: pd.DataFrame) -> str:
    """Bar chart: insurance coverage rate by income bracket."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    colors = [ACCENT if v == income_summary["insurance_pct"].min()
              else "#2980B9" for v in income_summary["insurance_pct"]]
    bars = ax.bar(income_summary["income_label"], income_summary["insurance_pct"],
                  color=colors, edgecolor="white", linewidth=0.8)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
    ax.set_ylim(0, 105)
    ax.set_xlabel("Annual Household Income", fontsize=12)
    ax.set_ylabel("% With Health Insurance", fontsize=12)
    ax.set_title("Insurance Coverage Rate by Income Level\n(CDC BRFSS)", fontsize=14, fontweight="bold")
    plt.xticks(rotation=30, ha="right")

    # Annotate bars
    for bar, val in zip(bars, income_summary["insurance_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val}%", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    return _save(fig, "01_insurance_by_income")


def plot_cost_barrier_by_income(income_summary: pd.DataFrame) -> str:
    """Bar chart: cost barrier rate by income bracket (reversed — lower is better)."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    colors = [ACCENT if v == income_summary["cost_barrier_pct"].max()
              else "#2980B9" for v in income_summary["cost_barrier_pct"]]
    bars = ax.bar(income_summary["income_label"], income_summary["cost_barrier_pct"],
                  color=colors, edgecolor="white", linewidth=0.8)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
    ax.set_xlabel("Annual Household Income", fontsize=12)
    ax.set_ylabel("% Who Couldn't Afford Doctor Visit", fontsize=12)
    ax.set_title("Cost Barrier to Care by Income Level\n(CDC BRFSS)", fontsize=14, fontweight="bold")
    plt.xticks(rotation=30, ha="right")

    for bar, val in zip(bars, income_summary["cost_barrier_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f"{val}%", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    return _save(fig, "02_cost_barrier_by_income")


def plot_insurance_by_education(education_summary: pd.DataFrame) -> str:
    """Bar chart: insurance coverage by education level."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    colors = [ACCENT if v == education_summary["insurance_pct"].min()
              else "#2980B9" for v in education_summary["insurance_pct"]]
    bars = ax.bar(education_summary["education_label"], education_summary["insurance_pct"],
                  color=colors, edgecolor="white", linewidth=0.8)

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
    ax.set_ylim(0, 110)
    ax.set_xlabel("Highest Education Level", fontsize=12)
    ax.set_ylabel("% With Health Insurance", fontsize=12)
    ax.set_title("Insurance Coverage Rate by Education Level\n(CDC BRFSS)", fontsize=14, fontweight="bold")
    plt.xticks(rotation=25, ha="right")

    for bar, val in zip(bars, education_summary["insurance_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val}%", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    return _save(fig, "03_insurance_by_education")


def plot_health_score_by_income(income_summary: pd.DataFrame) -> str:
    """Line plot: mean self-rated health score by income (1=Excellent, 5=Poor)."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.plot(income_summary["income_label"], income_summary["mean_health_score"],
            marker="o", linewidth=2.5, color="#2980B9", markersize=8)
    ax.fill_between(range(len(income_summary)),
                    income_summary["mean_health_score"],
                    alpha=0.12, color="#2980B9")

    ax.set_xticks(range(len(income_summary)))
    ax.set_xticklabels(income_summary["income_label"], rotation=30, ha="right")
    ax.set_xlabel("Annual Household Income", fontsize=12)
    ax.set_ylabel("Mean Health Score (1=Excellent, 5=Poor)", fontsize=12)
    ax.set_title("Self-Rated Health by Income Level\n(CDC BRFSS)", fontsize=14, fontweight="bold")
    ax.invert_yaxis()   # flip so up = better health

    fig.tight_layout()
    return _save(fig, "04_health_score_by_income")


def plot_correlation_heatmap(corr_matrix: pd.DataFrame) -> str:
    """Heatmap of Pearson correlations between key variables."""
    labels = {
        "income_level":    "Income Level",
        "education_level": "Education Level",
        "has_insurance":   "Has Insurance",
        "cost_barrier":    "Cost Barrier",
        "recent_checkup":  "Recent Checkup",
        "general_health":  "General Health\n(1=Excellent)",
    }
    renamed = corr_matrix.rename(index=labels, columns=labels)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(renamed, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1,
                linewidths=0.5, ax=ax,
                cbar_kws={"shrink": 0.8})
    ax.set_title("Correlation Matrix — Socioeconomic & Health Access Variables\n(CDC BRFSS)",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    return _save(fig, "05_correlation_heatmap")


def plot_odds_ratios(logit_result: dict, title: str, filename: str) -> str:
    """Forest plot of odds ratios from logistic regression."""
    df = logit_result["summary_df"].copy()
    df.index = ["Income Level", "Education Level", "Sex"]

    fig, ax = plt.subplots(figsize=(8, 4))
    y_pos = range(len(df))

    for i, (label, row) in enumerate(df.iterrows()):
        color = ACCENT if row["odds_ratio"] < 1 else GOOD
        ax.plot([row["CI_lower"], row["CI_upper"]], [i, i],
                color=color, linewidth=2.5, solid_capstyle="round")
        ax.scatter(row["odds_ratio"], i, color=color, s=80, zorder=5)
        ax.text(row["CI_upper"] + 0.01, i,
                f'OR={row["odds_ratio"]:.3f}', va="center", fontsize=10)

    ax.axvline(1.0, color="black", linestyle="--", linewidth=1, alpha=0.6)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(df.index, fontsize=11)
    ax.set_xlabel("Odds Ratio (with 95% CI)", fontsize=12)
    ax.set_title(title, fontsize=13, fontweight="bold")

    fig.tight_layout()
    return _save(fig, filename)


def plot_checkup_by_income(income_summary: pd.DataFrame) -> str:
    """Bar chart: recent checkup rate by income."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    colors = [ACCENT if v == income_summary["recent_checkup_pct"].min()
              else "#2980B9" for v in income_summary["recent_checkup_pct"]]
    bars = ax.bar(income_summary["income_label"], income_summary["recent_checkup_pct"],
                  color=colors, edgecolor="white")

    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
    ax.set_ylim(0, 110)
    ax.set_xlabel("Annual Household Income", fontsize=12)
    ax.set_ylabel("% With Routine Checkup in Past Year", fontsize=12)
    ax.set_title("Routine Checkup Rate by Income Level\n(CDC BRFSS)", fontsize=14, fontweight="bold")
    plt.xticks(rotation=30, ha="right")

    for bar, val in zip(bars, income_summary["recent_checkup_pct"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val}%", ha="center", va="bottom", fontsize=9)

    fig.tight_layout()
    return _save(fig, "06_checkup_by_income")


# ── Master runner ─────────────────────────────────────────────────────────────

def generate_all_figures(results: dict) -> list:
    """
    Generate and save all figures. Returns list of saved file paths.
    """
    set_style()
    print("Generating figures...")

    paths = [
        plot_insurance_by_income(results["income_summary"]),
        plot_cost_barrier_by_income(results["income_summary"]),
        plot_insurance_by_education(results["education_summary"]),
        plot_health_score_by_income(results["income_summary"]),
        plot_correlation_heatmap(results["correlation_matrix"]),
        plot_odds_ratios(
            results["logit_insurance"],
            title="Predictors of Insurance Coverage (Logistic Regression OR)",
            filename="07_odds_ratio_insurance",
        ),
        plot_odds_ratios(
            results["logit_cost_barrier"],
            title="Predictors of Cost Barrier to Care (Logistic Regression OR)",
            filename="08_odds_ratio_cost_barrier",
        ),
        plot_checkup_by_income(results["income_summary"]),
    ]
    print(f"  {len(paths)} figures saved to outputs/")
    return paths
