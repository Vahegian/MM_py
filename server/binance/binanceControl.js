const binanceAPI = require('./binanceAPI');

/*
        Binance functons
*/
var askbidMap = new Map();
var bPrices = null;
var pairDeptMap = new Map();

async function requirebPrice(tickers){
    bPrices = tickers;
    // console.log(bPrices.XRPUSDT)
}

async function requireAsk_Bid_OfPair(ticker){
    await askbidMap.set(ticker.symbol, ticker);
    // console.log(askbidMap);
}

async function setPairDept(symbol, dept){
    await pairDeptMap.set(symbol, dept);
    // console.log(pairDeptMap);
}



module.exports = {
    setUpAPI: function(key, secret){
        binanceAPI.setUp(key, secret);
    },

    updateBPrices: async function (){
         await binanceAPI.getBinancePrices(requirebPrice);
    },

    updateAsk_Bid: async function (pair){
        await binanceAPI.getBinanceAsk_Bid(pair, requireAsk_Bid_OfPair);
    },

    update_dept: async function(pair){
        await binanceAPI.getBinanceDept(pair, setPairDept);
    },
    
    getPrices: function(){
        return bPrices;
    },

    getaskbidMap: async function(){
        return askbidMap;
    },

    getdeptMap: function(){
        return pairDeptMap;
    }
}