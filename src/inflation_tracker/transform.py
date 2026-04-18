"""Data cleaning and harmonisation for multi-country macroeconomic panel."""

from __future__ import annotations

import numpy as np
import pandas as pd


def build_country_year_panel(raw_tidy_df: pd.DataFrame) -> pd.DataFrame:
    """Pivot tidy indicator rows into one country-year panel."""
    panel = raw_tidy_df.pivot_table(
        index=["country_code", "country", "year"],
        columns="indicator",
        values="value",
        aggfunc="mean",
    ).reset_index()

    panel.columns.name = None
    numeric_columns = [
        c
        for c in panel.columns
        if c not in {"country_code", "country", "year"}
    ]

    panel[numeric_columns] = panel[numeric_columns].apply(pd.to_numeric, errors="coerce")

    panel["cycle_phase"] = np.select(
        [panel["year"] <= 2019, panel["year"].between(2020, 2021), panel["year"] >= 2022],
        ["Pre-pandemic", "Pandemic shock", "Post-pandemic tightening"],
        default="Other",
    )

    panel = panel.sort_values(["country", "year"]).reset_index(drop=True)
    return panel


def add_indexed_exchange_rate(panel: pd.DataFrame, base_year: int = 2019) -> pd.DataFrame:
    """Create an indexed exchange-rate series by country to compare depreciation paths."""
    panel = panel.copy()

    def _index_group(group: pd.DataFrame) -> pd.Series:
        base = group.loc[group["year"] == base_year, "exchange_rate_lcu_per_usd"]
        if base.empty or pd.isna(base.iloc[0]) or base.iloc[0] == 0:
            return pd.Series(np.nan, index=group.index)
        return 100 * group["exchange_rate_lcu_per_usd"] / base.iloc[0]

    panel["exchange_rate_index_2019_100"] = (
        panel.groupby("country", group_keys=False).apply(_index_group).reset_index(drop=True)
    )
    return panel
