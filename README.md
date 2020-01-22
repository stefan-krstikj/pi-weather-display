# Mini-LCD-Display
16x2 display connected to a Raspberry Pi, used to display weather from OpenWeatherMap API

## Getting Started
This project is built using a 16x2 display directly connected to the Raspberry Pi. You can get one from any major E-Commerce Website

### Prerequisites

You are going to need to get:
* [pyowm](https://pyowm.readthedocs.io/en/latest/) - OpenWeatherMaps API for Python
* [LCD Driver](https://github.com/the-raspberry-pi-guy/lcd) - The Raspberry Pi Guy's LCD Driver is used as a submodule

To get pyowm, open your terminal and write
```
$ pip install pyowm
```

### Installing

To clone this github repository, use

```
git clone https://github.com/strayckler/Mini-LCD-Display.git
```

once that's done, you can go inside the newly created Mini-LCD-Display folder by typing

```
cd Mini-LCD-Display
```

and from inside, you will need to clone The Raspberry Pi Guy's repo as a submodule. To do that, use
```
git submodule init
git submodule update
```

End with an example of getting some data out of the system or using it for a little demo

### Get an API Key from OpenWeatherMaps

To use the OpenWeatherMaps API, you will need an API Key. To do that, visit [OpenWeatherMap](https://openweathermap.org/api) and subscribe
to the **Current Weather Data** api. Follow the steps provided and get your API Key.

Once you have your api key, open **config.ini** and paste your key into the **api_key** holder.
```
api_key = "Your key"
```
Next change the default locaiton to your location, as well as the measurement unit used. It's recommended that you do not change the update interval
```
location = "London"
measurement_unit = 0
update_interval = 15
```

### Launching

To start the program, navigate to the Mini-LCD-Display directory and launch weather.py with
```
python weather.py
```

## Troubleshooting

If you are getting I/O Errors, consider changing the LCD Address inside /lcd/lcddriver.py. Change
```
ADDRESS = 0x27
```
to
```
ADDRESS = 0x3f
```

If Python fails to find the project files needed, consider changing inside the same lcddriver.py file
```
import i2c_lib
```
to
```
from lcd import i2c_lib
```


## Built With

* [pyowm](https://pyowm.readthedocs.io/en/latest/) - OpenWeatherMaps for Python

## Authors

* **Stefan Krstikj** - [strayckler](https://github.com/strayckler)

## License

This project is licensed under the MIT License

## Acknowledgments

* [The Raspberry Pi Guy](https://github.com/the-raspberry-pi-guy)
* [Maker Tutor](https://youtu.be/3XLjVChVgec)
