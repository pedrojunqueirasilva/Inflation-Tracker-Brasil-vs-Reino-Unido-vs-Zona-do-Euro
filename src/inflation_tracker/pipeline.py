"""End-to-end pipeline for ingestion, processing, and analysis outputs."""

from __future__ import annotations

from pathlib import Path

from .analyse import generate_key_insights, save_insights, save_interactive_charts
from .fetch_world_bank import fetch_all_indicators
from .transform import add_indexed_exchange_rate, build_country_year_panel


def run_pipeline(project_root: Path) -> None:
    """Run all project stages and persist raw/processed analytical assets."""
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    figures_dir = project_root / "reports" / "figures"

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_tidy = fetch_all_indicators()
    raw_tidy.to_csv(raw_dir / "world_bank_tidy_indicators.csv", index=False)

    panel = build_country_year_panel(raw_tidy)
    panel = add_indexed_exchange_rate(panel)
    panel.to_csv(processed_dir / "macro_panel.csv", index=False)

    insights = generate_key_insights(panel)
    save_insights(insights, processed_dir / "key_insights.md")
    save_interactive_charts(panel, figures_dir)


if __name__ == "__main__":
    run_pipeline(Path(__file__).resolve().parents[2])
