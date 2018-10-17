# EthereumMeasurements

1. Download code and install nodejs and npm.
2. Run ``npm install``
3. Edit ``run.js`` changing the parameters ``PARALLELTRANS``, ``SECONDS`` and ``ETHER`` (corresponding to # of parllel transactions, second decimal digit whne to start the measurement, amount of ether to send) at the top of the file.
4. Connect to the blockchain network (for example guifi.net vpn)
4. Run ``npm run`` or ``node run.js``
5. The results are stored in the same folder with naming convention ``results_$REPETITIONS_$SECONDS.csv``

