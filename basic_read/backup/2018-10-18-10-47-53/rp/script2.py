# -*- coding: utf-8 -*-

import Adafruit_DHT
import datetime
import time

def read_sensor():
    sensor = 11    # GPIO (BCM notation)
    pin = 17
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    time = datetime.datetime.now()

    return str(time) + "\tTemperature={}ºC, Humidity={}%; ".format(temperature, humidity)


while True:
    t_end = time.time() + 4.999
    print(read_sensor())

    while time.time() < t_end:
        time.sleep(0.001)