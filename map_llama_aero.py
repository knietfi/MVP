import requests
import json

url = "https://yields.llama.fi/pools"
resp = requests.get(url)
data = resp.json().get("data", [])

for p in data:
    if p.get("chain") == "Base" and p.get("project") == "aerodrome-slipstream":
        symbol = p.get("symbol", "")
        if "USDC" in symbol and "WETH" in symbol:
            underlying = p.get("underlyingTokens", [])
            print(f"Pool: {p.get('pool')} | APY: {p.get('apy')} | Underlying: {underlying}")
