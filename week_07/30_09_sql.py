import sqlite3

conn = sqlite3.connect("crypto_test.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS prices")
cur.execute("""
CREATE TABLE prices (
    id INTEGER PRIMARY KEY,
    coin TEXT,
    price_usd REAL,
    volume REAL,
    date TEXT
)
""")

data = [
    ("bitcoin", 60000, 30000, "2026-09-01"),
    ("bitcoin", 62000, 28000, "2026-09-02"),
    ("bitcoin", 61000, 35000, "2026-09-03"),
    ("ethereum", 2400, 15000, "2026-09-01"),
    ("ethereum", 2500, 18000, "2026-09-02"),
    ("ethereum", 2350, 12000, "2026-09-03"),
    ("solana", 140, 5000, "2026-09-01"),
    ("solana", 150, 6500, "2026-09-02"),
    ("solana", 145, 4000, "2026-09-03"),
]
cur.executemany("INSERT INTO prices (coin, price_usd, volume, date) VALUES (?, ?, ?, ?)", data)
conn.commit()

SELECT *,
FROM prices 
WHERE coin = 'bitcoin'

conn.close()
print("Xong!")