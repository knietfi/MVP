import { createPublicClient, createWalletClient, http, encodeFunctionData, parseAbi, parseEther } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { baseSepolia } from 'viem/chains';

const account = privateKeyToAccount('0x2db62c054fc6605f38e5ed5ab5ff5b930fffa6dc02ef3cc2010c53d1da6c7f50');
console.log("Derived Address:", account.address);

const publicClient = createPublicClient({
  chain: baseSepolia,
  transport: http('https://base-sepolia.infura.io/v3/af810698c71c46dc865ec27dd1bfa6f9')
});

const walletClient = createWalletClient({
  account,
  chain: baseSepolia,
  transport: http('https://base-sepolia.infura.io/v3/af810698c71c46dc865ec27dd1bfa6f9')
});

async function main() {
  const balance = await publicClient.getBalance({ address: account.address });
  console.log("Agent ETH Balance:", balance.toString());

  if (balance === 0n) {
    console.log("Warning: Agent account has 0 ETH! Interaction will fail.");
    return;
  }
  
  const abi = parseAbi([
    'struct Intent { address targetVault; bytes4 functionSelector; uint256 minExpectedAPY; uint256 deadline; bytes callData; }',
    'function registerIntent(uint256 agentId, Intent calldata intent)'
  ]);

  const intent = {
    targetVault: '0x060725b1da8464eb52e3edbd935553ccd4d6c464', // MockYieldVault
    functionSelector: '0x12345678',
    minExpectedAPY: 1500n, // 1500 bps spike
    deadline: BigInt(Math.floor(Date.now() / 1000) + 3600),
    callData: '0x'
  };

  try {
    console.log("Broadcasting registerIntent to Base Sepolia...");
    const hash = await walletClient.writeContract({
        address: '0xeEa52b6e3bda8a93eDdE8D97B272025CC5e20Fba',
        abi,
        functionName: 'registerIntent',
        args: [1n, intent]
    });
    
    console.log("✅ Transaction Sent!");
    console.log("Transaction Hash:", hash);
    console.log(`Explore at: https://sepolia.basescan.org/tx/${hash}`);

  } catch (err) {
    console.error("Broadcast Failed:", err.shortMessage || err.message);
  }
}

main();
