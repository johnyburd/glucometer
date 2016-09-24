from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.actionbar import ActionBar
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from time import localtime, strftime

import FlappyBird
from subprocess import call
from blood_glucose_manager import BloodGlucoseManager

class MainScreen(Screen):
    pass

class BGScreen(Screen):
    def start_pb(self):
        event = Clock.schedule_interval(self.update_pb, 1 / 60.)
    def update_pb(self, dt):
        self.ids.pb.value = self.ids.pb.value + (1/3.)
        if self.ids.pb.value >= 100:
            self.ids.pb.value = 0
            return False

class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)
        
        bgm = BloodGlucoseManager()
        rows = bgm.get_whole_table("Cars")
        for row in rows:
            info = "%s %s %s" % (row["Id"], row["Name"], row["Price"])

            self.ids.layout.add_widget(Label(text=str(row["Id"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Label(text=str(row["Name"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Label(text=str(row["Price"]),text_size=(None, None), size_hint_y=None))
class SettingsScreen(Screen):
    def set_brightness(self, brightness):
        try:
            call(['gpio', '-g', '18', int(brightness)])
        except:
            print 'probably not running on a raspberry pi.  can\'t set brightness to ' + str(int(brightness))
class ExtrasScreen(Screen):
    pass
class HomeScreen(Screen):
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
        FlappyBird.FlappyBirdApp().run()

    def set_previous(self, screen_id):
       # sm = self.root.ids.sm
        if self.root and screen_id != 'home':
            self.root.ids.previousid.with_previous = True
            #print self.root.ids.previousid.with_previous
        elif self.root:
            self.root.ids.previousid.with_previous = False
    def set_time(self, dt):
        #title = self.root.ids.previousid.title
        Clock.schedule_once(self.set_time, 30)

        title = strftime("%Y-%m-%d %H:%M", localtime())
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


Glucometer().run()
