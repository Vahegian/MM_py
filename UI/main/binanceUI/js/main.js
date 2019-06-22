$.get("binanceUI/binancePairInfo.html", function (data) {
    $("#temp-pairInfo").replaceWith(data);
});

$.get("binanceUI/binanceOpenOrder.html", function (data) {
    $("#temp-openOrder").replaceWith(data);
});

$.get("binanceUI/binanceWallet.html", function (data) {
    $("#temp-wallet").replaceWith(data);
});

$.get("binanceUI/binanceAutoTrade.html", function (data) {
    $("#temp-autoTrade").replaceWith(data);
});

window.onunload = function(){
    stopBinance();
}

function updateTables() {
    populatePairTable();
    updateWalletTable();
    updateOrdersTable();
}

const pairInfoUpdate = setInterval(updateTables, 2000);