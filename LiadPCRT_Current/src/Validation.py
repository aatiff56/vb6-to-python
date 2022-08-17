from datetime import datetime

import enum
import MdlADOFunctions
import MdlGlobal
import MdlConnection

class ValidationObjectOption(enum.Enum):
    Non = 0
    Josh = 1
    Job = 2
    MachineObj = 3
    ControlParam = 4

class ValidationTypeOption(enum.Enum):
    Min = 1
    Max = 2
    Sum = 3
    Avg = 4
    Count = 5
    Between = 6
    Equals = 7
    NonEquals = 8

class ValidationTiming(enum.Enum):
    EndOfJosh = 1
    EndOfJob = 2
    StartOfJosh = 3
    StartOfJob = 4


class Validation:
    mID = 0
    mSourceObject = None
    mSourceObjectType = ValidationObjectOption
    mSourceFieldName = ''
    mSourceDefaultValue = ''
    mValidationType = ValidationTypeOption
    mValidationObjectType = ValidationObjectOption
    mValidationObject = None
    mValidationFieldName = ''
    mValidationConstantValue = ''
    mDestinationObject = None
    mDestinationObjectType = ValidationObjectOption
    mDestinationFieldName = ''
    mDestinationDefaultValue = ''
    mIsCritical = False
    mMachine = None
    mValidationTiming = ValidationTiming
    mSequence = 0

    def Init(self, pMachine, pid):
        strSQL = ''
        RstCursor = None
        tDestinationObject = None
        tSourceObject = None

        try:
            self.Machine = pMachine
            strSQL = 'SELECT * FROM TblValidations WHERE ID = ' + str(pid)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.ID = pid
                self.Sequence = MdlADOFunctions.fGetRstValLong(RstData.Sequence)
                self.SourceObjectType = MdlADOFunctions.fGetRstValLong(RstData.SourceObjectType)
                self.SourceFieldName = MdlADOFunctions.fGetRstValString(RstData.SourceFieldName)
                self.SourceDefaultValue = MdlADOFunctions.fGetRstValString(RstData.SourceDefaultValue)
                self.ValidationTiming = MdlADOFunctions.fGetRstValLong(RstData.ValidationTiming)
                self.ValidationType = MdlADOFunctions.fGetRstValLong(RstData.ValidationType)
                self.ValidationObjectType = MdlADOFunctions.fGetRstValLong(RstData.ValidationObjectType)
                self.ValidationFieldName = MdlADOFunctions.fGetRstValString(RstData.ValidationFieldName)
                self.ValidationConstantValue = MdlADOFunctions.fGetRstValString(RstData.ValidationConstantValue)
                self.DestinationObjectType = MdlADOFunctions.fGetRstValLong(RstData.DestinationObjectType)
                self.DestinationFieldName = MdlADOFunctions.fGetRstValString(RstData.DestinationFieldName)
                self.DestinationDefaultValue = MdlADOFunctions.fGetRstValString(RstData.DestinationDefaultValue)
                self.IsCritical = MdlADOFunctions.fGetRstValBool(RstData.IsCritical, False)

            RstCursor.close()
            RstCursor = None

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

            MdlGlobal.RecordError(type(self) + ".Init:", str(0), error.args[0], "ValidationID:" + str(pid) + ". Machine: " + str(pMachine.ID))

    def PrepareObjects(self, pJob=None, pJosh=None):
        tJob = None
        tJosh = None
        tMachine = None

        try:
            if (self.SourceObjectType == ValidationObjectOption.Job):
                if pJob is None:
                    self.SourceObject = self.Machine.ActiveJob
                else:
                    self.SourceObject = pJob
            elif (self.SourceObjectType == ValidationObjectOption.Josh):
                if pJosh is None:
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
                        pass

                elif (self.DestinationObjectType == ValidationObjectOption.MachineObj):
                    if (self.SourceObjectType == ValidationObjectOption.Job):
                        tJob = self.SourceObject
                        self.DestinationObject = tJob.Machine
                    elif (self.SourceObjectType == ValidationObjectOption.Josh):
                        tJosh = self.SourceObject
                        self.DestinationObject = tJosh.Machine

        except BaseException as error:
            MdlGlobal.RecordError(type(self) + ".PrepareObjects:", str(0), error.args[0], "ValidationID:" + str(self.ID) + ". Machine: " + str(self.Machine.ID))

    def Validate(self, pJob=None, pJosh=None):
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

            tSourceValue = MdlADOFunctions.fGetRstValDouble(CallByName(
                self.SourceObject, self.SourceFieldName, VbGet))

            if self.ValidationObjectType != None:
                tValidationValue = MdlADOFunctions.fGetRstValDouble(CallByName(
                    self.ValidationObject, self.ValidationFieldName, VbGet))
            else:
                tValidationValue = MdlADOFunctions.fGetRstValDouble(
                    self.ValidationConstantValue)
            if (self.ValidationType == ValidationTypeOption.Min):
                if tSourceValue >= tValidationValue:
                    fn_return_value = True
            elif (self.ValidationType == ValidationTypeOption.Max):
                if tSourceValue <= tValidationValue:
                    fn_return_value = True
            elif (self.ValidationType == ValidationTypeOption.Sum):
                pass
            elif (self.ValidationType == ValidationTypeOption.Avg):
                pass
            elif (self.ValidationType == ValidationTypeOption.Count):
                pass
            elif (self.ValidationType == ValidationTypeOption.Between):
                pass
            elif (self.ValidationType == ValidationTypeOption.Equals):
                if tSourceValue == tValidationValue:
                    fn_return_value = True
            elif (self.ValidationType == ValidationTypeOption.NonEquals):
                if tSourceValue != tValidationValue:
                    fn_return_value = True
            if self.Validate() == False:
                if self.SourceDefaultValue != '':
                    tSourcePreviousValue = MdlADOFunctions.fGetRstValString(
                        CallByName(self.SourceObject, self.SourceFieldName, VbGet))
                    tArgs = vbObjectInitialize((0,), Variant)
                    if UCase(self.SourceDefaultValue) == 'NULL':
                        tArgs[0] = int(- 999999999)
                    else:
                        tArgs[0] = int(self.SourceDefaultValue)
                    tSourceNewValue = MdlADOFunctions.fGetRstValString(tArgs(0))
                    CallByName(self.SourceObject,
                               self.SourceFieldName, VbLet, int(tArgs(0)))
                if self.DestinationObjectType != None:
                    if self.DestinationDefaultValue != '':
                        tDestinationPreviousValue = MdlADOFunctions.fGetRstValString(
                            CallByName(self.DestinationObject, self.DestinationFieldName, VbGet))
                        tArgs = vbObjectInitialize((0,), Variant)
                        if UCase(self.DestinationDefaultValue) == 'NULL':
                            tArgs[0] = int(- 999999999)
                        else:
                            tArgs[0] = int(self.DestinationDefaultValue)
                        tDestinationNewValue = MdlADOFunctions.fGetRstValString(CallByName(
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
            pass

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
