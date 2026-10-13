# ten,luong,ngay_cong
# Quang,8000000,22
# An,15000000,20
# Binh,9000000,18

import csv

# Tạo file test.csv
data = [
    ["ten", "luong", "ngay_cong"],
    ["Quang", 8000000, 22],
    ["An", 15000000, 20],
    ["Binh", 9000000, 18],
]

with open("test.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(data)


def tinh_luong_thuc(luong, ngay_cong, tong_ngay=22):
    return luong / tong_ngay * ngay_cong

with open("test.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        luong_thuc = tinh_luong_thuc(
            int(row["luong"]), 
            int(row["ngay_cong"])
        )
        print(f"{row['ten']:<10} — luong thuc: {luong_thuc:,.0f}")