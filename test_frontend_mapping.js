const fs = require('fs');

async function testParsing() {
  const json = await fetch('http://localhost:8080/api/zerion-proxy?address=0x2ba20848f5125dd14b2620d978f83a993176a43f&filter=all').then(r=>r.json());
  const data = json.data || [];
  console.log(`Initial items from Proxy: ${data.length}`);

  let aeroCount = 0;
  const positions = [];

  for (const item of data) {
    const attr = item.attributes;
    if (!attr) continue;
    
    // simulate portfolioService logic
    let protocolName = attr.application_metadata?.name ?? attr.protocol ?? (attr.position_type === 'wallet' ? 'Wallet' : 'Unknown');

    if (
      (attr.name && attr.name.toLowerCase().includes('aerodrome')) || 
      (item.id && item.id.toLowerCase().includes('aerodrome'))
    ) {
      protocolName = 'Aerodrome Slipstream';
      aeroCount++;
    }

    const valueUsd = attr.value ?? 0;
    
    // Simulate dust filter
    if (valueUsd <= 0) {
      if (protocolName === 'Aerodrome Slipstream') {
        console.log(`Filtered out aero position because valueUsd is ${valueUsd}`);
      }
      continue;
    }

    positions.push({
      id: item.id,
      name: attr.name,
      protocol: protocolName,
      value: valueUsd
    });
  }

  console.log(`Total aero detected: ${aeroCount}`);
  console.log(`Positions surviving filters: ${positions.length}`);
  const aeroSurviving = positions.filter(p => p.protocol.includes('Aero')).length;
  console.log(`Aero positions surviving: ${aeroSurviving}`);
  
  if (aeroSurviving > 0) {
    console.log('Surviving Aerodrome LPs:', positions.filter(p => p.protocol.includes('Aero')));
  }
}

testParsing().catch(console.error);
