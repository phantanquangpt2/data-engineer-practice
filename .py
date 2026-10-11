import requests

url = "https://api.github.com/users/octocat"

response = requests.get(url)

if response.status_code == 200: # 1. Kiểm tra status code

   data = response.json() # 2. Chuyển response thành Python object

   print(data["name"] )# 3. In username

   print(data["repository"] )  # 4. In số repository

   print(data["follower"] )   # 5. In số follower