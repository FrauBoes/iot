# -*- coding: utf-8 -*-

import Adafruit_DHT
import sched
import time
import datetime

s = sched.scheduler(time.time, time.sleep)

def read_sensor():
    sensor = 11    # GPIO (BCM notation)
    pin = 17
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    time = datetime.datetime.now()

    print(str(time) + "\tTemperature={}, Humidity={}%; ".format(temperature, humidity))

while True:
    s.enter(5, 1, read_sensor())
    s.enter(5, 1, read_sensor())
    s.run()



# def print_time(a='default'):
#     print("From print_time", time.time(), a)
#
# def print_some_times():
#     print(time.time())
#     s.enter(10, 1, print_time)
#     s.enter(5, 2, print_time, argument=('positional',))
#     s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
#     s.run()
#     print(time.time())
#
# print_some_times()