
# import os
# print("The Dir >>>>>>>: ",  os.curdir)

from uiControl.window_manager import WindowGer
from binanceAPI.binanceCom import BinanceCom
from IO.fileIO import FileIO
from communicator.organiser import Organiser

if __name__ == "__main__":
    fio = FileIO()
    bc = BinanceCom()
    wg = WindowGer()
    oser = Organiser(fio, bc, wg)
    


