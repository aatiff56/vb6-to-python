import os

# def GetOrCreateDepartment(pServer, pDepartmentID):
#     returnVal = None
#     tVariant = Variant()
#     tDepartment = Department()
#     Found = Boolean()
    
#     for tVariant in pServer.Departments:
#         tDepartment = tVariant
#         if tDepartment.ID == pDepartmentID:
#             returnVal = tDepartment
#             Found = True
#             break
#     if not Found:
#         tDepartment = Department()
#         tDepartment.Init(pServer, pDepartmentID)
#         pServer.Departments.Add(tDepartment, CStr(pDepartmentID))
#         returnVal = tDepartment
#     if Err.Number != 0:
#         RecordError('GetOrCreateDepartment', Err.Number, Err.Description, 'DepartmentID: ' + pDepartmentID)
#         Err.Clear()
#     return returnVal


# def GetOrCreateMachineType(pServer, pMachineTypeID):
#     returnVal = None
#     tVariant = Variant()
#     tMachineType = MachineType()
#     Found = Boolean()
    
#     for tVariant in pServer.MachineTypes:
#         tMachineType = tVariant
#         if tMachineType.ID == pMachineTypeID:
#             returnVal = tMachineType
#             Found = True
#             break
#     if not Found:
#         tMachineType = MachineType()
#         tMachineType.Init(pMachineTypeID)
#         pServer.MachineTypes.Add(tMachineType, CStr(pMachineTypeID))
#         returnVal = tMachineType
#     if Err.Number != 0:
#         RecordError('GetOrCreateMachineType', Err.Number, Err.Description, 'MachineTypeID: ' + pMachineTypeID)
#         Err.Clear()
#     return returnVal


# def GetOrCreateMold(pServer, pMoldID):
#     returnVal = None
#     tVariant = Variant()

#     tMold = Mold()

#     Found = Boolean()
    
#     for tVariant in pServer.Molds:
#         tMold = tVariant
#         if tMold.ID == pMoldID:
#             tMold.Refresh
#             returnVal = tMold
#             Found = True
#             break
#     if not Found:
#         tMold = Mold()
#         tMold.Init(pMoldID)
#         pServer.Molds.Add(tMold, CStr(pMoldID))
#         returnVal = tMold
#     if Err.Number != 0:
#         RecordError('GetOrCreateMold', Err.Number, Err.Description, 'MoldID: ' + pMoldID)
#         Err.Clear()
#     return returnVal


# def GetOrCreateProduct(pServer, pProductID):
#     returnVal = None
#     tVariant = Variant()

#     tProduct = Product()

#     Found = Boolean()
    
#     for tVariant in pServer.Products:
#         tProduct = tVariant
#         if tProduct.ID == pProductID:
#             returnVal = tProduct
#             Found = True
#             break
#     if not Found:
#         tProduct = Product()
#         tProduct.Init(pProductID)
#         pServer.Products.Add(tProduct, CStr(pProductID))
#         returnVal = tProduct
#     if Err.Number != 0:
#         RecordError('GetOrCreateProduct', Err.Number, Err.Description, 'ProductID: ' + pProductID)
#         Err.Clear()
#     return returnVal


def fCheckForDuplicateRealTimes(pServer):
    try:    
        if pServer.ShiftCalendar.WindowsProcessID != 0:
            os.kill(pServer.ShiftCalendar.WindowsProcessID, 0)
    except OSError:
        return False
    else:
        return True
        


# def IsDoubleNull(tValue):
#     returnVal = None
    
#     returnVal = False
#     if tValue == - 999999999:
#         returnVal = True
#     if Err.Number != 0:
#         Err.Clear()
#     return returnVal

# def GetRefMachineIDForRefControllerField(FieldName):
#     returnVal = None
#     tArray = vbObjectInitialize(objtype=String)

#     tMachineID = Long()
    
    
#     tArray = Split(FieldName, '.')
#     tArray[0] = Replace(tArray(0), 'M', '')
#     tMachineID = CLng(tArray(0))
#     returnVal = tMachineID
#     if Err.Number != 0:
#         Err.Clear()
#     return returnVal

# def GetRefFieldNameForRefControllerField(FieldName):
#     returnVal = None
#     tArray = vbObjectInitialize(objtype=String)

#     tFieldName = String()
    
    
#     tArray = Split(FieldName, '.')
#     tFieldName = tArray(1)
#     returnVal = tFieldName
#     if Err.Number != 0:
#         Err.Clear()
#     return returnVal



# def fCheckCalendarForCloseEventsOnStart(pMachineID, pEventTime, pDuration, pEventID, pEventGroupID):
#     returnVal = None
#     strSQL = String()
#     temp = String()
#     Rst = ADODB.Recordset()
#     CalendarID = Long()
#     Proportion = Double()
#     CDType = Long()
#     CEDateDiff = Double()
#     ProportionTemp = Double()
#     CalendarEventID = Variant()
#     CalendarEventGroupID = Long()
#     DepartmentID = Long()
#     DepCalendarID = Long()
    
#     returnVal = False
#     ProportionTemp = 0
#     CalendarEventID = 0
#     CalendarEventGroupID = 0
#     if pDuration <= 0:
#         Rst = None
#         return returnVal
#     strSQL = 'SELECT CalendarID, Department FROM TblMachines WHERE ID = ' + pMachineID
#     Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
#     Rst.ActiveConnection = None
#     if Rst.RecordCount == 1:
#         CalendarID = fGetRstValLong(Rst.Fields("CalendarID").Value)
#         DepartmentID = fGetRstValLong(Rst.Fields("Department").Value)
#     Rst.Close()
#     DepCalendarID = fGetRstValLong(GetSingleValue('CalendarID', 'STblDepartments', 'ID=' + DepartmentID, 'CN'))
#     strSQL = 'Select * From ViewTblCalendarExceptions Where (CalendarID = ' + CalendarID + ' OR CalendarID = ' + DepCalendarID + ') AND (Idle = ' + 1 + ')'
#     strSQL = strSQL + ' AND ('
#     strSQL = strSQL + '(DateFrom >= \'' + ShortDate(pEventTime, True, True) + '\' AND DateTo <= \'' + ShortDate(NowGMT, True, True) + '\') '
#     strSQL = strSQL + 'OR (DateFrom <= \'' + ShortDate(pEventTime, True, True) + '\' AND DateTo >= \'' + ShortDate(NowGMT, True, True) + '\') '
#     strSQL = strSQL + 'OR (DateFrom <= \'' + ShortDate(pEventTime, True, True) + '\' AND DateTo >= \'' + ShortDate(pEventTime, True, True) + '\' AND DateTo <= \'' + ShortDate(NowGMT, True, True) + '\') '
#     strSQL = strSQL + 'OR (DateFrom >= \'' + ShortDate(pEventTime, True, True) + '\' AND DateFrom <= \'' + ShortDate(NowGMT, True, True) + '\' AND DateTo >= \'' + ShortDate(NowGMT, True, True) + '\') '
#     strSQL = strSQL + ' ) AND YEAR(DateFrom) >= (YEAR(getdate()) - 1) ORDER BY DateFrom'
#     Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
#     Rst.ActiveConnection = None
#     Proportion = fGetRstValLong(GetSingleValue('CalendarEventProportion', 'STblSystemVariables', 'ID=1', 'CN'))
#     while not Rst.EOF:
#         if CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)) >= CDate(ShortDate(pEventTime, False, True)) and CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)) <= CDate(ShortDate(NowGMT, False, True)):
#             CDType = 1
            
#             CEDateDiff = DateDiff('s', CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)), CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)))
            
#         else:
#             if CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)) <= CDate(ShortDate(pEventTime, False, True)) and CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)) >= CDate(ShortDate(NowGMT, False, True)):
#                 CDType = 2
#                 CEDateDiff = pDuration
                
#             else:
#                 if CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)) <= CDate(ShortDate(pEventTime, False, True)) and CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)) <= CDate(ShortDate(NowGMT, False, True)):
#                     CDType = 3
                    
#                     CEDateDiff = DateDiff('s', CDate(ShortDate(pEventTime, False, True)), CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)))
#                 else:
#                     if CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)) >= CDate(ShortDate(pEventTime, False, True)) and CDate(ShortDate(Rst.Fields("DateTo").Value, False, True)) >= CDate(ShortDate(NowGMT, False, True)):
#                         CDType = 4
                        
#                         CEDateDiff = DateDiff('s', CDate(ShortDate(Rst.Fields("DateFrom").Value, False, True)), CDate(ShortDate(NowGMT, False, True)))
#                     else:
#                         CDType = 5
#                         CEDateDiff = 0
#         if CEDateDiff > 0:
#             if pDuration <= CEDateDiff:
#                 if ( ( ( pDuration / CEDateDiff )  * 100 )  >= Proportion )  and  ( ( ( pDuration / CEDateDiff )  * 100 )  > ProportionTemp ) :
#                     ProportionTemp = ( pDuration / CEDateDiff )  * 100
#                     CalendarEventID = fGetRstValLong(Rst.Fields("event").Value)
#                     CalendarEventGroupID = fGetRstValLong(Rst.Fields("EventGroup").Value)
#             else:
#                 if ( ( ( CEDateDiff / pDuration )  * 100 )  >= Proportion )  and  ( ( ( CEDateDiff / pDuration )  * 100 )  > ProportionTemp ) :
#                     ProportionTemp = ( CEDateDiff / pDuration )  * 100
#                     CalendarEventID = fGetRstValLong(Rst.Fields("event").Value)
#                     CalendarEventGroupID = fGetRstValLong(Rst.Fields("EventGroup").Value)
#         Rst.MoveNext()
#     Rst.Close()
#     if ( ProportionTemp >= Proportion )  and  ( ProportionTemp > 0 ) :
#         pEventID = CalendarEventID
#         pEventGroupID = CalendarEventGroupID
#         returnVal = True
#     else:
#         returnVal = False
#     if Err.Number != 0:
#         if InStr(Err.Description, 'nnection') > 0:
#             if CN.State == 1:
#                 CN.Close()
#             CN.Open()
#             if MetaCn.State == 1:
#                 MetaCn.Close()
#             MetaCn.Open()
#             Err.Clear()
            
#         RecordError('MdlServer:fCheckCalendarForCloseEventsOnStart', CStr(Err.Number), Err.Description, 'MachineID = ' + pMachineID)
#         Err.Clear()
#     if Rst.State != 0:
#         returnVal = False
#         Rst.Close()
#     Rst = None
#     return returnVal


