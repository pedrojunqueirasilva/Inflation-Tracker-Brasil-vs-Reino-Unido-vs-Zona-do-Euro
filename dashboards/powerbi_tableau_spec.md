# Dashboard Specification (Power BI / Tableau)

## Objective
Answer the core question: how Brazil, the UK, and the Euro Area behaved through recent economic cycles and what this implies for inflation pressure, policy stance, and cost of living.

## Visual Identity
- Primary: `#1A3A52`
- Secondary: `#2D7A4A`
- Accent: `#C9A961`
- Background: `#F8F9FA`
- Secondary text: `#4A5568`
- Typography: Inter (or Montserrat for titles if available)

## Page 1 — Executive Overview
1. **KPI row (latest year):** Inflation, real interest rate, unemployment, GDP growth, FX index (2019=100)
2. **Main chart:** Inflation trend (line chart, 3 countries)
3. **Secondary chart:** Real interest rate trend (line chart)
4. **Narrative panel:** Top 5 insights from `data/processed/key_insights.md`

## Page 2 — Cycle Comparison
1. **Cycle heatmap/table:** Pre-pandemic vs pandemic shock vs post-pandemic tightening averages
2. **Scatter plot:** Inflation vs unemployment by country-year
3. **Slope chart:** GDP growth shift (2019 to latest year)

## Page 3 — Cost-of-Living Risk Lens
1. **FX index trend:** Imported inflation risk proxy
2. **Inflation minus GDP growth:** Pressure on real income
3. **Country selector:** Single-country drilldown with consistent metric definitions

## Interaction Rules
- Global filters: country, year range, cycle phase
- Tooltips include source and unit
- Keep all visuals uncluttered; avoid decorative elements

## Data Model
Single fact table: `macro_panel.csv`
Dimensions: country, year, cycle phase
Measures: direct indicator fields plus derived calculations in BI layer
