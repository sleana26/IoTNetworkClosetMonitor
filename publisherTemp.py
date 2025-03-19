import paho.mqtt.client as mqtt
import time
import thermoHygrometer
import _sqlite3

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("temperature")
client.connect(mqttBroker)

while True:
    client.publish("home/temp", "temp", thermoHygrometer.getTemp())
    client.publish("home/humidity", "humidity" thermoHygrometer.getHumidity())
    print("Just published temp :" + thermoHygrometer.getTemp() + " and humidity: " + thermoHygrometer.getHumidity())
    time.sleep(2)