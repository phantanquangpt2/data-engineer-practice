import requests
import pandas  as pd
import time
import sqlite3

API_KEY = "CG-4GFeWEq8MPc8Z8kYP4SBbLgj"

url = "https://api.coingecko.com/api/v3/coins/markets"

params =   {
        "vs_currency":"usd",
        "ids": "bitcoin,ethereum"
    }

def get_coin_data(url, params, timeout=10, max_retries=3):
    headers = {
         "x-cg-demo-api-key": API_KEY
    }
    for attempt in range(max_retries):
        try:
           print(f" Đang thử kết nối lần{attempt  + 1}/{max_retries}")
           
           response = requests.get(url, params=params, timeout=timeout, headers=headers)
           if response.status_code == 200:
              return response.json()
          
           elif response.status_code == 429:
               print("Quá nhiều yêu cầu, xin vui lòng đơi 2 giây trước khi thử lại")
               if attempt < max_retries - 1:
                   time.sleep(2)
                   
           elif response.status_code == 500:
               print(" server lỗi")
               if attempt < max_retries - 1:
                  time.sleep(2)
                  
           else:
               print("loi:", response.status_code)
               return None
    
        except requests.exceptions.RequestException as e:
               print("lỗi kết nối API:",e)
               if attempt < max_retries - 1:
                  time.sleep(2) 
    return None

data = get_coin_data(url, params)
if data is None:
        print("không lấy được dữ liệu từ  API")
        exit()

def filter_coins(data):    
    coin1 = []
    for coin in  data:
          if coin["id"] == "bitcoin"  or   coin["id"]  ==  "ethereum":
            print(coin["name"],coin["symbol"], coin["current_price"])
            coin1.append(coin)
    return coin1

coin1 = filter_coins(data)

def create_dataframe(data):
    df = pd.DataFrame(data)
    df  = df[["id","name", "symbol","current_price", "market_cap", "total_volume", "price_change_percentage_24h"]]
    df = df.rename( columns={
        "id": "coin_id",
        "name": "coin_name",
        "symbol": "ticker",
        "current_price": "price",
        "price_change_percentage_24h": "price_change_24h"
    })
    return df
df = create_dataframe(coin1)

def analyze_data(df):
    average_price = df["price"].mean() 

    df_up = df[df["price_change_24h"] > 0]

    df_sorted = df.sort_values(by="price_change_24h", ascending=False)
    return average_price, df_up, df_sorted

average_price, df_up, df_sorted = analyze_data(df)

conn = sqlite3.connect("coin.db")
df_bitcoin = df[df["coin_id"] == "bitcoin"]
df_bitcoin.to_sql('bitcoin', conn, if_exists='replace', index=False)


df_ethereum = df[df["coin_id"] == "ethereum"]
df_ethereum.to_sql('ethereum', conn, if_exists='replace', index=False)

conn.close()
print("Dữ liệu đã được lưu vào cơ sở dữ liệu SQLite thành công.")