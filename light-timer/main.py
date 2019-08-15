import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
from datetime import datetime,time
from astral import *
from time import sleep
from pytz import timezone
import logging,pdb

'''initial var'''
RELAIS_4_GPIO = 2
'''hour to switch light off'''
off_time = time(23,59)
sleep_time = 600
influxdb_user = 'pippo'
influxdb_password = 'pippopassword'
influxdb_db = 'LIGHT'
influxdb_host = 'localhost'
influxdb_port = 8086
influxdbclient = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_db)
tz = 'Rome'

'''logging config'''
logging.basicConfig(
        level=logging.DEBUG,
        filename='light.log',
        format='[%(asctime)s] %(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

'''functions'''
def light_on():
    GPIO.output(RELAIS_4_GPIO, GPIO.LOW)
    logging.debug('Light On')
    return True

def light_off():
    GPIO.output(RELAIS_4_GPIO, GPIO.HIGH)
    logging.debug('Light Off')
    return True

def insert_influxdb_row(value):
    utcnow = datetime.utcnow()
    '''json_body template'''
    json_body = [
            {
                "measurement": "light",
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

def astral_query_time(today):
    '''find today sunrise'''
    a = Astral()
    location = a[tz]
    sun = location.sun(local=True, date=today)
    return sun['dawn'], sun['sunset']

def check_astral():
    '''astral check'''
    local_tz = timezone('Europe/Rome')
    now = datetime.now()
    #fix timezone naive problem
    now = local_tz.localize(now)
    today = now.date()
    #pdb.set_trace()
    logging.debug('today is: ' + today.strftime("%Y%m%d"))
    today_dawn, today_sunset = astral_query_time(today)
    today_datetime = now.astimezone(local_tz)
    if (
        today_datetime <= today_sunset and 
        today_datetime <= today_dawn
       ):
       '''It's early morning, keep on'''
       logging.debug("It's early morning, keep on")
       return True
    if (
        today_datetime <= today_sunset and 
        today_datetime >= today_dawn
       ):
       '''It's morning, switch off'''
       logging.debug("It's morning, switch off")
       return False
    if (
        today_datetime >= today_sunset and 
        today_datetime >= today_dawn
       ):
       '''It's evening, switch on'''
       logging.debug("It's evening, switch on")
       return True


def main():
    logging.info('Starting up ')
    '''GPIO settings'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAIS_4_GPIO, GPIO.OUT, initial=GPIO.HIGH)
    try: 
        '''main program'''
        while True:
            is_dark = check_astral()
            if is_dark:
                light_on()
                insert_influxdb_row(2)
            else:
                light_off()
                insert_influxdb_row(1)
            sleep(sleep_time)

    except KeyboardInterrupt:
        logging.info('shutting down for keyboard interrupt')

    except:
        logging.info('shutting down for other interrupt')

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
