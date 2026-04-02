import json

with open('zerion_unsorted.json', 'r') as f:
    data = json.load(f)

for i, item in enumerate(data.get('data', [])):
    attr = item['attributes']
    symbol = attr.get('fungible_info', {}).get('symbol', 'UNK')
    qty = attr.get('quantity', {}).get('float', 0)
    val = attr.get('value', 0)
    print(f"{i}: {symbol} qt={qty} val={val}")
