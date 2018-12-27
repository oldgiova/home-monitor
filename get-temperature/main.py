from sense_hat import SenseHat
import time,datetime,logging,subprocess
import ipdb
from influxdb import InfluxDBClient

'''initial var'''
factor=1.356
difference=12
sleeptime=60
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
        filename='temperature.log',
        format='[%(asctime)s] %(levelname)s:%(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

'''functions'''
def read_sense_temp(sense):
    temp = sense.get_temperature()
    return temp

def read_cpu_temp():
    cpu_temp = subprocess.getoutput("vcgencmd measure_temp")
    #ipdb.set_trace()
    array = cpu_temp.split("=")
    array2 = array[1].split("'")
    cpu_tempc = float(array2[0])
    cpu_tempc = float("{0:.2f}".format(cpu_tempc))
    return cpu_tempc

def calculates_real_temp(temp, cpu_temp, factor, difference):
    #ipdb.set_trace()
    '''first try - trictly bounded to CPU temp'''
    #return temp - ((cpu_temp - temp)/factor)
    '''second try - simply temp difference'''
    return temp - difference

def insert_influxdb_row(temperature):
    utcnow = datetime.datetime.utcnow()
    '''json_body template'''
    json_body = [
            {
                "measurement": "temperatura",
                "tags": {
                    "host": "rpi3"
                    },
                "time": utcnow,
                "fields": {
                    "value": temperature
                    }
                }
            ]
    logging.debug('writing a value to influxdb with temperature ', temperature)
    influxdbclient.write_points(json_body)


def main():
    sense = SenseHat()
    while True:
        temp = read_sense_temp(sense)
        cpu_temp = read_cpu_temp()
        real_temp = calculates_real_temp(temp, cpu_temp, factor, difference)
        insert_influxdb_row(real_temp)
        time.sleep(sleeptime)


if __name__ == "__main__":
    main()
