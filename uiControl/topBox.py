import constants.uiConsts as uiConst
import time
class TopBox:
    def __init__(self, organiser):
        self.og = organiser
        self.pairDict = None
        self.curPriceDict = {}
        self.stopThreads = False


    def setupTopBox(self, file, pairDict):
        self.pairDict = pairDict
        topCurPriceBox = self.og.wg.getObject(file, uiConst.curPriceBox)
        box = self.og.wg.mkGbox(0, len(pairDict))
        self.og.wg.insertStart(topCurPriceBox, box)

        for pair in pairDict.keys():
            pBox = self.og.wg.mkCurPriceBox()
            pBox.updateImg(uiConst.arrowUp)
            pBox.updatePair(pair)
            pBox.updatePrice(pairDict[pair])
            self.curPriceDict.update({pair: pBox})
            self.og.wg.insertStart(box, pBox)

    def updateCurPrice(self):

        while not self.stopThreads:
            self.og.wg.spinnerStart(uiConst.updateing)
            priceDict = self.og.getPairPriceDict(pairDict=self.pairDict)
            # i = 0.0
            for pair in self.curPriceDict.keys():
                pBox = self.curPriceDict[pair]
                price = float(priceDict[pair])
                if pBox.pair[-3:] == 'BTC':
                    price = price*float(priceDict["BTCUSDT"])

                pBox.updatePrice("${:.4f}".format(float(price)))

                if price<float(pBox.price[1:]):
                    # pBox.updateImg(uiConst.arrowDown)
                    pBox.green()
                else:
                    # pBox.updateImg(uiConst.arrowUp)
                    pBox.red()

                # i = i + (1.0 / len(priceDict))
                # self.og.wg.setpBarProgress(i, uiConst.updateing)


                # self.wg.pBarPlus()
            # self.og.wg.pBarPlus()
            # self.og.wg.setpBarProgress(0.0, uiConst.none)
            self.og.wg.spinnerStop()
            time.sleep(0.5)