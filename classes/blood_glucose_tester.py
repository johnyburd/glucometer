# This class handles interaction with the ADC and calculates actual readings
import time
import scipy
import threading
try:
    import Adafruit_ADS1x15
except:
    print "Error: Adafruit module not loaded"

STRIP_INSERT_THRESHOLD = 5000
SAMPLE_INSERT_THRESHOLD = 20000
READING_DELAY = 5
GAIN = 4

class ADCPollerThread (threading.Thread):
    def __init__(self, bgtester):
        threading.Thread.__init__(self)
        self.bgt = bgtester
    def run(self):
        print("Starting ADC Poller...")
        self.bgt.adc_poller(self)
        print("Stopping ADC Poller...")

class BloodGlucoseTester():
    def __init__(self, bgscreen):
        self.bgs = bgscreen
        try:
            self.adc = Adafruit_ADS1x15.ADS1115()
        except:
            pass
        try:
            poller_thread = ADCPollerThread(self)
            poller_thread.daemon = True
            poller_thread.start()
        except:
            print 'could not start thread'

    def open_popup(self):
        self.bgs.open_popup()
    def calculate_bg(value):
        pass
        #mgpdl = self.slope
    def adc_poller(self, thread):
    #  - 0 = Channel 0 minus channel 1
    #  - 1 = Channel 0 minus channel 3
    #  - 2 = Channel 1 minus channel 3
    #  - 3 = Channel 2 minus channel 3
        strip_inserted = False
        while True:
            value = self.adc.read_adc_difference(3, gain=GAIN)
            if value > STRIP_INSERT_THRESHOLD and not strip_inserted:
                strip_inserted = True
                time.sleep(1) # make sure we don't take a reading of inserting the strip
                self.open_popup()
            if value > SAMPLE_INSERT_THRESHOLD and strip_inserted:
                time.sleep(READING_DELAY)
                self.calculate_bg(value)
                thread.join()



