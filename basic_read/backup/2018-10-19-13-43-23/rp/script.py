# Script to read temp and humidity from DHT11 sensor

import Adafruit_DHT
import datetime
import time


sensor = 11    # Assign GPIO pin numbers
pin = 17


# Read temperature and humidity from DHT sensor
def read_sensor(sensor, pin):

    try:
        humidity, temp = Adafruit_DHT.read(sensor, pin)

    except:    # Return None if reading was unsuccessful
        print(str(datetime.datetime.now()) + ' Reading unsuccessful')
        return None, None

    return temp, humidity


# Write to file
def write_to_file(string):
    try:
        with open('log.txt', 'a') as f:
            f.write(string)

    except:   # Print error message if write was not executed
        print('Could not write to file.')


# Code for scheduled sensor readings
# Readings in 5 seconds intervals

t_next = time.time() + 5    # Set time of next reading to current time + 5 sec

while True:

    while time.time() < t_next:  # Sleep until t_next is reached
        time.sleep(0.0001)

    t_next += 5  # Set time of next reading to current time + 5 sec

    temp, humidity = read_sensor(sensor, pin)

    if temp is None or humidity is None:    # Handle None values from unsuccessful reading
        write_to_file(str(datetime.datetime.now()) + " No reading available\n")

    else:    # Otherwise write reading to file
        write_to_file(str(datetime.datetime.now()) + "\tTemperature={}, Humidity={}%\n".format(int(temp), int(humidity)))
