import constants.fileconsts as fconst
import constants.binanceConst as bConst
import constants.uiConsts as uiConst
import time
import threading
from uiControl.topBox import TopBox
from uiControl.tradeHelper import TradeHelper


class Organiser:
    def __init__(self, fio, bc, wg):
        self.stopThreads = False
        self.fio = fio
        self.bc = bc
        self.wg = wg

        self.tb = None
        self.th = None

        self.def_client = bc.connectToAccount(bConst.defaulKey, bConst.defaultSecret)

        self.pairDict = self.makePairPriceDictFromFile(fconst.pairsFile, self.def_client)

        self.curPriceDict = {}

        wg.showWindow(self.setupTheUI(self.pairDict))

        # wg.startGTK()



    def setupTheUI(self, pairDict):
        file = self.wg.openUIFile(fconst.uiFile)
        window = self.wg.getObject(file, uiConst.mainWindow)
        window.set_default_size(640, 640)

        self.wg.setupSpinner(file, uiConst.spinner)
        self.wg.setupProgressBar(file, uiConst.pBar)

        self.tb = TopBox(self)
        self.tb.setupTopBox(file, pairDict)

        self.th = TradeHelper(self)
        self.th.setupTradeHelper(file, pairDict)

        # self.updateUI()
        cutPriceThread = threading.Thread(target=self.updateUI)
        cutPriceThread.daemon = True
        cutPriceThread.start()



        return window

    def updateUI(self):
        step = 1.0/5.0
        self.wg.setpBarProgress(step)
        while not self.stopThreads:

            self.wg.spinnerStart(uiConst.updateing)

            pairDict = self.getPairPriceDict(self.pairDict)
            self.wg.pBarPulse()

            self.tb.updateCurPrice(pairDict)
            self.wg.pBarPulse()

            self.th.updateTradeData(pairDict)
            self.wg.pBarPulse()

            self.wg.spinnerStop()

            # self.wg.setpBarProgress(0.0)
            time.sleep(0.3)



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

        
    
