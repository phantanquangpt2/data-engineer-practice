import sqlite3

conn = sqlite3.connect("crypto_test.db")
cur = conn.cursor()

cur.execute("""SELECT coins1.name, coins1.price_usd, prices.price_usd
            FROM coins1 
             LEFT JOIN prices ON prices.coin = coins1.name 
             WHERE prices.price_usd is NULL            
             
             """)

cur.execute("""SELECT DISTINCT coins1.name
FROM coins1
LEFT JOIN prices ON prices.coin = coins1.name
WHERE prices.coin IS NULL""")

print(cur.fetchall())
conn.commit()
conn.close()