
from dateutil.parser import parse
import enum

LeaderSVR = None

class MaterialCalcObjectType(enum.Enum):
    FromJob = 0
    FromJosh = 1

class MaterialCalcStandardOption(enum.Enum):
    FromUnitsProducedOK = 0
    FromInjections = 1

class WareHouseLocationConsumptionMethod(enum.Enum):
    FIFO = 1
    LIFO = 2

class BatchAutoSubtractModeOption(enum.Enum):
    off = 0
    ByMinimumPercent = 1
    ByMinimumAmount = 2


def IsDate(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except BaseException as error:
        return False