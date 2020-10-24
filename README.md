```
NEURIOAPIKEY - Neurio API Key
NEURIOSECRET - Neurio API Secret
INFLUXHOST - influxdb host
INFLUXPORT - influxdb port
INFLUXDB -   influxdb database
POLL_INTERVAL - # seconds between API connections
```

```
docker run -d -e -e NEURIO_ADDR=<ip> --restart=always --name neurio thecase/neurio-influx
```
