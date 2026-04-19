const COUNTRIES = {
  BRA: { name: "Brazil", color: "#1A3A52" },
  GBR: { name: "United Kingdom", color: "#2D7A4A" },
  EMU: { name: "Euro Area", color: "#C9A961" },
};
const COUNTRY_COLOR_BY_NAME = Object.fromEntries(
  Object.values(COUNTRIES).map((country) => [country.name, country.color]),
);

const INDICATORS = {
  inflation_annual_pct: "FP.CPI.TOTL.ZG",
  real_interest_rate_pct: "FR.INR.RINR",
  unemployment_pct: "SL.UEM.TOTL.ZS",
  gdp_growth_pct: "NY.GDP.MKTP.KD.ZG",
  exchange_rate_lcu_per_usd: "PA.NUS.FCRF",
};

const countrySelect = document.getElementById("countrySelect");
const startYearSelect = document.getElementById("startYear");
const endYearSelect = document.getElementById("endYear");
const applyFiltersBtn = document.getElementById("applyFiltersBtn");

const kpiCards = document.getElementById("kpiCards");
const insightsBox = document.getElementById("insights");

let panel = [];

function selectedCountries() {
  return Array.from(countrySelect.selectedOptions).map((o) => o.value);
}

function selectedRange() {
  return {
    startYear: Number(startYearSelect.value),
    endYear: Number(endYearSelect.value),
  };
}

function fmt(v, digits = 1) {
  if (v === null || v === undefined || Number.isNaN(v)) return "n/a";
  return Number(v).toFixed(digits);
}

async function fetchIndicator(indicatorKey, indicatorCode) {
  // World Bank data for the current year is often incomplete, so we query up to last year.
  const currentYear = new Date().getUTCFullYear() - 1;
  const url =
    `https://api.worldbank.org/v2/country/BRA;GBR;EMU/indicator/${indicatorCode}` +
    `?format=json&per_page=20000&date=2000:${currentYear}`;

  const response = await fetch(url);
  if (!response.ok) throw new Error(`Failed to fetch ${indicatorKey}`);

  const data = await response.json();
  const rows = Array.isArray(data) ? data[1] || [] : [];

  return rows
    .filter((row) => row && row.value !== null && COUNTRIES[row.countryiso3code])
    .map((row) => ({
      country: COUNTRIES[row.countryiso3code].name,
      year: Number(row.date),
      [indicatorKey]: Number(row.value),
    }));
}

function mergeIndicators(parts) {
  const byKey = new Map();
  for (const rows of parts) {
    for (const row of rows) {
      const key = `${row.country}-${row.year}`;
      const existing = byKey.get(key) || { country: row.country, year: row.year };
      byKey.set(key, { ...existing, ...row });
    }
  }
  return Array.from(byKey.values()).sort((a, b) => a.year - b.year);
}

function addFxIndex(rows) {
  const baseline = new Map();
  for (const row of rows) {
    if (row.year === 2019 && row.exchange_rate_lcu_per_usd != null) {
      baseline.set(row.country, row.exchange_rate_lcu_per_usd);
    }
  }
  return rows.map((row) => {
    const base = baseline.get(row.country);
    return {
      ...row,
      exchange_rate_index_2019_100:
        base && row.exchange_rate_lcu_per_usd != null
          ? (row.exchange_rate_lcu_per_usd / base) * 100
          : null,
    };
  });
}

function populateYearFilters(rows) {
  const years = [...new Set(rows.map((r) => r.year))].sort((a, b) => a - b);
  startYearSelect.innerHTML = "";
  endYearSelect.innerHTML = "";
  years.forEach((year) => {
    const startOpt = document.createElement("option");
    startOpt.value = String(year);
    startOpt.textContent = String(year);
    const endOpt = document.createElement("option");
    endOpt.value = String(year);
    endOpt.textContent = String(year);
    startYearSelect.appendChild(startOpt);
    endYearSelect.appendChild(endOpt);
  });
  if (years.length) {
    startYearSelect.value = String(years[0]);
    endYearSelect.value = String(years[years.length - 1]);
  }
}

function filteredRows() {
  const countries = new Set(selectedCountries());
  const { startYear, endYear } = selectedRange();
  return panel.filter(
    (r) => countries.has(r.country) && r.year >= startYear && r.year <= endYear,
  );
}

function plotMetric(elementId, metric, yLabel) {
  const rows = filteredRows();
  const traces = selectedCountries().map((country) => {
    const countryRows = rows.filter((r) => r.country === country);
    return {
      x: countryRows.map((r) => r.year),
      y: countryRows.map((r) => r[metric]),
      mode: "lines+markers",
      name: country,
      line: { color: COUNTRY_COLOR_BY_NAME[country] || "#333" },
    };
  });

  Plotly.newPlot(
    elementId,
    traces,
    {
      margin: { t: 20, l: 50, r: 20, b: 40 },
      yaxis: { title: yLabel },
      xaxis: { title: "Year" },
      paper_bgcolor: "#ffffff",
      plot_bgcolor: "#F8F9FA",
      font: { family: "Inter, Roboto, sans-serif", color: "#4A5568" },
      legend: { orientation: "h" },
    },
    { responsive: true },
  );
}

function renderKpis() {
  const rows = filteredRows();
  const latestYear = Math.max(...rows.map((r) => r.year));
  const latest = rows.filter((r) => r.year === latestYear);

  kpiCards.innerHTML = selectedCountries()
    .map((country) => {
      const r = latest.find((row) => row.country === country);
      return `
        <article class="kpi-card">
          <h3>${country} — ${Number.isFinite(latestYear) ? latestYear : "n/a"}</h3>
          <ul>
            <li>Inflation: ${fmt(r?.inflation_annual_pct)}%</li>
            <li>Real interest rate: ${fmt(r?.real_interest_rate_pct)}%</li>
            <li>Unemployment: ${fmt(r?.unemployment_pct)}%</li>
            <li>GDP growth: ${fmt(r?.gdp_growth_pct)}%</li>
            <li>FX index (2019=100): ${fmt(r?.exchange_rate_index_2019_100)}</li>
          </ul>
        </article>
      `;
    })
    .join("");
}

function renderInsights() {
  const rows = filteredRows();
  const post = rows.filter((r) => r.year >= 2021);

  const avgByCountry = (metric, sortDesc = true) => {
    const values = selectedCountries().map((country) => {
      const subset = post.filter((r) => r.country === country && r[metric] != null).map((r) => r[metric]);
      const avg = subset.length ? subset.reduce((a, b) => a + b, 0) / subset.length : NaN;
      return { country, value: avg };
    });
    return values.sort((a, b) => (sortDesc ? b.value - a.value : a.value - b.value));
  };

  const inflation = avgByCountry("inflation_annual_pct", true);
  const unemployment = avgByCountry("unemployment_pct", false);
  const gdp = avgByCountry("gdp_growth_pct", true);

  insightsBox.innerHTML = `
    <strong>Key insights (post-2021)</strong>
    <ol>
      <li>Highest average inflation: <b>${inflation[0]?.country || "n/a"}</b> (${fmt(inflation[0]?.value)}%).</li>
      <li>Lowest average unemployment: <b>${unemployment[0]?.country || "n/a"}</b> (${fmt(unemployment[0]?.value)}%).</li>
      <li>Strongest average GDP growth: <b>${gdp[0]?.country || "n/a"}</b> (${fmt(gdp[0]?.value)}%).</li>
    </ol>
  `;
}

function renderAll() {
  renderKpis();
  renderInsights();
  plotMetric("inflationChart", "inflation_annual_pct", "Inflation (%)");
  plotMetric("realRateChart", "real_interest_rate_pct", "Real interest rate (%)");
  plotMetric("unemploymentChart", "unemployment_pct", "Unemployment (%)");
  plotMetric("gdpChart", "gdp_growth_pct", "GDP growth (%)");
  plotMetric("fxChart", "exchange_rate_index_2019_100", "Index (2019=100)");
}

async function init() {
  try {
    const fetched = await Promise.all(
      Object.entries(INDICATORS).map(([k, code]) => fetchIndicator(k, code)),
    );
    panel = addFxIndex(mergeIndicators(fetched));
    populateYearFilters(panel);
    renderAll();
  } catch (error) {
    insightsBox.innerHTML = `<strong>Data load error:</strong> ${error.message}`;
  }
}

applyFiltersBtn.addEventListener("click", renderAll);
init();
