import os
import MdlADOFunctions
import MdlGlobal
import MdlConnection

from Department import Department
from MachineType import MachineType
from Product import Product
from Mold import Mold

def GetOrCreateDepartment(pServer, pDepartmentID):
    returnVal = None
    tVariant = None
    tDepartment = None
    Found = False

    try:
        for tVariant in pServer.Departments.values():
            tDepartment = tVariant
            if tDepartment.ID == pDepartmentID:
                returnVal = tDepartment
                Found = True
                break
        if not Found:
            tDepartment = Department()
            tDepartment.Init(pServer, pDepartmentID)
            pServer.Departments[str(pDepartmentID)] = tDepartment
            returnVal = tDepartment

    except BaseException as error:
        MdlGlobal.RecordError('GetOrCreateDepartment', str(0), error.args[0], 'DepartmentID: ' + str(pDepartmentID))

    return returnVal


def GetOrCreateMachineType(pServer, pMachineTypeID):
    returnVal = None
    tVariant = None
    tMachineType = None
    Found = False

    try:
        for tVariant in pServer.MachineTypes.values():
            tMachineType = tVariant
            if tMachineType.ID == pMachineTypeID:
                returnVal = tMachineType
                Found = True
                break
        if not Found:
            tMachineType = MachineType()
            tMachineType.Init(pMachineTypeID)
            pServer.MachineTypes[str(pMachineTypeID)] = tMachineType
            returnVal = tMachineType

    except BaseException as error:
        MdlGlobal.RecordError('GetOrCreateMachineType', str(0), error.args[0], 'MachineTypeID: ' + str(pMachineTypeID))

    return returnVal


def GetOrCreateMold(pServer, pMoldID):
    returnVal = None
    tVariant = None
    tMold = None
    Found = False

    try:
        for tVariant in pServer.Molds.values():
            tMold = tVariant
            if tMold.ID == pMoldID:
                tMold.Refresh
                returnVal = tMold
                Found = True
                break

        if not Found:
            tMold = Mold()
            tMold.Init(pMoldID)
            pServer.Molds[str(pMoldID)] = tMold
            returnVal = tMold

    except BaseException as error:
        MdlGlobal.RecordError('GetOrCreateMold', str(0), error.args[0], 'MoldID: ' + str(pMoldID))

    return returnVal


def GetOrCreateProduct(pServer, pProductID):
    returnVal = None
    tVariant = None
    tProduct = None
    Found = False

    try:
        for tVariant in pServer.Products.values():
            tProduct = tVariant
            if tProduct.ID == pProductID:
                returnVal = tProduct
                Found = True
                break
        if not Found:
            tProduct = Product()
            tProduct.Init(pProductID)
            pServer.Products[str(pProductID)] = tProduct
            returnVal = tProduct

    except BaseException as error:
        MdlGlobal.RecordError('GetOrCreateProduct', str(0), error.args[0], 'ProductID: ' + str(pProductID))

    return returnVal


def fCheckForDuplicateRealTimes(pServer):
    try:    
        if pServer.ShiftCalendar.WindowsProcessID != 0:
            os.kill(pServer.ShiftCalendar.WindowsProcessID, 0)
    except OSError:
        return False
    else:
        return True
        

def IsDoubleNull(tValue):    
    returnVal = False

    try:
        if tValue == - 999999999:
            returnVal = True
    except:
        pass

    return returnVal

def GetRefMachineIDForRefControllerField(FieldName):
    returnVal = None
    tArray = []
    tMachineID = 0

    try:
        tArray = FieldName.split('.')
        tArray[0] = tArray[0].replace( 'M', '')
        tMachineID = int(tArray[0])
        returnVal = tMachineID
    except:
        pass

    return returnVal


def GetRefFieldNameForRefControllerField(FieldName):
    returnVal = None
    tArray = []
    tFieldName = ''

    tArray = FieldName.split('.')
    tFieldName = tArray[1]
    returnVal = tFieldName
    if Err.Number != 0:
        Err.Clear()
    return returnVal


def fCheckCalendarForCloseEventsOnStart(pMachineID, pEventTime, pDuration, pEventID, pEventGroupID):
    returnVal = None
    strSQL = ''
    temp = ''
    Rst = ADODB.Recordset()
    CalendarID = 0
    Proportion = 0.0
    CDType = 0
    CEDateDiff = 0.0
    ProportionTemp = 0.0
    CalendarEventID = None
    CalendarEventGroupID = 0
    DepartmentID = 0
    DepCalendarID = 0
    
    returnVal = False
    ProportionTemp = 0
    CalendarEventID = 0
    CalendarEventGroupID = 0
    if pDuration <= 0:
        Rst = None
        return returnVal
    strSQL = 'SELECT CalendarID, Department FROM TblMachines WHERE ID = ' + pMachineID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    if Rst.RecordCount == 1:
        CalendarID = MdlADOFunctions.fGetRstValLong(Rst.Fields("CalendarID").Value)
        DepartmentID = MdlADOFunctions.fGetRstValLong(Rst.Fields("Department").Value)
    Rst.Close()
    DepCalendarID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CalendarID', 'STblDepartments', 'ID=' + DepartmentID, 'CN'))
    strSQL = 'Select * From ViewTblCalendarExceptions Where (CalendarID = ' + CalendarID + ' OR CalendarID = ' + DepCalendarID + ') AND (Idle = ' + 1 + ')'
    strSQL = strSQL + ' AND ('
    strSQL = strSQL + '(DateFrom >= \'' + ShortDate(pEventTime, True, True) + '\' AND DateTo <= \'' + ShortDate(NowGMT, True, True) + '\') '
    strSQL = strSQL + 'OR (DateFrom <= \'' + ShortDate(pEventTime, True, True) + '\' AND DateTo >= \'' + ShortDate(NowGMT, True, True) + '\') '
    strSQL = strSQL + 'OR (DateFrom <= \'' + ShortDate(pEventTime, True, True) + '\' AND DateTo >= \'' + ShortDate(pEventTime, True, True) + '\' AND DateTo <= \'' + ShortDate(NowGMT, True, True) + '\') '
    strSQL = strSQL + 'OR (DateFrom >= \'' + ShortDate(pEventTime, True, True) + '\' AND DateFrom <= \'' + ShortDate(NowGMT, True, True) + '\' AND DateTo >= \'' + ShortDate(NowGMT, True, True) + '\') '
    strSQL = strSQL + ' ) AND YEAR(DateFrom) >= (YEAR(getdate()) - 1) ORDER BY DateFrom'
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    Proportion = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CalendarEventProportion', 'STblSystemVariables', 'ID=1', 'CN'))
    while not Rst.EOF:
        if CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)) >= CDate(ShortDate(pEventTime, False, True)) and CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)) <= CDate(ShortDate(NowGMT, False, True)):
            CDType = 1
            
            CEDateDiff = DateDiff('s', CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)), CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)))
            
        else:
            if CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)) <= CDate(ShortDate(pEventTime, False, True)) and CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)) >= CDate(ShortDate(NowGMT, False, True)):
                CDType = 2
                CEDateDiff = pDuration
                
            else:
                if CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)) <= CDate(ShortDate(pEventTime, False, True)) and CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)) <= CDate(ShortDate(NowGMT, False, True)):
                    CDType = 3
                    
                    CEDateDiff = DateDiff('s', CDate(ShortDate(pEventTime, False, True)), CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)))
                else:
                    if CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)) >= CDate(ShortDate(pEventTime, False, True)) and CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)) >= CDate(ShortDate(NowGMT, False, True)):
                        CDType = 4
                        
                        CEDateDiff = DateDiff('s', CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)), CDate(ShortDate(NowGMT, False, True)))
                    else:
                        CDType = 5
                        CEDateDiff = 0
        if CEDateDiff > 0:
            if pDuration <= CEDateDiff:
                if ( ( ( pDuration / CEDateDiff )  * 100 )  >= Proportion )  and  ( ( ( pDuration / CEDateDiff )  * 100 )  > ProportionTemp ) :
                    ProportionTemp = ( pDuration / CEDateDiff )  * 100
                    CalendarEventID = MdlADOFunctions.fGetRstValLong(Rst.Fields("event").Value)
                    CalendarEventGroupID = MdlADOFunctions.fGetRstValLong(Rst.Fields("EventGroup").Value)
            else:
                if ( ( ( CEDateDiff / pDuration )  * 100 )  >= Proportion )  and  ( ( ( CEDateDiff / pDuration )  * 100 )  > ProportionTemp ) :
                    ProportionTemp = ( CEDateDiff / pDuration )  * 100
                    CalendarEventID = MdlADOFunctions.fGetRstValLong(Rst.Fields("event").Value)
                    CalendarEventGroupID = MdlADOFunctions.fGetRstValLong(Rst.Fields("EventGroup").Value)
        Rst.MoveNext()
    Rst.Close()
    if ( ProportionTemp >= Proportion )  and  ( ProportionTemp > 0 ) :
        pEventID = CalendarEventID
        pEventGroupID = CalendarEventGroupID
        returnVal = True
    else:
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
            
        MdlGlobal.RecordError('MdlServer:fCheckCalendarForCloseEventsOnStart', str(Err.Number), Err.Description, 'MachineID = ' + pMachineID)
        Err.Clear()
    if Rst.State != 0:
        returnVal = False
        Rst.Close()
    Rst = None
    return returnVal


