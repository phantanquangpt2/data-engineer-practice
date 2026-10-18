# Data Engineer Practice

A personal learning repository for Data Engineering fundamentals. The exercises focus on collecting data from REST APIs, processing JSON with Python and pandas, saving results to CSV/SQLite, and querying data with SQL.

## Skills and tools

- **Python:** requests, pandas, python-dotenv, error handling, retries, timeouts
- **APIs:** Open-Meteo, REST Countries, CoinGecko
- **Storage:** CSV and SQLite
- **SQL:** aggregation with `SUM`, `AVG`, `COUNT`, `GROUP BY`, `HAVING`, and joins
- **Tools:** VS Code, Git, GitHub

## Exercises

- **REST API data collection:** retrieve public API data, parse JSON, and export results to CSV.
- **Weather pipeline:** collect historical weather data and summarize it by city and month.
- **Cryptocurrency pipeline:** retrieve market data from CoinGecko and export the coin list and historical prices to CSV.
- **CSV to SQLite:** validate the CSV files, load them into related SQLite tables, and run SQL checks.
- **SQL practice:** query tables and practice aggregation and joins as the exercises progress.

## Setup

Use Python 3.12 or another compatible Python 3 version.

1. Clone this repository and open the folder in VS Code.
2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) For CoinGecko API access, copy `.env.example` to `.env` and add your own API key to `COINGECKO_API_KEY`. Never commit `.env` or paste API keys into Python files.

## Run the CoinGecko CSV pipeline

From the repository root:

```bash
python week_04/bai_3.py
```

This creates `data/top_coins.csv` and `data/coin_prices.csv`. Requests use timeouts and bounded retries; API rate limits may still apply.

## Load CSV files into SQLite

After the CoinGecko CSV pipeline has created both CSV files, run:

```bash
python week_04/bai_4.py
```

This validates required columns, missing values, timestamp/date consistency, and duplicate coin-timestamp keys before rebuilding `data/crypto.db`. The database contains:

- `top_coins`: one row per coin, including its name and market capitalization.
- `coin_prices`: historical price observations, with a composite primary key on `(coin_id, timestamp_utc)` and a foreign key to `top_coins`.

The script prints record counts, price observations per coin, and each coin's latest available observation. “Latest” refers to the most recent timestamp in the downloaded CSV, not a live market quote.

Example SQL exercises are in `week_04/crypto_queries.sql`. You can run them with a SQLite client after opening `data/crypto.db`.

**Note:** `bai_4.py` rebuilds these two database tables from the CSV files each time it runs. The CSV files remain the source data.

## Run the separate CoinGecko database exercise

From the repository root:

```bash
python week_06/bai_1.py
```

This is a separate exercise that requests Bitcoin and Ethereum market data and writes its own database output. The database is ignored by Git.

## Current learning goals

- Strengthen Python and SQL fundamentals.
- Build reliable API-to-database ETL pipelines.
- Improve data validation, error handling, and incremental loading.
- Document each project so another person can reproduce it.

## Notes

This is a learning repository, so some weekly files are exercises rather than production-ready pipelines. Improvements will be documented as the exercises become more complete.
