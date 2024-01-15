import requests
import json

url = "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/update_product/1/name/updated_name"

response = requests.put(url)

print(response.text)