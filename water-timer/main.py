import RPi.GPIO as GPIO
from itertools import repeat
from datetime import datetime,time
from time import sleep
from pytz import timezone
import logging,pdb, sys

'''initial var'''
RELAIS_4_GPIO = 22
water_time = 1800 #30 min
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

def water_status():
    pin_status = GPIO.input(RELAIS_4_GPIO)
    print('pin status: ', pin_status, type(pin_status))
    if pin_status == 1:
        logging.info('Water is OFF')
        print('Water is OFF')
    else:
        logging.info('Water is ON')
        print('Water is ON')
    return True

def main():
    logging.info('Starting up ')
    '''GPIO settings'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #GPIO.setup(RELAIS_4_GPIO, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(RELAIS_4_GPIO, GPIO.OUT)
    try: 
        '''main program'''
        water_on()
        water_status()
        for i in range(water_time):
            sleep(1)
        water_off()
        water_status()
        sys.exit()

    except KeyboardInterrupt:
        logging.info('shutting down for keyboard interrupt')
        water_off()
        water_status()

    except:
        logging.info('shutting down for other interrupt')
        water_off()
        water_status()
        #GPIO.cleanup()


if __name__ == "__main__":
    main()
