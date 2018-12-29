from sense_hat import SenseHat
import time,datetime,logging,subprocess
import ipdb
from influxdb import InfluxDBClient

'''initial var'''
sleeptime = 60
now = datetime.datetime.now()
influxdb_user = 'pippo'
influxdb_password = 'pippopassword'
influxdb_db = 'TEMPERATURE'
influxdb_host = 'rpi2'
influxdb_port = 8086
influxdbclient = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_db)

'''logging config'''
logging.basicConfig(
        level=logging.WARNING,
        filename='humidity.log',
        format='[%(asctime)s] %(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

'''functions'''
def read_sense_temp(sense):
    humidity = sense.get_humidity()
    return humidity

def insert_influxdb_row(humidity):
    utcnow = datetime.datetime.utcnow()
    '''json_body template'''
    json_body = [
            {
                "measurement": "umidita",
                "tags": {
                    "host": "rpi3"
                    },
                "time": utcnow,
                "fields": {
                    "value": humidity
                    }
                }
            ]
    logging.debug('writing a value to influxdb with humidity ', humidity)
    influxdbclient.write_points(json_body)


def main():
    sense = SenseHat()
    while True:
        humidity = read_sense_temp(sense)
        insert_influxdb_row(humidity)
        time.sleep(sleeptime)


if __name__ == "__main__":
    main()
