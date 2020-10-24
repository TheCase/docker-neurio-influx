#!/usr/bin/env python3

import os, time, sys
from datetime import datetime
import neurio
from pprint import pprint

from influxdb import InfluxDBClient

import logging
fmt="%(asctime)s - %(levelname)-s - %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)
log = logging.getLogger(__name__)

def init():
  client = InfluxDBClient(os.getenv('INFLUXHOST', 'localhost'),
                          os.getenv('INFLUXPORT', '8086'),
                          os.getenv('INFLUXUSER', 'admin'),
                          os.getenv('INFLUXPASS', 'admin'),
                          os.getenv('INFLUXDB',   'neurio')
                         )
  return client

def insert(client, value):
   json_body = [
      {
         "measurement": "wattage",
         "tags": { "channel": "CONSUMPTION"},
         "fields": {
            "value": float(value)
         }
      }
   ]
   client.write_points(json_body)

# init influx client
client = init()

# create databse if not created
dbname = os.getenv('INFLUXDB', 'neurio')
dblist = client.get_list_database()
log.info("Checking database")
if not any(d['name'] == dbname for d in dblist):
  log.info("Creating database")
  client.create_database(dbname)

key    = os.getenv("NEURIOAPIKEY")
secret = os.getenv("NEURIOSECRET")
tp = neurio.TokenProvider(key=key, secret=secret)
nc = neurio.Client(token_provider=tp)
user_info = nc.get_user_information()

sleep_interval = os.getenv('POLL_INTERVAL', 60)

# start loop
while True:
  value = nc.get_samples_live_last(sensor_id=user_info["locations"][0]["sensors"][0]["sensorId"])['consumptionPower']
  insert(client,value)
  log.info("{}|{}: {} W".format("wattage","CONSUMPTION",value))
  log.info("sleeping {} seconds.".format(sleep_interval))
  time.sleep(sleep_interval)
