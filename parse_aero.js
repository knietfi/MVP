import fs from 'fs';

const data = JSON.parse(fs.readFileSync('proxy_test2.json', 'utf8'));
const positions = data['0xdf53b8dfc22aeCb06a8Dbf9A7482525b5AbaFe5b'].data;

const aero = positions.filter(p => JSON.stringify(p).toLowerCase().includes('aerodrome'));

console.log(JSON.stringify(aero, null, 2));
