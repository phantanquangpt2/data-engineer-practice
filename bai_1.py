import requests #  mở thư viện requests để gọi API
import pandas as  pd # mở  thư viện pandas để xử lý dữ liệu dạng bảng

BASE_URL  = 'https://countries.dev'

def get_countries_by_region(region): # region là tham số truyền vào

    url = f'{BASE_URL}/region/{region}' #  https://countries.dev/region/Americas

    response  = requests.get(url)  # gọi APi, nếu thành công  thì sẽ trả  về  list  và được lưu vào biến data, nếu lỗi thì trả về  rỗng  

    if response.status_code == 200: # nếu status_code = 200 thì gọi API thành công
       data = response.json() # dùng dể lấy dữ nội dung JSON mà API trả về và chuyển nó thành dữ liệu python để chương trình  có thể xử lý được. sau đó được lưu vào biến data
       if isinstance(data,  list):  # kiểm tra xem data có phải là list hay không 
           return  data # nếu đúng thì trả  về  data
       else:
            print(f'API tra ve khong phai list {data}') # nếu không phải list thì in ra thông báo lỗi
            return [] # trả về danh sách rỗng

    else:
         print(f'Error {response.status_code}: {response.text}') # nếu status_code khác 200 thì in ra thông báo lỗi
         return[] # trả về danh sách rỗng

  
def parse_country(country_json):  # gọi function parse_country với tham số country_json là một dict chứa thông tin của một quốc gia

    name = country_json.get('name', 'N/A') # lấy giá trị của key 'name' trong dict country_json, nếu không có thì trả về 'N/A'
    capital = country_json.get('capital', 'N/A') # lấy giá trị của key 'capital' trong dict country_json, nếu không có thì trả về 'N/A'
    population = country_json.get('population', 0) # lấy giá trị của key 'population' trong dict country_json, nếu không có thì trả về 0

    curr_list = country_json.get('currencies', []) # lấy giá trị của key 'currencies' trong dict country_json, nếu không có thì trả về danh sách rỗng
    currency = ', '.join([c.get('code', '') for c in curr_list]) if curr_list else 'N/A' # nếu curr_list không rỗng thì lấy giá trị của key 'code' trong từng dict của curr_list và nối chúng lại bằng dấu phẩy, nếu rỗng thì trả về 'N/A'

    return { # trả về một dict chứa các thông tin cần thiết
        'name': name,
        'capital': capital,
        'population': population,
        'currency': currency,
    }
   
if __name__ == '__main__': # nếu chạy file này trực tiếp thì thực hiện các lệnh bên dưới
    region = "Americas"
    raw_data = get_countries_by_region(region) # gọi function get_countries_by_region với tham số 'Asia' và lưu kết quả vào biến raw_data
    # parsed_data = [parse_country(country) for country in raw_data] # gọi function parse_country cho từng quốc gia trong raw_data và lưu kết quả vào biến parsed_data
    # print(parsed_data)
    parsed_data= []
    for country in raw_data:
        parsed_data.append(parse_country(country))
        if country.get('name') ==  'Panama':
          break
    print(parsed_data)

    df = pd.DataFrame(parsed_data) # tạo một DataFrame từ parsed_data
    df.to_csv(f'countries_{region}1.csv', index=False) # lưu DataFrame vào file CSV với tên 'countries_asia.csv' và không lưu chỉ số
    print(f"{len(parsed_data)} countries saved to countries_asia.csv") # in ra số lượng quốc gia đã lưu vào file CSV

    print(df.head()) # in ra 5 dòng đầu tiên của DataFrame
    print(df.info()) # in ra thông tin về DataFrame, bao gồm số lượng dòng, cột, kiểu dữ liệu và bộ nhớ sử dụng