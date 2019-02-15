# import necessary libraries
import lcd
import time
import pyowm

# initialize the display
lcd.init()

# import necessary API keys from OWM
owm = pyowm.OWM("9995828c00a169603b3ea26fe5b9e048")
observation = owm.weather_at_place("Skopje")

try:
    while True:
        # get current weather update
        w = observation.get_weather()
        temp = w.get_temperature('celsius')
        curr_temp = ("Current Temp: %dC" % temp['temp'])
        rain = w.get_snow()
        print(rain)
        lcd.printString(curr_temp, 1)
        time.sleep(1000)

except KeyboardInterrupt: 
    print("Ending!")
    lcd.clear()