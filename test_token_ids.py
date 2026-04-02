import json

with open("zerion_complex.json", "r") as f:
    data = json.load(f)

for item in data.get("data", []):
    attr = item["attributes"]
    name = attr.get("name")
    
    # get token_id
    token_id = attr.get("nft_info", {})
    if token_id:
        token_id = token_id.get("token_id", "none")
    else:
        token_id = "none"
        
    group_id = attr.get("group_id")
    fungible = attr.get("fungible_info", {})
    symbol = fungible.get("symbol") if fungible else "none"
    
    print(f"{name}: token_id={token_id} group_id={group_id} symbol={symbol} quantity={attr.get('quantity', {}).get('float')}")
