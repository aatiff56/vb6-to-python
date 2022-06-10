from Common import MdlADOFunctions as adoFunc
from LiadPCUnite.DataAccess import QueryExecutor as qe
from LiadPCUnite.BusinessLogic import SqlConnector as sc
from LiadPCUnite.Global import Logs
from datetime import datetime

class Validation:
    sqlCntr = sc.SqlConnector()
    logger = Logs.Logger()

    Non = 0
    Josh = 1
    Job = 2
    MachineObj = 3
    ControlParam = 4

    Min = 1
    Max = 2
    Sum = 3
    Avg = 4
    Count = 5
    Between = 6
    Equals = 7
    NonEquals = 8

    EndOfJosh = 1
    EndOfJob = 2
    StartOfJosh = 3
    StartOfJob = 4
    mID = 0
    mSourceObject = None
    mSourceObjectType = ValidationObjectOption()
    mSourceFieldName = ''
    mSourceDefaultValue = ''
    mValidationType = ValidationTypeOption()
    mValidationObjectType = ValidationObjectOption()
    mValidationObject = None
    mValidationFieldName = ''
    mValidationConstantValue = ''
    mDestinationObject = None
    mDestinationObjectType = ValidationObjectOption()
    mDestinationFieldName = ''
    mDestinationDefaultValue = ''
    mIsCritical = False
    mMachine = Machine()
    mValidationTiming = ValidationTiming()
    mSequence = 0

    def Init(self, pMachine, pid):
        try:
            strSQL = ''
            Rst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            tDestinationObject = None
            tSourceObject = None

            self.Machine = pMachine
            strSQL = 'SELECT * FROM TblValidations WHERE ID = ' + pid
            self.sqlCntr.OpenConnection()
            Rst.ActiveConnection = self.Non
            if Rst.RecordCount == 1:
                self.ID = pid
                self.Sequence = adoFunc.fGetRstValLong(
                    Rst.Fields("Sequence").Value)
                self.SourceObjectType = adoFunc.fGetRstValLong(
                    Rst.Fields("SourceObjectType").Value)
                self.SourceFieldName = adoFunc.fGetRstValString(
                    Rst.Fields("SourceFieldName").Value)
                self.SourceDefaultValue = adoFunc.fGetRstValString(
                    Rst.Fields("SourceDefaultValue").Value)
                self.ValidationTiming = adoFunc.fGetRstValLong(
                    Rst.Fields("ValidationTiming").Value)
                self.ValidationType = adoFunc.fGetRstValLong(
                    Rst.Fields("ValidationType").Value)
                self.ValidationObjectType = adoFunc.fGetRstValLong(
                    Rst.Fields("ValidationObjectType").Value)
                self.ValidationFieldName = adoFunc.fGetRstValString(
                    Rst.Fields("ValidationFieldName").Value)
                self.ValidationConstantValue = adoFunc.fGetRstValString(
                    Rst.Fields("ValidationConstantValue").Value)
                self.DestinationObjectType = adoFunc.fGetRstValLong(
                    Rst.Fields("DestinationObjectType").Value)
                self.DestinationFieldName = adoFunc.fGetRstValString(
                    Rst.Fields("DestinationFieldName").Value)
                self.DestinationDefaultValue = adoFunc.fGetRstValString(
                    Rst.Fields("DestinationDefaultValue").Value)
                self.IsCritical = adoFunc.fGetRstValBool(
                    Rst.Fields("IsCritical").Value, False)
            Rst.Close()
            Rst = self.Non
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)

    def PrepareObjects(self, pJob=Non, pJosh=Non):
        try:
            tJob = Job()
            tJosh = Josh()
            tMachine = self.Machine()

            if (self.SourceObjectType == ValidationObjectOption.Job):
                if IsMissing(pJob):
                    self.SourceObject = self.Machine.ActiveJob
                else:
                    self.SourceObject = pJob
            elif (self.SourceObjectType == ValidationObjectOption.Josh):
                if IsMissing(pJosh):
                    self.SourceObject = self.Machine.ActiveJob.ActiveJosh
                else:
                    self.SourceObject = pJosh
            elif (self.SourceObjectType == ValidationObjectOption.MachineObj):
                self.SourceObject = self.Machine
            if self.ValidationObjectType == None or self.ValidationObjectType == self.SourceObjectType:
                self.ValidationObject = self.SourceObject
            else:
                if (self.ValidationObjectType == ValidationObjectOption.Job):
                    if (self.SourceObjectType == ValidationObjectOption.Josh):
                        self.ValidationObject = self.SourceObject.Job
                    elif (self.SourceObjectType == ValidationObjectOption.MachineObj):
                        self.ValidationObject = self.SourceObject.Machine
                elif (self.ValidationObjectType == ValidationObjectOption.Josh):
                    if (self.SourceObjectType == ValidationObjectOption.Job):
                        self.ValidationObject = self.SourceObject.ActiveJosh
                    elif (self.SourceObjectType == ValidationObjectOption.MachineObj):
                        self.ValidationObject = self.SourceObject.Machine
                elif (self.ValidationObjectType == ValidationObjectOption.MachineObj):
                    if (self.SourceObjectType == ValidationObjectOption.Job):
                        self.ValidationObject = self.SourceObject.Machine
                    elif (self.SourceObjectType == ValidationObjectOption.Josh):
                        self.ValidationObject = self.SourceObject.Machine
            if self.DestinationObjectType == None or self.DestinationObjectType == self.SourceObjectType:
                if not self.SourceObject is None:
                    self.DestinationObject = self.SourceObject
            else:
                if (self.DestinationObjectType == ValidationObjectOption.Job):
                    if (self.SourceObjectType == ValidationObjectOption.Josh):
                        tJosh = self.SourceObject
                        self.DestinationObject = tJosh.Job
                    elif (self.SourceObjectType == ValidationObjectOption.MachineObj):
                        tMachine = self.SourceObject
                        self.DestinationObject = tMachine.ActiveJob
                elif (self.DestinationObjectType == ValidationObjectOption.Josh):
                    if (self.SourceObjectType == ValidationObjectOption.Job):
                        tJob = self.SourceObject
                        self.DestinationObject = tJob.ActiveJosh
                    elif (self.SourceObjectType == ValidationObjectOption.MachineObj):
                elif (self.DestinationObjectType == ValidationObjectOption.MachineObj):
                    if (self.SourceObjectType == ValidationObjectOption.Job):
                        tJob = self.SourceObject
                        self.DestinationObject = tJob.Machine
                    elif (self.SourceObjectType == ValidationObjectOption.Josh):
                        tJosh = self.SourceObject
                        self.DestinationObject = tJosh.Machine
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)

    def Validate(self, pJob=Non, pJosh=Non):
        try:
            tSourceValue = 0
            tValidationValue = 0
            tDestinationValue = 0
            tArgs = vbObjectInitialize(objtype=Variant)
            tObject = Object()
            tJosh = Josh()
            tSourcePreviousValue = ''
            tSourceNewValue = ''
            tDestinationPreviousValue = ''
            tDestinationNewValue = ''

            self.PrepareObjects(pJob, pJosh)
            fn_return_value = False

            tSourceValue = adoFunc.fGetRstValDouble(CallByName(
                self.SourceObject, self.SourceFieldName, VbGet))

            if self.ValidationObjectType != None:
                tValidationValue = adoFunc.fGetRstValDouble(CallByName(
                    self.ValidationObject, self.ValidationFieldName, VbGet))
            else:
                tValidationValue = adoFunc.fGetRstValDouble(
                    self.ValidationConstantValue)
            if (self.ValidationType == ValidationTypeOption.Min):
                if tSourceValue >= tValidationValue:
                    fn_return_value = True
            elif (self.ValidationType == ValidationTypeOption.Max):
                if tSourceValue <= tValidationValue:
                    fn_return_value = True
            elif (self.ValidationType == ValidationTypeOption.Sum):
            elif (self.ValidationType == ValidationTypeOption.Avg):
            elif (self.ValidationType == ValidationTypeOption.Count):
            elif (self.ValidationType == ValidationTypeOption.Between):
            elif (self.ValidationType == ValidationTypeOption.Equals):
                if tSourceValue == tValidationValue:
                    fn_return_value = True
            elif (self.ValidationType == ValidationTypeOption.NonEquals):
                if tSourceValue != tValidationValue:
                    fn_return_value = True
            if self.Validate() == False:
                if self.SourceDefaultValue != '':
                    tSourcePreviousValue = adoFunc.fGetRstValString(
                        CallByName(self.SourceObject, self.SourceFieldName, VbGet))
                    tArgs = vbObjectInitialize((0,), Variant)
                    if UCase(self.SourceDefaultValue) == 'NULL':
                        tArgs[0] = int(- 999999999)
                    else:
                        tArgs[0] = int(self.SourceDefaultValue)
                    tSourceNewValue = adoFunc.fGetRstValString(tArgs(0))
                    CallByName(self.SourceObject,
                               self.SourceFieldName, VbLet, int(tArgs(0)))
                if self.DestinationObjectType != None:
                    if self.DestinationDefaultValue != '':
                        tDestinationPreviousValue = adoFunc.fGetRstValString(
                            CallByName(self.DestinationObject, self.DestinationFieldName, VbGet))
                        tArgs = vbObjectInitialize((0,), Variant)
                        if UCase(self.DestinationDefaultValue) == 'NULL':
                            tArgs[0] = int(- 999999999)
                        else:
                            tArgs[0] = int(self.DestinationDefaultValue)
                        tDestinationNewValue = adoFunc.fGetRstValString(CallByName(
                            self.DestinationObject, self.DestinationFieldName, VbGet))
                        CallByName(self.DestinationObject,
                                   self.DestinationFieldName, VbLet, int(tArgs(0)))
                self.Log(tSourcePreviousValue, tSourceNewValue,
                         tDestinationPreviousValue, tDestinationNewValue)

            return fn_return_value
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)
            return fn_return_value

    def Log(self, pSourcePreviousValue, pSourceNewValue, pDestinationPreviousValue, pDestinationNewValue):
        try:
            tLog = ''
            tExistLog = ''

            if self.SourceDefaultValue != '':
                tLog = '[' + datetime.now() + '] ' + self.SourceFieldName + ': Previous Value: ' + \
                    pSourcePreviousValue + '. New Value: ' + pSourceNewValue + vbCrLf
            if self.DestinationDefaultValue != '':
                tLog = tLog + '[' + datetime.now() + '] ' + self.DestinationFieldName + ': Previous Value: ' + \
                    pDestinationPreviousValue + '. New Value: ' + pDestinationNewValue + vbCrLf
            if self.SourceObjectType == Josh or self.SourceObjectType == Job:
                self.SourceObject.ValidationLog = self.SourceObject.ValidationLog + tLog
            if tLog != '':
                tExistLog = CallByName(
                    self.SourceObject, 'ValidationLog', VbGet)
                CallByName(self.SourceObject, 'ValidationLog',
                           VbLet, str(tExistLog + tLog))
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)

    def ListProperties(self, Obj):
        TLIApp = TLI.TLIApplication()
        InterfaceInfo = TLI.InterfaceInfo()
        ClassMembers = TLI.Members()
        MemberInfo = TLI.MemberInfo()
        TLIApp = TLIApplication()
        InterfaceInfo = TLIApp.InterfaceInfoFromObject(Obj)
        ClassMembers = InterfaceInfo.Members

        for MemberInfo in ClassMembers:
            if (MemberInfo.InvokeKind == TLI.INVOKE_CONST):
                pass
            elif (MemberInfo.InvokeKind == TLI.INVOKE_EVENTFUNC):
                pass
            elif (MemberInfo.InvokeKind == TLI.INVOKE_PROPERTYGET):
                self.logger.Debug(MemberInfo.Name + ' Property Get')
            elif (MemberInfo.InvokeKind == TLI.INVOKE_PROPERTYPUT):
                self.logger.Debug(MemberInfo.Name + ' Property Let')
            elif (MemberInfo.InvokeKind == TLI.INVOKE_PROPERTYPUTREF):
                self.logger.Debug(MemberInfo.Name + ' Property Set')
            elif (MemberInfo.InvokeKind == TLI.INVOKE_UNKNOWN):
                pass

    def __del__(self):
        try:
            self.mSourceObject = self.Non
            self.mValidationObject = self.Non
            self.mDestinationObject = self.Non
            self.mMachine = self.Non
            self.logger.Debug('Validation Destory ' + self.mID)
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)

    def setID(self, value):
        self.mID = value

    def getID(self):
        fn_return_value = self.mID
        return fn_return_value
    ID = property(fset=setID, fget=getID)

    def setSourceObject(self, value):
        self.mSourceObject = value

    def getSourceObject(self):
        fn_return_value = self.mSourceObject
        return fn_return_value
    SourceObject = property(fset=setSourceObject, fget=getSourceObject)

    def setSourceObjectType(self, value):
        self.mSourceObjectType = value

    def getSourceObjectType(self):
        fn_return_value = self.mSourceObjectType
        return fn_return_value
    SourceObjectType = property(
        fset=setSourceObjectType, fget=getSourceObjectType)

    def setSourceFieldName(self, value):
        self.mSourceFieldName = value

    def getSourceFieldName(self):
        fn_return_value = self.mSourceFieldName
        return fn_return_value
    SourceFieldName = property(
        fset=setSourceFieldName, fget=getSourceFieldName)

    def setSourceDefaultValue(self, value):
        self.mSourceDefaultValue = value

    def getSourceDefaultValue(self):
        fn_return_value = self.mSourceDefaultValue
        return fn_return_value
    SourceDefaultValue = property(
        fset=setSourceDefaultValue, fget=getSourceDefaultValue)

    def setValidationType(self, value):
        self.mValidationType = value

    def getValidationType(self):
        fn_return_value = self.mValidationType
        return fn_return_value
    ValidationType = property(fset=setValidationType, fget=getValidationType)

    def setValidationObjectType(self, value):
        self.mValidationObjectType = value

    def getValidationObjectType(self):
        fn_return_value = self.mValidationObjectType
        return fn_return_value
    ValidationObjectType = property(
        fset=setValidationObjectType, fget=getValidationObjectType)

    def setValidationObject(self, value):
        self.mValidationObject = value

    def getValidationObject(self):
        fn_return_value = self.mValidationObject
        return fn_return_value
    ValidationObject = property(
        fset=setValidationObject, fget=getValidationObject)

    def setValidationFieldName(self, value):
        self.mValidationFieldName = value

    def getValidationFieldName(self):
        fn_return_value = self.mValidationFieldName
        return fn_return_value
    ValidationFieldName = property(
        fset=setValidationFieldName, fget=getValidationFieldName)

    def setValidationConstantValue(self, value):
        self.mValidationConstantValue = value

    def getValidationConstantValue(self):
        fn_return_value = self.mValidationConstantValue
        return fn_return_value
    ValidationConstantValue = property(
        fset=setValidationConstantValue, fget=getValidationConstantValue)

    def setDestinationObject(self, value):
        self.mDestinationObject = value

    def getDestinationObject(self):
        fn_return_value = self.mDestinationObject
        return fn_return_value
    DestinationObject = property(
        fset=setDestinationObject, fget=getDestinationObject)

    def setDestinationObjectType(self, value):
        self.mDestinationObjectType = value

    def getDestinationObjectType(self):
        fn_return_value = self.mDestinationObjectType
        return fn_return_value
    DestinationObjectType = property(
        fset=setDestinationObjectType, fget=getDestinationObjectType)

    def setDestinationFieldName(self, value):
        self.mDestinationFieldName = value

    def getDestinationFieldName(self):
        fn_return_value = self.mDestinationFieldName
        return fn_return_value
    DestinationFieldName = property(
        fset=setDestinationFieldName, fget=getDestinationFieldName)

    def setDestinationDefaultValue(self, value):
        self.mDestinationDefaultValue = value

    def getDestinationDefaultValue(self):
        fn_return_value = self.mDestinationDefaultValue
        return fn_return_value
    DestinationDefaultValue = property(
        fset=setDestinationDefaultValue, fget=getDestinationDefaultValue)

    def setIsCritical(self, value):
        self.mIsCritical = value

    def getIsCritical(self):
        fn_return_value = self.mIsCritical
        return fn_return_value
    IsCritical = property(fset=setIsCritical, fget=getIsCritical)

    def setMachine(self, value):
        self.mMachine = value

    def getMachine(self):
        fn_return_value = self.mMachine
        return fn_return_value
    Machine = property(fset=setMachine, fget=getMachine)

    def setSequence(self, value):
        self.mSequence = value

    def getSequence(self):
        fn_return_value = self.mSequence
        return fn_return_value
    Sequence = property(fset=setSequence, fget=getSequence)

    def setValidationTiming(self, value):
        self.mValidationTiming = value

    def getValidationTiming(self):
        fn_return_value = self.mValidationTiming
        return fn_return_value
    ValidationTiming = property(
        fset=setValidationTiming, fget=getValidationTiming)
