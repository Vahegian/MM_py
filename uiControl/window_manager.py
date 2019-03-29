import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import threading

class WindowGer:
    def init(self):
        # self.gtkBuilder = None
        pass

    def openUIFile(self, filePath):
        builder = Gtk.Builder()
        builder.add_from_file(filePath)
        return builder

    def getObject(self, uiFile, objID):
        return uiFile.get_object(objID)

    def showWindow(self, window):
        # window = self.gtkBuilder.get_object(windowName)
        window.show_all()
        th = threading.Thread(target=self.startGTK)
        # th.daemon = True
        th.start()

    def startGTK(self):
        Gtk.main()
        
if __name__ == "__main__":
    pass