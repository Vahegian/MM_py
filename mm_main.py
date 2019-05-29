
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
import json

from encdec.aes import Encdec

#def startServer():
    #sr = call("python3 ./MMDJGO/manage.py runserver", shell=True)

@eel.expose
def loginUser(login, password):
    with open('raw/uData.json') as udata:
        file = json.load(udata)
    userList = file['Users']
    ed = Encdec()
    for defUser in userList:
        try:
            ed.setNonce(bytes(defUser['nonce']))
            uName = defUser['uName']
            passw = ed.dec(bytes(defUser['pass'])).decode('utf-8')
            if login == uName and password==passw:
                # print (login," : ",password)
                # eel.lunch_main()
                return True
                # break
            else:
                print("not >>", uName )
        except Exception as e:
            print(e)


def mkDefUser():
    data = '''
    {
        "Users": [
            {
                "Name": "mmUser",
                "uName": "mm",
                "pass": "",
                "nonce": ""
            }
        ]
    }
    '''
    jsonData = json.loads(data)
    # user = jsonData['Users']
    ed = Encdec()
    encPass, nonce = ed.enc(b'mmpass')
    jsonData['Users'][0]['pass'] = list(encPass)
    jsonData['Users'][0]['nonce'] = list(nonce)

    with open('raw/uData.json', 'w') as outfile:
        json.dump(jsonData, outfile, sort_keys = True, indent = 4, ensure_ascii = False)


if __name__ == "__main__":
  
    fio = FileIO()
    bc = BinanceCom()
    # mkDefUser()

    eel.init('UI')
    eel.start('login/index.html')
