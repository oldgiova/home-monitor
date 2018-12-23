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

```


