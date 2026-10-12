# Function 2: phan_loai_don(doanh_thu, nguong=500000)
# → "Don lon" nếu doanh_thu >= nguong
# → "Don nho" nếu ngược lại
def phan_loai_don(doanh_thu, nguong=500000):
    if doanh_thu >= nguong:
        return "Đơn Lớn"
    else: 
        return "Đơn Nhỏ"
    
print(phan_loai_don(500))       
print(phan_loai_don(500000))     
print(phan_loai_don(1000000))    
print(phan_loai_don(300, nguong=200))  
