# import necessary libraries
from lcd import lcddriver
import time
import pyowm
import weather_display_model
import configparser

# read api key from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get("api_key")

# enter information
location = config.get("location")
measurement_unit = config.get("measurement_unit")  # 0 - Metric, 1 - Imperial
update_interval = config.get("update_interval")  # update interval in minutes

# import necessary API keys from OWM
owm = pyowm.OWM(api_key)  # API Key here
observation = owm.weather_at_place(location)
wd = weather_display_model.WeatherDisplay(location, measurement_unit)

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
