var autoTradeBut = document.getElementById("bAutoTradeBut");
var trade = false;
var tradeUpdate = null;

async function updateTraderTable(data, prices){
    // console.log(prices)
    var tableObj = document.getElementById("bTraderTable");
    tableObj.innerHTML = '';
    for (var index in data) {
        var row = document.createElement('tr');
        var pair = document.createElement('td');
        pair.innerHTML = data[index].pair;
        // if (text == "SELL") { order.style.color = "red"; }
        // else { order.style.color = "green" }
        var pred = document.createElement('td');
        text = parseFloat(data[index]["pred"]);
        if (text==0){text="DOWN"; pred.style.color="red";}
        else if (text==1){text="STABLE"; pred.style.color="black";}
        else if (text==2){text="UP";pred.style.color="green";}
        pred.innerHTML = text;
        var acc = document.createElement('td');
        acc.innerHTML = (parseFloat(data[index]["acc"])*100).toFixed(4)+"%";
        var price = document.createElement('td');
        price.innerHTML = "$"+parseFloat(data[index]["lastPrice"]).toFixed(4);

        var curPrice = document.createElement('td');
        for (var i in prices){
            if (data[index].pair=="bitcoin" && prices[i][0]=="BTCUSDT"){
                curPrice.innerHTML="$"+parseFloat(prices[i][1]).toFixed(4);
            }
            else if (data[index].pair=="ethereum" && prices[i][0]=="ETHUSDT"){
                curPrice.innerHTML="$"+parseFloat(prices[i][1]).toFixed(4);
            }else if (data[index].pair=="ripple" && prices[i][0]=="XRPUSDT"){
                curPrice.innerHTML="$"+parseFloat(prices[i][1]).toFixed(4);
            }else if (data[index].pair=="eos" && prices[i][0]=="EOSUSDT"){
                curPrice.innerHTML="$"+parseFloat(prices[i][1]).toFixed(4);
            }
            
        }

        row.appendChild(pair);
        row.appendChild(pred);
        row.appendChild(acc);
        row.appendChild(price);
        row.appendChild(curPrice);
        tableObj.appendChild(row);
    }
}

async function get_ai_predictions(){
    var ai_data = await getData('/io/gbAIPred');
    // for (var i in ai_data){
    //     console.log(ai_data[i]);
    // }
    var prices = await getData('/io/gbp');
    updateTraderTable(ai_data, prices);
}

$("#bAutoTradeBut").click(async () => {
    updateWalletTable();
    console.log("tradeButtPressed");
    if (!trade) {
        var data = await getData('/io/gbTrade');
        console.log(data);
        autoTradeBut.innerHTML = "Stop Trading";
        autoTradeBut.setAttribute("class", "btn btn-danger btn-lg btn-block");
        trade = true;
        tradeUpdate = setInterval(get_ai_predictions, 3000);
    } else {
        await fetch('/io/gbxTrade');
        autoTradeBut.innerHTML = "Auto Trade";
        autoTradeBut.setAttribute("class", "btn btn-success btn-lg btn-block");
        trade = false;
        clearInterval(tradeUpdate);
    }
});


