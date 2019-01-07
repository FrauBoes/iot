# file: l2capclient.py
# desc: Demo L2CAP client for bluetooth module.
# $Id: l2capclient.py 524 2007-08-15 04:04:52Z albert $

import sys
import bluetooth
import Adafruit_DHT
import datetime
import time


# Read temperature and humidity from DHT sensor
def read_sensor(sensor, pin):

    try:
        humidity, temp = Adafruit_DHT.read(sensor, pin)

    except:    # Return None if reading was unsuccessful
        print(str(datetime.datetime.now()) + '\tReading unsuccessful')
        return None, None

    return temp, humidity


if sys.version < '3':
    input = raw_input

sock=bluetooth.BluetoothSocket(bluetooth.L2CAP)

if len(sys.argv) < 2:
    print("usage: l2capclient.py <addr>")
    sys.exit(2)

bt_addr=sys.argv[1]
port = 0x1001

print("trying to connect to %s on PSM 0x%X" % (bt_addr, port))

sock.connect((bt_addr, port))

print("connected.")

# Code for scheduled sensor readings
# Readings in 5 seconds intervals

sensor = 11    # Assign GPIO pin numbers
pin = 17

t_next = time.time() + 5    # Set time of next reading to current time + 5 sec

log_store = []    # List of readings that coulc not be sent

while True:

    server_request = sock.recv(1024)
    print(server_request)

    if server_request == 'Read Request':
        temp, humidity = read_sensor(sensor, pin)  # Store reading

        timestamp = datetime.datetime.now()  # Store timestamp

        data_sent = str(timestamp) + "," + str(temp) + "," + str(humidity)

        try:
            sock.send(data_sent)
        except:
            log_store.append(data_sent)
            print('Reading not sent.')

sock.close()
