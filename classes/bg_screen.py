from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from .data_manager import DataManager
from .blood_glucose_tester import BloodGlucoseTester
from kivy.lang import Builder

Builder.load_file('kvfiles/bg_screen.kv')

class BGScreen(Screen):
    def __init__(self, **kwargs):
        super(BGScreen, self).__init__(**kwargs)
        self.bgt = BloodGlucoseTester(self)
    def open_popup(self):
        popup = BGPopup(self.bgt)
        popup.open()

class BGPopup(Popup):
    def __init__(self, bgtester, **kwargs):
        super(BGPopup, self).__init__(**kwargs)
        self.bgt = bgtester

    def start_pb(self):
        event = Clock.schedule_interval(self.update_pb, 1 / 60.)
    def update_pb(self, dt):
        self.ids.pb.value = self.ids.pb.value + (1/3.)
        if self.ids.pb.value >= 100:
            self.display_BG('106')
            self.ids.pb.value = 0
            return False
    def display_BG(self, value):
        popup = Popup(title='BG',
        content=Label(text=value,font_size=25),
        size_hint=(None, None), size=(125, 125))
        popup.bind(on_dismiss=self.dismiss_both)
        popup.open()
    def dismiss_both(self,instance):
        self.dismiss()
        return False
