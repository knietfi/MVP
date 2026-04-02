from web3 import Web3
w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))
addr = "0x7412118b069BC1aAfE6C53ab97bF8541330241b8"
abi = [{"inputs":[],"name":"owner","outputs":[{"type":"address"}],"stateMutability":"view","type":"function"}]
owner = w3.eth.contract(address=addr, abi=abi).functions.owner().call()
print(f"OWNER_IS:{owner}")
addr_d3fd = w3.eth.account.from_key("0x37832c1462d5ba92f9bfd1d1d5e8c784f3a50071fd74b40e90081458281f3484").address
print(f"D3FD_IS:{addr_d3fd}")
addr_2ba2 = "0x2Ba20848F5125Dd14B2620d978F83A993176A43f"
print(f"2BA2_IS:{addr_2ba2}")
