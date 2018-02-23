#!/usr/bin/env python3

import json
import sys
import os
import urllib.request
from datetime import datetime

from PyCCMiner import Client


#Define Functions


#[Telegraf script] collecting data in influx.

#Thread: Monitor
# Loop
#  Check temperature (temp limit in config)
#  Check Fan speed
#  Heuristic curve for fan speed vs temperature
#


#Load Config
cfgfile='config.json'
config=json.loads(open(cfgfile).read())

#Get config values
min_prft=config["min_profit"]
pmnt_addr=config["pmnt_addr"]
miner_name=config["miner_name"]
switch_threshold=config["switch_threshold"]
algos=config["algorithms"]

#Set up logging
loglevels={"debug":5,"info":4,"warn":3,"error":2,"fatal":1,"off":0}
loglevel=loglevels[config["loglevel"]]
logfile=config["logfile"]

c = Client()
c.Connect(c="summary")

