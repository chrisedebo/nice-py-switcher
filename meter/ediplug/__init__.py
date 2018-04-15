from meter import MeterBase
    
from . import smartplug

class Ediplug(MeterBase):
    def __init__(self):
        self.EdiUser="admin"
        self.EdiPass="g1vemethekeys"
        self.EdiUrl="eddie.niceltowers.co.uk"

    def getReading(self):
        p = smartplug.SmartPlug(self.EdiUrl, (self.EdiUser,self.EdiPass))
        Reading = p.power
        Unit = "Watts"
        return Reading,Unit

