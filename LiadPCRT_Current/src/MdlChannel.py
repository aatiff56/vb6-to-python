import MdlChannelSplit
import MdlConnection
import MdlADOFunctions
import MdlGlobal
from ClassModules.Channel import MaterialCalcObjectType


def GetChannelControllerFieldName(ChannelNum, NameType):
    result = ""
    if (NameType == MdlChannelSplit.ControllerFieldNameType.MaterialPC):
        result = 'Cnl' + ChannelNum + 'MaterialPC'
    elif (NameType == MdlChannelSplit.ControllerFieldNameType.MaterialPCTarget):
        result = 'Cnl' + ChannelNum + 'MaterialPCTarget'
    elif (NameType == MdlChannelSplit.ControllerFieldNameType.TotalWeight):
        result = 'Cnl' + ChannelNum + 'TotalWeight'
    elif (NameType == MdlChannelSplit.ControllerFieldNameType.TotalWeightLast):
        result = 'Cnl' + ChannelNum + 'TotalWeightLast'
    elif (NameType == MdlChannelSplit.ControllerFieldNameType.ChannelStatus):
        result = 'Cnl' + ChannelNum + 'Status'
    elif (NameType == MdlChannelSplit.ControllerFieldNameType.MaterialID):
        result = 'Cnl' + ChannelNum + 'MaterialID'
    return result


def GetChannelTotalWeight(pJobID, pJoshID, pTotalWeight, pChannelNum, pMaterialID, pMaterialBatch=''):
    strSQL = ""
    dbCursor = None

    try:
        if pJoshID != 0:
            strSQL = 'SELECT Amount, MaterialFlowAmount FROM TblJobMaterial WHERE Job = ' + pJobID
            strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
            strSQL = strSQL + ' AND SplitNum = 0'
            strSQL = strSQL + ' AND Material = ' + pMaterialID
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND MaterialBatch = \'' + pMaterialBatch + '\''
            
            dbCursor = MdlConnection.CN.cursor()
            dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                pTotalWeight.SetCurrentValue(MaterialCalcObjectType.FromJob, MdlADOFunctions.fGetRstValDouble(val["Amount"]))
                pTotalWeight.SetMaterialFlowAmount(MaterialCalcObjectType.FromJob, MdlADOFunctions.fGetRstValDouble(val["MaterialFlowAmount"]))
        
            if dbCursor:
                dbCursor.close()
            
            strSQL = 'SELECT SUM(MaterialActualIndex) AS MaterialActualIndex, '
            strSQL = strSQL + 'SUM(Amount) AS Amount, '
            strSQL = strSQL + 'SUM(AmountStandard) AS AmountStandard'
            strSQL = strSQL + ' FROM TblJobMaterial WHERE Job = ' + pJobID
            strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
            strSQL = strSQL + ' AND SplitNum = 0'
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND (Material <> ' + pMaterialID + ' OR (Material = ' + pMaterialID + ' AND MaterialBatch <> \'' + pMaterialBatch + '\'))'
            else:
                strSQL = strSQL + ' AND Material <> ' + pMaterialID

            dbCursor = MdlConnection.CN.cursor()
            dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                pTotalWeight.SetOtherMaterialsActualIndex(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(val["MaterialActualIndex"]), 5))
                pTotalWeight.SetOtherMaterialsAmount(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(val["Amount"]), 5))
                pTotalWeight.SetOtherMaterialsAmountStandard(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(val["AmountStandard"]), 5))
        
            if dbCursor:
                dbCursor.close()
            GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pMaterialID, pMaterialBatch)
        
        else:   
            strSQL = 'SELECT SUM(Amount) AS Amount, SUM(MaterialFlowAmount) AS MaterialFlowAmount FROM TblJoshMaterial WHERE JobID = ' + pJobID
            strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
            strSQL = strSQL + ' AND SplitNum = 0'
            strSQL = strSQL + ' AND Material = ' + pMaterialID
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND MaterialBatch = \'' + pMaterialBatch + '\''
            dbCursor = MdlConnection.CN.cursor()
            
            dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                pTotalWeight.SetCurrentValue(MaterialCalcObjectType.FromJob, MdlADOFunctions.fGetRstValDouble(val["Amount"]))
                pTotalWeight.SetMaterialFlowAmount(MaterialCalcObjectType.FromJob, MdlADOFunctions.fGetRstValDouble(val["MaterialFlowAmount"]))
        
            if dbCursor:
                dbCursor.close()
            
            strSQL = 'SELECT SUM(MaterialActualIndex) AS MaterialActualIndex, '
            strSQL = strSQL + ' SUM(Amount) AS Amount, '
            strSQL = strSQL + ' SUM(AmountStandard) AS AmountStandard '
            strSQL = strSQL + ' FROM TblJoshMaterial WHERE JobID = ' + pJobID
            strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
            strSQL = strSQL + ' AND SplitNum = 0'
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND (Material <> ' + pMaterialID + ' OR (Material = ' + pMaterialID + ' AND MaterialBatch <> \'' + pMaterialBatch + '\'))'
            else:
                strSQL = strSQL + ' AND Material <> ' + pMaterialID
            dbCursor = MdlConnection.CN.cursor()
            
            dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                pTotalWeight.SetOtherMaterialsActualIndex(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(val["MaterialActualIndex"]), 5))
                pTotalWeight.SetOtherMaterialsAmount(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(val["Amount"]), 5))
                pTotalWeight.SetOtherMaterialsAmountStandard(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(val["AmountStandard"]), 5))
        
            if dbCursor:
                dbCursor.close()
            
            
            if pTotalWeight.Parent.Job.Status == 10:
                pJoshID = pTotalWeight.Parent.Job.ActiveJosh.ID
                GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pMaterialID, pMaterialBatch)
                

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('GetChannelTotalWeight', 0, error.args[0], 'JobID: ' + pJobID + '. JoshID: ' + pJoshID + '. ChannelNum: ' + pChannelNum)

    if dbCursor:
        dbCursor.close()
    dbCursor = None


def GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pMaterialID, pMaterialBatch=''):
    strSQL = 'SELECT Amount,AmountStandard,MaterialFlowAmount FROM TblJoshMaterial WHERE JoshID = ' + pJoshID
    strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
    strSQL = strSQL + ' AND SplitNum = 0'
    strSQL = strSQL + ' AND Material = ' + pMaterialID
    if pMaterialBatch != '':
        strSQL = strSQL + ' AND MaterialBatch = \'' + pMaterialBatch + '\''
    dbCursor = MdlConnection.CN.cursor()
    
    dbCursor.execute(strSQL)
    val = dbCursor.fetchone()
    if val:
        pTotalWeight.SetCurrentValue(MaterialCalcObjectType.FromJosh, MdlADOFunctions.fGetRstValDouble(val["Amount"]))
        pTotalWeight.SetStandardValue(MaterialCalcObjectType.FromJosh, MdlADOFunctions.fGetRstValDouble(val["AmountStandard"]))
        pTotalWeight.SetMaterialFlowAmount(MaterialCalcObjectType.FromJosh, MdlADOFunctions.fGetRstValDouble(val["MaterialFlowAmount"]))

    if dbCursor:
        dbCursor.close()
    
    strSQL = 'SELECT SUM(MaterialActualIndex) as MaterialActualIndex, '
    strSQL = strSQL + ' SUM(Amount) AS Amount, '
    strSQL = strSQL + ' SUM(AmountStandard) AS AmountStandard '
    strSQL = strSQL + ' FROM TblJoshMaterial WHERE JoshID = ' + pJoshID
    strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
    strSQL = strSQL + ' AND SplitNum = 0'
    if pMaterialBatch != '':
        strSQL = strSQL + ' AND (Material <> ' + pMaterialID + ' OR (Material = ' + pMaterialID + ' AND MaterialBatch <> \'' + pMaterialBatch + '\'))'
    else:
        strSQL = strSQL + ' AND Material <> ' + pMaterialID
    dbCursor = MdlConnection.CN.cursor()
    
    dbCursor.execute(strSQL)
    val = dbCursor.fetchone()
    if val:
        pTotalWeight.SetOtherMaterialsActualIndex(MaterialCalcObjectType.FromJosh, round(MdlADOFunctions.fGetRstValDouble(val["MaterialActualIndex"]), 5))
        pTotalWeight.SetOtherMaterialsAmount(MaterialCalcObjectType.FromJosh, round(MdlADOFunctions.fGetRstValDouble(val["Amount"]), 5))
        pTotalWeight.SetOtherMaterialsAmountStandard(MaterialCalcObjectType.FromJosh, round(MdlADOFunctions.fGetRstValDouble(val["AmountStandard"]), 5))

    if dbCursor:
        dbCursor.close()


def GetChannelForecastWeight(pJobID, pForecastWeight, pChannelNum):
    tProductWeight = 0
    tUnitsTarget = 0
    tMaterialPCTarget = 0
    tCavitiesActual = 0
    tJobAmount = 0
    tJobAmountLeft = 0
        
    try:
        tProductWeight = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(pJobID, 'ProductWeight', 0, 0))
        tUnitsTarget = pForecastWeight.Parent.Job.UnitsTarget
        tCavitiesActual = pForecastWeight.Parent.Job.CavitiesActual
        tMaterialPCTarget = pForecastWeight.Parent.MaterialPCTarget.CurrentValue
        if pChannelNum != 100:
            tJobAmount = round(( tUnitsTarget / tCavitiesActual )  *  ( tProductWeight / 1000 )  *  ( tMaterialPCTarget / 100 ), 5)
        else:
            tJobAmount = round(( tUnitsTarget / tCavitiesActual )  *  ( tMaterialPCTarget ), 5)
        tJobAmountLeft = round(tJobAmount - pForecastWeight.Parent.TotalWeight.CurrentValue(MaterialCalcObjectType.FromJob), 5)
        pForecastWeight.JobAmount = tJobAmount
        pForecastWeight.JobAmountLeft = tJobAmountLeft
    except BaseException as error:
            MdlGlobal.RecordError('GetChannelForecastWeight', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum)


def GetChannelMaterialID(pJobID, pMaterialID, pChannelNum):
    tMaterialID = 0
    tMaterialClassID = 0
    tMPGI = 0
    strSQL = ""
    dbCursor = None
    tRefRecipeMaterialID = 0
    tRefRecipeMaterialMPGI = 0

    try:        
        tMaterialID = MdlADOFunctions.fGetRstValLong(fGetRecipeValueJob(pJobID, 'Material ID', pChannelNum, 0))
        if tMaterialID != 0:
            pMaterialID.CurrentValue = tMaterialID
            strSQL = 'SELECT CalcInMaterialTotal, IsPConfigSpecialMaterial, MaterialClassID, MaterialGroup FROM TblMaterial WHERE ID = ' + tMaterialID
            dbCursor = MdlConnection.CN.cursor()
            
            dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                pMaterialID.MaterialType = MdlADOFunctions.fGetRstValLong(val["MaterialGroup"])
                pMaterialID.IsPConfigSpecialMaterial = MdlADOFunctions.fGetRstValBool(val["IsPConfigSpecialMaterial"], False)
                pMaterialID.CalcInMaterialTotal = MdlADOFunctions.fGetRstValBool(val["CalcInMaterialTotal"], True)
                tMaterialClassID = MdlADOFunctions.fGetRstValLong(val["MaterialClassID"])
        
            if dbCursor:
                dbCursor.close()
            strSQL = 'SELECT IsRawMaterial,IsAdditiveMaterial,IsAccompanyingMaterial FROM STblMaterialGroup WHERE ID = ' + pMaterialID.MaterialType
            dbCursor = MdlConnection.CN.cursor()
            
            dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                pMaterialID.IsRawMaterial = MdlADOFunctions.fGetRstValBool(val["IsRawMaterial"], False)
                pMaterialID.IsAdditiveMaterial = MdlADOFunctions.fGetRstValBool(val["IsAdditiveMaterial"], False)
                pMaterialID.IsAccompanyingMaterial = MdlADOFunctions.fGetRstValBool(val["IsAccompanyingMaterial"], False)
        
            if dbCursor:
                dbCursor.close()
            pMaterialID.MaterialClassID = tMaterialClassID
            if tMaterialClassID != 0:
                tMPGI = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('MPGI', 'TblMaterialClass', 'ID = ' + tMaterialClassID))
                pMaterialID.MPGI = tMPGI
            else:
                pMaterialID.MPGI = 1
            
            if (pMaterialID.Parent.Job.RecipeRefType == 1):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(fGetRecipeValueProduct(pMaterialID.Parent.Job.Product.ID, 'Material ID', pChannelNum, 0))
            elif (pMaterialID.Parent.Job.RecipeRefType == 2):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(fGetRecipeValueJob(pMaterialID.Parent.Job.RecipeRefJob, 'Material ID', pChannelNum, 0))
            elif (pMaterialID.Parent.Job.RecipeRefType == 6):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(fGetRecipeValueStandard(pMaterialID.Parent.Job.RecipeRefStandardID, 'Material ID', pChannelNum, 0, pMaterialID.Parent.Job.Product.ID))
            if tRefRecipeMaterialID != 0:
                pMaterialID.RefRecipeValue = tRefRecipeMaterialID
                strSQL = 'SELECT CalcInMaterialTotal,MaterialClassID FROM TblMaterial WHERE ID = ' + tRefRecipeMaterialID
                dbCursor = MdlConnection.CN.cursor()
                
                dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                pMaterialID.RefRecipeMaterialClassID = MdlADOFunctions.fGetRstValLong(val["MaterialClassID"])
                pMaterialID.RefRecipeCalcInMaterialTotal = MdlADOFunctions.fGetRstValBool(val["CalcInMaterialTotal"], True)
        
                if dbCursor:
                    dbCursor.close()
                if pMaterialID.RefRecipeMaterialClassID != 0:
                    strSQL = 'SELECT MPGI FROM TblMaterialClass WHERE ID = ' + pMaterialID.RefRecipeMaterialClassID
                    dbCursor = MdlConnection.CN.cursor()
                    
                    dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                pMaterialID.RefRecipeMPGI = MdlADOFunctions.fGetRstValDouble(val["MPGI"])
        
                if dbCursor:
                    dbCursor.close()
                else:
                    pMaterialID.RefRecipeMPGI = 1
   
    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('GetChannelMaterialID', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum)

    if dbCursor:
        dbCursor.close()
    dbCursor = None


def GetChannelMaterialPC(pJobID, pMaterialPC, pChannelNum):
    tMaterialPC = 0

    try:        
        tMaterialPC = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(pJobID, 'MaterialPC', pChannelNum, 0))
        if tMaterialPC != 0:
            pMaterialPC.CurrentValue = tMaterialPC

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('GetChannelMaterialPC', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum)


def GetChannelMaterialPCTarget(pJobID, pMaterialPCTarget, pChannelNum):
    tMaterialPCTarget = 0
    tProductRecipeMaterialPCTarget = 0
    tProductStandardMaterialPCTarget = 0
    tRecipeRefMaterialPCTarget = 0

    try:        
        tMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(pJobID, 'MaterialPCTarget', pChannelNum, 0))
        if tMaterialPCTarget != 0:
            pMaterialPCTarget.CurrentValue = tMaterialPCTarget
        tProductRecipeMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueProduct(pMaterialPCTarget.Parent.Machine.ActiveJob.Product.ID, 'MaterialPCTarget', pChannelNum, 0))
        if tProductRecipeMaterialPCTarget != 0:
            pMaterialPCTarget.ProductRecipeValue = tProductRecipeMaterialPCTarget
        if pMaterialPCTarget.Parent.Machine.ActiveJob.RecipeRefStandardID != 0:
            tProductStandardMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueStandard(pMaterialPCTarget.Parent.Machine.ActiveJob.RecipeRefStandardID, 'MaterialPCTarget', pChannelNum, 0, pMaterialPCTarget.Parent.Machine.ActiveJob.Product.ID))
            if tProductStandardMaterialPCTarget != 0:
                pMaterialPCTarget.ProductStandardValue = tProductStandardMaterialPCTarget
        
        if (pMaterialPCTarget.Parent.Job.RecipeRefType == 1):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueProduct(pMaterialPCTarget.Parent.Job.Product.ID, 'MaterialPCTarget', pChannelNum, 0))
        elif (pMaterialPCTarget.Parent.Job.RecipeRefType == 2):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(pMaterialPCTarget.Parent.Job.RecipeRefJob, 'MaterialPCTarget', pChannelNum, 0))
        elif (pMaterialPCTarget.Parent.Job.RecipeRefType == 6):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueStandard(pMaterialPCTarget.Parent.Job.RecipeRefStandardID, 'MaterialPCTarget', pChannelNum, 0, pMaterialPCTarget.Parent.Job.Product.ID))
        if tRecipeRefMaterialPCTarget != 0:
            pMaterialPCTarget.RecipeRefValue = tRecipeRefMaterialPCTarget

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelMaterialPCTarget', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum)


def CheckChannelJobMaterialRecord(pChannel):
    strSQL = ""
    dbCursor = None
    strTitle = ""

    try:        
        strSQL = 'SELECT ID FROM TblJobMaterial WHERE Job = ' + pChannel.Job.ID
        strSQL = strSQL + ' AND ChannelNum = ' + pChannel.ChannelNum
        strSQL = strSQL + ' AND SplitNum = 0'
        strSQL = strSQL + ' AND Material = ' + pChannel.MaterialID.CurrentValue
        if not pChannel.MaterialBatch is None:
            strSQL = strSQL + ' AND MaterialBatch = \'' + pChannel.MaterialBatch.CurrentValue + '\''
        dbCursor = MdlConnection.CN.cursor()
        
        if dbCursor:
            strTitle = 'INSERT INTO TblJobMaterial'
            strSQL = ' ('
            strSQL = strSQL + 'Job'
            strSQL = strSQL + ',ChannelNum'
            strSQL = strSQL + ',SplitNum'
            strSQL = strSQL + ',Material'
            strSQL = strSQL + ',MaterialType'
            strSQL = strSQL + ',MaterialClassID'
            strSQL = strSQL + ',MaterialPC'
            strSQL = strSQL + ',MaterialPCStandad'
            if not pChannel.MaterialBatch is None:
                strSQL = strSQL + ',MaterialBatch'
                strSQL = strSQL + ',InventoryID'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + pChannel.Job.ID
            strSQL = strSQL + ',' + pChannel.ChannelNum
            strSQL = strSQL + ',0'
            strSQL = strSQL + ',' + pChannel.MaterialID.CurrentValue
            strSQL = strSQL + ',' + pChannel.MaterialID.MaterialType
            strSQL = strSQL + ',' + pChannel.MaterialID.MaterialClassID
            strSQL = strSQL + ',' + pChannel.MaterialPCTarget.CurrentValue
            strSQL = strSQL + ',' + pChannel.MaterialPCTarget.CurrentValue
            if not pChannel.MaterialBatch is None:
                strSQL = strSQL + ',\'' + pChannel.MaterialBatch.CurrentValue + '\''
                strSQL = strSQL + ',' + pChannel.MaterialBatch.ID
            strSQL = strSQL + ')'

            dbCursor.execute(strTitle + strSQL)
            if pChannel.Job.Status == 10:
                strTitle = 'INSERT INTO TblJobCurrentMaterial'
                dbCursor.execute(strTitle + strSQL)
        
    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('CheckChannelJobMaterialRecord', 0, error.args[0], 'JobID: ' + pChannel.Job.ID + '. ChannelNum: ' + pChannel.ChannelNum)

    if dbCursor:
        dbCursor.close()
    dbCursor = None


def CheckChannelJoshMaterialRecord(pChannel):
    strSQL = ""
    dbCursor = None
    strTitle = ""

    try:        
        strSQL = 'SELECT ID FROM TblJoshMaterial WHERE JoshID = ' + pChannel.Job.ActiveJosh.ID
        strSQL = strSQL + ' AND ChannelNum = ' + pChannel.ChannelNum
        strSQL = strSQL + ' AND SplitNum = 0'
        strSQL = strSQL + ' AND Material = ' + pChannel.MaterialID.CurrentValue
        if not pChannel.MaterialBatch is None:
            strSQL = strSQL + ' AND MaterialBatch = \'' + pChannel.MaterialBatch.CurrentValue + '\''
        dbCursor = MdlConnection.CN.cursor()
        
        if dbCursor:
            strTitle = 'INSERT INTO TblJoshMaterial'
            strSQL = ' ('
            strSQL = strSQL + 'JobID'
            strSQL = strSQL + ',JoshID'
            strSQL = strSQL + ',ProductID'
            strSQL = strSQL + ',ChannelNum'
            strSQL = strSQL + ',SplitNum'
            strSQL = strSQL + ',Material'
            strSQL = strSQL + ',MaterialTypeID'
            strSQL = strSQL + ',MaterialClassID'
            strSQL = strSQL + ',ShiftID'
            strSQL = strSQL + ',ShiftDefID'
            strSQL = strSQL + ',JoshStart'
            strSQL = strSQL + ',MachineID'
            strSQL = strSQL + ',MaterialPC'
            strSQL = strSQL + ',MaterialPCStandad'
            if not pChannel.MaterialBatch is None:
                strSQL = strSQL + ',MaterialBatch'
                strSQL = strSQL + ',InventoryID'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + pChannel.Job.ID
            strSQL = strSQL + ',' + pChannel.Job.ActiveJosh.ID
            strSQL = strSQL + ',' + pChannel.Job.Product.ID
            strSQL = strSQL + ',' + pChannel.ChannelNum
            strSQL = strSQL + ',0'
            strSQL = strSQL + ',' + pChannel.MaterialID.CurrentValue
            strSQL = strSQL + ',' + pChannel.MaterialID.MaterialType
            strSQL = strSQL + ',' + pChannel.MaterialID.MaterialClassID
            strSQL = strSQL + ',' + pChannel.Job.ActiveJosh.ShiftID
            strSQL = strSQL + ',' + pChannel.Job.ActiveJosh.ShiftDefID
            strSQL = strSQL + ',\'' + ShortDate(pChannel.Job.ActiveJosh.StartTime, True, True, True) + '\''
            strSQL = strSQL + ',' + pChannel.Job.Machine.ID
            strSQL = strSQL + ',' + pChannel.MaterialPCTarget.CurrentValue
            strSQL = strSQL + ',' + pChannel.MaterialPCTarget.CurrentValue
            if not pChannel.MaterialBatch is None:
                strSQL = strSQL + ',\'' + pChannel.MaterialBatch.CurrentValue + '\''
                strSQL = strSQL + ',' + pChannel.MaterialBatch.ID
            strSQL = strSQL + ')'
            dbCursor.execute(strTitle + strSQL)
            if pChannel.Job.Status == 10:
                strTitle = 'INSERT INTO TblJoshCurrentMaterial'
                dbCursor.execute(strTitle + strSQL)
        
    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('CheckChannelJoshMaterialRecord', 0, error.args[0], 'JobID: ' + pChannel.Job.ID + '. ChannelNum: ' + pChannel.ChannelNum)

    if dbCursor:
        dbCursor.close()                
    dbCursor = None


def GetChannelMaterialBatch(pJobID, pMaterialBatch, pChannelNum):
    tMaterialBatch = ""
    strSQL = ""
    dbCursor = None
    tInventoryID = 0

    try:        
        tMaterialBatch = fGetRecipeValueJob(pJobID, 'MaterialBatch', pChannelNum, 0)
        if tMaterialBatch != '':
            strSQL = 'SELECT ID,Amount,EffectiveAmount, EffectiveOriginalAmount,Weight,GrossWeight,ParentInventoryID FROM TblInventory WHERE Batch = \'' + tMaterialBatch + '\''
            dbCursor = MdlConnection.CN.cursor()
            
            dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            if val:
                tInventoryID = MdlADOFunctions.fGetRstValLong(val["ID"])
                pMaterialBatch = GetInventoryItemFromGlobalCollection(gServer.ActiveInventoryItems, tInventoryID)
                if pMaterialBatch is None:
                    pMaterialBatch = MaterialBatch()
                    pMaterialBatch.ID = tInventoryID
                    pMaterialBatch.CurrentValue = tMaterialBatch
                    pMaterialBatch.EffectiveAmount = MdlADOFunctions.fGetRstValDouble(val["EffectiveAmount"])
                    pMaterialBatch.Amount = MdlADOFunctions.fGetRstValDouble(val["Amount"])
                    pMaterialBatch.OriginalEffectiveAmount = MdlADOFunctions.fGetRstValDouble(val["EffectiveOriginalAmount"])
                    
                    pMaterialBatch.Weight = MdlADOFunctions.fGetRstValDouble(val["Weight"])
                    
                    pMaterialBatch.GrossWeight = MdlADOFunctions.fGetRstValDouble(val["GrossWeight"])
                    
                    pMaterialBatch.ParentInventoryID = MdlADOFunctions.fGetRstValLong(val["ParentInventoryID"])
                    AddInventoryItemToGlobalCollection(pMaterialBatch)
                        
    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('GetChannelMaterialPCTarget', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum)

    if dbCursor:
        dbCursor.close()
    dbCursor = None


def AddMaterialFlowAmountToChannel(pJob, pChannel, pAmount, pMaterialCalcObjectType):
    tWeightDiff = 0
        
    try:
        if pChannel.Job.Machine.DSIsActive == True and not pChannel.TotalWeight.ControllerField is None:
            if MdlADOFunctions.fGetRstValBool(pChannel.TotalWeight.ControllerField.DirectRead, False) == False:
                CalcWeightDiff(pJob, pChannel, pAmount, pMaterialCalcObjectType)
            tWeightDiff = pAmount
            if ( tWeightDiff > 0 and pChannel.Machine.IsOffline == False )  or pChannel.Machine.IsOffline == True:
                pChannel.TotalWeight.SetMaterialFlowAmount(pMaterialCalcObjectType, ( pJob.PConfigPC / 100 )  * tWeightDiff)
                pChannel.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, pChannel.TotalWeight.CurrentValue(pMaterialCalcObjectType) + pChannel.TotalWeight.MaterialFlowAmount(pMaterialCalcObjectType))
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    if not pChannel.MaterialBatch is None:
                        pChannel.MaterialBatch.EffectiveAmount = pChannel.MaterialBatch.EffectiveAmount - tWeightDiff
        else:
            CalcWeightDiff(pJob, pChannel, pAmount, pMaterialCalcObjectType)
    except:
        pass


def CalcWeightDiff(pJob, pChannel, pAmount, pMaterialCalcObjectType):
    if pChannel.ChannelNum != 100:
        tWeightDiff = pAmount *  ( pJob.ProductWeightLast / 1000 )  *  ( pChannel.MaterialPCTarget.CurrentValue / 100 )
    else:
        tWeightDiff = pAmount * pChannel.MaterialPCTarget.CurrentValue
    if ( tWeightDiff > 0 and pChannel.Machine.IsOffline == False )  or pChannel.Machine.IsOffline == True:
        pChannel.TotalWeight.SetMaterialFlowAmount(pMaterialCalcObjectType, tWeightDiff)
        pChannel.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, pChannel.TotalWeight.CurrentValue(pMaterialCalcObjectType) + pChannel.TotalWeight.MaterialFlowAmount(pMaterialCalcObjectType))
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            if not pChannel.MaterialBatch is None:
                pChannel.MaterialBatch.EffectiveAmount = pChannel.MaterialBatch.EffectiveAmount - tWeightDiff


def ReduceChannelAmountByRejects(pJob, pChannel, pRejects, pMaterialCalcObjectType):
    tAmount = 0
    tMaterialPCTarget = 0
    returnVal = False

    try:
        if pChannel.ChannelNum != 100:
            tMaterialPCTarget = ( pChannel.MaterialPCTarget.CurrentValue / 100 )
            tAmount = ( pRejects / pJob.CavitiesActual )  *  ( pJob.ProductWeightLast / 1000 )  * tMaterialPCTarget
        else:
            tMaterialPCTarget = pChannel.MaterialPCTarget.CurrentValue
            tAmount = ( pRejects / pJob.CavitiesActual )  * tMaterialPCTarget
        if tAmount != 0:
            pChannel.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, pChannel.TotalWeight.CurrentValue(pMaterialCalcObjectType) - tAmount)
            if not ( pChannel.MaterialBatch is None ) :
                pChannel.MaterialBatch.EffectiveAmount = pChannel.MaterialBatch.EffectiveAmount + tAmount
        returnVal = True
    
    except:
        pass
    return returnVal

def CheckRecipeChannelVSLocationMatch(pChannel, pControllerID, pInventoryMaterialID):
    tValidationFields = ""
    tFields = ""
    tRecipeSingleField = ""
    tInventorySingleField = ""
    tVariant = None
    tInventoryValidationValue = ""
    tRecipeValidationValue = ""
    tComparedFields = ""
    returnVal = False

    try:
        tValidationFields = MdlADOFunctions.fGetRstValString(GetChannelSplitProperty('RecipeVSLocationValidationFields', pControllerID, pChannel.ChannelNum, 0))

        if tValidationFields == '':
            tValidationFields = 'TblMaterial.ID=TblMaterial.ID'
        tFields = tValidationFields.split(',')
        for tVariant in tFields:
            tComparedFields = str(tVariant).split('=')
            tRecipeSingleField = str(tComparedFields(0)).split('.')
            select_3 = tRecipeSingleField(0)

            if (select_3 == 'TblMaterial'):
                if tRecipeSingleField(1) == 'ID':
                    tRecipeValidationValue = str(pChannel.MaterialID.CurrentValue)
                else:                    
                    tRecipeValidationValue = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue(tRecipeSingleField(1), tRecipeSingleField(0), 'ID = ' + pChannel.MaterialID.CurrentValue))
            else:
                raise("'" + select_3 + "' not found.")

            tInventorySingleField = str(tComparedFields(1)).split('.')
            select_4 = tInventorySingleField(0)
            if (select_4 == 'TblMaterial'):
                tInventoryValidationValue = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue(tInventorySingleField(1), tInventorySingleField(0), 'ID = ' + pInventoryMaterialID))
            else:
                raise("'" + select_4 + "' not found.")
            
            if tRecipeValidationValue == tInventoryValidationValue:
                returnVal = True
        
    except BaseException as error:
        MdlGlobal.RecordError('CheckRecipeChannelVSLocationMatch', 0, error.args[0], 'ControllerID = ' + pControllerID + '. ChannelNum = ' + pChannel.ChannelNum)

    return returnVal
    