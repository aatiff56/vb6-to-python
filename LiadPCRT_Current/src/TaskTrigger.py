import enum
import mdl_Common
import MdlADOFunctions
import MdlGlobal
import MdlConnection
import MdlUtilsH
import MdlOnlineTasks

class TaskTriggerIntervalType(enum.Enum):
    Timeinterval = 1
    ValueGT = 2
    ValueLT = 3
    ValueInterval = 4
    SpecificDay = 5

class TaskTriggerIntervalRelation(enum.Enum):
    value = 1
    ControllerField = 2
    JobField = 3
    MachineMemberField = 4

class TaskTrigger:    
    __TaskDefID = 0
    __TriggerDefID = 0
    __FireTriggerWhileSetup = False
    __IntervalType = TaskTriggerIntervalType
    __IntervalRelation = TaskTriggerIntervalRelation
    __IntervalRelationTarget = ''
    __IntervalValue = ''
    __ProductID = 0
    __MachineID = 0
    __MoldID = 0
    __LastFireTime = None
    __LastFireValue = 0.0
    ResetOnNewJob = False
    __ID = 0
    __IntervalFromLastFire = 0.0
    __pMachine = None
    __RelatedControlParam = None
    __FirstCheckDone = False
    __TriggerFired = False
    __NextFireTime = None
    __SpecificWeekDay = 0
    __SpecificTime = None
    __EventTypeID = 0

    def __init__(self):
        self.__FirstCheckDone = False
        self.__TriggerFired = False

    def Init(self, TaskDef, TaskTriggerDefID, vMachine):
        returnVal = False
        strSQL = ''
        TriggerRSTCursor = None
        RstCursor = None

        try:
            strSQL = 'Select * From TblTaskTriggerDef Where ID = ' + str(TaskTriggerDefID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.rowCount == 0:
                raise Exception("No data found.")
            
            strSQL = 'Select * From TblTaskTrigger Where TaskDef = ' + str(TaskDef) + ' AND MachineID = ' + str(vMachine.ID) + ' AND TaskTriggerDefID = ' + str(TaskTriggerDefID)
            if TriggerRSTCursor:
                TriggerRstCursor.close()

            TriggerRstCursor = MdlConnection.CN.cursor()
            TriggerRstCursor.execute(strSQL)
            TriggerRstData = TriggerRstCursor.fetchone()

            if TriggerRstData.rowCount == 0:
                TriggerRstData.AddNew()

            else:
                if MdlADOFunctions.fGetRstValBool(TriggerRstData.ResetOnNewJob, False) == False:
                    if TriggerRstData.LastFireTime:
                        self.__LastFireTime = MdlUtilsH.ShortDate(CDate(TriggerRstData.LastFireTime), False, True)
                    if TriggerRstData.LastFireValue:
                        self.__LastFireValue = '' + TriggerRstData.LastFireValue
                else:
                    if TriggerRstData.LastFireTime:
                        self.__LastFireTime = MdlUtilsH.ShortDate(CDate(TriggerRstData.LastFireTime), False, True)
                    if TriggerRstData.LastFireValue:
                        self.__LastFireValue = '' + TriggerRstData.LastFireValue
            TriggerRstData.TaskTriggerDefID = TaskTriggerDefID
            TriggerRstData.TaskDef = TaskDef
            TriggerRstData.IntervalType = RstCursor.IntervalType
            TriggerRstData.IntervalRelation = RstCursor.IntervalRelation
            TriggerRstData.IntervalRelationTarget = RstCursor.IntervalRelationTarget
            TriggerRstData.MachineID = vMachine.ID
            TriggerRstData.ResetOnNewJob = RstCursor.ResetOnNewJob
            TriggerRstData.FireTriggerWhileSetup = RstCursor.FireTriggerWhileSetup
            TriggerRstData.SpecificWeekDay = RstCursor.SpecificWeekDay
            TriggerRstData.SpecificTime = RstCursor.SpecificTime
            TriggerRstData.EventTypeID = RstCursor.EventTypeID
            
            if RstCursor.ProductGroup:
                TriggerRstData.ProductGroup = RstCursor.ProductGroup
            if RstCursor.ProductID:
                TriggerRstData.ProductID = RstCursor.ProductID
            if RstCursor.MachineGroup:
                TriggerRstData.MachineGroup = RstCursor.MachineGroup
            if RstCursor.MoldGroup:
                TriggerRstData.MoldGroup = RstCursor.MoldGroup
            if RstCursor.QualityGroup:
                TriggerRstData.QualityGroup = RstCursor.QualityGroup
            if RstCursor.JobField != '':
                TriggerRstData.JobField = RstCursor.JobField
            if RstCursor.JobFieldValue != '':
                TriggerRstData.JobFieldValue = RstCursor.JobFieldValue
            TriggerRstData.Update()
            self.__ID = TriggerRstData.ID
            TriggerRstCursor.close()
            self.__TaskDefID = TaskDef
            self.__TriggerDefID = TaskTriggerDefID
            self.__IntervalType = RstCursor.IntervalType
            if self.__IntervalType == TaskTriggerIntervalType.SpecificDay:
                self.__SpecificWeekDay = RstCursor.SpecificWeekDay
                self.__SpecificTime = RstCursor.SpecificTime
                self.__NextFireTime = MdlOnlineTasks.fGetNextTriggerDate(self.__SpecificWeekDay, self.__SpecificTime)
            self.__IntervalRelation = RstCursor.IntervalRelation
            if MdlADOFunctions.fGetRstValString(RstCursor.IntervalRelationTarget) != '':
                self.__IntervalRelationTarget = RstCursor.IntervalRelationTarget
            self.__ProductID = MdlADOFunctions.fGetRstValLong(RstCursor.ProductID)
            self.__MachineID = MdlADOFunctions.fGetRstValLong(RstCursor.MachineID)
            self.ResetOnNewJob = RstCursor.ResetOnNewJob
            self.__FireTriggerWhileSetup = MdlADOFunctions.fGetRstValBool(RstCursor.FireTriggerWhileSetup, True)
            
            self.__EventTypeID = MdlADOFunctions.fGetRstValLong(RstCursor.EventTypeID)
            self.__pMachine = vMachine
            if (self.__IntervalRelation == TaskTriggerIntervalRelation.ControllerField):
                if vMachine.GetParam(self.__IntervalRelationTarget, self.__RelatedControlParam) == False:
                    Err.Raise(1)
                self.__IntervalValue = RstCursor.IntervalSourceValue
                
            elif (self.__IntervalRelation == TaskTriggerIntervalRelation.JobField):
                self.__IntervalValue = RstCursor.IntervalSourceValue
            elif (self.__IntervalRelation == TaskTriggerIntervalRelation.MachineMemberField):
                self.__IntervalValue = RstCursor.IntervalSourceValue
            elif (self.__IntervalRelation == TaskTriggerIntervalRelation.value):
                self.__IntervalValue = RstCursor.IntervalSourceValue
            RstCursor.close()
            returnVal = True

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError('TaskTriggerInit', str(0), error.args[0], 'Cant init task trigger ' + str(TaskDef) + ' ON Machine ' + str(vMachine.ID) + ' - ' + str(vMachine.LName))
            
        if RstCursor:
            RstCursor.close()
        RstCursor = None

        if TriggerRSTCursor:
            TriggerRstCursor.close()
        TriggerRSTCursor = None

        return returnVal

    def CheckInterval(self):
        returnVal = None
        tmpValue = 0.0
        RefValue = 0.0
        RefJobValue = ''
        strSQL = ''
        TriggerRSTCursor = None        
        ErrCount = 0

        if (self.__IntervalRelation == TaskTriggerIntervalRelation.ControllerField):
            RefValue = self.__RelatedControlParam.LastValue
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.JobField):
            RefValue = MdlADOFunctions.GetSingleValue(self.__IntervalRelationTarget, 'TblJob', 'ID = ' + self.__pMachine.ActiveJobID)
            
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.MachineMemberField):
            if (self.__IntervalRelationTarget == 'NoProgressCount'):
                RefValue = self.__pMachine.NoProgressCount
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.value):
            RefValue = self.__IntervalValue
        returnVal = False
        if (self.__IntervalType == TaskTriggerIntervalType.Timeinterval):
            
            if DateDiff('n', self.__LastFireTime, mdl_Common.NowGMT()) >= int(self.__IntervalValue):
                returnVal = True
        elif (self.__IntervalType == TaskTriggerIntervalType.ValueGT):
            tmpValue = RefValue
            if tmpValue > float(self.__IntervalValue):
                if self.__TriggerFired == False:
                    returnVal = True
                    self.__LastFireValue = tmpValue
            else:
                self.__TriggerFired = False
        elif (self.__IntervalType == TaskTriggerIntervalType.ValueInterval):
            tmpValue = float(RefValue)
            if abs(tmpValue - self.__LastFireValue) >= abs(float(self.__IntervalValue)):
                if ( self.__LastFireValue == 0 )  and  ( tmpValue / float(self.__IntervalValue) )  >= 2:
                    self.__LastFireValue = 0
                    returnVal = False
                else:
                    self.__LastFireValue = tmpValue
                    returnVal = True
        elif (self.__IntervalType == TaskTriggerIntervalType.ValueLT):
            tmpValue = float(RefValue)
            if tmpValue < float(self.__IntervalValue):
                if self.__TriggerFired == False:
                    returnVal = True
            else:
                self.__TriggerFired = False
        elif (self.__IntervalType == TaskTriggerIntervalType.SpecificDay):
            if mdl_Common.NowGMT() >= self.__NextFireTime:
                returnVal = True
                self.__NextFireTime = MdlOnlineTasks.fGetNextTriggerDate(self.__SpecificWeekDay, self.__SpecificTime)
            else:
                returnVal = False
        
        if self.__IntervalRelation == TaskTriggerIntervalRelation.JobField:
            if self.__ProductID != 0:
                if self.__ProductID != self.__pMachine.ActiveJob.ProductID:
                    ErrCount = ErrCount + 1
            strSQL = 'Select * From TblTaskTrigger Where TaskDef = ' + self.__TaskDefID + ' AND MachineID = ' + str(self.__pMachine.ID) + ' AND TaskTriggerDefID = ' + self.__TriggerDefID
            
            TriggerRstCursor = MdlConnection.CN.cursor()
            TriggerRstCursor.execute(strSQL)
            TriggerRstData = TriggerRstCursor.fetchone()

            if TriggerRstData.rowCount == 1:
                if TriggerRstData.QualityGroup:
                    RefValue = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('QualityGroup', 'TblProduct', ' ID = ' + self.__pMachine.ActiveJob.ProductID))
                    if TriggerRstData.QualityGroup != 0:
                        ErrCount = ErrCount + 1
                if TriggerRstData.MachineGroup:
                    RefValue = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineGroupID', 'TblMachines', ' ID = ' + self.__pMachine.ID))
                    if TriggerRstData.MachineGroup != RefValue:
                        ErrCount = ErrCount + 1
                if TriggerRstData.ProductGroup:
                    RefValue = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductGroup', 'TblProduct', ' ID = ' + self.__pMachine.ActiveJob.ProductID))
                    if TriggerRstData.ProductGroup != RefValue:
                        ErrCount = ErrCount + 1
                if TriggerRstData.JobField:
                    RefJobValue = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue(TriggerRstData.JobField, 'TblJob', 'ID = ' + self.__pMachine.ActiveJobID))
                    if TriggerRstData.JobFieldValue != RefJobValue:
                        ErrCount = ErrCount + 1
        
        if ErrCount == 0:
            if self.CheckInterval() == True:
                returnVal = True
            else:
                if self.__IntervalType == 0:
                    returnVal = True
                else:
                    returnVal = False
        else:
            if ErrCount != 0:
                returnVal = False
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
        return returnVal

    def FireTrigger(self):
        returnVal = False
        strSQL = ''
        RstCursor = None
        SkillRst = None
        Descr = ''
        BasicPriority = 0.0
        StandardDuration = 0.0
        TaskType = 0
        CurrentShiftID = 0
        ShiftDefID = 0
        tmpMachineID = 0
        tmpProductID = 0
        UserTaskID = 0
        TaskDefID = 0
        tOpenNewTask = False
        
        try:
            tOpenNewTask = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'OpenNewTriggerTask\'', 'CN'), False)
            
            strSQL = 'Select ID, Descr, BasicPriority, StandardDuration, TaskType From TblTaskDef Where ID = ' + str(self.PTaskDefID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if not RstData:
                raise Exception('No data found, while firing trigger.')

            TaskDefID = MdlADOFunctions.fGetRstValLong(RstData.ID)
            Descr = '' + RstData.Descr
            BasicPriority = MdlADOFunctions.fGetRstValDouble(RstData.BasicPriority)
            StandardDuration = MdlADOFunctions.fGetRstValDouble(RstData.StandardDuration)
            TaskType = MdlADOFunctions.fGetRstValLong(RstData.TaskType)
            RstCursor.close()

            tmpMachineID = self.__pMachine.ID
            tmpProductID = self.__pMachine.ActiveJob.Product.ID
            CurrentShiftID = self.__pMachine.Server.CurrentShiftID
            ShiftDefID = self.__pMachine.Server.ShiftCalendar.CurrentShiftDefID
            
            if self.ResetOnNewJob:
                strSQL = 'Select ID From TblUserTasks Where (JobID = ' + str(self.__pMachine.ActiveJobID) + ') AND (MachineID = ' + str(self.__pMachine.ID) + ' OR ProductID = ' + str(self.__pMachine.ActiveProductID) + ') AND TaskDefID = ' + str(TaskDefID) + ' AND Status < 3'
            else:
                strSQL = 'Select ID From TblUserTasks Where (MachineID = ' + str(self.__pMachine.ID) + ' OR ProductID = ' + str(self.__pMachine.ActiveProductID) + ') AND TaskDefID = ' + TaskDefID + ' AND Status < 3'

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.rowCount == 0 or tOpenNewTask == True:
                
                strSQL = 'Insert TblUserTasks (TaskDefID, PriorityLevel, StandardDuration, ShiftID, ShiftDef, Status, TaskType, Descr, MachineID, ProductID, InvokeTime, JobID, JoshID) '
                strSQL = strSQL + ' VALUES(' + TaskDefID + ', ' + BasicPriority + ', ' + StandardDuration + ', ' + CurrentShiftID + ', ' + ShiftDefID + ', 1, ' + TaskType + ', \'' + Descr + '\', ' + tmpMachineID + ', ' + tmpProductID + ', \'' + MdlUtilsH.ShortDate(mdl_Common.NowGMT(), True, True) + '\', ' + self.__pMachine.ActiveJobID + ', ' + self.__pMachine.ActiveJoshID + ')'
                MdlConnection.CN.execute(strSQL)
                
                UserTaskID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblUserTasks', 'TaskDefID=' + TaskDefID + ' ORDER BY ID DESC', 'CN'))
                strSQL = 'Select QualificationID, BasicSkillLevel From TblTaskDefQualifications Where TaskDefID = ' + TaskDefID

                SkillRstCursor = MdlConnection.CN.cursor()
                SkillRstCursor.execute(strSQL)
                SkillRstValues = SkillRstCursor.fetchall()

                for SkillRstData in SkillRstValues:
                    strSQL = 'Insert TblUserTasksQualifications(UserTaskID, TaskDefID, QualificationID, BasicSkillLevel) VALUES(' + UserTaskID + ', ' + TaskDefID + ', ' + str(SkillRstData.QualificationID) + ', ' + str(SkillRstData.BasicSkillLevel) + ')'
                    MdlConnection.CN.execute(strSQL)

                SkillRst.close()
            RstCursor.close()
            strSQL = 'Update TblTaskTrigger Set LastFireTime = \'' + MdlUtilsH.ShortDate(mdl_Common.NowGMT(), True, True) + '\', LastFireValue=\'' + str(self.__LastFireValue) + '\''
            strSQL = strSQL + ' Where (MachineID = ' + str(self.__pMachine.ID) + ' OR ProductID = ' + str(self.__pMachine.ActiveProductID) + ') AND TaskDef = ' + TaskDefID + ' AND TaskTriggerDefID=' + self.__TriggerDefID
            
            MdlConnection.CN.execute(strSQL)
            self.__LastFireTime = MdlUtilsH.ShortDate(mdl_Common.NowGMT(), False, True)
            returnVal = True

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError('TaskTriggerFireTrigger', str(0), error.args[0], 'Cant fire trigger ' + str(self.__ID))

        if RstCursor:
            RstCursor.close()
        if SkillRst:
            SkillRst.close()
        RstCursor = None

        return returnVal


    def getPTaskDefID(self):
        returnVal = None
        returnVal = self.__TaskDefID
        return returnVal
    PTaskDefID = property(fget=getPTaskDefID)


    def getPTriggerDefID(self):
        returnVal = None
        returnVal = self.__TriggerDefID
        return returnVal
    PTriggerDefID = property(fget=getPTriggerDefID)


    def setPFireTriggerWhileSetup(self, the_mPFireTriggerWhileSetup):
        self.__FireTriggerWhileSetup = the_mPFireTriggerWhileSetup

    def getPFireTriggerWhileSetup(self):
        returnVal = None
        returnVal = self.__FireTriggerWhileSetup
        return returnVal
    PFireTriggerWhileSetup = property(fset=setPFireTriggerWhileSetup, fget=getPFireTriggerWhileSetup)


    def setPEventTypeID(self, value):
        self.__EventTypeID = value

    def getPEventTypeID(self):
        returnVal = None
        returnVal = self.__EventTypeID
        return returnVal
    PEventTypeID = property(fset=setPEventTypeID, fget=getPEventTypeID)


    def setPIntervalType(self, the_mPIntervalType):
        self.__IntervalType = the_mPIntervalType

    def getPIntervalType(self):
        returnVal = None
        returnVal = self.__IntervalType
        return returnVal
    PIntervalType = property(fset=setPIntervalType, fget=getPIntervalType)
