const fs = require('fs');
let userData = JSON.parse(fs.readFileSync('././privateConsts.json', 'utf-8'));
const exp = require('express');
const server = exp();
const binance = require('./binance/binanceControl');

// setup binance
binance.setUpAPI(userData.binance[0].apiKey, userData.binance[0].secret);

const apiLink = '/io';

server.listen(9823, ()=>console.log("server running"))
server.use(exp.static('UI'))
server.use(exp.json({limit: '1mb'}));



// binance.updateAsk_Bid('XRPUSDT');
// binance.update_dept('XRPUSDT');


server.post(apiLink, (request, response)=>{
    console.log('got request'+request.body)
});

server.get(apiLink+'/gbp', (req, resp)=>{
    bPrices = binance.getPrices();
    if (bPrices!=null){
        resp.json(bPrices);
        // console.log(bPrices.XRPUSDT);
    }
});

server.get(apiLink+'/gbA_B', (req, resp)=>{
    var data = binance.getaskbidMap();
    if (data!=null){
        resp.json(data);
        // console.log(bPrices.XRPUSDT);
    }
});

server.get(apiLink+'/Dept', (req, resp)=>{
    var data = binance.getdeptMap();
    if (data!=null){
        resp.json(data);
        // console.log(bPrices.XRPUSDT);
    }
});


function updateBinanceAskBidPerPair(){
    var pairs = userData.binance[0].pairs;
    for (var pairNum in pairs){
        // console.log(pair);
        binance.updateAsk_Bid(pairs[pairNum]);
    }
    // console.log(binance.getaskbidMap());
}

function updateBinanceDeptPerPair(){
    var pairs = userData.binance[0].pairs;
    for (var pairNum in pairs){
        // console.log(pair);
        binance.update_dept(pairs[pairNum]);
    }
    // console.log(binance.getdeptMap());
}

// update binance
const bUpdate = setInterval(binance.updateBPrices, 1000);
const bAskBidUpdate = setInterval(updateBinanceAskBidPerPair, 1000);
const bDeptUpdate = setInterval(updateBinanceDeptPerPair, 1000);