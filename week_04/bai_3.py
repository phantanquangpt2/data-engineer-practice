import os
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.coingecko.com/api/v3"
DATA_DIR = "data"

# A placeholder copied from .env.example is not a real API key.
API_KEY = os.getenv("COINGECKO_API_KEY", "").strip()
if not API_KEY or API_KEY == "your_coingecko_demo_api_key_here":
    API_KEY = None

HEADERS = {"x-cg-demo-api-key": API_KEY} if API_KEY else {}


def retry_delay(response, attempt):
    """Prefer the API's Retry-After header; otherwise use a bounded backoff."""
    if response is not None:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return max(1, min(int(retry_after), 60))
            except ValueError:
                try:
                    retry_at = parsedate_to_datetime(retry_after)
                    if retry_at.tzinfo is None:
                        retry_at = retry_at.replace(tzinfo=timezone.utc)
                    seconds = int((retry_at - datetime.now(timezone.utc)).total_seconds())
                    return max(1, min(seconds, 60))
                except (TypeError, ValueError, OverflowError):
                    pass
    return min(2 ** attempt, 30)


def safe_get(url, params, max_retries=4, timeout=15):
    """Call CoinGecko with a timeout and bounded retries for transient failures."""
    for attempt in range(1, max_retries + 1):
        response = None
        try:
            response = requests.get(
                url, params=params, headers=HEADERS, timeout=timeout
            )

            if response.status_code in (401, 403):
                print(
                    f"API access denied ({response.status_code}). "
                    "Check your CoinGecko API key/plan, or try again without a key "
                    "if you are using the public endpoint."
                )
                return None

            if response.status_code == 429 or response.status_code >= 500:
                if attempt == max_retries:
                    print(
                        f"API temporary error {response.status_code}; "
                        f"stopped after {max_retries} attempts: {url}"
                    )
                    return None
                wait_seconds = retry_delay(response, attempt)
                print(
                    f"API temporary error {response.status_code}. "
                    f"Waiting {wait_seconds}s before retry {attempt + 1}/{max_retries}..."
                )
                time.sleep(wait_seconds)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as exc:
            # Other client errors (for example, invalid parameters) are not transient.
            print(f"API request rejected; not retrying: {exc}")
            return None
        except requests.exceptions.RequestException as exc:
            if attempt == max_retries:
                print(f"Request failed after {max_retries} attempts for {url}: {exc}")
                return None
            wait_seconds = retry_delay(None, attempt)
            print(
                f"Request error: {exc}. Waiting {wait_seconds}s "
                f"before retry {attempt + 1}/{max_retries}..."
            )
            time.sleep(wait_seconds)

    return None


def get_top_coins(n=10):
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": n,
        "page": 1,
    }
    data = safe_get(url, params)

    if not data:
        return pd.DataFrame(columns=["coin_id", "name", "market_cap"])

    return pd.DataFrame(
        [
            {
                "coin_id": coin["id"],
                "name": coin["name"],
                "market_cap": coin["market_cap"],
            }
            for coin in data
        ]
    )


def get_coin_prices(coin_id, days=30):
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    data = safe_get(url, params)

    if not data or not data.get("prices"):
        return pd.DataFrame(columns=["date", "price", "coin_id"])

    df = pd.DataFrame(data["prices"], columns=["timestamp_ms", "price"])
    df["date"] = pd.to_datetime(df["timestamp_ms"], unit="ms", utc=True).dt.date
    df["coin_id"] = coin_id
    return df[["date", "price", "coin_id"]]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    if API_KEY:
        print("CoinGecko API key detected; requests will use the configured key.")
    else:
        print(
            "No real CoinGecko API key configured. Trying public API access; "
            "rate limits may apply."
        )

    top_coins = get_top_coins(n=10)
    if top_coins.empty:
        print("Could not retrieve the coin list; stopping without writing empty output.")
        return

    top_coins.to_csv(
        os.path.join(DATA_DIR, "top_coins.csv"), index=False, encoding="utf-8"
    )
    print(f"Saved {len(top_coins)} coins to data/top_coins.csv")

    all_price_dfs = []
    for index, coin_id in enumerate(top_coins["coin_id"], start=1):
        print(f"Fetching price history for {coin_id} ({index}/{len(top_coins)})...")
        df = get_coin_prices(coin_id, days=30)
        if not df.empty:
            all_price_dfs.append(df)
        if index < len(top_coins):
            time.sleep(2)

    if not all_price_dfs:
        print("Could not retrieve price history; no price CSV was written.")
        return

    coin_prices = pd.concat(all_price_dfs, ignore_index=True)
    coin_prices.to_csv(
        os.path.join(DATA_DIR, "coin_prices.csv"), index=False, encoding="utf-8"
    )
    print(f"Saved {len(coin_prices)} rows to data/coin_prices.csv")

    growth = []
    for coin_id, group in coin_prices.groupby("coin_id"):
        group = group.sort_values("date")
        first_price = group.iloc[0]["price"]
        last_price = group.iloc[-1]["price"]

        if pd.isna(first_price) or first_price == 0 or pd.isna(last_price):
            continue

        pct_change = (last_price - first_price) / first_price * 100
        growth.append({"coin_id": coin_id, "pct_change_30d": round(pct_change, 2)})

    if not growth:
        print("No valid price history available to calculate growth.")
        return

    growth_df = pd.DataFrame(growth).sort_values(
        "pct_change_30d", ascending=False
    )
    print("\n30-day price change:")
    print(growth_df.to_string(index=False))
    best = growth_df.iloc[0]
    print(
        f"\nCoin with the strongest observed 30-day change: {best['coin_id']} "
        f"({best['pct_change_30d']}%)"
    )


if __name__ == "__main__":
    main()
