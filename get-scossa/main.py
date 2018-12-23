from gpiozero import LightSensor
from influxdb import InfluxDBClient
import time,datetime

'''ldr IO number and sensitivity'''
ldr = LightSensor(4,1)

'''initial var'''
now = datetime.datetime.now()
influxdb_user = 'pippo'
influxdb_password = 'pippopassword'
influxdb_db = 'SCOSSA'
influxdb_host = 'localhost'
influxdb_port = 8086
influxdbclient = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_db)


'''functions'''
def ldr_get():
    ldr.wait_for_light()
    '''sleep a bit for not getting again the same pulse'''
    time.sleep(0.5)
    return True

def insert_influxdb_row():
    now = datetime.datetime.now()
    '''json_body template'''
    json_body = [
            {
                "measurement": "scossa_led",
                "tags": {
                    "host": "rpi2"
                    },
                "time": now,
                "fields": {
                    "value": 1
                    }
                }
            ]
    influxdbclient.write_points(json_body)


def main():
    while True:
        ldr_get()
        insert_influxdb_row()

if __name__ == "__main__":
    main()
