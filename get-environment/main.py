import Adafruit_DHT
import time,datetime,logging,subprocess
import pdb
from influxdb import InfluxDBClient

'''initial var'''
sleeptime=60
now = datetime.datetime.now()
sensor = Adafruit_DHT.DHT11
pin = 3
influxdb_user = 'pippo'
influxdb_password = 'pippopassword'
influxdb_db = 'ENVIRONMENT'
influxdb_host = 'cortile'
influxdb_port = 8086
influxdbclient = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_db)

'''logging config'''
logging.basicConfig(
        level=logging.DEBUG,
        filename='temperature.log',
        format='[%(asctime)s] %(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

'''functions'''
def read_dht11():
    humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
    return humidity, temperature

def insert_influxdb_row(measurement,value):
    utcnow = datetime.datetime.utcnow()
    '''json_body template'''
    json_body = [
            {
                "measurement": measurement,
                "tags": {
                    "host": "cortile"
                    },
                "time": utcnow,
                "fields": {
                    "value": value
                    }
                }
            ]
    logging.debug('writing ' + measurement + ' value to influxdb with value ' + str(value))
    influxdbclient.write_points(json_body)


def main():
    logging.info('Starting up ')
    while True:
        #temp = read_sense_temp(sense)
        humidity, temperature = read_dht11()
        if humidity is not None and temperature is not None:
            logging.debug('Temp=' + str(temperature) + ' - Humidity=' + str(humidity))
            insert_influxdb_row('humidity', humidity)
            insert_influxdb_row('temperature', temperature)
        else:
            logging.warning('Failed to get reading. Try again!')

        time.sleep(sleeptime)


if __name__ == "__main__":
    main()
