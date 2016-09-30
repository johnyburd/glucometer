
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from .data_manager import DataManager
from kivy.lang import Builder
from kivy.properties import ListProperty

from math import sin
from kivy.garden.graph import Graph, MeshLinePlot
import datetime

from classes.data_manager import DataManager

Builder.load_file('kvfiles/home_screen.kv')


class HomeScreen(Screen):
    def __init__(self, **kwargs):

        super(HomeScreen, self).__init__(**kwargs)

        self.dm = DataManager()

        negday = datetime.timedelta(days=-1)
        today = datetime.date.today()

        self.begindropdown = DropDown()
        self.enddropdown = DropDown()
        for index in range(200):
            displaydate = (today + (negday * index))
            year = displaydate.year
            month = displaydate.month
            day = displaydate.day

            begindatebtn = Button(text='%s/%s/%s' % (month,day,year), size_hint_y=None, height=34)
            enddatebtn = Button(text='%s/%s/%s' % (month,day,year), size_hint_y=None, height=34)

            begindatebtn.bind(on_release=lambda begindatebtn: self.begindropdown.select(begindatebtn.text))

            enddatebtn.bind(on_release=lambda enddatebtn: self.enddropdown.select(enddatebtn.text))

            begindatebtn.bind(on_release=self.update_graph)
            enddatebtn.bind(on_release=self.update_graph)

            self.begindropdown.add_widget(begindatebtn)
            self.enddropdown.add_widget(enddatebtn)
        self.endbtn = Button(text='%s/%s/%s' % (today.month, today.day, today.year))
        self.beginbtn = Button(text='%s/%s/%s' % ((today + negday*7).month, (today + negday*7).day, (today + negday*7).year))

        self.beginbtn.bind(on_release=self.begindropdown.open)
        self.endbtn.bind(on_release=self.enddropdown.open)

        self.begindropdown.bind(on_select=lambda instance, x: setattr(self.beginbtn, 'text', x))
        self.enddropdown.bind(on_select=lambda instance, x: setattr(self.endbtn, 'text', x))
        self.ids.dateselectid.add_widget(self.beginbtn)
        self.ids.dateselectid.add_widget(Label(text='-', font_size=15,size_hint_x= 0.2))
        self.ids.dateselectid.add_widget(self.endbtn)


        self.update_graph('fakeinstance')

    def update_graph(self,instance):
        upper_bound = self.dm.str_to_date(self.endbtn.text)
        lower_bound = self.dm.str_to_date(self.beginbtn.text)
        self.ids.graphid.xmin = lower_bound.day
        self.ids.graphid.xmax = upper_bound.day
        plot = MeshLinePlot(color=[.1, .7, 1, 1])
        #plot.points = [(x, 30*sin(x / 10.)+100+(x)) for x in range(0, 101)]
        rows = self.dm.get_whole_table("data")
        for row in rows:
            date = self.dm.str_to_date(row["Date"])
            if date > upper_bound or date < lower_bound:
                rows.remove(row)

        plot.points =[(self.dm.str_to_date(row["Date"]).day, row["Bg"]) for row in rows]
        #plot.points = pointslist


        self.ids.graphid.add_plot(plot)
