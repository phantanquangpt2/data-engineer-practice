def make_discount_calculator(discount_rate): #  tạo outer function tên là make_discount_calculator chứ tham số discount_rate
    def calculate(order_amount): # tạo inner ffunction tên calculate chứa tham số order_amount
        return order_amount * (1 - discount_rate) # thực hiện phép tính order_amount nhân (1 trừ dicount_rate) và trả  kết quả của phép tính về nơi gọi function
    return calculate # trả fuction calculate về  outer function
 
vip_discount = make_discount_calculator(0.2)   # giảm 20, nhận về kết quả  inner function  đồng thời closure này nhớ discount_rate = 0.2
regular_discount = make_discount_calculator(0.05)  # giảm 5% , nhận về  kết  quả của inner   function đồng thời closure này nhớ regular_discount = 0.05
 
print(vip_discount(1000000)) # gọi function  và  truyền  dữ liệu  vào  và  in  kết  quả 
print(regular_discount(1000000))  # gọi function  và  truyền  dữ liệu  vào  và  in  kết  quả