"""Central configuration for the macroeconomic comparison project."""

from datetime import datetime, timezone

# World Bank economy codes
COUNTRIES = {
    "BRA": "Brazil",
    "GBR": "United Kingdom",
    "EMU": "Euro Area",
}

# World Bank indicator codes
INDICATORS = {
    "inflation_pct": "FP.CPI.TOTL.ZG",  # Inflation, consumer prices (annual %)
    "real_interest_rate_pct": "FR.INR.RINR",  # Real interest rate (%)
    "unemployment_pct": "SL.UEM.TOTL.ZS",  # Unemployment, total (% of labour force)
    "gdp_growth_pct": "NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
    "exchange_rate_lcu_per_usd": "PA.NUS.FCRF",  # Official exchange rate (LCU per US$, period average)
}

START_YEAR = 2000
END_YEAR = datetime.now(timezone.utc).year - 1

WORLD_BANK_URL = "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"
MAX_API_RETRIES = 3
