def process_order(order_amount): # outer function
    def apply_discount(amount):  # inner  function
        return amount * 0.9   # lấy amount nhân  0.9 rồi trả  kq về nơi  gọi apply_discount()

    final_amount = apply_discount(order_amount) # gọi apply_discount() với giá  trị order_amount,  sau đó lưu kq mà function trả về vào final_amount
    return final_amount # trả kết quả về final_amount

print(process_order(200000)) # in ra  kết quả và truyền dữ liệu 200000 vào  tham số order_amount


