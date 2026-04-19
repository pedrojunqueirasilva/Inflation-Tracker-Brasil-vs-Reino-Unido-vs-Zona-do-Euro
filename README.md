# Inflation Tracker: Brazil vs United Kingdom vs Euro Area

A professional end-to-end analytics project analysing how Brazil, the UK, and the Euro Area behaved across recent economic cycles.

## Core Business and Policy Question
**How have Brazil, the UK, and the Euro Area behaved across recent economic cycles, and what does that reveal about inflation pressure, monetary policy, and cost-of-living conditions?**

## Analytical Hypothesis
Economies with stronger post-pandemic inflation pressure should also show tighter real-rate conditions and different labour-growth-exchange trade-offs.

## Project Structure
See `docs/project_plan.md` for the complete plan, folder structure, and technical roadmap.

## Data Sources (Public and Trustworthy)
This implementation uses the **World Bank API** (official, public, and fully reproducible):
- Inflation, consumer prices (annual %)
- Real interest rate (%)
- Unemployment (% of labour force)
- GDP growth (annual %)
- Official exchange rate (LCU per US$)

Country codes:
- Brazil (`BRA`)
- United Kingdom (`GBR`)
- Euro Area (`EMU`)

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
```

## Web Dashboard (English, Vercel-ready)
This repository now includes a browser dashboard in English:
- `index.html`
- `styles.css`
- `app.js`
- `vercel.json`

The dashboard loads data directly from the World Bank API, applies country/year filters, and renders:
- KPI cards by country (latest year in range)
- Key insights (post-2021)
- Inflation, real interest rate, unemployment, GDP growth, and FX index charts

### Run locally
Use a simple static server from the project root:
```bash
python -m http.server 8000
```
Then open `http://localhost:8000`.

### Deploy on Vercel (step by step)
1. Push your branch to GitHub.
2. Log in to Vercel: https://vercel.com
3. Click **Add New...** → **Project**.
4. Import this GitHub repository.
5. In project settings:
   - Framework Preset: **Other**
   - Build Command: *(leave empty)*
   - Output Directory: *(leave empty, root project)*
6. Click **Deploy**.
7. After deploy, open the generated Vercel URL and verify the charts load.

Notes:
- `vercel.json` is already configured for a clean static deployment.
- The dashboard requires internet access in the browser to reach `api.worldbank.org`.

## Outputs
- Raw tidy data: `data/raw/world_bank_tidy_indicators.csv`
- Processed analytical panel: `data/processed/macro_panel.csv`
- Key insights: `data/processed/key_insights.md`
- Interactive charts: `reports/figures/*.html`
- Notebook: `notebooks/01_macro_cycle_analysis.ipynb`
- Dashboard specifications:
  - `dashboards/powerbi_tableau_spec.md`
  - `dashboards/streamlit_spec.md`

## Notebook Workflow
Open `notebooks/01_macro_cycle_analysis.ipynb` after running the pipeline. The notebook contains:
1. Analytical framing
2. Trend comparison
3. Business and policy interpretation
4. Limitations and caveats

## At Least 5 Meaningful Insights Covered
The pipeline auto-generates a concise insight file (`key_insights.md`) including:
- Relative post-2021 inflation pressure
- Peak inflation comparison
- Labour-market resilience comparison
- Growth recovery comparison
- Exchange-rate pressure differences
- Inflation-interest co-movement

## Limitations and Caveats
- This baseline version uses annual frequency to keep cross-country comparability.
- “Real interest rate” is a broad indicator and not the exact policy rate.
- The next extension is monthly policy and inflation data from BCB, ONS, Eurostat, and ECB APIs.

## Design and Personal Brand Direction
All dashboard specs follow the requested palette and style:
- Deep Dark Blue `#1A3A52`
- Strategic Green `#2D7A4A`
- Soft Gold `#C9A961`
- Pure White `#F8F9FA`
- Charcoal Grey `#4A5568`

Tone and structure are kept analytical, minimalist, and professional (British English).
