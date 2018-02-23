#!/usr/bin/env python3

import json
import sys
import os
import urllib.request
from datetime import datetime

#Define Functions


#[Telegraf script] collecting data in influx.

#Thread: Check profitability from influx
# Loop
#  Check time elapsed vs mintime
#  If time elapsed < mintime
#   If current * switch threshold% < max profitability
#    Switch
#  Else
#   If current < max profitability 
#    Switch
#
#Thread: Start Miner and supervise
# Loop
#  Start most profitable miner
#  Sleep 30s
#  Check miner hashing
#   If not hashing
#    Restart miner at next location/next algo if all locations tried twice
#  Check Algorithm switch status
#   If not running most profitable
#    Stop running miner
#
#Thread: Monitor
# Loop
#  Check temperature (temp limit in config)
#  Check Fan speed
#  Heuristic curve for fan speed vs temperature
#
#Thread: Statistics collection
# Loop
#  Check stats and report to influxdb
#  profitiability and max other profitability (top algorithm if within min time and switch threshold, 2nd if not)
#  miner api: hashrate, power, difficulty, gpu usage, memory usage, clock frequencies, temperature, fan speed
#
#Thread: Tuning
# Monitor KHW from miner api
# Adjust GPU and MEM clocks
# Try to acheive best performance per watt.
#


#Load Config
cfgfile=sys.argv[1]
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



