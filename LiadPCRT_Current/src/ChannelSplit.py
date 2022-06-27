from GlobalVariables import WareHouseLocationConsumptionMethod
from GlobalVariables import BatchAutoSubtractModeOption
from GlobalVariables import MaterialCalcStandardOption
from GlobalVariables import MaterialCalcObjectType

from MaterialID import MaterialID
from MaterialPC import MaterialPC
from MaterialPCTarget import MaterialPCTarget
from MaterialBatch import MaterialBatch
from TotalWeight import TotalWeight
from ForecastWeight import ForecastWeight

import MdlADOFunctions
import MdlGlobal
import MdlConnection
import MdlChannelSplit
import MdlRTInventory

class ChannelSplit:

    __mParent = None
    __mSplitNum = 0
    __mMaterialID = None
    __mMaterialPC = None
    __mMaterialPCTarget = None
    __mTotalWeight = None
    __mWorkingWithBatchTracking = False
    __mMaterialCalcStandardOption = None
    __mMaterialBatch = None
    __mLastWeightDiff = 0.0
    __mForecastWeight = None
    __mMaterialFlowForNextJob = False
    __mPendingWareHouseLocationLink = False
    __mWareHouseLocationID = 0
    __mActiveInventoryID = 0
    __mActivateBatchFromLocation = False
    __mWareHouseLocationConsumptionMethodID = WareHouseLocationConsumptionMethod
    __mChangeLocationActiveBatchOnActiveJobBatchChange = False
    __mBatchAutoSubtractMode = BatchAutoSubtractModeOption
    __mBatchAutoSubtractValue = 0.0
    __mWorkingWithWarehouseLocation = False

    
    def Init(self, pChannel, pSplitNum, pWorkingWithBatchTracking, pMaterialStandardCalcOption, pJoshID, pWareHouseLocationID, pActivateBatchFromLocation, pWareHouseLocationConsumptionMethod, pChangeLocationActiveBatchOnActiveJobBatchChange, pBatchAutoSubtractMode, pBatchAutoSubtractValue, pWorkingWithWarehouseLocation, pFromActivateJob):
        
        try:
            self.Parent = pChannel
            self.SplitNum = pSplitNum
            self.WorkingWithBatchTracking = pWorkingWithBatchTracking
            if (pMaterialStandardCalcOption == 0):
                self.MaterialCalcStandardOption = MaterialCalcStandardOption.FromInjections
            elif (pMaterialStandardCalcOption == 1):
                self.MaterialCalcStandardOption = MaterialCalcStandardOption.FromUnitsProducedOK
            self.WareHouseLocationID = pWareHouseLocationID
            self.WareHouseLocationConsumptionMethodID = pWareHouseLocationConsumptionMethod
            self.ActivateBatchFromLocation = pActivateBatchFromLocation
            self.WorkingWithWarehouseLocation = pWorkingWithWarehouseLocation
            if self.WorkingWithWarehouseLocation:
                if pFromActivateJob:
                    self.ActivateBatchFromLocation = True
            
            self.__InitMaterialID()
            self.__InitMaterialPC()
            self.__InitMaterialPCTarget()
            self.__InitMaterialBatch()
            self.__InitTotalWeight(pJoshID)
            self.__InitForecastWeight()
            if self.MaterialID.CurrentValue != 0:
                MdlChannelSplit.CheckSplitJobMaterialRecord(self)
                MdlChannelSplit.CheckSplitJoshMaterialRecord(self)
            
            if self.Parent.Job.NextJobMaterialFlowStart != 0:
                self.StartMaterialFlowForNextJob()

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.Init:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))


    def Reset(self, pJoshID):
        try:
            self.InitMaterialID
            self.InitMaterialPC
            self.InitMaterialPCTarget
            self.InitTotalWeight(pJoshID)

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.Reset:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))

        
    def Calc(self, pMaterialCalcObjectType, pJob, pJosh):
        tProductWeightLast = 0.0
        tProductWeightStandard = 0.0
        tNextInventoryID = 0
        tTagName = ''
        tOldInventoryID = 0
        
        if pJob.PConfigID != 0 and  ( ( self.Parent.ChannelNum != 100 and pJob.PConfigIsMaterialCount == False ) or ( self.Parent.ChannelNum == 100 and pJob.PConfigIsChannel100Count == False ) ):
            GoTo(self.Update)
        if pJob.PConfigID != 0 and  ( self.MaterialID.IsPConfigSpecialMaterial == False and pJob.PConfigIsSpecialMaterialCount == True ) :
            GoTo(self.Update)
        
        if pJob.PConfigID != 0 and pJob.MachineType.PConfigSonsRefRecipeSource == FromPConfigParent:
            if not pJob.PConfigParentJob is None:
                tProductWeightLast = pJob.PConfigParentJob.ProductWeightLast *  ( pJob.PConfigPC / 100 )
                tProductWeightStandard = pJob.PConfigParentJob.ProductWeightStandard *  ( pJob.PConfigPC / 100 )
            else:
                tProductWeightLast = pJob.ProductWeightLast *  ( pJob.PConfigPC / 100 )
                tProductWeightStandard = pJob.ProductWeightStandard *  ( pJob.PConfigPC / 100 )
        else:
            tProductWeightLast = pJob.ProductWeightLast
            tProductWeightStandard = pJob.ProductWeightStandard
        if not self.MaterialFlowForNextJob:
            self.CalcAmount(pMaterialCalcObjectType, pJob, tProductWeightLast)
        self.CalcAmountStandard(pMaterialCalcObjectType, pJob, tProductWeightStandard, pJosh)
        self.CalcMaterialActualIndex(pMaterialCalcObjectType)
        self.CalcProductRecipeAmount(pMaterialCalcObjectType, pJob, pJosh)
        self.CalcProductStandardAmount(pMaterialCalcObjectType, pJob, pJosh)
        self.CalcRecipeRefAmount(pMaterialCalcObjectType, pJob, pJosh)
        self.CalcMaterialStandardIndex(pMaterialCalcObjectType, pJob)
        self.CalcMaterialForecast
        self.Update(pMaterialCalcObjectType, pJosh)
        
        if self.WorkingWithWarehouseLocation:
            if self.MaterialBatch is None:
                pJob.Machine.Server.ActivateLocationOnChannelSplit(pJob.MachineID, self.Parent.ChannelNum, self.SplitNum, self.WareHouseLocationID)
            if self.MaterialBatch.EffectiveAmount <= 0 and self.WareHouseLocationID != 0 and self.ActivateBatchFromLocation == True:
                tOldInventoryID = self.MaterialBatch.ID
                tNextInventoryID = self.CheckMaterialRecipeAndLocationMatch
                if tNextInventoryID != 0:
                    self.LoadNextInventoryItem(tNextInventoryID)
                    self.Reset(pJob.ActiveJosh.ID)
                    RemoveBatchFromLocationQueue(self.WareHouseLocationID, tOldInventoryID)
                else:
                    
                    tTagName = 'Cnl' + str(self.Parent.ChannelNum) + 'WrongMissingLocationBatch' + self.SplitNum
                    self.Parent.Job.Machine.SetFieldValue(tTagName, '1')
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.Calc:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    
    def Update(self, pMaterialCalcObjectType, pJosh):
        strSQL = ''

        strTitle = ''

        tParentEffectiveAmount = 0.0

        InventoryStatus = 0

        InventoryEffectiveAmount = 0.0

        Rst = ADODB.Recordset()
        
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            strTitle = 'UPDATE TblJobMaterial'
            strSQL = ' SET'
            strSQL = strSQL + ' Amount = ' + self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandard = ' + Round(self.TotalWeight.StandardValue(pMaterialCalcObjectType), 5)
            strSQL = strSQL + ' ,AmountDiff = ' + self.TotalWeight.AmountDiff(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountDiffPC = ' + Round(self.TotalWeight.AmountDiffPC(pMaterialCalcObjectType), 5)
            strSQL = strSQL + ' ,AmountStandardPC = ' + self.TotalWeight.AmountStandardPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialActualIndex = ' + self.TotalWeight.MaterialActualIndex(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialStandardIndex = ' + self.TotalWeight.MaterialStandardIndex(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialClassID = ' + self.MaterialID.MaterialClassID
            strSQL = strSQL + ' ,AmountProductStandard = ' + self.TotalWeight.ProductRecipeValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountProductStandardPC = ' + self.TotalWeight.AmountProductStandardPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountProductStandardDiff = ' + self.TotalWeight.AmountProductStandardDiff(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountProductStandardDiffPC = ' + self.TotalWeight.AmountProductStandardDiffPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandardStandard = ' + self.TotalWeight.ProductStandardValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandardStandardPC = ' + self.TotalWeight.AmountStandardStandardPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandardStandardDiff = ' + self.TotalWeight.AmountStandardStandardDiff(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandardStandardDiffPC = ' + self.TotalWeight.AmountStandardStandardDiffPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,RecipeRefAmount = ' + self.TotalWeight.RecipeRefValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MPGI = ' + self.MaterialID.MPGI
            strSQL = strSQL + ' ,RefRecipeMPGI = ' + self.MaterialID.RefRecipeMPGI
            strSQL = strSQL + ' ,MaterialFlowAmount = ' + self.TotalWeight.MaterialFlowAmount(pMaterialCalcObjectType)
            strSQL = strSQL + ' WHERE Job = ' + self.Parent.Job.ID
            strSQL = strSQL + ' AND ChannelNum = ' + self.Parent.ChannelNum
            strSQL = strSQL + ' AND SplitNum = ' + self.SplitNum
            strSQL = strSQL + ' AND Material = ' + self.MaterialID.CurrentValue
            if not self.MaterialBatch is None:
                strSQL = strSQL + ' AND MaterialBatch = \'' + self.MaterialBatch.CurrentValue + '\''
            CN.Execute(strTitle + strSQL)
            if self.Parent.Job.Status == 10:
                strTitle = 'UPDATE TblJobCurrentMaterial'
                CN.Execute(strTitle + strSQL)
            strTitle = 'UPDATE TblJobMaterialForecast'
            strSQL = ' SET '
            strSQL = strSQL + ' Amount = ' + self.ForecastWeight.JobAmountLeft
            strSQL = strSQL + ' WHERE Job = ' + self.Parent.Job.ID
            strSQL = strSQL + ' AND ChannelNum = ' + self.Parent.ChannelNum
            strSQL = strSQL + ' AND SplitNum = ' + self.SplitNum
            CN.Execute(strTitle + strSQL)
        if pMaterialCalcObjectType == FromJosh:
            strTitle = 'UPDATE TblJoshMaterial'
            strSQL = ' SET'
            strSQL = strSQL + ' Amount = ' + self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandard = ' + Round(self.TotalWeight.StandardValue(pMaterialCalcObjectType), 5)
            strSQL = strSQL + ' ,AmountDiff = ' + self.TotalWeight.AmountDiff(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountDiffPC = ' + Round(self.TotalWeight.AmountDiffPC(pMaterialCalcObjectType), 5)
            strSQL = strSQL + ' ,AmountStandardPC = ' + self.TotalWeight.AmountStandardPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,JobAmount = ' + self.TotalWeight.CurrentValue(MaterialCalcObjectType.MaterialCalcObjectType.FromJob)
            strSQL = strSQL + ' ,MaterialActualIndex = ' + self.TotalWeight.MaterialActualIndex(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialStandardIndex = ' + self.TotalWeight.MaterialStandardIndex(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialClassID = ' + self.MaterialID.MaterialClassID
            strSQL = strSQL + ' ,AmountProductStandard = ' + self.TotalWeight.ProductRecipeValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountProductStandardPC = ' + self.TotalWeight.AmountProductStandardPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountProductStandardDiff = ' + self.TotalWeight.AmountProductStandardDiff(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountProductStandardDiffPC = ' + self.TotalWeight.AmountProductStandardDiffPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandardStandard = ' + self.TotalWeight.ProductStandardValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandardStandardPC = ' + self.TotalWeight.AmountStandardStandardPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandardStandardDiff = ' + self.TotalWeight.AmountStandardStandardDiff(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandardStandardDiffPC = ' + self.TotalWeight.AmountStandardStandardDiffPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,RecipeRefAmount = ' + self.TotalWeight.RecipeRefValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MPGI = ' + self.MaterialID.MPGI
            strSQL = strSQL + ' ,RefRecipeMPGI = ' + self.MaterialID.RefRecipeMPGI
            strSQL = strSQL + ' ,MaterialFlowAmount = ' + self.TotalWeight.MaterialFlowAmount(pMaterialCalcObjectType)
            strSQL = strSQL + ' WHERE JoshID = ' + pJosh.ID
            strSQL = strSQL + ' AND ChannelNum = ' + self.Parent.ChannelNum
            strSQL = strSQL + ' AND SplitNum = ' + self.SplitNum
            strSQL = strSQL + ' AND Material = ' + self.MaterialID.CurrentValue
            if not self.MaterialBatch is None:
                strSQL = strSQL + ' AND MaterialBatch = \'' + self.MaterialBatch.CurrentValue + '\''
            CN.Execute(strTitle + strSQL)
            if pJosh.Status == 10:
                strTitle = 'UPDATE TblJoshCurrentMaterial'
                CN.Execute(strTitle + strSQL)
        if not self.MaterialBatch is None:
            InventoryStatus = 0
            InventoryEffectiveAmount = 0
            strSQL = 'SELECT ID, Status, EffectiveAmount FROM TblInventory WHERE ID = ' + self.MaterialBatch.ID
            Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            Rst.ActiveConnection = None
            if Rst.RecordCount == 1:
                InventoryStatus = fGetRstValLong(Rst.Fields("Status").Value)
                InventoryEffectiveAmount = fGetRstValDouble(Rst.Fields("EffectiveAmount").Value)
                strSQL = 'UPDATE TblInventory'
                strSQL = strSQL + ' SET '
                strSQL = strSQL + ' EffectiveAmount = ' + self.MaterialBatch.EffectiveAmount
                if self.MaterialBatch.EffectiveAmount <= 0:
                    strSQL = strSQL + ' ,Amount = 0'
                    strSQL = strSQL + ' ,WareHouseID = 2000'
                    strSQL = strSQL + ' ,Status = 2'
                
                strSQL = strSQL + ' ,Weight = ' + self.MaterialBatch.Weight
                
                strSQL = strSQL + ' ,GrossWeight = ' + self.MaterialBatch.GrossWeight
                strSQL = strSQL + ' WHERE Batch = \'' + self.MaterialBatch.CurrentValue + '\''
                CN.Execute(strSQL)
                
                if InventoryStatus != 2 and InventoryEffectiveAmount > 0:
                    
                    if self.MaterialBatch.EffectiveAmount <= 0:
                        AddInventoryHistoryRecord(self.MaterialBatch.ID, 7)
                
                
                if self.MaterialBatch.EffectiveAmount <= 0:
                    strSQL = 'UPDATE TblInventory SET EffectiveAmount = 0, Amount = 0, WareHouseID = 2000, Status = 2 WHERE ParentInventoryID = ' + self.MaterialBatch.ID
                    CN.Execute(strSQL)
            Rst.Close()
            
            
            if self.MaterialBatch.ParentInventoryID != 0:
                tParentEffectiveAmount = fGetRstValDouble(GetSingleValue('SUM(EffectiveAmount)', 'TblInventory', 'ParentInventoryID = ' + self.MaterialBatch.ParentInventoryID, 'CN'))
                if tParentEffectiveAmount <= 0:
                    strSQL = 'UPDATE TblInventory SET Amount = 0, WareHouseID = 2000, Status = 2 WHERE ID = ' + self.MaterialBatch.ParentInventoryID
                    CN.Execute(strSQL)
                    
                    if self.MaterialBatch.EffectiveAmount <= 0:
                        AddInventoryHistoryRecord(self.MaterialBatch.ParentInventoryID, 7)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.Update:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()
            
        strTitle = ''
        strSQL = ''

    
    def __InitMaterialID(self):
        tControllerFieldName = ''
        tControllerField = None
        tMaterialID = None

        try:
            tMaterialID = MaterialID()
            tMaterialID.Parent = self
            tControllerFieldName = MdlChannelSplit.GetSplitControllerFieldName(self.Parent.ChannelNum, self.SplitNum,  MdlChannelSplit.ControllerFieldNameType.MaterialID)
            if self.Parent.Machine.GetParam(tControllerFieldName, tControllerField) == True:
                tMaterialID.ControllerField = tControllerField
            MdlChannelSplit.GetChannelSplitMaterialID(self.Parent.Job.ID, tMaterialID, self.Parent.ChannelNum, self.SplitNum)
            self.MaterialID = tMaterialID

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMaterialID:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))

        tControllerField = None
        tMaterialID = None

    def __InitMaterialPC(self):
        ControllerFieldName = ''
        tMaterialPC = None
        tParam = None

        try:
            tMaterialPC = MaterialPC()
            tMaterialPC.Parent = self
            ControllerFieldName = MdlChannelSplit.GetSplitControllerFieldName(self.Parent.ChannelNum, self.SplitNum, MdlChannelSplit.ControllerFieldNameType.MaterialPC)
            if self.Parent.Machine.GetParam(ControllerFieldName, tParam) == True:
                tMaterialPC.ControllerField = tParam
            MdlChannelSplit.GetChannelSplitMaterialPC(self.Parent.Job.ID, tMaterialPC, self.Parent.ChannelNum, self.SplitNum)
            self.MaterialPC = tMaterialPC

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMaterialPC:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))

        tMaterialPC = None
        tParam = None

    def __InitMaterialPCTarget(self):
        ControllerFieldName = ''
        tMaterialPCTarget = None
        tParam = None

        try:
            tMaterialPCTarget = MaterialPCTarget()
            tMaterialPCTarget.Parent = self
            ControllerFieldName = MdlChannelSplit.GetSplitControllerFieldName(self.Parent.ChannelNum, self.SplitNum, MdlChannelSplit.ControllerFieldNameType.MaterialPCTarget)
            if self.Parent.Machine.GetParam(ControllerFieldName, tParam) == True:
                tMaterialPCTarget.ControllerField = tParam
            MdlChannelSplit.GetChannelSplitMaterialPCTarget(self.Parent.Job.ID, tMaterialPCTarget, self.Parent.ChannelNum, self.SplitNum)
            self.MaterialPCTarget = tMaterialPCTarget

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMaterialPCTarget:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))

        tParam = None
        tMaterialPCTarget = None

    def __InitTotalWeight(self, pJoshID):
        tTotalWeight = None
        tParam = None
        ControllerFieldName = ''
        tMaterialBatch = ''

        try:
            tTotalWeight = TotalWeight()
            tTotalWeight.Parent = self
            ControllerFieldName = MdlChannelSplit.GetSplitControllerFieldName(self.Parent.ChannelNum, self.SplitNum, MdlChannelSplit.ControllerFieldNameType.TotalWeight)
            if self.Parent.Machine.GetParam(ControllerFieldName, tParam) == True:
                tTotalWeight.ControllerField = tParam
            if not self.MaterialBatch is None:
                tMaterialBatch = self.MaterialBatch.CurrentValue
            else:
                tMaterialBatch = ''
            MdlChannelSplit.GetChannelSplitTotalWeight(self.Parent.Job.ID, pJoshID, tTotalWeight, self.Parent.ChannelNum, self.SplitNum, self.MaterialID.CurrentValue, tMaterialBatch)
            self.TotalWeight = tTotalWeight

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.InitTotalWeight:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))

        tTotalWeight = None
        tParam = None

    def __InitMaterialBatch(self):
        tMaterialBatch = None

        try:
            MdlChannelSplit.GetChannelSplitMaterialBatch(self.Parent.Job.ID, tMaterialBatch, self.Parent.ChannelNum, self.SplitNum)
            if not tMaterialBatch is None:
                tMaterialBatch.Parent = self
                if tMaterialBatch.CurrentValue != '':
                    self.MaterialBatch = tMaterialBatch
                    self.ActiveInventoryID = tMaterialBatch.ID
                    MdlRTInventory.AddInventoryItemToGlobalCollection(tMaterialBatch)

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMaterialBatch:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))

        tMaterialBatch = None

    def __InitForecastWeight(self):
        tForecastWeight = None

        try:
            tForecastWeight = ForecastWeight()
            tForecastWeight.Parent = self
            MdlChannelSplit.GetChannelSplitForecastWeight(self.Parent.Job.ID, tForecastWeight, self.Parent.ChannelNum, self.SplitNum)
            self.ForecastWeight = tForecastWeight

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.InitForecastWeight:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
        tForecastWeight = None

    def __CalcMaterialForecast(self):
        
        self.ForecastWeight.JobAmountLeft = self.ForecastWeight.JobAmount - self.TotalWeight.CurrentValue(MaterialCalcObjectType.FromJob)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcMaterialForecast:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    def ValidateAmount(self, pTimeDiff, pMaterialCalcObjectType):
        tMaximumAmount = 0.0

        strSQL = ''

        strTitle = ''
        
        if not self.TotalWeight.ControllerField is None:
            if self.TotalWeight.ControllerField.ValidateValue == True:
                tMaximumAmount = pTimeDiff * self.TotalWeight.ControllerField.MaxValueUnitsPerMin
                if not self.MaterialBatch is None:
                    pass
                else:
                    if self.TotalWeight.CurrentValue(pMaterialCalcObjectType) > tMaximumAmount:
                        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                            strTitle = 'UPDATE TblJobMaterial'
                            strSQL = strSQL + ' SET '
                            strSQL = strSQL + ' InvalidAmount = ' + self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
                            strSQL = strSQL + ' WHERE '
                            strSQL = strSQL + ' Job = ' + self.Parent.Job.ID
                            strSQL = strSQL + ' AND ChannelNum = ' + self.Parent.ChannelNum
                            strSQL = strSQL + ' AND SplitNum = ' + self.SplitNum
                            strSQL = strSQL + ' AND Material = ' + self.MaterialID.CurrentValue
                            CN.Execute(strTitle + strSQL)
                            if self.Parent.Job.Status == 10:
                                strTitle = 'UPDATE TblJobCurrentMaterial'
                                CN.Execute(strTitle + strSQL)
                        else:
                            strTitle = 'UPDATE TblJoshMaterial'
                            strSQL = strSQL + ' SET '
                            strSQL = strSQL + ' InvalidAmount = ' + self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
                            strSQL = strSQL + ' WHERE '
                            strSQL = strSQL + ' JoshID = ' + self.Parent.Job.ActiveJosh.ID
                            strSQL = strSQL + ' AND ChannelNum = ' + self.Parent.ChannelNum
                            strSQL = strSQL + ' AND SplitNum = ' + self.SplitNum
                            strSQL = strSQL + ' AND Material = ' + self.MaterialID.CurrentValue
                            CN.Execute(strTitle + strSQL)
                            if self.Parent.Job.ActiveJosh.Status == 10:
                                strTitle = 'UPDATE TblJoshCurrentMaterial'
                                CN.Execute(strTitle + strSQL)
                        self.Parent.Job.PrintRecordToHistory(310, 'C' + str(self.Parent.ChannelNum) + 'S' + self.SplitNum, CStr(self.TotalWeight.CurrentValue(pMaterialCalcObjectType)), CStr(self.TotalWeight.StandardValue(pMaterialCalcObjectType)))
                        self.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, self.TotalWeight.StandardValue(pMaterialCalcObjectType))
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.ValidateAmount:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    def CalcMaterialActualIndex(self, pMaterialCalcObjectType):
        
        self.TotalWeight.SetMaterialActualIndex(pMaterialCalcObjectType, self.MaterialID.MPGI * self.TotalWeight.CurrentValue(pMaterialCalcObjectType))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcMaterialActualIndex:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    
    def CalcAmount(self, pMaterialCalcObjectType, pJob, pProductWeightLast):
        tWeightDiff = 0.0

        tInventoryPart = 0.0
        
        
        if self.Parent.Job.Machine.DSIsActive == True and not self.TotalWeight.ControllerField is None:
            if fGetRstValBool(self.TotalWeight.ControllerField.DirectRead, False) == False:
                GoTo(CalcWeightDiff)
            
            if self.TotalWeight.ControllerField.Quality == 0 and self.TotalWeight.ControllerField.CitectDeviceType == 1:
                
                return
            
            
            if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                
                
                tWeightDiff = fGetRstValDouble(self.TotalWeight.ControllerField.LastValidValue) - fGetRstValDouble(self.TotalWeight.ControllerField.PrevValidValue)
                self.LastWeightDiff = tWeightDiff
            else:
                tWeightDiff = self.LastWeightDiff
                self.LastWeightDiff = 0
            if ( tWeightDiff > 0 and self.Parent.Machine.IsOffline == False )  or self.Parent.Machine.IsOffline == True:
                self.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, self.TotalWeight.CurrentValue(pMaterialCalcObjectType) +  ( self.Parent.Job.PConfigPC / 100 * tWeightDiff ))
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    if not self.MaterialBatch is None:
                        
                        
                        if self.MaterialBatch.EffectiveAmount != 0:
                            tInventoryPart = Round(tWeightDiff / self.MaterialBatch.EffectiveAmount, 5)
                            self.MaterialBatch.Weight = ( 1 - tInventoryPart )  * self.MaterialBatch.Weight
                            
                            self.MaterialBatch.GrossWeight = ( 1 - tInventoryPart )  * self.MaterialBatch.GrossWeight
                        self.MaterialBatch.EffectiveAmount = self.MaterialBatch.EffectiveAmount - tWeightDiff
        else:
            if self.Parent.ChannelNum != 100:
                tWeightDiff = pJob.InjectionsDiff *  ( pProductWeightLast / 1000 )  *  ( self.MaterialPCTarget.CurrentValue / 100 )
            else:
                
                if self.Parent.Machine.CalcChannel100MaterialByCavity == True:
                    tWeightDiff = pJob.InjectionsDiff * self.MaterialPCTarget.CurrentValue * pJob.CavitiesActual
                else:
                    tWeightDiff = pJob.InjectionsDiff * self.MaterialPCTarget.CurrentValue
            if ( tWeightDiff > 0 and self.Parent.Machine.IsOffline == False )  or self.Parent.Machine.IsOffline == True:
                self.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, self.TotalWeight.CurrentValue(pMaterialCalcObjectType) + tWeightDiff)
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    if not self.MaterialBatch is None:
                        
                        
                        if self.MaterialBatch.EffectiveAmount != 0:
                            tInventoryPart = Round(tWeightDiff / self.MaterialBatch.EffectiveAmount, 5)
                            self.MaterialBatch.Weight = ( 1 - tInventoryPart )  * self.MaterialBatch.Weight
                            
                            self.MaterialBatch.GrossWeight = ( 1 - tInventoryPart )  * self.MaterialBatch.GrossWeight
                        self.MaterialBatch.EffectiveAmount = self.MaterialBatch.EffectiveAmount - tWeightDiff
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcAmount:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    
    
    def CalcAmountStandard(self, pMaterialCalcObjectType, pJob, pProductWeightStandard, pJosh):
        tInjectionsCount = 0.0

        tUnitsProducedOK = 0.0
        
        if self.Parent.ChannelNum != 100:
            if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount
                self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( ( ( self.MaterialPCTarget.CurrentValue / 100 )  *  ( tInjectionsCount )  * pProductWeightStandard )  / 1000 )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType))
            elif self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromUnitsProducedOK:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tUnitsProducedOK = pJob.UnitsProducedOK
                else:
                    tUnitsProducedOK = pJosh.UnitsProducedOK
                self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( ( ( self.MaterialPCTarget.CurrentValue / 100 )  * tUnitsProducedOK *  ( pProductWeightStandard / pJob.CavitiesActual ) )  / 1000 )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType))
        else:
            if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount
                if self.Parent.Machine.CalcChannel100MaterialByCavity == True:
                    self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( pJob.CavitiesActual * self.MaterialPCTarget.CurrentValue * tInjectionsCount )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType))
                else:
                    self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.CurrentValue * tInjectionsCount )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType))
            elif self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromUnitsProducedOK:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tUnitsProducedOK = pJob.UnitsProducedOK
                else:
                    tUnitsProducedOK = pJosh.UnitsProducedOK
                self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.CurrentValue * tUnitsProducedOK )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcAmountStandard:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    
    
    def CalcProductRecipeAmount(self, pMaterialCalcObjectType, pJob, pJosh):
        tInjectionsCount = 0.0
        
        
        if self.Parent.ChannelNum != 100:
            if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
            else:
                tInjectionsCount = pJosh.InjectionsCount - pJosh.InjectionsCountStart
            self.TotalWeight.SetProductRecipeValue(pMaterialCalcObjectType, ( pJob.PConfigPC / 100 )  *  ( self.MaterialPCTarget.ProductRecipeValue / 100 )  *  ( pJob.ProductRecipeWeight / 1000 )  *  ( tInjectionsCount ))
        else:
            if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
            else:
                tInjectionsCount = pJosh.InjectionsCount - pJosh.InjectionsCountStart
            self.TotalWeight.SetProductRecipeValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.ProductRecipeValue / 100 )  *  ( tInjectionsCount ))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcProductRecipeAmount:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    
    
    def CalcProductStandardAmount(self, pMaterialCalcObjectType, pJob, pJosh):
        tInjectionsCount = 0.0
        
        
        if pJob.RecipeRefStandardID > 0:
            if self.Parent.ChannelNum != 100:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount - pJosh.InjectionsCountStart
                self.TotalWeight.SetProductStandardValue(pMaterialCalcObjectType, ( pJob.PConfigPC / 100 )  *  ( self.MaterialPCTarget.ProductStandardValue / 100 )  *  ( self.Parent.Machine.ActiveJob.ProductStandardRecipeWeight / 1000 )  *  ( tInjectionsCount ))
            else:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount - pJosh.InjectionsCountStart
                self.TotalWeight.SetProductStandardValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.ProductStandardValue / 100 )  *  ( tInjectionsCount ))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcProductStandardAmount:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    
    
    def CalcRecipeRefAmount(self, pMaterialCalcObjectType, pJob, pJosh):
        tInjectionsCount = 0.0

        tUnitsProducedOK = 0.0
        
        
        if self.Parent.ChannelNum != 100:
            if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount
                self.TotalWeight.SetRecipeRefValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.RecipeRefValue / 100 )  *  ( pJob.RefRecipeProductWeight / 1000 )  * tInjectionsCount)
            else:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tUnitsProducedOK = pJob.UnitsProducedOK
                else:
                    tUnitsProducedOK = pJosh.UnitsProducedOK
                self.TotalWeight.SetRecipeRefValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.RecipeRefValue / 100 )  *  ( pJob.RefRecipeUnitWeight / 1000 )  * tUnitsProducedOK)
        else:
            if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount
                self.TotalWeight.SetRecipeRefValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.RecipeRefValue )  * tInjectionsCount)
            else:
                if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
                    tUnitsProducedOK = pJob.UnitsProducedOK
                else:
                    tUnitsProducedOK = pJob.ActiveJosh.UnitsProducedOK
                self.TotalWeight.SetRecipeRefValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.RecipeRefValue )  * tUnitsProducedOK)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcRecipeRefAmount:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    
    def CalcMaterialStandardIndex(self, pMaterialCalcObjectType, pJob):
        
        
        if pJob.Machine.Server.SystemVariables.TotalEquipmentMaterialEfficencyOption == JobRecipe:
            self.TotalWeight.SetMaterialStandardIndex(pMaterialCalcObjectType, self.MaterialID.MPGI * self.TotalWeight.StandardValue(pMaterialCalcObjectType))
        else:
            self.TotalWeight.SetMaterialStandardIndex(pMaterialCalcObjectType, self.MaterialID.RefRecipeMPGI * self.TotalWeight.RecipeRefValue(pMaterialCalcObjectType))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcMaterialStandardIndex:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()

    def StartMaterialFlowForNextJob(self):
        try:
            self.MaterialFlowForNextJob = True
        except:
            pass

    def CheckMaterialRecipeAndLocationMatch(self):
        returnVal = None
        strSQL = ''

        Rst = ADODB.Recordset()

        tMaterialID = 0

        tAllowUsingMaterialSubst = False
        
        returnVal = 0
        if self.Parent.Job.Status == 10:
            if self.WareHouseLocationID != 0:
                strSQL = 'SELECT TOP 1 *' + vbCrLf
                strSQL = strSQL + 'FROM ViewRTLocationQueueMatch' + vbCrLf
                strSQL = strSQL + 'WHERE LocationID = ' + self.WareHouseLocationID + vbCrLf
                strSQL = strSQL + '     AND InventoryID <> ' + self.ActiveInventoryID + vbCrLf
                strSQL = strSQL + 'ORDER BY Sequence'
                Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                Rst.ActiveConnection = None
                if Rst.RecordCount == 1:
                    tAllowUsingMaterialSubst = fGetRstValBool(Rst.Fields("AllowUsingMaterialSubst").Value, False)
                    tMaterialID = fGetRstValLong(Rst.Fields("MaterialID").Value)
                    
                    if CheckRecipeChannelSplitVSLocationMatch(self, self.Parent.Job.Machine.ControllerID, tMaterialID) == True:
                        returnVal = fGetRstValLong(Rst.Fields("InventoryID").Value)
                    else:
                        if tAllowUsingMaterialSubst:
                            if CheckForMaterialSubstitute(fGetRstValLong(self.MaterialID.CurrentValue), tMaterialID):
                                returnVal = fGetRstValLong(Rst.Fields("InventoryID").Value)
                Rst.Close()
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.CheckMaterialRecipeAndLocationMatch:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()
        Rst = None
        return returnVal

    def LoadNextInventoryItem(self, pInventoryItem):
        strSQL = ''

        Rst = ADODB.Recordset()

        tMaterialBatch = self.MaterialBatch()

        tBatchTagName = ''
        
        
        if self.Parent.Job.Status == 10:
            if self.WareHouseLocationID != 0:
                
                tMaterialBatch = GetInventoryItemFromGlobalCollection(gServer.ActiveInventoryItems, pInventoryItem)
                if tMaterialBatch is None:
                    strSQL = 'SELECT ID,Batch,Amount,EffectiveAmount,EffectiveOriginalAmount FROM TblInventory WHERE ID = ' + pInventoryItem
                    Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                    Rst.ActiveConnection = None
                    if Rst.RecordCount == 1:
                        tMaterialBatch = self.MaterialBatch()
                        tMaterialBatch.ID = fGetRstValLong(Rst.Fields("ID").Value)
                        tMaterialBatch.CurrentValue = fGetRstValString(Rst.Fields("Batch").Value)
                        tMaterialBatch.Amount = fGetRstValDouble(Rst.Fields("Amount").Value)
                        tMaterialBatch.EffectiveAmount = fGetRstValDouble(Rst.Fields("EffectiveAmount").Value)
                        tMaterialBatch.OriginalEffectiveAmount = fGetRstValDouble(Rst.Fields("EffectiveOriginalAmount").Value)
                    Rst.Close()
                    AddInventoryItemToGlobalCollection(tMaterialBatch)
                if not tMaterialBatch is None:
                    self.MaterialBatch = tMaterialBatch
                    
                    CheckSplitJobMaterialRecord(self)
                    CheckSplitJoshMaterialRecord(self)
                    
                    tBatchTagName = 'Cnl' + str(self.Parent.ChannelNum) + 'MainMatBatch' + self.SplitNum
                    self.Parent.Job.Machine.SetFieldValue(tBatchTagName, self.MaterialBatch.CurrentValue)
                    
                    self.ActiveInventoryID = pInventoryItem
                    
                    strSQL = 'UPDATE TblControllerChannelsSplits' + vbCrLf
                    strSQL = strSQL + 'SET ActiveInventoryID = ' + self.ActiveInventoryID + vbCrLf
                    strSQL = strSQL + 'WHERE ControllerID = ' + self.Parent.Machine.ControllerID + ' AND ChannelNum = ' + str(self.Parent.ChannelNum) + ' AND SplitNum = ' + self.SplitNum
                    CN.Execute(strSQL)
                    UpdateJobRecipeFromBatchChange(self.Parent.Job, self.Parent.ChannelNum, self.SplitNum, tMaterialBatch)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.GetNextInventoryItem:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()
        Rst = None

    def AddSetupFromLocationBatchChange(self):
        returnVal = None
        tAmount = 0.0

        tValue = 0.0
        
        if self.Parent.Job.Machine.LocationBatchChangeSetupModeID != 0:
            if (self.Parent.Job.Machine.LocationBatchChangeSetupModeID == 1):
                tValue = self.Parent.Job.Machine.LocationBatchChangeSetupValue
                tAmount = tValue
            elif (self.Parent.Job.Machine.LocationBatchChangeSetupModeID == 2):
                tValue = self.Parent.Job.Machine.LocationBatchChangeSetupValue
                tAmount = ( tValue / 100 )  * self.MaterialBatch.EffectiveAmount
            elif (self.Parent.Job.Machine.LocationBatchChangeSetupModeID == 3):
                tValue = fGetRstValDouble(fGetRecipeValueJob(self.Parent.Job.ID, 'LocationBatchChangeSetupValue', self.Parent.ChannelNum, 0))
                tAmount = tValue
            elif (self.Parent.Job.Machine.LocationBatchChangeSetupModeID == 4):
                tValue = fGetRstValDouble(fGetRecipeValueJob(self.Parent.Job.ID, 'LocationBatchChangeSetupValue', self.Parent.ChannelNum, 0))
                tAmount = ( tValue / 100 )  * self.MaterialBatch.EffectiveAmount
            elif (self.Parent.Job.Machine.LocationBatchChangeSetupModeID == 5):
                tValue = fGetRstValDouble(fGetRecipeValueJob(self.Parent.Job.ID, 'LocationBatchChangeSetupValue', self.Parent.ChannelNum, self.SplitNum))
                tAmount = tValue
            elif (self.Parent.Job.Machine.LocationBatchChangeSetupModeID == 6):
                tValue = fGetRstValDouble(fGetRecipeValueJob(self.Parent.Job.ID, 'LocationBatchChangeSetupValue', self.Parent.ChannelNum, self.SplitNum))
                tAmount = ( tValue / 100 )  * self.MaterialBatch.EffectiveAmount
            if tAmount > 0:
                self.Parent.Job.AddRejects(tAmount, 0, 100, False)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.AddSetupFromLocationBatchChange:', str(0), error.args[0], 'JobID:' + str(self.Parent.Job.ID) + '. ChannelNum: ' + str(self.Parent.ChannelNum) + '. SplitNum:  ' + str(self.SplitNum))
            Err.Clear()
        return returnVal

    def PerformActivationForLocationBatch(self):
        tInventoryID = 0

        tAmount = 0.0
        
        if self.ActivateBatchFromLocation == False:
            self.ActivateBatchFromLocation = True
        tInventoryID = self.CheckMaterialRecipeAndLocationMatch()
        if tInventoryID != 0:
            
            if CheckBatchAutoSubtract(self.BatchAutoSubtractMode, self.BatchAutoSubtractValue, self.MaterialBatch):
                SubtractInventoryItem(self.MaterialBatch)
            self.LoadNextInventoryItem(tInventoryID)
        if Err.Number != 0:
            Err.Clear()

    def SetWareHouseLocationID(self, pWareHouseLocationID):
        
        self.WareHouseLocationID = pWareHouseLocationID
        if Err.Number != 0:
            Err.Clear()

    def __del__(self):
        
        self.__mParent = None
        self.__mMaterialID = None
        self.__mMaterialPC = None
        self.__mMaterialPCTarget = None
        self.__mTotalWeight = None
        self.__mMaterialBatch = None
        self.__mForecastWeight = None
        Debug.Print('Split Destroy' + self.__mSplitNum)


    def setParent(self, value):
        self.__mParent = value

    def getParent(self):
        returnVal = None
        returnVal = self.__mParent
        return returnVal
    Parent = property(fset=setParent, fget=getParent)


    def setMaterialID(self, value):
        self.__mMaterialID = value

    def getMaterialID(self):
        returnVal = None
        returnVal = self.__mMaterialID
        return returnVal
    MaterialID = property(fset=setMaterialID, fget=getMaterialID)


    def setMaterialPC(self, value):
        self.__mMaterialPC = value

    def getMaterialPC(self):
        returnVal = None
        returnVal = self.__mMaterialPC
        return returnVal
    MaterialPC = property(fset=setMaterialPC, fget=getMaterialPC)


    def setMaterialPCTarget(self, value):
        self.__mMaterialPCTarget = value

    def getMaterialPCTarget(self):
        returnVal = None
        returnVal = self.__mMaterialPCTarget
        return returnVal
    MaterialPCTarget = property(fset=setMaterialPCTarget, fget=getMaterialPCTarget)


    def setTotalWeight(self, value):
        self.__mTotalWeight = value

    def getTotalWeight(self):
        returnVal = None
        returnVal = self.__mTotalWeight
        return returnVal
    TotalWeight = property(fset=setTotalWeight, fget=getTotalWeight)


    def setWorkingWithBatchTracking(self, value):
        self.__mWorkingWithBatchTracking = value

    def getWorkingWithBatchTracking(self):
        returnVal = None
        returnVal = self.__mWorkingWithBatchTracking
        return returnVal
    WorkingWithBatchTracking = property(fset=setWorkingWithBatchTracking, fget=getWorkingWithBatchTracking)


    def setSplitNum(self, value):
        self.__mSplitNum = value

    def getSplitNum(self):
        returnVal = None
        returnVal = self.__mSplitNum
        return returnVal
    SplitNum = property(fset=setSplitNum, fget=getSplitNum)


    def setMaterialCalcStandardOption(self, value):
        self.__mMaterialCalcStandardOption = value

    def getMaterialCalcStandardOption(self):
        returnVal = None
        returnVal = self.__mMaterialCalcStandardOption
        return returnVal
    MaterialCalcStandardOption = property(fset=setMaterialCalcStandardOption, fget=getMaterialCalcStandardOption)


    def setMaterialBatch(self, value):
        self.__mMaterialBatch = value

    def getMaterialBatch(self):
        returnVal = None
        returnVal = self.__mMaterialBatch
        return returnVal
    MaterialBatch = property(fset=setMaterialBatch, fget=getMaterialBatch)


    def setLastWeightDiff(self, value):
        self.__mLastWeightDiff = value

    def getLastWeightDiff(self):
        returnVal = None
        returnVal = self.__mLastWeightDiff
        return returnVal
    LastWeightDiff = property(fset=setLastWeightDiff, fget=getLastWeightDiff)


    def setForecastWeight(self, value):
        self.__mForecastWeight = value

    def getForecastWeight(self):
        returnVal = None
        returnVal = self.__mForecastWeight
        return returnVal
    ForecastWeight = property(fset=setForecastWeight, fget=getForecastWeight)


    def setMaterialFlowForNextJob(self, value):
        self.__mMaterialFlowForNextJob = value

    def getMaterialFlowForNextJob(self):
        returnVal = None
        returnVal = self.__mMaterialFlowForNextJob
        return returnVal
    MaterialFlowForNextJob = property(fset=setMaterialFlowForNextJob, fget=getMaterialFlowForNextJob)


    def setPendingWareHouseLocationLink(self, value):
        self.__mPendingWareHouseLocationLink = value

    def getPendingWareHouseLocationLink(self):
        returnVal = None
        returnVal = self.__mPendingWareHouseLocationLink
        return returnVal
    PendingWareHouseLocationLink = property(fset=setPendingWareHouseLocationLink, fget=getPendingWareHouseLocationLink)


    def setWareHouseLocationID(self, value):
        self.__mWareHouseLocationID = value

    def getWareHouseLocationID(self):
        returnVal = None
        returnVal = self.__mWareHouseLocationID
        return returnVal
    WareHouseLocationID = property(fset=setWareHouseLocationID, fget=getWareHouseLocationID)


    def setActiveInventoryID(self, value):
        self.__mActiveInventoryID = value

    def getActiveInventoryID(self):
        returnVal = None
        returnVal = self.__mActiveInventoryID
        return returnVal
    ActiveInventoryID = property(fset=setActiveInventoryID, fget=getActiveInventoryID)


    def setActivateBatchFromLocation(self, value):
        self.__mActivateBatchFromLocation = value

    def getActivateBatchFromLocation(self):
        returnVal = None
        returnVal = self.__mActivateBatchFromLocation
        return returnVal
    ActivateBatchFromLocation = property(fset=setActivateBatchFromLocation, fget=getActivateBatchFromLocation)


    def setWareHouseLocationConsumptionMethodID(self, value):
        self.__mWareHouseLocationConsumptionMethodID = value

    def getWareHouseLocationConsumptionMethodID(self):
        returnVal = None
        returnVal = self.__mWareHouseLocationConsumptionMethodID
        return returnVal
    WareHouseLocationConsumptionMethodID = property(fset=setWareHouseLocationConsumptionMethodID, fget=getWareHouseLocationConsumptionMethodID)


    def setChangeLocationActiveBatchOnActiveJobBatchChange(self, value):
        self.__mChangeLocationActiveBatchOnActiveJobBatchChange = value

    def getChangeLocationActiveBatchOnActiveJobBatchChange(self):
        returnVal = None
        returnVal = self.__mChangeLocationActiveBatchOnActiveJobBatchChange
        return returnVal
    ChangeLocationActiveBatchOnActiveJobBatchChange = property(fset=setChangeLocationActiveBatchOnActiveJobBatchChange, fget=getChangeLocationActiveBatchOnActiveJobBatchChange)


    def setBatchAutoSubtractMode(self, value):
        self.__mBatchAutoSubtractMode = value

    def getBatchAutoSubtractMode(self):
        returnVal = None
        returnVal = self.__mBatchAutoSubtractMode
        return returnVal
    BatchAutoSubtractMode = property(fset=setBatchAutoSubtractMode, fget=getBatchAutoSubtractMode)


    def setBatchAutoSubtractValue(self, value):
        self.__mBatchAutoSubtractValue = value

    def getBatchAutoSubtractValue(self):
        returnVal = None
        returnVal = self.__mBatchAutoSubtractValue
        return returnVal
    BatchAutoSubtractValue = property(fset=setBatchAutoSubtractValue, fget=getBatchAutoSubtractValue)


    def setWorkingWithWarehouseLocation(self, value):
        self.__mWorkingWithWarehouseLocation = value

    def getWorkingWithWarehouseLocation(self):
        returnVal = None
        returnVal = self.__mWorkingWithWarehouseLocation
        return returnVal
    WorkingWithWarehouseLocation = property(fset=setWorkingWithWarehouseLocation, fget=getWorkingWithWarehouseLocation)

    
