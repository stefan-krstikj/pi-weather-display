# import necessary libraries
import lcddriver
import time
import pyowm

SLEEPTIME = 5 # seconds of time between messages

class WeatherDisplay:
    # Set default values for variables
    location = "None" # location of the observation
    temperature = 0 # temperature for the location
    humidity = 0 # humidity for the location
    wind = 0 # wind for the location
    rain = 0 # rain for the location
    snow = 0 # snow for the location
    status = "None" # weather status (ex. Rain, Windy, Snow, Heavy Snow)
    weather_info = "" # the weather info file containing all the data
    measurement_system = 0 # 0 - Metric, 1 - Imperial
    
    
    # constructor with location and measurement_system
    def __init__(self, location, measurement_system):
        self.location = location
        self.measurement_system = measurement_system
    
    # set the info for all the va riables
    def setInfo(self, weather_info):
        self.weather_info = weather_info # setting the weather_info variable to the given one
        
        # check the measurement system variable
        # used for pulling measurement value in given system
        # get_temperature('celsius') returns temp in celsius
        # get_temperature('fahrenheit') returns temp in fahrenheit
        celsius_fahrenheit = "celsius"
        if self.measurement_system == 1:
            celsius_fahrenheit = "fahrenheit"
        self.temperature = weather_info.get_temperature(celsius_fahrenheit)
        
        # setting the rest of the variables
        self.snow = weather_info.get_snow() # returns snow volume (ex. { } )
        self.rain = weather_info.get_rain() # returns rain volume (ex. '3h' : 0 } )
        self.wind = weather_info.get_wind() # returns wind speed and degree (ex. 2.600) in m/s
        self.humidity = weather_info.get_humidity() # returns humidity
        self.status = weather_info.get_detailed_status() # returns status (ex. 'Cloudy')
        self.clouds = weather_info.get_clouds() # returns cloud coverage (ex. 65)
        
    
    # check the rain if any
    # returns the most recent rain forecast
    def checkRain(self):
        if self.rain.get('1h') is not None:
            return ("Rain 1h: %.1fmm" % self.rain.get('1h'))
        elif self.rain.get('2h') is not None:
            return ("Rain 2h: %.1fmm" % self.rain.get('2h'))
        elif self.rain.get('3h') is not None:
            return ("Rain 3h: %.1fmm" % self.rain.get('3h'))
        return ""
    
    # check the snow if any
    # returns the most recent snow forecast
    def checkSnow(self):
        if self.snow.get('1h') is not None:
            return ("Snow 1h: %.1fmm" % self.snow.get('1h'))
        elif self.snow.get('2h') is not None:
            return ("Snow 2h: %.1fmm" % self.snow.get('2h'))
        elif self.snow.get('3h') is not None:
            return ("Snow 3h: %.1fmm" % self.snow.get('3h'))
        return ""
    
    # function that calls the respective variable's print methods
    # and prints them to the display
    def printInfoToDisplay(self):
        # initializing a display
        lcd = lcddriver
        lcd.init()
    
        lcd.printString(self.printLocation(), 1)
        
        lcd.printString(self.printStatus(), 2)
        time.sleep(SLEEPTIME)
        
        lcd.printString(self.printCurrTemperature(), 2)
        time.sleep(SLEEPTIME)
        
        lcd.printString(self.printHiLoTemperature(), 2)
        time.sleep(SLEEPTIME)
        
        lcd.printString(self.printHumidity(), 2)
        time.sleep(SLEEPTIME)
        
        lcd.printString(self.printWind(), 2)
        time.sleep(SLEEPTIME)
        
        lcd.printString(self.printClouds(), 2)
        time.sleep(SLEEPTIME)
        
        rain_string = self.checkRain()
        if rain_string is not "":
            lcd.printString(rain_string, 2)
            time.sleep(SLEEPTIME)
            
        snow_string = self.checkSnow()
        if snow_string is not "":
            lcd.printString(snow_string, 2)
            time.sleep(SLEEPTIME)
    

    
    def printLocation(self):
        location_string = self.location
        if len(location_string ) >= 16:
            location_string = location_string[0 : 16]
            if location_string[15] == ",":
                location_string = location_string[0 : 15]
        return location_string
    
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
        