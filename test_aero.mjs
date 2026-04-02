import 'dotenv/config';
import fs from 'fs';

async function fetchComplex() {
  const url = 'https://api.zerion.io/v1/wallets/0x2ba20848f5125dd14b2620d978f83a993176a43f/positions/?filter[positions]=only_complex';
  const apiKey = process.env.VITE_ZERION_API_KEY;
  const auth = 'Basic ' + Buffer.from(apiKey + ':').toString('base64');

  let r = await fetch(url, { headers: { Authorization: auth } });
  if (r.status === 429) {
    console.log('429 ratelimit. Retrying...');
    await new Promise(resolve => setTimeout(resolve, 2000));
    r = await fetch(url, { headers: { Authorization: auth } });
  }

  const data = await r.json();
  fs.writeFileSync('zerion_complex.json', JSON.stringify(data, null, 2));
  console.log('Saved complex payload to zerion_complex.json. Count:', data.data ? data.data.length : data);
}

fetchComplex();
