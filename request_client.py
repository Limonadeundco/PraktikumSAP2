import requests
import json

url = "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/add_product/Testaaaaaa&10&Test&10"

response = requests.post(url)

print(response.text)