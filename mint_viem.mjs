import { createWalletClient, createPublicClient, http, encodeFunctionData, parseAbi } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { baseSepolia } from 'viem/chains';

const account = privateKeyToAccount('0x2db62c054fc6605f38e5ed5ab5ff5b930fffa6dc02ef3cc2010c53d1da6c7f50');

const client = createWalletClient({
  account,
  chain: baseSepolia,
  transport: http('https://base-sepolia.infura.io/v3/af810698c71c46dc865ec27dd1bfa6f9')
});

const publicClient = createPublicClient({
  chain: baseSepolia,
  transport: http('https://base-sepolia.infura.io/v3/af810698c71c46dc865ec27dd1bfa6f9')
});

async function main() {
  const abi = parseAbi(['function mint(address to) external returns (uint256)']);
  
  try {
    const hash = await client.writeContract({
      address: '0xB2A02c5b8F918C6191F3D1a6Eb2f7ffc0de5c0AB',
      abi,
      functionName: 'mint',
      args: [account.address]
    });
    console.log("Mint Transaction Sent:", hash);
    const receipt = await publicClient.waitForTransactionReceipt({ hash });
    console.log("Mint Success:", receipt.status === 'success');
  } catch (err) {
    console.error("Mint Error:", err);
  }
}

main();
