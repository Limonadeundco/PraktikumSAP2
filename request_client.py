import requests
import json

url = "http://127.0.0.1:5000/update_product/1/count=2"

response = requests.put(url)

print(response.text)