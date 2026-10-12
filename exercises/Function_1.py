# Function 1: tinh_doanh_thu(quantity, price, thue=0)
# → Tính doanh thu sau thuế
# → Có default parameter thue=0
def tinh_doanh_thu(quantity, price, thue = 0):
    doanh_thu = quantity * price
    doanh_thu_sau_thue = doanh_thu * (1 - thue)
    return doanh_thu_sau_thue

print(tinh_doanh_thu(10, 100))
print(tinh_doanh_thu(10, 100, 0.1))
print(tinh_doanh_thu(10,100, thue = 0.2)) 


quantity = 10
price = 100
thue = 0

doanh_thu = quantity * price
print(f"doanh thu: {doanh_thu}")



quantity = 10
price = 100
thue = 0.1

doanh_thu = quantity * price
print(f"doanh thu: {doanh_thu}")



quantity = 10
price = 100
thue = 0.2

doanh_thu = quantity * price
print(f"doanh thu: {doanh_thu}")
