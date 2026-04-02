import requests
import json

url = "https://yields.llama.fi/pools"
resp = requests.get(url)
data = resp.json().get("data", [])

ids = ['68a26569-7935-430c-8438-e6d27464169d', '37a3de76-47b2-4d76-8575-5231dfb87340']

for p in data:
    if p.get("pool") in ids:
        print(json.dumps(p, indent=2))
