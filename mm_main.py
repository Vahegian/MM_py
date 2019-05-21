
# import os
# print("The Dir >>>>>>>: ",  os.curdir)

#from uiControl.window_manager import WindowGer
from subprocess import call
from binanceAPI.binanceCom import BinanceCom
from IO.fileIO import FileIO
# from communicator.organiser import Organiser
import time
import threading


def startServer():
    sr = call("python3 ./MMDJGO/manage.py runserver", shell=True)

if __name__ == "__main__":
    stThread = threading.Thread(target=startServer)
    stThread.deamon = True
    stThread.start()
  
    fio = FileIO()
    bc = BinanceCom()
    #wg = WindowGer()
    #oser = Organiser(fio, bc, wg)
    #wg.startGTK()
    
    time.sleep(2)
    browser = call("./MMDJGO/openChromeApp.sh", shell=True)


