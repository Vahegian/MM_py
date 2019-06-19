const binanceAPI = require('./binanceAPI');

/*
        Binance functons
*/
var askbidMap = new Map();
var bPrices = [];
var pairDeptMap = new Map();
var pairInfoLastID = null;
var pairTradeMap = new Map();
var openOrders = null;
var wallet = new Map();

async function requirebPrice(tickers) {
    bPrices = await tickers;
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

async function setTradeHist(symbol, history) {
    await pairTradeMap.set(symbol, history);
}

async function updateAsk_Bid(pair) {
    await binanceAPI.getBinanceAsk_Bid(pair, requireAsk_Bid_OfPair);
}

async function update_dept(pair) {
    await binanceAPI.getBinanceDept(pair, setPairDept);
}

function updateBinanceAskBidPerPair(userData, user) {
    var pairs = userData.binance[user].pairs;
    for (var pairNum in pairs) {
        // console.log(pair);
        updateAsk_Bid(pairs[pairNum]);
    }
    // console.log(binance.getaskbidMap());
}

function updateBinanceDeptPerPair(userData, user) {
    var pairs = userData.binance[user].pairs;
    for (var pairNum in pairs) {
        // console.log(pair);
        update_dept(pairs[pairNum]);
    }
    // console.log(binance.getdeptMap());
}

async function updateBPrices() {
    await binanceAPI.getBinancePrices(requirebPrice);
}

async function updateTradeHist(pair) {
    await binanceAPI.getTradeHistory(pair, setTradeHist);
}

async function updateOpenOrders(orders) {
    openOrders = orders;
}

async function updateWallet(balance) {
    var tpairs = ["ETH", "BTC"];
    for (var id in balance) {
        var amount = parseFloat(balance[id]["available"]);
        if (amount > 0.0000) {
            for (var index in tpairs) {
                try {
                    wallet.set(id, [amount, parseFloat(bPrices[id + 'USDT']) * amount]);


                } catch (Exception1) {
                    try {
                        // console.log(id+tpairs[index]+" : "+bPrices[id+tpairs[index]]);
                        var altPair = parseFloat(bPrices[id+tpairs[index]]);
                        var alyPairPrice= altPair*amount;
                    
                        wallet.set(id, [amount, parseFloat(bPrices[tpairs[index]+'USDT'])*alyPairPrice]);
                        break;
                    } catch (Exception2) {
                        // console.log(Exception2);
                    }
                }
            }
        }
    }
    // wallet=balance;
}
module.exports = {
    setUpAPI: function (key, secret) {
        binanceAPI.setUp(key, secret);
    },

    getPrices: function () {
        updateBPrices();
        return bPrices;
    },

    getaskbidMap: async function (userData, user) {
        updateBinanceAskBidPerPair(userData, user);
        return askbidMap;
    },

    getdeptMap: function (userData, user) {
        updateBinanceDeptPerPair(userData, user);
        return pairDeptMap;
    },

    getUserPairInfo: async function (userData, user) {
        await updateBPrices();
        var pairInfoMap = new Map();
        var bPairs = userData.binance[user].boughtPairs;
        var totalInvested = 0.0;
        var totalProfit = 0.0;
        try {
            for (var id in bPairs) {
                pairInfoLastID = id;
                var pairCurPrice = parseFloat(bPrices[bPairs[id][0]]);
                var pairAmount = parseFloat(bPairs[id][1]);
                var pairBPrice = parseFloat(bPairs[id][2]);
                var pairFee = parseFloat(bPairs[id][3]);

                // converting all pairs to USDT
                if (bPairs[id][0].substr(-4) != "USDT") {
                    pairCurPrice = pairCurPrice * parseFloat(bPrices[bPairs[id][0].substr(-3) + "USDT"]);
                }
                var totalBought = (pairBPrice * pairAmount);
                var total = (pairCurPrice * pairAmount) - totalBought;
                var feeAmount = (pairFee / 100) * total;
                var totalAfterFee = total - feeAmount;

                totalInvested += totalBought;
                totalProfit += totalAfterFee;

                pairInfoMap.set(Array.from(bPairs[id]), totalAfterFee);

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

    getLastPairInfoID: function () {
        return pairInfoLastID;
    },

    addToPairInfo: function (pairInfo, userData) {
        try {
            var pair = pairInfo[0];
            var amount = parseFloat(pairInfo[1]);
            var price = parseFloat(pairInfo[2]);
            var fee = parseFloat(pairInfo[3]);
            var id = parseFloat(pairInfoLastID) + 1;

            userData.binance.default.boughtPairs[id] = [pair, amount, price, fee];
            return userData;
        } catch (Exception) {
            // response.json("Failed: Incorrect data");
            console.log("failed : " + Exception);
        }
    },

    getTradeHist: async function (pair) {
        await updateTradeHist(pair);
        return pairTradeMap;
    },

    getOpenOrders: async function () {
        await binanceAPI.getAllOpenOrders(updateOpenOrders);
        return await openOrders;
        // await updateOpenOrders();
    },

    getWallet: async function () {
        await binanceAPI.getWalletInfo(updateWallet);
        return wallet;
    }


}