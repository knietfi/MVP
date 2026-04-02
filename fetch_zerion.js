import fs from 'fs';

async function go() {
  const address = '0xdf53b8dfc22aeCb06a8Dbf9A7482525b5AbaFe5b';
  
  // Just use regular fetch, do not ask for only_complex, allow everything.
  const url1 = `http://localhost:8080/api/zerion-proxy?address=${address}&filter=wallet,staked,deposit,locked,borrowed`;
  
  try {
    const res = await fetch(url1);
    const json = await res.json();
    
    fs.writeFileSync('all_assets.json', JSON.stringify(json, null, 2));
    console.log("Success! Saved to all_assets.json");
  } catch (err) {
    console.error(err);
  }
}
go();
