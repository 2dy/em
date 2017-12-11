import time
from relayr import Client
from relayr.dataconnection import MqttStream
c = Client(token='df27b5240c4075ba4f71e9b6dcd2ae51b58e414c')
dev = c.get_device(id='28-0000082964ce')
def mqtt_callback(topic, payload):
    print('%s %s' % (topic, payload))
stream = MqttStream(mqtt_callback, [dev])
stream.start()
time.sleep(10)
stream.stop()
