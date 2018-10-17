//const sendTransactions = require('./main').sendTransactions;
//const waitForSecond = require('./main').waitForSecond;
const { execSync } = require('child_process');

const PARALLELTRANS = [1000];
const ETHER = 1;
const SECONDS = [0,1,2,3,4];

for (rep in PARALLELTRANS) {
  for (sec in SECONDS) {
    cmd = 'node main.js '+PARALLELTRANS[rep]+' '+SECONDS[sec]+' '+ETHER
    try {
      console.log(cmd);
      execSync(cmd,{stdio:[0,1,2]});
    } catch (err){
      console.error(err);
    }
  }
}
