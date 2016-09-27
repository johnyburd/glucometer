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
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from time import localtime, strftime
import datetime

from classes.FlappyBird import FlappyBirdApp
from subprocess import call
from classes.data_manager import DataManager
from classes.blood_glucose_tester import BloodGlucoseTester
from classes.data_screen import DataScreen
from classes.home_screen import HomeScreen

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

class MainScreen(Screen):
    pass
class BGScreen(Screen):
    def __init__(self, **kwargs):
        super(BGScreen, self).__init__(**kwargs)
        self.bgt = BloodGlucoseTester(self) 
    def open_popup(self):
        popup = BGPopup(self.bgt)
        popup.open()

class SettingsScreen(Screen):
    def set_brightness(self, brightness):
        try:
            call(['gpio', '-g', 'mode', '18', 'pwm'])
            call(['gpio', '-g', 'pwm', '18', str(int(brightness))])
        except:
            print 'probably not running on a raspberry pi.  can\'t set brightness to ' + str(int(brightness))
class ExtrasScreen(Screen):
    pass

class CustomScreenManager(ScreenManager):

    screen_ids = ['bgtest', 'data', 'settings', 'extras']
    screen_names = ['BG test', 'Data', 'Settings', 'Extras']

    def __init__(self, **kwargs):

        super(CustomScreenManager,self).__init__(**kwargs)

        self.add_widget(HomeScreen(name='home'))
        self.add_widget(DataScreen(name='data'))
        self.add_widget(MainScreen(name='main'))
        self.add_widget(BGScreen(name='bgtest'))
        self.add_widget(SettingsScreen(name='settings'))
        self.add_widget(ExtrasScreen(name='extras'))

class Glucometer(App):

    test = StringProperty('test')

    screen_names = CustomScreenManager.screen_names
    screen_ids = CustomScreenManager.screen_ids

    def __init_(self, **kwargs):  # constructor is not necessary here
        super(Glucometer, self).__init__(**kwargs)

    def build(self):
        self.root.ids.spnr.text = "Home"

    def print_current_screen(self):
        return sm.current_screen.name
    def test(self):
        return StringProperty('test')
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

        #title = strftime("%Y-%m-%d %H:%M", localtime())
        today = datetime.datetime.now()
        hour = today.hour
        minute = today.minute
        if today.hour > 12:
            hour = today.hour - 12
        if minute < 10:
            minute = '0' + str(minute)
        title = "%s %s %s:%s" % (today.day, today.strftime('%B')[:3], hour, minute)
        return title
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
