import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import threading
import copy
from uiControl.curPriceBox import PriceBox
import constants.uiConsts as uiConst

class WindowGer:
    def __init__(self):
        # self.gtkBuilder = None
        self.spinner = None
        self.progressBar = None
        self.pBarInfo = None


    def spinnerStart(self, info):
        self.spinner.start()
        self.pBarInfo.set_text(info)

    def spinnerStop(self):
        self.spinner.stop()
        self.pBarInfo.set_text(uiConst.none)

    def setupSpinner(self, uifile, spinnerId):
        self.spinner = self.getObject(uifile, spinnerId)
        self.pBarInfo = self.getObject(uifile, uiConst.pBarInfo)

    def setupProgressBar(self, uifile, barID):
        self.progressBar = self.getObject(uifile, barID)

    def pBarPlus(self):
        self.progressBar.pulse()

    def setpBarProgress(self, size):
        self.progressBar.set_fraction(size)


    # def showProgress(self):
    #     self.spinnerStart()
    #     self.setpBarProgress(0.1)
    #     for i in range (0, 10):
    #         self.pBarPlus()
    #     self.spinnerStop()

    def openUIFile(self, filePath):
        builder = Gtk.Builder()
        builder.add_from_file(filePath)
        return builder

    def getObject(self, uiFile, objID):
        return uiFile.get_object(objID)

    def showWindow(self, window):
        # window = self.gtkBuilder.get_object(windowName)
        window.show_all()
        window.connect("destroy", Gtk.main_quit)
        th = threading.Thread(target=self.startGTK)
        # th.daemon = True
        th.start()

    def startGTK(self):
        Gtk.main()
        
    def insertStart(self, upper, lower):
        upper.pack_start(lower, True, True, 0)

    def insertEnd(self, upper, lower):
        upper.pack_end(lower, True, True, 0)
    
    def mkGbox(self, orientation, spacing):
        box = Gtk.Box()
        box.new(orientation, spacing)
        return box
    
    def mkCurPriceBox(self):
        return PriceBox()

    def mkGImg(self, path):
        img = Gtk.Image()
        img.set_from_file(path)
        return  img

        
if __name__ == "__main__":
    pass