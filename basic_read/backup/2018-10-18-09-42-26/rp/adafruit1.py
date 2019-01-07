import Adafruit_DHT
import datetime

sensor = 11
pin = 17

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    # GPIO (BCM notation)

    time = datetime.datetime.now()
    
    print(str(time) + " Humidity={}%; Temperature={}%C".format(humidity, temperature))
