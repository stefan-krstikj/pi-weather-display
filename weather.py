# import necessary libraries
import lcddriver
import time
import pyowm
import weatherDisplay

# enter information
location = "South Lake Tahoe, CA, USA" # Location for the Observation
measurementSystem = 1 # 0 - Metric, 1 - Imperial

# import necessary API keys from OWM
owm = pyowm.OWM("9995828c00a169603b3ea26fe5b9e048") # API Key here
observation = owm.weather_at_place(location)
wd = weatherDisplay.WeatherDisplay(location, measurementSystem)

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
time.sleep(1)


try:
    while True:
        # get current weather update
        w = observation.get_weather()
        wd.setInfo(w)
         
        loop_end_time = time.time() + 60 * 15 # how long the loop will run for
        while time.time() < loop_end_time:
            wd.printInfoToDisplay()
        
            
except KeyboardInterrupt: 
    print("Ending!")
    lcd.clear()