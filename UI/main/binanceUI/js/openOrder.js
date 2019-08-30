async function populateOrderTable(orderList) {
    var tableObj = document.getElementById("bTradeTable");
    tableObj.innerHTML = '';
    for (var index in orderList) {
        var row = document.createElement('tr');
        var order = document.createElement('td');
        var text = orderList[index]["side"];
        order.innerHTML = text;
        if (text == "SELL") { order.style.color = "red"; }
        else { order.style.color = "green" }
        var pair = document.createElement('td');;
        pair.innerHTML = orderList[index]["symbol"];
        var amount = document.createElement('td');
        amount.innerHTML = parseFloat(orderList[index]["origQty"]).toFixed(4);
        var price = document.createElement('td');
        price.innerHTML = "$"+parseFloat(orderList[index]["price"]).toFixed(4);

        row.appendChild(order);
        row.appendChild(pair);
        row.appendChild(amount);
        row.appendChild(price);
        tableObj.appendChild(row);
    }
}

async function updateOrdersTable() {
    var orderList = await getData('/io/gbOpenOrd');
    populateOrderTable(orderList);
    // var walletmap = await getData('/io/gbWallet');
    // console.log(walletmap);
}