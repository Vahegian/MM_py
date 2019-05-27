
# import os
# print("The Dir >>>>>>>: ",  os.curdir)

#from uiControl.window_manager import WindowGer
from subprocess import call
from binanceAPI.binanceCom import BinanceCom
from IO.fileIO import FileIO
# from communicator.organiser import Organiser  
import time
import threading
import sys
import eel

#def startServer():
    #sr = call("python3 ./MMDJGO/manage.py runserver", shell=True)

@eel.expose
def loginUser(login, password):
    print (login," : ",password)

if __name__ == "__main__":
  
    fio = FileIO()
    bc = BinanceCom()

    eel.init('UI')
    eel.start('login/index.html')
