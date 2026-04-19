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

## Deploy on Vercel

### Architecture
The project is deployed as a **static analytics site** on Vercel.  
At build time, Vercel runs the Python pipeline, fetches live data from the World Bank API, generates interactive Plotly charts, and assembles a self-contained `public/` directory that is then served as static HTML.

```
build.sh
  └─ pip install -r requirements.txt
  └─ python scripts/run_pipeline.py   →  data/processed/ + reports/figures/
  └─ python scripts/build_site.py     →  public/index.html + public/figures/
```

### Quick deploy
1. Fork or clone this repository.
2. Create a new project on [vercel.com](https://vercel.com) and import the repository.
3. Vercel will auto-detect `vercel.json` — no additional settings are required.
4. Click **Deploy**.

### Configuration (`vercel.json`)
| Setting | Value |
|---|---|
| Build command | `bash build.sh` |
| Output directory | `public/` |
| Framework preset | None (static) |

### Data-refresh model
Data is refreshed **on every deployment** (build-time refresh).  
To keep data current without manual deploys, set up a scheduled redeploy using the Vercel Deploy Hook:

1. Go to **Project → Settings → Git → Deploy Hooks** and create a hook URL.
2. Trigger the hook on a schedule (e.g., weekly) via GitHub Actions, a cron service, or a CI pipeline.

Example GitHub Actions schedule job (`push_refresh` step not required — just call the hook):
```yaml
# .github/workflows/refresh.yml
on:
  schedule:
    - cron: "0 6 * * 1"   # Every Monday 06:00 UTC
jobs:
  redeploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Vercel redeploy
        run: curl -X POST "${{ secrets.VERCEL_DEPLOY_HOOK_URL }}"
```

### Environment variables
No environment variables are required for the current World Bank data sources (public API, no key needed).  
Reserve the following names for future integrations:

| Name | Purpose |
|---|---|
| `BCB_API_KEY` | Banco Central do Brasil (optional, future) |
| `ONS_API_KEY` | ONS UK data API (optional, future) |

### Troubleshooting
| Symptom | Likely cause | Resolution |
|---|---|---|
| Build fails with `RuntimeError: Failed to fetch indicator` | World Bank API unavailable or rate-limited | Retry deploy; API is public and normally stable |
| Charts missing from site | `reports/figures/` not created | Check pipeline logs; ensure `run_pipeline.py` succeeded |
| `public/index.html` shows "No data" messages | Pipeline ran but outputs not found | Verify paths; check for `data/processed/` in build log |

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
