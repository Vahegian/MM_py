
$.get("navbar.html", function (data) {
    $("#nav-placeholder").replaceWith(data);
});

async function showBinance() {
    await fetch("/binance");

    $.get("binanceUI/binance.html", function (data) {
        // var body = document.getElementById("body-placeholder");
        $("#body-placeholder").append(data);
    });
}

function clearBody() {
    try {
        stopBinance();
        var div = document.getElementById("body-placeholder");
        div.innerHTML = '';
        // while (div.firstChild) {
        //     div.removeChild(div.firstChild);
        // }
    } catch (Exception) { }
}

function makeButton(text) {
    var button = document.createElement("button");
    button.setAttribute("type", "button");
    button.setAttribute("class", "btn btn-secondary waves-effect waves-light");
    button.appendChild(document.createTextNode(text));
    return button;

}

async function getData(link) {
    try {
        // let response = ;
        let listOfOrders = await (await fetch(link)).json();
        return listOfOrders;
    } catch (Exception) {
        console.log(Exception);
        // clearInterval(btime);
    }
}
