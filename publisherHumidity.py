import paho.mqtt.client as mqtt
import time
import thermoHygrometer

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("humidity")
client.connect(mqttBroker)

client.publish(thermoHygrometer.getTemp())