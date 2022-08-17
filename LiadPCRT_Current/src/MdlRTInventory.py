from datetime import datetime

import MdlADOFunctions
import MdlConnection
import MdlGlobal
import mdl_Common
import MdlRTLabels

def CheckBatchAutoSubtract(pBatchAutoSubtractModeOption, pBatchAutoSubtractValue, pMaterialBatch):
    returnVal = None
    
    returnVal = False
    if not pMaterialBatch is None:
        if pBatchAutoSubtractModeOption != off:
            if (pBatchAutoSubtractModeOption == ByMinimumAmount):
                if pMaterialBatch.EffectiveAmount <= pBatchAutoSubtractValue:
                    returnVal = True
            elif (pBatchAutoSubtractModeOption == ByMinimumPercent):
                if pMaterialBatch.OriginalEffectiveAmount > 0:
                    if ( pMaterialBatch.EffectiveAmount / pMaterialBatch.OriginalEffectiveAmount )  * 100 <= pBatchAutoSubtractValue:
                        returnVal = True
    if Err.Number != 0:
        MdlGlobal.RecordError('CheckBatchAutoSubtract', str(0), error.args[0], '')
        Err.Clear()
    return returnVal

def SubtractInventoryItem(pMaterialBatch):
    returnVal = None
    strSQL = ''
    
    if not pMaterialBatch is None:
        strSQL = 'UPDATE TblInventory' + '\n'
        strSQL = strSQL + 'SET' + '\n'
        strSQL = strSQL + 'Amount = 0' + '\n'
        strSQL = strSQL + ',EffectiveAmount = 0' + '\n'
        strSQL = strSQL + ',WareHouseID = 2000' + '\n'
        strSQL = strSQL + ',Status = 2' + '\n'
        strSQL = strSQL + 'WHERE ID = ' + str(pMaterialBatch.ID)
        MdlConnection.CN.execute(strSQL)

    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            Err.Clear()
            
        MdlGlobal.RecordError('SubtractInventoryItem', str(0), error.args[0], 'InventoryID: ' + pMaterialBatch.ID)
        Err.Clear()
    return returnVal

def GetInventoryItemFromGlobalCollection(pCollection, pInventoryID):
    returnVal = None
    tMaterialBatch = None

    try:
        if pCollection.Count > 0:
            if not ( pCollection[str(pInventoryID)] is None ) :
                tMaterialBatch = pCollection[str(pInventoryID)]
                returnVal = tMaterialBatch
            else:
                returnVal = None
        else:
            returnVal = None

    except BaseException as error:
        MdlGlobal.RecordError('GetInventoryItemFromGlobalCollection', str(0), error.args[0], 'InventoryID: ' + str(pInventoryID))
        returnVal = None
    return returnVal

def AddInventoryItemToGlobalCollection(pMaterialBatch):
    returnVal = False
    try:
        if MdlGlobal.gServer.ActiveInventoryItems[str(pMaterialBatch.ID)] is None:
            MdlGlobal.gServer.ActiveInventoryItems[str(pMaterialBatch.ID)] = pMaterialBatch
        returnVal = True

    except BaseException as error:
        MdlGlobal.RecordError('AddInventoryItemToGlobalCollection', str(0), error.args[0], 'InventoryID: ' + str(pMaterialBatch.ID))
    return returnVal



def UpdateJobRecipeFromBatchChange(pJob, pChannelNum, pSplitNum, pMaterialBatch):
    returnVal = None
    strSQL = ''

    tMaterialBatchPropertyID = 0
    
    tMaterialBatchPropertyID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue("ID", "STblMachineTypeProperties", "MachineType = " + pJob.MachineType.ID + " AND PropertyName = N'MaterialBatch'", "CN"))
    strSQL = strSQL + 'SET FValue = \'' + pMaterialBatch.CurrentValue + '\'' + '\n'
    strSQL = strSQL + 'WHERE JobID = ' + pJob.ID + ' AND ChannelNum = ' + pChannelNum + ' AND SplitNum = ' + pSplitNum + ' AND PropertyID = ' + tMaterialBatchPropertyID
    MdlConnection.CN.execute(strSQL)
    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            Err.Clear()
            
        MdlGlobal.RecordError('UpdateJobRecipeFromBatchChange', str(0), error.args[0], 'Job: ' + pJob.ID + '. InventoryID: ' + pMaterialBatch.ID)
        Err.Clear()
    return returnVal

def RemoveBatchFromLocationQueue(pLocationID, pInventoryID):
    returnVal = None
    strSQL = ''
    
    strSQL = 'DELETE FROM TblWareHouseLocationQueue WHERE LocationID = ' + pLocationID + ' AND InventoryID = ' + pInventoryID
    MdlConnection.CN.execute(strSQL)
    strSQL = 'UPDATE TblWareHouseLocationQueue SET Sequence = Sequence - 1 WHERE LocationID = ' + pLocationID
    MdlConnection.CN.execute(strSQL)
    if Err.Number != 0:
        if InStr(Err.Description, 'nnection') > 0:
            if CN.State == 1:
                CN.Close()
            CN.Open()
            if MetaCn.State == 1:
                MetaCn.Close()
            MetaCn.Open()
            Err.Clear()
            
        MdlGlobal.RecordError('RemoveBatchFromLocationQueue', str(0), error.args[0], 'LocationID: ' + pLocationID + '. InventoryID: ' + pInventoryID)
        Err.Clear()
    return returnVal

def AddInventoryHistoryRecord(InventoryID, ActionID, SourceWareHouseID=0, SourceWareHouseLocation='', SourceLocationID=0, pLocationQueueSequence=0, SyncComplete=False):
    returnVal = False
    strSQL = ''
    Rst = None
    AlreadyExist = False

    try:
        strSQL = 'SELECT * FROM TblInventory WHERE ID = ' + InventoryID

        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstData = RstCursor.fetchone()

        if RstData:
            strSQL = 'INSERT INTO TblInventoryHistory'
            strSQL = strSQL + ' ('
            strSQL = strSQL + 'InventoryID,'
            strSQL = strSQL + 'JobID,'
            strSQL = strSQL + 'ShiftID,'
            strSQL = strSQL + 'JoshID,'
            strSQL = strSQL + 'Batch,'
            strSQL = strSQL + 'CatalogID,'
            strSQL = strSQL + 'ProductID,'
            strSQL = strSQL + 'MaterialID,'
            strSQL = strSQL + 'ActionID,'
            if MdlADOFunctions.fGetRstValLong(MdlADOFunctions.SourceWareHouseID) != 0:
                strSQL = strSQL + 'FromWareHouse,'
                strSQL = strSQL + 'FromWareHouseLocation,'
                strSQL = strSQL + 'ToWareHouse,'
                strSQL = strSQL + 'ToWareHouseLocation,'
            strSQL = strSQL + 'Amount,'
            strSQL = strSQL + 'EffectiveAmount,'
            strSQL = strSQL + 'ExecTime,'
            strSQL = strSQL + 'UserID,'
            strSQL = strSQL + 'Status,'
            strSQL = strSQL + 'LocationQueueSequence,'
            strSQL = strSQL + 'ParentInventoryID,'
            strSQL = strSQL + 'SyncComplete'
            strSQL = strSQL + ') '
            strSQL = strSQL + '\n'
            strSQL = strSQL + 'VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + InventoryID + ','
            if RstData.JobID is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + RstData.JobID + ','
            if RstData.ShiftID is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + RstData.ShiftID + ','
            if RstData.JoshID is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + RstData.JoshID + ','
            if RstData.Batch is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + '\'' + RstData.Batch + '\','
            if RstData.CatalogID is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + '\'' + RstData.CatalogID + '\','
            if RstData.ProductID is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + RstData.ProductID + ','
            if RstData.MaterialID is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + RstData.MaterialID + ','
            strSQL = strSQL + ActionID + ','
            if MdlADOFunctions.fGetRstValLong(MdlADOFunctions.SourceWareHouseID) != 0:
                strSQL = strSQL + SourceWareHouseID + ','
                strSQL = strSQL + '\'' + SourceWareHouseLocation + '\','
                strSQL = strSQL + RstData.WareHouseID + ','
                strSQL = strSQL + '\'' + RstData.WareHouseLocation + '\','
            if RstData.Amount is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + RstData.Amount + ','
            if RstData.EffectiveAmount is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + RstData.EffectiveAmount + ','
            strSQL = strSQL + '\'' + datetime.strptime(datetime.now(), 'yyyy-mm-dd HH:nn:ss') + '\','
            strSQL = strSQL + - 1 + ','
            if RstData.Status is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + RstData.Status + ','
            if pLocationQueueSequence == 0:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + pLocationQueueSequence + ','
            if RstData.ParentInventoryID is None:
                strSQL = strSQL + 'NULL,'
            else:
                strSQL = strSQL + str(RstData.ParentInventoryID) + ','
            if SyncComplete:
                strSQL = strSQL + '1'
            else:
                strSQL = strSQL + '0'
            strSQL = strSQL + ' )'
            MdlConnection.CN.execute(strSQL)
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
            
        MdlGlobal.RecordError('AddInventoryHistoryRecord', str(0), error.args[0], 'InventoryID: ' + InventoryID + '. ActionID: ' + ActionID)

    if RstCursor:
        RstCursor.close()
    Rst = None

    return returnVal

def CreateInventoryTrace(InventoryID, JoshID=0):
    returnVal = False 
    strSQL = ''
    Rst = None

    
    if InventoryID != 0:
        if JoshID == 0:
            JoshID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('JoshID', 'TblInventory', 'ID = ' + InventoryID, 'CN'))
        if JoshID != 0:
            
            strSQL = 'DELETE FROM TblInventoryTrace WHERE InventoryID = ' + InventoryID
            MdlConnection.CN.execute(strSQL)
            
            strSQL = ''
            strSQL = 'SELECT DISTINCT InventoryID FROM TblJoshMaterial WHERE InventoryID IS NOT NULL AND JoshEnd IS NOT NULL AND JoshID = ' + JoshID
            Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            Rst.ActiveConnection = None
            while not Rst.EOF:
                if MdlADOFunctions.fGetRstValLong(RstData.InventoryID) != 0:
                    strSQL = ''
                    strSQL = 'INSERT INTO TblInventoryTrace'
                    strSQL = strSQL + ' ('
                    strSQL = strSQL + 'InventoryID'
                    strSQL = strSQL + ', SourceInventoryID'
                    strSQL = strSQL + ') VALUES ('
                    strSQL = strSQL + InventoryID
                    strSQL = strSQL + ', ' + MdlADOFunctions.fGetRstValLong(RstData.InventoryID)
                    strSQL = strSQL + ')'
                    MdlConnection.CN.execute(strSQL)
                Rst.MoveNext()
            RstCursor.close()
        else:
            Err.Raise(1)
    else:
        Err.Raise(1)
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
            
        if InventoryID == 0:
            MdlGlobal.RecordError('CreateInventoryTrace', str(0), error.args[0], ' InventoryID not found!')
        elif JoshID == 0:
            MdlGlobal.RecordError('CreateInventoryTrace', str(0), error.args[0], ' JoshID not found!')
        else:
            MdlGlobal.RecordError('CreateInventoryTrace', str(0), error.args[0], '')
        Err.Clear()
    if Rst.State != 0:
        RstCursor.close()
    Rst = None
    return returnVal


def AddInventoryItemToActivePallet(pInventoryID, pMachine):
    returnVal = False 
    strSQL = ''

    tActivePalletInventoryID = None

    tMachineID = False

    SyncComplete = False

    tIsHomogeneous = False

    OriginCatalogID = ''

    
    tActivePalletInventoryID = pMachine.ActivePalletInventoryID
    tMachineID = pMachine.ID
    tIsHomogeneous = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue("IsHomogeneous", "TblInventory", "ID=" + pInventoryID, "CN"), False)
    if tActivePalletInventoryID != 0:
        if tActivePalletInventoryID != 0:
            strSQL = 'UPDATE TblInventory SET ParentInventoryID = ' + tActivePalletInventoryID + ' WHERE ID = ' + pInventoryID
            if tIsHomogeneous == False:
                MdlConnection.CN.execute(strSQL)
                
                SyncComplete = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('ReportSyncComplete', 'STblInventoryActions', 'ID = 11', 'CN'), False)
                AddInventoryHistoryRecord(pInventoryID, 11, VBGetMissingArgument(AddInventoryHistoryRecord, 2), VBGetMissingArgument(AddInventoryHistoryRecord, 3), VBGetMissingArgument(AddInventoryHistoryRecord, 4), VBGetMissingArgument(AddInventoryHistoryRecord, 5), SyncComplete)
            else:
                OriginCatalogID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CatalogID', 'TblInventory', 'ID=' + pInventoryID, 'CN'))
                TargetCatalogID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CatalogID', 'TblInventory', 'ID=' + tActivePalletInventoryID, 'CN'))
                if OriginCatalogID == TargetCatalogID:
                    MdlConnection.CN.execute(strSQL)
                    
                    SyncComplete = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('ReportSyncComplete', 'STblInventoryActions', 'ID = 11', 'CN'), False)
                    AddInventoryHistoryRecord(pInventoryID, 11, VBGetMissingArgument(AddInventoryHistoryRecord, 2), VBGetMissingArgument(AddInventoryHistoryRecord, 3), VBGetMissingArgument(AddInventoryHistoryRecord, 4), VBGetMissingArgument(AddInventoryHistoryRecord, 5), SyncComplete)
            
            
            
            
    UpdateAmountsByInternalBatchs(tActivePalletInventoryID)
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
            
        MdlGlobal.RecordError('AddInventoryItemToActivePallet', str(0), error.args[0], 'InventoryID = ' + pInventoryID + '. MachineID = ' + tMachineID)
        Err.Clear()
    return returnVal


def CreateActivePalletInventortyItem(pMachine):
    returnVal = False
    strSQL = ''
    Rst = None
    tNumerator = False
    tNumeratorTypeID = 0
    tActiveJobID = 0
    tBatch = ''
    tInventoryBatchOption = None
    tActiveJoshID = False
    tUserID = 0
    tShiftID = 0
    tWareHouseID = 0
    tWareHouseLocation = ''
    tWareHouseLocationID = None
    tActivePalletInventoryID = False
    tCatalogID = ''
    tProductID = None
    tMaterialID = False
    tIsHomogeneous = False
    
    try:
        strSQL = 'SELECT DefaultWareHouse, DefaultWareHouseLocation, DefaultWareHouseLocationID, ActivePalletNumeratorTypeID FROM TblMachines WHERE ID = ' + str(pMachine.ID)
        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstData = RstCursor.fetchone()

        if RstData:
            tWareHouseID = MdlADOFunctions.fGetRstValLong(RstData.DefaultWareHouse)
            tWareHouseLocation = MdlADOFunctions.fGetRstValString(RstData.DefaultWareHouseLocation)
            tWareHouseLocationID = MdlADOFunctions.fGetRstValLong(RstData.DefaultWareHouseLocationID)
            tNumeratorTypeID = MdlADOFunctions.fGetRstValLong(RstData.ActivePalletNumeratorTypeID)
        RstCursor.close()
        
        tUserID = 0
        if not pMachine.ActiveJob is None:
            tActiveJobID = pMachine.ActiveJob.ID
            tActiveJoshID = pMachine.ActiveJob.ActiveJosh.ID
            tShiftID = pMachine.Server.CurrentShiftID
        else:
            pass
        
        tNumerator = MdlRTLabels.RaiseLabelNumerator(0, tActiveJobID, 1, tNumeratorTypeID)
        tInventoryBatchOption = pMachine.Server.SystemVariables.InventoryBatchOption
        tBatch = MdlRTLabels.CreateBatchFormat(tInventoryBatchOption, tActiveJobID, tActiveJoshID, tNumerator, True, 3)
        
        tIsHomogeneous = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('IsHomogeneous', 'TblPackageType', 'ID = 3', 'CN'), True)
        if tIsHomogeneous == True and tActiveJobID != 0:
            strSQL = ''
            strSQL = strSQL + ' SELECT TblJob.ProductID, TblProduct.CatalogID' + '\n'
            strSQL = strSQL + ' FROM TblJob INNER JOIN' + '\n'
            strSQL = strSQL + ' TblProduct ON TblJob.ProductID = TblProduct.ID' + '\n'
            strSQL = strSQL + ' WHERE TblJob.ID = ' + str(tActiveJobID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                tProductID = MdlADOFunctions.fGetRstValLong(RstData.ProductID)
                tCatalogID = MdlADOFunctions.fGetRstValString(RstData.CatalogID)

            RstCursor.close()
            if tCatalogID != '':
                tMaterialID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblMaterial', 'CatalogID = \'' + str(tCatalogID) + '\'', 'CN'))
        
        strSQL = 'INSERT INTO TblInventory'
        strSQL = strSQL + '('
        strSQL = strSQL + 'PackageTypeID'
        strSQL = strSQL + ',PackageBatchNum'
        strSQL = strSQL + ',Batch'
        strSQL = strSQL + ',UserID'
        strSQL = strSQL + ',ShiftID'
        strSQL = strSQL + ',Amount'
        strSQL = strSQL + ',OriginalAmount'
        strSQL = strSQL + ',EffectiveAmount'
        strSQL = strSQL + ',EffectiveOriginalAmount'
        strSQL = strSQL + ',LastEffectiveAmount'
        strSQL = strSQL + ',Date'
        strSQL = strSQL + ',LastUpdate'
        strSQL = strSQL + ',Status'
        strSQL = strSQL + ',WareHouseID'
        strSQL = strSQL + ',WareHouseLocation'
        strSQL = strSQL + ',WareHouseLocationID'
        strSQL = strSQL + ',JobID'
        strSQL = strSQL + ',JoshID'
        if tProductID != 0:
            strSQL = strSQL + ',ProductID'
        if tMaterialID != 0:
            strSQL = strSQL + ',MaterialID'
        if tCatalogID != '':
            strSQL = strSQL + ',CatalogID'
        strSQL = strSQL + ')'
        strSQL = strSQL + ' VALUES ' + '\n'
        strSQL = strSQL + '('
        strSQL = strSQL + '3'
        strSQL = strSQL + ', ' + str(tNumerator)
        strSQL = strSQL + ', \'' + str(tBatch) + '\''
        strSQL = strSQL + ', ' + str(tUserID)
        strSQL = strSQL + ', ' + str(tShiftID)
        strSQL = strSQL + ',1'
        strSQL = strSQL + ',1'
        strSQL = strSQL + ',0'
        strSQL = strSQL + ',0'
        strSQL = strSQL + ',0'
        strSQL = strSQL + ', \'' + datetime.strptime(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn:ss') + '\''
        strSQL = strSQL + ', \'' + datetime.strptime(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn:ss') + '\''
        strSQL = strSQL + ',1'
        strSQL = strSQL + ',' + str(tWareHouseID)
        strSQL = strSQL + ', \'' + str(tWareHouseLocation) + '\''
        strSQL = strSQL + ',' + str(tWareHouseLocationID)
        strSQL = strSQL + ',' + str(tActiveJobID)
        strSQL = strSQL + ',' + str(tActiveJoshID)
        if tProductID != 0:
            strSQL = strSQL + ',' + str(tProductID)
        if tMaterialID != 0:
            strSQL = strSQL + ',' + str(tMaterialID)
        if tCatalogID != '':
            strSQL = strSQL + ', \'' + str(tCatalogID) + '\''
        strSQL = strSQL + ')'

        MdlConnection.CN.execute(strSQL)
        tActivePalletInventoryID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblInventory', 'PackageTypeID = 3 AND UserID = ' + str(tUserID) + ' ORDER BY ID DESC', 'CN'))
        strSQL = 'UPDATE TblMachines SET ActivePalletInventoryID = ' + str(tActivePalletInventoryID) + ' WHERE ID = ' + str(pMachine.ID)
        MdlConnection.CN.execute(strSQL)
        pMachine.ActivePalletInventoryID = tActivePalletInventoryID
        
        AddInventoryHistoryRecord(tActivePalletInventoryID, 12)
        returnVal = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('CreateActivePalletInventortyItem', str(0), error.args[0], 'MachineID = ' + str(pMachine.ID))

    Rst = None
    return returnVal


def CloseActivePalletInventoryItem(pMachine):
    returnVal = False
    tActivePalletInventoryID = 0
    strSQL = ''
    RstCursor = None
    tTotalWeight = False
    tTotalEffectiveAmount = 0.0
    
    try:
        tActivePalletInventoryID = pMachine.ActivePalletInventoryID
        strSQL = 'UPDATE TblInventory SET LastUpdate = \'' + datetime.strptime(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn:ss') + '\' WHERE ID = ' + str(tActivePalletInventoryID)
        MdlConnection.CN.execute(strSQL)
        strSQL = 'UPDATE TblMachines SET ActivePalletInventoryID = 0 WHERE ID = ' + str(pMachine.ID)
        MdlConnection.CN.execute(strSQL)
        pMachine.ActivePalletInventoryID = 0
        
        strSQL = ''
        strSQL = 'SELECT SUM(Weight) as TotalWeight, SUM(EffectiveAmount) as TotalEffectiveAmount FROM TblInventory WHERE ParentInventoryID = ' + str(tActivePalletInventoryID)

        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstData = RstCursor.fetchone()

        if RstData:
            tTotalWeight = MdlADOFunctions.fGetRstValDouble(RstData.TotalWeight)
            tTotalEffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.TotalEffectiveAmount)

        RstCursor.close()
        strSQL = ''
        strSQL = strSQL + ' UPDATE TblInventory'
        strSQL = strSQL + ' SET'
        strSQL = strSQL + ' EffectiveAmount = ' + str(tTotalEffectiveAmount)
        strSQL = strSQL + ' , EffectiveOriginalAmount = ' + str(tTotalEffectiveAmount)
        strSQL = strSQL + ' , Weight = ' + str(tTotalWeight)
        strSQL = strSQL + ' WHERE ID = ' + str(tActivePalletInventoryID)
        MdlConnection.CN.execute(strSQL)
        
        AddInventoryHistoryRecord(tActivePalletInventoryID, 13)
        returnVal = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
        MdlGlobal.RecordError('CloseActivePalletInventoryItem', str(0), error.args[0], 'MachineID = ' + str(pMachine.ID))
    return returnVal

def UpdateAmountsByInternalBatchs(pInventoryID):
    returnVal = None
    strSQL = ''

    Rst = None

    tTotalWeight = False

    tTotalEffectiveAmount = 0.0
    
    returnVal = False
    strSQL = ''
    strSQL = 'SELECT SUM(Weight) as TotalWeight, SUM(EffectiveAmount) as TotalEffectiveAmount FROM TblInventory WHERE ParentInventoryID = ' + pInventoryID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    if RstData:
        tTotalWeight = MdlADOFunctions.fGetRstValDouble(RstData.TotalWeight)
        tTotalEffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.TotalEffectiveAmount)
    RstCursor.close()
    strSQL = ''
    strSQL = strSQL + ' UPDATE TblInventory'
    strSQL = strSQL + ' SET'
    strSQL = strSQL + ' EffectiveAmount = ' + tTotalEffectiveAmount
    strSQL = strSQL + ' , Weight = ' + tTotalWeight
    strSQL = strSQL + ' WHERE ID = ' + pInventoryID
    MdlConnection.CN.execute(strSQL)
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
        RstCursor.close()
    Rst = None
    return returnVal



def UpdatePalletForToolInventory(ValueDiff, pMachine):
    returnVal = False 
    LocationID = 0

    Location = ''

    InventoryID = None

    strSQL = False

    Rst = None
    
    Location = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('DefaultWareHouseLocation', 'TblMachines', ' ID = ' + str(pMachine.ID), 'CN'))
    LocationID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblWareHouseLocations', ' LocalID = \'' + Location + '\'', 'CN'))
    while ValueDiff > 0:
        strSQL = 'SELECT InventoryID FROM TblWareHouseLocationQueue WHERE LocationID = ' + LocationID + ' order by Sequence'
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        InventoryID = RstData.InventoryID
        RstCursor.close()
        UpdatePalletInventoryItem(InventoryID, pMachine)
        RemoveBatchFromLocationQueue(LocationID, InventoryID)
        ValueDiff = ValueDiff - 1
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
            
    return returnVal


def UpdatePalletInventoryItem(InventoryID, pMachine):
    returnVal = None
    strSQL = ''

    Rst = None

    tNumerator = False

    tNumeratorTypeID = 0

    tActiveJobID = 0

    tBatch = ''

    tInventoryBatchOption = None

    tActiveJoshID = False

    tUserID = 0

    tShiftID = 0

    tWareHouseID = 0

    tWareHouseLocation = ''

    tWareHouseLocationID = None

    tActivePalletInventoryID = False

    tDate = ''

    
    strSQL = 'SELECT Date,LastUpdate FROM TblInventory WHERE  ID = ' + InventoryID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    tDate = RstData.Date
    tLastUpdate = RstData.LastUpdate
    RstCursor.close()
    if tDate == '' or tLastUpdate == '':
        
        strSQL = 'SELECT DefaultWareHouse, DefaultWareHouseLocation, DefaultWareHouseLocationID, ActivePalletNumeratorTypeID FROM TblMachines WHERE ID = ' + str(pMachine.ID)
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        if Rst.RecordCount == 1:
            tWareHouseID = MdlADOFunctions.fGetRstValLong(RstData.DefaultWareHouse)
            tWareHouseLocation = MdlADOFunctions.fGetRstValString(RstData.DefaultWareHouseLocation)
            tWareHouseLocationID = MdlADOFunctions.fGetRstValLong(RstData.DefaultWareHouseLocationID)
            tNumeratorTypeID = MdlADOFunctions.fGetRstValLong(RstData.ActivePalletNumeratorTypeID)
        RstCursor.close()
        
        tUserID = 0
        if not pMachine.ActiveJob is None:
            tActiveJobID = pMachine.ActiveJob.ID
            tActiveJoshID = pMachine.ActiveJob.ActiveJosh.ID
            tShiftID = pMachine.Server.CurrentShiftID
        else:
            
            pass
        
        tNumerator = MdlRTLabels.RaiseLabelNumerator(0, tActiveJobID, 1, tNumeratorTypeID)
        
        tInventoryBatchOption = pMachine.Server.SystemVariables.InventoryBatchOption
        tBatch = CreateBatchdatetime.strptime(tInventoryBatchOption, tActiveJobID, tActiveJoshID, tNumerator, True, 3)
        
        strSQL = 'UPDATE TblInventory SET'
        
        strSQL = strSQL + 'PackageBatchNum = ' + tNumerator
        strSQL = strSQL + ',Batch = \'' + tBatch + '\''
        strSQL = strSQL + ',UserID = ' + tUserID
        strSQL = strSQL + ',ShiftID = ' + tShiftID
        strSQL = strSQL + ',Amount = 1'
        strSQL = strSQL + ',OriginalAmount = 1'
        strSQL = strSQL + ',EffectiveAmount = 0'
        strSQL = strSQL + ',EffectiveOriginalAmount = 0'
        strSQL = strSQL + ',LastEffectiveAmount = 0'
        strSQL = strSQL + ',Date = \'' + datetime.strptime(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn:ss') + '\''
        strSQL = strSQL + ',LastUpdate = \'' + datetime.strptime(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn:ss') + '\''
        strSQL = strSQL + ',Status = 1'
        
        strSQL = strSQL + ',WareHouseLocation = \'' + tWareHouseLocation + '\''
        
        strSQL = strSQL + ',JobID = ' + tActiveJobID
        strSQL = strSQL + ',JoshID = ' + tActiveJoshID
        strSQL = strSQL + 'WHERE InventoryID = ' + InventoryID
        MdlConnection.CN.execute(strSQL)
        tActivePalletInventoryID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblInventory', 'PackageTypeID = 3 AND UserID = ' + tUserID + ' ORDER BY ID DESC', 'CN'))
    else:
        tActivePalletInventoryID = InventoryID
    strSQL = 'UPDATE TblMachines SET ActivePalletInventoryID = ' + tActivePalletInventoryID + ' WHERE ID = ' + str(pMachine.ID)
    MdlConnection.CN.execute(strSQL)
    pMachine.ActivePalletInventoryID = tActivePalletInventoryID
    
    AddInventoryHistoryRecord(tActivePalletInventoryID, 12)
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
            
        MdlGlobal.RecordError('UpdatePalletInventoryItem', str(0), error.args[0], 'MachineID = ' + str(pMachine.ID))
        Err.Clear()
    if Rst.State != 0:
        RstCursor.close()
    Rst = None
    return returnVal

def AddInventoryItemToLocationQueue(InventoryID, LocationID, pAddAsActiveBatch=False, pAddAsFirstInQueue=False):
    returnVal = None
    ConsumptionMethod = 0

    MinSequence = 0

    MaxSequence = 0

    ActiveBatch = False

    RecordDeleted = False

    strSQL = ''

    Rst = None

    ArrFields = []

    ArrVals = []

    tRecordsDeleted = {}

    tRecordsChanged = {}

    tRecordsChangeDetails = {}

    tSequence = 0

    tMaximumItemsOnQueue = 0

    tTotalItemsInQueue = 0
    
    
    
    
    returnVal = False
    if InventoryID != 0:
        
        strSQL = 'SELECT Count(ID) AS CountID, MIN(Sequence) AS MinSeq, MAX(Sequence) AS MaxSeq FROM TblWareHouseLocationQueue ' + 'WHERE LocationID = ' + LocationID + 'GROUP BY LocationID'
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        if Rst.RecordCount == 1:
            if MdlADOFunctions.fGetRstValLong(RstData.CountID) == 0:
                ActiveBatch = True
            MinSequence = MdlADOFunctions.fGetRstValLong(RstData.MinSeq)
            MaxSequence = MdlADOFunctions.fGetRstValLong(RstData.MaxSeq)
            tTotalItemsInQueue = MdlADOFunctions.fGetRstValLong(RstData.CountID)
        RstCursor.close()
        tMaximumItemsOnQueue = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MaximumItemsOnQueue', 'TblWareHouseLocations', 'ID = ' + LocationID))
        if not pAddAsActiveBatch and not pAddAsFirstInQueue and tMaximumItemsOnQueue > 0:
            if tTotalItemsInQueue > tMaximumItemsOnQueue:
                
                Err.Raise(251)
                return returnVal
        if not CheckIfInventoryItemIsOnLocation(InventoryID, LocationID, True):
            Err.Raise(250)
        ConsumptionMethod = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ConsumptionMethodID', 'TblWareHouseLocations', 'ID = ' + LocationID, 'CN'))
        if (ConsumptionMethod == 1):
            if pAddAsActiveBatch:
                tSequence = 1
            else:
                tSequence = MaxSequence + 1
            if pAddAsFirstInQueue:
                tSequence = 2
            else:
                tSequence = MaxSequence + 1
                        
            InsertOrUpdateInventoryItemToLocationQueue(- 1, LocationID, InventoryID, tSequence)
        elif (ConsumptionMethod == 2):
            
            MinSequence = fCheckSequenceOnLoctionQueue(LocationID, MinSequence)
            if pAddAsActiveBatch:
                tSequence = 1
            else:
                tSequence = MinSequence + 1
            if pAddAsFirstInQueue:
                tSequence = 2
            else:
                tSequence = MinSequence + 1
            
            InsertOrUpdateInventoryItemToLocationQueue(- 1, LocationID, InventoryID, tSequence)
    ReOrderInventoryItemsOnWareHouseLocation(LocationID)
    LogInventoryItemAdditionToLocation(InventoryID, tSequence, LocationID)
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
            
        MdlGlobal.RecordError('AddInventoryItemToLocationQueue', str(0), error.args[0], 'LocationID = ' + LocationID)
        Err.Clear()
    tRecordsChanged = None
    tRecordsDeleted = None
    if Rst.State != 0:
        RstCursor.close()
    Rst = None
    return returnVal


def LogInventoryItemAdditionToLocation(pInventoryID, pSequence, pLocationID):
    returnVal = None
    
    returnVal = False
    AddInventoryHistoryRecord(pInventoryID, 8, VBGetMissingArgument(AddInventoryHistoryRecord, 2), VBGetMissingArgument(AddInventoryHistoryRecord, 3), VBGetMissingArgument(AddInventoryHistoryRecord, 4), str(pSequence))
    returnVal = True
    if Err.Number != 0:
        Err.Clear()
    return returnVal

def fCheckSequenceOnLoctionQueue(LocationID, MinSeq):
    returnVal = None
    ActiveMaterialIVID = 0

    ActiveMaterialParentIVID = 0

    ActiveMaterialToolID = 0

    InventoryID = 0

    ParentInventoryID = 0

    ToolID = 0

    Seq = 0

    strSQL = ''

    RstQueue = None

    ByTool = False

    ByParent = False
    
    
    ByTool = False
    ByParent = False
    ActiveMaterialIVID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('InventoryID', 'TblWareHouseLocationQueue', ' LocationID = ' + LocationID, 'CN'))
    if ActiveMaterialIVID != 0:
        ActiveMaterialParentIVID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ParentInventoryID', 'TblInventory', ' ID = ' + ActiveMaterialIVID, 'CN'))
        if ActiveMaterialParentIVID != 0:
            ActiveMaterialToolID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ToolID', 'TblInventory', ' ID = ' + ActiveMaterialParentIVID, 'CN'))
            if ActiveMaterialToolID != 0:
                ByTool = True
            else:
                ByParent = True
    strSQL = ' SELECT InventoryID,Sequence FROM TblWareHouseLocationQueue WHERE LocationID = ' + LocationID + ' ORDER BY Sequence'
    RstQueue.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    RstQueue.ActiveConnection = None
    if ActiveMaterialIVID != 0 and  ( ByTool or ByParent ) :
        while not RstQueue.EOF:
            InventoryID = RstQueue.Fields("InventoryID").Value
            Seq = RstQueue.Fields("Sequence").Value
            ParentInventoryID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ParentInventoryID', 'TblInventory', ' ID = ' + InventoryID, 'CN'))
            ToolID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ToolID', 'TblInventory', ' ID = ' + ParentInventoryID, 'CN'))
            if ByTool:
                if ToolID != ActiveMaterialToolID:
                    MinSeq = Seq - 1
                    returnVal = MinSeq
                    return returnVal
            elif ByParent:
                if ParentInventoryID != ActiveMaterialParentIVID:
                    MinSeq = Seq - 1
                    returnVal = MinSeq
                    return returnVal
            RstQueue.MoveNext()
    returnVal = MinSeq
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
    if RstQueue.State != 0:
        RstQueue.Close()
    RstQueue = None
    return returnVal

def CheckIfInventoryItemIsOnLocation(pInventoryID, pLocationID, pPerformInventoryTransfer):
    returnVal = False 
    tLocationWareHouseID = 0

    tItemWareHouseID = 0

    tItemLocationID = 0

    strSQL = ''

    Rst = None
    
    tLocationWareHouseID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('WareHouseID', 'TblWareHouseLocations', 'ID = ' + pLocationID, 'CN'))
    strSQL = 'SELECT WareHouseID, WareHouseLocationID FROM TblInventory WHERE ID = ' + pInventoryID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    if Rst.RecordCount == 1:
        tItemWareHouseID = MdlADOFunctions.fGetRstValLong(RstData.WareHouseID)
        tItemLocationID = MdlADOFunctions.fGetRstValLong(RstData.WareHouseLocationID)
    RstCursor.close()
    if not ( tItemWareHouseID == tLocationWareHouseID and tItemLocationID == pLocationID ) :
        if not pPerformInventoryTransfer:
            returnVal = False
        else:
            if fTransferInventoryItem(pInventoryID, tLocationWareHouseID, VBGetMissingArgument(fTransferInventoryItem, 2), pLocationID):
                returnVal = True
    else:
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

def fTransferInventoryItem(InventoryID, TargetWareHouseID, TargetWareHouseLocation='', TargetLocationID=0, SourceLocationID=0, SourceWareHouseID=0):
    returnVal = False 
    strSQL = ''

    RstBatchs = None
    
    if fCheckWareHouseValidation(3, TargetWareHouseID, InventoryID, TargetLocationID) == True:
        strSQL = 'SELECT ID FROM TblInventory WHERE ParentInventoryID = ' + InventoryID
        RstBatchs.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        RstBatchs.ActiveConnection = None
        while not RstBatchs.EOF:
            if fTransferInventoryItem(RstBatchs.Fields("ID").Value, TargetWareHouseID, TargetWareHouseLocation, TargetLocationID) == False:
                Err.Raise(1)
            RstBatchs.MoveNext()
        RstBatchs.Close()
        strSQL = 'UPDATE TblInventory SET WareHouseID = ' + TargetWareHouseID + ' , WareHouseLocation = \'' + TargetWareHouseLocation + '\', WareHouseLocationID = ' + TargetLocationID + ' WHERE ID = ' + InventoryID
        MdlConnection.CN.execute(strSQL)
        AddInventoryHistoryRecord(InventoryID, 3, SourceWareHouseID, TargetWareHouseLocation, SourceLocationID)
        strSQL = 'DELETE FROM TblWareHouseLocationQueue WHERE LocationID <> ' + TargetLocationID + ' AND InventoryID = ' + InventoryID
        MdlConnection.CN.execute(strSQL)
    else:
        Err.Raise(1)
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
            
        MdlGlobal.RecordError('fTransferInventoryItem', str(0), error.args[0], ' - InventoryID=' + InventoryID + ' :TargetWareHouse=' + TargetWareHouseID, 'LeaderWeb')
        Err.Clear()
    RstBatchs = None
    return returnVal

def fCheckWareHouseValidation(ActionID, WareHouseID=0, IVID=0, LocationID=0):
    returnVal = False
    vRst = None
    oRst = None
    strSQL = ''
    FieldName = ''
    RefFieldName = ''
    ObjectTableName = ''
    RefObjectTableName = ''
    ComparerTypeChar = ''
    ValidErrNum = 0
    ConstantValue = ''
    InventoryObjectID = ''
    ObjectField = ''
    ObjectID = 0
    CheckStatus = False


    CheckStatus = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('CheckStatus', 'TblWareHouseLocations', ' ID = ' + LocationID, 'CN'), False)
    ValidErrNum = 0
    strSQL = 'SELECT * FROM TblWareHouseValidations '
    strSQL = strSQL + ' WHERE ActionID = ' + ActionID
    if WareHouseID != 0:
        strSQL = strSQL + ' AND WareHouseID = ' + WareHouseID
    if LocationID != 0:
        strSQL = strSQL + ' AND  WareHouseLocationID = ' + LocationID
    vRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    vRst.ActiveConnection = None
    while not vRst.EOF:
        ObjectTableName = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('TableName', 'STblWareHouseValidationObjects', 'ID = ' + vRst.Fields("ObjectTypeID").Value, 'CN'))
        ComparerTypeChar = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CompSign', 'STblComparerTypes', 'ID = ' + vRst.Fields("ComparerTypeID").Value, 'CN'))
        FieldName = MdlADOFunctions.fGetRstValString(vRst.Fields("FieldName").Value)
        ConstantValue = MdlADOFunctions.fGetRstValString(vRst.Fields("RefConstantValue").Value)
        if ConstantValue == '':
            RefObjectTableName = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('TableName', 'STblWareHouseValidationObjects', 'ID = ' + vRst.Fields("RefObjectTypeID").Value, 'CN'))
            RefFieldName = MdlADOFunctions.fGetRstValString(vRst.Fields("RefFieldName").Value)
            if (RefObjectTableName == 'TblJob'):
                ObjectField = 'JobID'
            elif (RefObjectTableName == 'TblProduct'):
                ObjectField = 'ProductID'
            elif (RefObjectTableName == 'TblJosh'):
                ObjectField = 'JoshID'
            else:
                ObjectField = 'ID'
            ObjectID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue(ObjectField, 'TblInventory', 'ID = ' + IVID, 'CN'))
            ConstantValue = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue(RefFieldName, RefObjectTableName, 'ID = ' + ObjectID, 'CN'))
        
        if ( FieldName == 'Status' and CheckStatus == True )  or  ( FieldName != 'Status' ) :
            if ( ObjectTableName != '' )  and  ( ComparerTypeChar != '' )  and  ( FieldName != '' ) :
                if ObjectField == '':
                    ObjectField = 'ID'
                strSQL = 'SELECT * FROM TblInventory'
                strSQL = strSQL + ' WHERE ' + ObjectField + ' = ' + IVID
                strSQL = strSQL + ' AND ' + FieldName + ' ' + ComparerTypeChar + ' \'' + ConstantValue + '\''
                oRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                oRst.ActiveConnection = None
                if oRst.RecordCount == 0:
                    ValidErrNum = ValidErrNum + 1
                oRst.Close()
        vRst.MoveNext()
    vRst.Close()
    if ValidErrNum == 0:
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
            
        Err.Clear()
    vRst = None
    oRst = None
    return returnVal

def InsertOrUpdateInventoryItemToLocationQueue(pUserID, pLocationID, pInventoryID, pSequence):
    strSQL = ''

    tInsertRecord = None

    Rst = None
    
    strSQL = 'SELECT ID FROM TblWareHouseLocationQueue WHERE LocationID = ' + pLocationID + ' AND InventoryID = ' + pInventoryID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    if Rst.RecordCount == 0:
        tInsertRecord = True
    RstCursor.close()
    if tInsertRecord:
        strSQL = 'INSERT INTO TblWareHouseLocationQueue ' + '(LastUpdateUserID, LocationID, InventoryID, Sequence) ' + 'VALUES (' + pUserID + ', ' + pLocationID + ', ' + pInventoryID + ', ' + pSequence + ')'
    else:
        strSQL = 'UPDATE TblWareHouseLocationQueue ' + 'SET Sequence = ' + pSequence + ' ' + 'WHERE LocationID = ' + pLocationID + ' AND InventoryID = ' + pInventoryID
    MdlConnection.CN.execute(strSQL)
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

def ReOrderInventoryItemsOnWareHouseLocation(LocationID):
    strSQL = ''
    returnVal = False
    ItemsCount = 0
    Rst = None    
    
    strSQL = strSQL + ' SELECT ID FROM ViewTblWareHouseLocationQueue'
    strSQL = strSQL + ' WHERE Batch IN (SELECT DISTINCT MaterialBatch FROM TblJoshMaterial WHERE MaterialBatch <> \'\' AND JoshEnd <> \'\') AND LocationID = ' + LocationID
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    if RstData:
        strSQL = 'UPDATE TblWareHouseLocationQueue SET Sequence = 1 WHERE ID = ' + RstData.ID
        MdlConnection.CN.execute(strSQL)
        strSQL = 'UPDATE TblWareHouseLocationQueue SET Sequence = 2 WHERE Sequence IN(0,1) AND LocationID = ' + LocationID + ' AND ID <> ' + RstData.ID
        MdlConnection.CN.execute(strSQL)
    RstCursor.close()
    strSQL = 'SELECT ID FROM TblWareHouseLocationQueue WHERE LocationID = ' + LocationID + ' ORDER BY Sequence, ID DESC'
    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
    Rst.ActiveConnection = None
    while not Rst.EOF:
        ItemsCount = ItemsCount + 1
        strSQL = 'UPDATE TblWareHouseLocationQueue SET Sequence = ' + ItemsCount + ' WHERE ID = ' + RstData.ID
        MdlConnection.CN.execute(strSQL)
        Rst.MoveNext()
    RstCursor.close()
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
        RstCursor.close()
    Rst = None
    return returnVal


