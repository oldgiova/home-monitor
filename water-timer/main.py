import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
from itertools import repeat
from datetime import datetime,time
from time import sleep
from pytz import timezone
import logging,pdb, sys

'''initial var'''
RELAIS_4_GPIO = 22
water_time = 600
influxdb_user = 'pippo'
influxdb_password = 'pippopassword'
influxdb_db = 'LIGHT'
influxdb_host = 'localhost'
influxdb_port = 8086
influxdbclient = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_db)
tz = 'Rome'

'''logging config'''
logging.basicConfig(
        level=logging.INFO,
        filename='water.log',
        format='[%(asctime)s] %(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

'''functions'''
def water_on():
    GPIO.output(RELAIS_4_GPIO, GPIO.LOW)
    logging.debug('Water On')
    return True

def water_off():
    GPIO.output(RELAIS_4_GPIO, GPIO.HIGH)
    logging.debug('Water Off')
    return True

def insert_influxdb_row(value):
    utcnow = datetime.utcnow()
    '''json_body template'''
    json_body = [
            {
                "measurement": "water",
                "tags": {
                    "host": "cortile"
                    },
                "time": utcnow,
                "fields": {
                    "value": value
                    }
                }
            ]
    logging.debug('writing a value to influxdb with time ' + utcnow.strftime("%H:%M:%S"))
    influxdbclient.write_points(json_body)

def main():
    logging.info('Starting up ')
    '''GPIO settings'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAIS_4_GPIO, GPIO.OUT, initial=GPIO.HIGH)
    try: 
        '''main program'''
        water_on()
        for i in range(water_time):
            insert_influxdb_row(1)
            sleep(1)
        water_off()
        sys.exit()

    except KeyboardInterrupt:
        logging.info('shutting down for keyboard interrupt')
        water_off()
        insert_influxdb_row(1)

    except:
        logging.info('shutting down for other interrupt')
        water_off()
        insert_influxdb_row(1)

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
