# home-monitor
Home monitor projects composed of several tools and script for my home automation

----------------------
## Power LDR
scripts located on power-ldr directory
* setup influxdb
```
docker pull hypriot/rpi-influxdb
docker run -d --name=influxdb --volume=/home/nonno/docker/influxdb:/data -p8086:8086 hypriot/rpi-influxdb
```

```
docker exec -it influxdb /usr/bin/influx

Connected to http://localhost:8086 version 1.2.2
InfluxDB shell version: 1.2.2
> CREATE DATABASE SCOSSA
> SHOW DATABASES
name: databases
name
----
_internal
SCOSSA

> use SCOSSA
Using database SCOSSA
> CREATE USER pippo WITH PASSWORD 'ugopassword' WITH ALL PRIVILEGES
> GRANT ALL PRIVILEGES ON SCOSSA TO pippo

```

* start get-scossa with sudo:
```
nohup sudo python3 get-scossa/main.py &
```



