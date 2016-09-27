
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from .data_manager import DataManager
from kivy.lang import Builder
import datetime

Builder.load_file('kvfiles/HomeScreen.kv')

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

        begindropdown.bind(on_select=lambda instance, x: setattr(beginbtn, 'text', x))
        enddropdown.bind(on_select=lambda instance, x: setattr(endbtn, 'text', x))
        self.ids.dateselectid.add_widget(beginbtn)
        self.ids.dateselectid.add_widget(Label(text='-', font_size=15,size_hint_x= 0.2))
        self.ids.dateselectid.add_widget(endbtn)
