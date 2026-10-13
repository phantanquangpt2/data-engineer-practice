import pandas as pd
import sqlite3
conn = sqlite3.connect('orders.db')

df.to_sql('orders', conn, if_exists='replace', index=False)

print()
print("=" * 50)
print("  SQL: San pham ban duoc > 15 cai")
print("=" * 50)

sql_q1 = pd.read_sql_query('''
    SELECT
        product_name,
        SUM(quantity)        AS tong_ban,
        SUM(quantity*price)  AS doanh_thu
    FROM orders
    GROUP BY product_name
    HAVING tong_ban > 15
    ORDER BY tong_ban DESC
''', conn)

print(f"{'product_name':<14} {'tong_ban':>9} {'doanh_thu':>12}")
for _, row in sql_q1.iterrows():
    
    print(f"{row['product_name']:<14} {int(row['tong_ban']):>9} {row['doanh_thu']:>12,.0f}")