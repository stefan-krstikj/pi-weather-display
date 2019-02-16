# import necessary libraries
import lcddriver
import time
import pyowm

SLEEPTIME = 5 # seconds of time between messages

class WeatherDisplay:
    location = "None"
    temperature = 0
    humidity = 0
    wind = 0
    rain = 0
    snow = 0
    status = "None"
    weatherInfo = ""
    measurementSystem = 0 # 0 - Metric, 1 - Imperial
    
    def __init__(self, location, measurementSystem):
        self.location = location
        self.measurementSystem = measurementSystem
    
    def setInfo(self, weatherInfo):
        self.weatherInfo = weatherInfo
        
        celsiusOrFahrenheit = "celsius"
        if self.measurementSystem == 1:
            celsiusOrFahrenheit = "fahrenheit"
            self.temperatureSign = "F"
        self.temperature = weatherInfo.get_temperature(celsiusOrFahrenheit)
        
        self.snow = weatherInfo.get_snow() # returns snow volume (ex. { } )
        self.rain = weatherInfo.get_rain() # returns rain volume (ex. '3h' : 0 } )
        self.wind = weatherInfo.get_wind() # returns wind speed and degree (ex. 2.600) in m/s
        self.humidity = weatherInfo.get_humidity() # returns humidity
        self.status = weatherInfo.get_detailed_status() # returns status (ex. 'Cloudy')
        self.clouds = weatherInfo.get_clouds() # returns cloud coverage (ex. 65)
        
    
        
    def checkRain(self):
        if self.rain.get('1h') is not None:
            return ("Rain 1h: %.1fmm" % self.rain.get('1h'))
        elif self.rain.get('2h') is not None:
            return ("Rain 2h: %.1fmm" % self.rain.get('2h'))
        elif self.rain.get('3h') is not None:
            return ("Rain 3h: %.1fmm" % self.rain.get('3h'))
        return ""
    
    def checkSnow(self):
        if self.snow.get('1h') is not None:
            return ("Snow 1h: %.1fmm" % self.snow.get('1h'))
        elif self.snow.get('2h') is not None:
            return ("Snow 2h: %.1fmm" % self.snow.get('2h'))
        elif self.snow.get('3h') is not None:
            return ("Snow 3h: %.1fmm" % self.snow.get('3h'))
        return ""
    
    def printInfoToDisplay(self):
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
        if self.measurementSystem == 1:
            temperatureSign = "F"
        return ("Temperature: %d%s" %(self.temperature.get('temp'), temperatureSign))
    
    def printHiLoTemperature(self):
        temperatureSign = "C"
        if self.measurementSystem == 1:
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
        
        if self.measurementSystem == 1:
            wind_speed = wind_speed * 2.26
            speed_sign = "mp/h"
        else:
            wind_speed = wind_speed * 3.6
            
        return ("Wind: %d%s" % (wind_speed, speed_sign))
        