#!/usr/bin/env python

from r7insight import R7InsightHandler
import logging
import datetime
import time
import random
import bluetooth
import Adafruit_DHT
import threading
import Queue
import paho.mqtt.publish as publish


# Function for blocking until next read for trending purposes
# sec_div is second division to proceed at.
# E.g sec_div = 5 will block until the next 5 second division of 1 min
def block_until_second_div(sec_div):
    while round(time.time() - 0.5) % sec_div != 0:
        # Do nothing
        time.sleep(0.00001);


# Reads from sensor based on values set above in configuration
# If in offline-testing mode, values will be simulated
def read_sensor_values():
    # Read values from simulator
    humidity_raw, temperature_raw = Adafruit_DHT.read_retry(sensor, pin)
    return humidity_raw, temperature_raw


# Log data to file
def log_values_to_file(timestamp_val, humidity_val, temperature_val):
    logfile = open("log.txt", "a")
    data = timestamp_val + "\t" + "Temperature={}C; Humidity={}%".format(temperature_val, humidity_val)
    # logging.debug(data)
    logfile.write(data + "\n")


# Class defining entry to be logged to queue
class Entry:
    def __init__(self, timestamp, id, temp, humidity):
        self.timestamp = timestamp
        self.id = id
        self.temp = temp
        self.humidity = humidity


def bluetooth_comms(self):
    # bluetooth comms
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        bt_addr = "B8:27:EB:1C:9C:AE"
        port = 0x1001
        sock.settimeout(10)
        sock.connect((bt_addr, port))
        sock.settimeout(None)

        logging.debug("Sending data via bluetooth...")
        current_entry = q.get()
        message = str(current_entry.timestamp) + ",14209816,RFCOMM," + str(current_entry.temp) + "," + str(current_entry.humidity)
        logging.debug("BLUETOOTH COMMS: " + message)
        data_sent = message

        try:
            sock.send(data_sent)
        except:
            q.put(current_entry)
            print('Reading not sent.')

    except bluetooth.BluetoothError as e:
        logging.debug("Bluetooth did not connect..")
        time.sleep(1)

    sock.close()


def mqtt_comms(self):
    current_entry = q.get()
    message = str(current_entry.timestamp) + ",14209816,MQTT," + str(current_entry.temp) + "," + str(
        current_entry.humidity)
    logging.debug("MQTT COMMS: " + message)
    try:
        publish.single("sensor/14209816", message, hostname="rpjulia.local")
    except:
        q.put(current_entry)
        print('Reading not sent.')


# Class for thread which controls bluetooth comms to remote sensor
# Thread waits for connection and then requests data from sensor and adds to queue
class CommsThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(CommsThread, self).__init__()
        self.target = target
        self.name = name
        self.stop_event = threading.Event()

    def finish(self):
        self.stop_event.set()

    def run(self):

        daytime = True
        interval = 120
        change_time = time.time() + interval

        while not self.stop_event.is_set():

            # Set timing here
            current_time = time.time()
            if current_time > change_time:
                daytime = not daytime
                change_time = current_time + interval
                logging.debug("TIMING HAS CHANGED! Daytime=" + str(daytime))

            if not q.empty():
                if daytime:
                    mqtt_comms(self)
                else:
                    bluetooth_comms(self)
            else:
                time.sleep(1)
        return


class LocalSensorThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(LocalSensorThread, self).__init__()
        self.target = target
        self.name = name
        self.stop_event = threading.Event()

    def finish(self):
        self.stop_event.set()

    # This thread reads values from remote sensor via bluetooth and adds to queue
    def run(self):
        while not self.stop_event.is_set():
            block_until_second_div(5)
            timestamp_local = str(datetime.datetime.now())
            humidity_local, temperature_local = read_sensor_values()
            remote_entry = Entry(timestamp_local, '14209816', temperature_local, humidity_local)

            if not q.full():
                q.put(remote_entry)
                logging.debug('Putting ' + str(remote_entry) + ' : ' + str(q.qsize()) + ' items in queue')

            time.sleep(1)
        return


# Multi thread variables
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s', )
BUF_SIZE = 50
q = Queue.Queue(BUF_SIZE)

log = logging.getLogger('r7insight')
log.setLevel(logging.INFO)
handler = R7InsightHandler('1143ef16-8a10-444b-913c-28844b3ab4b2', 'eu')
log.addHandler(handler)

# Application Configuration parameters
testing = False

# Sensor Configuration parameters
sensor = 11
pin = 4

local = LocalSensorThread(name='sensor')
comms = CommsThread(name='comms')

local.start()
comms.start()

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    logging.debug("Stopping program. Should take 10 seconds at most.")
    local.finish()
    comms.finish()
