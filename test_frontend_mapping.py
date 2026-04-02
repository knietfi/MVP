import json

with open('zerion_complex.json', 'r') as f:
    data = json.load(f)

items = data.get('data', [])
print(f"Loaded {len(items)} items")

positions = []
for item in items:
    attr = item.get('attributes', {})
    
    # 1. Simulate dust filter
    value_usd = attr.get('value')
    if value_usd is None:
        value_usd = 0
        
    # Wait, the frontend says: if (valueUsd <= 0) continue;
    if value_usd <= 0:
        continue
        
    # 2. Simulate protocol mapping
    protocol_name = "Unknown"
    app_meta = attr.get('application_metadata')
    if app_meta and app_meta.get('name'):
        protocol_name = app_meta['name']
    elif attr.get('protocol'):
        protocol_name = attr['protocol']
    elif attr.get('position_type') == 'wallet':
        protocol_name = 'Wallet'
        
    name = attr.get('name', '')
    item_id = item.get('id', '')
    
    if (name and 'aerodrome' in name.lower()) or (item_id and 'aerodrome' in item_id.lower()):
        protocol_name = 'Aerodrome Slipstream'
        
    positions.push_or_append = True
    positions.append({
        'id': item_id,
        'protocol': protocol_name,
        'valueUsd': value_usd
    })

print(f"Positions surviving dust filter: {len(positions)}")
for p in positions:
    print(p)
