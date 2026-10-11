import pandas as pd


nhan_vien = [
    {"id": 1, "ten": "Quang",  "phong_ban": "SEO",  "luong": 8000000,  "ngay_cong": 22},
    {"id": 2, "ten": "An",     "phong_ban": "Dev",  "luong": 15000000, "ngay_cong": 20},
    {"id": 3, "ten": "Binh",   "phong_ban": "SEO",  "luong": 9000000,  "ngay_cong": 18},
    {"id": 4, "ten": "Lan",    "phong_ban": "Data", "luong": 12000000, "ngay_cong": 22},
    {"id": 5, "ten": "Minh",   "phong_ban": "Dev",  "luong": 16000000, "ngay_cong": 15},
    {"id": 6, "ten": "Huong",  "phong_ban": "Data", "luong": 11000000, "ngay_cong": 22},
]

df = pd.DataFrame(nhan_vien)

def tinh_luong_thuc(luong, ngay_cong, tong_ngay = 22):
    return luong / tong_ngay * ngay_cong

def xep_loai_nv(luong_thuc, nguong = 10000000):
    if luong_thuc > nguong:
        return "cao"
    else:
        return "thap"
    
def thong_ke_phong_ban(ds_nv):
   tong_luong = 0
   so_cao = 0
   so_thap = 0
   for nv in ds_nv:
       luong_thuc = tinh_luong_thuc(nv["luong"], nv["ngay_cong"])
       xep_loai = xep_loai_nv(luong_thuc)
       tong_luong += luong_thuc
       if xep_loai == "cao":
           so_cao += 1
       else: 
           so_thap += 1
   return tong_luong, so_cao, so_thap 

tong_luong, so_cao, so_thap = thong_ke_phong_ban(nhan_vien)
print("="*50)
print(" THÔNG KÊ NHÂN VIÊN THEP PHONG BAN")
print("="*50)
print(f"tong_luong: {tong_luong:,.0f}")
print(f"số_cao: {so_cao}")
print(f"số_thấp: {so_thap}")

print("\n" + "="*50)
print("          THÔNG TIN NHÂN VIÊN")
print("="*50)
print(f"{'ten':<10} | {'luong_thuc':>12} | {'xep_loai'}")
print("="*50)

for row in df.itertuples():
    luong_thuc = tinh_luong_thuc(row.luong, row.ngay_cong)
    xep_loai = xep_loai_nv(luong_thuc)
    print(f"{row.ten:<10} | {luong_thuc:>12,.0f} | {xep_loai}")

PAGE_SIZE = 2
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
        print(f" {row.ten} {row.luong} {row.phong_ban}")
    trang += 1
