# import necessary libraries
import lcddriver
import time
import pyowm

# initialize the display
lcd = lcddriver
lcd.init()

# import necessary API keys from OWM
owm = pyowm.OWM("9995828c00a169603b3ea26fe5b9e048") # API Key here
location = "South Lake Tahoe, CA, USA" # Location for the Observation
observation = owm.weather_at_place(location)

lcd.printString("Weather", 1)
time.sleep(2)
lcd.printString(" -Stefan", 2)


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
            status = "Snowing! Don't forget your boots"
        elif status == "Rain":
            status = "Raining! Bring an umbrella!"
        elif status == "Sunny":
            status = "Sunny! Bring the shades!"
            
        curr_temp = ("Current Temp: %dC" % temp['temp'])       
        curr_wind = ("Wind: %dkm/h" % (wind * 3.6))
        curr_humidity = ("Humidity: %d%%" % humidity)
        break
        #loop_end_time = time.time() + 60 * 15 # how long the loop will run for
        #while time.time() < t.end:
            
except KeyboardInterrupt: 
    print("Ending!")
    lcd.clear()