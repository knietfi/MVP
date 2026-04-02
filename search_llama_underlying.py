import requests
import json

url = "https://yields.llama.fi/pools"
resp = requests.get(url)
data = resp.json().get("data", [])

usdc = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913".lower()
weth = "0x4200000000000000000000000000000000000006".lower()

results = []
for p in data:
    if p.get("chain") == "Base" and "aerodrome" in p.get("project", "").lower():
        underlying = p.get("underlyingTokens", [])
        if underlying:
            underlying = [u.lower() for u in underlying]
            if usdc in underlying and weth in underlying:
                results.append(p)

print(f"Found {len(results)} pools matching USDC/WETH Aerodrome on Base")
for r in results:
    print(f"Project: {r.get('project')} Pool: {r.get('pool')} symbol: {r.get('symbol')} apy: {r.get('apy')}%")
