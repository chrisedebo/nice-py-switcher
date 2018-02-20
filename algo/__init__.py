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
    #Common Algorithm Name, internal. Must be the same in all modules
    def AlgoName(self):
        return self.AlgoName

    @property
    #Common MinerName
    def MinerName(self):
        return self.MinerName

    @property
    #Hash rate in GH/s
    def GHS(self):
        return self.ghs

    @property
    #Rig power consumption in KW.
    def KW(self):
        return self.kw

    @property
    #gpu core clock speed
    def GpuClock(self):
        return self.gpuclock

    @property
    #gpu memory clock speed
    def MemClock(self):
        return self.memclock

    @property
    #per GPU Power Limit in KW
    def PowerLimit(self):
        return self.powerlimit

class Algo:
    def __init__(self,AlgoName,AlgoBenchmark,AlgoProfitGHSDay):
        self.AlgoName = AlgoName
        self.AlgoBenchmark = AlgoBenchmark
        self.AlgoProfiGHSDay = AlgoProfitGHSDay

    @property
    #Common Algorithm Name, internal. Must be the same in all modules
    def AlgoName(self):
        return self.AlgoName
    
    @property
    #AlgoBenchmark type
    def AlgoBenchmark(self):
        return self.AlgoBenchmark
    
    @property
    #AlgoProfitGHSDay type
    def AlgoProfitGHSDay(self):
        return self.AlgoProfitGHSDay
   
class AlgorithmMap:
    @property
    #Common Algorithm Name, internal. Must be the same in all modules
    def AlgoName(self):
        return self.AlgoName
    #AltAlgoName

class AlgoProfitGHSDay:
    @property
    #Common Algorithm Name, internal. Must be the same in all modules
    def AlgoName(self):
        return self.AlgoName
    
    @property
    #ProfitRatio in Cryptocurrency/GHS/Day
    def ProfitRatio(self):
        return self.ProfitRatio

    @property
    #Earning CryptoCurreny symbol
    def CryptoCurrency(self):
        return self.CryptoCurrenct

    @property
    #Pool URL
    def URL(self):
        return URL

    @property
    #Pool Username (Wallet Address and minername if applicable
    def Username(self):
        return self.Username

    @property
    #Pool Password (usually x or payment instruction for pool eg c=BTC
    def Password(self):
        return Password


