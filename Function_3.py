# Function 3: thong_ke(filepath)
# → Đọc file CSV bằng csv.DictReader
# → Tính tổng doanh thu, đếm đơn lớn/nhỏ
# → Return 3 thứ: tong_dt, so_don_lon, so_don_nho

import csv

# ===== FUNCTION 1 =====
def tinh_doanh_thu(quantity, price, thue=0):
    doanh_thu = quantity * price
    return doanh_thu * (1 - thue)

# ===== FUNCTION 2 =====
def phan_loai_don(doanh_thu, nguong=100000):
    if doanh_thu >= nguong:
        return "Đơn Lớn"
    else:
        return "Đơn Nhỏ"

# ===== FUNCTION 3 =====
def thong_ke(filepath):
    tong_dt    = 0
    so_don_lon = 0
    so_don_nho = 0

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dt   = tinh_doanh_thu(int(row["quantity"]), int(row["price"]))
            loai = phan_loai_don(dt)
            tong_dt += dt
            if loai == "Đơn Lớn":
                so_don_lon += 1
            else:
                so_don_nho += 1

    return tong_dt, so_don_lon, so_don_nho

# ===== CHẠY THỬ =====
tong, lon, nho = thong_ke(r"orders.csv")
print("="*40)
print("THONG KE DON HANG")
print("="*40)
print(f"Tong doanh thu : {tong:,}")
print(f"Don lon        : {lon}")
print(f"Don nho        : {nho}")


