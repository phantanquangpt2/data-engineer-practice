import os
import time

import pandas as pd
import requests

BASE_URL = "https://api.coingecko.com/api/v3"
DATA_DIR = "data"


def safe_get(url, params, max_retries=5, timeout=15):
    """Gọi API có timeout và giới hạn số lần thử lại."""
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)

            if response.status_code == 429:
                if attempt == max_retries:
                    print(f"Đã hết {max_retries} lần thử do rate limit: {url}")
                    return None
                wait_seconds = min(10 * attempt, 60)
                print(f"Rate limited. Chờ {wait_seconds}s (lần {attempt})...")
                time.sleep(wait_seconds)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as exc:
            if attempt == max_retries:
                print(f"Đã hết {max_retries} lần thử cho {url}: {exc}")
                return None

            wait_seconds = min(2 * attempt, 10)
            print(f"Request lỗi: {exc}. Thử lại sau {wait_seconds}s...")
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
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    data = safe_get(url, params)

    if not data or not data.get("prices"):
        return pd.DataFrame(columns=["date", "price", "coin_id"])

    df = pd.DataFrame(data["prices"], columns=["timestamp_ms", "price"])
    df["date"] = pd.to_datetime(df["timestamp_ms"], unit="ms").dt.date
    df["coin_id"] = coin_id
    return df[["date", "price", "coin_id"]]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    top_coins = get_top_coins(n=10)
    if top_coins.empty:
        print("Không lấy được danh sách coin; dừng chương trình.")
        return

    top_coins.to_csv(
        os.path.join(DATA_DIR, "top_coins.csv"), index=False, encoding="utf-8"
    )

    all_price_dfs = []
    for coin_id in top_coins["coin_id"]:
        df = get_coin_prices(coin_id, days=30)
        if not df.empty:
            all_price_dfs.append(df)
        time.sleep(1.5)

    if not all_price_dfs:
        print("Không lấy được dữ liệu giá; dừng chương trình.")
        return

    coin_prices = pd.concat(all_price_dfs, ignore_index=True)
    coin_prices.to_csv(
        os.path.join(DATA_DIR, "coin_prices.csv"), index=False, encoding="utf-8"
    )
    print(f"Đã lưu {len(coin_prices)} dòng vào data/coin_prices.csv")

    growth = []
    for coin_id, group in coin_prices.groupby("coin_id"):
        group = group.sort_values("date")
        first_price = group.iloc[0]["price"]
        last_price = group.iloc[-1]["price"]

        if pd.isna(first_price) or first_price == 0 or pd.isna(last_price):
            continue

        pct_change = (last_price - first_price) / first_price * 100
        growth.append(
            {"coin_id": coin_id, "pct_change_30d": round(pct_change, 2)}
        )

    if not growth:
        print("Không đủ dữ liệu hợp lệ để tính tăng trưởng.")
        return

    growth_df = pd.DataFrame(growth).sort_values(
        "pct_change_30d", ascending=False
    )
    print(growth_df.to_string(index=False))
    best = growth_df.iloc[0]
    print(
        f"\nCoin tăng trưởng mạnh nhất: {best['coin_id']} "
        f"({best['pct_change_30d']}%)"
    )


if __name__ == "__main__":
    main()
