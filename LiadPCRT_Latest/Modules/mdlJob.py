import MdlConnection
import MdlADOFunctions
import MdlGlobal

def fCalcCycleTime(tMachine):
    CyclesInterval = 0
    TSCyclesInterval = 0
    TSCycleTime = 0
    tParam = ControlParam()
    strSQL = ""
    TSCycleTimeNet = 0
    dbCursor = None
    
    try:
        if tMachine.GetParam('TotalCycles', tParam) == True:
            if tParam.LastSampleTime > tParam.PrevSampleTime:
                if tMachine.CalcCycleTime == True:
                    CyclesInterval = tMachine.TotalCycles - tMachine.TotalCyclesLast
                    TSCyclesInterval = DateDiff('s', tParam.PrevSampleTime, tParam.LastSampleTime)
                    if CyclesInterval != 0:
                        TSCycleTime = round(TSCyclesInterval /  ( CyclesInterval ), 3)
                    if TSCycleTime < tMachine.MaxCycleTime and CyclesInterval != 0:
                        tDuration = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('SUM(Duration)', 'TblEvent', 'PConfigParentID = 0 AND EventTime >= \'' + ShortDate(tParam.PrevSampleTime, True, True, True) + '\' AND EndTime <= \'' + ShortDate(tParam.LastSampleTime, True, True, True) + '\' AND MachineID = ' + tMachine.ID, 'CN'))
                        
                        TSCycleTimeNet = TSCycleTime -  ( tDuration * 60 )
                        tMachine.CycleTime = TSCycleTime
                        if tParam.DirectRead == False:
                            
                            dbCursor = MdlConnection.CN.cursor()
                            if dbCursor:
                                tMachine.SetFieldValue('CycleTime', str(TSCycleTime))
                                strSQL = 'UPDATE TblControllerFields SET CurrentValue = ' + tMachine.CycleTime + ' WHERE FieldName = \'CycleTime\' AND MachineID = ' + tMachine.ID
                                dbCursor.execute(strSQL)
                                
                                tMachine.SetFieldValue('CycleTimeNet', str(TSCycleTimeNet))
                                strSQL = 'UPDATE TblControllerFields SET CurrentValue = ' + TSCycleTimeNet + ' WHERE FieldName = \'CycleTimeNet\' AND MachineID = ' + tMachine.ID
                                dbCursor.execute(strSQL)
            tParam.PrevSampleTime = tParam.LastSampleTime

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
    if dbCursor:
        dbCursor.close()
    dbCursor = None


def fMaterialChangeCalc(vMachine, parameters):
    strSQL = ""
    MachineType = 0
    MaterialIDProperty = 0
    temp = ""
    tmpMaterialID = 0
    timeToChangeMaterial = 0
    newJobMaterialID = 0
    TimeLeftHr = 0
    ChannelNum = 0
    SplitNum = 0
    tParam = ControlParam()
    jobDbCursor = None
    returnVal = 142000

    try:
        ChannelNum = Left(parameters, 1)
        SplitNum = Right(parameters, 1)
        
        if vMachine.GetParam('TimeLeftHr', tParam) == True:
            TimeLeftHr = MdlADOFunctions.fGetRstValDouble(tParam.LastValue)
        else:
            TimeLeftHr = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('CurrentValue', 'TblControllerFields', 'ControllerID = ' + vMachine.ControllerID + ' And FieldName = \'TimeLeftHr\'', 'CN'))
        
        temp = '' + MdlADOFunctions.GetSingleValue('ID', 'STblMachineTypeProperties', 'PropertyName = \'Material ID\' AND MachineType = ' + vMachine.TypeId)
        if temp.isnumeric():
            MaterialIDProperty = int(temp)
        timeToChangeMaterial = TimeLeftHr
        
        strSQL = 'MachineID = ' + vMachine.ID + ' And JobID = ' + vMachine.ActiveJobID + ' And ChannelNum = ' + ChannelNum
        strSQL = strSQL + ' And SplitNum = ' + SplitNum + ' And PropertyID = ' + MaterialIDProperty
        tmpMaterialID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('FValue', 'TblProductRecipeJob', strSQL, 'CN'))
        
        if tmpMaterialID > 0:
            strSQL = 'Select ID, TimeLeftHr From TblJob Where MachineID = ' + vMachine.ID + ' And (Status = 2 or Status = 3 or Status = 11) Order by MachineJobOrder ASC'
            jobDbCursor = MdlConnection.CN.cursor()
            if jobDbCursor:
                while jobDbCursor.next():
                    val = jobDbCursor.fetchone()
                    strSQL = 'MachineID = ' + vMachine.ID + ' And JobID = ' + val["ID"] + ' And ChannelNum = ' + ChannelNum
                    strSQL = strSQL + ' And SplitNum = ' + SplitNum + ' And PropertyID = ' + MaterialIDProperty
                    newJobMaterialID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('FValue', 'TblProductRecipeJob', strSQL, 'CN'))
                    if tmpMaterialID != newJobMaterialID:
                        timeToChangeMaterial = timeToChangeMaterial
                        break
                    else:
                        timeToChangeMaterial = timeToChangeMaterial + MdlADOFunctions.fGetRstValDouble(val["TimeLeftHr"])
                    jobDbCursor.execute(strSQL)
        returnVal = timeToChangeMaterial

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('fMaterialChangeCalc', 0, error.args[0], '')

    if jobDbCursor:
        jobDbCursor.Close()
    jobDbCursor = None

    return returnVal



