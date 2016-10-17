from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.actionbar import ActionBar
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty

from time import localtime, strftime
import datetime
from subprocess import call

from classes.FlappyBird import FlappyBirdApp
from classes.data_manager import DataManager
from classes.blood_glucose_tester import BloodGlucoseTester
from classes.data_screen import DataScreen
from classes.home_screen import HomeScreen
from classes.bg_screen import BGScreen
from classes.settings_screen import SettingsScreen
#from classes import settings

class NewEntryPopup(Popup):

    def __init__(self, **kwargs):
        super(NewEntryPopup, self).__init__(**kwargs)
        self.dm = DataManager()

    def submit(self):
        date = self.ids.date.text
        bg = self.ids.bg.text
        carbs = self.ids.bg.text
        bolus = self.ids.bolus.text
        self.dm.new_entry(date, bg, carbs, bolus)
        self.dismiss()

class ExtrasScreen(Screen):
    pass

class CustomScreenManager(ScreenManager):

    screen_ids = ['bgtest', 'data', 'settings', 'extras']
    screen_names = ['BG test', 'Data', 'Settings', 'Extras']

    def __init__(self, **kwargs):

        super(CustomScreenManager,self).__init__(**kwargs)

        self.add_widget(HomeScreen(name='home'))
        self.add_widget(DataScreen(name='data'))
        self.add_widget(BGScreen(name='bgtest'))
        self.add_widget(SettingsScreen(name='settings'))
        self.add_widget(ExtrasScreen(name='extras'))

class Glucometer(App):

    test = StringProperty('test')

    screen_names = CustomScreenManager.screen_names
    screen_ids = CustomScreenManager.screen_ids

    def __init_(self, **kwargs):
        super(Glucometer, self).__init__(**kwargs)

    def build(self):
        self.root.ids.spnr.text = "Home"

    def print_current_screen(self):
        return sm.current_screen.name
    def flappy(self):
        FlappyBirdApp().run()

    def set_previous(self, screen_id):
       # sm = self.root.ids.sm
        if self.root and screen_id != 'home':
            self.root.ids.previousid.with_previous = True
            #print self.root.ids.previousid.with_previous
        elif self.root:
            self.root.ids.previousid.with_previous = False
    def set_time(self, dt):
        Clock.schedule_once(self.set_time, 30)

        today = datetime.datetime.now()
        hour = today.hour
        minute = today.minute
        if today.hour > 12:
            hour = today.hour - 12
        if minute < 10:
            minute = '0' + str(minute)
        time = "%s %s %s:%s" % (today.strftime('%B')[:3], today.day, hour, minute)
        if self.root:
            self.root.ids.previousid.title = time
        return time
    def set_screen(self):
        sm = self.root.ids.sm
        #print sm.current_screen.name
        for i in xrange(0,len(self.screen_names)):
            if self.screen_names[i] == self.root.ids.spnr.text:
                sm.transition.direction = 'left'
                sm.current = self.screen_ids[i]
                self.set_previous(self.screen_ids[i])
                break;
    def open_new_entry_popup(self):
        popup = NewEntryPopup()
        popup.open()


Glucometer().run()
