
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from .data_manager import DataManager
from kivy.lang import Builder
from kivy.properties import ListProperty
import datetime

Builder.load_file('kvfiles/HomeScreen.kv')


class HomeScreen(Screen):
    def __init__(self, **kwargs):

        super(HomeScreen, self).__init__(**kwargs)

        #self.dropdowns = ListProperty([])
        negday = datetime.timedelta(days=-1)
        today = datetime.date.today()

        self.begindropdown = DropDown()
        self.enddropdown = DropDown()
        #self.dropdowns.append(begindropdown)
        for index in range(200):
            displaydate = (today + (negday * index))
            year = displaydate.year
            month = displaydate.month
            day = displaydate.day

            begindatebtn = Button(text='%s/%s/%s' % (month,day,year), size_hint_y=None, height=34)
            enddatebtn = Button(text='%s/%s/%s' % (month,day,year), size_hint_y=None, height=34)

            begindatebtn.bind(on_release=lambda begindatebtn: self.begindropdown.select(begindatebtn.text))
            enddatebtn.bind(on_release=lambda enddatebtn: self.enddropdown.select(enddatebtn.text))

            self.begindropdown.add_widget(begindatebtn)
            self.enddropdown.add_widget(enddatebtn)
        endbtn = Button(text='%s/%s/%s' % (today.month, today.day, today.year))
        beginbtn = Button(text='%s/%s/%s' % ((today + negday*7).month, (today + negday*7).day, (today + negday*7).year))

        beginbtn.bind(on_release=self.begindropdown.open)
        #beginbtn.bind(on_release=self.printtest)
        endbtn.bind(on_release=self.enddropdown.open)

        self.begindropdown.bind(on_select=lambda instance, x: setattr(beginbtn, 'text', x))
        self.enddropdown.bind(on_select=lambda instance, x: setattr(endbtn, 'text', x))
        self.ids.dateselectid.add_widget(beginbtn)
        self.ids.dateselectid.add_widget(Label(text='-', font_size=15,size_hint_x= 0.2))
        self.ids.dateselectid.add_widget(endbtn)

    def printtest(self,instance):
        print 'test'
