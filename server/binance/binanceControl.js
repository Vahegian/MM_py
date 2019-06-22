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
var walletBalance = null;
var hasBalances = false;
var hasOpenOrders = false;

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

async function updateBPrices(pairs) {
    bPrices = await binanceAPI.getBinancePrices(pairs);
    // console.log(bPrices);
}

async function updateTradeHist(pair) {
    await binanceAPI.getTradeHistory(pair, setTradeHist);
}

async function updateOpenOrders(orders) {
    openOrders = await orders;
    hasOpenOrders = true;
}

async function setBalances(balance){
    walletBalance = await balance;
    hasBalances = true;
}

async function updateWallet(balance) {
    var wallet = new Map();
    var tpairs = ["USDT", "ETH", "BTC", "BNB"];
    var totalPrice = 0.0;
    for (var id in balance) {
        var coin = balance[id];
        var amount = parseFloat(coin["available"]);
        var inOrder = parseFloat(coin["onOrder"]);
        if (amount > 0.00000 || inOrder > 0.00000) {
            var price = 0.0;
            var totalAmount = parseFloat(amount + inOrder);
            var pairPrice = 0.0;
            try {
                for (var pairNum in tpairs) {
                    var pair = tpairs[pairNum];
                    try {
                        var coinPair = id + pair;
                        if (id == "USDT") {
                            price = parseFloat(totalAmount);
                            break;
                        }
                        if (pair == "USDT") {
                            pairPrice = bPrices.get(coinPair);
                            if (pairPrice > 0.0) {
                                break;
                            }
                        } else {
                            pairPrice = bPrices.get(coinPair) * bPrices.get(pair + "USDT");
                            if (pairPrice > 0.0) {break;}
                        }
                    } catch (Exp) {}
                }
            } catch (Exception) {
                pairPrice = 0.0;
                console.log(Exception);
            }
            price = parseFloat(totalAmount) * parseFloat(pairPrice);
            //                     // console.log(coinPair, pairPrice, price);
            
            if (isNaN(price)) {
                totalPrice += 0.0;
                wallet.set(id, [amount.toFixed(5), inOrder.toFixed(5), 0.0]);
            } else {
                wallet.set(id, [amount.toFixed(5), inOrder.toFixed(5), price.toFixed(5)]);
                totalPrice += price;
            }
            wallet.set("total", totalPrice);
        }
    }
    return wallet;
    // console.log(wallet);
}
module.exports = {
    setUpAPI: function (key, secret) {
        binanceAPI.setUp(key, secret);
    },

    openWebSockets: function () {
        binanceAPI.openWebConnections();
    },

    closeWebSockets: function () {
        binanceAPI.closeConnections();
    },

    getPrices: async function (pairs) {
        await updateBPrices(pairs);
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
        await updateBPrices(userData.binance[user].pairs);

        var pairInfoMap = new Map();
        var bPairs = userData.binance[user].boughtPairs;
        var totalInvested = 0.0;
        var totalProfit = 0.0;
        try {
            for (var id in bPairs) {
                pairInfoLastID = id;
                var pairCurPrice = parseFloat(bPrices.get(bPairs[id][0]));

                var pairAmount = parseFloat(bPairs[id][1]);
                var pairBPrice = parseFloat(bPairs[id][2]);
                var pairFee = parseFloat(bPairs[id][3]);
                // console.log(pairCurPrice, pairAmount, pairBPrice, pairFee);
                // converting all pairs to USDT
                if (bPairs[id][0].substr(-4) != "USDT") {
                    pairCurPrice = pairCurPrice * parseFloat(bPrices.get(bPairs[id][0].substr(-3) + "USDT"));
                }
                var totalBought = (pairBPrice * pairAmount);
                var total = (pairCurPrice * pairAmount) - totalBought;
                var feeAmount = (pairFee / 100) * total;
                var totalAfterFee = total - feeAmount;

                totalInvested += totalBought;
                totalProfit += totalAfterFee;

                pairInfoMap.set(id, [Array.from(bPairs[id]), totalAfterFee]);

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

    addToPairInfo: function (pairInfo, userData, userAccount) {
        try {
            var pair = pairInfo[0];
            var amount = parseFloat(pairInfo[1]);
            var price = parseFloat(pairInfo[2]);
            var fee = parseFloat(pairInfo[3]);
            var id = parseFloat(pairInfoLastID) + 1;

            userData.binance[userAccount].boughtPairs[id] = [pair, amount, price, fee];
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
        if(!hasOpenOrders){
            await binanceAPI.getAllOpenOrders(updateOpenOrders);
        }
        return await openOrders;
        // await updateOpenOrders();
    },

    getWallet: async function () {
        if(!hasBalances){
            await binanceAPI.getWalletInfo(setBalances);
            console.log("got wallet balances");
        }
        
        return await updateWallet(walletBalance);
    }


}