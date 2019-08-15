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
sleep_time = 1800
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

def check_if_dark():
    '''tuned for nothern Italy'''
    now = datetime.now()
    now_time = now.time()
    #pdb.set_trace()
    logging.debug('now time: ' + now_time.strftime("%H %M"))
    currentMonth = datetime.now().month
    logging.debug('current month: ' + str(currentMonth))

    if currentMonth == 1 or currentMonth == 11 or currentMonth == 12:
        if now_time >= time(17,00) and now_time <= off_time:
            logging.debug('its ' + str(currentMonth) + ' and its dark ' + off_time.strftime("%H %M"))
            return True
        else:
            logging.debug('we have daylight or its deep night')
            return False
    elif currentMonth == 2 or currentMonth == 3:
        if now_time >= time(18,00) and now_time <= off_time:
            logging.debug('its ' + str(currentMonth) + ' and its dark ' + off_time.strftime("%H %M"))
            return True
        else:
            logging.debug('we have daylight or its deep night')
            return False
    elif currentMonth == 10:
        if now_time >= time(19,00) and now_time <= off_time:
            logging.debug('its ' + str(currentMonth) + ' and its dark ' + off_time.strftime("%H %M"))
            return True
        else:
            logging.debug('we have daylight or its deep night')
            return False
    elif currentMonth == 4 or currentMonth == 5 or currentMonth == 9:
        if now_time >= time(20,00) and now_time <= off_time:
            logging.debug('its ' + str(currentMonth) + ' and its dark ' + off_time.strftime("%H %M"))
            return True
        else:
            logging.debug('we have daylight or its deep night')
            return False
    elif currentMonth == 6 or currentMonth == 7 or currentMonth == 8:
        if now_time >= time(21,00) and now_time <= off_time:
            logging.debug('its ' + str(currentMonth) + ' and its dark ' + off_time.strftime("%H %M"))
            return True
        else:
            logging.debug('we have daylight or its deep night')
            return False

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
    # it's 03:00
    # dawn: 05:00
    # sunset: 21:00
    if (
        today_datetime <= today_sunset and 
        today_datetime <= today_dawn
       ):
       '''It's early morning, keep on'''
       logging.debug("It's early morning, keep on")
       return True
    # it's 10:00
    # dawn: 05:00
    # sunset: 21:00
    if (
        today_datetime <= today_sunset and 
        today_datetime >= today_dawn
       ):
       '''It's morning, switch off'''
       logging.debug("It's morning, switch off")
       return False
    # it's 22:00
    # dawn: 05:00
    # sunset: 21:00
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
            #is_dark = check_if_dark()
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
