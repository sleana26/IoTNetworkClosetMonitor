import paho.mqtt.client as mqtt
import time
import datetime
import sqlite3
from twilio.rest import Client
import os
from dotenv import load_dotenv

##load variables from .env
load_dotenv()

#access variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twillio_phone_num = os.environ.get('PHONE_NUM')

##connect to technician SMS
client = Client()

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
def send_technician_SMS():
    try:
        #attempt message
        message = client.message.create(
            body = "Network closet environment unstable"
            from_=twillio_phone_num
            to="+13154123162"
        )

        print(f"Message sent succesfully")

    except TwilioRestException as e:
        print(f"Error: {e.msg}")
        print(f"HTTP Status: {e.status}")
        print(f"More Info: {e.code}")

##publishes a request for a cooling to turn on
def cooling_activation():
    pass

## print data with time stamp
def manage_data(temp, humidity):
    timestamp = datetime.datetime()
    data = [timestamp, temp, humidity]
    ##print data
    print("Time: " + timestamp + "| Temp: " + temp + "| Humidity: " + humidity)
    if temp > 30:
        print("Temp high, sending message to technician")
        ##call technician_SMS function
        send_technician_SMS()
    if humidity > 60:
        print("Humidity high, sending message to technician")
        ##call technician_SMS function
        send_technician_SMS()
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