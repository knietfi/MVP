import json

with open('zerion_complex.json', 'r') as f:
    data = json.load(f)

for i, item in enumerate(data.get('data', [])):
    attr = item['attributes']
    print(f"Index {i}: {attr.get('fungible_info', {}).get('symbol')} | Pool Addr: {attr.get('pool_address')} | Value: {attr.get('value')}")
