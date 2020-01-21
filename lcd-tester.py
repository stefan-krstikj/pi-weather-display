# import necessary libraries
from lcd import lcddriver
import time
import pyowm

# initialize the display
lcd = lcddriver.lcd()


lcd.lcd_display_string("test string 1", 1)
time.sleep(2)
lcd.centered = 1
lcd.lcd_clear()
time.sleep(2)
lcd.lcd_display_string("test string 2", 1)
time.sleep(1)