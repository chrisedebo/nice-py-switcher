#Power meter.
from abc import ABC, abstractmethod

#Meter Base Typw
class MeterBase(ABC):

    def __init__(self):
        self.reading = reading
        self.unit = unit
        super().__init__()

    @abstractmethod
    def getReading(self):
        pass


