# -*- coding: utf-8 -*-

import Adafruit_DHT
import schedule
import time
import datetime


def read_sensor():
    sensor = 11    # GPIO (BCM notation)
    pin = 17
    humidity, temp = Adafruit_DHT.read(sensor, pin)

    if temp is None or humidity is None:    # Handle None values from unsuccessful reading
        print(str(datetime.datetime.now()) + " No reading available\n")

    else:
        print(str(datetime.datetime.now()) + "\tTemperature={}, Humidity={}%; ".format(temp, humidity))


schedule.every(5.00).seconds.do(read_sensor)

while True:
    schedule.run_pending()
