from abc import ABC, abstractmethod
from common import commonConfig
import math
import logging

#Algorithm base type
class Algo:

    def __init__(self,  publicName, currency, profitRatio):
        self.currency = currency
        self.publicName =  publicName
        self.profitRatio = profitRatio
  

#Deets to connect
class AlgoConnection:
    
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password



#Pool plugins must implement these things.
class PoolBase(ABC):

    def __init__(self, config):        
        self.baselog = logging.getLogger(__name__)
        self.poolName = config["name"]
        algomap = config["algoMap"]
        self.baselog.debug("creating algo maps")
        self.AlgoMap = {}
        self.AlgoMapRev = {}
        self.AlgoAdjust = {}       
        cConfig = commonConfig()
        for am in algomap:            
            algoName = am[0]          
            if algoName not in cConfig.EnabledAlgos():
                self.baselog.warn("Not loading configuration for algo as it is not enabled: %s", algoName)
            else:
                apiName = am[1]
          
                try:
                    adjust = int(am[2])
                except IndexError:
                    adjust = 0            

                self.AlgoMap[algoName] = apiName
                self.AlgoMapRev[apiName] = algoName
                self.AlgoAdjust[apiName] = adjust
            
        self.baselog.debug("algo maps created")
        super().__init__()
    
    def processAlgoList(self, algos, currency):
#        self.baselog.debug("Processing algo list: %s", algos)
        results = []
        appended= []
        ignored = []
        errored = []
        for algo in algos:
                algoname = algo[0]
                estimate = float(algo[1])

                try:
                    algoCommonName = self.AlgoMapRev[algoname]
                except KeyError:                    
                    self.baselog.debug("Ignoring pool(%s) algo, no match in config: %s", self.PoolName(), algoname)
                    ignored.append(algoname)
                else:
                    try:
                        profitRatio = self.adjustEstimate(algoname, estimate)
                        results.append(Algo(algoCommonName, currency, profitRatio))
                        appended.append(algoCommonName)
                    except: 
                        self.baselog.exception("Exception appending algo: %s", algoname)
                        errored.append(algoCommonName)
                    else:
                        self.baselog.debug("Appending algo: %s",algoname)

        # If none appended, log it...
        if len(appended)==0: 
            self.baselog.warn("No Algoriths appended for %s", self.PoolName())
        else:
            self.baselog.info("Appended: %s", ", ".join(appended))

        #Log ignored and errored if we have them.
        if len(ignored) > 0: self.baselog.warn("Ignored from pool: %s", ", ".join(ignored))
        if len(errored) > 0: self.baselog.error("Errored: %s", ", ".join(errored))

        return results

    def adjustEstimate(self, algoname, estimate):
        factor = math.pow(10,self.AlgoAdjust[algoname])
        if factor != 1:
            self.baselog.debug("Adjusting: %s by factor %s", algoname, factor)
        return float(estimate * factor)

    #"""Return a list of Algo information"""
    @abstractmethod
    def getAlgos(self):       
        pass

    #"""Return the AlgoConnection for a given algorhyththsms"""
    @abstractmethod
    def getAlgoConnection(self,algo):
        pass
    
    def PoolName(self):
        return self.poolName

