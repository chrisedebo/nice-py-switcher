#!/usr/bin/env python3

import json
import sys
import os
import urllib.request
import time

#Nicehash Algorithm Index list (order from https://www.nicehash.com/doc-api)
NHAlgoList=['Scrypt','SHA256','ScryptNf','X11','X13','Keccak','X15','Nist5','NeoScrypt', \
    'Lyra2RE','WhirlpoolX','Qubit','Quark','Axiom','Lyra2REv2','ScryptJaneNf16', \
    'Blake256r8','Blake256r14','Blake256r8vnl','Hodl','DaggerHashimoto','Decred', \
    'CryptoNight','Lbry','Equihash','Pascal','X11Gost','Sia','Blake2s','Skunk']

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

def getearnings(earningurl):
    #TODO? get earnings from nicehash.
    earnings=json.loads(getjson(earningurl))["result"]["stats"]

    return earnings

#Get algorithm profit values
def printprofits(sma,exrate,algos):

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
        

def printearnings(stats,exrate):
    
    for n in range(0,len(stats)):
        earning=stats[n]
        unpaid=0.0
        #try:
        #Get performance and power stats
        algoidx=earning["algo"]
        algoname=NHAlgoList[algoidx]
        unpaid=float(earning["balance"])
        unpaidfiat=unpaid*exrate
        rejected=earning["rejected_speed"]
        accepted=earning["accepted_speed"]

        influxline="earnings,miner={},currency={},algo={} unpaid={},rejected={},accepted={}"
        #Earnings in fiat
        print(influxline.format(miner_name,fiat,algoname,unpaidfiat,rejected,accepted))
        #Earnings in BTC
        print(influxline.format(miner_name,"BTC",algoname,unpaid,rejected,accepted))

        #except:
        #    pass

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
earningurl=config["earningurl"]

#Set up logging
loglevels={"debug":5,"info":4,"warn":3,"error":2,"fatal":1,"off":0}
loglevel=loglevels[config["loglevel"]]
logfile=config["logfile"]

#Get simple multi algo switching data and exchange rate
sma=getsmaratios(smaurl)
exrate=getexrate(exrateurl,fiat)

#Print influxline for exchangerate
influxline="exchangerates,crypto={},fiat={} fiattocrypto={},cryptotofiat={}"
print(influxline.format("BTC",fiat,exrate,1/exrate))

#Print potential earning stats value for each algorithm
printprofits(sma,exrate,algos)

# We can't be sure when telelgraf will actually execute the script
# just that we are told it will be "every 10 seconds". In order
# to only check earnings every 1 minute +/- 10 seconds, we need to
# divide unix timestamp by 10 to exclude the single digits
# Modulo with 6 (groups of 10 seconds) and therefore run every 1 minute (or so).
if (int(time.time()/10) % 6) == 0:
    earnings=getearnings(earningurl.replace('{ADDR}',pmnt_addr))
    printearnings(earnings,exrate)

