const web3 = require('./web3.js');
const fs = require('fs');
const json2csv = require('json2csv').parse;

const acc2 = '0xC202251cabC1393f8Face351057666c43f9a432A' //client

const REPETITIONS = 100;
const ETHER = 1;

let times = [];
let account;

const getAccount = async () => {
  const accounts = await web3.eth.getAccounts();
  account = accounts[0];
  console.log('Working from account ', account);
};

let isFinished = times => {
    return times.filter(a => typeof(a['completionTime']) === 'undefined');
}

let c = getAccount().then( async function() {
  let nonce = await web3.eth.getTransactionCount(account);
  //console.log(nonce);
  sendTransactions(nonce, REPETITIONS, ETHER);
});

function sendTransactions(nonce, repetitions, etherVal) {
  for (let id = 0; id <repetitions; id++) {
    nonce += 1;
    times[id] = {};
    times[id]['id'] = id;
    times[id]['start'] = Date.now();
    web3.eth.sendTransaction({
      from: account,
      to: acc2,
      //nonce: nonce, // increment the nonce for every transaction
      value: web3.utils.toWei(String(1)),
      gas: 3000000
    }).on('confirmation', function(confirmationNumber, receipt){
        if (confirmationNumber==0) {
          times[id]['mindTime']=Date.now()-times[id]['start'];
          console.log(times[id]);
        }
        if (confirmationNumber==12) {
          times[id]['completionTime']=Date.now()-times[id]['start'];
          console.log('ID: '+id);
          console.log(times[id]);
          if (isFinished(times).length == 0) {
            console.log('Process completed');
            try{
              let jsonContent = JSON.stringify(times);
              fs.writeFileSync("mennan.json", jsonContent, 'utf8');
              console.log("JSON file has been saved.");
            } catch (err){
              console.error(err);
            }
            try {
              const csv = json2csv(times, ['id','start', 'deploymentTime', 'mindTime', 'completionTime']);
              fs.writeFileSync('results_'+String(REPETITIONS)+'.csv', csv, 'utf8');
              console.log("CSV file has been saved.");
              process.exit(0)
            } catch (err) {
              console.error(err);
            }
          }
      };
    });
    times[id]['deploymentTime'] = Date.now()-times[id]['start'];
  }
}
