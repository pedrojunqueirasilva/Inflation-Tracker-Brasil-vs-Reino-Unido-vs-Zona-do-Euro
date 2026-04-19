"""Assemble the static public/ site from pipeline-generated outputs.

Reads:
  data/processed/key_insights.md
  reports/figures/*.html  (Plotly interactive charts)

Writes:
  public/index.html
  public/figures/<name>.html  (copied chart files)
"""

from __future__ import annotations

import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

PUBLIC_DIR = PROJECT_ROOT / "public"
FIGURES_SRC = PROJECT_ROOT / "reports" / "figures"
FIGURES_DST = PUBLIC_DIR / "figures"
INSIGHTS_SRC = PROJECT_ROOT / "data" / "processed" / "key_insights.md"

CHART_TITLES = {
    "inflation_pct": "Inflation (Annual %)",
    "real_interest_rate_pct": "Real Interest Rate (%)",
    "unemployment_pct": "Unemployment (%)",
    "gdp_growth_pct": "GDP Growth (Annual %)",
    "exchange_rate_index_2019_100": "Exchange-Rate Index (2019 = 100)",
}


def _read_insights(path: Path) -> list[str]:
    """Parse numbered bullet lines from the key_insights.md file."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    lines = []
    for line in text.splitlines():
        m = re.match(r"^\d+\.\s+(.+)$", line.strip())
        if m:
            lines.append(m.group(1))
    return lines


def _copy_figures(src: Path, dst: Path) -> list[str]:
    """Copy chart HTML files and return their filenames (without extension)."""
    if not src.exists():
        return []
    dst.mkdir(parents=True, exist_ok=True)
    names = []
    for html_file in sorted(src.glob("*.html")):
        shutil.copy2(html_file, dst / html_file.name)
        names.append(html_file.stem)
    return names


def _insight_cards_html(insights: list[str]) -> str:
    if not insights:
        return (
            '<p class="no-data">No insights available — run the pipeline first.</p>'
        )
    cards = []
    for i, text in enumerate(insights, start=1):
        cards.append(
            f'<div class="card">'
            f'<span class="card-num">{i:02d}</span>'
            f'<p>{text}</p>'
            f"</div>"
        )
    return "\n".join(cards)


def _chart_section_html(figure_stems: list[str]) -> str:
    if not figure_stems:
        return (
            '<p class="no-data">No charts available — run the pipeline first.</p>'
        )
    sections = []
    for stem in figure_stems:
        title = CHART_TITLES.get(stem, stem.replace("_", " ").title())
        sections.append(
            f'<section class="chart-block">'
            f"<h3>{title}</h3>"
            f'<iframe src="figures/{stem}.html" '
            f'title="{title}" '
            f'loading="lazy" '
            f'allowfullscreen>'
            f"</iframe>"
            f"</section>"
        )
    return "\n".join(sections)


HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Inflation Tracker — Brazil vs UK vs Euro Area</title>
  <meta name="description"
        content="End-to-end macro analytics comparing inflation pressure, monetary policy, and cost-of-living conditions across Brazil, the United Kingdom, and the Euro Area." />
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    :root {{
      --navy:   #1A3A52;
      --green:  #2D7A4A;
      --gold:   #C9A961;
      --white:  #F8F9FA;
      --grey:   #4A5568;
      --radius: 8px;
      --shadow: 0 2px 12px rgba(0,0,0,.10);
    }}

    body {{
      font-family: 'Inter', 'Roboto', system-ui, sans-serif;
      background: var(--white);
      color: var(--grey);
      line-height: 1.6;
    }}

    /* ─── Header ─────────────────────────────────────── */
    header {{
      background: var(--navy);
      color: var(--white);
      padding: 3rem 1.5rem 2.5rem;
      text-align: center;
    }}
    header h1 {{
      font-size: clamp(1.5rem, 3vw, 2.4rem);
      font-weight: 700;
      letter-spacing: -.02em;
      color: var(--white);
    }}
    header .subtitle {{
      margin-top: .6rem;
      font-size: 1.05rem;
      opacity: .85;
      max-width: 680px;
      margin-inline: auto;
    }}
    header .meta {{
      margin-top: 1.2rem;
      font-size: .85rem;
      opacity: .65;
    }}

    /* ─── Layout ─────────────────────────────────────── */
    main {{
      max-width: 1100px;
      margin-inline: auto;
      padding: 2.5rem 1.5rem 4rem;
    }}

    section {{ margin-bottom: 3rem; }}

    h2 {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--navy);
      border-left: 4px solid var(--gold);
      padding-left: .75rem;
      margin-bottom: 1.2rem;
    }}

    h3 {{
      font-size: 1rem;
      font-weight: 600;
      color: var(--navy);
      margin-bottom: .6rem;
    }}

    /* ─── Insight cards ──────────────────────────────── */
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }}
    .card {{
      background: var(--white);
      border: 1px solid #dde3ec;
      border-radius: var(--radius);
      padding: 1.1rem 1.2rem;
      box-shadow: var(--shadow);
      display: flex;
      gap: .85rem;
      align-items: flex-start;
    }}
    .card-num {{
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--gold);
      line-height: 1;
      flex-shrink: 0;
    }}
    .card p {{
      font-size: .92rem;
      color: var(--grey);
    }}

    /* ─── Charts ─────────────────────────────────────── */
    .chart-block {{
      border: 1px solid #dde3ec;
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: var(--shadow);
      background: var(--white);
      margin-bottom: 1.5rem;
    }}
    .chart-block h3 {{
      background: var(--navy);
      color: var(--white);
      padding: .6rem 1rem;
      font-size: .95rem;
    }}
    .chart-block iframe {{
      width: 100%;
      height: 440px;
      border: none;
      display: block;
    }}

    /* ─── No-data state ──────────────────────────────── */
    .no-data {{
      color: var(--grey);
      font-style: italic;
      opacity: .7;
      padding: 1rem 0;
    }}

    /* ─── Footer ─────────────────────────────────────── */
    footer {{
      background: var(--navy);
      color: rgba(248,249,250,.65);
      text-align: center;
      padding: 1.5rem 1rem;
      font-size: .82rem;
    }}
    footer a {{
      color: var(--gold);
      text-decoration: none;
    }}

    @media (max-width: 600px) {{
      .chart-block iframe {{ height: 320px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Inflation Tracker<br><span style="color:var(--gold)">Brazil · United Kingdom · Euro Area</span></h1>
    <p class="subtitle">
      How have Brazil, the UK, and the Euro Area behaved across recent economic cycles —
      and what does that reveal about inflation pressure, monetary policy, and cost-of-living conditions?
    </p>
    <p class="meta">Data: World Bank API &nbsp;·&nbsp; Updated: {updated}</p>
  </header>

  <main>
    <section id="insights">
      <h2>Key Insights</h2>
      <div class="cards">
        {insight_cards}
      </div>
    </section>

    <section id="charts">
      <h2>Interactive Charts</h2>
      {chart_sections}
    </section>

    <section id="about">
      <h2>About This Project</h2>
      <p>
        An end-to-end analytics project analysing macroeconomic cycles using
        official World Bank data (annual frequency).
        Indicators: Inflation (CPI), Real Interest Rate, Unemployment,
        GDP Growth, Official Exchange Rate.
      </p>
      <p style="margin-top:.75rem">
        Countries: <strong>Brazil (BRA)</strong> · <strong>United Kingdom (GBR)</strong> · <strong>Euro Area (EMU)</strong>.
        Cycle phases defined as Pre-pandemic (≤ 2019), Pandemic shock (2020–2021),
        and Post-pandemic tightening (≥ 2022).
      </p>
      <p style="margin-top:.75rem;font-size:.9rem;opacity:.8">
        <em>Caveat:</em> Annual data masks intra-year dynamics.
        "Real interest rate" is a broad World Bank indicator, not the exact
        central-bank policy rate.
      </p>
    </section>
  </main>

  <footer>
    <p>
      Built with Python · Plotly · Deployed on
      <a href="https://vercel.com" rel="noopener">Vercel</a>
      &nbsp;·&nbsp; Source on
      <a href="https://github.com/pedrojunqueirasilva/Inflation-Tracker-Brasil-vs-Reino-Unido-vs-Zona-do-Euro"
         rel="noopener">GitHub</a>
    </p>
  </footer>
</body>
</html>
"""


def build_site() -> None:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    insights = _read_insights(INSIGHTS_SRC)
    figure_stems = _copy_figures(FIGURES_SRC, FIGURES_DST)

    updated = datetime.now(timezone.utc).strftime("%d %B %Y")

    html = HTML_TEMPLATE.format(
        updated=updated,
        insight_cards=_insight_cards_html(insights),
        chart_sections=_chart_section_html(figure_stems),
    )

    (PUBLIC_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"  index.html written ({len(insights)} insights, {len(figure_stems)} charts)")


if __name__ == "__main__":
    build_site()
