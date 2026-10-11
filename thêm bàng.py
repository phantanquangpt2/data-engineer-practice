import json
import sqlite3 
row = """
{
  "date": "2026-09-30",
  "coins": [
    {"name": "bitcoin", "price_usd": 61000, "change_24h": 1.5},
    {"name": "ethereum", "price_usd": 2400, "change_24h": -0.8},
    {"name": "solana", "price_usd": 145, "change_24h": 3.2},
    {"name": "dogecoin", "price_usd": 0.18, "change_24h": -2.1}
  ]
}
"""
data = json.loads(row)
conn = sqlite3.connect("crypto_test.db")
cur = conn.cursor()
cur.execute("""
            CREATE TABLE IF NOT EXISTS daily_prices (
              date TEXT,
              name TEXT,
              price_usd REAL,
              change_24h REAL            
            )
         """)
for coin in data["coins"]:
    cur.execute("""
                INSERT INTO daily_prices (date, name, price_usd, change_24h)
                VALUES (?, ?, ?, ?)
                """, (data["date"], coin["name"], coin["price_usd"], coin["change_24h"]))   
    
cur.execute("ALTER TABLE daily_prices RENAME TO coins1")
conn.commit()
conn.close()