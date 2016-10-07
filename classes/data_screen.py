from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from .data_manager import DataManager
from kivy.properties import BooleanProperty
from kivy.lang import Builder

Builder.load_file('kvfiles/data_screen.kv')
class DateRow(BoxLayout):
    def __init__(self, date, **kwargs):
        super(DateRow, self).__init__(**kwargs)
        dm = DataManager()
        dateobj = dm.str_to_date(date)
        self.ids.date.text = "%s %s, %s" % (dateobj.strftime('%B')[:3], dateobj.day, dateobj.year)

class EntryRow(BoxLayout):

    widths_correct = BooleanProperty(False)
    def __init__(self, time, bg, carbs, bolus, notes, **kwargs):
        super(EntryRow, self).__init__(**kwargs)

        i = self.ids
        i.time.text = time
        i.bg.text = str(bg)
        i.carbs.text = str(carbs)
        i.bolus.text = str(bolus)
        i.notes.text = notes
    def refresh_widths(self):
        i = self.ids
        i.bg._label.refresh()      # have to refresh to update texture size
        i.carbs._label.refresh()
        i.bolus._label.refresh()
        i.notes._label.refresh()
        self.ids.layout.width = sum(x.width for x in self.ids.layout.children)
        totalwidth = i.layout.width + i.time.width
        if totalwidth < (240 + i.deletebtn.width + i.editbtn.width):
            i.spacer.width = 240 - totalwidth + i.deletebtn.width + i.editbtn.width
            self.refresh_widths()

class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)

        self.dm = DataManager()
        self.entryrows = []
        self.render_data()

    def render_data(self):
        layout = self.ids.layout

        rows = self.dm.get_whole_table("data")

        lastdate = ""
        rows.reverse()
        for row in rows:
            if row["Date"] != lastdate:
                lastdate = row["Date"]
                layout.add_widget(DateRow(row["Date"]))
            entry = EntryRow(row["Time"], row['Bg'], row['Carbs'], row['bolus'], row['Notes'])
            layout.add_widget(entry)
            self.entryrows.append(entry)
    def update_row_widths(self):
        for entry in self.entryrows:
            entry.refresh_widths()
    def delete_row(self, row):
        self.dm.delete_entry(row)
    '''
            deletecallback = lambda x:self.delete_row(row["Id"])
            self.ids.layout.add_widget(Button(text="x", on_release=deletecallback, size_hint_x=(0.4)))
        '''
