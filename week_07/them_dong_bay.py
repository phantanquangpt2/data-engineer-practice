import sqlite3

conn = sqlite3.connect("crypto_test.db")
cur = conn.cursor()

cur.execute("INSERT INTO prices (coin, price_usd, volume, date) VALUES ('bitcoin', 50, 1000, '2026-09-04')")
conn.commit()

conn.close()