import json
import logging
import math
from common import web
from pool.poolBase import PoolBase, Algo, PoolCreationError

class Yiimp(PoolBase):
    def __init__(self, config):
        self.log = logging.getLogger(__name__)
        self.log.debug("Creating Yiimp Pool: %s",config["name"])
        try:
            self.apiUrl = config["apiUrl"]
            self.poolUrl = config["stratumUrl"]
            self.profitData = config["statsData"]
            self.paymentAddress = config["paymentAddr"]
        except KeyError as e:
            raise PoolCreationError("{} was not found in pool config".format(e))
        super().__init__(config)

    def getApiEntries(self):    
        self.log.debug("Requesting json payload from: %s", self.apiUrl)
        entries =[]
        try:
            rawJson = web.downloadString(self.apiUrl)
        
            statusData = json.loads(rawJson)
            self.log.debug("Received payload: %s algo(s)", len(statusData))
        
            try:
                for n in statusData:            
                    data = statusData[n]
                    estimate = data[self.profitData]
                    algoname = data["name"]
                    port  = data["port"]
                    entries.append({"algoName": algoname, "estimate": estimate, "port":port})
            except:
                self.log.exception("Unable to process JSON Data: %s", rawJson)
        except:
            self.log.exception("Unable to donwload data from: %s", self.apiUrl)



        return entries
    
    def createAlgoConnection(self, algo, apiName):
        url = self.poolurl.format(apiName, algo.port)
        username = self.paymentAddress
        password = "c={}".format(algo.currency)
        
        return AlgoConnection(url,username,password)
