import requests
import json

url = 'http://localhost:8000/optimize'
payload = {'wallet_address': '0x2Ba20848F5125Dd14B2620d978F83A993176A43f'}

try:
    print(f"Calling optimization for {payload['wallet_address']}...")
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    res = r.json()
    
    positions = res.get("positions", [])
    print(f"Found {len(positions)} positions in Agent response.")
    
    for p in positions:
        print(f"--- Position ---")
        print(f"Protocol: {p.get('protocol')}")
        print(f"Tokens: {p.get('tokens')}")
        print(f"APY: {p.get('apy_pct')}%")
        print(f"ID: {p.get('token_id')}")
        print(f"Range: {p.get('range_status')}")
        print(f"----------------")
        
    opps = res.get("opportunities", [])
    print(f"Found {len(opps)} upgrade opportunities.")
    if opps:
        for o in opps:
            print(f"Best Opp: {o['candidate_project']} at {o['candidate_apy_pct']}%")

except Exception as e:
    print(f"Verification failed: {e}")
