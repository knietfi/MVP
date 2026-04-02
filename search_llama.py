import requests
import json

url = "https://yields.llama.fi/pools"
resp = requests.get(url)
data = resp.json().get("data", [])

# Search for the pool address
target = "0xf33a96b5932d9e9b9a0eda447abd8c9d48d2e0c8".lower()
matches = []
for p in data:
    pool = p.get("pool")
    meta = p.get("poolMeta")
    if pool and pool.lower() == target:
        matches.append(p)
    elif meta and meta.lower() == target:
        matches.append(p)

print(f"Found {len(matches)} matches for address {target}")
for m in matches:
    print(json.dumps(m, indent=2))

if not matches:
    print("\nNo address match. Searching by project='aerodrome-slipstream' and chain='Base'...")
    matches2 = [p for p in data if p.get("chain") == "Base" and p.get("project") == "aerodrome-slipstream"]
    print(f"Found {len(matches2)} aerodrome-slipstream pools on Base")
    for m in matches2:
        symbol = m.get("symbol", "")
        if symbol and "USDC" in symbol and "WETH" in symbol:
            print(json.dumps(m, indent=2))
