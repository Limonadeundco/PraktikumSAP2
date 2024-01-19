import requests
import json

url = "http://10.183.210.108:5000/clear_basket/*"

response = requests.delete(url)

print(response.text)