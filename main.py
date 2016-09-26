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

import FlappyBird
from subprocess import call
from data_manager import DataManager
from blood_glucose_tester import BloodGlucoseTester

class NewEntryPopup(Popup):
    pass
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

class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)

        bgm = DataManager()
        rows = bgm.get_whole_table("Data")

        self.ids.layout.add_widget(Label(text="Date",text_size=(None, None), size_hint_y=None))
        self.ids.layout.add_widget(Label(text="Bg",text_size=(None, None), size_hint_y=None))
        self.ids.layout.add_widget(Label(text="Carbs",text_size=(None, None), size_hint_y=None))
        self.ids.layout.add_widget(Label(text="Bolus",text_size=(None, None), size_hint_y=None))
        for row in rows:

            self.ids.layout.add_widget(Label(text=str(row["Date"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Label(text=str(row["Bg"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Label(text=str(row["Carbs"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Label(text=str(row["Bolus"]),text_size=(None, None), size_hint_y=None))
class SettingsScreen(Screen):
    def set_brightness(self, brightness):
        try:
            call(['gpio', '-g', 'mode', '18', 'pwm'])
            call(['gpio', '-g', 'pwm', '18', str(int(brightness))])
        except:
            print 'probably not running on a raspberry pi.  can\'t set brightness to ' + str(int(brightness))
class ExtrasScreen(Screen):
    pass
class HomeScreen(Screen):
    def __init__(self, **kwargs):

        super(HomeScreen, self).__init__(**kwargs)
        negday = datetime.timedelta(days=-1)
        today = datetime.date.today()

        begindropdown = DropDown()
        enddropdown = DropDown()
        for index in range(200):
            displaydate = (today + (negday * index))
            year = displaydate.year
            month = displaydate.month
            day = displaydate.day

            begindatebtn = Button(text='%s/%s/%s' % (month,day,year), size_hint_y=None, height=34)
            enddatebtn = Button(text='%s/%s/%s' % (month,day,year), size_hint_y=None, height=34)

            begindatebtn.bind(on_release=lambda begindatebtn: begindropdown.select(begindatebtn.text))
            enddatebtn.bind(on_release=lambda enddatebtn: enddropdown.select(enddatebtn.text))

            begindropdown.add_widget(begindatebtn)
            enddropdown.add_widget(enddatebtn)
        endbtn = Button(text='%s/%s/%s' % (today.month, today.day, today.year))
        beginbtn = Button(text='%s/%s/%s' % ((today + negday*7).month, (today + negday*7).day, (today + negday*7).year))

        beginbtn.bind(on_release=begindropdown.open)
        endbtn.bind(on_release=enddropdown.open)

        #otherbutton = Button(text='Date')
        #otherbutton.bind(on_release=dropdown.open)

        begindropdown.bind(on_select=lambda instance, x: setattr(beginbtn, 'text', x))
        enddropdown.bind(on_select=lambda instance, x: setattr(endbtn, 'text', x))
        #dropdown.bind(on_select=lambda instance, x: setattr(otherbutton, 'text', x))
        self.ids.dateselectid.add_widget(beginbtn)
        self.ids.dateselectid.add_widget(endbtn)

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
        Clock.schedule_once(self.set_time, 30)

        #title = strftime("%Y-%m-%d %H:%M", localtime())
        today = datetime.datetime.now()
        hour = today.hour
        if today.hour > 12:
            hour = today.hour - 12
        title = "%s %s %s:%s" % (today.day, today.strftime('%B')[:3], hour, today.minute)
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
