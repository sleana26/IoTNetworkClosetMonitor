import adafruit_dht
from board import <pin>

thermoHygrometer = adafruit_dht.DHT22(<pin>)

def getTemp():
    temperature = thermoHygrometer.temperature
    return temperature

def getHumidity(): 
    humidity = thermoHygrometer.humidity
    return humidity