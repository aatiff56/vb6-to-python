import enum
import MdlADOFunctions
import MdlConnection


class ControllerFieldAction:

    class ControllerFieldActionTiming(enum.Enum):
        Pre = 0
        Post = 1


    class ControllerFieldActionType(enum.Enum):
        ReadData = 0
        WriteData = 1


    class ControllerFieldActionExecuteOption(enum.Enum):
        Always = 0
        RunIfValid = 1
        RunIfInvalid = 2

    __mTiming = ControllerFieldActionTiming
    __mSequence = 0
    __mParent = None
    __mRefControllerField = None
    __mActionType = ControllerFieldActionType
    __mWriteValue = ''
    __mIsValid = False
    __mExecuteOption = ControllerFieldActionExecuteOption
    __mValidValue = ''
    __mID = 0
    __mComparerTypeID = 0


    def Init(self, ControllerFieldActionID):
        strSQL = ''
        RstCursor = None
        tTiming = 0
        tExecuteOption = 0
        tActionType = 0
        tRefControllerFieldName = ''
        tRefControllerField = None
        
        try:
            strSQL = 'SELECT * From TblControllerFieldActions WHERE ID = ' + str(ControllerFieldActionID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.ID = MdlADOFunctions.fGetRstValLong(RstData.ID)
                self.Sequence = MdlADOFunctions.fGetRstValLong(RstData.Sequence)
                tTiming = MdlADOFunctions.fGetRstValLong(RstData.Timing)
                if (tTiming == 1):
                    self.Timing = self.Timing.Pre
                elif (tTiming == 2):
                    self.Timing = self.Timing.Post
                tActionType = MdlADOFunctions.fGetRstValLong(RstData.Type)
                if (tActionType == 1):
                    self.ActionType = self.ActionType.ReadData
                elif (tActionType == 2):
                    self.ActionType = self.ActionType.WriteData
                tExecuteOption = MdlADOFunctions.fGetRstValLong(RstData.ExecuteOption)
                if (tExecuteOption == 1):
                    self.ExecuteOption = self.ExecuteOption.Always
                elif (tExecuteOption == 2):
                    self.ExecuteOption = self.ExecuteOption.RunIfValid
                elif (tExecuteOption == 3):
                    self.ExecuteOption = self.ExecuteOption.RunIfInvalid
                if MdlADOFunctions.fGetRstValString(RstData.ValidValue) != '':
                    self.ValidValue = MdlADOFunctions.fGetRstValString(RstData.ValidValue)
                if MdlADOFunctions.fGetRstValString(RstData.WriteValue) != '':
                    self.WriteValue = MdlADOFunctions.fGetRstValString(RstData.WriteValue)
                tRefControllerFieldName = MdlADOFunctions.fGetRstValString(RstData.RefControllerFieldName)
                if tRefControllerFieldName != '':
                    if self.Parent.pMachine.GetParam(tRefControllerFieldName, tRefControllerField) == True:
                        self.RefControllerField = tRefControllerField
                self.ComparerTypeID = MdlADOFunctions.fGetRstValLong(RstData.ComparerTypeID)
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)

        RstCursor = None


    def Execute(self):
        try:
            if self.ExecuteOption == self.ExecuteOption.Always or ( self.ExecuteOption == self.ExecuteOption.RunIfInvalid and self.IsValid == False )  or ( self.ExecuteOption == RunIfValid and self.IsValid == True ):
                if (self.ActionType == self.ActionType.ReadData):
                    if not ( self.RefControllerField is None ) :
                        self.RefControllerField.GetListData()
                    else:
                        self.Parent.GetListData()
                elif (self.ActionType == self.ActionType.WriteData):
                    if not ( self.RefControllerField is None ) :
                        self.RefControllerField.LastValue = self.WriteValue
                    else:
                        self.Parent.LastValue = self.WriteValue
        except:
            pass


    def Validate(self):
        try:
            if self.ValidValue != '':            
                if (self.ComparerTypeID == 1):
                    if Right(self.Parent.OPCItem.ItemID, 7) == 'Boolean':
                        if bool(str(self.Parent.LastValue)) == bool(str(self.ValidValue)):
                            self.IsValid = True
                        else:
                            self.IsValid = False
                    else:
                        if MdlADOFunctions.fGetRstValString(self.Parent.LastValue) == self.ValidValue:
                            self.IsValid = True
                        else:
                            self.IsValid = False
                elif (self.ComparerTypeID == 2):
                    if str(self.Parent.LastValue).isnumeric() and str(self.ValidValue).isnumeric():
                        if MdlADOFunctions.fGetRstValDouble(self.Parent.LastValue) != MdlADOFunctions.fGetRstValDouble(self.ValidValue):
                            self.IsValid = True
                        else:
                            self.IsValid = False
                    else:
                        self.IsValid = False
                elif (self.ComparerTypeID == 3):
                    if str(self.Parent.LastValue).isnumeric() and str(self.ValidValue).isnumeric():
                        if MdlADOFunctions.fGetRstValDouble(self.Parent.LastValue) > MdlADOFunctions.fGetRstValDouble(self.ValidValue):
                            self.IsValid = True
                        else:
                            self.IsValid = False
                    else:
                        self.IsValid = False
                elif (self.ComparerTypeID == 4):
                    if str(self.Parent.LastValue).isnumeric() and str(self.ValidValue).isnumeric():
                        if MdlADOFunctions.fGetRstValDouble(self.Parent.LastValue) >= MdlADOFunctions.fGetRstValDouble(self.ValidValue):
                            self.IsValid = True
                        else:
                            self.IsValid = False
                    else:
                        self.IsValid = False
                elif (self.ComparerTypeID == 5):
                    if str(self.Parent.LastValue).isnumeric() and str(self.ValidValue).isnumeric():
                        if MdlADOFunctions.fGetRstValDouble(self.Parent.LastValue) < MdlADOFunctions.fGetRstValDouble(self.ValidValue):
                            self.IsValid = True
                        else:
                            self.IsValid = False
                    else:
                        self.IsValid = False
                elif (self.ComparerTypeID == 6):
                    if str(self.Parent.LastValue).isnumeric() and str(self.ValidValue).isnumeric():
                        if MdlADOFunctions.fGetRstValDouble(self.Parent.LastValue) <= MdlADOFunctions.fGetRstValDouble(self.ValidValue):
                            self.IsValid = True
                        else:
                            self.IsValid = False
                    else:
                        self.IsValid = False
            else:
                self.IsValid = True
            if self.IsValid == False:
                self.Parent.ActionsAreValid = self.IsValid

        except:
            pass


    def __del__(self):
        self.__mParent = None
        self.__mRefControllerField = None


    def setComparerTypeID(self, value):
        self.__mComparerTypeID = value

    def getComparerTypeID(self):
        returnVal = None
        returnVal = self.__mComparerTypeID
        return returnVal
    ComparerTypeID = property(fset=setComparerTypeID, fget=getComparerTypeID)


    def setTiming(self, value):
        self.__mTiming = value

    def getTiming(self):
        returnVal = None
        returnVal = self.__mTiming
        return returnVal
    Timing = property(fset=setTiming, fget=getTiming)


    def setSequence(self, value):
        self.__mSequence = value

    def getSequence(self):
        returnVal = None
        returnVal = self.__mSequence
        return returnVal
    Sequence = property(fset=setSequence, fget=getSequence)


    
    def setParent(self, value):
        self.__mParent = value

    def getParent(self):
        returnVal = None
        returnVal = self.__mParent
        return returnVal
    Parent = property(fset=setParent, fget=getParent)


    
    def setRefControllerField(self, value):
        self.__mRefControllerField = value

    def getRefControllerField(self):
        returnVal = None
        returnVal = self.__mRefControllerField
        return returnVal
    RefControllerField = property(fset=setRefControllerField, fget=getRefControllerField)


    def setWriteValue(self, value):
        self.__mWriteValue = value

    def getWriteValue(self):
        returnVal = None
        returnVal = self.__mWriteValue
        return returnVal
    WriteValue = property(fset=setWriteValue, fget=getWriteValue)


    def setIsValid(self, value):
        self.__mIsValid = value

    def getIsValid(self):
        returnVal = None
        returnVal = self.__mIsValid
        return returnVal
    IsValid = property(fset=setIsValid, fget=getIsValid)


    def setExecuteOption(self, value):
        self.__mExecuteOption = value

    def getExecuteOption(self):
        returnVal = None
        returnVal = self.__mExecuteOption
        return returnVal
    ExecuteOption = property(fset=setExecuteOption, fget=getExecuteOption)


    def setActionType(self, value):
        self.__mActionType = value

    def getActionType(self):
        returnVal = None
        returnVal = self.__mActionType
        return returnVal
    ActionType = property(fset=setActionType, fget=getActionType)


    def setValidValue(self, value):
        self.__mValidValue = value

    def getValidValue(self):
        returnVal = None
        returnVal = self.__mValidValue
        return returnVal
    ValidValue = property(fset=setValidValue, fget=getValidValue)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)

