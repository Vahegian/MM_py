async function createOptoins(selectID) {
    var selectObj = document.getElementById(selectID);
    let pairs = await fetch('/io/gbPairs');
    let pairsArray = await pairs.json();
    // console.log(pairsArray);
    for (var pairnum in pairsArray) {
        var x = document.createElement("option");
        // x.setAttribute("value", "volvocar");
        var t = document.createTextNode(pairsArray[pairnum]);
        x.appendChild(t);
        selectObj.appendChild(x);
    }
}


$("#binanceAddPair").click(async function () {
    var pairInfo = [$("#bPairsSelect").val(),
    $("#addAmount").val(),
    $("#addPrice").val(),
    $("#addFee").val()];

    var options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(pairInfo)
    };
    var data = await (await fetch('/io/addbPairInfo', options)).json();
    alert(data);
    // console.log(pairInfo);
});



let data = null;
var pairInfo = [];
var showAll = false;

function setID(item, id) {
    item.setAttribute("id", id);
}

function makeRowItem(data) {
    var rowItem = document.createElement("td");
    rowItem.setAttribute("scope", "col");
    var text = document.createTextNode(data);
    rowItem.appendChild(text);
    return rowItem;
}

function updateTotals(data) {
    var total = parseFloat(data[1]);
    if (data[0] == "totalInvested") {
        var invested = document.getElementById("tInvested");
        invested.innerHTML = '$ ' + (total).toFixed(4);
        invested.style.color = "red";
        if (total > 0) invested.style.color = "green";
    } else {
        var totalprofittext = document.getElementById("tProfit")
        totalprofittext.innerHTML = '$ ' + (total).toFixed(4);
        totalprofittext.style.color = "red";
        if (total > 0) totalprofittext.style.color = "green";
    }
}

function makeTableHead(all) {
    var col = document.getElementById("bPairsTableHead");
    col.innerHTML = '';

    var pa = document.createElement("th");
    pa.innerHTML = "Pair";
    var am = document.createElement("th");
    am.innerHTML = "Amount";
    var pr = document.createElement("th");
    pr.innerHTML = "Price";
    var fee = document.createElement("th");
    fee.innerHTML = "Fee";
    var pf = document.createElement("th");
    pf.innerHTML = "Profit";
    var sa = document.createElement("th");
    sa.innerHTML = '';

    if (all) {
        col.appendChild(pa);
        col.appendChild(am);
        col.appendChild(pr);
        col.appendChild(fee);
        col.appendChild(pf);
        col.appendChild(sa);
    } else {
        col.appendChild(pa);
        col.appendChild(pf);
        col.appendChild(sa);
    }
}

function makePairInfoRow(id, pairInfo, profit, all = false) {
    makeTableHead(all);
    var row = document.createElement("tr");
    // setID(row, id);
    row.appendChild(makeRowItem(pairInfo[0]));
    if (all) {
        row.appendChild(makeRowItem(pairInfo[1]));
        row.appendChild(makeRowItem('$ ' + pairInfo[2]));
        row.appendChild(makeRowItem('% ' + pairInfo[3]));

    }

    profit = parseFloat(profit).toFixed(4);
    var item = makeRowItem('$ ' + profit);
    if (profit > 0.0) {
        item.style.color = "green";
    } else {
        item.style.color = "red";
    }
    row.appendChild(item);
    var button = makeButton("Remove");
    button.setAttribute("class", "binanceButton attention");
    // button.style.
    var flexCenterDiv = document.createElement("div");
    flexCenterDiv.setAttribute("class", "d-flex justify-content-end");
    flexCenterDiv.appendChild(button);
    row.appendChild(flexCenterDiv);
    button.addEventListener("click", async function () {
        // console.log(id);
        var rmoptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify([id])
        };
        var data = await (await fetch('/io/rmbPairInfo', rmoptions)).json();
        alert(data);
    });
    // console.log(row.childNodes.length);
    return row;
}

async function populatePairTable() {
    var data = await getUserInfo();
    // console.log(data);
    var tableObj = document.getElementById("bPairsTable");
    tableObj.innerHTML = '';
    for (var id in data) {
        if (data[id][0] != "totalInvested" && data[id][0] != "totalProfit") {
            var row = makePairInfoRow(data[id][0], data[id][1][0], data[id][1][1], showAll);
            tableObj.appendChild(row);
        } else {
            updateTotals(data[id]);
        }
    }
}

async function getUserInfo() {
    try {
        // let response = ;
        let data = await (await fetch('/io/gbUserPairInfo')).json();
        // console.log(data);
        return data;
    } catch (Exception) {
        console.log(Exception);
        // clearInterval(btime);
    }
}

// const btime = setInterval(getBPrices, 1000);

// populatePairTable();

var showAllBut = document.getElementById("showAllInfobut");
$("#showAllInfobut").click(function () {
    showAll = !showAll;
    if(!showAll){
        showAllBut.innerHTML = "More Info";
    }else{
        showAllBut.innerHTML = "Hide"
    }

});

async function stopBinance() {
    await fetch("/xbinance");
    clearInterval(pairInfoUpdate);
}

