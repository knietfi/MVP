import os
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))

nft_abi = [
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]
nft = w3.eth.contract(address="0xB2A02c5b8F918C6191F3D1a6Eb2f7ffc0de5c0AB", abi=nft_abi)
print(f"MockNFT ownerOf(1): {nft.functions.ownerOf(1).call()}")
