import requests
import pandas as pd

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "vs_currencies": "usd",
    "ids": "bitcoin"
}

try:
    response = requests.get(url, params=params, timeout=10)
    print(response.text)
    
    response.raise_for_status()

    print(f"kết quả:{response.status_code}")

    data = response.json()
    print(data)

except requests.exceptions.Timeout:
    print("API timeout")

except requests.exceptions.RequestException as e:
    print("API error:", e)
    
    
print(type(data))
print(data.keys())

coin = list(data.keys())[0]
currency = list(data["bitcoin"].keys())[0]
price = data["bitcoin"]["usd"]
print(coin)
print(currency)
print(price)

row = {
    "coin": coin,
    "currency": currency,
    "price": price
}

df = pd.DataFrame([row])
print(df)


df.to_csv("coin_price.csv", index=False)