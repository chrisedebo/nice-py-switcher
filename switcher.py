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

#Get algorithm pay ratios
def getsmaratios(smaurl):
    #Get nicehash simple multi algorigthm data
    sma=json.loads(getjson(smaurl))["result"]["simplemultialgo"]
    
    return sma

#Get Exghangerate Fiat/BTC
def getexrate(exrateurl,fiat):
    #Get coinbase exchangerate
    exrates=json.loads(getjson(exrateurl))
    exrate=float(exrates["data"]["rates"][fiat])
    if logenum >= 5:
        print(("exchange rate:{}").format(exrate))

    return exrate

#Get algorithm profit values
def getprofits(sma,exrate,algos):

    algoprofit={}
    for n in range(0,len(sma)):
        algo=sma[n]
        ghs=0.0
        kwh=0.0
        
        try:
            #Get performance and power stats
            ghs=algos[algo["name"]]["ghs"]
            kwh=algos[algo["name"]]["kwh"]
            
            #Get pay ratio
            paying=float(algo["paying"])
            
            #Calculate earnings, cost and profit
            incoming=float(ghs*paying*exrate)
            outgoing=float(kwh*24.0*pwr_cost)
            profit=incoming-outgoing

            name=algo["name"]
            algoprofit[name]=profit
            
            if logenum >= 5:
                rateformat="algo: {}, paying: {} BTC/GH/Day, in:€{}, out:€{}, net:€{}"
                print(rateformat.format(name,paying,incoming,outgoing,round(profit,2)))
            
            
        except:
            #if logenum >=1:
            #print(algo)
            pass
        
    return algoprofit

#Set up logging
loglevels={"debug":5,"info":4,"warn":3,"error":2,"fatal":1,"off":0}


#Get nicehash simple multi algorigthm data
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
fiat=config["fiat"]
min_prft=config["min_profit"]
pwr_cost=config["pwr_cost"]
pmnt_addr=config["pmnt_addr"]
miner_name=config["miner_name"]
switch_threshold=config["switch_threshold"]
algos=config["algorithms"]
exrateurl=config["exrateurl"]
smaurl=config["smaurl"]
loglevel=config["loglevel"]
logfile=config["logfile"]
logenum=loglevels[loglevel]

sma=getsmaratios(smaurl)
exrate=getexrate(exrateurl,fiat)
algoprofit=getprofits(sma,exrate,algos)

max_profit=0.0
max_profit_algo=""
for algo in algoprofit:
  print(algo)
  profit=(algoprofit[algo])
  if profit > max_profit:
    max_profit=profit
    max_profit_algo=algo

print(("{},{},{}").format(datetime.now(),max_profit_algo,max_profit))

