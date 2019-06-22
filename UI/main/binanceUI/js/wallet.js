async function populateWalletTable(walletData) {
    var tableObj = document.getElementById("bWalletTable");
    tableObj.innerHTML = '';

    var totalPriceObj = document.getElementById("bWalletTotal");
    totalPriceObj.innerHTML = '^9999^';

    for (var index in walletData) {
        if (walletData[index][0] == "total") {
            totalPriceObj.innerHTML = parseFloat(walletData[index][1]).toFixed(4);
        } else {
            var row = document.createElement('tr');
            var asset = document.createElement('td');
            asset.innerHTML = walletData[index][0];
            var amount = document.createElement('td');
            amount.innerHTML = parseFloat(walletData[index][1][0]).toFixed(4);
            var onOrder = document.createElement('td');
            onOrder.innerHTML = parseFloat(walletData[index][1][1]).toFixed(4);
            var price = document.createElement('td');
            price.innerHTML = parseFloat(walletData[index][1][2]).toFixed(4);

            row.appendChild(asset);
            row.appendChild(amount);
            row.appendChild(onOrder);
            row.appendChild(price);
            tableObj.appendChild(row);
        }

    }
}



async function updateWalletTable() {
    var walletData = await getData('/io/gbWallet');
    populateWalletTable(walletData);
    // console.log(walletData);

}
