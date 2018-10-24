# -*- coding: utf-8 -*-

import Adafruit_DHT
import datetime

def read_sensor():
    sensor = 11    # GPIO (BCM notation)
    pin = 17
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    time = datetime.datetime.now()

    return str(time) + "\tTemperature={}ºC, Humidity={}%; ".format(temperature, humidity)

while True:
    print(read_sensor())