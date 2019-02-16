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



try:
    while True:
        # get current weather update
        w = observation.get_weather()
        
        # get current weather information
        temp = w.get_temperature('celsius')
        snow = w.get_snow() # returns snow volume (ex. { } )
        rain = w.get_rain() # returns rain volume (ex. '3h' : 0 } )
        wind = w.get_wind().get('speed') # returns wind speed and degree (ex. 2.600)
        humidity = w.get_humidity() # returns humidity
        status = w.get_status() # returns status (ex. 'Cloudy')
        clouds = w.get_clouds() # returns cloud coverage (ex. 65)
        
        
        # form the Strings
        curr_location = location
        
        curr_status = status
        if status=="Snow":
            curr_status = "Snowing!"
        elif status == "Rain":
            curr_status = "Raining!"
        elif status == "Sunny":
            curr_status = "Sunny!"
        
        curr_temp = ("Temperature: %dC" % temp['temp'])       
        curr_wind = ("Wind: %dkm/h" % (wind * 3.6))
        curr_humidity = ("Humidity: %d%%" % humidity)
        lcd.clear()
        
        loop_end_time = time.time() + 60 * 15 # how long the loop will run for
        while time.time() < loop_end_time:
            lcd.printString(location, 1)
            
            lcd.printString(curr_status, 2)
            time.sleep(5)
            lcd.printString(curr_temp, 2)
            time.sleep(5)
            lcd.printString(curr_wind, 2)
            time.sleep(5)
            lcd.printString(curr_humidity, 2)
            time.sleep(5)
            
except KeyboardInterrupt: 
    print("Ending!")
    lcd.clear()