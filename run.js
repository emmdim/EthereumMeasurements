//const sendTransactions = require('./main').sendTransactions;
//const waitForSecond = require('./main').waitForSecond;
const { execSync } = require('child_process');

const REPETITIONS = [1,10,100];
const ETHER = 1;
const SECONDS = [0,1,2,3,4];

for (rep in REPETITIONS) {
  for (sec in SECONDS) {
    cmd = 'node main.js '+REPETITIONS[rep]+' '+SECONDS[sec]+' '+ETHER
    try {
      console.log(cmd);
      execSync(cmd,{stdio:[0,1,2]});
    } catch (err){
      console.error(err);
    }
  }
}
