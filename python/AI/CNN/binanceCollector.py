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
    
    def getData(self, client, pair):
        coinInfo = self.getCoinInfo(client, pair)
        lastPrice = coinInfo['lastPrice']
        prevClosePrice = coinInfo['prevClosePrice']
        highP = coinInfo['highPrice']
        lowP = coinInfo['lowPrice']
        bidQty = coinInfo['bidQty']
        bidP = coinInfo['bidPrice']
        askQty = coinInfo['askQty']
        askP = coinInfo['askPrice']
        return lastPrice, prevClosePrice, highP, lowP, bidQty, bidP, askQty, askP

    def getMinuteData(self, client, pair, file=None):
        header = 'minute,'+'lastPrice,'+'prevClosePrice,'+'highPrice,'\
                'lowPrice,'+'bidQty,'+'bidPrice,'+'askQty,'+'askPrice\n'
        firstRun = True
        fileExists = os.path.isfile(file)
        minute = 1
        print(pair, "started")
        while True:
            lastPrice,prevClosePrice,highP,lowP,bidQty,bidP,askQty,askP = self.getData(client, pair)
            
            minData = str(minute)+','+lastPrice+','+prevClosePrice+','+highP+','+lowP+','+bidQty\
            +','+bidP+','+askQty+','+askP+"\n"
            #print(minute, pair, minData)
            if file != None:
                with open(file, 'a') as csvfile:
                    if not fileExists and firstRun:
                        csvfile.write(header)
                        firstRun = False
                    csvfile.write(minData)
            else:
                break
            
            time.sleep(60)
            if minute == 60:
                minute=1
            else:
                minute+=1

if __name__ == "__main__":

    bc = BinanceCom()
    client = bc.connectToAccount("api_key","api_secret")

    pairs = bc.getDefaultPairs()

    fileLoc = "private/cryptoMinute/"        

    for pair in pairs:
        nThread = threading.Thread(target=bc.getMinuteData, args=(client, pair,fileLoc+pair+".csv"))
        nThread.start()

    
