from colorama import Fore
from ChannelSplit import ChannelSplit
from GlobalVariables import MaterialCalcStandardOption
from GlobalVariables import WareHouseLocationConsumptionMethod
from GlobalVariables import BatchAutoSubtractModeOption

import MdlADOFunctions
import MdlConnection
import MdlGlobal
import MdlChannel

# class MaterialCalcObjectType(enum.Enum):
#     FromJob = 0
#     FromJosh = 1

# class MaterialCalcStandardOption(enum.Enum):
#     FromUnitsProducedOK = 0
#     FromInjections = 1

# class WareHouseLocationConsumptionMethod(enum.Enum):
#     FIFO = 1
#     LIFO = 2

# class BatchAutoSubtractModeOption(enum.Enum):
#     off = 0
#     ByMinimumPercent = 1
#     ByMinimumAmount = 2


class Channel:
    __mID = 0
    __mSplits = {}
    __mSplitsCount = 0
    __mChannelNum = 0
    __mIsMain = False
    __mSplitDefinitionsFromTable = False
    __mWorkingWithBatchTracking = False
    __mLastReadTime = None
    __mLastWriteTime = None
    __mMachine = None
    __mMaterialID = None
    __mMaterialPCTarget = None
    __mMaterialPC = None
    __mTotalWeight = None
    __mMaterialCalcStandardOption = None
    __mJob = None
    __mMaterialBatch = None
    __mLastWeightDiff = 0
    __mForecastWeight = None
    __mMaterialFlowForNextJob = False
    __mPendingWareHouseLocationLink = False
    __mWareHouseLocationID = 0
    __mActiveInventoryID = 0
    __mActivateBatchFromLocation = False
    __mWareHouseLocationConsumptionMethodID = None
    __mChangeLocationActiveBatchOnActiveJobBatchChange = False
    __mBatchAutoSubtractMode = None
    __mBatchAutoSubtractValue = 0
    __mWorkingWithWarehouseLocation = False

    
    def Init(self, pMachine, pChannelID, pJob, pJoshID, pFromActivateJob):
        i = 0
        strSQL = ""
        RstCursor = None
        splitsRstCursor = None
        tSplit = None

        try:
            strSQL = 'SELECT *' + '\n'
            strSQL = strSQL + 'FROM ViewRTControllerChannels' + '\n'
            strSQL = strSQL + ' WHERE ID = ' + str(pChannelID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.ID = MdlADOFunctions.fGetRstValLong(RstData.ID)
                self.Machine = pMachine
                self.Job = pJob
                self.ChannelNum = MdlADOFunctions.fGetRstValLong(RstData.ChannelNum)
                self.IsMain = MdlADOFunctions.fGetRstValBool(RstData.IsMain, False)
                self.WorkingWithBatchTracking = MdlADOFunctions.fGetRstValBool(RstData.WorkingWithBatchTracking, False)
                self.SplitDefinitionsFromTable = MdlADOFunctions.fGetRstValBool(RstData.SplitDefinitionsFromTable, False)
                self.SplitsCounter = MdlADOFunctions.fGetRstValLong(RstData.ChannelSplits)
                self.WareHouseLocationID = MdlADOFunctions.fGetRstValLong(RstData.WareHouseLocationID)
                if self.WareHouseLocationID != 0:
                    self.WareHouseLocationConsumptionMethodID = MdlADOFunctions.fGetRstValLong(RstData.ConsumptionMethodID)
                self.ActivateBatchFromLocation = MdlADOFunctions.fGetRstValBool(RstData.ActivateBatchFromLocation, False)
                self.ChangeLocationActiveBatchOnActiveJobBatchChange = MdlADOFunctions.fGetRstValBool(RstData.ChangeLocationActiveBatchOnActiveJobBatchChange, False)
                self.BatchAutoSubtractMode = MdlADOFunctions.fGetRstValLong(RstData.BatchAutoSubtractModeID)
                self.BatchAutoSubtractValue = MdlADOFunctions.fGetRstValDouble(RstData.BatchAutoSubtractValue)
                self.WorkingWithWarehouseLocation = MdlADOFunctions.fGetRstValBool(RstData.WorkingWithWarehouseLocation, False)
                if self.WorkingWithWarehouseLocation:
                    if pFromActivateJob:
                        self.ActivateBatchFromLocation = True
                select_0 = MdlADOFunctions.fGetRstValLong(RstData.MaterialStandardCalcOption)
                if (select_0 == 0):
                    self.MaterialCalcStandardOption = MaterialCalcStandardOption.FromInjections
                elif (select_0 == 1):
                    self.MaterialCalcStandardOption = MaterialCalcStandardOption.FromUnitsProducedOK

                if self.SplitsCounter > 0:
                    if self.SplitDefinitionsFromTable == True:
                        strSQL = 'SELECT *' + '\n'
                        strSQL = strSQL + ' FROM ViewRTControllerChannelSplits'
                        strSQL = strSQL + ' WHERE ControllerID = ' + str(self.Machine.ControllerID) + ' AND ChannelNum = ' + str(self.ChannelNum)
                        splitsRstCursor = MdlConnection.CN.cursor()
                        splitsRstCursor.execute(strSQL)
                        splitsRstValues = splitsRstCursor.fetchall()
                        
                        for splitsRstData in splitsRstValues:
                            tSplit = ChannelSplit()
                            tSplit.Init(self. MdlADOFunctions.fGetRstValLong(splitsRstData.SplitNum), MdlADOFunctions.fGetRstValBool(splitsRstData.WorkingWithBatchTracking, False), MdlADOFunctions.fGetRstValLong(splitsRstData.MaterialStandardCalcOption), pJoshID, MdlADOFunctions.fGetRstValLong(splitsRstData.WareHouseLocationID), MdlADOFunctions.fGetRstValBool(splitsRstData.ActivateBatchFromLocation, False), MdlADOFunctions.fGetRstValLong(splitsRstData.ConsumptionMethodID), MdlADOFunctions.fGetRstValBool(splitsRstData.ChangeLocationActiveBatchOnActiveJobBatchChange, False), MdlADOFunctions.fGetRstValLong(splitsRstData.BatchAutoSubtractModeID), MdlADOFunctions.fGetRstValDouble(splitsRstData.BatchAutoSubtractValue), MdlADOFunctions.fGetRstValBool(splitsRstData.WorkingWithWarehouseLocation, False), pFromActivateJob)
                            self.Splits[MdlADOFunctions.fGetRstValString(splitsRstData.SplitNum)] = tSplit
                        splitsRstCursor.close()
                    else:
                        for i in range(1, self.SplitsCounter):
                            tSplit = ChannelSplit()
                            tSplit.Init(self, int(i), self.WorkingWithBatchTracking, MdlADOFunctions.fGetRstValLong(RstData.MaterialStandardCalcOption), pJoshID, 0, True, WareHouseLocationConsumptionMethod.FIFO, False, BatchAutoSubtractModeOption.off, 0, False, pFromActivateJob)
                            self.Splits[str(i)] = tSplit
                else:
                    self.__InitMaterialID()
                    self.__InitMaterialPC()
                    self.__InitMaterialPCTarget()
                    self.__InitMaterialBatch()
                    self.__InitTotalWeight(pJoshID)
                    self.__InitForecastWeight()
                    
                    if self.MaterialPCTarget.CurrentValue != 0 and self.MaterialPC.CurrentValue == 0:
                        self.MaterialPC.CurrentValue = self.MaterialPCTarget.CurrentValue
                    if self.MaterialID.CurrentValue != 0:
                        MdlChannel.CheckChannelJobMaterialRecord(self)
                        MdlChannel.CheckChannelJoshMaterialRecord(self)
            
            RstCursor.close()
            
            if self.Job.NextJobMaterialFlowStart != 0:
                self.MaterialFlowForNextJob = True

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.Init:', str(0), error.args[0], 'JobID:' + str(pJob.ID) + '. ChannelNum: ' + str(self.ChannelNum))

        RstCursor = None
        splitsRstCursor = None
        tSplit = None


    def Reset(self, pJoshID):
        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                tSplit.Reset(pJoshID)
        else:
            self.InitMaterialID
            self.InitMaterialPC
            self.InitMaterialPCTarget
            self.InitTotalWeight(pJoshID)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.Reset:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None


    def ResetJoshCounters(self):
        tVariant = Variant()

        tSplit = None
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                tSplit.TotalWeight.SetCurrentValue(FromJosh, 0)
                tSplit.TotalWeight.SetStandardValue(FromJosh, 0)
                tSplit.TotalWeight.SetProductRecipeValue(FromJosh, 0)
                tSplit.TotalWeight.SetProductStandardValue(FromJosh, 0)
                tSplit.TotalWeight.SetMaterialActualIndex(FromJosh, 0)
                tSplit.TotalWeight.SetOtherMaterialsActualIndex(FromJosh, 0)
                tSplit.TotalWeight.SetOtherMaterialsAmount(FromJosh, 0)
                tSplit.TotalWeight.SetOtherMaterialsAmountStandard(FromJosh, 0)
                tSplit.TotalWeight.SetMaterialFlowAmount(FromJosh, 0)
        else:
            self.TotalWeight.SetCurrentValue(FromJosh, 0)
            self.TotalWeight.SetStandardValue(FromJosh, 0)
            self.TotalWeight.SetProductRecipeValue(FromJosh, 0)
            self.TotalWeight.SetProductStandardValue(FromJosh, 0)
            self.TotalWeight.SetMaterialActualIndex(FromJosh, 0)
            self.TotalWeight.SetOtherMaterialsActualIndex(FromJosh, 0)
            self.TotalWeight.SetOtherMaterialsAmount(FromJosh, 0)
            self.TotalWeight.SetOtherMaterialsAmountStandard(FromJosh, 0)
            self.TotalWeight.SetMaterialFlowAmount(FromJosh, 0)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.ResetJoshCounters:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None

    
    
    def Calc(self, pMaterialCalcObjectType, pJob, pJosh):
        tSplit = None
        tVariant = Variant()
        tProductWeightLast = 0
        tProductWeightStandard = 0
        tNextInventoryID = 0
        tTagName = ""
        tOldInventoryID = 0
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                
                tSplit.Calc(pMaterialCalcObjectType, pJob, pJosh)
        else:
            
            if pJob.PConfigID != 0 and  ( ( pJob.PConfigIsMaterialCount == False and self.ChannelNum != 100 ) or ( pJob.PConfigIsChannel100Count == False and self.ChannelNum == 100 ) ):
                GoTo(self.Update)
            if pJob.PConfigID != 0 and  ( pJob.PConfigIsSpecialMaterialCount == True and self.MaterialID.IsPConfigSpecialMaterial == False ) :
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
            self.CalcMaterialStandardIndex(pMaterialCalcObjectType)
            self.CalcMaterialForecast
            self.Update(pMaterialCalcObjectType, pJosh)
            
            if self.WorkingWithWarehouseLocation:
                if self.MaterialBatch is None:
                    pJob.Machine.Server.ActivateLocationOnChannelSplit(pJob.MachineID, self.ChannelNum, 0, self.WareHouseLocationID)
                if self.MaterialBatch.EffectiveAmount <= 0 and self.WareHouseLocationID != 0 and self.ActivateBatchFromLocation == True:
                    tOldInventoryID = self.MaterialBatch.ID
                    tNextInventoryID = self.CheckMaterialRecipeAndLocationMatch
                    if tNextInventoryID != 0:
                        self.LoadNextInventoryItem(tNextInventoryID)
                        self.Reset(pJob.ActiveJosh.ID)
                    else:
                        
                        tTagName = 'Cnl' + self.ChannelNum + 'WrongMissingLocationBatch'
                        self.Job.Machine.SetFieldValue(tTagName, '1')
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.Calc:', str(0), error.args[0], 'JobID:' + str(pJob.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
            
        tSplit = None
        tVariant = None

    
    def Update(self, pMaterialCalcObjectType, pJosh):
        strSQL = ""

        strTitle = ""

        tParentEffectiveAmount = 0

        InventoryStatus = 0

        InventoryEffectiveAmount = 0

        RstCursor = None
        
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            strTitle = 'UPDATE TblJobMaterial'
            strSQL = ' SET '
            strSQL = strSQL + ' Amount = ' + self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandard = ' + Round(self.TotalWeight.StandardValue(pMaterialCalcObjectType), 5)
            strSQL = strSQL + ' ,AmountDiff = ' + self.TotalWeight.AmountDiff(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountDiffPC = ' + Round(self.TotalWeight.AmountDiffPC(pMaterialCalcObjectType), 5)
            strSQL = strSQL + ' ,AmountStandardPC = ' + self.TotalWeight.AmountStandardPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialClassID = ' + self.MaterialID.MaterialClassID
            strSQL = strSQL + ' ,MaterialActualIndex = ' + self.TotalWeight.MaterialActualIndex(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialStandardIndex = ' + self.TotalWeight.MaterialStandardIndex(pMaterialCalcObjectType)
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
            strSQL = strSQL + ' WHERE Job = ' + self.Job.ID
            strSQL = strSQL + ' AND ChannelNum = ' + self.ChannelNum
            strSQL = strSQL + ' AND SplitNum =  0'
            strSQL = strSQL + ' AND Material = ' + self.MaterialID.CurrentValue
            if not self.MaterialBatch is None:
                strSQL = strSQL + ' AND MaterialBatch = \'' + self.MaterialBatch.CurrentValue + '\''
            CN.Execute(strTitle + strSQL)
            if self.Job.Status == 10:
                strTitle = 'UPDATE TblJobCurrentMaterial'
                CN.Execute(strTitle + strSQL)
            strTitle = 'UPDATE TblJobMaterialForecast'
            strSQL = ' SET '
            strSQL = strSQL + ' Amount = ' + self.ForecastWeight.JobAmountLeft
            strSQL = strSQL + ' WHERE Job = ' + self.Job.ID
            strSQL = strSQL + ' AND ChannelNum = ' + self.ChannelNum
            strSQL = strSQL + ' AND SplitNum = 0'
            CN.Execute(strTitle + strSQL)
            if not self.TotalWeight.ControllerField is None:
                if self.TotalWeight.ControllerField.DirectRead == False:
                    self.TotalWeight.ControllerField.LastValue = self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
        if pMaterialCalcObjectType == FromJosh:
            strTitle = 'UPDATE TblJoshMaterial'
            strSQL = strSQL + ' SET '
            strSQL = strSQL + ' Amount = ' + self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountStandard = ' + Round(self.TotalWeight.StandardValue(pMaterialCalcObjectType), 5)
            strSQL = strSQL + ' ,AmountDiff = ' + self.TotalWeight.AmountDiff(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,AmountDiffPC = ' + Round(self.TotalWeight.AmountDiffPC(pMaterialCalcObjectType), 5)
            strSQL = strSQL + ' ,AmountStandardPC = ' + self.TotalWeight.AmountStandardPC(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialClassID = ' + self.MaterialID.MaterialClassID
            strSQL = strSQL + ' ,MaterialActualIndex = ' + self.TotalWeight.MaterialActualIndex(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,MaterialStandardIndex = ' + self.TotalWeight.MaterialStandardIndex(pMaterialCalcObjectType)
            strSQL = strSQL + ' ,JobAmount = ' + self.TotalWeight.CurrentValue(MaterialCalcObjectType.FromJob)
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
            strSQL = strSQL + ' AND ChannelNum = ' + self.ChannelNum
            strSQL = strSQL + ' AND SplitNum =  0'
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
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstData:
                InventoryStatus = MdlADOFunctions.fGetRstValLong(RstData.Status)
                InventoryEffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveAmount)
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
            RstCursor.close()
            
            if self.MaterialBatch.ParentInventoryID != 0:
                tParentEffectiveAmount = MdlADOFunctions.fGetRstValDouble(GetSingleValue('SUM(EffectiveAmount)', 'TblInventory', 'ParentInventoryID = ' + self.MaterialBatch.ParentInventoryID, 'CN'))
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
                
            MdlGlobal.RecordError(type(self).__name__ + '.Update:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        strTitle = vbNullString
        strSQL = vbNullString

    def __InitMaterialID(self):
        tControllerField = ControlParam()

        tControllerFieldName = ""

        tMaterialID = self.MaterialID()
        
        tMaterialID = self.MaterialID()
        tMaterialID.Parent = Me
        tControllerFieldName = GetChannelControllerFieldName(self.ChannelNum, ControllerFieldNameType.MaterialID)
        if self.Machine.GetParam(tControllerFieldName, tControllerField) == True:
            tMaterialID.ControllerField = tControllerField
        GetChannelMaterialID(self.Job.ID, tMaterialID, self.ChannelNum)
        self.MaterialID = tMaterialID
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMaterialID:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tControllerField = None
        tMaterialID = None

    def __InitMaterialPC(self):
        tControllerField = ControlParam()

        tControllerFieldName = ""

        tMaterialPC = self.MaterialPC()
        
        tMaterialPC = self.MaterialPC()
        tMaterialPC.Parent = Me
        tControllerFieldName = GetChannelControllerFieldName(self.ChannelNum, ControllerFieldNameType.MaterialPC)
        if self.Machine.GetParam(tControllerFieldName, tControllerField) == True:
            tMaterialPC.ControllerField = tControllerField
        GetChannelMaterialPC(self.Job.ID, tMaterialPC, self.ChannelNum)
        self.MaterialPC = tMaterialPC
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMaterialPC:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tControllerField = None
        tMaterialPC = None

    def __InitMaterialPCTarget(self):
        tControllerField = ControlParam()

        tControllerFieldName = ""

        tMaterialPCTarget = self.MaterialPCTarget()
        
        tMaterialPCTarget = self.MaterialPCTarget()
        tMaterialPCTarget.Parent = Me
        tControllerFieldName = GetChannelControllerFieldName(self.ChannelNum, ControllerFieldNameType.MaterialPCTarget)
        if self.Machine.GetParam(tControllerFieldName, tControllerField) == True:
            tMaterialPCTarget.ControllerField = tControllerField
        GetChannelMaterialPCTarget(self.Job.ID, tMaterialPCTarget, self.ChannelNum)
        self.MaterialPCTarget = tMaterialPCTarget
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMaterialPCTarget:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tControllerField = None
        tMaterialPCTarget = None

    def __InitTotalWeight(self, pJoshID):
        tControllerField = ControlParam()

        tControllerFieldName = ""

        tTotalWeight = self.TotalWeight()

        tMaterialBatch = ""
        
        tTotalWeight = self.TotalWeight()
        tTotalWeight.Parent = Me
        tControllerFieldName = GetChannelControllerFieldName(self.ChannelNum, ControllerFieldNameType.TotalWeight)
        if self.Machine.GetParam(tControllerFieldName, tControllerField) == True:
            tTotalWeight.ControllerField = tControllerField
        if not self.MaterialBatch is None:
            tMaterialBatch = self.MaterialBatch.CurrentValue
        else:
            tMaterialBatch = ''
        GetChannelTotalWeight(self.Job.ID, pJoshID, tTotalWeight, self.ChannelNum, self.MaterialID.CurrentValue, tMaterialBatch)
        self.TotalWeight = tTotalWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.InitTotalWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tControllerField = None
        tTotalWeight = None

    def GetTotalWeight(self, pMaterialCalcObjectType):
        returnVal = None
        tTotalWeight = 0

        tVariant = Variant()

        tSplit = None
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True:
                    tTotalWeight = tTotalWeight + tSplit.TotalWeight.CurrentValue(pMaterialCalcObjectType) + tSplit.TotalWeight.OtherMaterialsAmount(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True:
                tTotalWeight = self.TotalWeight.CurrentValue(pMaterialCalcObjectType) + self.TotalWeight.OtherMaterialsAmount(pMaterialCalcObjectType)
        returnVal = tTotalWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetTotalWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetMaterialPCTarget(self):
        returnVal = None
        tMaterialPCTarget = 0

        tVariant = Variant()

        tSplit = None
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                tMaterialPCTarget = tMaterialPCTarget + tSplit.MaterialPCTarget.CurrentValue
        else:
            tMaterialPCTarget = self.MaterialPCTarget.CurrentValue
        returnVal = tMaterialPCTarget
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetMaterialPCTarget:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetTotalWeightStandard(self, pMaterialCalcObjectType):
        returnVal = None
        tTotalWeightStandard = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True:
                    tTotalWeightStandard = tTotalWeightStandard + tSplit.TotalWeight.StandardValue(pMaterialCalcObjectType) + tSplit.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True:
                tTotalWeightStandard = self.TotalWeight.StandardValue(pMaterialCalcObjectType) + self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType)
        returnVal = tTotalWeightStandard
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetTotalWeightStandard:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetMaterialActualIndex(self, pMaterialCalcObjectType):
        returnVal = None
        tMaterialActualIndex = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True:
                    tMaterialActualIndex = tMaterialActualIndex +  ( tSplit.TotalWeight.MaterialActualIndex(pMaterialCalcObjectType) + tSplit.TotalWeight.OtherMaterialsActualIndex(pMaterialCalcObjectType) )
        else:
            if self.MaterialID.CalcInMaterialTotal == True:
                tMaterialActualIndex = self.TotalWeight.MaterialActualIndex(pMaterialCalcObjectType) + self.TotalWeight.OtherMaterialsActualIndex(pMaterialCalcObjectType)
        returnVal = tMaterialActualIndex
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetMaterialActualIndex:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def __InitMaterialBatch(self):
        tMaterialBatch = self.MaterialBatch()
        
        
        
        GetChannelMaterialBatch(self.Job.ID, tMaterialBatch, self.ChannelNum)
        if not tMaterialBatch is None:
            tMaterialBatch.Parent = Me
            if tMaterialBatch.CurrentValue != '':
                self.MaterialBatch = tMaterialBatch
                
                
                self.ActiveInventoryID = tMaterialBatch.ID
                AddInventoryItemToGlobalCollection(tMaterialBatch)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMaterialBatch:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tMaterialBatch = None

    def __InitForecastWeight(self):
        tForecastWeight = self.ForecastWeight()
        
        tForecastWeight = self.ForecastWeight()
        tForecastWeight.Parent = Me
        GetChannelForecastWeight(self.Job.ID, tForecastWeight, self.ChannelNum)
        self.ForecastWeight = tForecastWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.InitForecastWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tForecastWeight = None

    def __CalcMaterialForecast(self):
        try:
            self.ForecastWeight.JobAmountLeft = self.ForecastWeight.JobAmount - self.TotalWeight.CurrentValue(FromJob)

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcMaterialForecast:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum) + '. SplitNum: 0.')

    def GetMaterialStandardIndex(self, pMaterialCalcObjectType):
        returnVal = None
        tMaterialStandardIndex = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True:
                    tMaterialStandardIndex = tMaterialStandardIndex + tSplit.TotalWeight.MaterialStandardIndex(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True:
                tMaterialStandardIndex = self.TotalWeight.MaterialStandardIndex(pMaterialCalcObjectType)
        returnVal = tMaterialStandardIndex
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetMaterialStandardIndex:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetRawMaterialTotalWeight(self, pMaterialCalcObjectType):
        returnVal = None
        tTotalWeight = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True and tSplit.MaterialID.IsRawMaterial == True:
                    tTotalWeight = tTotalWeight + tSplit.TotalWeight.CurrentValue(pMaterialCalcObjectType) + tSplit.TotalWeight.OtherMaterialsAmount(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True and self.MaterialID.IsRawMaterial == True:
                tTotalWeight = self.TotalWeight.CurrentValue(pMaterialCalcObjectType) + self.TotalWeight.OtherMaterialsAmount(pMaterialCalcObjectType)
        returnVal = tTotalWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetRawMaterialTotalWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetAdditiveMaterialTotalWeight(self, pMaterialCalcObjectType):
        returnVal = None
        tTotalWeight = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True and tSplit.MaterialID.IsAdditiveMaterial == True:
                    tTotalWeight = tTotalWeight + tSplit.TotalWeight.CurrentValue(pMaterialCalcObjectType) + tSplit.TotalWeight.OtherMaterialsAmount(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True and self.MaterialID.IsAdditiveMaterial == True:
                tTotalWeight = self.TotalWeight.CurrentValue(pMaterialCalcObjectType) + self.TotalWeight.OtherMaterialsAmount(pMaterialCalcObjectType)
        returnVal = tTotalWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetAdditiveMaterialTotalWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetAccompanyingMaterialTotalWeight(self, pMaterialCalcObjectType):
        returnVal = None
        tTotalWeight = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True and tSplit.MaterialID.IsAccompanyingMaterial == True:
                    tTotalWeight = tTotalWeight + tSplit.TotalWeight.CurrentValue(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True and self.MaterialID.IsAccompanyingMaterial == True:
                tTotalWeight = self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
        returnVal = tTotalWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetAccompanyingMaterialTotalWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetRawMaterialStandardWeight(self, pMaterialCalcObjectType):
        returnVal = None
        tTotalWeight = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True and tSplit.MaterialID.IsRawMaterial == True:
                    tTotalWeight = tTotalWeight + tSplit.TotalWeight.StandardValue(pMaterialCalcObjectType) + tSplit.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True and self.MaterialID.IsRawMaterial == True:
                tTotalWeight = self.TotalWeight.StandardValue(pMaterialCalcObjectType) + self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType)
        returnVal = tTotalWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetRawMaterialStandardWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetAdditiveMaterialStandardWeight(self, pMaterialCalcObjectType):
        returnVal = None
        tTotalWeight = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True and tSplit.MaterialID.IsAdditiveMaterial == True:
                    tTotalWeight = tTotalWeight + tSplit.TotalWeight.StandardValue(pMaterialCalcObjectType) + tSplit.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True and self.MaterialID.IsAdditiveMaterial == True:
                tTotalWeight = self.TotalWeight.StandardValue(pMaterialCalcObjectType) + self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType)
        returnVal = tTotalWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetAdditiveMaterialStandardWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetAccompanyingMaterialStandardWeight(self, pMaterialCalcObjectType):
        returnVal = None
        tTotalWeight = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.CalcInMaterialTotal == True and tSplit.MaterialID.IsAccompanyingMaterial == True:
                    tTotalWeight = tTotalWeight + tSplit.TotalWeight.StandardValue(pMaterialCalcObjectType) + tSplit.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType)
        else:
            if self.MaterialID.CalcInMaterialTotal == True and self.MaterialID.IsAccompanyingMaterial == True:
                tTotalWeight = self.TotalWeight.StandardValue(pMaterialCalcObjectType) + self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType)
        returnVal = tTotalWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetAccompanyingMaterialStandardWeight:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetRawMaterialPCTarget(self):
        returnVal = None
        tMaterialPCTarget = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.IsRawMaterial == True:
                    tMaterialPCTarget = tMaterialPCTarget + tSplit.MaterialPCTarget.CurrentValue
        else:
            if self.MaterialID.IsRawMaterial == True:
                tMaterialPCTarget = self.MaterialPCTarget.CurrentValue
        returnVal = tMaterialPCTarget
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetRawMaterialPCTarget:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetAdditiveMaterialPCTarget(self):
        returnVal = None
        tMaterialPCTarget = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.IsAdditiveMaterial == True:
                    tMaterialPCTarget = tMaterialPCTarget + tSplit.MaterialPCTarget.CurrentValue
        else:
            if self.MaterialID.IsAdditiveMaterial == True:
                tMaterialPCTarget = self.MaterialPCTarget.CurrentValue
        returnVal = tMaterialPCTarget
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetAdditiveMaterialPCTarget:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def GetAccompanyingMaterialPCTarget(self):
        returnVal = None
        tMaterialPCTarget = 0

        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                if tSplit.MaterialID.IsAccompanyingMaterial == True:
                    tMaterialPCTarget = tMaterialPCTarget + tSplit.MaterialPCTarget.CurrentValue
        else:
            if self.MaterialID.IsAccompanyingMaterial == True:
                tMaterialPCTarget = self.MaterialPCTarget.CurrentValue
        returnVal = tMaterialPCTarget
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetAccompanyingMaterialPCTarget:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None
        return returnVal

    def ValidateAmount(self, pTimeDiff, pMaterialCalcObjectType):
        tMaximumAmount = 0

        strSQL = ""

        strTitle = ""

        tVariant = Variant()

        tChannelSplit = ChannelSplit()
        
        if self.SplitsCounter == 0:
            if not self.TotalWeight.ControllerField is None:
                if self.TotalWeight.ControllerField.ValidateValue == True:
                    tMaximumAmount = pTimeDiff * self.TotalWeight.ControllerField.MaxValueUnitsPerMin
                    if not self.MaterialBatch is None:
                        pass
                    else:
                        if self.TotalWeight.CurrentValue(pMaterialCalcObjectType) > tMaximumAmount:
                            if pMaterialCalcObjectType == FromJob:
                                strTitle = 'UPDATE TblJobMaterial'
                                strSQL = strSQL + ' SET '
                                strSQL = strSQL + ' InvalidAmount = ' + self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
                                strSQL = strSQL + ' WHERE '
                                strSQL = strSQL + ' Job = ' + self.Job.ID
                                strSQL = strSQL + ' AND ChannelNum = ' + self.ChannelNum
                                strSQL = strSQL + ' AND SplitNum = 0'
                                strSQL = strSQL + ' AND Material = ' + self.MaterialID.CurrentValue
                                CN.Execute(strTitle + strSQL)
                                if self.Job.Status == 10:
                                    strTitle = 'UPDATE TblJobCurrentMaterial'
                                    CN.Execute(strTitle + strSQL)
                            else:
                                strTitle = 'UPDATE TblJoshMaterial'
                                strSQL = strSQL + ' SET '
                                strSQL = strSQL + ' InvalidAmount = ' + self.TotalWeight.CurrentValue(pMaterialCalcObjectType)
                                strSQL = strSQL + ' WHERE '
                                strSQL = strSQL + ' JoshID = ' + self.Job.ActiveJosh.ID
                                strSQL = strSQL + ' AND ChannelNum = ' + self.ChannelNum
                                strSQL = strSQL + ' AND SplitNum = 0'
                                strSQL = strSQL + ' AND Material = ' + self.MaterialID.CurrentValue
                                CN.Execute(strTitle + strSQL)
                                if self.Job.ActiveJosh.Status == 10:
                                    strTitle = 'UPDATE TblJoshCurrentMaterial'
                                    CN.Execute(strTitle + strSQL)
                            self.Job.PrintRecordToHistory(310, 'C' + self.ChannelNum + 'S0', str(self.TotalWeight.CurrentValue(pMaterialCalcObjectType)), str(self.TotalWeight.StandardValue(pMaterialCalcObjectType)))
                            self.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, self.TotalWeight.StandardValue(pMaterialCalcObjectType))
        else:
            for tVariant in self.Splits:
                tChannelSplit = tVariant
                tChannelSplit.ValidateAmount(pTimeDiff, pMaterialCalcObjectType)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.ValidateAmount:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tChannelSplit = None

    def CalcMaterialActualIndex(self, pMaterialCalcObjectType):
        tVariant = Variant()

        tSplit = ChannelSplit()
        
        if self.SplitsCounter > 0:
            for tVariant in self.Splits:
                tSplit = tVariant
                tSplit.CalcMaterialActualIndex(pMaterialCalcObjectType)
        else:
            self.TotalWeight.SetMaterialActualIndex(pMaterialCalcObjectType, self.MaterialID.MPGI * self.TotalWeight.CurrentValue(pMaterialCalcObjectType))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcMaterialActualIndex:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        tVariant = None
        tSplit = None

    
    def CalcAmount(self, pMaterialCalcObjectType, pJob, pProductWeightLast):
        tWeightDiff = 0

        tInventoryPart = 0
        
        
        
        if self.Job.Machine.DSIsActive == True and not self.TotalWeight.ControllerField is None:
            if MdlADOFunctions.fGetRstValBool(self.TotalWeight.ControllerField.DirectRead, False) == False:
                GoTo(CalcWeightDiff)
            
            if self.TotalWeight.ControllerField.Quality == 0 and self.TotalWeight.ControllerField.CitectDeviceType == 1:
                
                return
            
            
            if pMaterialCalcObjectType == FromJob:
                
                
                tWeightDiff = MdlADOFunctions.fGetRstValDouble(self.TotalWeight.ControllerField.LastValidValue) - MdlADOFunctions.fGetRstValDouble(self.TotalWeight.ControllerField.PrevValidValue)
                self.LastWeightDiff = tWeightDiff
            else:
                tWeightDiff = self.LastWeightDiff
                self.LastWeightDiff = 0
            if ( tWeightDiff > 0 and self.Machine.IsOffline == False )  or self.Machine.IsOffline == True:
                self.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, self.TotalWeight.CurrentValue(pMaterialCalcObjectType) +  ( pJob.PConfigPC / 100 * tWeightDiff ))
                if pMaterialCalcObjectType == FromJob:
                    if not self.MaterialBatch is None:
                        
                        
                        if self.MaterialBatch.EffectiveAmount != 0:
                            tInventoryPart = Round(tWeightDiff / self.MaterialBatch.EffectiveAmount, 5)
                            self.MaterialBatch.Weight = ( 1 - tInventoryPart )  * self.MaterialBatch.Weight
                            
                            self.MaterialBatch.GrossWeight = ( 1 - tInventoryPart )  * self.MaterialBatch.GrossWeight
                        self.MaterialBatch.EffectiveAmount = self.MaterialBatch.EffectiveAmount - tWeightDiff
        else:
            if self.ChannelNum != 100:
                tWeightDiff = pJob.InjectionsDiff *  ( pProductWeightLast / 1000 )  *  ( self.MaterialPCTarget.CurrentValue / 100 )
            else:
                tWeightDiff = pJob.InjectionsDiff * self.MaterialPCTarget.CurrentValue
            if ( tWeightDiff > 0 and self.Machine.IsOffline == False )  or self.Machine.IsOffline == True:
                self.TotalWeight.SetCurrentValue(pMaterialCalcObjectType, self.TotalWeight.CurrentValue(pMaterialCalcObjectType) + tWeightDiff)
                if pMaterialCalcObjectType == FromJob:
                    if not self.MaterialBatch is None:
                        
                        
                        if self.MaterialBatch.EffectiveAmount != 0:
                            tInventoryPart = Round(tWeightDiff / self.MaterialBatch.EffectiveAmount, 5)
                            self.MaterialBatch.Weight = ( 1 - tInventoryPart )  * self.MaterialBatch.Weight
                            
                            self.MaterialBatch.GrossWeight = ( 1 - tInventoryPart )  * self.MaterialBatch.GrossWeight
                        self.MaterialBatch.EffectiveAmount = self.MaterialBatch.EffectiveAmount - tWeightDiff
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcAmount:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()

    
    
    def CalcAmountStandard(self, pMaterialCalcObjectType, pJob, pProductWeightStandard, pJosh):
        tInjectionsCount = 0

        tUnitsProducedOK = 0
        
        
        if self.ChannelNum != 100:
            if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                if pMaterialCalcObjectType == FromJob:
                    
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount
                self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( ( self.MaterialPCTarget.CurrentValue / 100 )  * tInjectionsCount *  ( pProductWeightStandard / 1000 )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType) ))
            elif self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromUnitsProducedOK:
                if pMaterialCalcObjectType == FromJob:
                    tUnitsProducedOK = pJob.UnitsProducedOK
                else:
                    tUnitsProducedOK = pJosh.UnitsProducedOK
                self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( ( self.MaterialPCTarget.CurrentValue / 100 )  * tUnitsProducedOK *  ( pProductWeightStandard / self.Machine.ActiveJob.CavitiesActual )  / 1000 )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType))
        else:
            if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                if pMaterialCalcObjectType == FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount - pJosh.InjectionsCountStart
                self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( ( tInjectionsCount )  * self.MaterialPCTarget.CurrentValue )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType))
            elif self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromUnitsProducedOK:
                if pMaterialCalcObjectType == FromJob:
                    tUnitsProducedOK = pJob.UnitsProducedOK
                else:
                    tUnitsProducedOK = pJob.ActiveJosh.UnitsProducedOK
                self.TotalWeight.SetStandardValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.CurrentValue * tUnitsProducedOK )  - self.TotalWeight.OtherMaterialsAmountStandard(pMaterialCalcObjectType))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcAmountStandard:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()

    
    
    def CalcProductRecipeAmount(self, pMaterialCalcObjectType, pJob, pJosh):
        tInjectionsCount = 0
        
        if pMaterialCalcObjectType == FromJob:
            tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
        else:
            tInjectionsCount = pJosh.InjectionsCount - pJosh.InjectionsCountStart
        if self.ChannelNum != 100:
            self.TotalWeight.SetProductRecipeValue(pMaterialCalcObjectType, ( pJob.PConfigPC / 100 )  *  ( self.MaterialPCTarget.ProductRecipeValue / 100 )  *  ( self.Machine.ActiveJob.ProductRecipeWeight / 1000 )  * tInjectionsCount)
        else:
            self.TotalWeight.SetProductRecipeValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.ProductRecipeValue )  * tInjectionsCount)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcProductRecipeAmount:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()

    
    
    def CalcProductStandardAmount(self, pMaterialCalcObjectType, pJob, pJosh):
        tInjectionsCount = 0

        tUnitsProducedOK = 0
        
        
        if pJob.RecipeRefStandardID > 0:
            if self.ChannelNum != 100:
                if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                    if pMaterialCalcObjectType == FromJob:
                        tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                    else:
                        tInjectionsCount = pJosh.InjectionsCount - pJosh.InjectionsCountStart
                    self.TotalWeight.SetProductStandardValue(pMaterialCalcObjectType, ( pJob.PConfigPC / 100 )  *  ( self.MaterialPCTarget.ProductStandardValue / 100 )  *  ( self.Machine.ActiveJob.ProductStandardRecipeWeight / 1000 )  * tInjectionsCount)
                else:
                    if pMaterialCalcObjectType == FromJob:
                        tUnitsProducedOK = pJob.UnitsProducedOK
                    else:
                        tUnitsProducedOK = pJosh.UnitsProducedOK
                    self.TotalWeight.SetProductStandardValue(pMaterialCalcObjectType, ( pJob.PConfigPC / 100 )  *  ( self.MaterialPCTarget.ProductStandardValue / 100 )  *  ( self.Machine.ActiveJob.ProductStandardRecipeWeight / 1000 )  * tInjectionsCount)
            else:
                if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                    if pMaterialCalcObjectType == FromJob:
                        tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                    else:
                        tInjectionsCount = pJosh.InjectionsCount - pJosh.InjectionsCountStart
                    self.TotalWeight.SetProductStandardValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.ProductStandardValue / 100 )  *  ( tInjectionsCount ))
                else:
                    if pMaterialCalcObjectType == FromJob:
                        tUnitsProducedOK = pJob.UnitsProducedOK
                    else:
                        tUnitsProducedOK = pJosh.UnitsProducedOK
                    self.TotalWeight.SetProductStandardValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.ProductStandardValue / 100 )  *  ( tUnitsProducedOK ))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcProductStandardAmount:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()

    
    
    def CalcRecipeRefAmount(self, pMaterialCalcObjectType, pJob, pJosh):
        tInjectionsCount = 0

        tUnitsProducedOK = 0
        
        
        if self.ChannelNum != 100:
            if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                if pMaterialCalcObjectType == FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount
                self.TotalWeight.SetRecipeRefValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.RecipeRefValue / 100 )  *  ( pJob.RefRecipeProductWeight / 1000 )  * tInjectionsCount)
            else:
                if pMaterialCalcObjectType == FromJob:
                    tUnitsProducedOK = pJob.UnitsProducedOK
                else:
                    tUnitsProducedOK = pJosh.UnitsProducedOK
                self.TotalWeight.SetRecipeRefValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.RecipeRefValue / 100 )  *  ( pJob.RefRecipeUnitWeight / 1000 )  * tUnitsProducedOK)
        else:
            if self.MaterialCalcStandardOption == MaterialCalcStandardOption.FromInjections:
                if pMaterialCalcObjectType == FromJob:
                    tInjectionsCount = pJob.InjectionsCount - pJob.InjectionsCountStart
                else:
                    tInjectionsCount = pJosh.InjectionsCount
                self.TotalWeight.SetRecipeRefValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.RecipeRefValue )  * tInjectionsCount)
            else:
                if pMaterialCalcObjectType == FromJob:
                    tUnitsProducedOK = pJob.UnitsProducedOK
                else:
                    tUnitsProducedOK = pJosh.UnitsProducedOK
                self.TotalWeight.SetRecipeRefValue(pMaterialCalcObjectType, ( self.MaterialPCTarget.RecipeRefValue )  * tUnitsProducedOK)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcRecipeRefAmount:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()

    def CalcMaterialStandardIndex(self, pMaterialCalcObjectType):
        
        
        if self.Job.Machine.Server.SystemVariables.TotalEquipmentMaterialEfficencyOption == JobRecipe:
            self.TotalWeight.SetMaterialStandardIndex(pMaterialCalcObjectType, self.MaterialID.MPGI * self.TotalWeight.StandardValue(pMaterialCalcObjectType))
        else:
            self.TotalWeight.SetMaterialStandardIndex(pMaterialCalcObjectType, self.MaterialID.RefRecipeMPGI * self.TotalWeight.RecipeRefValue(pMaterialCalcObjectType))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcMaterialStandardIndex:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()

    def CheckMaterialRecipeAndLocationMatch(self):
        returnVal = None
        strSQL = ""

        RstCursor = None

        tMaterialID = 0

        tAllowUsingMaterialSubst = False
        
        returnVal = 0
        if self.Job.Status == 10:
            if self.WareHouseLocationID != 0:
                strSQL = 'SELECT TOP 1 *' + '\n'
                strSQL = strSQL + 'FROM ViewRTLocationQueueMatch' + '\n'
                strSQL = strSQL + 'WHERE LocationID = ' + self.WareHouseLocationID + '\n'
                strSQL = strSQL + '     AND InventoryID <> ' + self.ActiveInventoryID + '\n'
                strSQL = strSQL + 'ORDER BY Sequence'
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()
                
                if RstData:
                    tAllowUsingMaterialSubst = MdlADOFunctions.fGetRstValBool(RstData.AllowUsingMaterialSubst, False)
                    tMaterialID = MdlADOFunctions.fGetRstValLong(RstData.MaterialID)
                    
                    if CheckRecipeChannelVSLocationMatch(self. self.Job.Machine.ControllerID, tMaterialID):
                        returnVal = MdlADOFunctions.fGetRstValLong(RstData.InventoryID)
                    else:
                        if tAllowUsingMaterialSubst:
                            if CheckForMaterialSubstitute(MdlADOFunctions.fGetRstValLong(self.MaterialID.CurrentValue), tMaterialID):
                                returnVal = MdlADOFunctions.fGetRstValLong(RstData.InventoryID)
                RstCursor.close()
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.CheckMaterialRecipeAndLocationMatch:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        RstCursor = None
        return returnVal

    def LoadNextInventoryItem(self, pInventoryItem):
        strSQL = ""

        RstCursor = None

        tMaterialBatch = self.MaterialBatch()

        tBatchTagName = ""
        
        
        if self.Job.Status == 10:
            if self.WareHouseLocationID != 0:
                
                tMaterialBatch = GetInventoryItemFromGlobalCollection(gServer.ActiveInventoryItems, pInventoryItem)
                if tMaterialBatch is None:
                    strSQL = 'SELECT ID,Batch,Amount,EffectiveAmount,EffectiveOriginalAmount FROM TblInventory WHERE ID = ' + pInventoryItem
                    RstCursor = MdlConnection.CN.cursor()
                    RstCursor.execute(strSQL)
                    RstData = RstCursor.fetchone()
                    
                    if RstData:
                        tMaterialBatch = self.MaterialBatch()
                        tMaterialBatch.ID = MdlADOFunctions.fGetRstValLong(RstData.ID)
                        tMaterialBatch.CurrentValue = MdlADOFunctions.fGetRstValString(RstData.Batch)
                        tMaterialBatch.Amount = MdlADOFunctions.fGetRstValDouble(RstData.Amount)
                        tMaterialBatch.EffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveAmount)
                        tMaterialBatch.OriginalEffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveOriginalAmount)
                    RstCursor.close()
                if not tMaterialBatch is None:
                    self.MaterialBatch = tMaterialBatch
                    
                    CheckChannelJobMaterialRecord(self)
                    CheckChannelJoshMaterialRecord(self)
                    
                    tBatchTagName = 'Cnl' + self.ChannelNum + 'MaterialBatch'
                    self.Job.Machine.SetFieldValue(tBatchTagName, self.MaterialBatch.CurrentValue)
                    
                    self.ActiveInventoryID = pInventoryItem
                    
                    strSQL = 'UPDATE TblControllerChannels' + '\n'
                    strSQL = strSQL + 'SET ActiveInventoryID = ' + self.ActiveInventoryID
                    strSQL = strSQL + 'WHERE ControllerID = ' + self.Machine.ControllerID + ' AND ChannelNum = ' + self.ChannelNum
                    CN.Execute(strSQL)
                    UpdateJobRecipeFromBatchChange(self.Job, self.ChannelNum, 0, tMaterialBatch)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.GetNextInventoryItem:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum))
            Err.Clear()
        RstCursor = None

    def AddSetupFromLocationBatchChange(self):
        returnVal = None
        tAmount = 0

        tValue = 0
        
        if self.Job.Machine.LocationBatchChangeSetupModeID != 0:
            if (self.Job.Machine.LocationBatchChangeSetupModeID == 1):
                tValue = self.Job.Machine.LocationBatchChangeSetupValue
                tAmount = tValue
            elif (self.Job.Machine.LocationBatchChangeSetupModeID == 2):
                tValue = self.Job.Machine.LocationBatchChangeSetupValue
                tAmount = ( tValue / 100 )  * self.MaterialBatch.EffectiveAmount
            elif (self.Job.Machine.LocationBatchChangeSetupModeID == 3):
                tValue = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(self.Job.ID, 'LocationBatchChangeSetupValue', self.ChannelNum, 0))
                tAmount = tValue
            elif (self.Job.Machine.LocationBatchChangeSetupModeID == 4):
                tValue = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(self.Job.ID, 'LocationBatchChangeSetupValue', self.ChannelNum, 0))
                tAmount = ( tValue / 100 )  * self.MaterialBatch.EffectiveAmount
            elif (self.Job.Machine.LocationBatchChangeSetupModeID == 5):
                tValue = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(self.Job.ID, 'LocationBatchChangeSetupValue', self.ChannelNum, 0))
                tAmount = tValue
            elif (self.Job.Machine.LocationBatchChangeSetupModeID == 6):
                tValue = MdlADOFunctions.fGetRstValDouble(fGetRecipeValueJob(self.Job.ID, 'LocationBatchChangeSetupValue', self.ChannelNum, 0))
                tAmount = ( tValue / 100 )  * self.MaterialBatch.EffectiveAmount
            if tAmount > 0:
                self.Job.AddRejects(tAmount, 0, 100, False)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.AddSetupFromLocationBatchChange:', str(0), error.args[0], 'JobID:' + str(self.Job.ID) + '. ChannelNum: ' + str(self.ChannelNum) + '. SplitNum:  ' + self)
            Err.Clear()
        return returnVal

    def PerformActivationForLocationBatch(self):
        tInventoryID = 0

        tEffectiveAmount = 0
        
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
        Counter = 0
        
        for Counter in range(1, self.__mSplits.Count):
            self.__mSplits.Item[Counter] = None
            self.__mSplits.Remove(Counter)
        self.__mSplits = None
        self.__mMachine = None
        self.__mMaterialID = None
        self.__mMaterialPCTarget = None
        self.__mMaterialPC = None
        self.__mTotalWeight = None
        self.__mJob = None
        self.__mMaterialBatch = None
        self.__mForecastWeight = None
        print(Fore.GREEN + 'Channel Destroy' + str(self.__mID))


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    def setSplits(self, value):
        self.__mSplits = value

    def getSplits(self):
        returnVal = None
        returnVal = self.__mSplits
        return returnVal
    Splits = property(fset=setSplits, fget=getSplits)


    def setSplitsCounter(self, value):
        self.__mSplitsCount = value

    def getSplitsCounter(self):
        returnVal = None
        returnVal = self.__mSplitsCount
        return returnVal
    SplitsCounter = property(fset=setSplitsCounter, fget=getSplitsCounter)


    def setChannelNum(self, value):
        self.__mChannelNum = value

    def getChannelNum(self):
        returnVal = None
        returnVal = self.__mChannelNum
        return returnVal
    ChannelNum = property(fset=setChannelNum, fget=getChannelNum)


    def setIsMain(self, value):
        self.__mIsMain = value

    def getIsMain(self):
        returnVal = None
        returnVal = self.__mIsMain
        return returnVal
    IsMain = property(fset=setIsMain, fget=getIsMain)


    def setSplitDefinitionsFromTable(self, value):
        self.__mSplitDefinitionsFromTable = value

    def getSplitDefinitionsFromTable(self):
        returnVal = None
        returnVal = self.__mSplitDefinitionsFromTable
        return returnVal
    SplitDefinitionsFromTable = property(fset=setSplitDefinitionsFromTable, fget=getSplitDefinitionsFromTable)


    def setWorkingWithBatchTracking(self, value):
        self.__mWorkingWithBatchTracking = value

    def getWorkingWithBatchTracking(self):
        returnVal = None
        returnVal = self.__mWorkingWithBatchTracking
        return returnVal
    WorkingWithBatchTracking = property(fset=setWorkingWithBatchTracking, fget=getWorkingWithBatchTracking)


    def setLastReadTime(self, value):
        self.__mLastReadTime = value

    def getLastReadTime(self):
        returnVal = None
        returnVal = self.__mLastReadTime
        return returnVal
    LastReadTime = property(fset=setLastReadTime, fget=getLastReadTime)


    
    def setMachine(self, value):
        self.__mMachine = value

    def getMachine(self):
        returnVal = None
        returnVal = self.__mMachine
        return returnVal
    Machine = property(fset=setMachine, fget=getMachine)


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


    def setMaterialCalcStandardOption(self, value):
        self.__mMaterialCalcStandardOption = value

    def getMaterialCalcStandardOption(self):
        returnVal = None
        returnVal = self.__mMaterialCalcStandardOption
        return returnVal
    MaterialCalcStandardOption = property(fset=setMaterialCalcStandardOption, fget=getMaterialCalcStandardOption)


    def setJob(self, value):
        self.__mJob = value

    def getJob(self):
        returnVal = None
        returnVal = self.__mJob
        return returnVal
    Job = property(fset=setJob, fget=getJob)


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
