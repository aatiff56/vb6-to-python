from Common import MdlADOFunctions as adoFunc
from LiadPCUnite.Global import Logs
from numpy import ndarray


class ValidateValue:
    logger = Logs.Logger()
    mArrValues = []
    mLastValidationPast = False
    mControllerID = 0
    mID = 0

    def Init(self, pParam):
        try:
            i = 0
            if not pParam is None:
                self.mID = pParam.ID
                self.mControllerID = pParam.pMachine.ControllerID

                self.mArrValues = ndarray((5,), object)
                for i in range(0, len(self.mArrValues)):
                    self.mArrValues[i] = 0
                self.mLastValidationPast = True
        except BaseException as error:
            self.logger.Error(error)

    def AddValue(self, pValue):
        try:
            i = 0
            for i in range(0, len(self.mArrValues)):
                if i == len(self.mArrValues):
                    self.mArrValues[i] = pValue
                else:
                    self.mArrValues[i] = self.mArrValues(i + 1)
        except BaseException as error:
            self.logger.Error(error)

    def CheckValues(self, pParam):
        try:
            i = 0
            j = 0
            tValidCounter = 0
            tValuesDiff = 0
            tTempArr = []
            tValidCounter = 0

            for i in range(0, len(self.mArrValues)):
                if self.mArrValues(i) > 0:
                    tValidCounter = tValidCounter + 1

            if tValidCounter >= 3:

                tTempArr = ndarray((tValidCounter - 1,), object)
                for i in range(0, len(self.mArrValues)):
                    if self.mArrValues(i) > 0:
                        tTempArr[j] = self.mArrValues(i)
                        j = j + 1
                tValidCounter = 0
                for i in range(1, len(tTempArr)):
                    if tTempArr(i) > 0:
                        if tTempArr(i) > tTempArr(i - 1):
                            tValidCounter = tValidCounter + 1
                        else:
                            tValidCounter = 0
                            break
                if tValidCounter > 0:

                    if adoFunc.fGetRstValDouble(pParam.LastValue) > adoFunc.fGetRstValDouble(pParam.LastValidValue):
                        tValuesDiff = adoFunc.fGetRstValDouble(
                            pParam.LastValue) - adoFunc.fGetRstValDouble(pParam.LastValidValue)
                        self.LastValidationPast = True
                    else:
                        if self.mArrValues(len(self.mArrValues)) == 0:

                            tValuesDiff = 0
                            self.LastValidationPast = False
                        else:
                            tValuesDiff = abs(self.mArrValues(
                                len(self.mArrValues)) - self.mArrValues(0))

                            self.LastValidationPast = True
                else:
                    self.LastValidationPast = False
            else:
                self.LastValidationPast = False
            if self.LastValidationPast == True:
                fn_return_value = tValuesDiff
            return fn_return_value
        except BaseException as error:
            self.logger.Error(error)

    def setArrValues(self, value):
        self.mArrValues = value

    def getArrValues(self):
        fn_return_value = self.mArrValues
        return fn_return_value
    ArrValues = property(fset=setArrValues, fget=getArrValues)

    def setLastValidationPast(self, value):
        self.mLastValidationPast = value

    def getLastValidationPast(self):
        fn_return_value = self.mLastValidationPast
        return fn_return_value
    LastValidationPast = property(
        fset=setLastValidationPast, fget=getLastValidationPast)

    def setControllerID(self, value):
        self.mControllerID = value

    def getControllerID(self):
        fn_return_value = self.mControllerID
        return fn_return_value
    ControllerID = property(fset=setControllerID, fget=getControllerID)

    def setID(self, value):
        self.mID = value

    def getID(self):
        fn_return_value = self.mID
        return fn_return_value
    ID = property(fset=setID, fget=getID)
