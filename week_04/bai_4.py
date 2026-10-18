from pathlib import Path
import sqlite3

import pandas as pd


# Resolve paths from this script, so it works from any terminal directory.
REPO_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_DIR / "data"
PRICES_CSV = DATA_DIR / "coin_prices.csv"
COINS_CSV = DATA_DIR / "top_coins.csv"
DB_PATH = DATA_DIR / "crypto.db"

PRICE_COLUMNS = ["timestamp_utc", "date", "price", "coin_id"]
COIN_COLUMNS = ["coin_id", "name", "market_cap"]


def load_and_validate_csvs():
    """Read the two CSV files and stop early if their data is invalid."""
    for path in (PRICES_CSV, COINS_CSV):
        if not path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy {path.relative_to(REPO_DIR)}. "
                "Hãy chạy week_04/bai_3.py trước."
            )

    prices = pd.read_csv(PRICES_CSV)
    coins = pd.read_csv(COINS_CSV)

    missing_price_columns = set(PRICE_COLUMNS) - set(prices.columns)
    missing_coin_columns = set(COIN_COLUMNS) - set(coins.columns)
    if missing_price_columns:
        raise ValueError(f"coin_prices.csv thiếu cột: {sorted(missing_price_columns)}")
    if missing_coin_columns:
        raise ValueError(f"top_coins.csv thiếu cột: {sorted(missing_coin_columns)}")
    if prices.empty or coins.empty:
        raise ValueError("CSV đang rỗng; dừng lại để tránh tạo database rỗng.")

    # Normalize timestamps to a consistent UTC ISO-8601 string.
    timestamps = pd.to_datetime(prices["timestamp_utc"], utc=True, errors="coerce")
    if timestamps.isna().any():
        raise ValueError("timestamp_utc có giá trị không hợp lệ.")
    prices["timestamp_utc"] = timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    dates = pd.to_datetime(prices["date"], errors="coerce")
    if dates.isna().any():
        raise ValueError("date có giá trị không hợp lệ.")
    prices["date"] = dates.dt.strftime("%Y-%m-%d")

    prices["price"] = pd.to_numeric(prices["price"], errors="coerce")
    if prices[PRICE_COLUMNS].isna().any().any():
        raise ValueError("Dữ liệu giá có giá trị NULL hoặc không chuyển đổi được.")
    if (prices["price"] < 0).any():
        raise ValueError("Phát hiện giá âm; dừng để kiểm tra dữ liệu.")

    # The date column should match the UTC date portion of timestamp_utc.
    expected_dates = prices["timestamp_utc"].str[:10]
    if not prices["date"].eq(expected_dates).all():
        raise ValueError("date không khớp với ngày UTC trong timestamp_utc.")

    if prices.duplicated(["coin_id", "timestamp_utc"]).any():
        count = int(prices.duplicated(["coin_id", "timestamp_utc"]).sum())
        raise ValueError(
            f"Phát hiện {count} khóa coin_id + timestamp_utc bị trùng; "
            "hãy kiểm tra CSV trước khi nạp."
        )

    for column in ("coin_id",):
        prices[column] = prices[column].astype(str).str.strip()
        coins[column] = coins[column].astype(str).str.strip()
    coins["name"] = coins["name"].astype(str).str.strip()
    coins["market_cap"] = pd.to_numeric(coins["market_cap"], errors="coerce")

    if prices["coin_id"].eq("").any() or coins[["coin_id", "name"]].eq("").any().any():
        raise ValueError("coin_id hoặc name đang để trống.")
    if coins["coin_id"].duplicated().any():
        raise ValueError("top_coins.csv có coin_id trùng lặp.")

    unknown_coins = sorted(set(prices["coin_id"]) - set(coins["coin_id"]))
    if unknown_coins:
        raise ValueError(f"Có coin_id trong lịch sử giá không nằm trong danh sách: {unknown_coins}")

    return coins[COIN_COLUMNS], prices[PRICE_COLUMNS]


def rebuild_database(coins, prices):
    """Rebuild the two tables from the validated CSV source files."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("DROP TABLE IF EXISTS coin_prices")
        connection.execute("DROP TABLE IF EXISTS top_coins")

        connection.execute(
            """
            CREATE TABLE top_coins (
                coin_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                market_cap REAL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE coin_prices (
                timestamp_utc TEXT NOT NULL,
                date TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                coin_id TEXT NOT NULL,
                PRIMARY KEY (coin_id, timestamp_utc),
                FOREIGN KEY (coin_id) REFERENCES top_coins (coin_id)
            )
            """
        )

        coins.to_sql("top_coins", connection, if_exists="append", index=False)
        prices.to_sql("coin_prices", connection, if_exists="append", index=False)

        connection.execute(
            "CREATE INDEX idx_coin_prices_date ON coin_prices (date)"
        )


def show_sql_checks():
    """Run a few SQL queries to verify and explore the loaded tables."""
    with sqlite3.connect(DB_PATH) as connection:
        coin_count = connection.execute(
            "SELECT COUNT(*) FROM top_coins"
        ).fetchone()[0]
        price_count = connection.execute(
            "SELECT COUNT(*) FROM coin_prices"
        ).fetchone()[0]

        print(f"\nĐã tạo database: {DB_PATH.relative_to(REPO_DIR)}")
        print(f"Số coin trong top_coins: {coin_count}")
        print(f"Số dòng trong coin_prices: {price_count}")

        counts = pd.read_sql_query(
            """
            SELECT c.coin_id, c.name, COUNT(p.timestamp_utc) AS price_points
            FROM top_coins AS c
            LEFT JOIN coin_prices AS p ON p.coin_id = c.coin_id
            GROUP BY c.coin_id, c.name
            ORDER BY price_points DESC, c.coin_id
            """,
            connection,
        )
        print("\nSố điểm dữ liệu giá theo coin (JOIN + GROUP BY):")
        print(counts.to_string(index=False))

        latest = pd.read_sql_query(
            """
            SELECT c.coin_id, c.name, p.timestamp_utc, p.price
            FROM top_coins AS c
            JOIN coin_prices AS p ON p.coin_id = c.coin_id
            WHERE p.timestamp_utc = (
                SELECT MAX(p2.timestamp_utc)
                FROM coin_prices AS p2
                WHERE p2.coin_id = c.coin_id
            )
            ORDER BY c.name
            """,
            connection,
        )
        print("\nGiá mới nhất có trong CSV cho mỗi coin:")
        print(latest.to_string(index=False))


def main():
    coins, prices = load_and_validate_csvs()
    print(f"Đã kiểm tra CSV: {len(coins)} coin, {len(prices)} dòng giá.")
    rebuild_database(coins, prices)
    show_sql_checks()


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, sqlite3.Error) as exc:
        raise SystemExit(f"Lỗi: {exc}") from exc
