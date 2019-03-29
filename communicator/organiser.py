import constants.fileconsts as fconst
import constants.binanceConst as bConst
import constants.uiConsts as uiConst
import time
import threading
from uiControl.topBox import TopBox

class Organiser:
    def __init__(self, fio, bc, wg):
        self.stopThreads = False
        self.fio = fio
        self.bc = bc
        self.wg = wg
        self.def_client = bc.connectToAccount(bConst.defaulKey, bConst.defaultSecret)

        pairDict = self.makePairPriceDictFromFile(fconst.pairsFile, self.def_client)

        self.curPriceDict = {}

        wg.showWindow(self.setupTheUI(pairDict))



    def setupTheUI(self, pairDict):
        file = self.wg.openUIFile(fconst.uiFile)
        window = self.wg.getObject(file, uiConst.mainWindow)

        self.wg.setupSpinner(file, uiConst.spinner)
        self.wg.setupProgressBar(file, uiConst.pBar)

        tb = TopBox(self)
        tb.setupTopBox(file, pairDict)
        cutPriceThread = threading.Thread(target=tb.updateCurPrice)
        cutPriceThread.daemon = True
        cutPriceThread.start()



        return window

    # def updateCurPrice(self):
    #     while not self.stopThreads:
    #         pBarStep = 1/len(self.curPriceDict)
    #         i = 0
    #         self.wg.setpBarProgress(pBarStep)
    #         self.wg.spinnerStart()
    #         for pair in self.curPriceDict.keys():
    #             i=i+1
    #             pBox = self.curPriceDict[pair]
    #             price = float(self.bc.getCoinInfo(self.def_client, pair)['lastPrice'])
    #             if pBox.pair[-3:] == 'BTC':
    #                 price = float(price)*float(self.curPriceDict["BTCUSDT"].price[1:])
    #
    #             if price<float(pBox.price[1:]):
    #                 pBox.updateImg(uiConst.arrowDown)
    #             else:
    #                 pBox.updateImg(uiConst.arrowUp)
    #
    #             pBox.updatePrice("${:.4f}".format(float(price)))
    #
    #             # self.wg.pBarPlus()
    #             self.wg.setpBarProgress(pBarStep * i)
    #         self.wg.spinnerStop()
    #         self.wg.setpBarProgress(0.0)
    #         # self.wg.pBarPlus()
    #         time.sleep(0.5)

    def makePairPriceDictFromFile(self, filePath, client):
        pairList = []
        dPairs = self.fio.readCSV(self.fio.openToRead(filePath), ",")
        for row in dPairs:
            for pair in row:
                pairList.append(pair)
        return self.getPairPriceDict(pairList)

    def makeDefaultPairDict(self, client):
        dPairs = self.bc.getDefaultPairs()
        return self.getPairPriceDict(dPairs)

    def getPairPriceDict(self, listOfPairs = None, pairDict = None):
        if pairDict != None:
            for pair in pairDict.keys():
                pairDict.update({pair: self.bc.getCoinInfo(self.def_client, pair)['lastPrice']})
            return pairDict

        if listOfPairs != None:
            pairDict = {}
            for pair in listOfPairs:
                pairDict.update({pair: self.bc.getCoinInfo(self.def_client, pair)['lastPrice']})
            return pairDict


        
    
