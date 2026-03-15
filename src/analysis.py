"""
analysis.py
-----------
Statistical analysis of socioeconomic bias in U.S. healthcare access.
Includes chi-square tests, logistic regression, and disparity metrics.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")


# ── Descriptive statistics ────────────────────────────────────────────────────

def access_by_income(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute insurance coverage rate, cost barrier rate, and recent checkup
    rate grouped by income level.

    Returns a DataFrame indexed by income_label, sorted by income_level.
    """
    order = df.groupby("income_label")["income_level"].mean().sort_values().index

    result = (
        df.groupby("income_label")
        .agg(
            n                 = ("has_insurance", "count"),
            insurance_rate    = ("has_insurance", "mean"),
            cost_barrier_rate = ("cost_barrier",  "mean"),
            recent_checkup_rate = ("recent_checkup", "mean"),
            mean_health_score = ("general_health", "mean"),   # lower = better
        )
        .reindex(order)
        .reset_index()
    )
    result["insurance_pct"]      = (result["insurance_rate"]      * 100).round(1)
    result["cost_barrier_pct"]   = (result["cost_barrier_rate"]   * 100).round(1)
    result["recent_checkup_pct"] = (result["recent_checkup_rate"] * 100).round(1)
    return result


def access_by_education(df: pd.DataFrame) -> pd.DataFrame:
    """
    Same metrics grouped by education level.
    """
    order = df.groupby("education_label")["education_level"].mean().sort_values().index

    result = (
        df.groupby("education_label")
        .agg(
            n                   = ("has_insurance", "count"),
            insurance_rate      = ("has_insurance", "mean"),
            cost_barrier_rate   = ("cost_barrier",  "mean"),
            recent_checkup_rate = ("recent_checkup", "mean"),
            mean_health_score   = ("general_health", "mean"),
        )
        .reindex(order)
        .reset_index()
    )
    result["insurance_pct"]      = (result["insurance_rate"]      * 100).round(1)
    result["cost_barrier_pct"]   = (result["cost_barrier_rate"]   * 100).round(1)
    result["recent_checkup_pct"] = (result["recent_checkup_rate"] * 100).round(1)
    return result


# ── Disparity gap metrics ─────────────────────────────────────────────────────

def disparity_gap(summary_df: pd.DataFrame, metric_col: str) -> dict:
    """
    Compute the absolute disparity gap between the best- and worst-off groups.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Output of access_by_income() or access_by_education().
    metric_col : str
        Column name ending in '_pct' to compare.

    Returns
    -------
    dict with keys: best_group, worst_group, best_val, worst_val, gap
    """
    best_idx  = summary_df[metric_col].idxmax()
    worst_idx = summary_df[metric_col].idxmin()
    label_col = summary_df.columns[0]  # first column is the group label
    return {
        "best_group":  summary_df.loc[best_idx,  label_col],
        "worst_group": summary_df.loc[worst_idx, label_col],
        "best_val":    summary_df.loc[best_idx,  metric_col],
        "worst_val":   summary_df.loc[worst_idx, metric_col],
        "gap":         round(summary_df.loc[best_idx, metric_col]
                             - summary_df.loc[worst_idx, metric_col], 1),
    }


# ── Chi-square tests ──────────────────────────────────────────────────────────

def chi_square_test(df: pd.DataFrame, group_col: str, outcome_col: str) -> dict:
    """
    Run a chi-square test of independence between a grouping variable
    (income or education) and a binary outcome (insurance / cost barrier).

    Returns dict with chi2, p_value, degrees_of_freedom, and interpretation.
    """
    contingency = pd.crosstab(df[group_col], df[outcome_col])
    chi2, p, dof, _ = stats.chi2_contingency(contingency)
    return {
        "chi2":   round(chi2, 2),
        "p_value": p,
        "dof":    dof,
        "significant": p < 0.05,
        "interpretation": (
            f"Significant association (p={p:.2e}) between {group_col} "
            f"and {outcome_col}."
            if p < 0.05
            else f"No significant association found (p={p:.4f})."
        ),
    }


# ── Logistic regression ───────────────────────────────────────────────────────

def logistic_regression_insurance(df: pd.DataFrame) -> dict:
    """
    Predict insurance coverage from income level, education level, and sex
    using statsmodels logistic regression for interpretable odds ratios.

    Returns a summary dict with odds ratios and confidence intervals.
    """
    cols = ["income_level", "education_level", "sex", "has_insurance"]
    sub  = df[cols].dropna()

    X = sub[["income_level", "education_level", "sex"]]
    y = sub["has_insurance"]

    X_const = sm.add_constant(X)
    model   = sm.Logit(y, X_const).fit(disp=False)

    odds_ratios = np.exp(model.params)
    conf_int    = np.exp(model.conf_int())
    conf_int.columns = ["CI_lower", "CI_upper"]

    summary = pd.concat([odds_ratios.rename("odds_ratio"), conf_int], axis=1)
    summary = summary.drop("const").round(3)

    return {
        "model":       model,
        "summary_df":  summary,
        "pseudo_r2":   round(model.prsquared, 4),
        "n_obs":       int(model.nobs),
    }


def logistic_regression_cost_barrier(df: pd.DataFrame) -> dict:
    """
    Predict cost barrier from income level, education level, and sex.
    Lower income → higher odds of cost barrier?
    """
    cols = ["income_level", "education_level", "sex", "cost_barrier"]
    sub  = df[cols].dropna()

    X = sub[["income_level", "education_level", "sex"]]
    y = sub["cost_barrier"]

    X_const = sm.add_constant(X)
    model   = sm.Logit(y, X_const).fit(disp=False)

    odds_ratios = np.exp(model.params)
    conf_int    = np.exp(model.conf_int())
    conf_int.columns = ["CI_lower", "CI_upper"]

    summary = pd.concat([odds_ratios.rename("odds_ratio"), conf_int], axis=1)
    summary = summary.drop("const").round(3)

    return {
        "model":      model,
        "summary_df": summary,
        "pseudo_r2":  round(model.prsquared, 4),
        "n_obs":      int(model.nobs),
    }


# ── Correlation ───────────────────────────────────────────────────────────────

def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pearson correlation matrix for numeric socioeconomic + health variables.
    """
    cols = [
        "income_level", "education_level",
        "has_insurance", "cost_barrier",
        "recent_checkup", "general_health",
    ]
    return df[cols].dropna().corr().round(3)


# ── Master runner ─────────────────────────────────────────────────────────────

def run_all_analyses(df: pd.DataFrame) -> dict:
    """
    Run all analyses and return results as a single dictionary.
    Useful for the Jupyter notebook.
    """
    print("Running analyses...")

    income_summary    = access_by_income(df)
    education_summary = access_by_education(df)

    results = {
        "income_summary":    income_summary,
        "education_summary": education_summary,

        # Disparity gaps
        "insurance_gap_income":    disparity_gap(income_summary,    "insurance_pct"),
        "cost_barrier_gap_income": disparity_gap(income_summary,    "cost_barrier_pct"),
        "insurance_gap_edu":       disparity_gap(education_summary, "insurance_pct"),

        # Chi-square tests
        "chi2_income_insurance":    chi_square_test(df, "income_level",    "has_insurance"),
        "chi2_income_cost":         chi_square_test(df, "income_level",    "cost_barrier"),
        "chi2_education_insurance": chi_square_test(df, "education_level", "has_insurance"),

        # Logistic regression
        "logit_insurance":    logistic_regression_insurance(df),
        "logit_cost_barrier": logistic_regression_cost_barrier(df),

        # Correlation
        "correlation_matrix": correlation_matrix(df),
    }

    print("  All analyses complete.")
    return results
