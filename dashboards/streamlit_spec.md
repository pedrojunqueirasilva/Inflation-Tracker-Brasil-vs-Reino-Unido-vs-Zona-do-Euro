# Streamlit App Specification

## App Goal
Provide a lightweight alternative to BI tools using the same processed dataset.

## Layout
- Sidebar filters: country multi-select, year range, indicator selector
- Top row cards: latest-year values
- Middle section: trend line for selected indicator
- Bottom section: cycle-phase comparison table and insights text

## Technical Notes
- Use `st.cache_data` when loading `data/processed/macro_panel.csv`
- Reuse project colour palette for consistency
- Keep app intentionally minimal and professional
