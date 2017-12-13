import json
import time

import paho.mqtt.client as mqtt

creds = {
    "user": "3c37970d-2676-46d1-90d5-de7f9e6851a1",
    "password": "fN9d.DLyqs8k",
    "clientId": "TPDeXDSZ2RtGQ1d5/nmhRoQ",
    "topic": "/v1/3c37970d-2676-46d1-90d5-de7f9e6851a1/",
	'server':   'mqtt.relayr.io',
    'port':     1883
}

def read_temperature(device_id):
    "Read float temperature value from 1wire device DS18B20."
    with open('/sys/bus/w1/devices/%s/w1_slave' % device_id) as f:
        text = f.read().strip()
        fragments = text.split()
        return float(fragments[-1][2:]) / 1000.


publishing_period = 1000


class MqttDelegate(object):
    "A delegate class providing callbacks for an MQTT client."

    def __init__(self, client, credentials):
        self.client = client
        self.credentials = credentials

    def on_connect(self, client, userdata, flags, rc):
        print('Connected.')
        self.client.subscribe(self.credentials['topic'] + 'cmd')

    def on_message(self, client, userdata, msg):
        print('Command received: %s' % msg.payload)

    def on_publish(self, client, userdata, mid):
        print('Message published.')


def main(credentials, publishing_period):
    client = mqtt.Client(client_id=credentials['clientId'])
    delegate = MqttDelegate(client, creds)
    client.on_connect = delegate.on_connect
    client.on_message = delegate.on_message
    client.on_publish = delegate.on_publish
    user, password = credentials['user'], credentials['password']
    client.username_pw_set(user, password)

    try:
        print('Connecting to mqtt server.')
        server, port = credentials['server'], credentials['port']
        client.connect(server, port=port, keepalive=60)
    except:
        print('Connection failed, check your credentials!')
        return


    if publishing_period < 200:
        publishing_period = 200

    while True:
        client.loop()
        device_id = '28-0000082964ce'
        sensor_value = read_temperature(device_id)

        message = {
            'meaning': 'temperature',
            'value': sensor_value
        }
        client.publish(credentials['topic'] + 'data', json.dumps(message))
        time.sleep(publishing_period / 1000.)

if __name__ == '__main__':
    main(creds, publishing_period)
