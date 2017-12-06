import os
import time
import sys
import Adafruit_DHT as dht
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'Demo_token'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'temperature': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        temperature = dht.read_retry(dht.DHT22, 4)
        temperature = round(temperature, 2)
        print(u"Temperature: {:g}\u".format(temperature))
        sensor_data['temperature'] = temperature

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry',json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time) 
except KeyboardInterrupt:
    pass

client.loop_stop() 
client.disconnect()
