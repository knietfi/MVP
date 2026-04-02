import requests
url = 'https://yields.llama.fi/pools'
resp = requests.get(url)
data = resp.json().get('data', [])
for p in data:
    if p.get('chain').lower() == 'base':
        print(f"Found Base chain as: {p.get('chain')}")
        break
