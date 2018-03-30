#Wallet Base Class
from abc import ABC, abstractmethod

#Algorithm base type
class Algo:

    def __init__(self,  publicName, currency, profitRatio):
        self.currency = currency
        self.publicName =  publicName
  
#Wallet plugins must implement these things.
class WalletBase(ABC):

    def __init__(self):        
        super().__init__()

    #"""Return a list of Algo information"""
    @abstractmethod
    def getBalance(self):       
        pass



