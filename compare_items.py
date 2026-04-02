import json

with open('zerion_complex.json', 'r') as f:
    data = json.load(f)

items = data.get('data', [])

# Indices 0 and 1 are both USDC but different quantities
u1 = items[0]
u2 = items[1]

print("Comparing Index 0 and Index 1 (USDC):")
for k, v in u1['attributes'].items():
    if k in u2['attributes']:
        v2 = u2['attributes'][k]
        if v != v2:
            print(f"Attr '{k}' differs: {v} vs {v2}")
    else:
        print(f"Attr '{k}' only in Index 0")

print("\nID 0:", u1['id'])
print("ID 1:", u2['id'])
