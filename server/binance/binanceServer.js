const binance = require('./binanceControl');
const apiLink = '/io';
var userAccount = "Vahegian";


function openServer(server, userData, userFile, fs ){
    binance.setUpAPI(userData.binance[userAccount].apiKey, userData.binance[userAccount].secret);

    server.post(apiLink+'/addbPairInfo', (request, response) => {
        var pairInfo = request.body;
        var newUserData = binance.addToPairInfo(pairInfo, userData);
        try{
            fs.writeFileSync(userFile, JSON.stringify(newUserData),'utf-8');
            response.json("Successfully Added");
        }catch(Exception){
            response.json("Failed: Incorrect data");
        }
        // console.log('got request : ' + );
    });
    
    server.post(apiLink+'/rmbPairInfo', (request, response) => {
        var id = request.body;
        try{
            delete userData.binance[userAccount].boughtPairs[id];
            fs.writeFileSync(userFile, JSON.stringify(userData),'utf-8');
            response.json("Removed");
        //    console.log(id[0]); 
        }catch(Exception){
            response.json("Failed: not removed");
            console.log("failed : "+ Exception);
        }
        // console.log('got request : ' + );
    });
    
    server.get(apiLink + '/gbp', (req, resp) => {
        bPrices = binance.getPrices();
        if (bPrices != null) {
            resp.json(bPrices);
            // console.log(bPrices.XRPUSDT);
        }
    
    });
    
    server.get(apiLink + '/gbA_B', (req, resp) => {
        // binance.updateBinanceAskBidPerPair(userData);
        var data = binance.getaskbidMap(userData, userAccount);
        if (data != null) {
            resp.json(data);
            // console.log(bPrices.XRPUSDT);
        }
    });
    
    server.get(apiLink + '/gbDept', (req, resp) => {
        // binance.updateBinanceDeptPerPair(userData);
        var data = binance.getdeptMap(userData, userAccount);
        if (data != null) {
            resp.json(data);
            // console.log(bPrices.XRPUSDT);
        }
    });
    
    server.get(apiLink + '/gbPairs', (req, resp) => {
        resp.json(userData.binance[userAccount].pairs);
    });
    
    server.get(apiLink + '/gbBPairs', (req, resp) => {
        resp.json(userData.binance[userAccount].boughtPairs);
    });
    
    server.get(apiLink + '/androidApp', (req, resp) => {
        resp.download("./server/Android/apk/mm.apk")
    });
    
    server.get(apiLink + '/gbUserPairInfo', async (req, resp) => {
        // await binance.getPrices();
        var info = await binance.getUserPairInfo(userData, userAccount);
        // console.log(info);
        if (info != null) {
            resp.json(Array.from(info));
        }

        // var th = await binance.getTradeHist("XRPUSDT");
        // console.log(th);
        // console.log();
    });

    server.get(apiLink + '/gbOpenOrd', async (req, resp) => {
        var data = await binance.getOpenOrders();
        // console.log(data); 
        resp.json(data);
    });

    server.get(apiLink + '/gbWallet', async (req, resp) => {
        var data = await binance.getWallet();
        // console.log(data); 
        resp.json(Array.from(data));
    });

}

module.exports = {
    startBinanceServer: async function(server, userData, userFile, fs){
        openServer(server, userData, userFile, fs);
        
    }
}