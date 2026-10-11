total_orders = 0 # tạo biến total_orders và gắn giá trị ban dầu là 0. vì nó  nằm  ngoài function nên nó là global variable  

def add_order(order_amount): # function tên add_order tham  số order_amount
    total_orders = total_orders + order_amount # lỗi vì chưa sửa dụng global mà sử dụng biến total_orders  lỗi UnboundLocalError vì  trong  function  là local chưa phải globla
    return total_orders 

add_order(100)
add_order(50)

print(total_orders)

# sửa lại

total_orders = 0 # tạo biến total_orders và gắn giá trị ban dầu là 0. vì nó  nằm  ngoài function nên nó là global variable  

def add_order(order_amount): # function tên add_order tham  số order_amount
    global total_orders # khai báo total_orders trong function là biến global. Nếu muốn thay đổi biến global mà không dùng global  thì sẽ gặp lỗi UnboundLocalError.
    total_orders = total_orders + order_amount # lấy giá trị ban đầu cộng thêm order_amount 
    return total_orders # trả giá trị hiện tại total_orders ra nơi gọi function   

add_order(100) # gọi function add_order và truyền dữ liệu vào order_amount
add_order(50) # gọi function add_order và truyền dữ liệu vào order_amount

print(total_orders) #  in ra kết quả sau khi chạy xong
