import requests
import json

url = "http://127.0.0.1:5000/update_product/1/id=3"

response = requests.put(url)

print(response.text)