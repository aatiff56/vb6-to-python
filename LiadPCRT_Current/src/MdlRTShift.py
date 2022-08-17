from Shift import Shift

import MdlADOFunctions
import MdlConnection
import MdlGlobal
import mdl_Common
import MdlUtils

def fCalcShiftChange(tserver):
    returnVal = None
    RstCursor = None
    strSQL = ''
    CurrentShiftID = 0
    CurrentShiftDef = 0
    NextShiftDef = 0
    lngRet = 0
    LngStat = 0
    NextShiftFound = 0
    CWDay = 0.0
    CTime = 0.0
    ShiftEndTime = 0.0
    ShiftStartTime = 0.0
    LastWeekShift = False
    NewShiftID = 0
    RotateSMNow = False
    AutoResetMachines = False
    tShift = None
    tNextShiftDefID = 0
    tNeedToFindCurrentShift = False
    tCurrentShiftID = 0
    tCurrentShiftDefID = 0
    RotateSMNow = False
    returnVal = False
    
    try:
        if tserver.SystemVariables.FirstDayOfWeek == 'Monday':
            CWDay = mdl_Common.DateGMT().weekday()
        else:
            CWDay = (mdl_Common.DateGMT().weekday() + 1) % 7

        CTime = mdl_Common.TimeGMT()
        CTime = CWDay + CTime
        if tserver.SCID > 0:
            tCurrentShiftID = tserver.CurrentShiftID
            tCurrentShiftDefID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CurrentShiftDefID', 'STblShiftCalendar', 'ID = ' + str(tserver.SCID), 'CN'))
        else:
            strSQL = 'SELECT * From STblSystemVariables'
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                tCurrentShiftID = MdlADOFunctions.fGetRstValLong(RstData.CurrentShiftID)
                tCurrentShiftDefID = MdlADOFunctions.fGetRstValLong(RstData.CurrentShiftDef)
            RstCursor.close()

        if tCurrentShiftDefID != 0:
            strSQL = 'SELECT * FROM TblShiftDef WHERE ID = ' + str(tCurrentShiftDefID) + ' AND IsActive <> 0'
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                ShiftEndTime = MdlADOFunctions.fGetRstValDouble(RstData.EndCalcNum)
                ShiftStartTime = MdlADOFunctions.fGetRstValDouble(RstData.StartCalcNum)
                NextShiftDef = MdlADOFunctions.fGetRstValLong(RstData.NextShiftDef)
            RstCursor.close()
            
        if ShiftStartTime > ShiftEndTime:
            LastWeekShift = True
            if CTime >= 7:
                CTime = 0
            else:
                CTime = CTime
        
        if ( tCurrentShiftID == 0 and tCurrentShiftDefID == 0 ) or ( CTime >= ShiftEndTime ) or ( CTime < ShiftStartTime and ShiftStartTime > ShiftEndTime and LastWeekShift == False ):
            tNeedToFindCurrentShift = True
        if LastWeekShift == False:
            if not ( ( CTime >= ShiftStartTime )  and  ( CTime <= ShiftEndTime ) ) :
                tNeedToFindCurrentShift = True
        
        if tNeedToFindCurrentShift:            
            NextShiftFound = 0
            if tserver.SCID > 0:
                strSQL = 'Select * From TblShiftDef Where ID > 0 AND IsActive <> 0 AND ShiftCalendarID = ' + str(tserver.SCID)
            else:
                strSQL = 'Select * From TblShiftDef Where ID > 0 AND IsActive <> 0'
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()

            for RstData in RstValues:
                if NextShiftFound == 0:
                    if tserver.SystemVariables.FirstDayOfWeek == 'Monday':
                        CWDay = mdl_Common.DateGMT().weekday()
                    else:
                        CWDay = (mdl_Common.DateGMT().weekday() + 1) % 7
                    CTime = mdl_Common.TimeGMT()
                    CTime = CWDay + CTime
                    ShiftEndTime = MdlADOFunctions.fGetRstValDouble(RstData.EndCalcNum)
                    ShiftStartTime = MdlADOFunctions.fGetRstValDouble(RstData.StartCalcNum)
                    if ShiftStartTime > ShiftEndTime:
                        ShiftEndTime = ShiftEndTime + 7
                        
                    if ( CTime >= ShiftStartTime )  and  ( CTime <= ShiftEndTime ) :
                        NextShiftFound = 1
                        NextShiftDef = MdlADOFunctions.fGetRstValLong(RstData.ID)
            RstCursor.close()
            if ( NextShiftFound == 1 ) :
                AutoResetMachines = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('AutoResetMachines', 'TblShiftDef', 'ID = ' + str(CurrentShiftDef), 'CN'), False)
                if AutoResetMachines:
                    fAutoResetMachines(tserver.SCID, tserver)
                
                RotateSMNow = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('RotateShiftManagers', 'TblShiftDef', 'ID = ' + str(CurrentShiftDef), 'CN'), False)
                if RotateSMNow:
                    RotateShiftManagers(tserver.SCID)
                
                fShiftChange(mdl_Common.NowGMT(), tserver, tCurrentShiftID, NextShiftDef)
                if tserver.SCID > 0:
                    NewShiftID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CurrentShiftID', 'STblShiftCalendar', 'ID = ' + str(tserver.SCID), 'CN'))
                else:
                    NewShiftID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CurrentShiftID', 'STblSystemVariables', 'ID=1', 'CN'))
                tserver.CurrentShiftID = NewShiftID
                tserver.ClearUserMessages()
                
                strSQL = 'DELETE FROM TblSystemAlarms WHERE ShiftID <> 0 AND ShiftID IN(SELECT ID FROM TblShift WHERE EndTime IS NOT NULL AND ShiftCalendarID = ' + str(tserver.SCID) if tserver.SCID > 0 else str(1) + ')'
                MdlConnection.CN.execute(strSQL)
                UpdateShiftManagers(tCurrentShiftID, NewShiftID, NextShiftDef)
        else:
            if tserver.CurrentShift is None:
                tShift = Shift()
                tShift.Init(tCurrentShiftID)
                tserver.CurrentShift = tShift
        returnVal = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('LeaderRT:fCalcShiftChange', str(0), error.args[0], 'CurrentShiftID: ' + str(CurrentShiftID) + 'NextShiftDef: ' + str(NextShiftDef))
        
    
    # if RstCursor:
    #     RstCursor.close()
    RstCursor = None
    return returnVal

def RotateShiftManagers(SCID):
    RstCursor = None
    strSQL = ''
    ArrUsers = []
    i = 0
    tmpLng = 0
    pos = 0
    RotationOrder = 0

    try:
        if SCID == 0:
            raise Exception('SCID is 0 in RotateShiftManagers()')
        RotationOrder = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('SMRotationOrder', 'STblShiftCalendar', 'ID = ' + str(SCID), 'CN'))
        
        if RotationOrder == 1:
            strSQL = 'UPDATE TblShiftDef'
            strSQL = strSQL + ' SET ManagerUserID = (SELECT NextManagerUserID FROM ViewShiftManagersRotation WHERE ViewShiftManagersRotation.ID = TblShiftDef.ID)'
            strSQL = strSQL + ' WHERE FixManagerUserID = 0 AND ShiftCalendarID = ' + str(SCID)
        elif RotationOrder == 2:
            strSQL = 'UPDATE TblShiftDef'
            strSQL = strSQL + ' SET ManagerUserID = (SELECT PreviousManagerUserID FROM ViewShiftManagersRotation WHERE ViewShiftManagersRotation.ID = TblShiftDef.ID)'
            strSQL = strSQL + ' WHERE FixManagerUserID = 0 AND ShiftCalendarID = ' + str(SCID)
        else:
            strSQL = 'UPDATE TblShiftDef'
            strSQL = strSQL + ' SET ManagerUserID = (SELECT NextManagerUserID FROM ViewShiftManagersRotation WHERE ViewShiftManagersRotation.ID = TblShiftDef.ID)'
            strSQL = strSQL + ' WHERE FixManagerUserID = 0 AND ShiftCalendarID = ' + str(SCID)
        MdlConnection.CN.execute(strSQL)

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('RotateShiftManagers:', str(0), error.args[0], '')

    if RstCursor:
        RstCursor.close()
    RstCursor = None

def fGetIDStringForSC(SCID, DataSourceTable, SCFieldName='ShiftCalendarID', IDFieldName='ID', AdditionalWhereCon=''):
    returnVal = None
    RstCursor = None

    strSQL = ''
    
    
    returnVal = ''
    if AdditionalWhereCon != '':
        strSQL = 'Select ' + IDFieldName + ' from ' + DataSourceTable + ' Where (' + SCFieldName + ' = ' + SCID + ' AND ' + AdditionalWhereCon + ')'
    else:
        strSQL = 'Select ' + IDFieldName + ' from ' + DataSourceTable + ' Where ' + SCFieldName + ' = ' + SCID
    
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    while not Rst.EOF:
        returnVal = fGetIDStringForSC() + Rst.Fields(IDFieldName).value + ', '
        Rst.MoveNext()
    if fGetIDStringForSC() != '':
        returnVal = Left(fGetIDStringForSC(), Len(fGetIDStringForSC()) - 2)
    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            
        MdlGlobal.RecordError('LeaderRT:fGetIDStringForSC', str(0), error.args[0], strSQL + ';' + fGetIDStringForSC())
        returnVal = ''
    RstCursor = None
    return returnVal


def fShiftChange(EndTimeForOldShift, tserver, OldShift=0, NewShiftDef=0, ManagerID=0):
    returnVal = None
    strSQL = ''

    situation = 0

    NewShiftID = 0

    OldJoshID = 0

    JoshID = 0

    SetupDuration = 0.0

    NewJoshID = 0

    JobID = 0

    ShiftDefID = 0

    Counter = 0

    tMachine = Machine()

    DepForSC = ''

    tVariant = Variant()

    tVariant2 = Variant()

    tChildJob = Job()

    ShiftUnitsTarget = 0.0
    
    returnVal = False
    if OldShift != 0 and NewShiftDef != 0:
        situation = 1
    if OldShift != 0 and NewShiftDef == 0:
        situation = 2
    if OldShift == 0 and NewShiftDef != 0:
        situation = 3
    if situation != 3:
        
        tserver.WriteAllMachines(False)
    if situation != 2:
        if not fAddNewShift(tserver, EndTimeForOldShift, OldShift, NewShiftDef, ManagerID):
            Err.Raise(1)
    if (situation == 1):
        for tVariant in tserver.Machines:
            tMachine = tVariant
            if not tMachine.ActiveJob is None:
                
                fCopyJobRecipeToJoshRecipe(tMachine.ActiveJob.ID, tMachine.ActiveJosh.ID)
                tMachine.ActiveJob.CreateJoshForNewShift
                if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
                    for tVariant2 in tMachine.ActiveJob.PConfigJobs:
                        tChildJob = tVariant2
                        tChildJob.CreateJoshForNewShift
            tMachine.BatchReadLastRecord = 0
            
            ShiftUnitsTarget = MdlADOFunctions.GetSingleValue('TargetValue', 'TblMachineShiftDefTarget', 'MachineID = ' + tMachine.ID + ' AND ShiftDefID = ' + NewShiftDef, 'CN')
            if ShiftUnitsTarget > 0:
                strSQL = 'UPDATE TblMachines SET ShiftUnitsTarget = ' + ShiftUnitsTarget + ' WHERE ID = ' + tMachine.ID
                MdlConnection.CN.execute(strSQL)
            tMachine.UpdateShiftMachineCycleTime(tserver.CurrentShiftID)
        
        
        
        gServer.fClearAlarms(tserver.SCID)
        returnVal = True
        
        gServer.CleanUnusedObjects
    
    strSQL = 'UPDATE TblCalendarExceptions SET IsActive = 0 WHERE DateTo <= \'' + ShortDate(EndTimeForOldShift, True, True) + '\''
    MdlConnection.CN.execute(strSQL)
    if tserver.SCID != 0:    
        pass
    else:
        if NewShiftID > 0:
            strSQL = 'Delete TblJoshCurrentMaterial Where ShiftID <> ' + NewShiftID
            MdlConnection.CN.execute(strSQL)
        
        if NewShiftID > 0:
            strSQL = 'Delete TblJoshCurrent Where ShiftID <> ' + NewShiftID
            MdlConnection.CN.execute(strSQL)
    
    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            
        MdlGlobal.RecordError('LeaderRT:fShiftChange', str(0), error.args[0], strSQL)
        
    return returnVal

def fAddNewShift(tserver, EndTimeForOldShift, pOldShift, pNewShiftDef, ManagerID=0):
    returnVal = None
    strSQL = ''

    NewShift = 0

    tShift = None
    
    returnVal = False
    if pOldShift == 0:
        if tserver.SCID > 0:
            pOldShift = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CurrentShiftID', 'STblShiftCalendar', 'ID = ' + tserver.SCID))
        else:
            pOldShift = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CurrentShiftID', 'STblSystemVariables', 'ID=1'))
    tShift = None
    tShift.Create(pNewShiftDef)
    
    if pOldShift > 0:
        tserver.CurrentShift.CloseShift(tShift.ID)
    tserver.CurrentShift = tShift
    tserver.CurrentShiftID = tShift.ID
    returnVal = True
    if Err.Number != 0:
        MdlGlobal.RecordError('LeaderRT:fAddNewShift', str(0), error.args[0], strSQL)
        
    return returnVal

def fAutoResetMachines(SCID, tserver):
    returnVal = False
    rstJOBSCursor = None
    strSQL = ''

    try:
        strSQL = 'Select TblJob.ID AS JobID, TblMachines.AutoResetShiftTarget AS AutoResetShiftTarget, TblMachines.ID AS MachineID  From STblDepartments Inner Join TblMachines ON STblDepartments.ID = TblMachines.Department '
        strSQL = strSQL + ' INNER JOIN TblJob ON TblMachines.ID = TblJob.MachineID Where STblDepartments.ShiftCalendarID = ' + str(SCID) + ' AND TblJob.Status = 10 AND TblMachines.AutoResetOnShiftChange <> 0'

        rstJOBSCursor = MdlConnection.CN.cursor()
        rstJOBSCursor.execute(strSQL)
        rstJOBSValues = rstJOBSCursor.fetchall()

        for rstJOBSData in rstJOBSValues:
            strSQL = 'UPDATE TblJob SET UnitsTarget = ' + str(rstJOBSData.AutoResetShiftTarget) + ' Where MachineID = ' + str(rstJOBSData.MachineID) + ' AND Status = 10'
            MdlConnection.CN.execute(strSQL)
            strSQL = 'UPDATE TblJobCurrent SET UnitsTarget = ' + str(rstJOBSData.AutoResetShiftTarget) + ' Where MachineID = ' + str(rstJOBSData.MachineID) + ' AND Status = 10'
            MdlConnection.CN.execute(strSQL)
            if tserver.ResetMachineByID(rstJOBSData.MachineID) == False:
                raise Exception('Could not Reset Machine By ID in fAutoResetMachines()')

        rstJOBSCursor.close()
        returnVal = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
    # if rstJOBSCursor:
    #     rstJOBSCursor.Close()
    rstJOBSCursor = None
    return returnVal

def fCopyJobRecipeToJoshRecipe(JobID, JoshID):
    returnVal = None
    strSQL = ''

    JobRecipeRstCursor = None

    JoshRecipeRstCursor = None

    Field = ADODB.Field()

    MachineID = 0

    RecordJoshRecipe = False
    
    MachineID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineID', 'TblJosh', 'ID = ' + JoshID, 'CN'))
    if MachineID == 0:
        JobRecipeRstCursor = None
        JoshRecipeRstCursor = None
        return returnVal
    else:
        RecordJoshRecipe = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('RecordJoshRecipe', 'TblMachines', 'ID = ' + MachineID, 'CN'), False)
        if not RecordJoshRecipe:
            JobRecipeRstCursor = None
            JoshRecipeRstCursor = None
            return returnVal
    
    strSQL = 'Delete From TblProductRecipeJosh Where JoshID = ' + JoshID
    MdlConnection.CN.execute(strSQL)
    
    strSQL = 'SELECT * From TblProductRecipeJob Where JobID = ' + JobID
    JobRecipeRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    JobRecipeRst.ActiveConnection = None
    
    strSQL = 'SELECT * From TblProductRecipeJosh Where JoshID = ' + JoshID
    JoshRecipeRst.Open(strSQL, CN, adOpenDynamic, adLockOptimistic)
    while not JobRecipeRst.EOF:
        JoshRecipeRst.AddNew()
        JoshRecipeRstData.JoshID = JoshID
        for Field in JobRecipeRst.Fields:
            if Field.Name != 'ID':
                JoshRecipeRst.Fields[Field.Name].value = Field.value
        JoshRecipeRst.Update()
        JobRecipeRst.MoveNext()
    JobRecipeRstCursor.close()
    JoshRecipeRstCursor.close()
    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            
        MdlGlobal.RecordError('MdlRTShift:fCopyJobRecipeToJoshRecipe', str(0), error.args[0], 'JobID: ' + JobID + ' JoshID: ' + JoshID)
    JobRecipeRstCursor = None
    JoshRecipeRstCursor = None
    return returnVal

def UpdateShiftManagers(OldShiftID, NewShiftID, NewShiftDefID):
    returnVal = False
    strSQL = ''
    RstCursor = None
    IsShiftManagerFromShift = False
    IsDisconnectShiftManager = False
    ShiftManagerID = 0
    ShiftCalendarID = 0
    keys = {}
    values = {}
    NewRecID = 0

    try:
        strSQL = 'SELECT ID, IsShiftManagerFromShift, IsDisconnectShiftManager, ShiftCalendarID FROM TblShiftDef WHERE ID = ' + str(NewShiftDefID)
        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstData = RstCursor.fetchone()

        if RstData:
            IsShiftManagerFromShift = MdlADOFunctions.fGetRstValBool(RstData.IsShiftManagerFromShift, False)
            IsDisconnectShiftManager = MdlADOFunctions.fGetRstValBool(RstData.IsDisconnectShiftManager, False)
            ShiftCalendarID = MdlADOFunctions.fGetRstValLong(RstData.ShiftCalendarID)
        RstCursor.close()

        if IsShiftManagerFromShift:
            ShiftManagerID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ManagerUserID', 'TblShiftDef', 'ID = ' + NewShiftDefIDstr(), 'CN'))
            if ShiftManagerID > 0:
                strSQL = 'SELECT ID FROM STblDepartments WHERE ID > 0 IsActive = 1 AND ShiftCalendarID = ' + ShiftCalendarID
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstValues = RstCursor.fetchall()

                for RstData in RstValues:
                    keys.removeAll()
                    values.removeAll()
                    keys['ShiftID'] = NewShiftID
                    keys['DepartmentID'] = MdlADOFunctions.fGetRstValLong(RstData.ID)
                    values['ShiftID'] = NewShiftID
                    values['DepartmentID'] = MdlADOFunctions.fGetRstValLong(RstData.ID)
                    values['UserID'] = ShiftManagerID
                    MdlUtils.GenericUpsert(NewRecID, 'TblShiftManager', values, keys)
                RstCursor.close()

        elif not IsDisconnectShiftManager:
            strSQL = 'SELECT ID FROM STblDepartments WHERE ID > 0 AND IsActive = 1 AND ShiftCalendarID = ' + str(ShiftCalendarID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()

            for RstData in RstValues:
                ShiftManagerID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('UserID', 'TblShiftManager', 'ShiftID = ' + str(OldShiftID) + ' AND DepartmentID = ' + str(MdlADOFunctions.fGetRstValLong(RstData.ID)), 'CN'))
                keys.removeAll()
                values.removeAll()
                keys['ShiftID'] = NewShiftID
                keys['DepartmentID'] = MdlADOFunctions.fGetRstValLong(RstData.ID)
                values['ShiftID'] = NewShiftID
                values['DepartmentID'] = MdlADOFunctions.fGetRstValLong(RstData.ID)
                values['UserID'] = ShiftManagerID
                MdlUtils.GenericUpsert(NewRecID, 'TblShiftManager', values, keys)
            RstCursor.close()
        else:
            strSQL = 'SELECT ID FROM STblDepartments WHERE ID > 0 AND IsActive = 1 AND ShiftCalendarID = ' + str(ShiftCalendarID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()

            for RstData in RstValues:
                keys.removeAll()
                values.removeAll()
                keys['ShiftID'] = NewShiftID
                keys['DepartmentID'] = MdlADOFunctions.fGetRstValLong(RstData.ID)
                values['ShiftID'] = NewShiftID
                values['DepartmentID'] = MdlADOFunctions.fGetRstValLong(RstData.ID)
                values['UserID'] = 0
                MdlUtils.GenericUpsert(NewRecID, 'TblShiftManager', values, keys)
            RstCursor.close()
        returnVal = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
    # if RstCursor:
    #     RstCursor.close()
    RstCursor = None
    return returnVal

