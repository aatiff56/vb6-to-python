from GlobalVariables import MaterialCalcObjectType
from MaterialBatch import MaterialBatch

import enum
import MdlConnection
import MdlADOFunctions
import MdlGlobal
import MdlUtilsH
import MdlUtils
import MdlRTInventory

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
        result = 'Cnl' + str(ChannelNum) + 'MainMatPC' + str(SplitNum)
    elif (NameType == ControllerFieldNameType.MaterialPCTarget):
        result = 'Cnl' + str(ChannelNum) + 'MainMatPCTarget' + str(SplitNum)
    elif (NameType == ControllerFieldNameType.TotalWeight):
        result = 'Cnl' + str(ChannelNum) + 'MainMatTTLW' + str(SplitNum)
    elif (NameType == ControllerFieldNameType.TotalWeightLast):
        result = 'Cnl' + str(ChannelNum) + 'MainMatTTLWLast' + str(SplitNum)
    elif (NameType == ControllerFieldNameType.MaterialID):
        result = 'Cnl' + str(ChannelNum) + 'MainMatID' + str(SplitNum)
    return result


def GetChannelSplitTotalWeight(pJobID, pJoshID, pTotalWeight, pChannelNum, pSplitNum, pMaterialID, pMaterialBatch=''):
    strSQL = ""
    RstCursor = None

    try:
        if pJoshID != 0:
            strSQL = 'SELECT Amount, MaterialFlowAmount FROM TblJobMaterial WHERE Job = ' + str(pJobID)
            strSQL = strSQL + ' AND ChannelNum = ' + str(pChannelNum)
            strSQL = strSQL + ' AND SplitNum = ' + str(pSplitNum)
            strSQL = strSQL + ' AND Material = ' + str(pMaterialID)
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND MaterialBatch = \'' + str(pMaterialBatch) + '\''
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstData:
                pTotalWeight.SetCurrentValue(MaterialCalcObjectType.FromJob, MdlADOFunctions.fGetRstValDouble(RstData.Amount))
                pTotalWeight.SetMaterialFlowAmount(MaterialCalcObjectType.FromJob, MdlADOFunctions.fGetRstValDouble(RstData.MaterialFlowAmount))
            if RstCursor:
                RstCursor.close()
            
            strSQL = 'SELECT SUM(MaterialActualIndex) AS MaterialActualIndex, '
            strSQL = strSQL + ' SUM(Amount) AS Amount, '
            strSQL = strSQL + ' SUM(AmountStandard) AS AmountStandard '
            strSQL = strSQL + ' FROM TblJobMaterial WHERE Job = ' + str(pJobID)
            strSQL = strSQL + ' AND ChannelNum = ' + str(pChannelNum)
            strSQL = strSQL + ' AND SplitNum = ' + str(pSplitNum)
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND (Material <> ' + str(pMaterialID) + ' OR (Material = ' + str(pMaterialID) + ' AND MaterialBatch <> \'' + str(pMaterialBatch) + '\'))'
            else:
                strSQL = strSQL + ' AND Material <> ' + str(pMaterialID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstData:
                pTotalWeight.SetOtherMaterialsActualIndex(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(RstData.MaterialActualIndex), 5))
                pTotalWeight.SetOtherMaterialsAmount(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(RstData.Amount), 5))
                pTotalWeight.SetOtherMaterialsAmountStandard(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(RstData.AmountStandard), 5))
            if RstCursor:
                RstCursor.close()
 
            GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pSplitNum, pMaterialID, pMaterialBatch='')

        else:            
            strSQL = 'SELECT SUM(Amount) AS Amount FROM TblJoshMaterial WHERE JobID = ' + str(pJobID)
            strSQL = strSQL + ' AND ChannelNum = ' + str(pChannelNum)
            strSQL = strSQL + ' AND SplitNum = ' + str(pSplitNum)
            strSQL = strSQL + ' AND Material = ' + str(pMaterialID)
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND MaterialBatch = \'' + str(pMaterialBatch) + '\''
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstData:
                pTotalWeight.SetCurrentValue(MaterialCalcObjectType.FromJob, MdlADOFunctions.fGetRstValDouble(RstData.Amount))
            if RstCursor:
                RstCursor.close()
            
            strSQL = 'SELECT SUM(MaterialActualIndex) AS MaterialActualIndex, '
            strSQL = strSQL + ' SUM(Amount) AS Amount, '
            strSQL = strSQL + ' SUM(AmountStandard) AS AmountStandard '
            strSQL = strSQL + ' FROM TblJoshMaterial WHERE JobID = ' + str(pJobID)
            strSQL = strSQL + ' AND ChannelNum = ' + str(pChannelNum)
            strSQL = strSQL + ' AND SplitNum = ' + str(pSplitNum)
            if pMaterialBatch != '':
                strSQL = strSQL + ' AND (Material <> ' + str(pMaterialID) + ' OR (Material = ' + str(pMaterialID) + ' AND MaterialBatch <> \'' + str(pMaterialBatch) + '\'))'
            else:
                strSQL = strSQL + ' AND Material <> ' + str(pMaterialID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstData:
                pTotalWeight.SetOtherMaterialsActualIndex(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(RstData.MaterialActualIndex), 5))
                pTotalWeight.SetOtherMaterialsAmount(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(RstData.Amount), 5))
                pTotalWeight.SetOtherMaterialsAmountStandard(MaterialCalcObjectType.FromJob, round(MdlADOFunctions.fGetRstValDouble(RstData.AmountStandard), 5))

            if RstCursor:
                RstCursor.close()
                        
            if pTotalWeight.Parent.Parent.Job.Status == 10:
                pJoshID = pTotalWeight.Parent.Parent.Job.ActiveJosh.ID
                GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pSplitNum, pMaterialID, pMaterialBatch='')

        RstCursor = None

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('GetChannelSplitTotalWeight', 0, error.args[0], 'JobID: ' + str(pJobID) + '. JoshID: ' + str(pJoshID) + '. ChannelNum: ' + str(pChannelNum) + '. SplitNum: ' + str(pSplitNum))


def GetAmountForJosh(pJoshID, pTotalWeight, pChannelNum, pSplitNum, pMaterialID, pMaterialBatch=''):
    strSQL = 'SELECT Amount,AmountStandard,MaterialFlowAmount FROM TblJoshMaterial WHERE JoshID = ' + str(pJoshID)
    strSQL = strSQL + ' AND ChannelNum = ' + str(pChannelNum)
    strSQL = strSQL + ' AND SplitNum = ' + str(pSplitNum)
    strSQL = strSQL + ' AND Material = ' + str(pMaterialID)
    if pMaterialBatch != '':
        strSQL = strSQL + ' AND MaterialBatch = \'' + str(pMaterialBatch) + '\''
    RstCursor = MdlConnection.CN.cursor()
    RstCursor.execute(strSQL)
    RstData = RstCursor.fetchone()
    
    if RstData:
        pTotalWeight.SetCurrentValue(MaterialCalcObjectType.FromJosh, MdlADOFunctions.fGetRstValDouble(RstData.Amount))
        pTotalWeight.SetStandardValue(MaterialCalcObjectType.FromJosh, MdlADOFunctions.fGetRstValDouble(RstData.AmountStandard))
        pTotalWeight.SetMaterialFlowAmount(MaterialCalcObjectType.FromJosh, MdlADOFunctions.fGetRstValDouble(RstData.MaterialFlowAmount))
    if RstCursor:
        RstCursor.close()
    
    strSQL = 'SELECT SUM(MaterialActualIndex) AS MaterialActualIndex, '
    strSQL = strSQL + ' SUM(Amount) AS Amount,'
    strSQL = strSQL + ' SUM(AmountStandard) AS AmountStandard '
    strSQL = strSQL + ' FROM TblJoshMaterial WHERE JoshID = ' + str(pJoshID)
    strSQL = strSQL + ' AND ChannelNum = ' + str(pChannelNum)
    strSQL = strSQL + ' AND SplitNum = ' + str(pSplitNum)
    if pMaterialBatch != '':
        strSQL = strSQL + ' AND (Material <> ' + str(pMaterialID) + ' OR (Material = ' + str(pMaterialID) + ' AND MaterialBatch <> \'' + str(pMaterialBatch) + '\'))'
    else:
        strSQL = strSQL + ' AND Material <> ' + str(pMaterialID)
    RstCursor = MdlConnection.CN.cursor()
    RstCursor.execute(strSQL)
    RstData = RstCursor.fetchone()
    
    if RstData:
        pTotalWeight.SetOtherMaterialsActualIndex(MaterialCalcObjectType.FromJosh, round(MdlADOFunctions.fGetRstValDouble(RstData.MaterialActualIndex), 5))
        pTotalWeight.SetOtherMaterialsAmount(MaterialCalcObjectType.FromJosh, round(MdlADOFunctions.fGetRstValDouble(RstData.Amount), 5))
        pTotalWeight.SetOtherMaterialsAmountStandard(MaterialCalcObjectType.FromJosh, round(MdlADOFunctions.fGetRstValDouble(RstData.AmountStandard), 5))
    if RstCursor:
        RstCursor.close()


def GetChannelSplitForecastWeight(pJobID, pForecastWeight, pChannelNum, pSplitNum):
    tProductWeight = 0
    tUnitsTarget = 0.0
    tCavitiesActual = 0.0
    tMaterialPCTarget = 0.0
    tJobAmount = 0.0
    tJobAmountLeft = 0.0

    try:    
        tProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(pJobID, 'ProductWeight', 0, 0))
        tUnitsTarget = pForecastWeight.Parent.Parent.Job.UnitsTarget
        tCavitiesActual = pForecastWeight.Parent.Parent.Job.CavitiesActual
        tMaterialPCTarget = pForecastWeight.Parent.MaterialPCTarget.CurrentValue
        if pChannelNum != 100:
            tJobAmount = round(( tUnitsTarget / tCavitiesActual )  *  ( tProductWeight / 1000 )  *  ( tMaterialPCTarget / 100 ), 5)
        else:
            tJobAmount = round(( tUnitsTarget / tCavitiesActual )  *  ( tMaterialPCTarget ), 5)
        tJobAmountLeft = round(tJobAmount - pForecastWeight.Parent.TotalWeight.getCurrentValue(MaterialCalcObjectType.FromJob), 5)
        pForecastWeight.JobAmount = tJobAmount
        pForecastWeight.JobAmountLeft = tJobAmountLeft

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelSplitForecastWeight', 0, error.args[0], 'JobID: ' + str(pJobID) + '. ChannelNum: ' + str(pChannelNum) + '. SplitNum: ' + str(pSplitNum))



def GetChannelSplitMaterialID(pJobID, pMaterialID, pChannelNum, pSplitNum):
    tMaterialID = 0
    tMaterialClassID = 0
    tMPGI = 0.0
    strSQL = ""
    RstCursor = None
    tRefRecipeMaterialID = 0

    try:    
        tMaterialID = MdlADOFunctions.fGetRstValLong(MdlUtilsH.fGetRecipeValueJob(pJobID, 'Material ID', pChannelNum, pSplitNum))
        if tMaterialID != 0:
            pMaterialID.CurrentValue = tMaterialID
            strSQL = 'SELECT CalcInMaterialTotal, IsPConfigSpecialMaterial, MaterialClassID, MaterialGroup FROM TblMaterial WHERE ID = ' + str(tMaterialID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstData:
                pMaterialID.MaterialType = MdlADOFunctions.fGetRstValLong(RstData.MaterialGroup)
                pMaterialID.IsPConfigSpecialMaterial = MdlADOFunctions.fGetRstValBool(RstData.IsPConfigSpecialMaterial, False)
                pMaterialID.CalcInMaterialTotal = MdlADOFunctions.fGetRstValBool(RstData.CalcInMaterialTotal, True)
                tMaterialClassID = MdlADOFunctions.fGetRstValLong(RstData.MaterialClassID)
            if RstCursor:
                RstCursor.close()
            strSQL = 'SELECT IsRawMaterial,IsAdditiveMaterial,IsAccompanyingMaterial FROM STblMaterialGroup WHERE ID = ' + str(pMaterialID.MaterialType)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstData:
                pMaterialID.IsRawMaterial = MdlADOFunctions.fGetRstValBool(RstData.IsRawMaterial, False)
                pMaterialID.IsAdditiveMaterial = MdlADOFunctions.fGetRstValBool(RstData.IsAdditiveMaterial, False)
                pMaterialID.IsAccompanyingMaterial = MdlADOFunctions.fGetRstValBool(RstData.IsAccompanyingMaterial, False)
            if RstCursor:
                RstCursor.close()
            pMaterialID.MaterialClassID = tMaterialClassID
            if tMaterialClassID != 0:
                tMPGI = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('MPGI', 'TblMaterialClass', 'ID = ' + str(tMaterialClassID)))
                pMaterialID.MPGI = tMPGI
            else:
                pMaterialID.MPGI = 1
            
            if (pMaterialID.Parent.Parent.Job.RecipeRefType == 1):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(MdlUtilsH.fGetRecipeValueProduct(pMaterialID.Parent.Parent.Job.Product.ID, 'Material ID', pChannelNum, pSplitNum))
            elif (pMaterialID.Parent.Parent.Job.RecipeRefType == 2):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(MdlUtilsH.fGetRecipeValueJob(pMaterialID.Parent.Parent.Job.RecipeRefJob, 'Material ID', pChannelNum, pSplitNum))
            elif (pMaterialID.Parent.Parent.Job.RecipeRefType == 6):
                tRefRecipeMaterialID = MdlADOFunctions.fGetRstValLong(MdlUtils.fGetRecipeValueStandard(pMaterialID.Parent.Parent.Job.RecipeRefStandardID, 'Material ID', pChannelNum, pSplitNum, pMaterialID.Parent.Parent.Job.Product.ID))
            if tRefRecipeMaterialID != 0:
                pMaterialID.RefRecipeValue = tRefRecipeMaterialID
                strSQL = 'SELECT CalcInMaterialTotal,MaterialClassID FROM TblMaterial WHERE ID = ' + str(tRefRecipeMaterialID)
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()
                
                if RstData:
                    pMaterialID.RefRecipeMaterialClassID = MdlADOFunctions.fGetRstValLong(RstData.MaterialClassID)
                    pMaterialID.RefRecipeCalcInMaterialTotal = MdlADOFunctions.fGetRstValBool(RstData.CalcInMaterialTotal, True)
                if RstCursor:
                    RstCursor.close()
                if pMaterialID.RefRecipeMaterialClassID != 0:
                    strSQL = 'SELECT MPGI FROM TblMaterialClass WHERE ID = ' + str(pMaterialID.RefRecipeMaterialClassID)
                    RstCursor = MdlConnection.CN.cursor()
                    RstCursor.execute(strSQL)
                    RstData = RstCursor.fetchone()
                    
                    if RstData:
                        pMaterialID.RefRecipeMPGI = MdlADOFunctions.fGetRstValDouble(RstData.MPGI)
                    if RstCursor:
                        RstCursor.close()
                else:
                    pMaterialID.RefRecipeMPGI = 1
        RstCursor = None

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelSplitMaterialID', 0, error.args[0], 'JobID: ' + str(pJobID) + '. ChannelNum: ' + str(pChannelNum) + '. SplitNum: ' + str(pSplitNum))


def GetChannelSplitMaterialPC(pJobID, pMaterialPC, pChannelNum, pSplitNum):
    tMaterialPC = 0.0
    try:
        tMaterialPC = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(pJobID, 'MaterialPC', pChannelNum, pSplitNum))
        if tMaterialPC != 0:
            pMaterialPC.CurrentValue = tMaterialPC

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelSplitMaterialPC', 0, error.args[0], 'JobID: ' + str(pJobID) + '. ChannelNum: ' + str(pChannelNum) + '. SplitNum: ' + str(pSplitNum))


def GetChannelSplitMaterialPCTarget(pJobID, pMaterialPCTarget, pChannelNum, pSplitNum):
    tMaterialPCTarget = 0.0
    tProductRecipeMaterialPCTarget = 0.0
    tProductStandardMaterialPCTarget = 0.0
    tRecipeRefMaterialPCTarget = 0.0
    
    try:
        tMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(pJobID, 'MaterialPCTarget', pChannelNum, pSplitNum))
        if tMaterialPCTarget != 0:
            pMaterialPCTarget.CurrentValue = tMaterialPCTarget
        tProductRecipeMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(pMaterialPCTarget.Parent.Parent.Machine.ActiveJob.Product.ID, 'MaterialPCTarget', pChannelNum, pSplitNum))
        if tProductRecipeMaterialPCTarget != 0:
            pMaterialPCTarget.ProductRecipeValue = tProductRecipeMaterialPCTarget
        if pMaterialPCTarget.Parent.Parent.Machine.ActiveJob.RecipeRefStandardID > 0:
            tProductStandardMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(MdlUtils.fGetRecipeValueStandard(pMaterialPCTarget.Parent.Parent.Machine.ActiveJob.RecipeRefStandardID, 'MaterialPCTarget', pChannelNum, pSplitNum, pMaterialPCTarget.Parent.Parent.Machine.ActiveJob.Product.ID))
            if tProductStandardMaterialPCTarget != 0:
                pMaterialPCTarget.ProductStandardValue = tProductStandardMaterialPCTarget
        
        if (pMaterialPCTarget.Parent.Parent.Job.RecipeRefType == 1):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(pMaterialPCTarget.Parent.Parent.Job.Product.ID, 'MaterialPCTarget', pChannelNum, pSplitNum))
        elif (pMaterialPCTarget.Parent.Parent.Job.RecipeRefType == 2):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(pMaterialPCTarget.Parent.Parent.Job.RecipeRefJob, 'MaterialPCTarget', pChannelNum, pSplitNum))
        elif (pMaterialPCTarget.Parent.Parent.Job.RecipeRefType == 6):
            tRecipeRefMaterialPCTarget = MdlADOFunctions.fGetRstValDouble(MdlUtils.fGetRecipeValueStandard(pMaterialPCTarget.Parent.Parent.Job.RecipeRefStandardID, 'MaterialPCTarget', pChannelNum, pSplitNum, pMaterialPCTarget.Parent.Parent.Job.Product.ID))
        if tRecipeRefMaterialPCTarget != 0:
            pMaterialPCTarget.RecipeRefValue = tRecipeRefMaterialPCTarget

    except BaseException as error:
        MdlGlobal.RecordError('GetChannelSplitMaterialPCTarget', 0, error.args[0], 'JobID: ' + str(pJobID) + '. ChannelNum: ' + str(pChannelNum) + '. SplitNum: ' + str(pSplitNum))


def CheckSplitJobMaterialRecord(pSplit):
    strSQL = ""
    RstCursor = None
    strTitle = ""

    try:    
        strSQL = 'SELECT ID FROM TblJobMaterial WHERE Job = ' + str(pSplit.Parent.Job.ID)
        strSQL = strSQL + ' AND ChannelNum = ' + str(pSplit.Parent.ChannelNum)
        strSQL = strSQL + ' AND SplitNum = ' + str(pSplit.SplitNum)
        strSQL = strSQL + ' AND Material = ' + str(pSplit.MaterialID.CurrentValue)
        if not pSplit.MaterialBatch is None:
            strSQL = strSQL + ' AND MaterialBatch = \'' + str(pSplit.MaterialBatch.CurrentValue) + '\''
        RstCursor = MdlConnection.CN.cursor()
        if RstCursor:
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
            if pSplit.MaterialBatch:
                strSQL = strSQL + ',MaterialBatch'
                strSQL = strSQL + ',InventoryID'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + str(pSplit.Parent.Job.ID)
            strSQL = strSQL + ',' + str(pSplit.Parent.ChannelNum)
            strSQL = strSQL + ',' + str(pSplit.SplitNum)
            strSQL = strSQL + ',' + str(pSplit.MaterialID.CurrentValue)
            strSQL = strSQL + ',' + str(pSplit.MaterialID.MaterialType)
            strSQL = strSQL + ',' + str(pSplit.MaterialID.MaterialClassID)
            strSQL = strSQL + ',' + str(pSplit.MaterialPCTarget.CurrentValue)
            strSQL = strSQL + ',' + str(pSplit.MaterialPCTarget.CurrentValue)

            if pSplit.MaterialBatch:
                strSQL = strSQL + ',\'' + str(pSplit.MaterialBatch.CurrentValue) + '\''
                strSQL = strSQL + ',' + str(pSplit.MaterialBatch.ID)
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

    if RstCursor:
        RstCursor.close()
    RstCursor = None


def CheckSplitJoshMaterialRecord(pSplit):
    strSQL = ""
    RstCursor = None
    strTitle = ""

    try:    
        strSQL = 'SELECT ID FROM TblJoshMaterial WHERE JoshID = ' + str(pSplit.Parent.Job.ActiveJosh.ID)
        strSQL = strSQL + ' AND ChannelNum = ' + str(pSplit.Parent.ChannelNum)
        strSQL = strSQL + ' AND SplitNum = ' + str(pSplit.SplitNum)
        strSQL = strSQL + ' AND Material = ' + str(pSplit.MaterialID.CurrentValue)
        if pSplit.MaterialBatch:
            strSQL = strSQL + ' AND MaterialBatch = \'' + str(pSplit.MaterialBatch.CurrentValue) + '\''
        RstCursor = MdlConnection.CN.cursor()
        if RstCursor:
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
            
            if pSplit.MaterialBatch:
                strSQL = strSQL + ',MaterialBatch'
                strSQL = strSQL + ',InventoryID'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + str(pSplit.Parent.Job.ID)
            strSQL = strSQL + ',' + str(pSplit.Parent.Job.ActiveJosh.ID)
            strSQL = strSQL + ',' + str(pSplit.Parent.Job.Product.ID)
            strSQL = strSQL + ',' + str(pSplit.Parent.ChannelNum)
            strSQL = strSQL + ',' + str(pSplit.SplitNum)
            strSQL = strSQL + ',' + str(pSplit.MaterialID.CurrentValue)
            strSQL = strSQL + ',' + str(pSplit.MaterialID.MaterialType)
            strSQL = strSQL + ',' + str(pSplit.MaterialID.MaterialClassID)
            strSQL = strSQL + ',' + str(pSplit.Parent.Job.ActiveJosh.ShiftID)
            strSQL = strSQL + ',' + str(pSplit.Parent.Job.ActiveJosh.ShiftDefID)
            strSQL = strSQL + ',\'' + MdlUtilsH.ShortDate(pSplit.Parent.Job.ActiveJosh.StartTime, True, True, True) + '\''
            strSQL = strSQL + ',' + str(pSplit.Parent.Job.Machine.ID)
            strSQL = strSQL + ',' + str(pSplit.MaterialPCTarget.CurrentValue)
            strSQL = strSQL + ',' + str(pSplit.MaterialPCTarget.CurrentValue)
            
            if pSplit.MaterialBatch:
                strSQL = strSQL + ',\'' + str(pSplit.MaterialBatch.CurrentValue) + '\''
                strSQL = strSQL + ',' + str(pSplit.MaterialBatch.ID)
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

    if RstCursor:
        RstCursor.close()
    RstCursor = None


def GetChannelSplitMaterialBatch(pJobID, pMaterialBatch, pChannelNum, pSplitNum):
    tMaterialBatch = ""
    strSQL = ""
    RstCursor = None
    tInventoryID = 0
    
    try:
        tMaterialBatch = MdlUtilsH.fGetRecipeValueJob(pJobID, 'MaterialBatch', pChannelNum, pSplitNum)
        if tMaterialBatch != '':
            strSQL = 'SELECT ID,Amount,EffectiveAmount,EffectiveOriginalAmount,Weight,GrossWeight,ParentInventoryID FROM TblInventory WHERE Batch = \'' + str(tMaterialBatch) + '\''
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstData:
                tInventoryID = MdlADOFunctions.fGetRstValLong(RstData.ID)
                pMaterialBatch = MdlRTInventory.GetInventoryItemFromGlobalCollection(MdlGlobal.gServer.ActiveInventoryItems, tInventoryID)
                if pMaterialBatch is None:
                    pMaterialBatch = MaterialBatch()
                    pMaterialBatch.ID = tInventoryID
                    pMaterialBatch.CurrentValue = tMaterialBatch
                    pMaterialBatch.EffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveAmount)
                    pMaterialBatch.Amount = MdlADOFunctions.fGetRstValDouble(RstData.Amount)
                    pMaterialBatch.OriginalEffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveOriginalAmount)
                    
                    pMaterialBatch.Weight = MdlADOFunctions.fGetRstValDouble(RstData.Weight)
                    
                    pMaterialBatch.GrossWeight = MdlADOFunctions.fGetRstValDouble(RstData.GrossWeight)
                    
                    pMaterialBatch.ParentInventoryID = MdlADOFunctions.fGetRstValLong(RstData.ParentInventoryID)
                    MdlRTInventory.AddInventoryItemToGlobalCollection(pMaterialBatch)

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('GetChannelSplitMaterialBatch', 0, error.args[0], 'JobID: ' + str(pJobID) + '. ChannelNum: ' + str(pChannelNum) + '. SplitNum: ' + str(pSplitNum))

    if RstCursor:
        RstCursor.close()
    RstCursor = None


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

