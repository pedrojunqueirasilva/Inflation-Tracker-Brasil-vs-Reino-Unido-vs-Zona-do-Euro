# Project Plan and Technical Roadmap

## 1) Project Goal
Build an end-to-end analytics project to compare inflation pressure, policy conditions, labour-market stress, output growth, and exchange-rate dynamics across Brazil, the UK, and the Euro Area.

## 2) Core Analytical Angle
**Hypothesis:** Countries with stronger post-pandemic inflation pressure should show tighter real-rate conditions and a different cost-of-living profile, reflected in unemployment, growth, and exchange-rate paths.

## 3) Recommended Folder Structure

```text
Inflation-Tracker-Brasil-vs-Reino-Unido-vs-Zona-do-Euro/
├── data/
│   ├── raw/
│   └── processed/
├── src/inflation_tracker/
│   ├── config.py
│   ├── fetch_world_bank.py
│   ├── transform.py
│   ├── analyse.py
│   └── pipeline.py
├── scripts/
│   └── run_pipeline.py
├── notebooks/
│   └── 01_macro_cycle_analysis.ipynb
├── dashboards/
│   ├── powerbi_tableau_spec.md
│   └── streamlit_spec.md
├── docs/
│   ├── project_plan.md
│   ├── linkedin_post.md
│   └── interview_talking_points.md
├── reports/
│   └── figures/
├── requirements.txt
└── README.md
```

## 4) Reliable Public Data Sources and APIs
- **World Bank API (implemented):** harmonised annual macro indicators for all three economies.
- Optional extensions for deeper policy analysis:
  - Banco Central do Brasil (BCB SGS API) for policy rates and BR-specific monthly series
  - ONS API for UK details
  - Eurostat API for Euro Area labour and inflation detail
  - ECB SDW API for rates and monetary aggregates

## 5) Technical Roadmap (Simple Step-by-Step)
1. Define countries and indicators in `config.py`.
2. Pull data from World Bank API in `fetch_world_bank.py`.
3. Store raw tidy data in `data/raw/`.
4. Pivot and clean data into a country-year panel in `transform.py`.
5. Add exchange-rate index for comparability (2019=100).
6. Save processed table in `data/processed/macro_panel.csv`.
7. Generate insight text and charts in `analyse.py`.
8. Use notebook for interpretation and caveats.
9. Build dashboard using provided specification.

## 6) Analytical Requirements Mapping
- Trend comparison over time: handled by panel and charts.
- Frequency/unit differences: harmonised to annual level and documented.
- Business/policy implications: captured in insight generator and notebook narrative.
- Meaningful insights: pipeline exports at least five.
- Limitations: documented in README and notebook.
