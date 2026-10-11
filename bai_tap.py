import pandas as pd
import sqlite3

df = pd.read_csv('d:/Học DATA ENGINEER/Tuần 2/orders.csv')

df['doanh_thu'] = df['quantity'] * df['price']  

print()
print("=" * 45)
print("  PANDAS: Doanh thu theo Category")
print("=" * 45)

pandas_category = (
    df.groupby('category')['doanh_thu'].sum().reset_index().sort_values('doanh_thu', ascending=False)
)

print(f"{'category':<12} {'doanh_thu':>12}")
for _, row in pandas_category.iterrows():
    print(f"{row['category']:<12} {row['doanh_thu']:>12,}")

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
    
print()
print("=" * 50)
print("  SQL: Doanh thu theo thanh pho")
print("=" * 50)

sql_q2 = pd.read_sql_query('''
    SELECT
        city,
        SUM(quantity*price) AS doanh_thu
    FROM orders
    GROUP BY city
    ORDER BY doanh_thu DESC
''', conn)
print(f"{'city':<10} {'doanh_thu':>12}")
for _, row in sql_q2.iterrows():
    print(f"{row['city']:<10} {row['doanh_thu']:>12,.0f}")

conn.close()