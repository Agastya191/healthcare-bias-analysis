"""
preprocess.py
-------------
Loads and cleans the CDC BRFSS dataset for socioeconomic bias analysis.
Selects relevant columns, recodes values, and handles missing data.
"""

import pandas as pd
import numpy as np


# ── Column mappings from BRFSS codebook ──────────────────────────────────────

COLUMNS_OF_INTEREST = {
    "INCOME3":    "income_level",
    "EDUCA":      "education_level",
    "_HLTHPLN":   "has_insurance",
    "MEDCOST1":   "cost_barrier",
    "CHECKUP1":   "last_checkup",
    "GENHLTH":    "general_health",
    "SEXVAR":     "sex",
    "_IMPRACE":   "race",
    "_STATE":     "state",
}

# Human-readable labels for plots
INCOME_LABELS = {
    1: "< $10k",
    2: "$10k–$15k",
    3: "$15k–$20k",
    4: "$20k–$25k",
    5: "$25k–$35k",
    6: "$35k–$50k",
    7: "$50k–$75k",
    8: "> $75k",
}

EDUCATION_LABELS = {
    1: "Never attended",
    2: "Grades 1–8",
    3: "Grades 9–11",
    4: "Grade 12 / GED",
    5: "Some college",
    6: "College graduate",
}

HEALTH_LABELS = {
    1: "Excellent",
    2: "Very good",
    3: "Good",
    4: "Fair",
    5: "Poor",
}


def load_brfss(filepath: str) -> pd.DataFrame:
    """
    Load raw BRFSS CSV file and select columns of interest.

    Parameters
    ----------
    filepath : str
        Path to the downloaded BRFSS .csv file.

    Returns
    -------
    pd.DataFrame
        Raw dataframe with renamed columns.
    """
    print(f"Loading BRFSS data from: {filepath}")
    import pyreadstat
    df, meta = pyreadstat.read_xport(filepath, encoding="latin1")
    df = df[[c for c in COLUMNS_OF_INTEREST.keys() if c in df.columns]]
    df.rename(columns=COLUMNS_OF_INTEREST, inplace=True)
    print(f"  Raw shape: {df.shape}")
    return df


def clean_brfss(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recode BRFSS sentinel values (7=Don't know, 9=Refused) to NaN,
    apply human-readable labels, and drop rows with too many missing values.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe from load_brfss().

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe ready for analysis.
    """
    df = df.copy()

    # Recode don't-know / refused / missing sentinels to NaN
    sentinel_map = {
        "income_level":    [77, 99],
        "education_level": [9],
        "has_insurance":   [7, 9],
        "cost_barrier":    [7, 9],
        "last_checkup":    [7, 8, 9],
        "general_health":  [7, 9],
        "sex":             [7, 9],
        "race":            [9],
    }
    for col, sentinels in sentinel_map.items():
        if col in df.columns:
            df[col] = df[col].replace(sentinels, np.nan)

    # Binary flags (1=Yes, 2=No → 1=Yes, 0=No)
    df["has_insurance"] = df["has_insurance"].map({1: 1, 2: 0})
    df["cost_barrier"]  = df["cost_barrier"].map({1: 1, 2: 0})

    # Had a routine checkup in the past year (1=Yes, else No)
    df["recent_checkup"] = df["last_checkup"].map({1: 1, 2: 0, 3: 0, 4: 0, 8: 0})

    # Readable labels
    df["income_label"]    = df["income_level"].map(INCOME_LABELS)
    df["education_label"] = df["education_level"].map(EDUCATION_LABELS)
    df["health_label"]    = df["general_health"].map(HEALTH_LABELS)

    # Drop rows missing our three key outcome variables
    df.dropna(subset=["income_level", "has_insurance", "cost_barrier"], inplace=True)

    print(f"  Cleaned shape: {df.shape}")
    return df


def load_and_clean(filepath: str) -> pd.DataFrame:
    """Convenience wrapper: load + clean in one call."""
    return clean_brfss(load_brfss(filepath))
