order_json = '''  
{
    "order_id": 1024,
    "customer": {
        "name": "Nguyen Van A",
        "address": {
            "city": "Ho Chi Minh City",
            "district": "Q1"
        }
    },
    "items": [
        {"product": "Laptop", "qty": 1, "price": 15000000},
        {"product": "Mouse", "qty": 2, "price": 200000}
    ]
}
'''  #  ở  trên  là  dữ  liệu  dạng  json  
import json  #   mở  thư viện  json

order  = json.loads(order_json) # chuyển dữ liệu  json ( string) sang dữ  liệu  python (dictionary)

order["customer"]["name"] # truy xuất  giá  trị từ ngoài vào trong vì đang ở  dữ liệu python (dictionary)  nên  gọi  bằng key
order["customer"]["address"]["city"]  # truy xuất  giá  trị từ ngoài vào trong vì đang ở  dữ liệu python (dictionary)  nên  gọi  bằng key

total = 0 # tạo biến total gắn giá trị ban đầu là 0
for items in order["items"]: # duyệt items qua từng giá trị trong list order["items"], items đại diện cho  từng dictionary trong list
    items["qty"] # truy cập giá trị của key "qty" trong dictionary items
    items["price"] # truy cập giá trị của key "price" trong dictionary items
    total = total + items["qty"] * items["price"] # cộng các giá trị lại với nhau và lưu vào biến total

print(f"Order #{order['order_id']}- {order['customer']['name']} - Total:{total:,}VND")
 # in ra kết quả 


