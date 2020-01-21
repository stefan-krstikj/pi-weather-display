# import necessary libraries
from lcd import lcddriver
import time
import pyowm
import weather_display

# enter information
location = "Skopje"
measurementSystem = 0 # 0 - Metric, 1 - Imperial
update_interval = 15 # update interval in minutes

# import necessary API keys from OWM
owm = pyowm.OWM("9995828c00a169603b3ea26fe5b9e048") # API Key here
observation = owm.weather_at_place(location)
wd = weather_display.WeatherDisplay(location, measurementSystem)

# initialize the display
lcd = lcddriver.lcd()

# welcome message
lcd.lcd_display_string("Weather Display", 1)
lcd.lcd_display_string(" -Stefan Krstikj", 2)
time.sleep(2)
lcd.lcd_clear()
lcd.centered = 1 # set the text to be centered: 0 - not centered, 1 - centered
lcd.lcd_display_string("Getting data", 1)
time.sleep(1)


try:
    while True:
        # get current weather update
        w = observation.get_weather() # get weather from the observation for a given location
        wd.setInfo(w) # constructor for wd (Weather Data)
        
        loop_end_time = time.time() + 60 * update_interval # how long the loop will run for
        while time.time() < loop_end_time:
            wd.printInfoToDisplay() # print the display constantly until the next update interval
        
            
except KeyboardInterrupt: 
    print("Ending!")
    lcd.lcd_clear()