import requests
import json

url = "https://yields.llama.fi/pools"
resp = requests.get(url)
data = resp.json().get("data", [])

target_addr = "0xf33a96b5932d9e9b9a0eda447abd8c9d48d2e0c8".lower()

for p in data:
    if p.get("chain") == "Base" and "aerodrome" in p.get("project", "").lower():
        if target_addr in str(p).lower():
            print(f"Address {target_addr} found in pool: {p.get('pool')}")
            print(json.dumps(p, indent=2))
