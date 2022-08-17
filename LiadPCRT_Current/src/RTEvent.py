from datetime import datetime
import MdlADOFunctions
import MdlGlobal
import MdlConnection
import mdl_Common
import MdlUtilsH
import GlobalVariables

class RTEvent:
    __mID = 0
    __mEventGroup = 0
    __mEventID = 0
    __mTitle = ''
    __mDescr = ''
    __mEventTime = None
    __mEndTime = None
    __mDuration = 0.0
    __mDownTime = 0.0
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
    __mInActiveTime = 0.0
    __mPConfigParentID = 0
    __mPConfigID = 0
    __mPConfigRelation = 0
    __mPConfigPC = 0.0
    __mEffectiveDuration = 0.0
    __mEffectiveDownTime = 0.0
    __mEffectiveInActiveTime = 0.0
    __mIsCalendarEvent = False
    __mTechnicianUserID = 0
    __mRootEventID = 0
    __mIsShortEvent = False
    __mDurationSec = 0.0
    __mDownTimeSec = 0.0
    __mInActiveTimeSec = 0.0

    def Init(self, pJob, pEventID):
        strSQL = ''

        RstCursor = None
        try:        
            strSQL = 'SELECT * FROM TblEvent WHERE ID = ' + str(pEventID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.arraysize == 1:
                self.ID = pEventID
                self.ControllerID = MdlADOFunctions.fGetRstValLong(RstData.ControllerID)
                self.Job = pJob
                self.Department = pJob.Department
                self.EventTime = RstData.EventTime
                self.EventGroup = MdlADOFunctions.fGetRstValLong(RstData.EventGroup)
                self.EventID = MdlADOFunctions.fGetRstValLong(RstData.Event)
                self.Josh = self.Job.ActiveJosh
                self.IsCalendarEvent = False
                self.Product = pJob.Product
                self.Machine = pJob.Machine
                self.MachineType = pJob.MachineType
                self.Mold = pJob.Mold
                self.PConfigID = pJob.PConfigID
                self.PConfigParentID = pJob.PConfigParentID
                self.PConfigPC = pJob.PConfigPC
                self.PConfigRelation = pJob.PConfigRelation
                self.RootEventID = MdlADOFunctions.fGetRstValLong(RstData.RootEventID)
                self.IsShortEvent = MdlADOFunctions.fGetRstValBool(RstData.IsShortEvent, False)

            RstCursor.close()

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

    
    
    def Create(self, pMachine, pEventGroupID, pEventID, pDescr, pJob, pFromNewShift=False, pRootEventID=0, pEventTime=datetime.strptime('00:00:00', '%H:%M:%S')):
        strSQL = ''
        RstCursor = None
        tNewEventID = 0
        tChildJob = None
        tVariant = None
        tEvent = None
        EventGroupID = 0
        ActivateProductionMode = False
        ActivateProductionModeID = 0

        try:        
            if EventGroupID > 0:
                pEventGroupID = EventGroupID
            strSQL = 'INSERT INTO TblEvent '
            strSQL = strSQL + '(ControllerID,'
            strSQL = strSQL + 'MachineID,'
            strSQL = strSQL + 'EventGroup,'
            strSQL = strSQL + 'Event,'
            strSQL = strSQL + 'Title,'
            strSQL = strSQL + 'MachineType,'
            strSQL = strSQL + 'JobID,'
            strSQL = strSQL + 'JoshID,'
            strSQL = strSQL + 'Department,'
            strSQL = strSQL + 'ShiftID,'
            strSQL = strSQL + 'MoldID,'
            strSQL = strSQL + 'ProductID,'
            strSQL = strSQL + 'EventTime,'
            strSQL = strSQL + 'RootEventID,'
            strSQL = strSQL + 'PConfigID'
            if pMachine.ActiveJob.PConfigID != 0:
                strSQL = strSQL + ','
                strSQL = strSQL + 'PconfigParentID,'
                strSQL = strSQL + 'PConfigRelation,'
                strSQL = strSQL + 'PConfigPC'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + str(pMachine.ControllerID) + ','
            strSQL = strSQL + str(pMachine.ID) + ','
            strSQL = strSQL + str(pEventGroupID) + ','
            strSQL = strSQL + str(pEventID) + ','
            strSQL = strSQL + '\'' + str(pMachine.EName) + ': ' + str(self.Descr) + '\','
            strSQL = strSQL + str(pMachine.TypeId) + ','
            strSQL = strSQL + str(pJob.ID) + ','
            strSQL = strSQL + str(pJob.ActiveJosh.ID) + ','
            strSQL = strSQL + str(pJob.Department.ID) + ','
            strSQL = strSQL + str(pJob.Machine.Server.CurrentShiftID) + ','
            strSQL = strSQL + str(pJob.Mold.ID) + ','
            strSQL = strSQL + str(pJob.Product.ID) + ','
            
            if pEventTime > datetime.strptime('00:00:00', '%H:%M:%S'):
                strSQL = strSQL + '\'' + MdlUtilsH.ShortDate(pEventTime, True, True, True) + '\','
            else:
                strSQL = strSQL + '\'' + MdlUtilsH.ShortDate(mdl_Common.NowGMT(), True, True, True) + '\','
            strSQL = strSQL + str(pRootEventID) + ','
            strSQL = strSQL + str(pJob.PConfigID)
            if pMachine.ActiveJob.PConfigID != 0:
                strSQL = strSQL + ','
                strSQL = strSQL + str(pJob.PConfigParentID) + ','
                strSQL = strSQL + str(pJob.PConfigRelation) + ','
                strSQL = strSQL + str(pJob.PConfigPC)
            strSQL = strSQL + ')'
            MdlConnection.CN.execute(strSQL)
            
            strSQL = 'SELECT TOP 1 ID FROM TblEvent Where JobID = ' + str(pJob.ID) + ' AND ShiftID = ' + str(pJob.Machine.Server.CurrentShiftID) + ' AND Event = ' + str(pEventID) + ' ORDER BY ID DESC'
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.arraysize == 1:
                tNewEventID = RstData.ID
            RstCursor.close()
            self.Init(pJob, tNewEventID)
            
            if ( ( self.Machine.NewJob == False or ( self.Machine.NewJob == True and self.Machine.SetupEventIDOnSetupEnd == 2 ) ) and self.Machine.ProductionModeID == 1 ) or ( self.Machine.ProductionModeID > 1 and not self.Machine.ProductionModeOverCalendarEvent ):
                if fCheckForActiveCalendarEvent(self.Machine, self.EventTime, pEventID, pEventGroupID, ActivateProductionMode, ActivateProductionModeID) == True:
                    self.EventID = pEventID
                    self.EventGroup = pEventGroupID
                    self.IsCalendarEvent = True
                    self.RootEventID = 0
                    self.Update()
                    
                    if ActivateProductionMode and ActivateProductionModeID > 0:
                        self.Machine.ActiveCalendarEvent = True
                        self.Machine.ActiveCalendarEventProductionModeID = ActivateProductionModeID
                        strSQL = 'UPDATE TblMachines SET ActiveCalendarEvent = 1, ActiveCalendarEventProductionModeID = ' + self.Machine.ActiveCalendarEventProductionModeID + ' WHERE ID = ' + self.Machine.ID
                        MdlConnection.CN.execute(strSQL)
                    else:
                        self.Machine.ActiveCalendarEvent = False
                        self.Machine.ActiveCalendarEventProductionModeID = 0
                        strSQL = 'UPDATE TblMachines SET ActiveCalendarEvent = 0, ActiveCalendarEventProductionModeID = ' + self.Machine.ActiveCalendarEventProductionModeID + ' WHERE ID = ' + self.Machine.ID
                        MdlConnection.CN.execute(strSQL)
            if not pFromNewShift:
                if pJob.PConfigID != 0 and pJob.IsPConfigMain == True:
                    for tVariant in self.Job.PConfigJobs:
                        tChildJob = tVariant
                        tEvent = RTEvent()
                        tEvent.Create(pMachine, pEventGroupID, pEventID, pDescr, tChildJob, VBGetMissingArgument(tEvent.Create, 5), pRootEventID, pEventTime)
                        tChildJob.OpenEvent = tEvent

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            if not pJob is None:
                MdlGlobal.RecordError(type(self).__name__ + '.Create:', str(0), error.args[0], 'JobID: ' + str(pJob.ID))
            
        RstCursor = None
        tChildJob = None
        tVariant = None
        tEvent = None


    def CalcEffective(self):
        try:
            self.EffectiveDownTime = self.DownTime * self.PConfigPC / 100
            self.EffectiveDuration = self.Duration * self.PConfigPC / 100
            self.EffectiveInActiveTime = self.InActiveTime * self.PConfigPC / 100

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcEffective:', str(0), error.args[0], 'EventID: ' + self.ID)


    def EndEvent(self, pCheckCalendar, pTechnicianUserID=0, pEndTime=datetime.strptime('00:00:00', '%H:%M:%S')):
        strSQL = ''
        RstCursor = None
        tIsInActiveTime = False
        tIsDownTime = False
        tEventID = 0
        tEventGroupID = 0
        tMachine = self.Machine()
        ActivateProductionMode = False
        ActivateProductionModeID = 0

        try:       
            if self.Machine.ID == 3:
                tEventID = tEventID
            if pEndTime > datetime.strptime('00:00:00', '%H:%M:%S') and pEndTime > self.EventTime:
                self.EndTime = pEndTime
            else:
                self.EndTime = mdl_Common.NowGMT()
            self.Duration = DateDiff('n', self.EventTime, self.EndTime)
            self.DurationSec = DateDiff('s', self.EventTime, self.EndTime)
            
            if self.Job.MachineType.MinEventDuration > 0 and self.Duration <= self.Job.MachineType.MinEventDuration and self.Job.MachineType.MinEventReasonID > 0 and self.EventID != 100 and self.EventID != 18 and self.Machine.ProductionModeID == 1:
                self.EventGroup = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('EventGroupID', 'STblEventDesr', 'ID = ' + self.Job.MachineType.MinEventReasonID, 'CN'))
                self.EventID = self.Job.MachineType.MinEventReasonID
                self.IsCalendarEvent = False
                self.IsShortEvent = True
                strSQL = ''
                strSQL = strSQL + 'UPDATE TblEvent SET' + '\n'
                strSQL = strSQL + 'Event = ' + self.EventID + ',' + '\n'
                strSQL = strSQL + 'EventGroup = ' + self.EventGroup + ',' + '\n'
                strSQL = strSQL + 'IsCalendarEvent = 0,' + '\n'
                strSQL = strSQL + 'IsShortEvent = 1'
                strSQL = strSQL + 'WHERE ID = ' + self.ID
                MdlConnection.CN.execute(( strSQL ))

            if ( ( self.Machine.NewJob == False or  ( self.Machine.NewJob == True and self.Machine.SetupEventIDOnSetupEnd == 2 ) )  and self.Machine.ProductionModeID == 1 ) or ( self.Machine.ProductionModeID > 1 and not self.Machine.ProductionModeOverCalendarEvent ):
                if fCheckCalendar(self.Machine, self.EventTime, self.DurationSec, tEventID, tEventGroupID, ActivateProductionMode, ActivateProductionModeID) == True:
                    self.EventID = tEventID
                    self.EventGroup = tEventGroupID
                    self.IsCalendarEvent = True
                    self.RootEventID = 0
                else:
                    if self.IsCalendarEvent:
                        if self.Machine.ProductionModeReasonID != 0:
                            self.EventID = self.Machine.ProductionModeReasonID
                            self.EventGroup = self.Machine.ProductionModeGroupReasonID
                            self.IsCalendarEvent = False
                            strSQL = ''
                            strSQL = strSQL + 'UPDATE TblEvent SET' + '\n'
                            strSQL = strSQL + 'Event = ' + self.Machine.ProductionModeReasonID + ',' + '\n'
                            strSQL = strSQL + 'EventGroup = ' + self.Machine.ProductionModeGroupReasonID + ',' + '\n'
                            strSQL = strSQL + 'IsCalendarEvent = 0'
                            strSQL = strSQL + 'WHERE ID = ' + self.ID
                            MdlConnection.CN.execute(( strSQL ))
                        else:
                            self.EventID = 0
                            self.EventGroup = 6
                            self.IsCalendarEvent = False
                            strSQL = ''
                            strSQL = strSQL + 'UPDATE TblEvent SET' + '\n'
                            strSQL = strSQL + 'Event = 0,' + '\n'
                            strSQL = strSQL + 'EventGroup = 6,' + '\n'
                            strSQL = strSQL + 'IsCalendarEvent = 0'
                            strSQL = strSQL + 'WHERE ID = ' + self.ID
                            MdlConnection.CN.execute(( strSQL ))
            
            self.EffectiveDuration = self.Duration *  ( self.Job.PConfigPC / 100 )
            if self.EventID == 0 and not self.Machine.Server.SystemVariables.AllowEventReasonsWithNoDefinition:
                self.DownTime = self.Duration
                self.DownTimeSec = self.DurationSec
                self.EffectiveDownTime = self.EffectiveDuration
            else:
                RstCursor = None
                strSQL = 'SELECT IsDownTime,IsInActiveTime FROM STblEventDesr WHERE ID = ' + self.EventID
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstCursor.arraysize == 1:
                    tIsInActiveTime = MdlADOFunctions.fGetRstValBool(RstData.IsInactiveTime, False)
                    tIsDownTime = MdlADOFunctions.fGetRstValBool(RstData.IsDownTime, False)
                RstCursor.close()
                if tIsInActiveTime == True:
                    self.InActiveTime = self.Duration
                    self.InActiveTimeSec = self.DurationSec
                    self.EffectiveInActiveTime = self.EffectiveDuration
                else:
                    self.InActiveTime = 0
                    self.InActiveTimeSec = 0
                    self.EffectiveInActiveTime = 0
                if tIsDownTime == True:
                    self.DownTime = self.Duration
                    self.DownTimeSec = self.DurationSec
                    self.EffectiveDownTime = self.EffectiveDuration
                else:
                    self.DownTime = 0
                    self.DownTimeSec = 0
                    self.EffectiveDownTime = 0
            
            if self.PConfigParentID != 0:
                self.Duration = 0
                self.DurationSec = 0
            if pTechnicianUserID != 0:
                self.TechnicianUserID = pTechnicianUserID
            self.Update()
            if self.Machine.ActiveJob.ID != self.Job.ID:
                self.Job.DetailsCalc(False, False)

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.EndEvent:', str(0), error.args[0], 'EventID: ' + self.ID)

        RstCursor = None


    def CloseAndCreateForNewShift(self, pNewShiftID, pCheckCalendar, pRootEventID=0, pFromShiftChange=False):
        tEvent = RTEvent()
        tMachine = self.Machine()
        strSQL = ''
        RstCursor = None
        OriginalRootEvent = 0

        try:
            self.EndEvent(pCheckCalendar)
            OriginalRootEvent = self.ID
            tEvent = self
            self.EndTime = 0
            self.Duration = 0
            self.DurationSec = 0
            self.EffectiveDuration = 0
            self.DownTime = 0
            self.DownTimeSec = 0
            self.EffectiveDownTime = 0
            self.InActiveTime = 0
            self.InActiveTimeSec = 0
            self.EffectiveInActiveTime = 0
            if pRootEventID == 0:
                pRootEventID = tEvent.RootEventID
            
            if not tEvent.IsCalendarEvent:
                if tEvent.Machine.ProductionModeReasonID != 0:
                    self.Create(tEvent.Machine, tEvent.Machine.ProductionModeGroupReasonID, tEvent.Machine.ProductionModeReasonID, '', self.Job, True)
                    
                elif tEvent.IsShortEvent or  ( pFromShiftChange and not tEvent.Machine.ContinueEventReasonOnShiftChange ) :
                    self.Create(tEvent.Machine, 6, 0, '', self.Job, True, pRootEventID)
                else:
                    self.Create(tEvent.Machine, tEvent.EventGroup, tEvent.EventID, tEvent.Descr, self.Job, True, pRootEventID)
            else:
                if tEvent.Machine.NewJob:
                    tEvent.Create(tEvent.Machine, 10, 100, 'Setup', self.Job, True)
                else:
                    if tEvent.Machine.ProductionModeReasonID != 0 and tEvent.Machine.ProductionModeOverCalendarEvent:
                        self.Create(tEvent.Machine, tEvent.Machine.ProductionModeGroupReasonID, tEvent.Machine.ProductionModeReasonID, '', self.Job, True)
                    else:
                        self.Create(tEvent.Machine, 6, 0, '', self.Job, True, pRootEventID)
                    
            
            if tEvent.RootEventID == 0 and tEvent.EventID != 18 and tEvent.IsCalendarEvent == 0:
                strSQL = 'SELECT DISTINCT MachineID FROM TblEvent WHERE RootEventID = ' + OriginalRootEvent
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                while not RstCursor.EOF:
                    tMachine = self.Machine.Server.Machines.Item(str(RstData.MachineID))
                    
                    tMachine.Server.SplitActiveEvent(tMachine.ID, pNewShiftID, VBGetMissingArgument(tMachine.Server.SplitActiveEvent, 2), self.ID)
                    RstCursor.MoveNext()
                RstCursor.close()
        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CloseAndCreateForNewShift:', str(0), error.args[0], 'EventID: ' + str(self.ID) + '. New ShiftID: ' + str(pNewShiftID))
            
        tEvent = None

    def Update(self):
        strSQL = ''

        try:
            strSQL = 'UPDATE TblEvent'
            strSQL = strSQL + ' SET'
            strSQL = strSQL + ' Duration = ' + str(self.Duration)
            strSQL = strSQL + ' ,DurationSec = ' + str(self.DurationSec)
            strSQL = strSQL + ' ,DownTime = ' + str(self.DownTime)
            strSQL = strSQL + ' ,DownTimeSec = ' + str(self.DownTimeSec)
            strSQL = strSQL + ' ,InActiveTime = ' + str(self.InActiveTime)
            strSQL = strSQL + ' ,InActiveTimeSec = ' + str(self.InActiveTimeSec)
            strSQL = strSQL + ' ,EffectiveDownTime = ' + str(self.EffectiveDownTime)
            strSQL = strSQL + ' ,EffectiveDuration = ' + str(self.EffectiveDuration)
            strSQL = strSQL + ' ,EffectiveInActiveTime = ' + str(self.EffectiveInActiveTime)
            strSQL = strSQL + ' ,TechnicianUserID = ' + str(self.TechnicianUserID)
            if not self.Josh is None:
                strSQL = strSQL + ' ,JoshID = ' + str(self.Josh.ID)
            strSQL = strSQL + ' ,Status = 1'
            strSQL = strSQL + ' ,IsCalendarEvent = ' 
            if self.IsCalendarEvent == True:
                strSQL = strSQL + str(1)
            else:
                strSQL = strSQL + str(0)
             
            if GlobalVariables.IsDate(self.EndTime) and str(self.EndTime) != '00:00:00':
                
                strSQL = strSQL + ' ,EndTime = \'' + MdlUtilsH.ShortDate(self.EndTime, True, True, True) + '\''
            if self.IsCalendarEvent == True:
                strSQL = strSQL + ' ,Event = ' + str(self.EventID)
                strSQL = strSQL + ' ,EventGroup = ' + str(self.EventGroup)
            strSQL = strSQL + ' ,RootEventID = ' + str(self.RootEventID)
            strSQL = strSQL + ' ,IsShortEvent = ' 
            if self.IsShortEvent == True:
                strSQL = strSQL + str(1)
            else:
                strSQL = strSQL + str(0)

            strSQL = strSQL + ' WHERE ID = ' + str(self.ID)
            MdlConnection.CN.execute(strSQL)

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.Update:', str(0), error.args[0], 'EventID: ' + str(self.ID))
            
        strSQL = ''

    def Refresh(self, pEventGroupID=0, pEventID=0):
        strSQL = ''
        RstCursor = None
        tEventID = 0
        tEventGroupID = 0

        try:        
            if not ( IsMissing(pEventGroupID) and IsMissing(pEventID) ) :
                self.EventGroup = pEventGroupID
                self.EventID = pEventID
            else:
                strSQL = 'SELECT EventGroup, Event FROM TblEvent WHERE ID = ' + self.ID

                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstCursor.arraysize == 1:
                    tEventGroupID = MdlADOFunctions.fGetRstValLong(RstData.EventGroup)
                    tEventID = MdlADOFunctions.fGetRstValLong(RstData.event)
                RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

        RstCursor = None

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
            MdlGlobal.RecordError('RTEvent Destroy ' + self.__mID, str(0), 'Error terminating class RTEvent', '')


    def setInActiveTimeSec(self, value):
        self.__mInActiveTimeSec = value

    def getInActiveTimeSec(self):
        returnVal = None
        returnVal = self.__mInActiveTimeSec
        return returnVal
    InActiveTimeSec = property(fset=setInActiveTimeSec, fget=getInActiveTimeSec)


    def setDownTimeSec(self, value):
        self.__mDownTimeSec = value

    def getDownTimeSec(self):
        returnVal = None
        returnVal = self.__mDownTimeSec
        return returnVal
    DownTimeSec = property(fset=setDownTimeSec, fget=getDownTimeSec)


    def setDurationSec(self, value):
        self.__mDurationSec = value

    def getDurationSec(self):
        returnVal = None
        returnVal = self.__mDurationSec
        return returnVal
    DurationSec = property(fset=setDurationSec, fget=getDurationSec)


    def setIsShortEvent(self, value):
        self.__mIsShortEvent = value

    def getIsShortEvent(self):
        returnVal = None
        returnVal = self.__mIsShortEvent
        return returnVal
    IsShortEvent = property(fset=setIsShortEvent, fget=getIsShortEvent)


    def setRootEventID(self, value):
        self.__mRootEventID = value

    def getRootEventID(self):
        returnVal = None
        returnVal = self.__mRootEventID
        return returnVal
    RootEventID = property(fset=setRootEventID, fget=getRootEventID)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    def setEventGroup(self, value):
        self.__mEventGroup = value

    def getEventGroup(self):
        returnVal = None
        returnVal = self.__mEventGroup
        return returnVal
    EventGroup = property(fset=setEventGroup, fget=getEventGroup)


    def setEventID(self, value):
        self.__mEventID = value

    def getEventID(self):
        returnVal = None
        returnVal = self.__mEventID
        return returnVal
    EventID = property(fset=setEventID, fget=getEventID)


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


    def setDownTime(self, value):
        self.__mDownTime = value

    def getDownTime(self):
        returnVal = None
        returnVal = self.__mDownTime
        return returnVal
    DownTime = property(fset=setDownTime, fget=getDownTime)


    
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


    def setStatus(self, value):
        self.__mStatus = value

    def getStatus(self):
        returnVal = None
        returnVal = self.__mStatus
        return returnVal
    Status = property(fset=setStatus, fget=getStatus)


    
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


    def setInActiveTime(self, value):
        self.__mInActiveTime = value

    def getInActiveTime(self):
        returnVal = None
        returnVal = self.__mInActiveTime
        return returnVal
    InActiveTime = property(fset=setInActiveTime, fget=getInActiveTime)


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


    def setEffectiveDownTime(self, value):
        self.__mEffectiveDownTime = value

    def getEffectiveDownTime(self):
        returnVal = None
        returnVal = self.__mEffectiveDownTime
        return returnVal
    EffectiveDownTime = property(fset=setEffectiveDownTime, fget=getEffectiveDownTime)


    def setEffectiveInActiveTime(self, value):
        self.__mEffectiveInActiveTime = value

    def getEffectiveInActiveTime(self):
        returnVal = None
        returnVal = self.__mEffectiveInActiveTime
        return returnVal
    EffectiveInActiveTime = property(fset=setEffectiveInActiveTime, fget=getEffectiveInActiveTime)


    def setIsCalendarEvent(self, value):
        self.__mIsCalendarEvent = value

    def getIsCalendarEvent(self):
        returnVal = None
        returnVal = self.__mIsCalendarEvent
        return returnVal
    IsCalendarEvent = property(fset=setIsCalendarEvent, fget=getIsCalendarEvent)


    def setTechnicianUserID(self, value):
        self.__mTechnicianUserID = value

    def getTechnicianUserID(self):
        returnVal = None
        returnVal = self.__mTechnicianUserID
        return returnVal
    TechnicianUserID = property(fset=setTechnicianUserID, fget=getTechnicianUserID)

    
    
