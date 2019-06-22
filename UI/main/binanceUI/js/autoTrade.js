var autoTradeBut = document.getElementById("bAutoTradeBut");
var trade = false;

$("#bAutoTradeBut").click(async () => {
    updateWalletTable();
    console.log("tradeButtPressed");
    if (!trade) {
        autoTradeBut.innerHTML = "Stop Trading";
        autoTradeBut.setAttribute("class", "btn btn-danger btn-lg btn-block");
        trade = true;
    } else {

        autoTradeBut.innerHTML = "Auto Trade";
        autoTradeBut.setAttribute("class", "btn btn-success btn-lg btn-block");
        trade = false;
    }
});