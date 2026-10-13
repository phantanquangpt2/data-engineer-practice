import time # thêm khả năng làm việc với tg
import requests # thêm khả năng gọi  API
import pandas as pd # thêm khả năng xử lý bảng dữ  liệu

BASE_URL = 'https://api.open-meteo.com/v1/forecast' # URL của API

CITIES = [
    {'name': 'Ha Noi', 'lat': 21.0278, 'lon': 105.8342},
    {'name': 'Ho Chi Minh', 'lat': 10.8231, 'lon': 106.6297},
    {'name': 'Da Nang', 'lat': 16.0544, 'lon': 108.2022},
]

def get_weather(lat, lon, start_date, end_date, city_name): # gọi function get_weather với các tham số lat, lon, start_date, end_date, city_name 
    params =  { # tạo dict params chứa các tham số cần thiết để gọi API
         'latitude': lat, # tọa độ vĩ độ
         'longtitude': lon, # tọa độ kinh độ
         'daily': 'temperature_2m_max, temperature_2m_min, precipitation_sum', # các thông số thời tiết cần lấy nghĩa của nó là nhiệt độ cao nhất trong ngày ở độ cao 2m, nhiệt độ thấp nhất trong ngày ở độ cao 2m, tổng lượng mưa trong ngày
        'start_date': start_date, # ngày bắt đầu lấy dữ liệu
        'end_date': end_date, # ngày kết thúc lấy dữ liệu
        'timezone': 'Asia/Ho_Chi_Minh', # múi giờ

         }

    attempts = 0 # tạo biến attempts để đếm số lần gọi APT
    while True: # vòng lặp vô hạn
        attempts += 1 #  tăng biến attempts lên 1
        response = requests.get(BASE_URL, params=params) # gọi API với URL và params, lưu kết quả vào biến response

        if response.status_code == 200: #  nếu status_code = 200 thì gọi API thành công
            break # thoát vòng lặp
        if attempts >= 3: # néue attempts >= 3 thì gọi API thất bại
            print(f'[{city_name}] That bai sau 3 lan thu') # in ra thông báo lỗi
            return None # trả về None

        print(f'[{city_name}] lan thu {attempts} lỗi, thử lại...') # in ra thông báo lỗi 



    daily = response.json()['daily'] # lấy dữ liệu daily từ response

    df = pd.DataFrame({ # tạo DataFrame từ dữ liệu daily
        'date': daily['time'], # cột date lấy từ daily['time']  
        'temp_max': daily['temperature_2m_max'], # cột temp_max lấy từ daily['temperature_2m_max']
        'temp_min': daily['temperature_2m_min'], # cột temp_min lấy từ daily['temperature_2m_min']
        'precipitation': daily['precipitation_sum'], # cột precipitation lấy từ daily['precipitation_sum']
        'city': city_name, # cột city lấy từ city_name
    })
    return df   # trả về DataFrame df

if __name__ == '__main__':  # nếu chạy file này trực tiếp thì thực hiện các lệnh bên dưới
    all_dfs =  [] # tạo danh sách rỗng all_dfs để lưu trữ dữ liệu thời tiết của các thành phố
    for city in CITIES: # lặp qua từng thành phố trong danh sách CITIESI
        df  =  get_weather(city['lat'], city['lon'],  '2026-01-01', '2026-01-07', city['name']) # gọi function get_weather với các tham số lat, lon, start_date, end_date, city_name
        if df is not None:  # nếu df ko phải None thì thêm  df vào  danh sách all_dfs
            all_dfs.append(df) # thêm df vào danh sách all_dfs  

if not all_dfs: # nếu danh sách all_dfs rỗng thì in ra thông báo lỗi
    print('không có dữ liệu thời tiết để lưu') # in ra thông báo lỗi
else:
    conmined = pd.concat(all_dfs, ignore_index=True) # nối các DataFrame trong danh sách all_dfs thành một DataFrame duy nhất conmined_df
    conmined['month']  = pd.to_datetime(conmined['date']).dt.month # chuyển cột date sang định dạng datetime và lấy tháng, lưu vào cột month
    conmined.to_csv('weather_data.csv', index=False) # lưu DataFrame conmined vào file CSV với tên 'weather_data.csv' và không lưu chỉ số
    print(f'Da luu {len(conmined)} dong du lieu thoi tiet vao weather_data.csv') # in ra số lượng dòng dữ liệu thời tiết đã lưu vào file CSV


    # Bao cao theo thang: nhiet do trung binh + tong luong mua
    monthly = conmined.groupby(['city', 'month']). agg( # nhóm dữ liệu theo city và month, tính toán các giá trị trung bình và tổng AGG: LÀ TÍNH TOÁN TRENEN TỪNG NHÓM
        avg_temp_max=('temp_max', 'mean'), # tính trung bình nhiệt độ cao nhất trong ngày
        avg_temp_min=('temp_min', 'mean'), # tính trung bình nhiệt độ thấp nhất trong ngày
        total_rain_mm=('precipitation', 'sum'), # tính tổng lượng mưa trong ngày
    ).round(1).reset_index() # làm tròn các giá trị đến 1 chữ số thập phân và đặt lại chỉ số

    print(monthly) # in ra bảng báo cáo theo tháng