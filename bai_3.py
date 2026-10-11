import time # thêm khả năng làm việc với tg
import requests # thêm  khả năng gọi API
import pandas as pd # thêm khả năng xử lý bảng dữ liệu

BASE_URL = 'https://api.coingecko.com/api/v3'

def safe_get(url, params, max_retries=5): # tạo 1  function tên safe_get, nhận vào URL, tham số API, và số lần thử lại tối đa mặc định là 5 lần ( 3 ĐẾN  5 LẦN )
    attempt = 0 # tạo biến attempt để đếm số lần gọi  API
    while True: # vòng lặp vô hạn
        attempt += 1 #  tăng biến attempt lên 1
        response = requests.get(url, params=params) # gọi API với URL và gửi kèm dữ liệu params, sau đó lưu kết quả trả về vào response

        if response.status_code == 200: #  nếu API trả về kết quả 200 thì trả về dữ liệu JSON sang dictionary luôn
           return response.json()

        if response.status_code == 429: # nếu API trả về kết quả 429 (gửi quá nhiều requests)
           wait = 10 *  attempt # chương trình sẽ chờ dựa trên số lần thử vd: wait = 10 * attempt ( 10 * 1 lần thử  lại)
           print(f'Rate limited. Doi {wait}s... (lan{attempt})') # in thông báo rate limited (đã đạt giới hạn tốc độ ) và chờ
           time.sleep(wait) # tạm dừng tro ng khoảng  thời gian  đó trước khi tiếp tục

        else:
           print(f'loi {response.status_code}: {response.text}')  #  nếu api trả về không phải  lỗi  429 thì  in ra mã  lỗi và in nội dung lỗi ra

        if attempt >= max_retries:  #  nếu số lần thử lại lớn hơn max_retries (5) thì
           print(f'Đã hết {max_retries} lần thử cho {url}') # in ra thông  báo này
           return  None # kết thúc và trả kết quả về None

def get_top_coins(n=10): # tạo fuction có tên là get_top_coins có tham số mặc định là 10
    url = f'{BASE_URL}/coins/markets' #https://api.coingecko.com/api/v3/coins/markets
    params = { # tạo  1 dictionary params để chứa các tham số sẽ gửi về khi gọi kèm API
        'vs_currency': 'usd', # yc giá  coin đc tính theo usd
        'order': 'market_cap_desc', # sắp xếp coin theo vốn hóa thị trường giảm dần
        'per_page': n, # số coin muốn lấy trên mỗi trang là n =10
        'page': 1, # lấy trang số  1

    }

    data =  safe_get(url, params) # tạo 1 biến data để lưu trữ dữ liệu trả về từ function safe_get, sau  khi function này gọi API bằng url và params
    if data is None: # nếu data  trả về là None (api ko lấy được dữ liệu) và kết thúc fuction
        return pd.DataFrame() # thì trả về dataframe rỗng

    rows = [{'coin_id':c['id'], 'name':c['name'], 'market_cap': c['market_cap']} for c in data ] # tạo list rows, duyệt từng dictionary c  trong data, lấy các giá trị id, name market và tạo dictionary mới
    return pd.DataFrame(rows) # chuyển list rows thành DataFrame và trả kết quả df về nơi  gọi function

def get_coin_prices(coin_id, days=30): # tạo fuctionary get_coin_prices với tham số cần gọi coin_id và tham số mặc định days = 30
    url = f'{BASE_URL}/coins/{coin_id}/market_chart' # https://api.coingecko.com/api/v3/coins/bitcoin/market_chart (vidu coin_id = bitcoin)
    params = {'vs_currency': 'usd', 'days': days, 'interval': 'daily'} # tạo dictionary chứa các tham số gửi kèm khi  gọi API tiền tệ usd, sô ngày cần lấy dữ liệu là days, và dữ liệu được  láy theo khoảng daily
    data = safe_get(url, params) # tạo 1 biến data để lưu trữ dữ liệu trả về từ function safe_get, sau  khi function này gọi API bằng url và params
    if data is None: # nếu safe_get ko lấy đc dữ liệu và trả về none 
       return  None # thì trả về nơi gọi  function là none

    price = data['prices'] # tạo biến price để lưu dữ liệu trong key prices của dictionary data
    df = pd.DataFrame(price, columns=['timestamp_ms', 'price']) # chuyển dữ liệu prices thành 1 dataframe(dạng  bảng), và đặt tên 2 cột đó là timestamps_ms và price, rồi lưu dataframe đó và biến df
    df['date']= pd.to_datetime(df['timestamp_ms'], unit='ms').dt.date # chuyển dữ liệu cột timestamps_ms từ đơn vị mili-giây sang ngày tháng, và lấy phần ngày và lưu nó vào cột date
    df['coin_id'] = coin_id # tạo cột coin_id và lưu coin_id vào cột đó
    return df[['date', 'price', 'coin_id']] # trả về dataframe nhưng chỉ lấy 3 cột này (ở đây sử  dụng [[ ]]: để lấy nhiều cột)

if __name__=='__main__': # nếu file chạy thì đúng cho qua chạy tiếp
    top_coins = get_top_coins(n=10) # tạo biến top_coins để lưu fuction get_top_coins(n=10) và gọi fuction get_top_coins(n=10)
    top_coins.to_csv('top_cons.csv', index=False) # lưu file này dưới dạng file csv tên là top_coins.csv

    all_price_dfs = [] # tạo list all_price_dfs rỗng
    for coin_id in top_coins['coin_id']: # duyệt qua từng giá trị trong cột coin_id của DataFrame top_cois
        df = get_coin_prices(coin_id, days=30) # gọi function get_top_coins(coin_id, days=30) lưu vào biến df
        if df is not None: # nếu df không none 
            all_price_dfs.append(df) # thêm DataFrame df vào cuối list all_price_dfs
        time.sleep(1.5) # dừng chương trình 1.5 giây trước chạy tiếp, để tránh gửi requests quá liên tục

coin_prices = pd.concat(all_price_dfs, ignore_index=True) # nối các DataFrame trong all_price_dfc, bỏ index cũ vào index mới, lưu  và coin_prices
coin_prices.to_csv('coin_price.csv', index=False) # tạo file csv tên coin_prices.csv và bỏ index
print(f'đã lưu{len(coin_prices)} dòng vào coin_prices.csv\n') # in ra dòng lệnh đã lưu đồng thời hiện số dòng trong bảng coin_prices và \n  là xuống  dòng

growth = [] # tạo list growth rỗng
for coin_id, group in coin_prices.groupby('coin_id'): # nhóm DataFrame coin_prices theo cột coin_id, sau đó duyệt qua từng nhóm: coin_id nhận giá trị của nhóm  và group chứa dữ liệu của nhóm đó
    group = group.sort_values('date') # sắp xếp DataFrame group theo cột date và lưu trong biến group
    first_price = group.iloc[0]['price'] # lấy  giá trị price ở dòng đầu tiên của Group và lưu vào biến first_price
    last_price = group.iloc[-1]['price']# lấy  giá trị price ở dòng cuối cùng của Group và lưu vào biến last_price
    pct_change = (last_price - first_price) / first_price * 100 # Lấy giá cuối trừ giá đầu, chia cho giá đầu, nhân 100 để tính phần trăm thay đổi của giá, sau đó lưu kết quả vào biến pct_change
    growth.append({'coin_id': coin_id, 'pct_change_30d': round(pct_change,2)}) # thêm 1 dictionary vào list growth, gồm coin_id và phần trăm thay đổi trong 30 ngày đc làm tròn  đến 2 chữ số thập phân

growth_df = pd.DataFrame(growth).sort_values('pct_change_30d', ascending=False) # chuyển list growth thành datafame và sắp xếp cột pct_change_30d giảm dần, lưu kết quả vào biến growth_df
print(growth_df) # in biến growth_df
print(f"\nCoin tăng trưởng  mạnh nhất:{growth_df.iloc[0]['coin_id']}({growth_df.iloc[0]['pct_change_30d']}%)") # in ra mức tăng trưởng mạnh nhật bằng cách lấu cion_id và pct_change_30d ở dòng đầu tiên của growth_df