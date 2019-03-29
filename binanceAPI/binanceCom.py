from binance.client import Client

class BinanceCom:
    def init(self):
        pass

    def connectToAccount(self, apiKey, apiSecret):
        return Client(apiKey, apiSecret)

    def getCoinInfo(self, client, pair):
        return client.get_ticker(symbol=pair)

    def getServerTime(self, client):
        return client.get_server_time()
    
    def getDefaultPairs(self):
        return ['BTCUSDT', 'XRPUSDT', 'AGIBTC', 'XVGBTC']