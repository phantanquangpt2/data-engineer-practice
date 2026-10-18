# Data Engineer Practice

A personal learning repository for Data Engineering fundamentals. The exercises focus on collecting data from REST APIs, processing JSON with Python and pandas, saving results to CSV/SQLite, and querying data with SQL.

## Skills and tools

- **Python:** requests, pandas, python-dotenv, error handling, retries, timeouts
- **APIs:** Open-Meteo, REST Countries, CoinGecko
- **Storage:** CSV and SQLite
- **SQL:** aggregation with `SUM`, `AVG`, `COUNT`, `GROUP BY`, and `HAVING`
- **Tools:** VS Code, Git, GitHub

## Exercises

- **REST API data collection:** retrieve public API data, parse JSON, and export results to CSV.
- **Cryptocurrency data:** retrieve Bitcoin and Ethereum market data from CoinGecko, analyze it with pandas, and save it into SQLite.
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

## Run the CoinGecko exercise

From the repository root:

```bash
python week_06/bai_1.py
```

The script requests market data for Bitcoin and Ethereum, prints a small analysis, and writes the results to `coin.db` in the current working directory. The database is ignored by Git.

## Current learning goals

- Strengthen Python and SQL fundamentals.
- Build reliable API-to-database ETL pipelines.
- Improve data validation, error handling, and incremental loading.
- Document each project so another person can reproduce it.

## Notes

This is a learning repository, so some weekly files are exercises rather than production-ready pipelines. Improvements will be documented as the exercises become more complete.
