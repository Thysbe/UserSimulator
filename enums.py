from enum import Enum, IntEnum


class DegreeOfTracking(IntEnum):
    LOW = 1
    MID = 2
    HIGH = 3


class Levels(Enum):
    LOW = [True,False,False]
    MID = [False,True,False]
    HIGH = [False,False,True]

    def r_low(self):
        return self.LOW

    def r_mid(self):
        return self.MID

    def r_High(self):
        return self.HIGH
