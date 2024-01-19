import requests
import json

url = "http://10.183.210.108:5000/update_product/1/name=hgfidsfhdfhhfjdhfhdhf"

response = requests.put(url)

print(response.text)