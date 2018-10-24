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


# Write to logfile
def write_to_file(timestamp, string):
    try:
        with open('log.txt', 'a') as f:
            f.write(str(timestamp) + "\t" + string + "\n")

    except:   # Print error message if write was not executed
        print('Could not write to file.')


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

        if temp is None or humidity is None:  # Handle None values from unsuccessful reading
            write_to_file(timestamp, "No reading available")

        else:  # Otherwise write reading to file
            write_to_file(timestamp, "Temperature={}, Humidity={}%".format(int(temp), int(humidity)))

            # Check alert conditions
            if temp < -2 or temp > 52:
                write_to_file(timestamp, "Temperature reading faulty")

            elif temp < 18:
                write_to_file(timestamp, "Temperature is high")

            elif temp > 22:
                write_to_file(timestamp, "Temperature is high")

            if humidity < 15 or humidity > 85:
                write_to_file(timestamp, "Humidity reading faulty")

            elif 0 <= humidity <= 45:
                write_to_file(timestamp, "Humidity is low")

            elif 78 <= humidity <= 85:
                write_to_file(timestamp, "Humidity is high")

    except:
        print("Something went wrong.")



