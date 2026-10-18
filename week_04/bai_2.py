import os
import time

import pandas as pd
import requests

# API archive phù hợp với dữ liệu lịch sử.
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
DATA_DIR = "data"
CITIES = [
    {"name": "Ha Noi", "lat": 21.0278, "lon": 105.8342},
    {"name": "Ho Chi Minh", "lat": 10.8231, "lon": 106.6297},
    {"name": "Da Nang", "lat": 16.0544, "lon": 108.2022},
]


def get_weather(lat, lon, start_date, end_date, city_name, max_retries=3):
    """Lấy dữ liệu thời tiết lịch sử, có timeout và số lần thử lại giới hạn."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "Asia/Ho_Chi_Minh",
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            daily = response.json().get("daily")

            if not daily or not daily.get("time"):
                print(f"[{city_name}] API không trả về dữ liệu daily.")
                return None

            return pd.DataFrame(
                {
                    "date": daily["time"],
                    "temp_max": daily["temperature_2m_max"],
                    "temp_min": daily["temperature_2m_min"],
                    "precipitation": daily["precipitation_sum"],
                    "city": city_name,
                }
            )

        except (requests.exceptions.RequestException, ValueError, KeyError) as exc:
            if attempt == max_retries:
                print(f"[{city_name}] Thất bại sau {max_retries} lần thử: {exc}")
                return None

            wait_seconds = attempt * 2
            print(
                f"[{city_name}] Lần thử {attempt} lỗi: {exc}. "
                f"Thử lại sau {wait_seconds} giây..."
            )
            time.sleep(wait_seconds)

    return None


def main():
    all_dfs = []

    for city in CITIES:
        df = get_weather(
            city["lat"],
            city["lon"],
            start_date="2026-01-01",
            end_date="2026-01-07",
            city_name=city["name"],
        )
        if df is not None and not df.empty:
            all_dfs.append(df)

    if not all_dfs:
        print("Không có dữ liệu thời tiết để lưu.")
        return

    combined = pd.concat(all_dfs, ignore_index=True)
    combined["month"] = pd.to_datetime(combined["date"]).dt.month

    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, "weather_data.csv")
    combined.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Đã lưu {len(combined)} dòng vào {output_path}")

    monthly = (
        combined.groupby(["city", "month"])
        .agg(
            avg_temp_max=("temp_max", "mean"),
            avg_temp_min=("temp_min", "mean"),
            total_rain_mm=("precipitation", "sum"),
        )
        .round(1)
        .reset_index()
    )

    print("\nBáo cáo theo thành phố và tháng:")
    print(monthly.to_string(index=False))


if __name__ == "__main__":
    main()
