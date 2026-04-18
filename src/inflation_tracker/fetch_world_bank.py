"""Fetches official macroeconomic indicators from the World Bank API."""

from __future__ import annotations

import logging
import time
from typing import Iterable

import pandas as pd
import requests

from .config import (
    COUNTRIES,
    END_YEAR,
    INDICATORS,
    MAX_API_RETRIES,
    START_YEAR,
    WORLD_BANK_URL,
)

LOGGER = logging.getLogger(__name__)


def fetch_indicator(indicator_code: str, indicator_name: str) -> pd.DataFrame:
    """Fetch one indicator for all selected countries and return tidy rows."""
    countries = ";".join(COUNTRIES.keys())
    url = WORLD_BANK_URL.format(countries=countries, indicator=indicator_code)
    params = {
        "format": "json",
        "per_page": 20000,
        "date": f"{START_YEAR}:{END_YEAR}",
    }

    response = None
    for attempt in range(1, MAX_API_RETRIES + 1):
        try:
            response = requests.get(url, params=params, timeout=30)
        except requests.RequestException as exc:
            LOGGER.warning(
                "Request failed for %s on attempt %s/%s: %s",
                indicator_name,
                attempt,
                MAX_API_RETRIES,
                exc,
            )
            time.sleep(1)
            continue

        if response.ok:
            break

        LOGGER.warning(
            "Non-200 response for %s on attempt %s/%s (status=%s)",
            indicator_name,
            attempt,
            MAX_API_RETRIES,
            response.status_code,
        )
        time.sleep(1)

    if response is None or not response.ok:
        raise RuntimeError(f"Failed to fetch indicator {indicator_name} ({indicator_code})")

    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2:
        raise RuntimeError(f"Unexpected World Bank response for {indicator_name}")

    rows = []
    for item in payload[1]:
        value = item.get("value")
        year = item.get("date")
        country = item.get("country", {}).get("value")
        country_code = item.get("countryiso3code")
        if value is None or year is None or country_code not in COUNTRIES:
            continue

        rows.append(
            {
                "country_code": country_code,
                "country": COUNTRIES[country_code],
                "year": int(year),
                "indicator": indicator_name,
                "value": float(value),
                "source_country_label": country,
            }
        )

    return pd.DataFrame(rows)


def fetch_all_indicators(indicators: dict[str, str] | None = None) -> pd.DataFrame:
    """Fetch all configured indicators and concatenate into a single tidy DataFrame."""
    indicator_map = indicators or INDICATORS
    frames: Iterable[pd.DataFrame] = [
        fetch_indicator(code, name) for name, code in indicator_map.items()
    ]
    combined = pd.concat(frames, ignore_index=True)
    return combined.sort_values(["country_code", "year", "indicator"]).reset_index(drop=True)
