import requests
import json

url = "https://silver-goldfish-7xg65j5rx5xhww4g-5000.app.github.dev/clear_basket/*"

response = requests.delete(url)

print(response.text)