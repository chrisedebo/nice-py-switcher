#!/usr/bin/env python3

import json
import sys
import os
import urllib.request
from datetime import datetime

#Define Functions

#Get JSON from URL
def getjson(url):
    with urllib.request.urlopen(url) as response:
        return response.read()

#TODO 
#Thread: Check profitability
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
#    Restart miner at next location/next algo if no more locations
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

#Load Config
cfgfile=sys.argv[1]
config=json.loads(open(cfgfile).read())

#Get config values
fiat=config["fiat"]
min_prft=config["min_profit"]
pwr_cost=config["pwr_cost"]
pmnt_addr=config["pmnt_addr"]
miner_name=config["miner_name"]
switch_threshold=config["switch_threshold"]
algos=config["algorithms"]

#Get nicehash simple multi algorigthm data
smaurl="https://api.nicehash.com/api?method=simplemultialgo.info"
sma=json.loads(getjson(smaurl))["result"]["simplemultialgo"]

#Get coinbase exchangerate
exrateurl="https://api.coinbase.com/v2/exchange-rates?currency=BTC"
exrates=json.loads(getjson(exrateurl))
print(exrates)
exrate=float(exrates["data"]["rates"][fiat])
print(("exchange rate:{}").format(exrate))

algoprofit={}
for n in range(0,len(sma)):
  algo=sma[n]
  ghs=0.0
  kwh=0.0
  
  try:
    ghs=algos[algo["name"]]["ghs"]
    kwh=algos[algo["name"]]["kwh"]

    paying=float(algo["paying"])
    name=algo["name"]
    incoming=float(ghs*paying*exrate)
    outgoing=float(kwh*24.0*pwr_cost)
    profit=incoming-outgoing
    print(("algo: {}, paying: {} BTC/GH/Day, in:€{}, out:€{}, net:€{}").format(name,paying,incoming,outgoing,round(profit,2)))

    algoprofit[name]=incoming-outgoing

  except:
    pass

max_profit=0.0
max_profit_algo=""
for algo in algoprofit:
  profit=(algoprofit[algo])
  if profit > max_profit:
    max_profit=profit
    max_profit_algo=algo

print(("{},{}").format(datetime.now(),max_profit))

