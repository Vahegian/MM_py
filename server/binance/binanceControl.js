const binanceAPI = require('./binanceAPI');

/*
        Binance functons
*/
var askbidMap = new Map();
var bPrices = null;
var pairDeptMap = new Map();
var pairInfoLastID = null;

async function requirebPrice(tickers) {
    bPrices = tickers;
    // console.log(bPrices.XRPUSDT)
}

async function requireAsk_Bid_OfPair(ticker) {
    await askbidMap.set(ticker.symbol, ticker);
    // console.log(askbidMap);
}

async function setPairDept(symbol, dept) {
    await pairDeptMap.set(symbol, dept);
    // console.log(pairDeptMap);
}

async function updateAsk_Bid(pair) {
    await binanceAPI.getBinanceAsk_Bid(pair, requireAsk_Bid_OfPair);
}

async function update_dept(pair) {
    await binanceAPI.getBinanceDept(pair, setPairDept);
}

function updateBinanceAskBidPerPair(userData) {
    var pairs = userData.binance.default.pairs;
    for (var pairNum in pairs) {
        // console.log(pair);
        updateAsk_Bid(pairs[pairNum]);
    }
    // console.log(binance.getaskbidMap());
}

function updateBinanceDeptPerPair(userData) {
    var pairs = userData.binance.default.pairs;
    for (var pairNum in pairs) {
        // console.log(pair);
        update_dept(pairs[pairNum]);
    }
    // console.log(binance.getdeptMap());
}

async function updateBPrices() {
    await binanceAPI.getBinancePrices(requirebPrice);
}

module.exports = {
    setUpAPI: function (key, secret) {
        binanceAPI.setUp(key, secret);
    },

    getPrices: function () {
        updateBPrices();
        return bPrices;
    },

    getaskbidMap: async function (userData) {
        updateBinanceAskBidPerPair(userData);
        return askbidMap;
    },

    getdeptMap: function (userData) {
        updateBinanceDeptPerPair(userData);
        return pairDeptMap;
    },

    getUserPairInfo: async function (userData) {
        await updateBPrices();
        var pairInfoMap = new Map();
        var bPairs = userData.binance.default.boughtPairs;
        var totalInvested = 0.0;
        var totalProfit = 0.0;
        try {
            for (var id in bPairs) {
                pairInfoLastID = id;
                // for(var list in bPairs[id]){

                // }

                // console.log(bPrices);
                var pairCurPrice = parseFloat(bPrices[bPairs[id][0]]);
                var pairAmount = parseFloat(bPairs[id][1]);
                var pairBPrice = parseFloat(bPairs[id][2]);
                var pairFee = parseFloat(bPairs[id][3]);

                // converting all pairs to USDT
                if(bPairs[id][0].substr(-4) != "USDT"){
                    pairCurPrice = pairCurPrice * parseFloat(bPrices[bPairs[id][0].substr(-3) + "USDT"]);
                }
                var totalBought = (pairBPrice * pairAmount);
                var total = (pairCurPrice * pairAmount) - totalBought;
                var feeAmount = (pairFee / 100) * total;
                var totalAfterFee = total - feeAmount;

                totalInvested += totalBought;
                totalProfit += totalAfterFee;

                pairInfoMap.set(Array.from(bPairs[id]), totalAfterFee);
                // console.log(1+" - "+pairCurPrice);
                // console.log(2+" - "+pairAmount);
                // console.log(3+" - "+pairBPrice);
                // console.log(4+" - "+pairFee);
                // console.log(5+" - "+totalBought);
                // console.log(6+" - "+total);
                // console.log(7+" - "+feeAmount);

                // console.log(id+" : "+totalAfterFee+"\n");

            }
            pairInfoMap.set("totalInvested", totalInvested);
            pairInfoMap.set("totalProfit", totalProfit);
            // console.log(pairInfoMap);
            return pairInfoMap;
        } catch (Exception) {
            console.log(Exception);
            return null;
        }
    },

    getLastPairInfoID: function(){
        return pairInfoLastID;
    },

    addToPairInfo: function(pairInfo, userData){
        try{
            var pair = pairInfo[0];
            var amount = parseFloat(pairInfo[1]);
            var price = parseFloat(pairInfo[2]);
            var fee = parseFloat(pairInfo[3]);
            var id = parseFloat(pairInfoLastID)+1;

            userData.binance.default.boughtPairs[id] = [pair, amount, price, fee];
            return userData;
        }catch(Exception){
            // response.json("Failed: Incorrect data");
            console.log("failed : "+ Exception);
        }
    }


}