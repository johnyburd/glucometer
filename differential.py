# Simple demo of reading the difference between channel 1 and 0 on an ADS1x15 ADC.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15


adc = Adafruit_ADS1x15.ADS1115()

#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
GAIN = 4
count = 0
print('#Press Ctrl-C to quit...')
print('#channel 0 minus channel 1')



while True:
#for i in xrange(1000):
    # Read the difference between channel 0 and 1 (i.e. channel 0 minus channel 1).
    # Note you can change the differential value to the following:
    #  - 0 = Channel 0 minus channel 1
    #  - 1 = Channel 0 minus channel 3
    #  - 2 = Channel 1 minus channel 3
    #  - 3 = Channel 2 minus channel 3
    value = adc.read_adc_difference(0, gain=GAIN)
    othervalue = adc.read_adc_difference(3, gain=GAIN)
    # Note you can also pass an optional data_rate parameter above, see
    # simpletest.py and the read_adc function for more information.
    print(str(count) + ' {0}'.format( othervalue))

    count = count + 0.1
    # Pause for half a second.
    time.sleep(0.1)
