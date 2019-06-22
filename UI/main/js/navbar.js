var binanceBut = document.getElementById("navButtBinance");
var allBut = document.getElementById("navButtAll");
var coinbaseBut = document.getElementById("navButtCoinbase");
var bitmexBut = document.getElementById("navButtBitmex");

var origBColor = binanceBut.style.backgroundColor;
var origColor = binanceBut.style.color;

function mkButDefaultColor() {
    binanceBut.style.backgroundColor = origBColor;
    binanceBut.style.color = origColor;
    allBut.style.backgroundColor = origBColor;
    allBut.style.color = origColor;
    coinbaseBut.style.backgroundColor = origBColor;
    coinbaseBut.style.color = origColor;
    bitmexBut.style.backgroundColor = origBColor;
    bitmexBut.style.color = origColor;
}

allBut.addEventListener("click", function () {
    // alert("All");
    clearBody();
    mkButDefaultColor();
    allBut.style.backgroundColor = "white";
    allBut.style.color = "black";
});

binanceBut.addEventListener("click", function () {
    // alert("Binance");
    clearBody();
    showBinance();
    mkButDefaultColor();
    binanceBut.style.backgroundColor = "white";
    binanceBut.style.color = "black";
});

coinbaseBut.addEventListener("click", function () {
    clearBody();
    mkButDefaultColor();
    coinbaseBut.style.backgroundColor = "white";
    coinbaseBut.style.color = "black";
});

bitmexBut.addEventListener("click", function () {
    clearBody();
    mkButDefaultColor();
    bitmexBut.style.backgroundColor = "white";
    bitmexBut.style.color = "black";
});

document.getElementById("navGetApp").addEventListener("click", async function () {
    window.open('/io/androidApp', '_self');
});