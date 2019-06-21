const fs = require('fs');
const userFile = '././privateConsts.json';
let userData = JSON.parse(fs.readFileSync(userFile, 'utf-8'));
const exp = require('express');
const server = exp();

const binance = require('./binance/binanceServer');

server.listen(9823, () => console.log("server running"))
server.use(exp.static('UI'))
server.use(exp.json({ limit: '1mb' }));
binance.startBinanceServer(server, userData, userFile, fs);

server.get('/binance', async (req, resp) => {
    await binance.openWebSockets();
    resp.json("started")
});

server.get('/xbinance', async (req, resp) => {
    await binance.closeWebSockets();
    resp.json("stopped")
});
