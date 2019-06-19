// const fs = require('fs');
// let data = JSON.parse(fs.readFileSync('././privateConsts.json', 'utf-8'));
// console.log(jsonData);

var binance = null;

module.exports = {
    setUp: function (apikey, secret) {
        binance = require('node-binance-api')().options({
            APIKEY: apikey,
            APISECRET: secret,
            useServerTime: true // If you get timestamp errors, synchronize to server time at startup
        });
    },

    getBinancePrices: async function (callback) {
        await binance.prices((error, ticker) => {
            // console.log("prices()", ticker);
            return callback(ticker);
        });
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

    getTradeHistory: async function(pair, callback){
        await binance.trades(pair, (error, trades, symbol) => {
            return callback(symbol, trades);
          });
    },

    getAllOpenOrders: async function(callback){
        await binance.openOrders(false, (error, openOrders) => {
            // console.log("openOrders()", openOrders);
            return callback(openOrders);
          });
    },

    getWalletInfo: async function(callback){
        await binance.balance((error, balances) => {
            if ( error ) return console.error(error);
            callback(balances);
            // console.log("balances()", balances);
            // console.log("ETH balance: ", balances.ETH.available);
          });
    }
};
