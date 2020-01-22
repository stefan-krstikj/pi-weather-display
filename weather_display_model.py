# import necessary libraries
from lcd import lcddriver
import time
import pyowm
from Utils import calculate_centered

# time between messages
SLEEPTIME = 5


class WeatherDisplay:
    # Set default values for variables
    location = "None"
    temperature = 0
    humidity = 0
    wind = 0
    clouds = 0
    rain = 0
    snow = 0
    status = "None"  # weather status (ex. Rain, Windy, Snow, Heavy Snow)
    weather_info = ""  # the weather info file containing all the data
    measurement_system = 0  # 0 - Metric, 1 - Imperial
    lcd = None

    def __init__(self, location, measurement_system):
        self.location = location
        self.measurement_system = measurement_system
        self.lcd = lcddriver.lcd()
        self.lcd.lcd_display_string("Getting data", 1)
        time.sleep(2)
        self.lcd.lcd_clear()

    def set_info(self, weather_info):
        self.weather_info = weather_info
        celsius_fahrenheit = "celsius"
        if self.measurement_system == 1:
            celsius_fahrenheit = "fahrenheit"
        self.temperature = weather_info.get_temperature(celsius_fahrenheit)
        self.snow = weather_info.get_snow()
        self.rain = weather_info.get_rain()
        self.wind = weather_info.get_wind()
        self.humidity = weather_info.get_humidity()
        self.status = weather_info.get_detailed_status()
        self.clouds = weather_info.get_clouds()
        print("Finished setting info")

    # returns the most recent rain forecast
    def check_rain(self):
        if self.rain.get('1h') is not None:
            return "Rain 1h: %.1fmm" % self.rain.get('1h')
        elif self.rain.get('2h') is not None:
            return "Rain 2h: %.1fmm" % self.rain.get('2h')
        elif self.rain.get('3h') is not None:
            return "Rain 3h: %.1fmm" % self.rain.get('3h')
        return ""

    # returns the most recent snow forecast
    def check_snow(self):
        if self.snow.get('1h') is not None:
            return "Snow 1h: %.1fmm" % self.snow.get('1h')
        elif self.snow.get('2h') is not None:
            return "Snow 2h: %.1fmm" % self.snow.get('2h')
        elif self.snow.get('3h') is not None:
            return "Snow 3h: %.1fmm" % self.snow.get('3h')
        return ""
    
    def calculate_centered(self, message):
        if len(message) >= 16:
            return message
        empty_spaces = 16 - len(message)
        left_spaces = (empty_spaces / 2)
        final_message = " " * int(left_spaces) + message
        return final_message

    def print_info_to_display(self):
        # todo: Refactor
        self.__print_location()
        self.__print_status()
        self.__print_current_temperature()
        self.__print_hilo_temperature()
        self.__print_humidity()
        self.__print_wind()
        self.__print_clouds()
        self.__print_rain()
        self.__print_snow()

    def __print_location(self):
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string(calculate_centered(self.location), 1)

    def __print_status(self):
        self.__print_location()
        self.lcd.lcd_display_string(calculate_centered(self.status), 2)
        time.sleep(SLEEPTIME)

    def __print_current_temperature(self):
        self.__print_location()
        temp_sign = "C"
        if self.measurement_system == 1:
            temp_sign = "F"
        temp_string = ("Temperature: %d%s" % (self.temperature.get('temp'), temp_sign))
        self.lcd.lcd_display_string(calculate_centered(temp_string), 2)
        time.sleep(SLEEPTIME)

    def __print_hilo_temperature(self):
        self.__print_location()
        temp_sign = "C"
        if self.measurement_system == 1:
            temp_sign = "F"
        hilo_temp_string = ("HI: %d%s LO: %d%s" % (self.temperature.get('temp_max'), temp_sign,
                                                   self.temperature.get('temp_min'), temp_sign))

        self.lcd.lcd_display_string(calculate_centered(hilo_temp_string), 2)
        time.sleep(SLEEPTIME)

    def __print_humidity(self):
        self.__print_location()
        humidity_string = ("Humidity: %d%%" % self.humidity)
        self.lcd.lcd_display_string(calculate_centered(humidity_string), 2)
        time.sleep(SLEEPTIME)

    def __print_clouds(self):
        self.__print_location()
        clouds_string = ("Clouds: %d%%" % self.clouds)
        self.lcd.lcd_display_string(calculate_centered(clouds_string), 2)
        time.sleep(SLEEPTIME)

    def __print_wind(self):
        self.__print_location()
        wind_speed = self.wind.get('speed')
        wind_deg = self.wind.get('deg')
        speed_sign = "km/h"

        if self.measurement_system == 1:
            wind_speed = wind_speed * 2.26
            speed_sign = "mp/h"
        else:
            wind_speed = wind_speed * 3.6

        wind_string = ("Wind: %d%s" % (wind_speed, speed_sign))
        self.lcd.lcd_display_string(calculate_centered(wind_string), 2)
        time.sleep(SLEEPTIME)

    def __print_rain(self):
        rain_string = self.check_rain()
        if rain_string is not "":
            self.__print_location()
            self.lcd.lcd_display_string(calculate_centered(rain_string), 2)
            time.sleep(SLEEPTIME)

    def __print_snow(self):
        snow_string = self.check_snow()
        if snow_string is not "":
            self.__print_location()
            self.lcd.lcd_display_string(calculate_centered(snow_string), 2)
            time.sleep(SLEEPTIME)