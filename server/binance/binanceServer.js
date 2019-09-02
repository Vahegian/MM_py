const binance = require('./binanceControl');
const apiLink = '/io';
var userAccount = "Vahegian";


function openServer(server, userData, userFile, fs ){
    binance.setUpAPI(userData.binance[userAccount].apiKey, userData.binance[userAccount].secret);

    server.post(apiLink+'/addbPairInfo', (request, response) => {
        var pairInfo = request.body;
        var newUserData = binance.addToPairInfo(pairInfo, userData, userAccount);
        try{
            fs.writeFileSync(userFile, JSON.stringify(newUserData),'utf-8');
            response.json("Successfully Added");
        }catch(Exception){
            response.json("Failed: Incorrect data");
        }
        // console.log('got request : ' + );
    });
    
    server.post(apiLink+'/rmbPairInfo', async (request, response) => {
        var id = request.body;
        try{
            await delete userData.binance[userAccount].boughtPairs[id];
            await fs.writeFileSync(userFile, JSON.stringify(userData),'utf-8');
            response.json("Removed");
        //    console.log(id); 
        }catch(Exception){
            response.json("Failed: not removed");
            console.log("failed : "+ Exception);
        }
        // console.log('got request : ' + );
    });
    
    server.get(apiLink + '/gbp', async (req, resp) => {
        await binance.getPrices(userData.binance[userAccount].pairs, resp);
        // if (bPrices != null) {
        //     resp.json(bPrices);
        //     // console.log(bPrices.XRPUSDT);
        // }
    
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
        // binance.closeWebSockets();
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

    server.post(apiLink+'/prediction', async (request, response) => {
        var pairInfo = await request.body;
        // console.log(pairInfo);
        binance.updateCNNPreds(pairInfo);
        response.json("Prediction received")
    });

    server.get(apiLink + '/gbTrade', async (req, resp) => {
        // var data = await binance.getWallet();
        await binance.get_cnn_preds();
        // binance.response_and_trade(resp)
        console.log("Trading"); 
        resp.json("Trading");
    });

    server.get(apiLink + '/gbxTrade', async (req, resp) => {
        // var data = await binance.getWallet();
        console.log("Stopped Trading");
        resp.json("Stopped");
    });

    server.get(apiLink + '/gbAIPred', async (req, resp) => {
        // var data = await binance.getWallet();
        binance.getPreds(resp);
        // console.log("Stopped Trading");
        // resp.json("Stopped");
    });
    
    console.log("Binance Server Running");
}

module.exports = {
    startBinanceServer: async function(server, userData, userFile, fs){
        openServer(server, userData, userFile, fs);
        
    },

    openWebSockets: function(){
        binance.openWebSockets();
    },

    closeWebSockets: function(){
        binance.closeWebSockets();
    }
}