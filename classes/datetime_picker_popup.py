
from kivy.lang import Builder
from kivy.uix.popup import Popup

Builder.load_file('kvfiles/datetime_picker_popup.kv')

class DatetimePickerPopup(Popup):
    
    def __init__(self, **kwargs):
        super(DatetimePickerPopup, self).__init__(**kwargs)
    
