from abc import ABC, abstractmethod

class AlgoBenchmark:
    def __init__(self,AlgoName,MinerName,GHS,KW,GpuClock,MemClock,PowerLimit):
        self.AlgoName = AlgoName
        self.MinerName = MinerName
        self.GHS = GHS
        self.KW = KW
        self.GpuClock = GpuClock
        self.MemClock = MemClock
        self.PowerLimit = PowerLimit
    
    @property
    def AlgoName(self):
        return self.AlgoName:
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


