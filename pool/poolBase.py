from abc import ABC, abstractmethod
from common import commonConfig
import math
import logging

class PoolCreationError(Exception):
    pass

#Algorithm base type
class Algo:

    def __init__(self,  publicName, currency, profitRatio, port):
        self.currency = currency
        self.publicName =  publicName
        self.profitRatio = profitRatio
        self.port = port
  

#Deets to connect
class AlgoConnection:
    
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password


#Pool plugins must implement these things.
class PoolBase(ABC):

    def __init__(self, config):        
        try:
            self.baselog = logging.getLogger(__name__)
            self.processConfig(config, commonConfig())
            self.ProcessedAlgos = {}        
            self.LoadedProcessedAlgos = False
            super().__init__()
        except:
            raise PoolCreationException()

    # was thinking of making this cached, by providing proerties to access all the parts of config
    # and decorating with the @cahced_property value
    # but part of me things we still want to do it on construction of the object
    def processConfig(self, poolConfig, commonConfig):
        #Parse Config
        try:
            self.poolName = poolConfig["name"]
            algomap = poolConfig["algoMap"]
            self.baselog.info("Config parsed Successfully: %s",self.poolName)

            #Build Algorithm Map, Reverse Lookup Map and Adjustment map.
            self.AlgoMap = {}
            self.AlgoMapRev = {}

            for am in algomap:            
                #Internal Name
                algoName = am["name"]

                #Check to see if Algo is enabled, disabled or unspported
                if algoName in commonConfig.EnabledAlgos():
            
                    #Pool Name
                    apiName = am["apiName"]
          
                    try:
                        #Adjustment Factor
                        adjust = int(am["adjFactor"])
                    except KeyError:
                        #Set to 0 if not present in config
                        adjust = 0            
                
                    try: 
                        currency = am["cryptoPaid"]
                        self.baselog.debug("Currency Override: %s currency: %s",apiName, currency)
                    except KeyError:
                        currency = poolConfig["cryptoPaid"]
                    
                    self.AlgoMap[algoName] = { "apiName": apiName, "adjFactor": adjust, "currency": currency } 
                    self.AlgoMapRev[apiName] = algoName
                    self.baselog.debug("Mapped Algo: %s ApiName: %s Adjust Factor: %d Currency: %s",algoName,apiName,adjust,currency)
                else:
                    if algoName in commonConfig.DisabledAlgos():
                        self.baselog.warn("Unmapped Algo: %s Reason: disabled", algoName)
                    else:
                        self.baselog.error("Unmapped Algo: %s Reason: unsupported", algoName)
    
            #All done, log and get outta here.
            self.baselog.info("AlgoMap built for pool: %s Algos Mapped: %d",self.poolName,len(self.AlgoMap))

        except KeyError as e:
            self.baselog.exception("Unmapped Algo: %s Reason: Unable to locate required config '%s'", algoName, e.args[0])
            raise e

    def processAlgoList(self, algos):
        appended= []
        ignored = []
        errored = []
        for algo in algos:
            try:
                algoname = algo["algoName"]
                estimate = float(algo["estimate"])
                port = algo["port"]
            except KeyError as e:
                errored.append("Unknown Algo")
                self.baselog.exception("Unable to process algo: %s Missing Key '%s'",algo,e.args[0])
            else:
                try:
                    algoCommonName = self.AlgoMapRev[algoname]
                except KeyError:                    
                    self.baselog.debug("Ignoring pool(%s) algo, no match in config: %s", self.PoolName(), algoname)
                    ignored.append(algoname)
                else:
                    try:
                        profitRatio = self.adjustEstimate(algoname, estimate)
                        
                        currency = self.AlgoMap[algoCommonName]["currency"]

                        self.ProcessedAlgos[algoCommonName] = Algo(algoCommonName, currency, profitRatio, port)
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

    def adjustEstimate(self, algoname, estimate):
        algoCommonName = self.AlgoMapRev[algoname]
        factor = math.pow(10,self.AlgoMap[algoCommonName]["adjFactor"])
        if factor != 1:
            self.baselog.debug("Adjusting: %s by factor %s", algoname, factor)
        return float(estimate * factor)

    #"""Return a list of Algo information"""
    def getAlgos(self):       
        return self.getProcessedAlgos().values()

    #"""Return the AlgoConnection for a given algorhyththsms"""
    def getAlgoConnection(self,algoName):
        apiName = self.AlgoMapRev[algo]
        self.getProcessedAlgos()
        algo = self.ProcessedAlgos[algoName]
        return self.createAlgoConnection(algo, apiName)

    @abstractmethod
    def createAlgoConnection(self, algo, apiName):
        pass

    @abstractmethod
    def getApiEntries(self):
        pass


    def PoolName(self):
        return self.poolName

    def getProcessedAlgos(self):
        self.log.debug("Getting processed Algos")
        if not self.LoadedProcessedAlgos:
            self.LoadedProcessedAlgos = True
            self.log.debug("Requesting API data") 
            entries = self.getApiEntries()
            self.log.debug("Processing %d API entries", len(entries))
            self.processAlgoList(entries)
        return self.ProcessedAlgos
