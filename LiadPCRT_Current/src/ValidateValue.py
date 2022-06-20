import MdlADOFunctions
import MdlGlobal

class ValidateValue:

    __mArrValues = []
    __mLastValidationPast = False
    __mControllerID = 0
    __mID = 0

    def Init(self, pParam):
        i = 0
        try:
            if not pParam is None:
                self.__mID = pParam.ID
                self.__mControllerID = pParam.pMachine.ControllerID
                self.__mArrValues = [None, None, None, None, None]
                for i in range(0, len(self.__mArrValues)):
                    self.__mArrValues[i] = 0
                self.__mLastValidationPast = True
        
        except BaseException as error:
            MdlGlobal.RecordError(type(self) + '.Init:', 0, error.args[0], 'ControllerID: ' + str(self.__mControllerID) + '. ID: ' + str(self.__mID))

    def AddValue(self, pValue):
        i = 0

        try:
            #Enter new value in the end of the array.
            #Like queue, the first value is removed and all the values are moving in one position to the left.
            for i in range(0, len(self.__mArrValues)):
                if i == len(self.__mArrValues):
                    self.__mArrValues[i] = pValue
                else:
                    self.__mArrValues[i] = self.__mArrValues(i + 1)
        
        except BaseException as error:
            MdlGlobal.RecordError(type(self) + '.AddValue:', 0, error.args[0], 'ControllerID: ' + str(self.__mControllerID) + '. Value: ' + str(pValue) + '. ID: ' + str(self.__mID))

    def CheckValues(self, pParam):
        returnVal = None
        i = 0
        j = 0
        tValidCounter = 0
        tValuesDiff = 0
        tTempArr = []

        try:
            #This function check the values in the array for some conditions and returns the valid diff between the values.
            #Check the amount of the valid values
            for i in range(0, len(self.__mArrValues)):
                if self.__mArrValues(i) > 0:
                    tValidCounter = tValidCounter + 1
            #Start the tests on the array
            if tValidCounter >= 3:
                #Enter to new array only the valid values.
                tTempArr = vbObjectInitialize((tValidCounter - 1,), Variant)
                for i in range(0, len(self.__mArrValues)):
                    if self.__mArrValues(i) > 0:
                        tTempArr[j] = self.__mArrValues(i)
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
                    #Check 3 - If until now everything went fine,
                    #check that the last value that has been read is larger from the LastValidValue if so calc the diff between them,
                    #else, calc the diff between the first and the last values in the array.
                    if MdlADOFunctions.fGetRstValDouble(pParam.LastValue) > MdlADOFunctions.fGetRstValDouble(pParam.LastValidValue):
                        tValuesDiff = MdlADOFunctions.fGetRstValDouble(pParam.LastValue) - MdlADOFunctions.fGetRstValDouble(pParam.LastValidValue)
                        self.LastValidationPast = True
                    else:
                        if self.__mArrValues(len(self.__mArrValues)) == 0:
                            #If tTempArr(len(tTempArr)) = 0 Then
                            tValuesDiff = 0
                            self.LastValidationPast = False
                        else:
                            tValuesDiff = abs(self.__mArrValues(len(self.__mArrValues)) - self.__mArrValues(0))
                            #tValuesDiff = Abs(tTempArr(len(tTempArr)) - tTempArr(0))
                            self.LastValidationPast = True
                else:
                    self.LastValidationPast = False
            else:
                self.LastValidationPast = False
            if self.LastValidationPast == True:
                returnVal = tValuesDiff
    
        except BaseException as error:
            MdlGlobal.RecordError(type(self) + '.CheckValues:', 0, error.args[0], 'ControllerID: ' + str(self.ControllerID) + '. ID: ' + str(self.ID))

        return returnVal


    def setArrValues(self, value):
        self.__mArrValues = value

    def getArrValues(self):
        returnVal = None
        returnVal = self.__mArrValues
        return returnVal
    ArrValues = property(fset=setArrValues, fget=getArrValues)


    def setLastValidationPast(self, value):
        self.__mLastValidationPast = value

    def getLastValidationPast(self):
        returnVal = None
        returnVal = self.__mLastValidationPast
        return returnVal
    LastValidationPast = property(fset=setLastValidationPast, fget=getLastValidationPast)


    def setControllerID(self, value):
        self.__mControllerID = value

    def getControllerID(self):
        returnVal = None
        returnVal = self.__mControllerID
        return returnVal
    ControllerID = property(fset=setControllerID, fget=getControllerID)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)

