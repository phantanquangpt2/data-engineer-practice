import requests
import pandas as pd
import sqlite3

# Bước 1: Gọi API
response = requests.get("https://jsonplaceholder.typicode.com/posts")

if response.status_code == 200:
    data = response.json()
    
    # Bước 2: Chuyển thành DataFrame
    df = pd.DataFrame(data)
    print(f"Lay duoc {len(df)} posts")
    print(df.head())
    
    # Bước 3: Lưu vào SQLite
    conn = sqlite3.connect("posts.db")
    df.to_sql("posts", conn, if_exists="replace", index=False)
    conn.close()
    print("Luu vao SQLite thanh cong!")
else:
    print("Loi:", response.status_code)