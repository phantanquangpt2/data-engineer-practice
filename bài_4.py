import csv # thư viện csv

def summarize_orders(filepath): # tạo function outer tên summarize_orders(),  nhận filepath là đg dẫn file 
    result = {}  # tạo  dictionary  nằm  trong function  outer

    def add_to_customer(customer, amount): # tạo function  inner add_to_customer, nhận  customer và amount
        if customer in result:  # kiểm tra customer đã tồn tại dictionary result hay chưa
            result[customer] += amount # nếu đã tồn tại thì cộng thêm amount vào tổng tiền hiện tại của kh đó
        else: # ngược lại nếu  chưa tồn tại 
            result[customer] = amount # thì thêm khách hàng vào result và gán amount là tổng tiền ban đầu

    with open(filepath, 'r') as f: # mở file tại filepath ở chở độ đọc('r') và đặt tên file vào biến f
        reader = csv.DictReader(f) # tạo reader = csv.DictReader(f) để đọc từng dòng csv dưới dạng dictionary

        for row in reader: # duyệt row qua từng giá trị ở trong file csv, mỗi row là 1 dictionary
            add_to_customer(row['customer'], float(row['amount'])) # lấy tên KH từ row['customer'], lấy số  tiền tuwfw row['amount'] chuyển số tiền từ str sang float rồi truyền 2 giá trị  đó vào add_to_customer()
    return result # trả về biến result về nơi gọi summarize_orders()