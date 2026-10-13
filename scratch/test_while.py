trang = 1
while trang <= 5:
    so_dong = trang * 10
    print(f"Dang tai trang {trang} — lay duoc {so_dong} dong")
    trang += 1

print("Tai xong!")


print("="*50)

trang = 1
while True:
    so_dong = trang * 10
    print(f"Dang tai trang {trang} — lay duoc {so_dong} dong")
    trang += 1
    if trang > 5:
        break

print("Tai xong!")


print("="*50)
# Ví dụ thực tế — gọi API
trang = 1
while True:
    du_lieu = goi_api(trang)        # gọi API lấy data
    
    if len(du_lieu) == 0:           # không còn data nữa
        break                        # dừng — không biết trước trang mấy
    
    xu_ly(du_lieu)                  # xử lý data
    trang += 1