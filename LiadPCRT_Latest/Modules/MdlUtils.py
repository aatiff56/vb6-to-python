import MdlADOFunctions
import mdl_Common
import MdlConnection
import MdlGlobal
import requests

def XmlHeader():
    return strXMLHeader

def fGetStringNumber(strString, Num, MaxDigits):
    Counter = 0
    strTemp = ''
    tNum = 0
    NCount = 0
    tNum = Num
    strTemp = strString

    for Counter in range(1, MaxDigits):
        if int(tNum / 10) > 0:
            NCount = NCount + 1
            tNum = tNum / 10
    if MaxDigits > NCount:
        for Counter in range(1, MaxDigits - NCount - 1):
            strTemp = strTemp + '0'
    fn_return_value = strTemp + Num
    return fn_return_value

def fMoveTableToHistory(TableName, TimeField, JobField, HistoryEndIntervalMin, HistoryIntervalMin, MachineID, ParamID, HistoryType, boolEndOfBatchTablesForTrigger=False):
    strSQL = ''
    strTemp = ''
    strFieldName = ''
    tDate = Date()
    fcount = 0
    Job = 0
    CurrentDate = Date()
    RstCursor = None
    rstDestCursor = None
    LastHistoryTSRstCursor = MdlConnection.CN.cursor()
    HistoryInterval = 0
    temp = 0
    Counter = 0
    tempSqlTS = ''
    LastRecordSPCTableTS = Date()
    LastRecordControllerTableTS = Date()
    tempTS = ''
    RecrdCount = 0
    
    try:
        HistoryInterval = gServer.SystemVariables.HistoryIntervalMin
        if HistoryInterval == 0:
            HistoryInterval = 15
        HistoryEndIntervalMin = gServer.SystemVariables.HistoryEndIntervalMin
        strSQL = 'SELECT * FROM ' + TableName + 'History WHERE ID = 0'

        rstDestCursor = MdlConnection.CN.cursor()
        rstDestCursor.execute(strSQL)
        rstDestVal = rstDestCursor.fetchone()

        tDate = DateAdd('n', 0 - HistoryEndIntervalMin, NowGMT())
        strTemp = Month(tDate) + '/' + Day(tDate) + '/' + Year(tDate) + ' ' + Hour(tDate) + ':' + Minute(tDate) + ':' + Second(tDate)
        strSQL = 'Select Count(ID) AS CID From ' + TableName + ' Where MachineID = ' + MachineID + ' AND ' + TimeField + ' <=\'' + strTemp + '\''

        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstVal = RstCursor.fetchone()

        while RstVal["CID"] > 0:
            RstCursor.Close()
            strSQL = 'Select TOP 10000 * From ' + TableName + ' Where MachineID = ' + MachineID + ' AND ' + TimeField + ' <=\'' + strTemp + '\' Order BY ' + JobField + ' , ' + TimeField

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstVal = RstCursor.fetchone()
            Counter = 0
            while not RstCursor.next():
                if Counter == 0:
                    if HistoryType == 'ControllerUser':
                        tempTS = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('LastRecordToControllerUserHistoryTableTS', 'TblControllerFields', 'ID = ' + ParamID, 'CN'))
                        if IsDate(tempTS):
                            CurrentDate = CDate(tempTS)
                    else:
                        tempTS = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('LastRecordToTSPCHistoryTableTS', 'TblControllerFields', 'ID = ' + ParamID, 'CN'))
                        if IsDate(tempTS):
                            CurrentDate = CDate(tempTS)
                Job = RstVal[JobField]
                if RstVal[JobField] != Job or abs(DateDiff('n', CurrentDate, RstVal[TimeField])) > HistoryInterval:
                    
                    CurrentDate = RstVal[TimeField]
                    rstDestCursor.AddNew()
                    for fcount in range(0, RstCursor.Fields.Count - 1):
                        strFieldName = RstVal[fcount].Name
                        if strFieldName != 'ID':
                            rstDestCursor.Fields[strFieldName].value = RstVal[strFieldName]
                    rstDestCursor.Update()
                else:
                    pass
                Counter = Counter + 1
                
                RstCursor.execute('Delete ' + TableName + ' Where ID = ' + RstVal["ID"])
            RstCursor.Close()
            if HistoryType == 'ControllerUser' and boolEndOfBatchTablesForTrigger:
                tempTS = MdlADOFunctions.fGetDateTimeFormat(CurrentDate, True)
                tempSqlTS = 'UPDATE TblControllerFields SET LastRecordToControllerUserHistoryTableTS = ' + tempTS + ' WHERE ID = ' + ParamID
                RstCursor.execute(tempSqlTS)
            else:
                if HistoryType == 'TSPC':
                    tempTS = MdlADOFunctions.fGetDateTimeFormat(CurrentDate, True)
                    tempSqlTS = 'UPDATE TblControllerFields SET LastRecordToTSPCHistoryTableTS = ' + tempTS + ' WHERE ID = ' + ParamID
                    RstCursor.execute(( tempSqlTS ))
            strTemp = Month(tDate) + '/' + Day(tDate) + '/' + Year(tDate) + ' ' + Hour(tDate) + ':' + Minute(tDate) + ':' + Second(tDate)
            strSQL = 'SELECT Count(ID) AS CID From ' + TableName + ' Where  MachineID = ' + MachineID + ' AND ' + TimeField + ' <=\'' + strTemp + '\''
            RstCursor = MdlConnection.CN.cursor()

        RstCursor.Close()
        rstDestCursor.Close()

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('LeaderRT:fMoveTableToHistory', 0, error.args[0], '')
                
    if RstCursor:
        RstCursor.Close()
    RstCursor = None

    if LastHistoryTSRstCursor:
        LastHistoryTSRstCursor.Close()
    LastHistoryTSRstCursor = None

    if rstDestCursor:
        rstDestCursor.Close()
    rstDestCursor = None


def fGetRecipeValueStandard(StandardID, PropertyName, ChannelNum, SplitNum, ProductID):
    PropertyID = 0
    MachineType = 0
    strTemp = ''
    MachineType = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineType', 'TblProduct', 'ID = ' + ProductID, 'CN'))
    PropertyID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'STblMachineTypeProperties', 'MachineType = ' + MachineType + ' AND PropertyName = \'' + PropertyName + '\'', 'CN'))
    if PropertyID > 0:
        strTemp = '' + MdlADOFunctions.GetSingleValue('FValue', 'TblRecipeStandards', 'StandardID = ' + StandardID + ' AND PropertyID = ' + PropertyID + ' AND ChannelNum =  ' + ChannelNum + ' AND SplitNum = ' + SplitNum, 'CN')
    return strTemp


def GetValueFromConversion(ConversionID, SourceValue):
    strSQL = ''
    RstCursor = None
    fn_return_value = ''
    try:
        strSQL = 'SELECT TargetValue FROM STblControllerFieldsConversionValues WHERE ConversionID = ' + ConversionID + ' AND SourceValue = N\'' + SourceValue + '\''
        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        val = RstCursor.fetchone()
        if val:
            fn_return_value = '' + val["TargetValue"]
        else:
            fn_return_value = SourceValue

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

    if RstCursor:
        RstCursor.Close()
    RstCursor = None
    return fn_return_value


def CallAPIRequest(APIFunction, RequestBody, RequestMethod='POST', Async=False):
    requests.pos
    sUrl = ''
    sResponse = ''
    sRequest = ''
    key = None
    FirstItem = False
    sResponseStatus = ''
    fn_return_value = False
    httpResponse = None
    requestHeaders = {
            'Content-Type', 'application/json',
            'x-app-key', 'TGVhZGVyUmVhbFRpbWU7VEdWaFpHVnlVbVZoYkZScGJXVXhNak09'
        }

    try:
        sUrl = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'CustomerAPIAddress\'', 'CN'))
        FirstItem = True
        if not RequestBody is None:
            for key in RequestBody.keys:
                if not FirstItem:
                    sRequest = sRequest + ','
                else:
                    FirstItem = False
                sRequest = sRequest + chr(34) + key + chr(34) + ': ' + chr(34) + RequestBody(key) + chr(34)
        sRequest = '{' + sRequest + '}'
        httpResponse = requests.post(url = 'https://' + sUrl + '/LeaderMESApi/' + APIFunction, headers = requestHeaders)
        if not Async:
            sResponseStatus = MdlADOFunctions.fGetRstValString(httpResponse.request.Status)
            sResponse = MdlADOFunctions.fGetRstValString(httpResponse.request.ResponseText)
        else:
            sResponseStatus = '200'
        if Async:
            fn_return_value = True
        else:
            if 'FunctionSucceed' + chr(34) + ':false' > 0 or sResponseStatus != '200' in sResponse:
                MdlGlobal.RecordError('CallAPIRequest', 0, '', 'Function:' + APIFunction + ' | Request:' + sRequest + ' | Response: ' + sResponse + ' | Status: ' + sResponseStatus)
                fn_return_value = False
            else:
                fn_return_value = True

    except BaseException as error:
        if sResponse != '':
            MdlGlobal.RecordError('CallAPIRequest', 0, error.args[0], 'Function:' + APIFunction + ' | Request:' + sRequest + ' | Response: ' + sResponse + ' | Status: ' + sResponseStatus)
        else:
            MdlGlobal.RecordError('CallAPIRequest', 0, error.args[0], 'Function:' + APIFunction + ' | Request:' + sRequest)

    httpResponse = None
    return fn_return_value


def GenericUpsert(NewRecordID, TableName, values, keys, isMeta=False):
    strSQL = ''
    Exists = 0
    FirstItem = False
    keysWhere = ''
    FuncResult = ''
    key = None
    fn_return_value = False
    
    try:
        FirstItem = True
        if not keys is None:
            for key in keys.keys:
                if not FirstItem:
                    keysWhere = keysWhere + ' AND '
                else:
                    FirstItem = False
                keysWhere = keysWhere + key + ' = ' + keys(key)
        if isMeta:
            Exists = MdlADOFunctions.GetSingleValue('ID', TableName, keysWhere, 'MetaCN')
        else:
            Exists = MdlADOFunctions.GetSingleValue('ID', TableName, keysWhere)
        if Exists > 0:
            
            if not SqlUpdate(FuncResult, TableName, values, keysWhere, isMeta):
                fn_return_value = False
            else:
                fn_return_value = True
        else:
            
            if not SqlInsert(FuncResult, TableName, values, isMeta):
                fn_return_value = False
            else:
                fn_return_value = True
                if FuncResult:
                    NewRecordID = MdlADOFunctions.fGetRstValLong(FuncResult)

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
    return fn_return_value


def SqlUpdate(FuncResult, TableName, values, where, isMeta=False):
    strSQL = ''
    valuesUpdate = ''
    Item = None
    FirstItem = False
    fn_return_value = False
    FirstItem = True

    try:
        for Item in values:
            if not FirstItem:
                valuesUpdate = valuesUpdate + ' ,'
            else:
                FirstItem = False
            valuesUpdate = valuesUpdate + Item + ' = ' + values(Item)
        strSQL = 'UPDATE ' + TableName + ' SET ' + valuesUpdate + ' WHERE ' + where
        if isMeta:
            MdlConnection.MetaCn.cursor().execute(strSQL)
        else:
            MdlConnection.CN.cursor().execute(strSQL)
        fn_return_value = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            FuncResult = 'SqlUpdate: ' + error.args[0]
    return fn_return_value


def SqlInsert(FuncResult, TableName, values, isMeta=False):
    strSQL = ''
    valuesInsert = ''
    columns = ''
    # rsTemp = Recordset()
    Item = None
    FirstItem = False
    fn_return_value = False
    FirstItem = True

    try:
        for Item in values:
            if not FirstItem:
                valuesInsert = valuesInsert + ' ,'
                columns = columns + ' ,'
            else:
                FirstItem = False
            valuesInsert = valuesInsert + values(Item)
            columns = columns + Item
        strSQL = 'INSERT INTO ' + TableName + ' (' + columns + ') output INSERTED.ID VALUES(' + valuesInsert + ')'
        if isMeta:
            MdlConnection.MetaCn.cursor().execute(strSQL)
        else:
            MdlConnection.CN.cursor().execute(strSQL)
        
        fn_return_value = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

            FuncResult = 'SqlInsert: ' + error.args[0]
    return fn_return_value
