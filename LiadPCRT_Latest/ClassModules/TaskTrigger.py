from datetime import datetime
from Common import MdlADOFunctions as adoFunc
from LiadPCUnite.DataAccess import QueryExecutor as qe
from LiadPCUnite.BusinessLogic import SqlConnector as sc
from LiadPCUnite.Global import Logs

class TaskTrigger:
    sqlCntr = sc.SqlConnector()
    logger = Logs.Logger()
    
    Timeinterval = 1
    ValueGT = 2
    ValueLT = 3
    ValueInterval = 4
    SpecificDay = 5
    
    value = 1
    ControllerField = 2
    JobField = 3
    MachineMemberField = 4
    TaskDefID = 0
    TriggerDefID = 0
    FireTriggerWhileSetup = False
    IntervalType = TaskTriggerIntervalType()
    IntervalRelation = TaskTriggerIntervalRelation()
    IntervalRelationTarget = ''
    IntervalValue = ''
    ProductID = 0
    MachineID = 0
    MoldID = 0
    LastFireTime = datetime.date()
    LastFireValue = 0
    ResetOnNewJob = False
    ID = 0
    IntervalFromLastFire = 0
    pMachine = Machine()
    RelatedControlParam = ControlParam()
    FirstCheckDone = False
    TriggerFired = False
    NextFireTime = datetime.date()
    SpecificWeekDay = 0
    SpecificTime = datetime.date()
    EventTypeID = 0

    def __init__(self):
        
        self.FirstCheckDone = False
        self.TriggerFired = False

    def Init(self, TaskDef, TaskTriggerDefID, vMachine):
        try:
            strSQL = ''
            TriggerRST = qe.QueryExecutor(self.sqlCntr.GetConnection())

            Rst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            fn_return_value = False

            strSQL = 'Select * From TblTaskTriggerDef Where ID = ' + TaskTriggerDefID
            RstData = Rst.SelectAllData(strSQL)
            self.sqlCntr.OpenConnection()
            if not RstData.RecordCount > 0:
                raise Exception('Invalid operation')
            
            strSQL = 'Select * From TblTaskTrigger Where TaskDef = ' + TaskDef + ' AND MachineID = ' + vMachine.ID + ' AND TaskTriggerDefID = ' + TaskTriggerDefID
            TriggerRSTData = Rst.SelectAllData(strSQL)
            if TriggerRST.State != 0:
                TriggerRST.Close()
            self.sqlCntr.OpenConnection()
            if TriggerRST.RecordCount == 0:
                TriggerRST.AddNew()
            else:
                if adoFunc.fGetRstValBool(TriggerRSTData["ResetOnNewJob"], False) == False:
                    if TriggerRSTData["LastFireTime"] != None:
                        self.LastFireTime = datetime.strptime(TriggerRSTData["LastFireTime"], "%Y-%m-%d")
                    if TriggerRSTData["LastFireValue"] != None:
                        self.LastFireValue = '' + TriggerRSTData["LastFireValue"]
                else:
                    if TriggerRSTData["LastFireTime"] != None:\
                        self.LastFireTime = datetime.strptime(TriggerRSTData["LastFireTime"], "%Y-%m-%d")
                    if TriggerRSTData["LastFireValue"] != None:
                        self.LastFireValue = '' + TriggerRSTData["LastFireValue"]
            TriggerRSTData["TaskTriggerDefID"] = TaskTriggerDefID
            TriggerRSTData["TaskDef"] = TaskDef
            TriggerRSTData["IntervalType"] = RstData["IntervalType"]
            TriggerRSTData["IntervalRelation"] = RstData["IntervalRelation"]
            TriggerRSTData["IntervalRelationTarget"] = RstData["IntervalRelationTarget"]
            TriggerRSTData["MachineID"] = vMachine.ID
            TriggerRSTData["ResetOnNewJob"] = RstData["ResetOnNewJob"]
            TriggerRSTData["FireTriggerWhileSetup"] = RstData["FireTriggerWhileSetup"]
            TriggerRSTData["SpecificWeekDay"] = RstData["SpecificWeekDay"]
            TriggerRSTData["SpecificTime"] = RstData["SpecificTime"]
            TriggerRSTData["EventTypeID"] = RstData["EventTypeID"]
            
            if RstData["ProductGroup"] != None:
                TriggerRSTData["ProductGroup"] = RstData["ProductGroup"]
            if RstData["ProductID"] != None:
                TriggerRSTData["ProductID"] = RstData["ProductID"]
            if RstData["MachineGroup"] != None:
                TriggerRSTData["MachineGroup"] = RstData["MachineGroup"]
            if RstData["MoldGroup"] != None:
                TriggerRSTData["MoldGroup"] = RstData["MoldGroup"]
            if RstData["QualityGroup"] != None:
                TriggerRSTData["QualityGroup"] = RstData["QualityGroup"]
            if RstData["JobField"] != '':
                TriggerRSTData["JobField"] = RstData["JobField"]
            if RstData["JobFieldValue"] != '':
                TriggerRSTData["JobFieldValue"] = RstData["JobFieldValue"]
            TriggerRST.Update()
            self.ID = TriggerRSTData["ID"]
            TriggerRST.Close()
            self.TaskDefID = TaskDef
            self.TriggerDefID = TaskTriggerDefID
            self.IntervalType = RstData["IntervalType"]
            if self.IntervalType == SpecificDay:
                self.SpecificWeekDay = RstData["SpecificWeekDay"]
                self.SpecificTime = RstData["SpecificTime"]
                self.NextFireTime = fGetNextTriggerDate(self.SpecificWeekDay, self.SpecificTime)
            self.IntervalRelation = RstData["IntervalRelation"]
            if adoFunc.fGetRstValString(RstData["IntervalRelationTarget"]) != '':
                self.IntervalRelationTarget = RstData["IntervalRelationTarget"]
            self.ProductID = adoFunc.fGetRstValLong(RstData["ProductID"])
            self.MachineID = adoFunc.fGetRstValLong(RstData["MachineID"])
            self.ResetOnNewJob = RstData["ResetOnNewJob"]
            self.FireTriggerWhileSetup = adoFunc.fGetRstValBool(RstData["FireTriggerWhileSetup"], True)
            
            self.EventTypeID = adoFunc.fGetRstValLong(RstData["EventTypeID"])
            self.pMachine = vMachine
            select_variable_0 = self.IntervalRelation
            if (select_variable_0 == TaskTriggerIntervalRelation.ControllerField):
                if vMachine.GetParam(self.IntervalRelationTarget, self.RelatedControlParam) == False:
                    raise Exception('Invalid operation')
                self.IntervalValue = RstData["IntervalSourceValue"]
                
            elif (select_variable_0 == TaskTriggerIntervalRelation.JobField):
                self.IntervalValue = RstData["IntervalSourceValue"]
            elif (select_variable_0 == TaskTriggerIntervalRelation.MachineMemberField):
                self.IntervalValue = RstData["IntervalSourceValue"]
            elif (select_variable_0 == TaskTriggerIntervalRelation.value):
                self.IntervalValue = RstData["IntervalSourceValue"]
            Rst.Close()
            fn_return_value = True
                
            if Rst.State != 0:
                Rst.Close()
            Rst = None
            if TriggerRST.State != 0:
                TriggerRST.Close()
            TriggerRST = None
            return fn_return_value
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)
            return False

    def CheckInterval(self):
        try:
            tmpValue = 0
            RefValue = 0
            RefJobValue = ''
            strSQL = ''
            TriggerRST = qe.QueryExecutor(self.sqlCntr.GetConnection())
            ErrCount = 0
            select_variable_1 = self.IntervalRelation

            if (select_variable_1 == TaskTriggerIntervalRelation.ControllerField):
                RefValue = self.RelatedControlParam.LastValue
            elif (select_variable_1 == TaskTriggerIntervalRelation.JobField):
                RefValue = adoFunc.GetSingleValue(self.IntervalRelationTarget, 'TblJob', 'ID = ' + self.pMachine.ActiveJobID)
                
            elif (select_variable_1 == TaskTriggerIntervalRelation.MachineMemberField):
                select_variable_2 = self.IntervalRelationTarget
                if (select_variable_2 == 'NoProgressCount'):
                    RefValue = self.pMachine.NoProgressCount
            elif (select_variable_1 == TaskTriggerIntervalRelation.value):
                RefValue = self.IntervalValue
            fn_return_value = False
            select_variable_3 = self.IntervalType
            if (select_variable_3 == TaskTriggerIntervalType.Timeinterval):
                
                if DateDiff('n', self.LastFireTime, datetime.now()) >= int(self.IntervalValue):
                    fn_return_value = True
            elif (select_variable_3 == TaskTriggerIntervalType.ValueGT):
                tmpValue = RefValue
                if tmpValue > float(self.IntervalValue):
                    if self.TriggerFired == False:
                        fn_return_value = True
                        self.LastFireValue = tmpValue
                else:
                    self.TriggerFired = False
            elif (select_variable_3 == TaskTriggerIntervalType.ValueInterval):
                tmpValue = float(RefValue)
                if abs(tmpValue - self.LastFireValue) >= abs(float(self.IntervalValue)):
                    if ( self.LastFireValue == 0 )  and  ( tmpValue / float(self.IntervalValue) )  >= 2:
                        self.LastFireValue = 0
                        fn_return_value = False
                    else:
                        self.LastFireValue = tmpValue
                        fn_return_value = True
            elif (select_variable_3 == TaskTriggerIntervalType.ValueLT):
                tmpValue = float(RefValue)
                if tmpValue < float(self.IntervalValue):
                    if self.TriggerFired == False:
                        fn_return_value = True
                else:
                    self.TriggerFired = False
            elif (select_variable_3 == TaskTriggerIntervalType.SpecificDay):
                if datetime.now() >= self.NextFireTime:
                    fn_return_value = True
                    self.NextFireTime = fGetNextTriggerDate(self.SpecificWeekDay, self.SpecificTime)
                else:
                    fn_return_value = False
            
            if self.IntervalRelation == TaskTriggerIntervalRelation.JobField:
                if self.ProductID != 0:
                    if self.ProductID != self.pMachine.ActiveJob.ProductID:
                        ErrCount = ErrCount + 1
                strSQL = 'Select * From TblTaskTrigger Where TaskDef = ' + self.TaskDefID + ' AND MachineID = ' + self.pMachine.ID + ' AND TaskTriggerDefID = ' + self.TriggerDefID
                
                self.sqlCntr.OpenConnection()
                TriggerRSTData = TriggerRST.SelectAllData(strSQL)
                TriggerRSTData.ActiveConnection = None
                if TriggerRSTData.RecordCount == 1:
                    if TriggerRSTData['QualityGroup'] != None:
                        RefValue = adoFunc.fGetRstValLong(adoFunc.GetSingleValue('QualityGroup', 'TblProduct', ' ID = ' + self.pMachine.ActiveJob.ProductID))
                        if TriggerRSTData['QualityGroup'] != 0:
                            ErrCount = ErrCount + 1
                    if TriggerRSTData['MachineGroup'] != None:
                        RefValue = adoFunc.fGetRstValLong(adoFunc.GetSingleValue('MachineGroupID', 'TblMachines', ' ID = ' + self.pMachine.ID))
                        if TriggerRSTData['MachineGroup'] != RefValue:
                            ErrCount = ErrCount + 1
                    if TriggerRSTData['ProductGroup'] != None:
                        RefValue = adoFunc.fGetRstValLong(adoFunc.GetSingleValue('ProductGroup', 'TblProduct', ' ID = ' + self.pMachine.ActiveJob.ProductID))
                        if TriggerRSTData['ProductGroup'] != RefValue:
                            ErrCount = ErrCount + 1
                    if TriggerRSTData['JobField'] != None:
                        RefJobValue = adoFunc.fGetRstValString(adoFunc.GetSingleValue(TriggerRSTData['JobField'], 'TblJob', 'ID = ' + self.pMachine.ActiveJobID))
                        if TriggerRSTData['JobFieldValue'] != RefJobValue:
                            ErrCount = ErrCount + 1
            
            if ErrCount == 0:
                if self.CheckInterval() == True:
                    fn_return_value = True
                else:
                    if self.IntervalType == 0:
                        fn_return_value = True
                    else:
                        fn_return_value = False
            else:
                if ErrCount != 0:
                    fn_return_value = False
            return fn_return_value
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)
            return False


    def FireTrigger(self):
        try:
            strSQL = ''
            Rst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            SkillRst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            Descr = ''
            BasicPriority = 0
            StandardDuration = 0
            TaskType = 0
            CurrentShiftID = 0
            ShiftDefID = 0
            tmpMachineID = 0
            tmpProductID = 0
            UserTaskID = 0
            TaskDefID = 0
            tOpenNewTask = False
            fn_return_value = False        
            tOpenNewTask = adoFunc.fGetRstValBool(adoFunc.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'OpenNewTriggerTask\'', 'CN'), False)
            
            strSQL = 'Select ID, Descr, BasicPriority, StandardDuration, TaskType From TblTaskDef Where ID = ' + self.PTaskDefID
            self.sqlCntr.OpenConnection()
            RstData = Rst.SelectAllData(strSQL)
            RstData.ActiveConnection = None
            if not RstData.RecordCount > 0:
                raise Exception('Invalid operation')
            TaskDefID = adoFunc.fGetRstValLong(RstData["ID"])
            Descr = '' + RstData["Descr"]
            BasicPriority = adoFunc.fGetRstValDouble(RstData["BasicPriority"])
            StandardDuration = adoFunc.fGetRstValDouble(RstData["StandardDuration"])
            TaskType = adoFunc.fGetRstValLong(RstData["TaskType"])
            Rst.Close()
            tmpMachineID = self.pMachine.ID
            tmpProductID = self.pMachine.ActiveJob.Product.ID
            CurrentShiftID = self.pMachine.Server.CurrentShiftID
            ShiftDefID = self.pMachine.Server.ShiftCalendar.CurrentShiftDefID
            
            if self.ResetOnNewJob:
                strSQL = 'Select ID From TblUserTasks Where (JobID = ' + self.pMachine.ActiveJobID + ') AND (MachineID = ' + self.pMachine.ID + ' OR ProductID = ' + self.pMachine.ActiveProductID + ') AND TaskDefID = ' + TaskDefID + ' AND Status < 3'
            else:
                strSQL = 'Select ID From TblUserTasks Where (MachineID = ' + self.pMachine.ID + ' OR ProductID = ' + self.pMachine.ActiveProductID + ') AND TaskDefID = ' + TaskDefID + ' AND Status < 3'
            self.sqlCntr.OpenConnection()
            Rst.ActiveConnection = None
            if Rst.RecordCount == 0 or tOpenNewTask == True:
                
                strSQL = 'Insert TblUserTasks (TaskDefID, PriorityLevel, StandardDuration, ShiftID, ShiftDef, Status, TaskType, Descr, MachineID, ProductID, InvokeTime, JobID, JoshID) '
                strSQL = strSQL + ' VALUES(' + TaskDefID + ', ' + BasicPriority + ', ' + StandardDuration + ', ' + CurrentShiftID + ', ' + ShiftDefID + ', 1, ' + TaskType + ', \'' + Descr + '\', ' + tmpMachineID + ', ' + tmpProductID + ', \'' + datetime.strptime(datetime.now(), "%Y-%m-%d") + '\', ' + self.pMachine.ActiveJobID + ', ' + self.pMachine.ActiveJoshID + ')'
                Rst.ManipulateData(strSQL)
                
                UserTaskID = adoFunc.fGetRstValLong(adoFunc.GetSingleValue('ID', 'TblUserTasks', 'TaskDefID=' + TaskDefID + ' ORDER BY ID DESC', 'CN'))
                strSQL = 'Select QualificationID, BasicSkillLevel From TblTaskDefQualifications Where TaskDefID = ' + TaskDefID
                self.sqlCntr.OpenConnection()
                SkillRst.ActiveConnection = None
                while not SkillRst.EOF:
                    strSQL = 'Insert TblUserTasksQualifications(UserTaskID, TaskDefID, QualificationID, BasicSkillLevel) VALUES(' + UserTaskID + ', ' + TaskDefID + ', ' + SkillRst.Fields("QualificationID"] + ', ' + SkillRst.Fields("BasicSkillLevel"] + ')'
                    Rst.ManipulateData(strSQL)
                    SkillRst.MoveNext()
                SkillRst.Close()
            Rst.Close()
            strSQL = 'Update TblTaskTrigger Set LastFireTime = \'' + datetime.strptime(datetime.now(), "%Y-%m-%d") + '\', LastFireValue=\'' + self.LastFireValue + '\''
            strSQL = strSQL + ' Where (MachineID = ' + self.pMachine.ID + ' OR ProductID = ' + self.pMachine.ActiveProductID + ') AND TaskDef = ' + TaskDefID + ' AND TaskTriggerDefID=' + self.TriggerDefID
            
            Rst.ManipulateData(strSQL)
            self.LastFireTime = datetime.strptime(datetime.now(), "%Y-%m-%d")
            fn_return_value = True
            if Rst.State != 0:
                Rst.Close()
            if SkillRst.State != 0:
                SkillRst.Close()
            Rst = None
            return fn_return_value
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)
            return False

    def getPTaskDefID(self):
        fn_return_value = self.TaskDefID
        return fn_return_value
    PTaskDefID = property(fget=getPTaskDefID)


    def getPTriggerDefID(self):
        fn_return_value = self.TriggerDefID
        return fn_return_value
    PTriggerDefID = property(fget=getPTriggerDefID)


    def setPFireTriggerWhileSetup(self, the_mPFireTriggerWhileSetup):
        self.FireTriggerWhileSetup = the_mPFireTriggerWhileSetup

    def getPFireTriggerWhileSetup(self):
        fn_return_value = self.FireTriggerWhileSetup
        return fn_return_value
    PFireTriggerWhileSetup = property(fset=setPFireTriggerWhileSetup, fget=getPFireTriggerWhileSetup)


    def setPEventTypeID(self, value):
        self.EventTypeID = value

    def getPEventTypeID(self):
        fn_return_value = self.EventTypeID
        return fn_return_value
    PEventTypeID = property(fset=setPEventTypeID, fget=getPEventTypeID)


    def setPIntervalType(self, the_mPIntervalType):
        self.IntervalType = the_mPIntervalType

    def getPIntervalType(self):
        fn_return_value = self.IntervalType
        return fn_return_value
    PIntervalType = property(fset=setPIntervalType, fget=getPIntervalType)

    
    
    
