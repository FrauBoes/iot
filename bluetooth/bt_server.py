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
    data = timestamp_val + "\t" + "Temperature={}; Humidity={}".format(temperature_val, humidity_val)
    # logging.debug(data)
    logfile.write(data + "\n")


# Log data to file
def log_values_to_logentries(timestamp_val, student_num, humidity_val, temperature_val):
    data = timestamp_val + "\t SensorID=" + student_num + ", Temperature={}, Humidity={}".format(temperature_val, humidity_val)
    logging.debug(data)
    log.info(data)


# Class defining entry to be logged to queue
class Entry:
    def __init__(self, timestamp, id, temp, humidity):
        self.timestamp = timestamp
        self.id = id
        self.temp = temp
        self.humidity = humidity


# Class for thread which controls bluetooth comms to remote sensor
# Thread waits for connection and then requests data from sensor and adds to queue
class BluetoothThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(BluetoothThread, self).__init__()
        self.target = target
        self.name = name
        self.stop_event = threading.Event()

    def finish(self):
        self.stop_event.set()

    def run(self):

        while not self.stop_event.is_set():
            # Start bluetooth connection
            try:
                server_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
                port = 0x1001
                server_sock.bind(("", port))
                server_sock.listen(1)
                server_sock.settimeout(10)

                logging.debug("Waiting for connection...")
                client_sock, address = server_sock.accept()
                server_sock.settimeout(None)
                # logging.debug("Accepted connection from ", address)

                while not self.stop_event.is_set():

                    block_until_second_div(5)

                    logging.debug("Requesting remote data...")
                    client_sock.send("Read Request")
                    data = client_sock.recv(1024)
                    # logging.debug("Data received:", str(data))

                    timestamp_blue, temperature_blue, humidity_blue = data.split(',')
                    # logging.debug("vals:" + timestamp_blue + ", " + temperature_blue + ", " + humidity_blue)

                    remote_entry = Entry(timestamp_blue, '14209816', temperature_blue, humidity_blue)

                    if not q.full():
                        q.put(remote_entry)
                        #logging.debug('Putting ' + str(remote_entry) + ' : ' + str(q.qsize()) + ' items in queue')

                    time.sleep(1)

            except bluetooth.BluetoothError as e:
                logging.debug("Bluetooth did not connect.. Retrying..")
                server_sock.close();

        server_sock.close();
        return


# Class for thread which controls transfer of values in queue to rapid7 insight ops
# Thread waits for connection and then requests data from sensor and adds to queue
class InsightPushThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(InsightPushThread, self).__init__()
        self.target = target
        self.name = name
        self.stop_event = threading.Event()

    def finish(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            if not q.empty():
                current_entry = q.get()
                try:
                    logging.debug('Getting ' + str(current_entry) + ' : ' + str(q.qsize()) + ' items in queue')

                    # Push to rapid7
                    log_values_to_logentries(current_entry.timestamp, current_entry.id, current_entry.humidity, current_entry.temp)
                    # Simulate extreme values:
                    # log_values_to_logentries(current_entry.timestamp, current_entry.id, 100, -10)
                except Exception as e:
                    logging.debug("An error has occurred, entry placed back on the queue")
                    print(e)
                    q.put(current_entry)
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
            remote_entry = Entry(timestamp_local, '17205685', temperature_local, humidity_local)

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
pin = 17

local = LocalSensorThread(name='local-sensor')
blue = BluetoothThread(name='bluetooth-sensor')
insight = InsightPushThread(name='insight-push')

local.start()
blue.start()
insight.start()

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    logging.debug("Stopping program. Should take 10 seconds at most.")
    local.finish()
    blue.finish()
    insight.finish()
