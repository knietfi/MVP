import { createPublicClient, http, parseAbiItem } from 'viem';
import { baseSepolia } from 'viem/chains';

const client = createPublicClient({
  chain: baseSepolia,
  transport: http('https://base-sepolia.infura.io/v3/af810698c71c46dc865ec27dd1bfa6f9')
});

async function main() {
  const currentBlock = await client.getBlockNumber();
  const logs = await client.getLogs({
    address: '0xeEa52b6e3bda8a93eDdE8D97B272025CC5e20Fba',
    event: parseAbiItem('event IntentRegistered(uint256 indexed agentId, address targetVault)'),
    fromBlock: currentBlock - 1000n,
    toBlock: 'latest'
  });
  
  if (logs.length === 0) {
    console.log("No intents registered in the last 1000 blocks.");
  } else {
    console.log("Found IntentRegistered Events:");
    logs.forEach(l => console.log(`- Agent ${l.args.agentId} -> Vault ${l.args.targetVault} (Block ${l.blockNumber})`));
  }
}

main();
