// const fs = require('fs');
// let data = JSON.parse(fs.readFileSync('././privateConsts.json', 'utf-8'));
// console.log(jsonData);

var binance = null;
var webSocket = null;
var isGettingPrices = false;
var isGettingUserData = false;
var latsPrices = new Map();

async function openBinanceWebSocket() {
    if (webSocket == null) {
        webSocket = await binance.websockets;
    }
}

async function closeBinanceWebSocket() {
    if (webSocket != null) {
        let connections = webSocket.subscriptions();
        for (let endpoint in connections) {
            console.log(endpoint);
            await webSocket.terminate(endpoint);
        }

        isGettingPrices = false;
        isGettingUserData = false;
        webSocket = null;
    }
}

async function getLastPrices(pairs) {
    if (webSocket != null) {
        isGettingPrices = true;
        await pairs.forEach(async pair => {
            webSocket.chart(pair, "1m", async (symbol, interval, chart) => {
                try {
                    let tick = await binance.last(chart);
                    const last = await chart[tick].close;
                    await latsPrices.set(symbol, parseFloat(last));
                } catch (Exception) {
                    console.log(Exception);
                }
            });
        });

    }
}

function balance_update(data) {
    console.log("Balance Update");
    for (let obj of data.B) {
        let { a: asset, f: available, l: onOrder } = obj;
        if (available == "0.00000000") continue;
        console.log(asset + "\tavailable: " + available + " (" + onOrder + " on order)");
    }
}
function order_update(data) {
    let { x: executionType, s: symbol, p: price, q: quantity, S: side, o: orderType, i: orderId, X: orderStatus } = data;
    if (executionType == "NEW") {
        if (orderStatus == "REJECTED") {
            console.log("Order Failed! Reason: " + data.r);
        }
        console.log(symbol + " " + side + " " + orderType + " ORDER #" + orderId + " (" + orderStatus + ")");
        console.log("..price: " + price + ", quantity: " + quantity);
        return;
    }
    //NEW, CANCELED, REPLACED, REJECTED, TRADE, EXPIRED
    console.log(symbol + "\t" + side + " " + executionType + " " + orderType + " ORDER #" + orderId);
}

function getUserData() {
    if (webSocket != null) {
        binance.websockets.userData(balance_update, order_update);
    }
}

module.exports = {
    setUp: function (apikey, secret) {
        binance = require('node-binance-api')().options({
            APIKEY: apikey,
            APISECRET: secret,
            useServerTime: true, // If you get timestamp errors, synchronize to server time at startup
            reconnect: false
        });

    },

    openWebConnections: function () {
        openBinanceWebSocket();
    },

    closeConnections: function () {
        closeBinanceWebSocket();
    },

    showLimits: async function () {
        var limits = null;
        await binance.exchangeInfo(function (response) {
            console.log(response);
            limits = response;
        });
        return limits;
    },

    getBinancePrices: async function (pairs) {
        if (!isGettingPrices) {
            getLastPrices(pairs);
        }
        return latsPrices;
    },

    getBinanceAsk_Bid: async function (pair, callback) {
        await binance.bookTickers(pair, (error, ticker) => {
            // console.log("bookTickers", ticker);
            return callback(ticker);
        });
    },

    getBinanceDept: async function (pair, callback) {
        await binance.depth(pair, (error, depth, symbol) => {
            // console.log(symbol+" market depth", depth);
            return callback(symbol, depth);
        });
    },

    limitBuy: async function (pair, amount, price, callback) {
        await binance.buy(pair, amount, price, { type: 'LIMIT' }, callback);
    },

    limitSell: async function (pair, amount, price, callback) {
        await binance.sell(pair, amount, price, { type: 'LIMIT' }, callback);
    },

    marketBuy: async function (pair, amount) {
        await binance.marketBuy(pair, amount);
    },

    marketSell: async function (pair, amount) {
        await binance.marketSell(pair, amount);
    },

    getTradeHistory: async function (pair, callback) {
        await binance.trades(pair, (error, trades, symbol) => {
            return callback(symbol, trades);
        });
    },

    getAllOpenOrders: async function (callback) {
        await binance.openOrders(false, (error, openOrders) => {
            // console.log("openOrders()", openOrders);
            return callback(openOrders);
        });

        // if(!isGettingUserData){
        //     getUserData();
        //     isGettingUserData =true;
        // }

    },

    getWalletInfo: async function (callback) {
        await binance.balance((error, balances) => {
            if (error) return console.error(error);
            callback(balances);
            // console.log("balances()", balances);
            // console.log("ETH balance: ", balances.ETH.available);
        });
        // if(!isGettingUserData){
        //     getUserData();
        //     isGettingUserData =true;
        // }
    }
};
