from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))
pk = "0x37832c1462d5ba92f9bfd1d1d5e8c784f3a50071fd74b40e90081458281f3484"
account = w3.eth.account.from_key(pk)
print(f"Executing from: {account.address}")

session_module_address = "0x7412118b069BC1aAfE6C53ab97bF8541330241b8"
agent_id = 2
operator_address = "0x2Ba20848F5125Dd14B2620d978F83A993176A43f"

abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "agentId", "type": "uint256"},
            {"internalType": "address", "name": "operator", "type": "address"}
        ],
        "name": "setAgentOperator",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

contract = w3.eth.contract(address=session_module_address, abi=abi)

print(f"Building transaction for Agent ID {agent_id}, Operator {operator_address}...")
try:
    tx = contract.functions.setAgentOperator(agent_id, operator_address).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
    })
    print("Transaction built successfully. Estimating gas...")
    # Gas estimation check
    gas_est = w3.eth.estimate_gas(tx)
    print(f"Gas Estimate: {gas_est}")
    
    # Actually sign and send? No, let's just see if it builds/estimates.
    print("Simulation (gas estimation) passed! The transaction SHOULD be valid.")
except Exception as e:
    print(f"Execution Failed in Simulation: {e}")
