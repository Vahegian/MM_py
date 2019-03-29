import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import constants.uiConsts as uiConst

class PriceBox(Gtk.Box):
    def __init__(self):
        # self.new(Gtk.Orientation.HORIZONTAL, 3)
        # self.set_spacing(3)
        super(PriceBox, self).__init__(Gtk.Orientation.HORIZONTAL, 3)
        
        self.pairlb = Gtk.Label()
        self.pricelb = Gtk.Label()
        self.img = Gtk.Image()

        self.pack_end(self.pricelb, True, True, 5)
        self.pack_end(self.pairlb, True, True, 0)
        self.pack_end(self.img, True, True, 0)

        self.pair = ""
        self.price = ""
        
    def updateImg(self, imgPath):
        self.img.set_from_file(imgPath)

    def updatePair(self, pair):
        self.pairlb.set_text(pair)
        self.pair = pair

    def updatePrice(self, price):
        self.pricelb.set_text(price)
        self.price = price

    def green(self):
        self.updateImg(uiConst.arrowUp)
        self.pairlb.set_markup("<span color='green'>{} </span>".format(self.pair))
        self.pricelb.set_markup("<span color='green'>{} </span>".format(self.price))

    def red(self):
        self.updateImg(uiConst.arrowDown)
        self.pairlb.set_markup("<span color='red'>{} </span>".format(self.pair))
        self.pricelb.set_markup("<span color='red'>{} </span>".format(self.price))


if __name__ == "__main__":
    pass