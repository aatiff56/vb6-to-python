import MdlADOFunctions
import MdlConnection
import MdlGlobal

def PrepareDataForLabel(pLabelID, pObjectID, pLabelQueueID, pUserID):
    returnVal = None
    RstFields = None

    RstValues = None

    RstData = None

    tDataSource = ''

    tUserID = 0

    tObjectID = 0

    tHasRecipeFields = 0

    tRecipeRst = None

    tMachineTypeID = 0

    tDefaultOutputPackageTypeID = 0

    tLabelGroupID = 0

    tSourceTable = ''

    tSourceField = ''

    tSourceID = 0

    tEnumerator = 0
    
    returnVal = False
    strFields = ''
    strValues = ''
    tDataSource = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('JobDataSource', 'MetaTblLabels', 'ID = ' + pLabelID, 'MetaCN'))
    tLabelGroupID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('LabelGroupID', 'MetaTblLabels', 'ID = ' + pLabelID, 'MetaCN'))
    
    tUserID = pUserID
    if (tLabelGroupID == 1):
        tObjectID = pObjectID
    elif (tLabelGroupID == 2):
        pass
    elif (tLabelGroupID == 3):
        pass
    elif (tLabelGroupID == 4):
        pass
    elif (tLabelGroupID == 7):
        pass
    else:
        tObjectID = pObjectID
    
    tHasRecipeFields = MdlADOFunctions.GetSingleValue('COUNT(ID)', 'MetaTblLabelFields', 'DisplayType = N\'JobRecipe\' AND LabelID = ' + pLabelID, 'MetaCN')
    
    if tHasRecipeFields != 0:
        
        strSQL = 'SELECT * FROM ViewLabelJobRecipe WHERE JobID = ' + tObjectID
        tRecipeRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        tRecipeRst.ActiveConnection = None
    strSQL = 'SELECT * FROM ' + tDataSource + ' WHERE ID = ' + tObjectID
    RstData.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    RstData.ActiveConnection = None
    if RstData.RecordCount == 1:
        strSQL = 'SELECT * FROM MetaTblLabelFields WHERE LabelID = ' + pLabelID
        RstFields.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
        RstFields.ActiveConnection = None
        
        
        
        
        strSQL = 'SELECT * FROM MetaTblLabelFieldValues WHERE ID = 0'
        RstValues.Open(strSQL, MetaCn, adOpenDynamic, adLockOptimistic)
        while not RstFields.EOF:
            RstValues.AddNew()
            RstValues.Fields("UserID").Value = tUserID
            RstValues.Fields("LabelID").Value = pLabelID
            RstValues.Fields("FieldName").Value = RstFields.Fields("FieldName").Value
            RstValues.Fields("QueueID").Value = pLabelQueueID
            select_1 = UCase(RstFields.Fields("DisplayType").Value)
            if (select_1 == 'CALC'):
                RstValues.Fields("value").Value = PrepareCalculatedLabelField(MdlADOFunctions.fGetRstValString(RstFields.Fields("CalcFunction").Value), RstData)
            elif (select_1 == 'SYSTEMVAR'):
                
                RstValues.Fields("value").Value = PrepareSystemVarLabelField(MdlADOFunctions.fGetRstValString(RstFields.Fields("CalcFunction").Value), MdlADOFunctions.fGetRstValLong(RstData.Fields("ID").Value))
            elif (select_1 == 'NUMERATOR'):
                tValue = RaiseLabelNumerator(pLabelID, pObjectID)
                RstValues.Fields("value").Value = tValue
            elif (select_1 == 'JOBRECIPE'):
                RstValues.Fields("value").Value = PrepareJobRecipeLabelField(MdlADOFunctions.fGetRstValString(RstFields.Fields("FieldName").Value), tRecipeRst)
            elif (select_1 == 'INV_STATUS_1'):
                tValue = MdlADOFunctions.fGetRstValLong(GetInventoryItemsCountForStatus(tObjectID, 1, tLabelGroupID))
                if tLabelGroupID == 1:
                    tValue = MdlADOFunctions.fGetRstValLong(tValue) + 1
                elif tValue == '-1':
                    tValue = ''
                RstValues.Fields("value").Value = tValue
            elif (select_1 == 'ENUMERATOR'):
                if tObjectID != 0:
                    tSourceTable = MdlADOFunctions.fGetRstValString(RstFields.Fields("sourceTable").Value)
                    tSourceField = MdlADOFunctions.fGetRstValString(RstFields.Fields("SourceField").Value)
                    if tSourceTable != '' and tSourceField != '':
                        tSourceID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue(tSourceField, 'TblJob', 'ID = ' + tObjectID, 'CN'))
                        if tSourceID != 0:
                            
                            strSQL = 'SELECT * FROM ' + tSourceTable + ' WHERE ID = ' + tSourceID
                            Rst.Open(strSQL, CN, adOpenDynamic, adLockOptimistic)
                            if Rst.RecordCount == 1:
                                tEnumerator = MdlADOFunctions.fGetRstValLong(Rst.Fields("LabelEnumerator").Value)
                                tEnumerator = tEnumerator + 1
                                tValue = tEnumerator
                                Rst.Fields("LabelEnumerator").Value = tEnumerator
                                Rst.Update()
                            Rst.Close()
                        else:
                            tValue = ''
                    else:
                        tValue = ''
                else:
                    tValue = ''
                RstValues.Fields("value").Value = tValue
            else:
                if MdlADOFunctions.fGetRstValBool(RstFields.Fields("AllowEntry").Value, False) == False or  ( MdlADOFunctions.fGetRstValBool(RstFields.Fields("AllowEntry").Value, False) == True and MdlADOFunctions.fGetRstValString(RstFields.Fields("defaultValue").Value) == '' ) :
                    if CheckIfRstFieldExists(RstData, RstFields.Fields("FieldName").Value) == True:
                        if MdlADOFunctions.fGetRstValString(RstData.Fields(MdlADOFunctions.fGetRstValString(RstFields.Fields("FieldName").Value)).value) != '':
                            RstValues.Fields("value").Value = RstData.Fields(MdlADOFunctions.fGetRstValString(RstFields.Fields("FieldName").Value)).value
                        else:
                            RstValues.Fields("value").Value = ''
                    else:
                        MdlGlobal.RecordError('PrepareDataForLabel', '1', 'Field: ' + RstFields.Fields("FieldName").Value + ' was not found on ' + tDataSource, 'LabelID: ' + tLabelID + '. UserID: ' + tUserID)
                        RstValues.Fields("value").Value = ''
                else:
                    RstValues.Fields("value").Value = MdlADOFunctions.fGetRstValString(RstFields.Fields("defaultValue").Value)
            RstValues.Update()
            RstFields.MoveNext()
    RstData.Close()
    RstFields.Close()
    RstValues.Close()
    if tHasRecipeFields != 0:
        tRecipeRst.Close()
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
            
        Err.Clear()
        
    RstFields = None
    RstValues = None
    RstData = None
    return returnVal

def PrepareCalculatedLabelField(pCalcType, pDataRst):
    returnVal = None
    tValue = ''

    tValid = False
    
    returnVal = ''
    select_2 = UCase(pCalcType)
    if (select_2 == 'TIME') or (select_2 == 'TIME()'):
        tValue = Format(NowGMT, 'HH:nn')
    elif (select_2 == 'DATE') or (select_2 == 'DATE()'):
        tValue = ShortDate(NowGMT, False, False, False)
    elif (select_2 == 'NOW') or (select_2 == 'NOW()'):
        tValue = Now()
    elif (select_2 == 'NOWTEXT') or (select_2 == 'NOWTEXT()'):
        tValue = Format(NowGMT, 'yyyy-mm-dd hh:nn:ss')
    else:
        tValue = CalcLabelExpression(pCalcType, pDataRst, tValid)
    returnVal = tValue
    if Err.Number != 0:
        Err.Clear()
    return returnVal

def PrepareSystemVarLabelField(pVariableName, pJobID=0):
    returnVal = None
    tValue = ''

    tUserID = 0

    tDisplayName = ''
    
    
    returnVal = ''
    select_3 = UCase(pVariableName)
    if (select_3 == 'USER') or (select_3 == 'USERID'):
        tValue = 0
    elif (select_3 == 'USERNAME'):
        
        
        tValue = 'System'
        
    elif (select_3 == 'Shift') or (select_3 == 'ShiftID'):
        if pJobID != 0:
            tValue = MdlADOFunctions.fGetRstValString(fGetCurrentShiftDefIDByShiftCalendar(fGetShiftCalendarIDByMachine(MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineID', 'TblJob', 'ID = ' + pJobID, 'CN')))))
        else:
            tValue = MdlADOFunctions.fGetRstValString(fGetCurrentShiftDefIDByShiftCalendar(1))
        
        tValue = MdlADOFunctions.GetSingleValue('ShiftName', 'TblShiftDef', 'ID = ' + MdlADOFunctions.fGetRstValLong(tValue), 'CN')
    elif (select_3 == 'ShiftManagerID'):
        if pJobID != 0:
            tValue = MdlADOFunctions.fGetRstValString(fGetCurrentShiftIDByShiftCalendar(fGetShiftCalendarIDByMachine(MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineID', 'TblJob', 'ID = ' + pJobID, 'CN')))))
            tValue = MdlADOFunctions.GetSingleValue('ManagerID', 'TblShift', 'ID = ' + MdlADOFunctions.fGetRstValLong(tValue), 'CN')
        else:
            tValue = MdlADOFunctions.fGetRstValString(fGetCurrentShiftDefIDByShiftCalendar(1))
            tValue = MdlADOFunctions.GetSingleValue('ManagerUserID', 'TblShiftDef', 'ID = ' + MdlADOFunctions.fGetRstValLong(tValue), 'CN')
    elif (select_3 == 'ShiftManagerName'):
        if pJobID != 0:
            tValue = MdlADOFunctions.fGetRstValString(fGetCurrentShiftIDByShiftCalendar(fGetShiftCalendarIDByMachine(MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineID', 'TblJob', 'ID = ' + pJobID, 'CN')))))
            tValue = MdlADOFunctions.GetSingleValue('ManagerID', 'TblShift', 'ID = ' + MdlADOFunctions.fGetRstValLong(tValue), 'CN')
        else:
            tValue = MdlADOFunctions.fGetRstValString(fGetCurrentShiftDefIDByShiftCalendar(1))
            tValue = MdlADOFunctions.GetSingleValue('ManagerUserID', 'TblShiftDef', 'ID = ' + MdlADOFunctions.fGetRstValLong(tValue), 'CN')
        
        tDisplayName = 'DisplayName'
        tValue = MdlADOFunctions.GetSingleValue(tDisplayName, 'STbl_Users', 'ID = ' + MdlADOFunctions.fGetRstValLong(tValue), 'CN')
    else:
        tValue = MdlADOFunctions.GetSingleValue(pVariableName, 'STblSystemVariables', 'ID=1', 'CN')
    returnVal = tValue
    if Err.Number != 0:
        Err.Clear()
    return returnVal



def CheckIfRstFieldExists(PRst, FieldName):
    returnVal = None
    Field = ADODB.Field()
    
    FieldName = UCase(FieldName)
    for Field in PRst.Fields:
        if UCase(Field.Name) == FieldName:
            returnVal = True
            return returnVal
    returnVal = False
    if Err.Number != 0:
        Err.Clear()
    return returnVal

def RaiseLabelNumerator(pLabelID, pJobID, pRaiseStep=1, pSpecificNumeratorTypeID=0):
    returnVal = - 1
    strSQL = ''
    tCurrentValue = 0
    tNumeratorID = 0
    
    try:
        tCurrentValue = GetLabelNumerator(pLabelID, pJobID, tNumeratorID, pSpecificNumeratorTypeID)
        if tCurrentValue != - 1:
            tCurrentValue = tCurrentValue + pRaiseStep
            strSQL = 'UPDATE TblNumerators SET Value = ' + str(tCurrentValue) + ' WHERE ID = ' + str(tNumeratorID)
            MdlConnection.CN.execute(strSQL)
        else:
            raise Exception('Invalid current value in "RaiseLabelNumerator"')

        returnVal = tCurrentValue

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('RaiseLabelNumerator', str(0), error.args[0], 'LabelID = ' + str(pLabelID))

    return returnVal


def GetLabelNumerator(pLabelID, pJobID, pNumeratorID, pSpecificNumeratorTypeID=0):
    returnVal = None
    strSQL = ''

    Rst = None

    tPackageTypeID = 0

    tLabelNumeratorTypeID = 0

    tPriority = 0

    tCreateAutomatically = False

    tValue = 0

    tJobID = 0

    tERPJobID = ''

    tProductID = 0

    tClientID = 0

    tProductClientID = 0

    tNumeratorEnabled = False
    
    if pSpecificNumeratorTypeID == 0:
        strSQL = 'SELECT NumeratorTypeID, DefaultPackageTypeID' + vbCrLf
        strSQL = strSQL + 'FROM MetaTblLabels' + vbCrLf
        strSQL = strSQL + 'WHERE ID = ' + pLabelID
        Rst.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        if Rst.RecordCount == 1:
            tPackageTypeID = MdlADOFunctions.fGetRstValLong(Rst.Fields("DefaultPackageTypeID").Value)
            tLabelNumeratorTypeID = MdlADOFunctions.fGetRstValLong(Rst.Fields("NumeratorTypeID").Value)
        Rst.Close()
    else:
        tLabelNumeratorTypeID = pSpecificNumeratorTypeID
        tPackageTypeID = 3
    tPriority = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('Priority', 'STblLabelNumeratorTypes', 'ID = ' + tLabelNumeratorTypeID, 'MetaCN'))
    tJobID = pJobID
    tValue = - 1
    
    strSQL = 'SELECT * FROM STblLabelNumeratorTypes WHERE Priority <= ' + tPriority + ' ORDER BY Priority DESC'
    Rst.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    while not Rst.EOF:
        tLabelNumeratorTypeID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
        tCreateAutomatically = MdlADOFunctions.fGetRstValBool(Rst.Fields("CreateAutomatically").Value, True)
        if (tLabelNumeratorTypeID == 1):
            tValue = GetNumerator(2, tCreateAutomatically, pNumeratorID, tPackageTypeID, tJobID)
        elif (tLabelNumeratorTypeID == 2):
            tERPJobID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('ERPJobID', 'TblJob', 'ID = ' + tJobID, 'CN'))
            if tERPJobID != '':
                tValue = GetNumerator(2, tCreateAutomatically, pNumeratorID, tPackageTypeID, VBGetMissingArgument(GetNumerator, 4), tERPJobID)
            else:
                GoTo(NextPriority)
        elif (tLabelNumeratorTypeID == 3):
            tProductID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductID', 'TblJob', 'ID = ' + tJobID, 'CN'))
            if tProductID != 0:
                tNumeratorEnabled = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('NumeratorEnabled', 'TblObjectLabelSettings', 'ProductID = ' + tProductID, 'CN'), False)
                if tNumeratorEnabled:
                    tValue = GetNumerator(2, tCreateAutomatically, pNumeratorID, tPackageTypeID, VBGetMissingArgument(GetNumerator, 4), VBGetMissingArgument(GetNumerator, 5), tProductID)
                else:
                    GoTo(NextPriority)
            else:
                GoTo(NextPriority)
        elif (tLabelNumeratorTypeID == 4):
            tClientID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ClientID', 'TblJob', 'ID = ' + tJobID, 'CN'))
            if tClientID != 0:
                tNumeratorEnabled = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('NumeratorEnabled', 'TblObjectLabelSettings', 'ClientID = ' + tClientID, 'CN'), False)
                if tNumeratorEnabled:
                    tValue = GetNumerator(2, tCreateAutomatically, pNumeratorID, tPackageTypeID, VBGetMissingArgument(GetNumerator, 4), VBGetMissingArgument(GetNumerator, 5), VBGetMissingArgument(GetNumerator, 6), tClientID)
                else:
                    GoTo(NextPriority)
            else:
                GoTo(NextPriority)
        elif (tLabelNumeratorTypeID == 5):
            tProductID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductID', 'TblJob', 'ID = ' + tJobID, 'CN'))
            tClientID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ClientID', 'TblJob', 'ID = ' + tJobID, 'CN'))
            if tProductID != 0 and tClientID != 0:
                tProductClientID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblProductClients', 'ProductID = ' + tProductID + ' AND ClientID = ' + tClientID, 'CN'))
                tNumeratorEnabled = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('NumeratorEnabled', 'TblObjectLabelSettings', 'ProductClientID = ' + tClientID, 'CN'), False)
                if tNumeratorEnabled:
                    tValue = GetNumerator(2, tCreateAutomatically, pNumeratorID, tPackageTypeID, VBGetMissingArgument(GetNumerator, 4), VBGetMissingArgument(GetNumerator, 5), VBGetMissingArgument(GetNumerator, 6), VBGetMissingArgument(GetNumerator, 7), tProductClientID)
                else:
                    GoTo(NextPriority)
            else:
                GoTo(NextPriority)
        if tValue != - 1:
            GoTo(ExitWhile)
        Rst.MoveNext()
    Rst.Close()
    returnVal = tValue
    if Err.Number != 0:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('GetLabelNumerator', str(0), error.args[0], 'LabelID = ' + str(pLabelID))
        Err.Clear()
    Rst = None
    return returnVal


def GetNumerator(pNumeratorTypeID, pCreateAutomatically, pNumeratorID, pPackageTypeID=0, pJobID=0, pERPJobID='', pProductID=0, pClientID=0, pProductClientID=0):
    returnVal = None
    strSQL = ''

    Rst = None

    tValue = 0
    
    
    returnVal = CLng(- 1)
    strSQL = ''
    strSQL = strSQL + 'SELECT ID,Value' + vbCrLf
    strSQL = strSQL + 'FROM TblNumerators' + vbCrLf
    strSQL = strSQL + 'WHERE NumeratorTypeID = ' + pNumeratorTypeID
    if pPackageTypeID != 0:
        strSQL = strSQL + ' AND PackageTypeID = ' + pPackageTypeID
    else:
        strSQL = strSQL + ' AND PackageTypeID IS NULL'
    if pJobID != 0:
        strSQL = strSQL + ' AND JobID = ' + pJobID
    else:
        strSQL = strSQL + ' AND JobID IS NULL'
    if pERPJobID != '':
        strSQL = strSQL + ' AND ERPJobID = \'' + pERPJobID + '\''
    else:
        strSQL = strSQL + ' AND ERPJobID IS NULL'
    if pProductID != 0:
        strSQL = strSQL + ' AND ProductID = ' + pProductID
    else:
        strSQL = strSQL + ' AND ProductID IS NULL'
    if pClientID != 0:
        strSQL = strSQL + ' AND ClientID = ' + pClientID
    else:
        strSQL = strSQL + ' AND ClientID IS NULL'
    if pProductClientID != 0:
        strSQL = strSQL + ' AND ProductClientID = ' + pProductClientID
    else:
        strSQL = strSQL + ' AND ProductClientID IS NULL'
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    if Rst.RecordCount == 1:
        pNumeratorID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
        tValue = MdlADOFunctions.fGetRstValLong(Rst.Fields("value").Value)
    elif Rst.RecordCount > 1:
        while not Rst.EOF:
            if MdlADOFunctions.fGetRstValLong(Rst.Fields("value").Value) > 0:
                pNumeratorID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
                tValue = MdlADOFunctions.fGetRstValLong(Rst.Fields("value").Value)
            Rst.MoveNext()
        if pNumeratorID == 0:
            Rst.MoveFirst()
            pNumeratorID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
            tValue = MdlADOFunctions.fGetRstValLong(Rst.Fields("value").Value)
    elif Rst.RecordCount == 0:
        if pCreateAutomatically:
            strSQL = ''
            strSQL = strSQL + 'INSERT INTO TblNumerators' + vbCrLf
            strSQL = strSQL + '('
            strSQL = strSQL + 'NumeratorTypeID,'
            strSQL = strSQL + 'PackageTypeID,'
            strSQL = strSQL + 'JobID,'
            strSQL = strSQL + 'ERPJobID,'
            strSQL = strSQL + 'ProductID,'
            strSQL = strSQL + 'ClientID,'
            strSQL = strSQL + 'ProductClientID'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + pNumeratorTypeID + ','
            if pPackageTypeID != 0:
                strSQL = strSQL + str(pPackageTypeID) + ','
            else:
                strSQL = strSQL + 'NULL,'
            if pJobID != 0:
                strSQL = strSQL + str(pJobID) + ','
            else:
                strSQL = strSQL + 'NULL,'
            if pERPJobID != '':
                strSQL = strSQL + '\'' + pERPJobID + '\','
            else:
                strSQL = strSQL + 'NULL,'
            if pProductID != 0:
                strSQL = strSQL + pProductID + ','
            else:
                strSQL = strSQL + 'NULL,'
            if pClientID != 0:
                strSQL = strSQL + pClientID + ','
            else:
                strSQL = strSQL + 'NULL,'
            if pProductClientID != 0:
                strSQL = strSQL + pProductClientID + ','
            else:
                strSQL = strSQL + 'NULL'
            strSQL = strSQL + ')'
            MdlConnection.CN.execute(strSQL)
            tValue = 0
            pNumeratorID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MAX(ID)', 'TblNumerators', 'ID <> 0'))
        else:
            tValue = - 1
    else:
        Err.Raise(30001)
    returnVal = tValue
    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            Err.Clear()
            
        Err.Clear()
    Rst = None
    return returnVal

def AddToLabelsQueue(pLabelID, pCriteria, pNumberOfCopies, pJob):
    returnVal = None
    tLabelGroupID = 0

    tTableName = ''

    strSQL = ''

    SRst = None

    TRst = None

    tUserID = 0

    tMinID = 0
    
    
    tUserID = pJob.Machine.Server.SCID * - 1
    returnVal = tMinID
    tLabelGroupID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('LabelGroupID', 'MetaTblLabels', 'ID = ' + pLabelID, 'MetaCN'))
    if (tLabelGroupID == 1):
        tTableName = 'TblJob'
    elif (tLabelGroupID == 2):
        tTableName = 'TblQualityTests'
    elif (tLabelGroupID == 3):
        tTableName = 'TblRejects'
    elif (tLabelGroupID == 4):
        tTableName = 'TblInventory'
    elif (tLabelGroupID == 7):
        tTableName = 'TblNC'
    else:
        tTableName = 'TblJob'
    
    
    strSQL = 'SELECT ID FROM ' + tTableName + ' ' + pCriteria
    SRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    strSQL = 'SELECT * FROM TblLabelsQueue WHERE ID = 0'
    TRst.Open(strSQL, CN, adOpenDynamic, adLockOptimistic)
    while not SRst.EOF:
        TRst.AddNew()
        TRst.Fields("UserID").Value = tUserID
        TRst.Fields("LabelID").Value = pLabelID
        TRst.Fields("ObjectID").Value = SRst.Fields("ID").Value
        TRst.Fields("Copies").Value = pNumberOfCopies
        TRst.Fields("AutomaticLabel").Value = pJob.Machine.AutoPrintLabel
        TRst.Update()
        if tMinID == 0:
            tMinID = TRst.Fields("ID").Value
        SRst.MoveNext()
    TRst.Close()
    SRst.Close()
    returnVal = tMinID
    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            Err.Clear()
            
        Err.Clear()
        
    TRst = None
    SRst = None
    return returnVal

def ProcessCurrentLabelSession(pJob, pLabelID, pEffectiveAmount, pInventoryStatus, pMinQueueID):
    returnVal = None
    strSQL = ''

    Rst = None

    tUserID = 0

    tQueueID = 0

    tInventoryReportOption = 0

    tInventoryID = 0

    tWareHouseID = 0

    tWareHouseLocation = ''

    tWareHouseLocationID = 0

    tObjectID = 0

    tLabelGroupID = 0

    tAddUnitsReportedOKToJob = False

    tAddUnitsReportedOKField = ''

    tPackagesInventory = False

    tJobID = 0

    tJoshID = 0

    MachinesRst = None

    tMachineID = 0

    tAddToActivePallet = False

    tDisconnectFromParentInventoryID = False
    
    returnVal = False
    
    tUserID = pJob.Machine.Server.SCID * - 1
    strSQL = 'SELECT ID,ObjectID FROM TblLabelsQueue' + vbCrLf
    strSQL = strSQL + 'WHERE LabelID = ' + pLabelID + ' AND UserID = ' + tUserID + ' AND ID >= ' + pMinQueueID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    while not Rst.EOF:
        tQueueID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
        tObjectID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ObjectID").Value)
        if not PrepareDataForLabel(pLabelID, tObjectID, tQueueID, tUserID):
            Err.Raise(20080)
        if not GetLabelReportingProperties(pLabelID, tLabelGroupID, tInventoryReportOption, tAddUnitsReportedOKToJob, tAddUnitsReportedOKField, tPackagesInventory, tAddToActivePallet):
            Err.Raise(20081)
        if tInventoryReportOption > 0:
            tJobID = pJob.ID
            tJoshID = pJob.ActiveJosh.ID
            tMachineID = pJob.Machine.ID
            
            
            
            
            
            
            
            
            
            if not GetLabelInventoryReportParameters(tInventoryReportOption, tWareHouseID, tWareHouseLocation, tWareHouseLocationID, pLabelID, tMachineID, tJobID):
                Err.Raise(20082)
            tInventoryID = CreateInventoryItemFromLabel(tQueueID, pLabelID, tUserID, tWareHouseID, tWareHouseLocation, tWareHouseLocationID, tObjectID, pEffectiveAmount, pInventoryStatus)
            if tInventoryID != 0:
                
                AddInventoryHistoryRecord(tInventoryID, 1)
                
                
                tDisconnectFromParentInventoryID = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('DisconnectFromParentInventoryID', 'STblInventoryStatus', 'ID = ' + pInventoryStatus, 'CN'), False)
                if tAddToActivePallet and tDisconnectFromParentInventoryID == False:
                    AddInventoryItemToActivePallet(tInventoryID, pJob.Machine)
            else:
                Err.Raise(20082)
            if tPackagesInventory:
                
                pass
            CreateInventoryTrace(tInventoryID, tJoshID)
        if tAddUnitsReportedOKToJob:
            pJob.UnitsReportedOK = pJob.UnitsReportedOK + pEffectiveAmount
            pJob.ActiveJosh.UnitsReportedOK = pJob.ActiveJosh.UnitsReportedOK + pEffectiveAmount
        Rst.MoveNext()
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
            
        Err.Clear()
    Rst = None
    MachinesRst = None
    return returnVal


def CalcLabelExpression(Expr, pDataRst, Valid):
    returnVal = None
    ParCount = Double()

    ParBalance = Double()

    Counter = 0

    ExpLen = 0

    IsValid = False

    OpenPar = 0

    ExprStart = 0

    NewExpr = ''

    ParExpr = ''

    temp = ''

    tVal = ''

    TestOpen = 0

    SampleOpen = 0

    ClosePar = 0

    MidLen = 0

    AggFunc = ''

    Fields = ''

    FieldLoc = 0

    FieldName = ''

    FieldExt = ''

    pos = 0
    
    Valid = False
    ParBalance = ExpressionParBalance(Expr, ParCount)
    if ParCount < 0 or ParBalance != 0:
        Err.Raise(1)
        
    ExpLen = Len(Expr)
    if ParCount == 0:
        
        for Counter in range(0, ExpLen):
            temp = mID(Expr, Counter, 1)
            if (temp == '['):
                TestOpen = Counter
            elif (temp == ']'):
                temp = mID(Expr, TestOpen + 1, Counter - TestOpen - 1)
                pos = InStr(1, temp, '.')
                if pos == 0:
                    Err.Raise(1)
                else:
                    FieldName = Left(temp, pos - 1)
                    FieldExt = Right(temp, Len(temp) - pos)
                
                
                tVal = MdlADOFunctions.fGetRstValString(pDataRst.Fields(FieldName).value)
                if not IsNumeric(tVal):
                    Err.Raise(1)
                else:
                    NewExpr = NewExpr + tVal
                TestOpen = 0
            else:
                if TestOpen == 0 and SampleOpen == 0:
                    NewExpr = NewExpr + temp
        
        returnVal = CalcSimpleExpression(NewExpr, IsValid)
    else:
        for Counter in range(0, ExpLen):
            select_7 = mID(Expr, Counter, 1)
            if (select_7 == '('):
                if ParBalance == 0:
                    OpenPar = Counter
                ParBalance = ParBalance + 1
            elif (select_7 == ')'):
                ParBalance = ParBalance - 1
                if ParBalance == 0:
                    
                    ParExpr = mID(Expr, OpenPar + 1, Counter - OpenPar - 1)
                    MidLen = OpenPar - ClosePar - 1
                    if MidLen > 0:
                        NewExpr = NewExpr + mID(Expr, ClosePar + 1, MidLen) + CalcLabelExpression(ParExpr, pDataRst, IsValid) + Right(Expr, ExpLen - Counter)
                    else:
                        NewExpr = NewExpr + CalcLabelExpression(ParExpr, pDataRst, IsValid) + Right(Expr, ExpLen - Counter)

        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('CalcLabelExpression', str(0), error.args[0], '')
        str(Err).Clear()
        Valid = False
    return returnVal

def CreateInventoryItemFromLabel(pLabelQueueID, pLabelID, pUserID, pWareHouseID, pWareHouseLocation, pWareHouseLocationID, pObjectID, pEffectiveAmount, pInventoryStatus):
    returnVal = None
    strSQL = ''

    tValuesRst = None

    tInventoryRst = None

    tLabelsRst = None

    tFieldName = ''

    tPackageTypeID = 0

    tEffectiveAmountField = ''

    tInventoryID = 0

    tLabelGroupID = 0

    tJobID = 0

    tJoshID = 0

    tProductID = 0

    tCatalogID = ''

    tMaterialID = 0

    tInventoryBatchOption = 0

    tNumerator = 0

    tNumeratorFieldName = ''

    tShiftID = 0

    AddPackageTypeToInventoryBatch = False
    
    returnVal = 0
    
    strSQL = 'SELECT AddUnitsReportedOKField, DefaultPackageTypeID, LabelGroupID FROM MetaTblLabels WHERE ID = ' + pLabelID
    tLabelsRst.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
    tLabelsRst.ActiveConnection = None
    if tLabelsRst.RecordCount == 1:
        tPackageTypeID = MdlADOFunctions.fGetRstValLong(tLabelsRst.Fields("DefaultPackageTypeID").Value)
        tEffectiveAmountField = MdlADOFunctions.fGetRstValString(tLabelsRst.Fields("AddUnitsReportedOKField").Value)
        if tEffectiveAmountField == '':
            tEffectiveAmountField = 'BoxUnits'
        tLabelGroupID = MdlADOFunctions.fGetRstValLong(tLabelsRst.Fields("LabelGroupID").Value)
    tLabelsRst.Close()
    strSQL = 'SELECT FieldName FROM MetaTblLabelFields WHERE DisplayType = N\'Numerator\' AND LabelID = ' + pLabelID
    tLabelsRst.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
    tLabelsRst.ActiveConnection = None
    if tLabelsRst.RecordCount == 1:
        tNumeratorFieldName = MdlADOFunctions.fGetRstValString(tLabelsRst.Fields("FieldName").Value)
    tLabelsRst.Close()
    tJobID = GetJobIDByLabelObjectID(tLabelGroupID, pObjectID)
    tJoshID = GetCurrentOrLastJoshForJob(tJobID)
    tShiftID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ShiftID', 'TblJosh', 'ID = ' + tJoshID, 'CN'))
    if not GetProductInformationForLabel(tJobID, tProductID, tCatalogID, tMaterialID):
        pass
    if pWareHouseID == 0:
        pWareHouseID = 2
        
    tInventoryBatchOption = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'InventoryBatchOption\'', 'CN'))
    
    AddPackageTypeToInventoryBatch = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'AddPackageTypeToInventoryBatch\'', 'CN'), False)
    
    strSQL = 'SELECT * FROM MetaTblLabelFieldValues WHERE UserID = ' + pUserID + ' AND LabelID = ' + pLabelID + ' AND QueueID = ' + pLabelQueueID
    tValuesRst.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
    tValuesRst.ActiveConnection = None
    strSQL = 'SELECT * FROM TblInventory WHERE ID = 0'
    tInventoryRst.Open(strSQL, CN, adOpenForwardOnly, adLockOptimistic)
    tInventoryRst.AddNew()
    tInventoryRst.Fields("Status").Value = pInventoryStatus
    tInventoryRst.Fields("LabelID").Value = pLabelID
    tInventoryRst.Fields("Date").Value = NowGMT()
    tInventoryRst.Fields("LastUpdate").Value = NowGMT()
    tInventoryRst.Fields("UserID").Value = pUserID
    tInventoryRst.Fields("WareHouseID").Value = pWareHouseID
    tInventoryRst.Fields("WareHouseLocation").Value = pWareHouseLocation
    tInventoryRst.Fields("WareHouseLocationID").Value = pWareHouseLocationID
    tInventoryRst.Fields("Amount").Value = 1
    tInventoryRst.Fields("OriginalAmount").Value = 1
    tInventoryRst.Fields("JobID").Value = tJobID
    tInventoryRst.Fields("JoshID").Value = tJoshID
    tInventoryRst.Fields("PackageTypeID").Value = tPackageTypeID
    tInventoryRst.Fields("ProductID").Value = tProductID
    tInventoryRst.Fields("MaterialID").Value = tMaterialID
    tInventoryRst.Fields("CatalogID").Value = tCatalogID
    tInventoryRst.Fields("ShiftID").Value = tShiftID
    while not tValuesRst.EOF:
        tFieldName = MdlADOFunctions.fGetRstValString(tValuesRst.Fields("FieldName").Value)
        if CheckIfRstFieldExists(tInventoryRst, tFieldName):
            if tInventoryRst.Fields(tFieldName).Type == adInteger or tInventoryRst.Fields(tFieldName).Type == adBigInt or tInventoryRst.Fields(tFieldName).Type == adDouble or tInventoryRst.Fields(tFieldName).Type == adNumeric or tInventoryRst.Fields(tFieldName).Type == adSingle or tInventoryRst.Fields(tFieldName).Type == adSmallInt:
                if MdlADOFunctions.fGetRstValString(tValuesRst.Fields("value").Value) != '':
                    tInventoryRst.Fields[tFieldName].value = MdlADOFunctions.fGetRstValString(tValuesRst.Fields("value").Value)
            else:
                tInventoryRst.Fields[tFieldName].value = MdlADOFunctions.fGetRstValString(tValuesRst.Fields("value").Value)
        
        if tFieldName == tNumeratorFieldName:
            tNumerator = MdlADOFunctions.fGetRstValLong(tValuesRst.Fields("value").Value)
            tInventoryRst.Fields("PackageBatchNum").Value = tNumerator
        tValuesRst.MoveNext()
    if tNumerator == 0:
        tNumerator = RaiseLabelNumerator(pLabelID, tJobID)
        tInventoryRst.Fields("PackageBatchNum").Value = tNumerator
    if tNumerator == 0:
        tInventoryRst.CancelUpdate()
        tInventoryRst.Close()
        return returnVal
    tInventoryRst.Fields("EffectiveAmount").Value = pEffectiveAmount
    tInventoryRst.Fields("LastEffectiveAmount").Value = pEffectiveAmount
    tInventoryRst.Fields("EffectiveOriginalAmount").Value = pEffectiveAmount
    tInventoryRst.Fields("Batch").Value = CreateBatchFormat(tInventoryBatchOption, tJobID, tJoshID, tNumerator, AddPackageTypeToInventoryBatch, tPackageTypeID)
    tInventoryRst.Update()
    tInventoryID = MdlADOFunctions.fGetRstValLong(tInventoryRst.Fields("ID").Value)
    tInventoryRst.Close()
    tValuesRst.Close()
    returnVal = tInventoryID

    if Err.Number != 0:
        if InStr('nnection') in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

        MdlGlobal.RecordError('CreateInventoryItemFromLabel', str(0), error.args[0], '')
        str(Err).Clear()
        
    tValuesRst = None
    tInventoryRst = None
    return returnVal

def GetJobIDByLabelObjectID(pLabelGroupID, pObjectID):
    returnVal = None
    tJobID = 0
    
    returnVal = tJobID
    if (pLabelGroupID == 1):
        tJobID = pObjectID
    elif (pLabelGroupID == 2):
        tJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('JobID', 'TblQualityTests', 'ID = ' + pObjectID, 'CN'))
    elif (pLabelGroupID == 3):
        tJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('JobID', 'TblRejects', 'ID = ' + pObjectID, 'CN'))
    elif (pLabelGroupID == 4):
        tJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('JobID', 'TblInventory', 'ID = ' + pObjectID, 'CN'))
    returnVal = tJobID
    if Err.Number != 0:
        Err.Clear()
    return returnVal

def GetCurrentOrLastJoshForJob(pJobID):
    returnVal = None
    strSQL = ''

    if 'nnection' in error.args[0]:
        if MdlConnection.CN:
            MdlConnection.Close(MdlConnection.CN)
        MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

        if MdlConnection.MetaCn:
            MdlConnection.Close(MdlConnection.MetaCn)
        MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
    if Err.Number != 0:
        MdlGlobal.RecordError('GetCurrentOrLastJoshForJob', str(0), error.args[0], 'JobID = ' + str(pJobID))
        Err.Clear()
    Rst = None
    return returnVal




def GetProductInformationForLabel(pJobID, pProductID, pCatalogID, pMaterialID):
    returnVal = None
    strSQL = ''

    Rst = None
    
    returnVal = False
    strSQL = 'SELECT P.ID AS ProductID, P.CatalogID, P.MaterialID' + vbCrLf
    strSQL = strSQL + 'FROM TblJob J' + vbCrLf
    strSQL = strSQL + '    INNER JOIN TblProduct P ON J.ProductID = P.ID' + vbCrLf
    strSQL = strSQL + 'WHERE J.ID = ' + pJobID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    if Rst.RecordCount == 1:
        pProductID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ProductID").Value)
        pCatalogID = MdlADOFunctions.fGetRstValString(Rst.Fields("CatalogID").Value)
        pMaterialID = MdlADOFunctions.fGetRstValLong(Rst.Fields("MaterialID").Value)
        if pMaterialID == 0 and pCatalogID != '':
            pMaterialID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblMaterial', 'CatalogID = \'' + pCatalogID + '\'', 'CN'))
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
            
        Err.Clear()
    Rst = None
    return returnVal

def CreateBatchFormat(pInventoryBatchOption, pJobID, pJoshID, pPackageBatchNum, pAddPackageTypeToInventoryBatch, pPackageTypeID=1):
    returnVal = ''
    tERPJobID = ''
    tOriginalJobID = 0
    tBatch = ''
    tInventoryBatchOption = 0
    tInventoryBatchOptionFromPackageType = False
    tInventoryBatchOptionFormat = ''
    tStr = ''
    tFormatString = ''
    tFieldName = ''
    tSets = []
    tSingleSet = []
    TCount = 0
    tBatch = ''
    
    try:
        tInventoryBatchOptionFromPackageType = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'InventoryBatchOptionFromPackageType\'', 'CN'), False)
        if tInventoryBatchOptionFromPackageType == True:
            pInventoryBatchOption = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('InventoryBatchOption', 'TblPackageType', 'ID = ' + str(pPackageTypeID), 'CN'))
        if pAddPackageTypeToInventoryBatch == True:

            if (pInventoryBatchOption == 1):
                if pJobID > 0:
                    tBatch = pJobID
                    if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                        tBatch = str(pJobID) + '.' + str(pPackageTypeID) + '.' + str(pPackageBatchNum)

            elif (pInventoryBatchOption == 2):
                if pJoshID > 0:
                    tBatch = pJoshID
                    if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                        tBatch = str(pJoshID) + '.' + str(pPackageTypeID) + '.' + str(pPackageBatchNum)
                else:
                    if pJobID > 0:
                        tBatch = pJobID
                        if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                            tBatch = str(pJobID) + '.' + str(pPackageTypeID) + '.' + str(pPackageBatchNum)

            elif (pInventoryBatchOption == 3):
                if pJobID > 0:
                    tERPJobID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('ERPJobID', 'TblJob', 'ID = ' + str(pJobID), 'CN'))
                    if tERPJobID != '':
                        tBatch = tERPJobID
                        if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                            tBatch = tERPJobID + '.' + str(pPackageTypeID) + '.' + str(pPackageBatchNum)
                    else:
                        tOriginalJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('OriginalJobID', 'TblJob', 'ID = ' + str(pJobID), 'CN'))
                        if tOriginalJobID > 0:
                            tBatch = str(tOriginalJobID)
                            if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                                tBatch = str(tOriginalJobID) + '.' + str(pPackageTypeID) + '.' + str(pPackageBatchNum)

            elif (pInventoryBatchOption == 4):
                if pJobID > 0:
                    tOriginalJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('OriginalJobID', 'TblJob', 'ID = ' + str(pJobID), 'CN'))
                    if tOriginalJobID > 0:
                        tBatch = str(tOriginalJobID)
                        if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                            tBatch = str(tOriginalJobID) + '.' + str(pPackageTypeID) + '.' + str(pPackageBatchNum)
                    else:
                        tBatch = str(pJobID)
                        if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                            tBatch = str(pJobID) + '.' + str(pPackageTypeID) + '.' + str(pPackageBatchNum)

            elif (pInventoryBatchOption == 5):
                tInventoryBatchOptionFormat = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('InventoryBatchOptionFormat', 'TblPackageType', 'ID = ' + str(pPackageTypeID), 'CN'))
                if tInventoryBatchOptionFormat != '':
                    
                    tSets = Split(tInventoryBatchOptionFormat, ';')
                    for TCount in range(0, ( len(tSets) - 1 )):
                        tSingleSet = Split(tSets(TCount), ':')
                        tFieldName = MdlADOFunctions.fGetRstValString(tSingleSet(0))
                        tFormatString = MdlADOFunctions.fGetRstValString(tSingleSet(1))
                        if tFieldName != '' and tFormatString != '':
                            if (tFieldName == 'JobID'):
                                tStr = pJobID
                            elif (tFieldName == 'JoshID'):
                                tStr = pJoshID
                            elif (tFieldName == 'ERPJobID'):
                                tERPJobID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('ERPJobID', 'TblJob', 'ID = ' + str(pJobID), 'CN'))
                                if tERPJobID != '':
                                    tStr = tERPJobID
                            elif (tFieldName == 'PackageBatchNum'):
                                tStr = pPackageBatchNum
                            elif (tFieldName == 'PackageTypeID'):
                                tStr = pPackageTypeID
                            else:
                                tStr = tFieldName
                            tBatch = tBatch + Format(tStr, tFormatString)
            else:
                if pJobID > 0:
                    tBatch = pJobID
                    if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                        tBatch = str(pJobID) + '.' + str(pPackageTypeID) + '.' + str(pPackageBatchNum)
        else:
            if (pInventoryBatchOption == 1):
                if pJobID > 0:
                    tBatch = pJobID
                    if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                        tBatch = str(pJobID) + '.' + str(pPackageBatchNum)
            
            elif (pInventoryBatchOption == 2):
                if pJoshID > 0:
                    tBatch = pJoshID
                    if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                        tBatch = str(pJoshID) + '.' + str(pPackageBatchNum)
                else:
                    if pJobID > 0:
                        tBatch = pJobID
                        if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                            tBatch = str(pJobID) + '.' + str(pPackageBatchNum)
            
            elif (pInventoryBatchOption == 3):
                if pJobID > 0:
                    tERPJobID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('ERPJobID', 'TblJob', 'ID = ' + str(pJobID), 'CN'))
                    if tERPJobID != '':
                        tBatch = tERPJobID
                        if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                            tBatch = tERPJobID + '.' + str(pPackageBatchNum)
                    else:
                        tOriginalJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('OriginalJobID', 'TblJob', 'ID = ' + str(pJobID), 'CN'))
                        if tOriginalJobID > 0:
                            tBatch = str(tOriginalJobID)
                            if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                                tBatch = str(tOriginalJobID) + '.' + str(pPackageBatchNum)

            elif (pInventoryBatchOption == 4):
                if pJobID > 0:
                    tOriginalJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('OriginalJobID', 'TblJob', 'ID = ' + str(pJobID), 'CN'))
                    if tOriginalJobID > 0:
                        tBatch = str(tOriginalJobID)
                        if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                            tBatch = str(tOriginalJobID) + '.' + str(pPackageBatchNum)
                    else:
                        tBatch = str(pJobID)
                        if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                            tBatch = str(pJobID) + '.' + str(pPackageBatchNum)

            elif (pInventoryBatchOption == 5):
                tInventoryBatchOptionFormat = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('InventoryBatchOptionFormat', 'TblPackageType', 'ID = ' + str(pPackageTypeID), 'CN'))
                if tInventoryBatchOptionFormat != '':
                    
                    tSets = tInventoryBatchOptionFormat.split(';')
                    for TCount in range(0, ( len(tSets) - 1 )):
                        tSingleSet = tSets[TCount].split(':')
                        tFieldName = MdlADOFunctions.fGetRstValString(tSingleSet(0))
                        tFormatString = MdlADOFunctions.fGetRstValString(tSingleSet(1))
                        if tFieldName != '' and tFormatString != '':
                            if (tFieldName == 'JobID'):
                                tStr = pJobID
                            elif (tFieldName == 'JoshID'):
                                tStr = pJoshID
                            elif (tFieldName == 'ERPJobID'):
                                tERPJobID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('ERPJobID', 'TblJob', 'ID = ' + str(pJobID), 'CN'))
                                if tERPJobID != '':
                                    tStr = tERPJobID
                            elif (tFieldName == 'PackageBatchNum'):
                                tStr = pPackageBatchNum
                            elif (tFieldName == 'PackageTypeID'):
                                tStr = pPackageTypeID
                            else:
                                tStr = tFieldName

                        tBatch = tBatch + tStr.format(tFormatString)
            else:
                if pJobID > 0:
                    tBatch = pJobID
                    if MdlADOFunctions.fGetRstValLong(pPackageBatchNum) > 0:
                        tBatch = str(pJobID) + "." + str(pPackageBatchNum)

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('CreateBatchFormat', str(0), error.args[0], 'PackageType = ' + str(pPackageTypeID) + ' | JobID = ' + str(pJobID) + ' | Numerator = ' + str(pPackageBatchNum))

    return returnVal






def GetLabelReportingProperties(pLabelID, pLabelGroupID, pInventoryReportOption, pAddUnitsReportedOKToJob, pAddUnitsReportedOKField, pPackagesInventory, pAddToActivePallet):
    returnVal = None
    strSQL = ''

    Rst = None
    
    returnVal = False
    strSQL = 'SELECT PackagesInventory, LabelGroupID, InventoryReportOption, AddUnitsReportedOKToJob, AddUnitsReportedOKField, AddToActivePallet' + vbCrLf
    strSQL = strSQL + 'FROM MetaTblLabels' + vbCrLf
    strSQL = strSQL + 'WHERE ID = ' + pLabelID
    Rst.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    if Rst.RecordCount == 1:
        pLabelGroupID = MdlADOFunctions.fGetRstValLong(Rst.Fields("LabelGroupID").Value)
        pInventoryReportOption = MdlADOFunctions.fGetRstValLong(Rst.Fields("InventoryReportOption").Value)
        pAddUnitsReportedOKToJob = MdlADOFunctions.fGetRstValBool(Rst.Fields("AddUnitsReportedOKToJob").Value, False)
        pAddUnitsReportedOKField = MdlADOFunctions.fGetRstValString(Rst.Fields("AddUnitsReportedOKField").Value)
        pPackagesInventory = MdlADOFunctions.fGetRstValBool(Rst.Fields("PackagesInventory").Value, False)
        pAddToActivePallet = MdlADOFunctions.fGetRstValBool(Rst.Fields("AddToActivePallet").Value, False)
    Rst.Close()
    returnVal = True
    if Err.Number != 0:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('GetLabelReportingProperties', str(0), error.args[0], 'LabelID = ' + str(pLabelID))
        Err.Clear()
    Rst = None
    return returnVal


def DeleteLabelData(pJobID):
    returnVal = None
    strSQL = ''

    Rst = None

    tQueueID = 0
    
    strSQL = 'SELECT * FROM TblLabelsQueue WHERE UserID = -' + gServer.SCID + ' AND ObjectID = ' + pJobID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    while not Rst.EOF:
        tQueueID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
        strSQL = 'DELETE FROM MetaTblLabelFieldValues WHERE QueueID = ' + tQueueID
        MetaMdlConnection.Cn.execute(strSQL)
        Rst.MoveNext()
    Rst.Close()
    strSQL = 'DELETE FROM TblLabelsQueue WHERE UserID = -' + gServer.SCID + ' AND ObjectID = ' + pJobID
    MdlConnection.CN.execute(strSQL)
    if Err.Number != 0:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('DeleteLabelData', str(0), error.args[0], 'JobID = ' + str(pJobID))
        Err.Clear()
    Rst = None
    return returnVal

def PrepareJobRecipeLabelField(pFieldName, pRecipeRst):
    returnVal = None
    tValue = ''
    
    returnVal = ''
    pRecipeRst.Filter = ''
    pRecipeRst.Filter = 'ChannelNum = 0 AND SplitNum = 0 AND PropertyName = \'' + pFieldName + '\''
    if pRecipeRst.RecordCount == 1:
        returnVal = MdlADOFunctions.fGetRstValString(pRecipeRst.Fields("FValue").Value)
    pRecipeRst.Filter = ''
    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            Err.Clear()
            
        Err.Clear()
    return returnVal








def GetLabelInventoryReportParameters(pInventoryReportOption, pWareHouseID, pWareHouseLocation, pWareHouseLocationID, pLabelID, pMachineID, pJobID):
    returnVal = None
    tProductID = 0

    strSQL = ''

    Rst = None
    
    returnVal = False
    if (pInventoryReportOption == 1):
        strSQL = 'SELECT DefaultWareHouse, DefaultWareHouseLocation, DefaultWareHouseLocationID FROM TblMachines WHERE ID = ' + pMachineID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        pWareHouseID = MdlADOFunctions.fGetRstValLong(Rst.Fields("DefaultWareHouse").Value)
        pWareHouseLocation = MdlADOFunctions.fGetRstValString(Rst.Fields("DefaultWareHouseLocation").Value)
        pWareHouseLocationID = MdlADOFunctions.fGetRstValLong(Rst.Fields("DefaultWareHouseLocationID").Value)
        Rst.Close()
    elif (pInventoryReportOption == 3):
        strSQL = 'SELECT DestinationWareHouse, DestinationWareHouseLocation, DestinationWareHouseLocationID FROM TblJob WHERE ID = ' + pJobID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        pWareHouseID = MdlADOFunctions.fGetRstValLong(Rst.Fields("DestinationWareHouse").Value)
        pWareHouseLocation = MdlADOFunctions.fGetRstValString(Rst.Fields("DestinationWareHouseLocation").Value)
        pWareHouseLocationID = MdlADOFunctions.fGetRstValLong(Rst.Fields("DestinationWareHouseLocationID").Value)
        Rst.Close()
    elif (pInventoryReportOption == 4):
        tProductID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductID', 'TblJob', 'ID = ' + str(tProductID), 'CN'))
        strSQL = 'SELECT DefaultWareHouse, DefaultWareHouseLocation, DefaultWareHouseLocationID FROM TblProduct WHERE ID = ' + tProductID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        pWareHouseID = MdlADOFunctions.fGetRstValLong(Rst.Fields("DefaultWareHouse").Value)
        pWareHouseLocation = MdlADOFunctions.fGetRstValString(Rst.Fields("DefaultWareHouseLocation").Value)
        pWareHouseLocationID = MdlADOFunctions.fGetRstValLong(Rst.Fields("DefaultWareHouseLocationID").Value)
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
            
        Err.Clear()
    if Rst.State != 0:
        Rst.Close()
    Rst = None
    return returnVal

def GetInventoryItemsCountForStatus(pJobID, pStatus, pLabelGroupID):
    returnVal = None
    tInventoryBatchOption = 0

    tMachineTypeID = 0

    tDefaultOutputPackageTypeID = 0

    tItemsCount = 0

    tERPJobID = ''

    strSQL = ''

    Rst = None
    
    returnVal = 0
    tMachineTypeID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineType', 'TblJob', 'ID = ' + pJobID, 'CN'))
    tDefaultOutputPackageTypeID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('DefaultOutputPackageTypeID', 'STblMachineTypes', 'ID = ' + tMachineTypeID, 'CN'))
    tInventoryBatchOption = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'InventoryBatchOption\'', 'CN'))
    if tMachineTypeID > 0 and tDefaultOutputPackageTypeID > 0 and pJobID > 0:
        if (tInventoryBatchOption == 1):
            if (pLabelGroupID == 1):
                strSQL = 'SELECT (CASE WHEN EXISTS (SELECT ID FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND Status IN(12, ' + pStatus + ') AND PackageLocalNumber =  (SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')))' + vbCrLf
                strSQL = strSQL + 'THEN (SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')) + 1' + vbCrLf
                strSQL = strSQL + 'ELSE' + vbCrLf
                strSQL = strSQL + '(SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')) END) AS CountID'
                Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                Rst.ActiveConnection = None
                if Rst.RecordCount == 1:
                    tItemsCount = MdlADOFunctions.fGetRstValLong(Rst.Fields("CountID").Value)
                Rst.Close()
            elif (pLabelGroupID == 4):
                tItemsCount = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('COUNT(ID)', 'TblInventory', 'JobID = ' + str(pJobID) + ' AND Status IN (12, ' + pStatus + ') AND PackageTypeID = ' + tDefaultOutputPackageTypeID, 'CN'))
        elif (tInventoryBatchOption == 2):
            if (pLabelGroupID == 1):
                strSQL = 'SELECT (CASE WHEN EXISTS (SELECT ID FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND Status IN(12, ' + pStatus + ') AND PackageLocalNumber =  (SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')))' + vbCrLf
                strSQL = strSQL + 'THEN (SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')) + 1' + vbCrLf
                strSQL = strSQL + 'ELSE' + vbCrLf
                strSQL = strSQL + '(SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')) END) AS CountID'
                Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                Rst.ActiveConnection = None
                if Rst.RecordCount == 1:
                    tItemsCount = MdlADOFunctions.fGetRstValLong(Rst.Fields("CountID").Value)
                Rst.Close()
            elif (pLabelGroupID == 4):
                tItemsCount = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('COUNT(ID)', 'TblInventory', 'JobID = ' + str(pJobID) + ' AND Status IN (12, ' + pStatus + ') AND PackageTypeID = ' + tDefaultOutputPackageTypeID, 'CN'))
        elif (tInventoryBatchOption == 3):
            tERPJobID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('ERPJobID', 'TblJob', 'ID = ' + pJobID, 'CN'))
            if tERPJobID != '':
                if (pLabelGroupID == 1):
                    strSQL = 'SELECT (CASE WHEN EXISTS (SELECT ID FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND Status IN(12, ' + pStatus + ') AND PackageLocalNumber =  (SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID IN (SELECT ID FROM TblJob WHERE ERPJobID = \'' + tERPJobID + '\') AND Status IN(12,' + pStatus + ')))' + vbCrLf
                    strSQL = strSQL + 'THEN (SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID IN (SELECT ID FROM TblJob WHERE ERPJobID = \'' + tERPJobID + '\') AND Status IN(12,' + pStatus + ')) + 1' + vbCrLf
                    strSQL = strSQL + 'ELSE' + vbCrLf
                    strSQL = strSQL + '(SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID IN (SELECT ID FROM TblJob WHERE ERPJobID = \'' + tERPJobID + '\') AND Status IN(12,' + pStatus + ')) END) AS CountID'
                    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                    Rst.ActiveConnection = None
                    if Rst.RecordCount == 1:
                        tItemsCount = MdlADOFunctions.fGetRstValLong(Rst.Fields("CountID").Value)
                    Rst.Close()
                elif (pLabelGroupID == 4):
                    tItemsCount = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('COUNT(ID)', 'TblInventory', 'JobID IN (SELECT ID FROM TblJob WHERE ERPJobID = \'' + tERPJobID + '\') AND Status IN (12, ' + pStatus + ') AND PackageTypeID = ' + tDefaultOutputPackageTypeID, 'CN'))
            else:
                
                strSQL = 'SELECT (CASE WHEN EXISTS (SELECT ID FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND Status IN(12, ' + pStatus + ') AND PackageLocalNumber =  (SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')))' + vbCrLf
                strSQL = strSQL + 'THEN (SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')) + 1' + vbCrLf
                strSQL = strSQL + 'ELSE' + vbCrLf
                strSQL = strSQL + '(SELECT COUNT(ID) FROM TblInventory WHERE PackageTypeID = ' + tDefaultOutputPackageTypeID + ' AND JobID = ' + str(pJobID) + ' AND Status IN(12,' + pStatus + ')) END) AS CountID'
                Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                Rst.ActiveConnection = None
                if Rst.RecordCount == 1:
                    tItemsCount = MdlADOFunctions.fGetRstValLong(Rst.Fields("CountID").Value)
                Rst.Close()
    else:
        tItemsCount = - 1
    returnVal = tItemsCount
    if Err.Number != 0:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('GetInventoryItemsCountForStatus', str(0), error.args[0], 'JobID=' + str(pJobID))
        Err.Clear()
    Rst = None
    return returnVal
