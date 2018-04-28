import json
import logging
import math
from common import web
from pool.poolBase import PoolBase, Algo

class Yiimp(PoolBase):
    def __init__(self, config):
        self.log = logging.getLogger(__name__)
        self.log.info("Creating Yiimp Pool: %s",config["name"])
#        self.log.debug("config: %s", config)
        self.apiUrl = config["apiUrl"]
        self.poolUrl = config["stratumUrl"]
        self.profitData = config["statsData"]
        self.currency = config["cryptoPaid"]        
        super().__init__(config)

    def getAlgos(self):
        algos=[]
        self.log.debug("Requesting json payload from: %s", self.apiUrl)
        rawJson = web.downloadString(self.apiUrl)
        #self.log.debug("raw json: %s",rawJson)
        statusData = json.loads(rawJson)
        self.log.debug("Received payload: %s algo(s)", len(statusData))
        entries =[]
        for n in statusData:            
            data = statusData[n]
            estimate = data[self.profitData]
            algoname = data["name"]            
            entries.append((algoname,estimate))
        return self.processAlgoList(entries, self.currency)

    def getAlgoConnection(self, algo):
        self.AlgoMap[algo]
        return
