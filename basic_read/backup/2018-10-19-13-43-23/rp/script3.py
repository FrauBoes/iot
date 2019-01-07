# -*- coding: utf-8 -*-

import Adafruit_DHT
import schedule
import time
import datetime


def read_sensor():
    sensor = 11    # GPIO (BCM notation)
    pin = 17
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    time = datetime.datetime.now()

    print(str(time) + "\tTemperature={}, Humidity={}%; ".format(temperature, humidity))


schedule.every(5).seconds.do(read_sensor)

while True:
    schedule.run_pending()
    time.sleep(0.5)


# while True:
#     s.enter(5, 0, read_sensor(), {})
    # t_end = time.time() + 4.999
    # print(read_sensor())
    #
    # while time.time() < t_end:
    #     time.sleep(0.001)
