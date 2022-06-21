import MdlADOFunctions

class TaskTrigger:
    Timeinterval = 1
    ValueGT = 2
    ValueLT = 3
    ValueInterval = 4
    SpecificDay = 5
    
    value = 1
    ControllerField = 2
    JobField = 3
    MachineMemberField = 4

    __TaskDefID = 0
    __TriggerDefID = 0
    __FireTriggerWhileSetup = False
    __IntervalType = TaskTriggerIntervalType()
    __IntervalRelation = TaskTriggerIntervalRelation()
    __IntervalRelationTarget = ''
    __IntervalValue = ''
    __ProductID = 0
    __MachineID = 0
    __MoldID = 0
    __LastFireTime = Date()
    __LastFireValue = 0.0
    ResetOnNewJob = False
    __ID = 0
    __IntervalFromLastFire = 0.0
    __pMachine = Machine()
    __RelatedControlParam = ControlParam()
    __FirstCheckDone = False
    __TriggerFired = False
    __NextFireTime = Date()
    __SpecificWeekDay = 0
    __SpecificTime = Date()
    __EventTypeID = 0

    def __init__(self):
        
        self.__FirstCheckDone = False
        self.__TriggerFired = False

    def Init(self, TaskDef, TaskTriggerDefID, vMachine):
        returnVal = None
        strSQL = ''

        TriggerRST = ADODB.Recordset()
        Rst = ADODB.Recordset()
        
        returnVal = False
        strSQL = 'Select * From TblTaskTriggerDef Where ID = ' + TaskTriggerDefID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        if not Rst.RecordCount > 0:
            Err.Raise(1)
        
        strSQL = 'Select * From TblTaskTrigger Where TaskDef = ' + TaskDef + ' AND MachineID = ' + vMachine.ID + ' AND TaskTriggerDefID = ' + TaskTriggerDefID
        if TriggerRST.State != 0:
            TriggerRST.Close()
        TriggerRST.Open(strSQL, CN, adOpenForwardOnly, adLockOptimistic)
        if TriggerRST.RecordCount == 0:
            TriggerRST.AddNew()
        else:
            if MdlADOFunctions.fGetRstValBool(TriggerRST.Fields("ResetOnNewJob").Value, False) == False:
                if not IsNull(TriggerRST.Fields("LastFireTime").Value):
                    self.__LastFireTime = ShortDate(CDate(TriggerRST.Fields("LastFireTime").Value), False, True)
                if not IsNull(TriggerRST.Fields("LastFireValue").Value):
                    self.__LastFireValue = '' + TriggerRST.Fields("LastFireValue").Value
            else:
                if not IsNull(TriggerRST.Fields("LastFireTime").Value):
                    self.__LastFireTime = ShortDate(CDate(TriggerRST.Fields("LastFireTime").Value), False, True)
                if not IsNull(TriggerRST.Fields("LastFireValue").Value):
                    self.__LastFireValue = '' + TriggerRST.Fields("LastFireValue").Value
        TriggerRST.Fields("TaskTriggerDefID").Value = TaskTriggerDefID
        TriggerRST.Fields("TaskDef").Value = TaskDef
        TriggerRST.Fields("IntervalType").Value = Rst.Fields("IntervalType").Value
        TriggerRST.Fields("IntervalRelation").Value = Rst.Fields("IntervalRelation").Value
        TriggerRST.Fields("IntervalRelationTarget").Value = Rst.Fields("IntervalRelationTarget").Value
        TriggerRST.Fields("MachineID").Value = vMachine.ID
        TriggerRST.Fields("ResetOnNewJob").Value = Rst.Fields("ResetOnNewJob").Value
        TriggerRST.Fields("FireTriggerWhileSetup").Value = Rst.Fields("FireTriggerWhileSetup").Value
        TriggerRST.Fields("SpecificWeekDay").Value = Rst.Fields("SpecificWeekDay").Value
        TriggerRST.Fields("SpecificTime").Value = Rst.Fields("SpecificTime").Value
        TriggerRST.Fields("EventTypeID").Value = Rst.Fields("EventTypeID").Value
        
        if not IsNull(Rst.Fields("ProductGroup").Value):
            TriggerRST.Fields("ProductGroup").Value = Rst.Fields("ProductGroup").Value
        if not IsNull(Rst.Fields("ProductID").Value):
            TriggerRST.Fields("ProductID").Value = Rst.Fields("ProductID").Value
        if not IsNull(Rst.Fields("MachineGroup").Value):
            TriggerRST.Fields("MachineGroup").Value = Rst.Fields("MachineGroup").Value
        if not IsNull(Rst.Fields("MoldGroup").Value):
            TriggerRST.Fields("MoldGroup").Value = Rst.Fields("MoldGroup").Value
        if not IsNull(Rst.Fields("QualityGroup").Value):
            TriggerRST.Fields("QualityGroup").Value = Rst.Fields("QualityGroup").Value
        if Rst.Fields("JobField").Value != '':
            TriggerRST.Fields("JobField").Value = Rst.Fields("JobField").Value
        if Rst.Fields("JobFieldValue").Value != '':
            TriggerRST.Fields("JobFieldValue").Value = Rst.Fields("JobFieldValue").Value
        TriggerRST.Update()
        self.__ID = TriggerRST.Fields("ID").Value
        TriggerRST.Close()
        self.__TaskDefID = TaskDef
        self.__TriggerDefID = TaskTriggerDefID
        self.__IntervalType = Rst.Fields("IntervalType").Value
        if self.__IntervalType == SpecificDay:
            self.__SpecificWeekDay = Rst.Fields("SpecificWeekDay").Value
            self.__SpecificTime = Rst.Fields("SpecificTime").Value
            self.__NextFireTime = fGetNextTriggerDate(self.__SpecificWeekDay, self.__SpecificTime)
        self.__IntervalRelation = Rst.Fields("IntervalRelation").Value
        if MdlADOFunctions.fGetRstValString(Rst.Fields("IntervalRelationTarget").Value) != '':
            self.__IntervalRelationTarget = Rst.Fields("IntervalRelationTarget").Value
        self.__ProductID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ProductID").Value)
        self.__MachineID = MdlADOFunctions.fGetRstValLong(Rst.Fields("MachineID").Value)
        self.ResetOnNewJob = Rst.Fields("ResetOnNewJob").Value
        self.__FireTriggerWhileSetup = MdlADOFunctions.fGetRstValBool(Rst.Fields("FireTriggerWhileSetup").Value, True)
        
        self.__EventTypeID = MdlADOFunctions.fGetRstValLong(Rst.Fields("EventTypeID").Value)
        self.__pMachine = vMachine
        if (self.__IntervalRelation == TaskTriggerIntervalRelation.ControllerField):
            if vMachine.GetParam(self.__IntervalRelationTarget, self.__RelatedControlParam) == False:
                Err.Raise(1)
            self.__IntervalValue = Rst.Fields("IntervalSourceValue").Value
            
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.JobField):
            self.__IntervalValue = Rst.Fields("IntervalSourceValue").Value
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.MachineMemberField):
            self.__IntervalValue = Rst.Fields("IntervalSourceValue").Value
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.value):
            self.__IntervalValue = Rst.Fields("IntervalSourceValue").Value
        Rst.Close()
        returnVal = True
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('TaskTriggerInit', Err.Number, Err.Description, 'Cant init task trigger ' + TaskDef + ' ON Machine ' + vMachine.ID + ' - ' + vMachine.LName)
            
        if Rst.State != 0:
            Rst.Close()
        Rst = None
        if TriggerRST.State != 0:
            TriggerRST.Close()
        TriggerRST = None
        return returnVal

    def CheckInterval(self):
        returnVal = None
        tmpValue = 0.0

        RefValue = 0.0

        RefJobValue = ''

        strSQL = ''

        TriggerRST = ADODB.Recordset()

        ErrCount = 0
        
        
        ErrCount = 0
        if (self.__IntervalRelation == TaskTriggerIntervalRelation.ControllerField):
            RefValue = self.__RelatedControlParam.LastValue
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.JobField):
            RefValue = GetSingleValue(self.__IntervalRelationTarget, 'TblJob', 'ID = ' + self.__pMachine.ActiveJobID)
            
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.MachineMemberField):
            if (self.__IntervalRelationTarget == 'NoProgressCount'):
                RefValue = self.__pMachine.NoProgressCount
        elif (self.__IntervalRelation == TaskTriggerIntervalRelation.value):
            RefValue = self.__IntervalValue
        returnVal = False
        if (self.__IntervalType == TaskTriggerIntervalType.Timeinterval):
            
            if DateDiff('n', self.__LastFireTime, NowGMT()) >= CLng(self.__IntervalValue):
                returnVal = True
        elif (self.__IntervalType == TaskTriggerIntervalType.ValueGT):
            tmpValue = RefValue
            if tmpValue > CDbl(self.__IntervalValue):
                if self.__TriggerFired == False:
                    returnVal = True
                    self.__LastFireValue = tmpValue
            else:
                self.__TriggerFired = False
        elif (self.__IntervalType == TaskTriggerIntervalType.ValueInterval):
            tmpValue = CDbl(RefValue)
            if Abs(tmpValue - self.__LastFireValue) >= Abs(CDbl(self.__IntervalValue)):
                if ( self.__LastFireValue == 0 )  and  ( tmpValue / CDbl(self.__IntervalValue) )  >= 2:
                    self.__LastFireValue = 0
                    returnVal = False
                else:
                    self.__LastFireValue = tmpValue
                    returnVal = True
        elif (self.__IntervalType == TaskTriggerIntervalType.ValueLT):
            tmpValue = CDbl(RefValue)
            if tmpValue < CDbl(self.__IntervalValue):
                if self.__TriggerFired == False:
                    returnVal = True
            else:
                self.__TriggerFired = False
        elif (self.__IntervalType == TaskTriggerIntervalType.SpecificDay):
            if NowGMT() >= self.__NextFireTime:
                returnVal = True
                self.__NextFireTime = fGetNextTriggerDate(self.__SpecificWeekDay, self.__SpecificTime)
            else:
                returnVal = False
        
        if self.__IntervalRelation == TaskTriggerIntervalRelation.JobField:
            if self.__ProductID != 0:
                if self.__ProductID != self.__pMachine.ActiveJob.ProductID:
                    ErrCount = ErrCount + 1
            strSQL = 'Select * From TblTaskTrigger Where TaskDef = ' + self.__TaskDefID + ' AND MachineID = ' + self.__pMachine.ID + ' AND TaskTriggerDefID = ' + self.__TriggerDefID
            
            TriggerRST.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            TriggerRST.ActiveConnection = None
            if TriggerRST.RecordCount == 1:
                if not IsNull(TriggerRST('QualityGroup').value):
                    RefValue = MdlADOFunctions.fGetRstValLong(GetSingleValue('QualityGroup', 'TblProduct', ' ID = ' + self.__pMachine.ActiveJob.ProductID))
                    if TriggerRST('QualityGroup').value != 0:
                        ErrCount = ErrCount + 1
                if not IsNull(TriggerRST('MachineGroup').value):
                    RefValue = MdlADOFunctions.fGetRstValLong(GetSingleValue('MachineGroupID', 'TblMachines', ' ID = ' + self.__pMachine.ID))
                    if TriggerRST('MachineGroup').value != RefValue:
                        ErrCount = ErrCount + 1
                if not IsNull(TriggerRST('ProductGroup').value):
                    RefValue = MdlADOFunctions.fGetRstValLong(GetSingleValue('ProductGroup', 'TblProduct', ' ID = ' + self.__pMachine.ActiveJob.ProductID))
                    if TriggerRST('ProductGroup').value != RefValue:
                        ErrCount = ErrCount + 1
                if not IsNull(TriggerRST('JobField').value):
                    RefJobValue = MdlADOFunctions.fGetRstValString(GetSingleValue(TriggerRST('JobField').value, 'TblJob', 'ID = ' + self.__pMachine.ActiveJobID))
                    if TriggerRST('JobFieldValue').value != RefJobValue:
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
        returnVal = None
        strSQL = ''

        Rst = ADODB.Recordset()

        SkillRst = ADODB.Recordset()

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
        
        returnVal = False
        
        tOpenNewTask = MdlADOFunctions.fGetRstValBool(GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'OpenNewTriggerTask\'', 'CN'), False)
        
        strSQL = 'Select ID, Descr, BasicPriority, StandardDuration, TaskType From TblTaskDef Where ID = ' + self.PTaskDefID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        if not Rst.RecordCount > 0:
            Err.Raise(1)
        TaskDefID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
        Descr = '' + Rst.Fields("Descr").Value
        BasicPriority = fGetRstValDouble(Rst.Fields("BasicPriority").Value)
        StandardDuration = fGetRstValDouble(Rst.Fields("StandardDuration").Value)
        TaskType = MdlADOFunctions.fGetRstValLong(Rst.Fields("TaskType").Value)
        Rst.Close()
        tmpMachineID = self.__pMachine.ID
        tmpProductID = self.__pMachine.ActiveJob.Product.ID
        CurrentShiftID = self.__pMachine.Server.CurrentShiftID
        ShiftDefID = self.__pMachine.Server.ShiftCalendar.CurrentShiftDefID
        
        if Me.ResetOnNewJob:
            strSQL = 'Select ID From TblUserTasks Where (JobID = ' + self.__pMachine.ActiveJobID + ') AND (MachineID = ' + self.__pMachine.ID + ' OR ProductID = ' + self.__pMachine.ActiveProductID + ') AND TaskDefID = ' + TaskDefID + ' AND Status < 3'
        else:
            strSQL = 'Select ID From TblUserTasks Where (MachineID = ' + self.__pMachine.ID + ' OR ProductID = ' + self.__pMachine.ActiveProductID + ') AND TaskDefID = ' + TaskDefID + ' AND Status < 3'
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        if Rst.RecordCount == 0 or tOpenNewTask == True:
            
            strSQL = 'Insert TblUserTasks (TaskDefID, PriorityLevel, StandardDuration, ShiftID, ShiftDef, Status, TaskType, Descr, MachineID, ProductID, InvokeTime, JobID, JoshID) '
            strSQL = strSQL + ' VALUES(' + TaskDefID + ', ' + BasicPriority + ', ' + StandardDuration + ', ' + CurrentShiftID + ', ' + ShiftDefID + ', 1, ' + TaskType + ', \'' + Descr + '\', ' + tmpMachineID + ', ' + tmpProductID + ', \'' + ShortDate(NowGMT(), True, True) + '\', ' + self.__pMachine.ActiveJobID + ', ' + self.__pMachine.ActiveJoshID + ')'
            CN.Execute(strSQL)
            
            UserTaskID = MdlADOFunctions.fGetRstValLong(GetSingleValue('ID', 'TblUserTasks', 'TaskDefID=' + TaskDefID + ' ORDER BY ID DESC', 'CN'))
            strSQL = 'Select QualificationID, BasicSkillLevel From TblTaskDefQualifications Where TaskDefID = ' + TaskDefID
            SkillRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            SkillRst.ActiveConnection = None
            while not SkillRst.EOF:
                strSQL = 'Insert TblUserTasksQualifications(UserTaskID, TaskDefID, QualificationID, BasicSkillLevel) VALUES(' + UserTaskID + ', ' + TaskDefID + ', ' + SkillRst.Fields("QualificationID").Value + ', ' + SkillRst.Fields("BasicSkillLevel").Value + ')'
                CN.Execute(strSQL)
                SkillRst.MoveNext()
            SkillRst.Close()
        Rst.Close()
        strSQL = 'Update TblTaskTrigger Set LastFireTime = \'' + ShortDate(NowGMT(), True, True) + '\', LastFireValue=\'' + self.__LastFireValue + '\''
        strSQL = strSQL + ' Where (MachineID = ' + self.__pMachine.ID + ' OR ProductID = ' + self.__pMachine.ActiveProductID + ') AND TaskDef = ' + TaskDefID + ' AND TaskTriggerDefID=' + self.__TriggerDefID
        
        CN.Execute(strSQL)
        self.__LastFireTime = ShortDate(NowGMT(), False, True)
        returnVal = True
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('TaskTriggerFireTrigger', Err.Number, Err.Description, 'Cant fire trigger ' + self.__ID)
        if Rst.State != 0:
            Rst.Close()
        if SkillRst.State != 0:
            SkillRst.Close()
        Rst = None
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
