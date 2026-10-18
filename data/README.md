# Data directory

This folder contains small CSV datasets and outputs used by the learning exercises.

- Existing CSV files are retained as practice/sample data.
- Scripts may regenerate outputs such as `weather_data.csv`, `top_coins.csv`, and `coin_prices.csv`.
- Local SQLite databases (`.db`, `.sqlite`, `.sqlite3`) and secret environment files (`.env`) should stay local and are ignored by Git.
- Do not store API keys, passwords, personal information, or other secrets in this folder.

Run scripts from the repository root so relative paths such as `data/weather_data.csv` resolve consistently.
