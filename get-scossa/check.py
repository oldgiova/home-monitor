from influxdb import InfluxDBClient
import time,datetime

'''initial var'''
now = datetime.datetime.now()
influxdb_user = 'pippo'
influxdb_password = 'pippopassword'
influxdb_db = 'SCOSSA'
influxdb_host = 'localhost'
influxdb_port = 8086
influxdbclient = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_db)


'''functions'''
def query_influxdb():
    result = influxdbclient.query('select value from scossa_led;')
    print("Result: {0}".format(result))

def main():
    query_influxdb()

if __name__ == "__main__":
    main()
