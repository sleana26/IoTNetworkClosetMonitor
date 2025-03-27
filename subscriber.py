import paho.mqtt.client as mqtt
import time
import datetime
import sqlite3

##connect to SQLite
con = sqlite3.connect("tempHumidity.db")
cur = con.cursor()
cur.execute("CREATE TABLE NetworkClosetEnv(time, temp, humidity)")
##testing table creation
result = cur.execute("SELECT name FROM sqlite_master")
result.fetchone()

##buffer values enables adding to database at same timestamp
temp = None
humidity = None

##sends message to technician to inspect reason for high temp or humidity levels
def technician_SMS():
    pass

##publishes a request for a fan to turn on
def fan_activation():
    pass

## print data with time stamp
def manage_data(temp, humidity):
    timestamp = datetime.datetime()
    data = [timestamp, temp, humidity]
    ##print data
    print("Time: " + timestamp + "| Temp: " + temp + "| Humidity: " + humidity)
    if temp > 30:
        print("Temperature high, sending message to technician")
        ##call technician_SMS function
    if humidity > 60:
        print("Humidity high, sending message to technician")
        ##call technician_SMS function
    ##store data in SQLite
    cur.executemany("INSERT INTO NetworkClosetEnv VALUES(?, ?, ?)", data)
    con.commit()

##defines on_message response. We want to take in the data as an int, check which value it is, temp or humidity, set a value for 
def on_message(client, userdata, message):
    data = int(message.payload.decode("utf-8"))
    if message.topic == 'temp':
        temp = data
        if humidity != None:
            ##both values aquired, manage data together
            manage_data(temp, humidity)
            ##set values to zero after handling data
            temp = None
            humiidity = None
    if message.topic == 'humidity':
        humidity = data
        if temp != None:
            ##both values aquired, manage data together
            manage_data(temp, humidity)
            ##set values to zero after handling data
            temp = None
            humiidity = None

##connect client to broker and subscribe to temp/humidity data
broker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Subscriber")
client.connect(broker)
client.subscribe("home/temp")
client.subscribe("home/humidity")
client.on_message = on_message

##handle data for 30 seconds
client.loop_start()
time.sleep(30)
client.loop_end()