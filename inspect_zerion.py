import json

with open('zerion_complex.json', 'r') as f:
    data = json.load(f)

for i, item in enumerate(data.get('data', [])):
    attrs = item.get('attributes', {})
    print(f"Index: {i}")
    print(f"ID: {item.get('id')}")
    print(f"Symbol: {attrs.get('fungible_info', {}).get('symbol')}")
    print(f"Value: {attrs.get('value')}")
    print(f"Quantity: {attrs.get('quantity', {}).get('float')}")
    print(f"Position Type: {attrs.get('position_type')}")
    print(f"Protocol: {attrs.get('protocol')}")
    print("-" * 20)
