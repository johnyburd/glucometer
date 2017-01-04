from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
Builder.load_file('kvfiles/extras_screen.kv')
import usb.core
from kivy.clock import Clock

class ExtrasScreen(Screen):

    def __init__(self, **kwargs):

        Clock.schedule_once(self.update_debug, 1)
        super(ExtrasScreen, self).__init__(**kwargs)

    def update_debug(self, *args):


#        dev = usb.core.find()
        dev = 'dum'
        self.ids.debug.text = str(dev)
