from binance.client import Client
# from python.IO.fileIO import FileIO
import time
import threading
import os.path


class BinanceCom:
    def __init__(self):
        pass

    def connectToAccount(self, apiKey, apiSecret):
        return Client(apiKey, apiSecret)

    def getCoinInfo(self, client, pair):
        return client.get_ticker(symbol=pair)

    def getServerTime(self, client):
        return client.get_server_time()
    
    def getDefaultPairs(self):
        return ['BTCUSDT', 'XRPUSDT', 'EOSUSDT', 'ETHUSDT', 'BATUSDT']
    
bc = BinanceCom()
client = bc.connectToAccount("api_key","api_secret")

pairs = bc.getDefaultPairs()

def getMinuteData(pair, file):
    header = 'minute,'+'lastPrice,'+'prevClosePrice,'+'highPrice,'\
            'lowPrice,'+'bidQty,'+'bidPrice,'+'askQty,'+'askPrice\n'
    firstRun = True
    fileExists = os.path.isfile(file)
    minute = 1
    while True:
        coinInfo = bc.getCoinInfo(client, pair)
        lastPrice = coinInfo['lastPrice']
        prevClosePrice = coinInfo['prevClosePrice']
        highP = coinInfo['highPrice']
        lowP = coinInfo['lowPrice']
        bidQty = coinInfo['bidQty']
        bidP = coinInfo['bidPrice']
        askQty = coinInfo['askQty']
        askP = coinInfo['askPrice']
        
        minData = str(minute)+','+lastPrice+','+prevClosePrice+','+highP+','+lowP+','+bidQty\
        +','+bidP+','+askQty+','+askP+"\n"
        print(minute, pair, minData)
        with open(file, 'a') as csvfile:
            if not fileExists and firstRun:
                csvfile.write(header)
                firstRun = False
            csvfile.write(minData)
        time.sleep(60)
        if minute == 60:
             minute=1
        else:
            minute+=1

fileLoc = "private/CryptoData/minuteHist/"        

for pair in pairs:
    nThread = threading.Thread(target=getMinuteData, args=(pair,fileLoc+pair+".csv"))
    nThread.start()

    