from abc import ABC, abstractmethod

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

    def __init__(self):        
        #self.poolName = poolname
        super().__init__()

    #"""Return a list of Exchange Rate information"""
    @abstractmethod
    def getExrates(self)       
        pass
