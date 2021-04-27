#!/usr/bin/env python3

import os
import sys
import time
import re
from datetime import datetime, timedelta
import neurio
from influxdb import InfluxDBClient
import logging

fmt="%(asctime)s - %(levelname)-s - %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)
log = logging.getLogger(__name__)


def dbinit():
    dbname = os.getenv('INFLUXDB', 'neurio')
    client = InfluxDBClient(os.getenv('INFLUXHOST', 'localhost'),
                            os.getenv('INFLUXPORT', '8086'),
                            os.getenv('INFLUXUSER', 'admin'),
                            os.getenv('INFLUXPASS', 'admin'),
                            os.getenv('INFLUXDB',   'neurio')
    )
    try:
        dblist = client.get_list_database()
    except Exception as e:
        log.error(e)
        sys.exit()
    log.info("Checking database")
    if not any(d['name'] == dbname for d in dblist):
        log.info("DB '{}'not found.  Creating...".format(dbname))
        client.create_database(dbname)
    return client


def insert(client, value):
    json_body = [
        {
         "measurement": "wattage",
         "tags": { "channel": "CO  NSUMPTION"},
       "fields":   {
          "value":   float(value)
         }
      }
    ]
    client.write_points(json_body)

def ncinit():
    key    = os.getenv('NEURIOAPIKEY')
    secret = os.getenv('NEURIOSECRET')
    tp = neurio.TokenProvider(key=key, secret=secret)
    nc = neurio.Client(token_provider=tp)
    return nc

def info(action):
    global nc, sensor_id
    if action == 'user':
        while True:
            log.info('getting user_info from neurio api...')
            result = nc.get_user_information()
            if 'status' in result:
                if result['status'] == 429 and result['code'] == 'rate_limit_exceeding':
                    log.info(result)
                    pattern = "([0-9]+) milliseconds"
                    millis = re.search(pattern, result['message']).group(1)
                    wait = (int(millis) / 1000) + 1
                    log.warning("caught rate limit. Sleeping {} seconds for reset".format(wait))
                    time.sleep(wait)
                else:
                    log.info("got user_info...")
                    break
    if action == 'sample':
        try:
            result = nc.get_samples_live_last(sensor_id=sensor_id)['consumptionPower']
        except Exception as e:
            log.error(e)
            sys.exit(127)
    return result


# inits
dbc = dbinit()
nc = ncinit()

user_info = info('user')
sensor_id = user_info["locations"][0]["sensors"][0]["sensorId"]
log.info("got sensor id: {}".format(sensor_id))
sleep_interval = int(os.getenv('POLL_INTERVAL', 60))

# start loop
while True:
    value = info('sample')
    insert(dbc,value)
    log.info("{}|{}: {} W".format("wattage","CONSUMPTION",value))
    log.info("sleeping {} seconds.".format(sleep_interval))
    time.sleep(sleep_interval)
