# import necessary libraries
from lcd import lcddriver
import time
import pyowm
import weather_display_model
import configparser

# read api key from api.ini
config = configparser.ConfigParser()
config.read('api.ini')
api_key = config.get("api_key")

# enter information
location = "London"
measurementSystem = 0 # 0 - Metric, 1 - Imperial
update_interval = 15 # update interval in minutes

# import necessary API keys from OWM
owm = pyowm.OWM("Your API") # API Key here
observation = owm.weather_at_place(location)
wd = weather_display_model.WeatherDisplay(location, measurementSystem)

try:
    while True:
        # get current weather update
        w = observation.get_weather()
        wd.set_info(w)
        loop_end_time = time.time() + 60 * update_interval
        while time.time() < loop_end_time:
            wd.print_info_to_display()
            
except KeyboardInterrupt: 
    print("Ending!")
    # lcd.lcd_clear()