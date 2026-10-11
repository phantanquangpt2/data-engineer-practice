import requests #  mở thư viện requests giống như mở thư  viện pandas

response = requests.get("https://jsonplaceholder.typicode.com/posts/9999")
# requests.get() = gửi yêu cầu GET lên server 
# URL = địa chỉ server cần hỏi
# Giống như:
# Quang mở Chrome → gõ URL → nhấn Enter
# Python làm y vậy nhưng không hiện web
# → chỉ lấy DATA về thôi

# "/posts/1" = lấy bài post số 1
# "/posts/2" = lấy bài post số 2

print("Status code:", response.status_code)

# response = gói hàng server gửi về
# status_code = mã trạng thái trong gói hàng

# 200 = thành công ✅
# 404 = không tìm thấy ❌
# 500 = server lỗi ❌

print("Data:", response.json())

# response.json() = mở gói hàng ra lấy data
# → tự động chuyển JSON thành dictionary Python

# JSON từ server:          Dictionary Python:
# {                        {
#   "id": 1,       →         'id': 1,
#   "title": "..."            'title': '...'
# }                        }

