import RPi.GPIO as GPIO
from influxdb import InfluxDBClient
from datetime import datetime,time
from time import sleep
import logging,pdb

'''initial var'''
RELAIS_4_GPIO = 2
'''hour to switch light off'''
off_time = time(23,59)
sleep_time = 1800
#influxdb_user = 'pippo'
#influxdb_password = 'pippopassword'
#influxdb_db = 'LIGHT'
#influxdb_host = 'localhost'
#influxdb_port = 8086
#influxdbclient = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_db)

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

def insert_influxdb_row():
    utcnow = datetime.datetime.utcnow()
    '''json_body template'''
    json_body = [
            {
                "measurement": "scossa_led",
                "tags": {
                    "host": "rpi2"
                    },
                "time": utcnow,
                "fields": {
                    "value": 1
                    }
                }
            ]
    logging.debug('writing a value to influxdb with time ', utcnow)
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



def main():
    logging.info('Starting up ')
    '''GPIO settings'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAIS_4_GPIO, GPIO.OUT, initial=GPIO.HIGH)
    try: 
        '''main program'''
        while True:
            is_dark = check_if_dark()
            if is_dark:
                light_on()
            else:
                light_off()
            sleep(sleep_time)

    except KeyboardInterrupt:
        logging.info('shutting down for keyboard interrupt')

    except:
        logging.info('shutting down for other interrupt')

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
