# import necessary libraries
from lcd import lcddriver
from Utils import calculateCentered
import time
import pyowm

# time between messages
SLEEPTIME = 5

class WeatherDisplay:
    # Set default values for variables
    location = "None"
    temperature = 0
    humidity = 0
    wind = 0
    rain = 0
    snow = 0
    status = "None" # weather status (ex. Rain, Windy, Snow, Heavy Snow)
    weather_info = "" # the weather info file containing all the data
    measurement_system = 0 # 0 - Metric, 1 - Imperial
    lcd = None

    def __init__(self, location, measurement_system):
        self.location = location
        self.measurement_system = measurement_system
        self.lcd = lcddriver.lcd()
        self.lcd.lcd_display_string("Getting data", 1)
        time.sleep(1)
        self.lcd.lcd_clear()

    def setInfo(self, weather_info):
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
        
    # returns the most recent rain forecast
    def checkRain(self):
        if self.rain.get('1h') is not None:
            return ("Rain 1h: %.1fmm" % self.rain.get('1h'))
        elif self.rain.get('2h') is not None:
            return ("Rain 2h: %.1fmm" % self.rain.get('2h'))
        elif self.rain.get('3h') is not None:
            return ("Rain 3h: %.1fmm" % self.rain.get('3h'))
        return ""
    
    # returns the most recent snow forecast
    def checkSnow(self):
        if self.snow.get('1h') is not None:
            return ("Snow 1h: %.1fmm" % self.snow.get('1h'))
        elif self.snow.get('2h') is not None:
            return ("Snow 2h: %.1fmm" % self.snow.get('2h'))
        elif self.snow.get('3h') is not None:
            return ("Snow 3h: %.1fmm" % self.snow.get('3h'))
        return ""

    def printInfoToDisplay(self):
        # todo: Refactor
        self.lcd.lcd_display_string(calculateCentered(self.location), 1)
        self.lcd.lcd_display_string(calculateCentered(self.printStatus()), 2)
        time.sleep(SLEEPTIME)
        self.lcd.lcd_clear()
        
        self.lcd.lcd_display_string(calculateCentered(self.location), 1)
        self.lcd.lcd_display_string((self.printCurrTemperature()), 2)
        time.sleep(SLEEPTIME)
        self.lcd.lcd_clear()
        
        self.lcd.lcd_display_string(calculateCentered(self.location), 1)
        self.lcd.lcd_display_string(calculateCentered(self.printHiLoTemperature()), 2)
        time.sleep(SLEEPTIME)
        self.lcd.lcd_clear()

        self.lcd.lcd_display_string(calculateCentered(self.location), 1)
        self.lcd.lcd_display_string(calculateCentered(self.printHumidity()), 2)
        time.sleep(SLEEPTIME)
        self.lcd.lcd_clear()
        
        self.lcd.lcd_display_string(calculateCentered(self.location), 1)
        self.lcd.lcd_display_string(calculateCentered(self.printWind()), 2)
        time.sleep(SLEEPTIME)
        self.lcd.lcd_clear()
        
        self.lcd.lcd_display_string(calculateCentered(self.location), 1)
        self.lcd.lcd_display_string(calculateCentered(self.printClouds()), 2)
        time.sleep(SLEEPTIME)
        self.lcd.lcd_clear()
        
        self.lcd.lcd_display_string(calculateCentered(self.location), 1)
        rain_string = self.checkRain()
        if rain_string is not "":
            self.lcd.lcd_display_string(calculateCentered(rain_string), 2)
            time.sleep(SLEEPTIME)
            self.lcd.lcd_clear()
        
        self.lcd.lcd_display_string(calculateCentered(self.location), 1)
        snow_string = self.checkSnow()
        if snow_string is not "":
            self.lcd.lcd_display_string(calculateCentered(snow_string), 2)
            time.sleep(SLEEPTIME)
            self.lcd.lcd_clear()


    # todo: delete
    # def printLocation(self):
    #     location_string = self.location
    #     if len(location_string ) >= 16:
    #         location_string = location_string[0 : 16]
    #         if location_string[15] == ",":
    #             location_string = location_string[0 : 15]
    #     return location_string
    
    def printStatus(self):
        return self.status.title()
    
    def printCurrTemperature(self):
        temperatureSign = "C"
        if self.measurement_system == 1:
            temperatureSign = "F"
        return ("Temperature: %d%s" %(self.temperature.get('temp'), temperatureSign))
    
    def printHiLoTemperature(self):
        temperatureSign = "C"
        if self.measurement_system == 1:
            temperatureSign = "F"
        return ("HI: %d%s LO: %d%s" %(self.temperature.get('temp_max'),temperatureSign,
                                               self.temperature.get('temp_min'),temperatureSign))
    def printHumidity(self):
        return ("Humidity: %d%%" %self.humidity)
    
    def printClouds(self):
        return ("Clouds: %d%%" %self.clouds)
    
    def printWind(self):
        wind_speed = self.wind.get('speed')
        wind_deg = self.wind.get('deg')
        speed_sign = "km/h"
        
        if self.measurement_system == 1:
            wind_speed = wind_speed * 2.26
            speed_sign = "mp/h"
        else:
            wind_speed = wind_speed * 3.6
            
        return ("Wind: %d%s" % (wind_speed, speed_sign))
        