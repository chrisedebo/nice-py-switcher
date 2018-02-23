from abc import ABC, abstractmethod


class AlgoBenchmark:
    #AlgoName
    #MinerName
    #GHS
    #KW
    #GpuClock
    #MemClock
    #PowerLimit

class Algo:
    #AlgoName
    #AlgoBenchmark
    #AlgoProfitGHSDay
   
class AlgorithmMap:
    #AlgoName
    #AltAlgoName

class AlgoProfitGHSDay:
    #AlgoName
    #ProfitRatio
    #CryptoCurreny
    #URL
    #Username
    #Password

class ExchangeRate:
    #BTC
    #CryptoCurrency




class PoolBase(ABC):

    def __init__(self, value):
        self.value = value
        super().__init__()

    @abc.abstractmethod
    def getAlgos(self):
        pass
    
    @property
    def URL(self):
        return self.url

    @property
    def Username(self):
        return self.Username

    @property
    def Password(self):
        return self.Password

    @property
    

class Bird(abc.ABC):
    @abc.abstractmethod
    def fly(self):
        pass
