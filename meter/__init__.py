#Power meter.
from abc import ABC, abstractmethod

#Meter Base Typw
class MeterBase(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def getReading(self):
        pass


