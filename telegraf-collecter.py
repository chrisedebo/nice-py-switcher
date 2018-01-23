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
            inbtc=float(ghs*paying)
            outgoing=float(kwh*24.0*pwr_cost)
            outbtc=float(outgoing/exrate)
            profit=incoming-outgoing
            profitbtc=inbtc-outbtc
    
            name=algo["name"]
            algoprofit[name]=profit
            
            influxline="profit_stats,miner={},currency={},algo={} in={},out={},profit={}"
            #Profits in Fiat
            print(influxline.format(miner_name,fiat,name, \
                                        round(incoming,5), \
                                        round(outgoing,5), \
                                        round(profit,5) \
                                        ))
            #Profit in BTC
            print(influxline.format(miner_name,"BTC",name, \
                                        round(inbtc,5), \
                                        round(outbtc,5), \
                                        round(profitbtc,5) \
                                        ))
                
        except:
            pass
        
    return algoprofit

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

#Set up logging
loglevels={"debug":5,"info":4,"warn":3,"error":2,"fatal":1,"off":0}
loglevel=loglevels[config["loglevel"]]
logfile=config["logfile"]


sma=getsmaratios(smaurl)
exrate=getexrate(exrateurl,fiat)

influxline="exchangerates,crypto={},fiat={} fiattocrypto={},cryptotofiat={}"
print(influxline.format("BTC",fiat,exrate,1/exrate))

getprofits(sma,exrate,algos)
