import enum
import MdlConnection
import MdlADOFunctions
from ClassModules.Channel import MaterialCalcObjectType
import MdlGlobal

class ControllerFieldNameType(enum.Enum):
    MaterialPC = 0
    MaterialPCTarget = 1
    TotalWeight = 2
    TotalWeightLast = 3
    ChannelStatus = 4
    MaterialID = 5

def GetSplitControllerFieldName(ChannelNum, SplitNum, NameType):
    result = ""
    if (NameType == ControllerFieldNameType.MaterialPC):
        result = 'Cnl' + ChannelNum + 'MainMatPC' + SplitNum
    elif (NameType == ControllerFieldNameType.MaterialPCTarget):
        result = 'Cnl' + ChannelNum + 'MainMatPCTarget' + SplitNum
    elif (NameType == ControllerFieldNameType.TotalWeight):
        result = 'Cnl' + ChannelNum + 'MainMatTTLW' + SplitNum
    elif (NameType == ControllerFieldNameType.TotalWeightLast):
        result = 'Cnl' + ChannelNum + 'MainMatTTLWLast' + SplitNum
    elif (NameType == ControllerFieldNameType.MaterialID):
        result = 'Cnl' + ChannelNum + 'MainMatID' + SplitNum
    return result


def GetChannelSplitTotalWeight(pJobID, pJoshID, pTotalWeight, pChannelNum, pSplitNum, pMaterialID, pMaterialBatch=''):
    strSQL = ""
    dbCursor = None

    try:
        if pJoshID != 0:
            strSQL = 'SELECT Amount, MaterialFlowAmount FROM TblJobMaterial WHERE Job = ' + pJobID
            strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
            strSQL = strSQL + ' AND SplitNum = ' + pSplitNum
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
            strSQL = strSQL + ' FROM TblJobMaterial WHERE Job = ' + pJobID
            strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
            strSQL = strSQL + ' AND SplitNum = ' + pSplitNum
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
 
            GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pSplitNum, pMaterialID, pMaterialBatch='')

        else:
            
            strSQL = 'SELECT SUM(Amount) AS Amount FROM TblJoshMaterial WHERE JobID = ' + pJobID
            strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
            strSQL = strSQL + ' AND SplitNum = ' + pSplitNum
            strSQL = strSQL + ' AND Material = ' + pMaterialID
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND MaterialBatch = \'' + pMaterialBatch + '\''
            dbCursor = MdlConnection.CN.cursor()
            dbCursor.execute(strSQL)
            val = dbCursor.fetchone()
            
            if val:
                pTotalWeight.SetCurrentValue(MaterialCalcObjectType.FromJob, MdlADOFunctions.fGetRstValDouble(val["Amount"]))
            if dbCursor:
                dbCursor.close()
            
            strSQL = 'SELECT SUM(MaterialActualIndex) AS MaterialActualIndex, '
            strSQL = strSQL + ' SUM(Amount) AS Amount, '
            strSQL = strSQL + ' SUM(AmountStandard) AS AmountStandard '
            strSQL = strSQL + ' FROM TblJoshMaterial WHERE JobID = ' + pJobID
            strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
            strSQL = strSQL + ' AND SplitNum = ' + pSplitNum
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
                        
            if pTotalWeight.Parent.Parent.Job.Status == 10:
                pJoshID = pTotalWeight.Parent.Parent.Job.ActiveJosh.ID
                GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pSplitNum, pMaterialID, pMaterialBatch='')

        dbCursor = None
    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('GetChannelSplitTotalWeight', 0, error.args[0], 'JobID: ' + pJobID + '. JoshID: ' + pJoshID + '. ChannelNum: ' + pChannelNum + '. SplitNum: ' + pSplitNum)


def GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pSplitNum, pMaterialID, pMaterialBatch=''):
    strSQL = 'SELECT Amount,AmountStandard,MaterialFlowAmount FROM TblJoshMaterial WHERE JoshID = ' + pJoshID
    strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
    strSQL = strSQL + ' AND SplitNum = ' + pSplitNum
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
    
    strSQL = 'SELECT SUM(MaterialActualIndex) AS MaterialActualIndex, '
    strSQL = strSQL + ' SUM(Amount) AS Amount,'
    strSQL = strSQL + ' SUM(AmountStandard) AS AmountStandard '
    strSQL = strSQL + ' FROM TblJoshMaterial WHERE JoshID = ' + pJoshID
    strSQL = strSQL + ' AND ChannelNum = ' + pChannelNum
    strSQL = strSQL + ' AND SplitNum = ' + pSplitNum
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


def GetChannelSplitForecastWeight(pJobID, pForecastWeight, pChannelNum, pSplitNum):
    tProductWeight = 0
    tUnitsTarget = 0.0
    tCavitiesActual = 0.0
    tMaterialPCTarget = 0.0
    tJobAmount = 0.0
    tJobAmountLeft = 0.0

    try:    
        tProductWeight = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(pJobID, 'ProductWeight', 0, 0))
        tUnitsTarget = pForecastWeight.Parent.Parent.Job.UnitsTarget
        tCavitiesActual = pForecastWeight.Parent.Parent.Job.CavitiesActual
        tMaterialPCTarget = pForecastWeight.Parent.MaterialPCTarget.CurrentValue
        if pChannelNum != 100:
            tJobAmount = round(( tUnitsTarget / tCavitiesActual )  *  ( tProductWeight / 1000 )  *  ( tMaterialPCTarget / 100 ), 5)
        else:
            tJobAmount = round(( tUnitsTarget / tCavitiesActual )  *  ( tMaterialPCTarget ), 5)
        tJobAmountLeft = round(tJobAmount - pForecastWeight.Parent.TotalWeight.CurrentValue(MaterialCalcObjectType.FromJob), 5)
        pForecastWeight.JobAmount = tJobAmount
        pForecastWeight.JobAmountLeft = tJobAmountLeft

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelSplitForecastWeight', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum + '. SplitNum: ' + pSplitNum)



def GetChannelSplitMaterialID(pJobID, pMaterialID, pChannelNum, pSplitNum):
    tMaterialID = 0
    tMaterialClassID = 0
    tMPGI = 0.0
    strSQL = ""
    dbCursor = None
    tRefRecipeMaterialID = 0

    try:    
        tMaterialID = MdlADOFunctions.fGetRstValLong(fGetRecipeValueJob(pJobID, 'Material ID', pChannelNum, pSplitNum))
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
            
            if (pMaterialID.Parent.Parent.Job.RecipeRefType == 1):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(fGetRecipeValueProduct(pMaterialID.Parent.Parent.Job.Product.ID, 'Material ID', pChannelNum, pSplitNum))
            elif (pMaterialID.Parent.Parent.Job.RecipeRefType == 2):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(fGetRecipeValueJob(pMaterialID.Parent.Parent.Job.RecipeRefJob, 'Material ID', pChannelNum, pSplitNum))
            elif (pMaterialID.Parent.Parent.Job.RecipeRefType == 6):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(fGetRecipeValueStandard(pMaterialID.Parent.Parent.Job.RecipeRefStandardID, 'Material ID', pChannelNum, pSplitNum, pMaterialID.Parent.Parent.Job.Product.ID))
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
        dbCursor = None

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelSplitMaterialID', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum + '. SplitNum: ' + pSplitNum)


def GetChannelSplitMaterialPC(pJobID, pMaterialPC, pChannelNum, pSplitNum):
    tMaterialPC = 0.0
    try:
        tMaterialPC = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(pJobID, 'MaterialPC', pChannelNum, pSplitNum))
        if tMaterialPC != 0:
            pMaterialPC.CurrentValue = tMaterialPC

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelSplitMaterialPC', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum + '. SplitNum: ' + pSplitNum)


def GetChannelSplitMaterialPCTarget(pJobID, pMaterialPCTarget, pChannelNum, pSplitNum):
    tMaterialPCTarget = 0.0
    tProductRecipeMaterialPCTarget = 0.0
    tProductStandardMaterialPCTarget = 0.0
    tRecipeRefMaterialPCTarget = 0.0
    
    try:
        tMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(pJobID, 'MaterialPCTarget', pChannelNum, pSplitNum))
        if tMaterialPCTarget != 0:
            pMaterialPCTarget.CurrentValue = tMaterialPCTarget
        tProductRecipeMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueProduct(pMaterialPCTarget.Parent.Parent.Machine.ActiveJob.Product.ID, 'MaterialPCTarget', pChannelNum, pSplitNum))
        if tProductRecipeMaterialPCTarget != 0:
            pMaterialPCTarget.ProductRecipeValue = tProductRecipeMaterialPCTarget
        if pMaterialPCTarget.Parent.Parent.Machine.ActiveJob.RecipeRefStandardID > 0:
            tProductStandardMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueStandard(pMaterialPCTarget.Parent.Parent.Machine.ActiveJob.RecipeRefStandardID, 'MaterialPCTarget', pChannelNum, pSplitNum, pMaterialPCTarget.Parent.Parent.Machine.ActiveJob.Product.ID))
            if tProductStandardMaterialPCTarget != 0:
                pMaterialPCTarget.ProductStandardValue = tProductStandardMaterialPCTarget
        
        if (pMaterialPCTarget.Parent.Parent.Job.RecipeRefType == 1):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueProduct(pMaterialPCTarget.Parent.Parent.Job.Product.ID, 'MaterialPCTarget', pChannelNum, pSplitNum))
        elif (pMaterialPCTarget.Parent.Parent.Job.RecipeRefType == 2):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(pMaterialPCTarget.Parent.Parent.Job.RecipeRefJob, 'MaterialPCTarget', pChannelNum, pSplitNum))
        elif (pMaterialPCTarget.Parent.Parent.Job.RecipeRefType == 6):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueStandard(pMaterialPCTarget.Parent.Parent.Job.RecipeRefStandardID, 'MaterialPCTarget', pChannelNum, pSplitNum, pMaterialPCTarget.Parent.Parent.Job.Product.ID))
        if tRecipeRefMaterialPCTarget != 0:
            pMaterialPCTarget.RecipeRefValue = tRecipeRefMaterialPCTarget

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelSplitMaterialPCTarget', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum + '. SplitNum: ' + pSplitNum)


def CheckSplitJobMaterialRecord(pSplit):
    strSQL = ""
    dbCursor = None
    strTitle = ""

    try:    
        strSQL = 'SELECT ID FROM TblJobMaterial WHERE Job = ' + pSplit.Parent.Job.ID
        strSQL = strSQL + ' AND ChannelNum = ' + pSplit.Parent.ChannelNum
        strSQL = strSQL + ' AND SplitNum = ' + pSplit.SplitNum
        strSQL = strSQL + ' AND Material = ' + pSplit.MaterialID.CurrentValue
        if not pSplit.MaterialBatch is None:
            strSQL = strSQL + ' AND MaterialBatch = \'' + pSplit.MaterialBatch.CurrentValue + '\''
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
            if not pSplit.MaterialBatch is None:
                strSQL = strSQL + ',MaterialBatch'
                strSQL = strSQL + ',InventoryID'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + pSplit.Parent.Job.ID
            strSQL = strSQL + ',' + pSplit.Parent.ChannelNum
            strSQL = strSQL + ',' + pSplit.SplitNum
            strSQL = strSQL + ',' + pSplit.MaterialID.CurrentValue
            strSQL = strSQL + ',' + pSplit.MaterialID.MaterialType
            strSQL = strSQL + ',' + pSplit.MaterialID.MaterialClassID
            strSQL = strSQL + ',' + pSplit.MaterialPCTarget.CurrentValue
            strSQL = strSQL + ',' + pSplit.MaterialPCTarget.CurrentValue
            if not pSplit.MaterialBatch is None:
                strSQL = strSQL + ',\'' + pSplit.MaterialBatch.CurrentValue + '\''
                strSQL = strSQL + ',' + pSplit.MaterialBatch.ID
            strSQL = strSQL + ')'

            MdlConnection.CN.execute(strTitle + strSQL)
            if pSplit.Parent.Job.Status == 10:
                strTitle = 'INSERT INTO TblJobCurrentMaterial'
                MdlConnection.CN.execute(strTitle + strSQL)

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('CheckSplitJobMaterialRecord', 0, error.args[0], 'JobID: ' + pSplit.Parent.Job.ID + '. ChannelNum: ' + pSplit.Parent.ChannelNum + '. SplitNum: ' + pSplit.SplitNum)

    if dbCursor:
        dbCursor.close()
    dbCursor = None


def CheckSplitJoshMaterialRecord(pSplit):
    strSQL = ""
    dbCursor = None
    strTitle = ""

    try:    
        strSQL = 'SELECT ID FROM TblJoshMaterial WHERE JoshID = ' + pSplit.Parent.Job.ActiveJosh.ID
        strSQL = strSQL + ' AND ChannelNum = ' + pSplit.Parent.ChannelNum
        strSQL = strSQL + ' AND SplitNum = ' + pSplit.SplitNum
        strSQL = strSQL + ' AND Material = ' + pSplit.MaterialID.CurrentValue
        if not pSplit.MaterialBatch is None:
            strSQL = strSQL + ' AND MaterialBatch = \'' + pSplit.MaterialBatch.CurrentValue + '\''
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
            if not pSplit.MaterialBatch is None:
                strSQL = strSQL + ',MaterialBatch'
                strSQL = strSQL + ',InventoryID'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + pSplit.Parent.Job.ID
            strSQL = strSQL + ',' + pSplit.Parent.Job.ActiveJosh.ID
            strSQL = strSQL + ',' + pSplit.Parent.Job.Product.ID
            strSQL = strSQL + ',' + pSplit.Parent.ChannelNum
            strSQL = strSQL + ',' + pSplit.SplitNum
            strSQL = strSQL + ',' + pSplit.MaterialID.CurrentValue
            strSQL = strSQL + ',' + pSplit.MaterialID.MaterialType
            strSQL = strSQL + ',' + pSplit.MaterialID.MaterialClassID
            strSQL = strSQL + ',' + pSplit.Parent.Job.ActiveJosh.ShiftID
            strSQL = strSQL + ',' + pSplit.Parent.Job.ActiveJosh.ShiftDefID
            strSQL = strSQL + ',\'' + ShortDate(pSplit.Parent.Job.ActiveJosh.StartTime, True, True, True) + '\''
            strSQL = strSQL + ',' + pSplit.Parent.Job.Machine.ID
            strSQL = strSQL + ',' + pSplit.MaterialPCTarget.CurrentValue
            strSQL = strSQL + ',' + pSplit.MaterialPCTarget.CurrentValue
            if not pSplit.MaterialBatch is None:
                strSQL = strSQL + ',\'' + pSplit.MaterialBatch.CurrentValue + '\''
                strSQL = strSQL + ',' + pSplit.MaterialBatch.ID
            strSQL = strSQL + ')'
            MdlConnection.CN.execute(strTitle + strSQL)
            if pSplit.Parent.Job.Status == 10:
                strTitle = 'INSERT INTO TblJoshCurrentMaterial'
                MdlConnection.CN.execute(strTitle + strSQL)

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('CheckSplitJoshMaterialRecord', 0, error.args[0], 'JobID: ' + pSplit.Parent.Job.ID + '. ChannelNum: ' + pSplit.Parent.ChannelNum + '. SplitNum: ' + pSplit.SplitNum)

    if dbCursor:
        dbCursor.close()
    dbCursor = None


def GetChannelSplitMaterialBatch(pJobID, pMaterialBatch, pChannelNum, pSplitNum):
    tMaterialBatch = ""
    strSQL = ""
    dbCursor = None
    tInventoryID = 0
    
    try:
        tMaterialBatch = fGetRecipeValueJob(pJobID, 'MaterialBatch', pChannelNum, pSplitNum)
        if tMaterialBatch != '':
            strSQL = 'SELECT ID,Amount,EffectiveAmount,EffectiveOriginalAmount,Weight,GrossWeight,ParentInventoryID FROM TblInventory WHERE Batch = \'' + tMaterialBatch + '\''
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
        MdlGlobal.RecordError('GetChannelSplitMaterialBatch', 0, error.args[0], 'JobID: ' + pJobID + '. ChannelNum: ' + pChannelNum + '. SplitNum: ' + pSplitNum)

    if dbCursor:
        dbCursor.close()
    dbCursor = None


def AddMaterialFlowAmountToSplit(pJob, pSplit, pAmount, pMaterialCalcObjectType):
    tWeightDiff = 0.0
    
    try:
        if pJob.Machine.DSIsActive == True and not pSplit.TotalWeight.ControllerField is None:
            if MdlADOFunctions.fGetRstValBool(pSplit.TotalWeight.ControllerField.DirectRead, False) == False:
                CalcWeightDiff(pJob, pSplit, pAmount, pMaterialCalcObjectType)
            tWeightDiff = pAmount
            if ( tWeightDiff > 0 and pJob.Machine.IsOffline == False )  or pJob.Machine.IsOffline == True:
                pSplit.TotalWeight.SetMaterialFlowAmount(pMaterialCalcObjectType, ( pJob.PConfigPC / 100 )  * tWeightDiff)
                pSplit.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, pSplit.TotalWeight.CurrentValue(pMaterialCalcObjectType) + pSplit.TotalWeight.MaterialFlowAmount(pMaterialCalcObjectType))
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    if not pSplit.MaterialBatch is None:
                        pSplit.MaterialBatch.EffectiveAmount = pSplit.MaterialBatch.EffectiveAmount - tWeightDiff
        else:
            CalcWeightDiff(pJob, pSplit, pAmount, pMaterialCalcObjectType)
    except:
        pass


def CalcWeightDiff(pJob, pSplit, pAmount, pMaterialCalcObjectType):
    if pSplit.Parent.ChannelNum != 100:
        tWeightDiff = pAmount *  ( pJob.ProductWeightLast / 1000 )  *  ( pSplit.MaterialPCTarget.CurrentValue / 100 )
    else:
        tWeightDiff = pAmount * pSplit.MaterialPCTarget.CurrentValue
    if ( tWeightDiff > 0 and pJob.Machine.IsOffline == False )  or pJob.Machine.IsOffline == True:
        pSplit.TotalWeight.SetMaterialFlowAmount(pMaterialCalcObjectType, tWeightDiff)
        pSplit.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, pSplit.TotalWeight.CurrentValue(pMaterialCalcObjectType) + pSplit.TotalWeight.MaterialFlowAmount(pMaterialCalcObjectType))
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            if not pSplit.MaterialBatch is None:
                pSplit.MaterialBatch.EffectiveAmount = pSplit.MaterialBatch.EffectiveAmount - tWeightDiff


def ReduceSplitAmountByRejects(pJob, pSplit, pRejects, pMaterialCalcObjectType):
    tAmount = 0.0
    tMaterialPCTarget = 0.0
    returnVal = False
    try:
        if pSplit.Parent.ChannelNum != 100:
            tMaterialPCTarget = ( pSplit.MaterialPCTarget.CurrentValue / 100 )
            tAmount = ( pRejects / pJob.CavitiesActual )  *  ( pJob.ProductWeightLast / 1000 )  * tMaterialPCTarget
        else:
            tMaterialPCTarget = pSplit.MaterialPCTarget.CurrentValue
            tAmount = ( pRejects / pJob.CavitiesActual )  * tMaterialPCTarget
        if tAmount != 0:
            pSplit.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, pSplit.TotalWeight.CurrentValue(pMaterialCalcObjectType) - tAmount)
            if not ( pSplit.MaterialBatch is None ) :
                pSplit.MaterialBatch.EffectiveAmount = pSplit.MaterialBatch.EffectiveAmount + tAmount
        returnVal = True
    
    except BaseException as error:
        pass

    return returnVal

def CheckRecipeChannelSplitVSLocationMatch(pSplit, pControllerID, pInventoryMaterialID):
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
        tValidationFields = MdlADOFunctions.fGetRstValString(GetChannelSplitProperty('RecipeVSLocationValidationFields', pControllerID, pSplit.Parent.ChannelNum, pSplit.SplitNum))
        
        if tValidationFields == '':
            tValidationFields = 'TblMaterial.ID=TblMaterial.ID'
        tFields = tValidationFields.split(',')
        for tVariant in tFields:            
            tComparedFields = str(tVariant).split('=')
            tRecipeSingleField = str(tComparedFields(0)).split('.')
            select_3 = tRecipeSingleField(0)
            if (select_3 == 'TblMaterial'):
                if tRecipeSingleField(1) == 'ID':
                    tRecipeValidationValue = str(pSplit.MaterialID.CurrentValue)
                else:
                    
                    tRecipeValidationValue = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue(tRecipeSingleField(1), tRecipeSingleField(0), 'ID = ' + pSplit.MaterialID.CurrentValue))
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
        MdlGlobal.RecordError('CheckRecipeChannelSplitVSLocationMatch', 0, error.args[0], 'ControllerID = ' + pControllerID + '. ChannelNum = ' + pSplit.Parent.ChannelNum + '. SplitNum = ' + pSplit.SplitNum)

    return returnVal

