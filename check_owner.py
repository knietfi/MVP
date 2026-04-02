from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))
session_module_address = "0x7412118b069BC1aAfE6C53ab97bF8541330241b8"
intent_registry_address = "0xeEa52b6e3bda8a93eDdE8D97B272025CC5e20Fba"

abi = [
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]

print("--- Contract Ownership Check ---")
try:
    sm = w3.eth.contract(address=session_module_address, abi=abi)
    sm_owner = sm.functions.owner().call()
    print(f"SessionModule ({session_module_address}) Owner: {sm_owner}")
except Exception as e:
    print(f"Error checking SessionModule owner: {e}")

try:
    ir = w3.eth.contract(address=intent_registry_address, abi=abi)
    ir_owner = ir.functions.owner().call()
    print(f"IntentRegistry ({intent_registry_address}) Owner: {ir_owner}")
except Exception as e:
    print(f"Error checking IntentRegistry owner: {e}")

print("\n--- Key Match Check ---")
pk_3783 = "0x37832c1462d5ba92f9bfd1d1d5e8c784f3a50071fd74b40e90081458281f3484"
addr_3783 = w3.eth.account.from_key(pk_3783).address
print(f"Address for PK 0x3783... (d3fd): {addr_3783}")

agent_address = "0x2Ba20848F5125Dd14B2620d978F83A993176A43f"
print(f"Agent Wallet Address:            {agent_address}")

if sm_owner.lower() == addr_3783.lower():
    print("\n✅ MATCH: Deployer (d3fd) is the owner of SessionModule.")
elif sm_owner.lower() == agent_address.lower():
    print("\n⚠️ ALERT: Agent Wallet (2Ba2) is the owner of SessionModule!")
else:
    print(f"\n❌ UNKNOWN: Owner is {sm_owner}")
