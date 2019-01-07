# Script to read temp and humidity from DHT11 sensor

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


# Code for scheduled sensor readings
# Readings in 5 seconds intervals

sensor = 11    # Assign GPIO pin numbers
pin = 17

t_next = time.time() + 5    # Set time of next reading to current time + 5 sec

while True:

    while time.time() < t_next:  # Sleep until t_next is reached
        time.sleep(0.0001)

    t_next += 5  # Reset t_next

    try:
        temp, humidity = read_sensor(sensor, pin)    # Store reading

        timestamp = datetime.datetime.now()  # Store timestamp
    except:
        print('Something went wrong.')



