# import necessary libraries
import lcddriver
import time
import pyowm

# initialize the display
lcd = lcddriver
lcd.init()

line1 = lcd.line1
line2 = lcd.line2


lcd.printString("Stefana", 1)
time.sleep(2)
lcd.centered = 1
lcd.clear()
time.sleep(2)
lcd.printString("Stefana", 1)
time.sleep(1)