
import sys
import time

def read_temperature(device_id):
    "Read float temperature value from 1wire device DS18B20."

    with open('/sys/bus/w1/devices/%s/w1_slave' % device_id) as f:
        text = f.read().strip()
        fragments = text.split()
        return float(fragments[-1][2:]) / 1000.

while True:
        print(read_temperature('28-0000082964ce'))
        time.sleep(1)
