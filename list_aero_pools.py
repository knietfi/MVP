import requests
import json

url = "https://yields.llama.fi/pools"
resp = requests.get(url)
data = resp.json().get("data", [])

usdc = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913".lower()
weth = "0x4200000000000000000000000000000000000006".lower()

print(f"{'Pool UUID':40} | {'Symbol':20} | {'APY':8} | {'Project':20}")
for p in data:
    if p.get("chain") == "Base" and "aerodrome" in p.get("project", "").lower():
        u = [t.lower() for t in p.get("underlyingTokens", [])]
        if usdc in u and weth in u:
            print(f"{p.get('pool'):40} | {p.get('symbol'):20} | {p.get('apy'):8.2f}% | {p.get('project'):20}")
