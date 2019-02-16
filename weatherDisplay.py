# import necessary libraries
import lcddriver
import time
import pyowm

# initialize the display
lcd = lcddriver
lcd.init()

# welcome message
lcd.printString("Weather Display", 1)
lcd.printString(" -Stefan Krstikj", 2)
time.sleep(2)
lcd.clear()
lcd.centered = 1
lcd.printString("Getting data", 1)

# import necessary API keys from OWM
owm = pyowm.OWM("9995828c00a169603b3ea26fe5b9e048") # API Key here
location = "Skopje" # Location for the Observation
observation = owm.weather_at_place(location)


class WeatherDisplay:
    location = "None"
    temperature = 0
    humidity = 0
    wind = 0
    rain = 0
    snow = 0
    status = "None"
    
    def __init__(self, location):
        self.location = location
    
    def setInfo(self, temperature, humidity, wind, rain, snow, status):
        