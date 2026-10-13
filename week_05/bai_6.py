def calculate_total(amount):
    if amount > 100000:
        discount = amount * 0.1
        final_amount = amount - discount
        return final_amount

    return amount  
# 1. discount và final_amount nằm trong block : if
# 2 return amount ko nằm trong if
# 3. calculate_total() là function nên nó tạo scope riêng đúng không đúng rồi


def check_order(amount):
    if amount > 100000:
        discount = amount * 0.1
    final_amount = amount - discount
        return final_amount

print(check_order(200000))

# tìm lỗi sai
#  final_amount = amount - discount dòng này chưa thụt lề

# =============================

def calculate_price(amount, is_vip):

    if is_vip:

    discount = 0.2 # thụt lề

    else:

    discount = 0.05 # thụt lề

    final_price = amount * (1 - discount)

    return final_price

#    sửa 

def calculate_price(amount, is_vip):

    if is_vip:

       discount = 0.2

    else:

       discount = 0.05

    final_price = amount * (1 - discount)

    return final_price

# if/else tạo code block (một nhóm các dòng code) nhưng không tạo scope( phạm vị hoạt động ) riêng. 
# calculate_price() là function nên tạo scope riêng. 
# Vì vậy biến discount vẫn có thể được sử dụng ở dòng final_price bên ngoài if/else, 
# miễn là một trong hai nhánh if hoặc else đã được thực thi.