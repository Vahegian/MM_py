const fs = require('fs');
let userData = JSON.parse(fs.readFileSync('././privateConsts.json', 'utf-8'));
const exp = require('express');
const server = exp();
const binance = require('./binance/binanceControl');

// setup binance
binance.setUpAPI(userData.binance.default.apiKey, userData.binance.default.secret);

const apiLink = '/io';

server.listen(9823, () => console.log("server running"))
server.use(exp.static('UI'))
server.use(exp.json({ limit: '1mb' }));

binance.getUserPairInfo(userData);

// binance.updateAsk_Bid('XRPUSDT');
// binance.update_dept('XRPUSDT');


server.post(apiLink, (request, response) => {
    console.log('got request' + request.body)
});

server.get(apiLink + '/gbp', (req, resp) => {
    bPrices = binance.getPrices();
    if (bPrices != null) {
        resp.json(bPrices);
        // console.log(bPrices.XRPUSDT);
    }

});

server.get(apiLink + '/gbA_B', (req, resp) => {
    // binance.updateBinanceAskBidPerPair(userData);
    var data = binance.getaskbidMap(userData);
    if (data != null) {
        resp.json(data);
        // console.log(bPrices.XRPUSDT);
    }
});

server.get(apiLink + '/gbDept', (req, resp) => {
    // binance.updateBinanceDeptPerPair(userData);
    var data = binance.getdeptMap(userData);
    if (data != null) {
        resp.json(data);
        // console.log(bPrices.XRPUSDT);
    }
});

server.get(apiLink + '/gbPairs', (req, resp) => {
    resp.json(userData.binance.default.pairs);
});

server.get(apiLink + '/gbBPairs', (req, resp) => {
    resp.json(userData.binance.default.boughtPairs);
});

server.get(apiLink + '/androidApp', (req, resp) => {
    resp.download("./server/Android/apk/mm.apk")
});

server.get(apiLink + '/gbUserPairInfo', async (req, resp) => {
    var info = await binance.getUserPairInfo(userData);
    // console.log(info);
    if (info != null) {
        resp.json(Array.from(info));
    }
});

// update binance
// const bUpdate = setInterval(binance.updateBPrices, 1000);
