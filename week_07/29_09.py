import requests

url = "https://api.coingecko.com/api/v3/simple/price"
params = {"ids": "bitcoin", "vs_currencies": "usd"}
response = requests.get(url, params=params)
if response.status_code == 200:
   data = response.json()
   print(f"lấy dữ liệu thành công:{response.status_code}")
else:
    print(f"Request failed with status code:{response.status_code}")
    print(f"Response content: {response.text}")