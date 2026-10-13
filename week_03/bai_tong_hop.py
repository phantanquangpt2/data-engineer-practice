import csv
import pandas as pd

# ===== FUNCTION 1 =====
def tinh_doanh_thu(quantity, price, thue=0):
    doanh_thu = quantity * price
    return doanh_thu * (1 - thue)

# ===== FUNCTION 2 =====
def phan_loai_don(doanh_thu, nguong=200000):
    if doanh_thu >= nguong:
        return "Don Lon"
    else:
        return "Don Nho"
    
df = pd.read_csv("orders.csv")

# ===== DUYỆT BẰNG ITERTUPLES =====
print("="*55)
print(f"{'San pham':<15} {'So luong':<10} {'Doanh thu':<12} {'Loai'}")
print("="*55)

for row in df.itertuples():
    dt   = tinh_doanh_thu(row.quantity, row.price)
    loai = phan_loai_don(dt)
    print(f"{row.product:<15} {row.quantity:<10} {dt:<12,.0f} {loai}")


# ===== PHAN TRANG BANG WHILE =====
PAGE_SIZE = 3   # mỗi trang 3 dòng
trang = 0
total = len(df)

print("\n" + "="*55)
print("PHAN TRANG DU LIEU")

while True:
    bat_dau = trang * PAGE_SIZE
    ket_thuc = bat_dau + PAGE_SIZE

    if bat_dau >= total:
        print("Het du lieu!")
        break

    trang_hien_tai = df.iloc[bat_dau:ket_thuc]
    print(f"\nTrang {trang + 1}:")
    for row in trang_hien_tai.itertuples():
        print(f"  {row.product:<15} {row.quantity}")

    trang += 1
