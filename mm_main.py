
# import os
# print("The Dir >>>>>>>: ",  os.curdir)

from uiControl.window_manager import WindowGer
from binanceAPI.binanceCom import BinanceCom
from IO.fileIO import FileIO
import constants.fileconsts as fconst
import constants.binanceConst as bConst

if __name__ == "__main__":
    fio = FileIO()
    bc = BinanceCom()
    wg = WindowGer()
    
    dPairs = bc.getDefaultPairs()
    client = bc.connectToAccount(bConst.defaulKey, bConst.defaultSecret)
    info = bc.getCoinInfo(client, 'BTCUSDT')
    for pair in dPairs:
        fio.writeRowToCSV(fconst.pairsFile, "," , [pair])
    print(bc.getServerTime(client), info)

    
    file = wg.openUIFile("/home/lavaguiny/projects/Python/MM/UI/mm.glade")    
    window = wg.getObject(file, "main_window")
    wg.showWindow(window)
    print("\nbinancen\n")
    


