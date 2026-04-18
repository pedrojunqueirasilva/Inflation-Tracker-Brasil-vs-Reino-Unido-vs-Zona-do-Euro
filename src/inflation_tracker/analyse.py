"""Insight generation and visual outputs for the macro comparison."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px


def _fmt(value: float, decimals: int = 1) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{value:.{decimals}f}"


def generate_key_insights(panel: pd.DataFrame) -> list[str]:
    """Generate concise, business-oriented insights from the processed panel."""
    post = panel[panel["year"] >= 2021]
    latest_year = panel["year"].max()
    latest = panel[panel["year"] == latest_year]

    avg_inflation = post.groupby("country")["inflation_pct"].mean().sort_values(ascending=False)
    avg_unemployment = post.groupby("country")["unemployment_pct"].mean().sort_values()
    avg_gdp = post.groupby("country")["gdp_growth_pct"].mean().sort_values(ascending=False)

    peak_inflation = (
        panel.groupby("country")["inflation_pct"]
        .max()
        .sort_values(ascending=False)
    )

    corr = (
        panel.groupby("country")[["inflation_pct", "real_interest_rate_pct"]]
        .corr()
        .loc[(slice(None), "inflation_pct"), "real_interest_rate_pct"]
        .reset_index(name="inflation_interest_corr")
        .drop(columns="level_1")
    )

    fx_latest = latest.set_index("country")["exchange_rate_index_2019_100"].sort_values(ascending=False)

    insights = [
        f"Post-2021 average inflation was highest in {avg_inflation.index[0]} ({_fmt(avg_inflation.iloc[0])}%), indicating stronger sustained price pressure.",
        f"The highest inflation peak over the full sample occurred in {peak_inflation.index[0]} ({_fmt(peak_inflation.iloc[0])}%), highlighting larger cycle volatility.",
        f"From 2021 onwards, {avg_unemployment.index[0]} recorded the lowest average unemployment ({_fmt(avg_unemployment.iloc[0])}%), suggesting comparatively resilient labour-market conditions.",
        f"Average GDP growth since 2021 was strongest in {avg_gdp.index[0]} ({_fmt(avg_gdp.iloc[0])}%), reflecting a relatively stronger output recovery.",
        f"In {latest_year}, the largest exchange-rate move versus 2019 was observed in {fx_latest.index[0]} (index {_fmt(fx_latest.iloc[0])}), relevant for imported inflation risk.",
    ]

    corr_sorted = corr.sort_values("inflation_interest_corr", ascending=False)
    if not corr_sorted.empty:
        top = corr_sorted.iloc[0]
        insights.append(
            f"The strongest inflation-interest co-movement appears in {top['country']} (correlation {_fmt(top['inflation_interest_corr'], 2)}), consistent with tighter real-rate responses when inflation rises."
        )

    return insights


def save_insights(insights: list[str], output_path: Path) -> None:
    """Save insights as markdown for README and reporting reuse."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Key Insights", ""] + [f"{idx}. {txt}" for idx, txt in enumerate(insights, start=1)]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def save_interactive_charts(panel: pd.DataFrame, output_dir: Path) -> None:
    """Create clean interactive line charts per macro indicator."""
    output_dir.mkdir(parents=True, exist_ok=True)

    chart_specs = {
        "inflation_pct": "Inflation (annual %)",
        "real_interest_rate_pct": "Real interest rate (%)",
        "unemployment_pct": "Unemployment (%)",
        "gdp_growth_pct": "GDP growth (annual %)",
        "exchange_rate_index_2019_100": "Exchange-rate index (2019=100)",
    }

    for column, title in chart_specs.items():
        fig = px.line(
            panel,
            x="year",
            y=column,
            color="country",
            title=title,
            template="plotly_white",
            color_discrete_map={
                "Brazil": "#1A3A52",
                "United Kingdom": "#2D7A4A",
                "Euro Area": "#C9A961",
            },
        )
        fig.update_layout(
            font={"family": "Inter, Roboto, sans-serif", "color": "#4A5568"},
            plot_bgcolor="#F8F9FA",
            paper_bgcolor="#F8F9FA",
        )
        fig.write_html(output_dir / f"{column}.html", include_plotlyjs="cdn")
