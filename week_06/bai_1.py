import os
import sqlite3
import time

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum",
}
API_KEY = os.getenv("COINGECKO_API_KEY")


def get_coin_data(url=BASE_URL, params=PARAMS, timeout=10, max_retries=3):
    """Fetch market data with a timeout and retries for temporary failures."""
    headers = {"x-cg-demo-api-key": API_KEY} if API_KEY else {}

    for attempt in range(max_retries):
        try:
            print(f"Fetching coin data (attempt {attempt + 1}/{max_retries})...")
            response = requests.get(
                url,
                params=params,
                timeout=timeout,
                headers=headers,
            )

            if response.status_code == 429 or response.status_code >= 500:
                if attempt < max_retries - 1:
                    wait_seconds = 2 * (attempt + 1)
                    print(
                        f"Temporary API error ({response.status_code}); "
                        f"retrying in {wait_seconds} seconds."
                    )
                    time.sleep(wait_seconds)
                    continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as exc:
            if attempt < max_retries - 1:
                wait_seconds = 2 * (attempt + 1)
                print(f"Request failed: {exc}. Retrying in {wait_seconds} seconds.")
                time.sleep(wait_seconds)
            else:
                print(f"Could not fetch data after {max_retries} attempts: {exc}")

    return None


def create_dataframe(data):
    """Keep the fields used by this exercise and give them clear names."""
    if not data:
        return pd.DataFrame(
            columns=[
                "coin_id",
                "coin_name",
                "ticker",
                "price",
                "market_cap",
                "total_volume",
                "price_change_24h",
            ]
        )

    df = pd.DataFrame(data)
    columns = [
        "id",
        "name",
        "symbol",
        "current_price",
        "market_cap",
        "total_volume",
        "price_change_percentage_24h",
    ]
    df = df[columns].rename(
        columns={
            "id": "coin_id",
            "name": "coin_name",
            "symbol": "ticker",
            "current_price": "price",
            "price_change_percentage_24h": "price_change_24h",
        }
    )
    return df


def analyze_data(df):
    """Return the average price, rising coins, and rows sorted by 24h change."""
    if df.empty:
        return None, df.copy(), df.copy()

    average_price = df["price"].mean()
    df_up = df[df["price_change_24h"] > 0]
    df_sorted = df.sort_values(by="price_change_24h", ascending=False)
    return average_price, df_up, df_sorted


def save_to_sqlite(df, database_path="coin.db"):
    """Save each coin to its own SQLite table."""
    if df.empty:
        print("No data to save.")
        return

    with sqlite3.connect(database_path) as conn:
        for coin_id in ("bitcoin", "ethereum"):
            coin_df = df[df["coin_id"] == coin_id]
            if not coin_df.empty:
                coin_df.to_sql(coin_id, conn, if_exists="replace", index=False)


def main():
    data = get_coin_data()
    if data is None:
        print("No data was retrieved; stopping without saving.")
        return

    df = create_dataframe(data)
    if df.empty:
        print("The API returned no coin records; stopping without saving.")
        return

    average_price, df_up, df_sorted = analyze_data(df)
    print("\nRetrieved prices:")
    print(df[["coin_name", "ticker", "price"]].to_string(index=False))
    print(f"\nAverage price across returned coins: {average_price}")
    print("\nCoins with a positive 24-hour price change:")
    print(df_up[["coin_name", "price_change_24h"]].to_string(index=False))
    print("\nCoins sorted by 24-hour price change:")
    print(df_sorted[["coin_name", "price_change_24h"]].to_string(index=False))

    save_to_sqlite(df)
    print("\nData saved to coin.db.")


if __name__ == "__main__":
    main()
