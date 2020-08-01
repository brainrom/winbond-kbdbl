""" Class to control the lights """
from platform import system
from colour import Color
import kbdbl.usbadapter as usbadapter
from kbdbl import keyboard
import random, copy


if system() == 'Windows':
    import kbdbl.usbwindows as usbwindows
else:
    import kbdbl.usblinux as usblinux

class Keylights:
    """
    Primary (maybe only) class of the fdclct project.
    This tries to find an attached Drevo Calibur keyboard and
    opens a connection to the device.

    Throws ValueError if something is wrong, description in message.

    see: Keylights.setall() and Keylights.setkey() for practical uses
    """
    adapter: usbadapter.Usbadapter = None

    def __init__(self):
        if system() == 'Windows':
            self.adapter = usbwindows.Usbwindows()
        else:
            self.adapter = usblinux.Usblinux()

    def gencolorprofile(self, color):
        colorlist = copy.deepcopy(keyboard) #Easiest way to get keys list

        if not isinstance(color, Color):
            color = Color(color)
        colorstr = color.hex_l[1:]
        for i in colorlist:
            colorlist[i]=colorstr
        return(colorlist)


    def setall(self, color):
        """
        Sets the color of all keys.

        The color parameter is a colour.Color object
        or alternatively a string interpretable by the colour.Color constructor
        """
        self.adapter.sendhex(self.gencolorprofile(color))

    def setallrandom(self):
        color = Color(hsl=(random.uniform(0.0, 1.0), 1, 0.5))
        self.adapter.sendhex(self.gencolorprofile(color))

    def setrandom(self):
        """
        Sets random colors for each key.
        """
        colorlist = copy.deepcopy(keyboard)

        for i in colorlist:
            color = Color(hsl=(random.uniform(0.0, 1.0), 1, 0.5))
            colorlist[i]=color.hex_l[1:]
        self.adapter.sendhex(colorlist)

    def setbrightness(self, brightness):
        if brightness>7:
            brightness=7
        self.adapter.sendbrightness(abs(brightness))

    def setkey(self, keycode, color):
        """
        Sets the color of a single key.
        """

        if not isinstance(color, Color):
            color = Color(color)
        colorstr = color.hex_l[1:]

        colorlist={}
        colorlist[keycode]=colorstr #Thats all! Just add key to colorlist and it'll be correctly sent to the keyboard
        self.adapter.sendhex(colorlist)

    def setprofile(self, json):
        self.adapter.sendhex(json)