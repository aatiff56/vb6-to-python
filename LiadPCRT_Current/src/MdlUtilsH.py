from datetime import datetime
import MdlADOFunctions
import mdl_Common
import GlobalVariables

cnTypeDateTime = '135'
cnTypeNVarCHar = '202'

def ShortDate(tDate, sql=False, AddTime=False, AddSecond=False):
    returnVal = ''
    try:

        if tDate.year > 1900:
            returnVal = str(tDate.day) + '/' + str(tDate.month) + '/' + str(tDate.year)
            if sql == True and mdl_Common.SQLDateOrder == 1:
                returnVal = str(tDate.month) + '/' + str(tDate.day) + '/' + str(tDate.year)

        if AddTime == True and  ( tDate.hour + tDate.minute )  > 0:
            if tDate.hour < 10:
                returnVal = returnVal + ' 0' + str(tDate.hour) + ':'
            else:
                returnVal = returnVal + ' ' + str(tDate.hour) + ':'
            if tDate.minute < 10:
                returnVal = returnVal + '0' + str(tDate.minute)
            else:
                returnVal = returnVal + str(tDate.minute)
 
        if AddSecond == True and  ( tDate.hour + tDate.minute + tDate.second > 0 ) :
            if tDate.hour + tDate.minute > 0:
                if tDate.second < 10:
                    returnVal = returnVal + ':0' + str(tDate.second)
                else:
                    returnVal = returnVal + ':' + str(tDate.second)
            else:
                returnVal = returnVal + ' 00:00'
                if tDate.second < 10:
                    returnVal = returnVal + ':0' + str(tDate.second)
                else:
                    returnVal = returnVal + ':' + str(tDate.second)

    except BaseException as error:
        returnVal = ''

    return returnVal


def fCopyRecordByForm(RstSource, RstTarget, RstFields):
    returnVal = None
    strFName = ''

    returnVal = False
    RstFields.MoveFirst()
    while not RstFields.EOF:
        strFName = '' + RstFields.Fields("Name").Value
        RstTarget.Fields[strFName].value = RstSource.Fields(strFName).value
        RstFields.MoveNext()
    returnVal = True
    return returnVal


def fGetShiftCalendarIDByMachine(pMachineID):
    returnVal = None
    strSQL = ''
    DepID = 0
    tDepartment = None
    tMachine = None
    tVariant = None
    returnVal = 0

    for tVariant in GlobalVariables.LeaderSVR.Machines:
        tMachine = tVariant
        if tMachine.ID == pMachineID:
            break
        tMachine = None
    if not tMachine is None:
        for tVariant in tMachine.Server.Departments:
            tDepartment = tVariant
            if tDepartment.ID == tMachine.Department:
                returnVal = tDepartment.ShiftCalendarID
                break
    else:
        if pMachineID != 0:
            DepID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('Department', 'TblMachines', 'ID = ' + pMachineID, 'CN'))
            if DepID != 0:
                returnVal = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ShiftCalendarID', 'STblDepartments', 'ID = ' + DepID, 'CN'))
            else:
                returnVal = 0
        else:
            returnVal = 0
    if Err.Number != 0:
        returnVal = 0
        Err.Clear()
    return returnVal


def fGetRecipeValueProduct(ProductID, PropertyName, ChannelNum, SplitNum, FieldName='FValue'):
    strTemp = ''
    PropertyID = 0
    MachineType = 0

    MachineType = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineType', 'TblProduct', 'ID = ' + str(ProductID), 'CN'))
    PropertyID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue("ID", "STblMachineTypeProperties", "MachineType = " + str(MachineType) + " AND PropertyName = '" + str(PropertyName) + "'", "CN"))
    if PropertyID > 0:
        strTemp = MdlADOFunctions.GetSingleValue(FieldName, 'TblProductRecipe', 'ProductID = ' + str(ProductID) + ' AND PropertyID = ' + str(PropertyID) + ' AND ChannelNum = ' + str(ChannelNum) + ' AND SplitNum = ' + str(SplitNum), 'CN')

    return strTemp


def fGetRecipeValueJob(JobID, PropertyName, ChannelNum, SplitNum, FieldName='FValue'):
    returnVal = None
    ProductID = 0
    PropertyID = 0
    MachineType = 0

    PropertyID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue("ID", "STblMachineTypeProperties", "MachineType = " & MachineType & " AND PropertyName = '" + PropertyName + "'", "CN"))

    if PropertyID > 0:
        strTemp = '' + MdlADOFunctions.GetSingleValue(FieldName, 'TblProductRecipeJob', 'JobID = ' + JobID + ' AND PropertyID = ' + PropertyID + ' AND ChannelNum =  ' + ChannelNum + ' AND SplitNum = ' + SplitNum, 'CN')
    returnVal = strTemp
    return returnVal


def GetChannelSplitProperty(pPropertyFieldName, pControllerID, pChannelNum, pSplitNum):
    returnVal = None
    if pChannelNum != 0:
        if pSplitNum != 0:
            returnVal = MdlADOFunctions.GetSingleValue(pPropertyFieldName, 'TblControllerChannelsSplits', 'ControllerID = ' + pControllerID + ' AND ChannelNum = ' + pChannelNum + ' AND SplitNum = ' + pSplitNum, 'CN')
        else:
            returnVal = MdlADOFunctions.GetSingleValue(pPropertyFieldName, 'TblControllerChannels', 'ControllerID = ' + pControllerID + ' AND ChannelNum = ' + pChannelNum, 'CN')
    if Err.Number != 0:
        Err.Clear()
    return returnVal
