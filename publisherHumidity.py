import paho.mqtt.client as mqtt
import time
import publisherHumidity


mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("humidity")
client.connect(mqttBroker)

client.publish(publisherTemp.getTemp())
