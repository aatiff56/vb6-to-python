import MdlADOFunctions
import MdlGlobal
import MdlConnection

class RTWorkingEvent:
    __mID = 0
    __mEventGroup = 0
    __mEventID = 0
    __mTitle = ''
    __mDescr = ''
    __mEventTime = None
    __mEndTime = None
    __mDuration = 0.0
    __mMachineType = None
    __mMachine = None
    __mControllerID = 0
    __mJob = None
    __mDepartment = None
    __mShift = None
    __mStatus = 0
    __mProduct = None
    __mMold = None
    __mJosh = None
    __mPConfigParentID = 0
    __mPConfigID = 0
    __mPConfigRelation = 0
    __mPConfigPC = 0.0
    __mEffectiveDuration = 0.0
    __mEventDistributionID = 0
    __mDurationSec = 0.0

    def Init(self, pJob, pEventID):
        strSQL = ''
        RstCursor = None
        try:
            strSQL = 'SELECT * FROM TblWorkingEvents WHERE ID = ' + str(pEventID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.arraysize == 1:
                self.ID = pEventID
                self.ControllerID = MdlADOFunctions.fGetRstValLong(RstData.ControllerID)
                self.Job = pJob
                self.Department = pJob.Department
                self.EventTime = RstData.EventTime
                self.Josh = self.Job.ActiveJosh
                self.Product = pJob.Product
                self.Machine = pJob.Machine
                self.MachineType = pJob.MachineType
                self.Mold = pJob.Mold
                self.PConfigID = pJob.PConfigID
                self.PConfigParentID = pJob.PConfigParentID
                self.PConfigPC = pJob.PConfigPC
                self.PConfigRelation = pJob.PConfigRelation
                self.EventDistributionID = MdlADOFunctions.fGetRstValLong(RstData.EventDistributionID)
            RstCursor.Close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                    
                MdlGlobal.RecordError(type(self).__name__ + '.Init:', str(0), error.args[0], 'EventID:' + str(pEventID) + '. JobID: ' + str(pJob.ID))

        RstCursor = None

    
    
    def Create(self, pMachine, pEventDistributionID, pDescr, pJob, pFromNewShift=False):
        strSQL = ''
        RstCursor = None
        tNewEventID = 0
        tChildJob = self.Job()
        tVariant = None
        tEvent = RTWorkingEvent()
        
        strSQL = 'INSERT INTO TblWorkingEvents '
        strSQL = strSQL + '(ControllerID,'
        strSQL = strSQL + 'MachineID,'
        strSQL = strSQL + 'EventDistributionID,'
        strSQL = strSQL + 'Title,'
        strSQL = strSQL + 'MachineType,'
        strSQL = strSQL + 'JobID,'
        strSQL = strSQL + 'JoshID,'
        strSQL = strSQL + 'Department,'
        strSQL = strSQL + 'ShiftID,'
        strSQL = strSQL + 'MoldID,'
        strSQL = strSQL + 'ProductID,'
        strSQL = strSQL + 'EventTime,'
        strSQL = strSQL + 'PConfigID'
        if pMachine.ActiveJob.PConfigID != 0:
            strSQL = strSQL + ','
            strSQL = strSQL + 'PconfigParentID,'
            strSQL = strSQL + 'PConfigRelation,'
            strSQL = strSQL + 'PConfigPC'
        if pMachine.AlarmsOnCount > 0 and pEventDistributionID == 7:
            strSQL = strSQL + ','
            strSQL = strSQL + 'AlarmsParamsIDs,'
            strSQL = strSQL + 'AlarmsParamsLName,'
            strSQL = strSQL + 'AlarmsParamsEName'
        strSQL = strSQL + ')'
        strSQL = strSQL + ' VALUES '
        strSQL = strSQL + '('
        strSQL = strSQL + pMachine.ControllerID + ','
        strSQL = strSQL + pMachine.ID + ','
        strSQL = strSQL + pEventDistributionID + ','
        strSQL = strSQL + '\'' + pMachine.EName + ': ' + self.Descr + '\','
        strSQL = strSQL + pMachine.TypeId + ','
        strSQL = strSQL + str(pJob.ID) + ','
        strSQL = strSQL + pJob.ActiveJosh.ID + ','
        strSQL = strSQL + pJob.Department.ID + ','
        strSQL = strSQL + pJob.Machine.Server.CurrentShiftID + ','
        strSQL = strSQL + pJob.Mold.ID + ','
        strSQL = strSQL + pJob.Product.ID + ','
        
        strSQL = strSQL + '\'' + ShortDate(NowGMT(), True, True, True) + '\','
        strSQL = strSQL + pJob.PConfigID
        if pMachine.ActiveJob.PConfigID != 0:
            strSQL = strSQL + ','
            strSQL = strSQL + pJob.PConfigParentID + ','
            strSQL = strSQL + pJob.PConfigRelation + ','
            strSQL = strSQL + pJob.PConfigPC
        if pMachine.AlarmsOnCount > 0 and pEventDistributionID == 7:
            strSQL = strSQL + ','
            strSQL = strSQL + '\'' + self.GetAlarmsParamsIDs(pMachine.ActiveJob.OpenAlarms) + '\','
            strSQL = strSQL + 'N\'' + self.GetAlarmsParamsNames(pMachine, 'LName') + '\','
            strSQL = strSQL + 'N\'' + self.GetAlarmsParamsNames(pMachine, 'EName') + '\''
        strSQL = strSQL + ')'
        CN.Execute(strSQL)
        
        strSQL = 'SELECT TOP 1 ID FROM TblWorkingEvents Where JobID = ' + str(pJob.ID) + ' AND ShiftID = ' + pJob.Machine.Server.CurrentShiftID + ' AND EventDistributionID = ' + pEventDistributionID + ' ORDER BY ID DESC'
        RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        RstCursor.ActiveConnection = None

        if RstCursor.arraysize == 1:
            tNewEventID = RstData.ID
        RstCursor.Close()
        self.Init(pJob, tNewEventID)
        
        if not pFromNewShift:
            if pJob.PConfigID != 0 and pJob.IsPConfigMain == True:
                for tVariant in self.Job.PConfigJobs:
                    tChildJob = tVariant
                    tEvent = RTWorkingEvent()
                    tEvent.Create(pMachine, pEventDistributionID, pDescr, tChildJob)
                    tChildJob.OpenWorkingEvent = tEvent
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                CN.Close()
                CN.Open()
                MetaCn.Close()
                MetaCn.Open()

                
            if not pJob is None:
                MdlGlobal.RecordError(type(self).__name__ + '.Create:', str(0), error.args[0], 'JobID: ' + str(pJob.ID))
            
        RstCursor = None
        tChildJob = None
        tVariant = None
        tEvent = None

    def CalcEffective(self):
        
        self.EffectiveDuration = self.Duration * self.PConfigPC / 100
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcEffective:', str(0), error.args[0], 'EventID: ' + self.ID)


    def EndEvent(self):
        
        self.EndTime = NowGMT()
        self.Duration = DateDiff('n', self.EventTime, self.EndTime)
        self.DurationSec = DateDiff('s', self.EventTime, self.EndTime)
        self.EffectiveDuration = self.Duration *  ( self.Job.PConfigPC / 100 )
        
        if self.PConfigParentID != 0:
            self.Duration = 0
        self.Update
        
        
        
        
        
        
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.EndEvent:', str(0), error.args[0], 'EventID: ' + self.ID)


    def CloseAndCreateForNewShift(self, pNewShiftID):
        tEvent = RTWorkingEvent()
        
        
        self.EndEvent
        tEvent = Me
        self.EndTime = 0
        self.Duration = 0
        self.EffectiveDuration = 0
        
        self.Create(tEvent.Machine, tEvent.EventDistributionID, tEvent.Descr, self.Job, True)
        
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CloseAndCreateForNewShift:', str(0), error.args[0], 'EventID: ' + self.ID + '. New ShiftID: ' + pNewShiftID)

            
        tEvent = None

    def Update(self):
        strSQL = ''
        
        strSQL = 'UPDATE TblWorkingEvents'
        strSQL = strSQL + ' SET'
        strSQL = strSQL + ' Duration = ' + self.Duration
        strSQL = strSQL + ' ,DurationSec = ' + self.DurationSec
        strSQL = strSQL + ' ,EffectiveDuration = ' + self.EffectiveDuration
        if not self.Josh is None:
            strSQL = strSQL + ' ,JoshID = ' + self.Josh.ID
        if IsDate(self.EndTime) and CStr(self.EndTime) != '00:00:00':
            
            strSQL = strSQL + ' ,EndTime = \'' + ShortDate(self.EndTime, True, True, True) + '\''
        strSQL = strSQL + ' WHERE ID = ' + self.ID
        CN.Execute(strSQL)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                CN.Close()
                CN.Open()
                MetaCn.Close()
                MetaCn.Open()

                
            MdlGlobal.RecordError(type(self).__name__ + '.Update:', str(0), error.args[0], 'EventID: ' + self.ID)

            
        strSQL = vbNullString

    def Refresh(self, pEventDistributionID=0):
        
        try:
            if pEventDistributionID:
                self.EventDistributionID = pEventDistributionID
        except:
            pass


    def GetAlarmsParamsIDs(self, pAlarms):
        returnVal = None
        tAlarm = Alarm()

        tVariant = None

        tParamsIDs = ''

        FirstItem = Boolean()
        
        FirstItem = True
        tParamsIDs = ''
        for tVariant in pAlarms:
            tAlarm = tVariant
            if not FirstItem:
                tParamsIDs = tParamsIDs + ','
            tParamsIDs = tParamsIDs + CStr(tAlarm.ParamID)
            FirstItem = False
        returnVal = tParamsIDs
        if Err.Number != 0:

            returnVal = ''
        return returnVal

    def GetAlarmsParamsNames(self, pMachine, FieldName='LName'):
        returnVal = None
        tAlarm = Alarm()

        tVariant = None

        tParamsNames = ''

        FirstItem = Boolean()
        
        FirstItem = True
        tParamsNames = ''
        for tVariant in pMachine.ActiveJob.OpenAlarms:
            tAlarm = tVariant
            if not FirstItem:
                tParamsNames = tParamsNames + ','
            if UCase(FieldName) == 'ENAME':
                tParamsNames = tParamsNames + CStr(pMachine.CParams.Item(tAlarm.ParameterName).EName)
            else:
                tParamsNames = tParamsNames + CStr(pMachine.CParams.Item(tAlarm.ParameterName).LName)
            FirstItem = False
        returnVal = strFixBadChars(tParamsNames)
        if Err.Number != 0:

            
            returnVal = ''
        return returnVal

    def __del__(self):
        
        try:
            self.__mMachineType = None
            self.__mMachine = None
            self.__mJob = None
            self.__mDepartment = None
            self.__mShift = None
            self.__mMold = None
            self.__mProduct = None
            self.__mJosh = None
        
        except BaseException as error:
            MdlGlobal.RecordError('RTWorkingEvent Destroy ' + str(self.__mID), error.args[0], 'Error terminating class RTWorkingEvent', '')


    def setDurationSec(self, value):
        self.__mDurationSec = value

    def getDurationSec(self):
        returnVal = None
        returnVal = self.__mDurationSec
        return returnVal
    DurationSec = property(fset=setDurationSec, fget=getDurationSec)


    def setEventDistributionID(self, value):
        self.__mEventDistributionID = value

    def getEventDistributionID(self):
        returnVal = None
        returnVal = self.__mEventDistributionID
        return returnVal
    EventDistributionID = property(fset=setEventDistributionID, fget=getEventDistributionID)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    def setTitle(self, value):
        self.__mTitle = value

    def getTitle(self):
        returnVal = None
        returnVal = self.__mTitle
        return returnVal
    Title = property(fset=setTitle, fget=getTitle)


    def setDescr(self, value):
        self.__mDescr = value

    def getDescr(self):
        returnVal = None
        returnVal = self.__mDescr
        return returnVal
    Descr = property(fset=setDescr, fget=getDescr)


    def setEventTime(self, value):
        self.__mEventTime = value

    def getEventTime(self):
        returnVal = None
        returnVal = self.__mEventTime
        return returnVal
    EventTime = property(fset=setEventTime, fget=getEventTime)


    def setEndTime(self, value):
        self.__mEndTime = value

    def getEndTime(self):
        returnVal = None
        returnVal = self.__mEndTime
        return returnVal
    EndTime = property(fset=setEndTime, fget=getEndTime)


    def setDuration(self, value):
        self.__mDuration = value

    def getDuration(self):
        returnVal = None
        returnVal = self.__mDuration
        return returnVal
    Duration = property(fset=setDuration, fget=getDuration)


    
    def setMachineType(self, value):
        self.__mMachineType = value

    def getMachineType(self):
        returnVal = None
        returnVal = self.__mMachineType
        return returnVal
    MachineType = property(fset=setMachineType, fget=getMachineType)


    
    def setMachine(self, value):
        self.__mMachine = value

    def getMachine(self):
        returnVal = None
        returnVal = self.__mMachine
        return returnVal
    Machine = property(fset=setMachine, fget=getMachine)


    def setControllerID(self, value):
        self.__mControllerID = value

    def getControllerID(self):
        returnVal = None
        returnVal = self.__mControllerID
        return returnVal
    ControllerID = property(fset=setControllerID, fget=getControllerID)


    
    def setJob(self, value):
        self.__mJob = value

    def getJob(self):
        returnVal = None
        returnVal = self.__mJob
        return returnVal
    Job = property(fset=setJob, fget=getJob)


    
    def setDepartment(self, value):
        self.__mDepartment = value

    def getDepartment(self):
        returnVal = None
        returnVal = self.__mDepartment
        return returnVal
    Department = property(fset=setDepartment, fget=getDepartment)


    
    def setShift(self, value):
        self.__mShift = value

    def getShift(self):
        returnVal = None
        returnVal = self.__mShift
        return returnVal
    Shift = property(fset=setShift, fget=getShift)


    
    def setProduct(self, value):
        self.__mProduct = value

    def getProduct(self):
        returnVal = None
        returnVal = self.__mProduct
        return returnVal
    Product = property(fset=setProduct, fget=getProduct)


    
    def setMold(self, value):
        self.__mMold = value

    def getMold(self):
        returnVal = None
        returnVal = self.__mMold
        return returnVal
    Mold = property(fset=setMold, fget=getMold)


    
    def setJosh(self, value):
        self.__mJosh = value

    def getJosh(self):
        returnVal = None
        returnVal = self.__mJosh
        return returnVal
    Josh = property(fset=setJosh, fget=getJosh)


    def setPConfigParentID(self, value):
        self.__mPConfigParentID = value

    def getPConfigParentID(self):
        returnVal = None
        returnVal = self.__mPConfigParentID
        return returnVal
    PConfigParentID = property(fset=setPConfigParentID, fget=getPConfigParentID)


    def setPConfigID(self, value):
        self.__mPConfigID = value

    def getPConfigID(self):
        returnVal = None
        returnVal = self.__mPConfigID
        return returnVal
    PConfigID = property(fset=setPConfigID, fget=getPConfigID)


    def setPConfigRelation(self, value):
        self.__mPConfigRelation = value

    def getPConfigRelation(self):
        returnVal = None
        returnVal = self.__mPConfigRelation
        return returnVal
    PConfigRelation = property(fset=setPConfigRelation, fget=getPConfigRelation)


    def setPConfigPC(self, value):
        self.__mPConfigPC = value

    def getPConfigPC(self):
        returnVal = None
        returnVal = self.__mPConfigPC
        return returnVal
    PConfigPC = property(fset=setPConfigPC, fget=getPConfigPC)


    def setEffectiveDuration(self, value):
        self.__mEffectiveDuration = value

    def getEffectiveDuration(self):
        returnVal = None
        returnVal = self.__mEffectiveDuration
        return returnVal
    EffectiveDuration = property(fset=setEffectiveDuration, fget=getEffectiveDuration)
