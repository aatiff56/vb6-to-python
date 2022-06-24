from colorama import Fore
from datetime import datetime

from Channel import Channel
from MachineType import PConfigSonsRefRecipeSourceOption
from RTEvent import RTEvent
from RTEngineEvent import RTEngineEvent

import MdlADOFunctions
import MdlConnection
import MdlGlobal
import mdl_Common
import MdlServer
import MdlUtilsH
import MdlUtils
import GlobalVariables


class Job:
    __mID = 0
    __mProductID = 0
    __mProduct = None
    __mDepartmentID = 0
    __mDepartment = None
    __mStatus = 0
    __mStartTimeTarget = None
    __mStartTime = None
    __mEndTimeTarget = None
    __mEndTime = None
    __mEndTimeForecast = None
    __mControllerID = 0
    __mLastJobID = 0
    __mSetUpStart = None
    __mSetUpEnd = None
    __mSetupDuration = 0.0
    __mFirstProductUserID = 0
    __mSetUpEndInjectionsCount = 0.0
    __mSetUpEndActiveTimeMin = 0
    __mSetUpEndAutoRejects = 0.0
    __mSetUpProductionTimeMin = 0.0
    __mSetUpDownTimeMin = 0.0
    __mPConfigID = 0
    __mPConfigJobID = 0
    __mPConfigPC = 0.0
    __mIsPConfigMain = False
    __mPConfigUnits = 0.0
    __mPConfigParentID = 0
    __mPConfigRelation = 0
    __mPConfigJobCycles = 0.0
    __mPConfigProductionOrder = 0
    __mPConfigIsMaterialCount = False
    __mPConfigIsChannel100Count = False
    __mPConfigIsSpecialMaterialCount = False
    __mPConfigJobs = {}
    __mPConfigParentJob = None
    __mCavitiesStandard = 0.0
    __mCavitiesActual = 0.0
    __mMoldID = 0
    __mMold = None
    __mCavitiesPC = 0.0
    __mCavitiesEfficiency = 0.0
    __mMachineStatus = 0
    __mMachineID = 0
    __mMachine = None
    __mMachineType = None
    __mCycleTimeLast = 0.0
    __mCycleTimeAvg = 0.0
    __mCycleTimeAvgDiff = 0.0
    __mCycleTimeAvgDiffPC = 0.0
    __mCycleTimeEfficiency = 0.0
    __mCycleTimeStandard = 0.0
    __mCycleTimeAvgSMean = 0.0
    __mRejectsTotal = 0.0
    __mRejectsPC = 0.0
    __mRejectsEfficiency = 0.0
    __mTotalWasteKg = 0.0
    __mRejectsRead = 0.0
    __mRejectsReported = 0.0
    __mReportedRejectsDiff = 0.0
    __mRejectsForEfficiency = None
    __mRejectsForConsumption = None
    __mAutoRejects = 0.0
    __mUnitsTarget = 0.0
    __mUnitsProduced = 0.0
    __mUnitsProducedStart = 0.0
    __mUnitsProducedOK = 0.0
    __mUnitsProducedPC = 0.0
    __mUnitsProducedLeft = 0.0
    __mUnitsReportedOK = 0.0
    __mUnitsReportedOKDiff = 0.0
    __mUnitsReportedOKDiffPC = 0.0
    __mUnitsProducedOKDiff = 0.0
    __mUnitsProducedTheoretically = 0.0
    __mUnitsProducedTheoreticallyPC = 0.0
    __mQuantityAdjustmentUnits = 0.0
    __mDownTimeMin = 0.0
    __mDownTimePC = 0.0
    __mDownTimeEfficiency = 0.0
    __mDownTimeEfficiencyOEE = 0.0
    __mInActiveTimeMin = 0.0
    __mInActiveTimePC = 0.0
    __mActiveTimeMin = 0
    __mActiveTimePC = 0.0
    __mProductionTimeMin = 0
    __mProductionTimePC = 0.0
    __mProductionUsabilityPC = 0.0
    __mTimeLeftHr = 0.0
    __mDurationMin = 0
    __mDurationForecast = 0
    __mEngineTimeMin = 0.0
    __mOriginalJobID = 0
    __mOriginalUnitsTarget = 0.0
    __mOriginalUnitsProducedOK = 0.0
    __mInjectionsCount = 0.0
    __mInjectionsCountLast = 0.0
    __mInjectionsCountStart = 0.0
    __mCyclesDroped = 0.0
    __mCyclesNetActual = 0.0
    __mInjectionsDiff = 0.0
    __mTotalCycles = 0.0
    __mProductWeightLast = 0.0
    __mProductWeightAvg = 0.0
    __mProductWeightDiff = 0.0
    __mProductWeightDiffPC = 0.0
    __mProductWeightPC = 0.0
    __mProductWeightStandard = 0.0
    __mProductRecipeWeight = 0.0
    __mProductStandardRecipeWeight = 0.0
    __mRefRecipeProductWeight = 0.0
    __mRefRecipeUnitWeight = 0.0
    __mMaterialTotal = 0.0
    __mMaterialTotalMainPC = 0.0
    __mMaterialTotalAdditivePC = 0.0
    __mMainMaterialTotal = 0.0
    __mMainMaterialStandard = 0.0
    __mMainMaterialStandardPC = 0.0
    __mMainMaterialStandardCalcPC = 0.0
    __mMainMaterialStandardPCCalcC = 0.0
    __mAdditiveMaterialTotal = 0.0
    __mAdditiveMaterialStandard = 0.0
    __mAdditiveMaterialStandardPC = 0.0
    __mAdditiveMaterialStandardCalcPC = 0.0
    __mAdditiveMaterialStandardPCCalcC = 0.0
    __mMaterialConsumptionKgtoHour = 0.0
    __mCycleWeightActualAvg = 0.0
    __mMaterialActualIndex = 0.0
    __mMaterialRecipeIndexJob = 0.0
    __mMaterialRecipeIndexProduct = 0.0
    __mMaterialStandardIndex = 0.0
    __mSetupMaterialTotal = 0.0
    __mEfficiencyTotal = 0.0
    __mTotalMaterialEfficiencyActual = 0.0
    __mTotalMaterialEfficiencyTheoretical = 0.0
    __mTotalEquipmentMaterialEfficency = 0.0
    __mPEE = 0.0
    __mEffectiveDurationMin = 0.0
    __mEffectiveDownTimeMin = 0.0
    __mEffectiveInActiveTimeMin = 0.0
    __mEffectiveActiveTimeMin = 0.0
    __mEffectiveProductionTimeMin = 0.0
    __mEffectiveSetupDurationMin = 0.0
    __mEffectiveCycleTime = 0.0
    __mEffectiveWeight = 0.0
    __mRecipeRefType = 0
    __mRecipeRefJob = 0
    __mRecipeRefStandardID = 0
    __mActiveJosh = None
    __mOpenEvent = None
    __mOpenWorkingEvent = None
    __mOpenEngineEvent = None
    __mOpenAlarms = {}
    __mControllerChannels = {}
    __mMoldChangeFirstOtherMoldMachineJobOrder = 0
    __mMoldChangeTimeLeftHr = 0.0
    __mMoldChangeUnitsTarget = 0.0
    __mMoldChangeUnitsProducedOK = 0.0
    __mValidationLog = ''
    __mNextJobMaterialFlowStart = None
    __mJobDef = 0
    __mJobDefCalcEfficiencies = False
    __mJobDefDisableProductionTime = False
    __mJobDefSetUpEndGeneralCycles = 0.0
    __mERPJobIndexKey = ''
    __mPlannedSetupType = 0
    __mSetupTypeSetUpEndGeneralCycles = 0.0

    
    def Init(self, pMachine, pJobID, pFromActivateJob, pPConfigParentJob=None, pFromINITMachine=False):
        strSQL = ''
        RstCursor = None
        PConfigRstCursor = None
        tJob = Job()
        tControllerChannel = Channel()
        jdRstCursor = None

        try:
            strSQL = 'SELECT * FROM TblJob WHERE ID = ' + str(pJobID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.ID = pJobID
                self.Machine = pMachine
                if MdlADOFunctions.fGetRstValString(RstData.StartTime) != '':
                    self.StartTime = RstData.StartTime
                else:
                    self.StartTime = mdl_Common.NowGMT()
                if MdlADOFunctions.fGetRstValString(RstData.EndTime) != '':
                    self.EndTime = RstData.EndTime
                if MdlADOFunctions.fGetRstValString(RstData.SetUpStart) != '':
                    self.SetUpStart = RstData.SetUpStart
                if MdlADOFunctions.fGetRstValString(RstData.SetUpEnd) != '':
                    self.SetUpEnd = RstData.SetUpEnd
                    self.Machine.NewJob = False
                    self.SetUpEndInjectionsCount = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndInjectionsCount)
                    
                    self.SetUpEndAutoRejects = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndAutoRejects)
                else:
                    self.Machine.NewJob = True
                
                self.AutoRejects = MdlADOFunctions.fGetRstValDouble(RstData.AutoRejects)
                self.SetupDuration = MdlADOFunctions.fGetRstValLong(RstData.SetupDuration)
                self.ProductID = MdlADOFunctions.fGetRstValLong(RstData.ProductID)
                self.Product = MdlServer.GetOrCreateProduct(self.Machine.Server, self.ProductID)
                self.MoldID = MdlADOFunctions.fGetRstValLong(RstData.MoldID)
                self.Mold = MdlServer.GetOrCreateMold(self.Machine.Server, self.MoldID)
                
                
                self.GetUnitsInCycle(RstData)
                self.MachineID = MdlADOFunctions.fGetRstValLong(RstData.MachineID)
                self.DepartmentID = MdlADOFunctions.fGetRstValLong(RstData.Department)
                self.Department = MdlServer.GetOrCreateDepartment(self.Machine.Server, self.DepartmentID)
                self.MachineType = MdlServer.GetOrCreateMachineType(self.Machine.Server, MdlADOFunctions.fGetRstValLong(RstData.MachineType))
                
                if pFromActivateJob and not pFromINITMachine:
                    self.InjectionsCount = 0
                else:
                    self.InjectionsCount = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCount)
                if pFromActivateJob and not pFromINITMachine:
                    self.InjectionsCountLast = 0
                else:
                    self.InjectionsCountLast = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCountLast)
                if pFromActivateJob and not pFromINITMachine:
                    self.InjectionsCountStart = 0
                else:
                    self.InjectionsCountStart = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCountStart)
                self.UnitsTarget = MdlADOFunctions.fGetRstValDouble(RstData.UnitsTarget)
                if pFromActivateJob and not pFromINITMachine:
                    self.UnitsProduced = 0
                else:
                    self.UnitsProduced = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProduced)
                if pFromActivateJob and not pFromINITMachine:
                    self.UnitsProducedOK = 0
                else:
                    self.UnitsProducedOK = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedOK)
                
                self.UnitsProducedTheoretically = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedTheoretically)
                self.UnitsProducedTheoreticallyPC = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedTheoreticallyPC)
                self.QuantityAdjustmentUnits = MdlADOFunctions.fGetRstValDouble(RstData.QuantityAdjustmentUnits)
                print(Fore.GREEN + 'Inside Job.Init | MachineID=' + str(self.MachineID) + ' JobID=' + str(pJobID) + ' UnitsProduced=' + str(self.UnitsProduced) + ' UnitsProducedOK=' + str(self.UnitsProducedOK) + ' FromActivateJob=' + str(pFromActivateJob) + ' | ' + str(mdl_Common.NowGMT()) + '\n')
                self.UnitsProducedLeft = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedLeft)
                self.DurationMin = MdlADOFunctions.fGetRstValLong(RstData.DurationMin)
                self.DownTimeMin = MdlADOFunctions.fGetRstValLong(RstData.DownTimeMin)
                self.SetUpDownTimeMin = MdlADOFunctions.fGetRstValLong(RstData.SetUpDownTimeMin)
                self.InActiveTimeMin = MdlADOFunctions.fGetRstValLong(RstData.InActiveTimeMin)
                self.OriginalJobID = MdlADOFunctions.fGetRstValLong(RstData.OriginalJobID)
                self.OriginalUnitsTarget = MdlADOFunctions.fGetRstValDouble(RstData.OriginalUnitsTarget)
                self.OriginalUnitsProducedOK = MdlADOFunctions.fGetRstValDouble(RstData.OriginalUnitsProducedOK)
                self.ProductWeightAvg = MdlADOFunctions.fGetRstValDouble(RstData.ProductWeightAvg)
                self.ProductWeightStandard = MdlADOFunctions.fGetRstValDouble(RstData.ProductWeightStandard)
                self.ProductRecipeWeight = MdlADOFunctions.fGetRstValDouble(RstData.ProductRecipeWeight)
                if self.ProductRecipeWeight == 0:
                    self.ProductRecipeWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(self.Product.ID, 'ProductWeight', 0, 0))
                self.CycleTimeStandard = MdlADOFunctions.fGetRstValDouble(RstData.CycleTimeStandard)
                self.CycleTimeAvg = MdlADOFunctions.fGetRstValDouble(RstData.CycleTimeAvg)
                self.Status = MdlADOFunctions.fGetRstValLong(RstData.Status)
                
                self.PConfigID = MdlADOFunctions.fGetRstValLong(RstData.PConfigID)
                self.PConfigPC = MdlADOFunctions.fGetRstValDouble(RstData.PConfigPC)
                
                self.PConfigUnits = MdlADOFunctions.fGetRstValDouble(RstData.PConfigUnits)
                self.PConfigJobID = MdlADOFunctions.fGetRstValLong(RstData.PConfigJobID)
                self.PConfigParentID = MdlADOFunctions.fGetRstValLong(RstData.PConfigParentID)
                self.IsPConfigMain = MdlADOFunctions.fGetRstValBool(RstData.IsPConfigMain, True)
                self.PConfigIsMaterialCount = MdlADOFunctions.fGetRstValBool(RstData.PConfigIsMaterialCount, True)
                self.PConfigIsChannel100Count = MdlADOFunctions.fGetRstValBool(RstData.PConfigIsChannel100Count, True)
                self.PConfigIsSpecialMaterialCount = MdlADOFunctions.fGetRstValBool(RstData.PConfigIsSpecialMaterialCount, True)
                
                self.RecipeRefType = MdlADOFunctions.fGetRstValLong(RstData.RecipeRefType)
                self.RecipeRefJob = MdlADOFunctions.fGetRstValLong(RstData.RecipeRefJob)
                self.RecipeRefStandardID = MdlADOFunctions.fGetRstValLong(RstData.RecipeRefStandardID)
                self.GetRefRecipeProductWeight()
                self.GetRefRecipeUnitWeight()
                if self.RecipeRefStandardID != 0:
                    self.ProductStandardRecipeWeight = MdlADOFunctions.fGetRstValDouble(MdlUtils.MdlUtils.fGetRecipeValueStandard(self.RecipeRefStandardID, 'ProductWeight', 0, 0, self.Product.ID))
                self.MaterialRecipeIndexJob = MdlADOFunctions.fGetRstValDouble(RstData.MaterialRecipeIndexJob)
                self.MaterialRecipeIndexProduct = MdlADOFunctions.fGetRstValDouble(RstData.MaterialRecipeIndexProduct)
                self.ERPJobIndexKey = MdlADOFunctions.fGetRstValString(RstData.ERPJobIndexKey)
                
                self.JobDef = MdlADOFunctions.fGetRstValLong(RstData.ERPJobDef)
                if self.JobDef > 0:
                    strSQL = 'SELECT * FROM STblJobDefinitions WHERE ID = ' + str(self.JobDef)
                    jdRstCursor = MdlConnection.CN.cursor()
                    jdRstCursor.execute(strSQL)
                    jdRstData = jdRstCursor.fetchone()

                    if jdRstData:
                        self.JobDefCalcEfficiencies = MdlADOFunctions.fGetRstValBool(( jdRstData.CalcEfficiencies ), True)
                        self.JobDefDisableProductionTime = MdlADOFunctions.fGetRstValBool(( jdRstData.DisableProductionTime ), False)
                        self.JobDefSetUpEndGeneralCycles = MdlADOFunctions.fGetRstValDouble(jdRstData.SetUpEndGeneralCycles)
                    jdRstCursor.close()
                
                self.PlannedSetupType = MdlADOFunctions.fGetRstValLong(RstData.PlannedSetupType)
                if self.PlannedSetupType > 0:
                    strSQL = 'SELECT * FROM STblMachineTypeSetupTypes WHERE ID = ' + str(self.PlannedSetupType)
                    jdRstCursor = MdlConnection.CN.cursor()
                    jdRstCursor.execute(strSQL)
                    jdRstData = jdRstCursor.fetchone()

                    if jdRstData:
                        self.SetupTypeSetUpEndGeneralCycles = MdlADOFunctions.fGetRstValDouble(jdRstData.SetUpEndGeneralCycles)
                    jdRstCursor.close()

                self.UnitsReportedOK = MdlADOFunctions.fGetRstValDouble(RstData.UnitsReportedOK)                
                self.GetOpenEvent()
                
                if self.OpenEvent is None:
                    self.GetOpenWorkingEvent()
                self.GetOpenEngineEvent()
                
                if self.Status == 10:
                    self.__mOpenAlarms = {}                    
                    self.LoadAlarms()
                else:
                    self.DurationMin = MdlADOFunctions.fGetRstValLong(RstData.DurationMin)
                    self.ProductionTimeMin = MdlADOFunctions.fGetRstValLong(RstData.ProductionTimeMin)
                    self.SetUpProductionTimeMin = MdlADOFunctions.fGetRstValLong(RstData.SetUpProductionTimeMin)
                    self.ProductionTimePC = MdlADOFunctions.fGetRstValDouble(RstData.ProductionTimePC)
                    self.ProductionUsabilityPC = MdlADOFunctions.fGetRstValDouble(RstData.ProductionUsabilityPC)
                    self.ActiveTimeMin = MdlADOFunctions.fGetRstValLong(RstData.ActiveTimeMin)
                    self.ActiveTimePC = MdlADOFunctions.fGetRstValDouble(RstData.ActiveTimePC)
                    self.InActiveTimeMin = MdlADOFunctions.fGetRstValLong(RstData.InActiveTimeMin)
                    self.InActiveTimePC = MdlADOFunctions.fGetRstValDouble(RstData.InActiveTimePC)
                    self.DownTimeMin = MdlADOFunctions.fGetRstValLong(RstData.DownTimeMin)
                    self.SetUpDownTimeMin = MdlADOFunctions.fGetRstValLong(RstData.SetUpDownTimeMin)
                    self.DownTimePC = MdlADOFunctions.fGetRstValDouble(RstData.DownTimePC)
                    self.TimeLeftHr = MdlADOFunctions.fGetRstValDouble(RstData.TimeLeftHr)
                    self.EngineTimeMin = MdlADOFunctions.fGetRstValLong(RstData.EngineTimeMin)
                    
                    self.MaterialTotal = MdlADOFunctions.fGetRstValDouble(RstData.MaterialTotal)
                    self.MaterialTotalAdditivePC = MdlADOFunctions.fGetRstValDouble(RstData.MaterialTotalAdditivePC)
                    self.MaterialTotalMainPC = MdlADOFunctions.fGetRstValDouble(RstData.MaterialTotalMainPC)
                    self.MainMaterialTotal = MdlADOFunctions.fGetRstValDouble(RstData.MainMaterialTotal)
                    self.MainMaterialStandard = MdlADOFunctions.fGetRstValDouble(RstData.MainMaterialStandard)
                    self.MainMaterialStandardPC = MdlADOFunctions.fGetRstValDouble(RstData.MainMaterialStandardPC)
                    self.MainMaterialStandardCalcPC = MdlADOFunctions.fGetRstValDouble(RstData.MainMaterialStandardCalcPC)
                    self.MainMaterialStandardPCCalcC = MdlADOFunctions.fGetRstValDouble(RstData.MainMaterialStandardPCCalcC)
                    self.AdditiveMaterialTotal = MdlADOFunctions.fGetRstValDouble(RstData.AdditiveMaterialTotal)
                    self.AdditiveMaterialStandard = MdlADOFunctions.fGetRstValDouble(RstData.AdditiveMaterialStandard)
                    self.AdditiveMaterialStandardPC = MdlADOFunctions.fGetRstValDouble(RstData.AdditiveMaterialStandardPC)
                    self.AdditiveMaterialStandardCalcPC = MdlADOFunctions.fGetRstValDouble(RstData.AdditiveMaterialStandardCalcPC)
                    self.AdditiveMaterialStandardPCCalcC = MdlADOFunctions.fGetRstValDouble(RstData.AdditiveMaterialStandardPCCalcC)
                    self.MaterialActualIndex = MdlADOFunctions.fGetRstValDouble(RstData.MaterialActualIndex)
                    self.CycleWeightActualAvg = MdlADOFunctions.fGetRstValDouble(RstData.CycleWeightActualAvg)
                    self.MaterialConsumptionKgtoHour = MdlADOFunctions.fGetRstValDouble(RstData.MaterialConsumptionKgtoHour)
                    self.SetupMaterialTotal = MdlADOFunctions.fGetRstValDouble(RstData.SetupMaterialTotal)
                    
                    self.EfficiencyTotal = MdlADOFunctions.fGetRstValDouble(RstData.EfficiencyTotal)
                    self.TotalEquipmentMaterialEfficency = MdlADOFunctions.fGetRstValDouble(RstData.TotalEquipmentMaterialEfficency)
                    self.TotalMaterialEfficiencyActual = MdlADOFunctions.fGetRstValDouble(RstData.TotalMaterialEfficiencyActual)
                    self.TotalMaterialEfficiencyTheoretical = MdlADOFunctions.fGetRstValDouble(RstData.TotalMaterialEfficiencyTheoretical)
                    
                    self.EffectiveActiveTimeMin = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveActiveTimeMin)
                    self.EffectiveCycleTime = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveCycleTime)
                    self.EffectiveDownTimeMin = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveDownTimeMin)
                    self.EffectiveDurationMin = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveDurationMin)
                    self.EffectiveInActiveTimeMin = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveInActiveTimeMin)
                    self.EffectiveProductionTimeMin = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveProductionTimeMin)
                    self.EffectiveSetupDurationMin = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveSetupDurationMin)
                    self.EffectiveWeight = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveWeight)
                    self.MaterialRecipeIndexJob = MdlADOFunctions.fGetRstValDouble(RstData.MaterialRecipeIndexJob)
                    self.MaterialRecipeIndexProduct = MdlADOFunctions.fGetRstValDouble(RstData.MaterialRecipeIndexProduct)
                    self.UnitsProducedPC = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedPC)
                    
                    self.ProductWeightStandard = MdlADOFunctions.fGetRstValDouble(RstData.ProductWeightStandard)
                    self.ProductWeightAvg = MdlADOFunctions.fGetRstValDouble(RstData.ProductWeightAvg)
                    self.ProductWeightLast = MdlADOFunctions.fGetRstValDouble(RstData.ProductWeightLast)
                    self.ProductRecipeWeight = MdlADOFunctions.fGetRstValDouble(RstData.ProductRecipeWeight)
                
                if self.PConfigID > 0 and self.IsPConfigMain == False:
                    self.PConfigParentJob = pPConfigParentJob
                    self.Status = self.PConfigParentJob.Status
                
                
                if self.PConfigID != 0 and self.MachineType.PConfigSonsRefRecipeSource == PConfigSonsRefRecipeSourceOption.FromProductRecipe:
                    self.ProductWeightStandard = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, 'ProductWeight', 0, 0))
                    self.ProductWeightLast = self.ProductWeightStandard
                    self.ProductWeightAvg = self.ProductWeightStandard
                
                if self.PConfigID > 0 and self.IsPConfigMain == True:
                    self.PConfigJobs = {}
                    PConfigRstCursor = None
                    strSQL = 'SELECT ID FROM TblJob WHERE PConfigParentID = ' + str(self.ID) + ' AND ID <> ' + str(self.ID)
 
                    PConfigRstCursor = MdlConnection.CN.cursor()
                    PConfigRstCursor.execute(strSQL)
                    PConfigRstValues = PConfigRstCursor.fetchall()

                    for PConfigRstData in PConfigRstValues:
                        tJob = Job()
                        tJob.Init(pMachine, MdlADOFunctions.fGetRstValLong(PConfigRstData.ID), pFromActivateJob, self)
                        self.PConfigJobs[str(tJob.PConfigJobID)] = tJob
                    PConfigRstCursor.close()
                
                self.ValidationLog = MdlADOFunctions.fGetRstValString(RstData.ValidationLog)
                
                if GlobalVariables.IsDate(RstData.NextJobMaterialFlowStart):
                    self.NextJobMaterialFlowStart = datetime.strptime(RstData.NextJobMaterialFlowStart, '%d/%m/%Y %H:%M:%S')
            RstCursor.close()
            
            if self.Status == 10 and ( self.PConfigID == 0 or ( self.PConfigID != 0 and self.IsPConfigMain == True )):
                self.InitMachineControlParams()
                self.InitMoldChangeDetails()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                    
                MdlGlobal.RecordError(type(self).__name__ + '.Init:', str(0), error.args[0], 'JobID:' + str(pJobID))
                print(Fore.RED + 'Job.Init: Error Descr=' + error.args[0] + ' JobID=' + str(pJobID) + ' | ' + str(mdl_Common.NowGMT()))
            
        RstCursor = None
        PConfigRstCursor = None
        tJob = None
        tControllerChannel = None

    def InitControllerChannels(self, pJoshID, pFromActivateJob):
        strSQL = ''
        RstCursor = None
        tControllerChannel = Channel()
        self.ControllerChannels = None
        self.ControllerChannels = {}

        try:
            strSQL = 'SELECT * FROM TblControllerChannels WHERE ControllerID = ' + str(self.Machine.ControllerID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()

            for RstData in RstValues:
                tControllerChannel = Channel()
                tControllerChannel.Init(self.Machine, MdlADOFunctions.fGetRstValLong(RstData.ID), self, pJoshID, pFromActivateJob)
                self.ControllerChannels.Add(tControllerChannel, MdlADOFunctions.fGetRstValString(RstData.ChannelNum))
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.InitControllerChannels:', str(0), error.args[0], 'JobID:' + str(self.ID))
        RstCursor = None

    def GetOpenEvent(self):
        strSQL = ''
        RstCursor = None
        tEvent = None
        
        try:
            strSQL = 'SELECT ID FROM TblEvent Where JobID = ' + str(self.ID) + ' AND EndTime IS NULL'

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                tEvent = RTEvent()
                tEvent.Init(self, MdlADOFunctions.fGetRstValLong(RstData.ID))
                self.OpenEvent = tEvent
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                    
            MdlGlobal.RecordError(type(self).__name__ + '.GetOpenEvent:', str(0), error.args[0], 'JobID:' + str(self.ID))

        RstCursor = None

    def GetOpenWorkingEvent(self):
        strSQL = ''
        RstCursor = None
        tEvent = None
        
        try:
            strSQL = 'SELECT ID FROM TblWorkingEvents Where JobID = ' + str(self.ID) + ' AND EndTime IS NULL'
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                tEvent = RTWorkingEvent()
                tEvent.Init(self, MdlADOFunctions.fGetRstValLong(RstCursor.ID))
                self.OpenWorkingEvent = tEvent
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.GetOpenWorkingEvent:', str(0), error.args[0], 'JobID:' + str(self.ID))
        RstCursor = None

    def GetOpenEngineEvent(self):
        strSQL = ''
        RstCursor = None
        tEvent = None
        
        try:
            strSQL = 'SELECT ID FROM TblEngineEvents Where JobID = ' + str(self.ID) + ' AND EndTime IS NULL'
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                tEvent = RTEngineEvent()
                tEvent.Init(self, MdlADOFunctions.fGetRstValLong(RstData.ID))
                self.OpenEngineEvent = tEvent
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.GetOpenEngineEvent:', str(0), error.args[0], 'JobID:' + str(self.ID))
        RstCursor = None

    def InitMachineControlParams(self):
        
        try:
            self.Machine.SetFieldValue('UnitsTarget', str(self.UnitsTarget))
            self.Machine.SetFieldValue('TotalCycles', str(self.Machine.TotalCycles))
            self.Machine.SetFieldValue('UnitsProduced', str(self.UnitsProduced))
            self.Machine.SetFieldValue('UnitsProducedOK', str(self.UnitsProduced))
            self.Machine.SetFieldValue('MoldID', str(self.Mold.ID))
            self.Machine.SetFieldValue('MoldCavities', str(self.CavitiesActual))

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.InitMachineControlParams:', str(0), error.args[0], 'JobID:' + str(self.ID))

    def DetailsCalc(self, pCalcTimes, pCalcMaterial):
        tVariant = None

        tChildJob = Job()
        
        if self.Machine.ID == 38:
            tVariant = tVariant
        
        if self.Status == 10 and self.Machine.IsOffline == False:
            
            if not self.PConfigParentJob is None:
                self.InjectionsDiff = self.PConfigParentJob.InjectionsDiff
            else:
                self.InjectionsDiff = self.Machine.TotalCycles - self.Machine.TotalCyclesLast - self.InjectionsCountStart
            if self.InjectionsDiff < 0:
                self.InjectionsDiff = 0
            self.InjectionsCountLast = self.InjectionsCount
            self.InjectionsCount = self.InjectionsCount + self.InjectionsDiff
            self.GetCycleTime
            if not self.Machine.ActiveJob is None:
                if self.Machine.NewJob and self.ID == self.Machine.ActiveJob.ID:
                    self.CheckAutomaticSetupEnd
            
            self.Machine.TotalCyclesLast = self.Machine.TotalCycles
            
        elif self.Machine.IsOffline == True:
            self.GetParametersForOfflineJob
        
        if ( self.Machine.CycleTimeFilter == False )  or  ( self.Status != 10 ) :
            self.CalcRejects
            self.CalcUnits(self.InjectionsDiff)
            self.CalcUnitsReportedOK
            self.CalcOriginalJobData(self.InjectionsDiff)
            self.CyclesNetActual = self.InjectionsCount - self.CyclesDroped
        elif self.Machine.CycleTimeFilter == True:
            if self.Machine.IgnoreCycleTimeFilter == True:
                self.CalcRejects
                self.CalcUnits(self.InjectionsDiff)
                self.CalcUnitsReportedOK
                self.CalcOriginalJobData(self.InjectionsDiff)
                self.CyclesNetActual = self.InjectionsCount - self.CyclesDroped
            else:
                if self.CheckFilters() == True:
                    self.CalcRejects
                    self.CalcUnits(self.InjectionsDiff)
                    self.CalcUnitsReportedOK
                    self.CalcOriginalJobData(self.InjectionsDiff)
        if pCalcTimes == True:
            self.CalcTimes
            self.CalcEffectiveData
            self.CalcCycleTimeParams
            self.CalcTimeLeftHr
        if pCalcMaterial == True:
            self.MaterialCalc
        
        if pCalcTimes == True:
            self.CalcEfficiencies
        if self.Status == 10 and  ( self.PConfigID == 0 or  ( self.PConfigID != 0 and self.IsPConfigMain == True ) ) :
            self.UpdateMachineControlParams
            self.CalcMoldChangeDetails
            self.Mold.CalcInjections(self.InjectionsDiff, self.MachineID)
        self.Update
        if not ( self.ActiveJosh is None ) :
            if self.ActiveJosh.ID != 0:
                self.ActiveJosh.DetailsCalc(pCalcTimes, pCalcMaterial)
        
        if self.PConfigID != 0 and self.IsPConfigMain == True:
            for tVariant in self.PConfigJobs:
                tChildJob = tVariant
                tChildJob.DetailsCalc(pCalcTimes, pCalcMaterial)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.DetailsCalc:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        tChildJob = None

    def EndSetUp(self, pRejectReasonID, pTechnicianUserID=0, pFromEndJob=False):
        strSQL = ''

        tVariant = None

        tJob = Job()

        tUnitsProduced = 0

        RstCursor = None

        tMaterialCalc = False

        temp = ''

        tParam = ControlParam()

        TRst = None

        IncludeInRejectsTotal = False
        
        
        
        
        if self.SetUpEnd > 0:
            return
        self.SetUpEnd = mdl_Common.NowGMT
        self.SetupDuration = DateDiff('n', self.SetUpStart, self.SetUpEnd)
        self.SetUpEndInjectionsCount = self.InjectionsCount
        self.SetUpEndActiveTimeMin = self.EffectiveActiveTimeMin
        
        self.SetUpEndAutoRejects = self.AutoRejects
        
        if MdlADOFunctions.fGetRstValBool(self.Machine.AllowAutoRejectsOnSetup, True) == False:
            strSQL = 'Select * From TblControllerFields Where RejectReasonID > 0 AND MachineID = ' + self.Machine.ID
            RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            RstCursor.ActiveConnection = None
            while ( not RstCursor.EOF ):
                temp = RstCursor.Fields('FieldName').value
                if self.Machine.GetParam(temp, tParam) == True:
                    
                    if tParam.RejectReasonID > 0 and self.ID > 0:
                        strSQL = 'SELECT SUM(Amount) as RejectsAmount FROM TblRejects Where JobID = ' + str(self.ID) + ' AND ReasonID =' + tParam.RejectReasonID
                        TRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                        tParam.RejectsA = MdlADOFunctions.fGetRstValDouble(TRst.RejectsAmount)
                        TRst.Close()
                        tParam.RejectsALast = tParam.RejectsA
                RstCursor.MoveNext()
            RstCursor.close()
        if not self.ActiveJosh is None:
            self.ActiveJosh.SetupDuration = self.ActiveJosh.EffectiveDurationMin
            self.ActiveJosh.SetUpEndInjectionsCount = self.ActiveJosh.InjectionsCount
            strSQL = 'UPDATE TblJosh SET '
            strSQL = strSQL + 'SetUpEndInjectionsCount = InjectionsCount '
            strSQL = strSQL + 'WHERE JobID = ' + str(self.ID) + ' AND ID < ' + self.ActiveJosh.ID
            CN.Execute(strSQL)
        
        if self.PConfigParentJob is None:
            strSQL = 'INSERT INTO TblProductSetupHistory'
            strSQL = strSQL + ' (CurrentJobID,LastJobID,SetupDuration)'
            strSQL = strSQL + ' VALUES (' + str(self.ID) + ',' + self.LastJobID + ',' + self.SetupDuration + ')'
            CN.Execute(strSQL)
        
        if self.Machine.AddRejectsOnSetupEnd == True:
            IncludeInRejectsTotal = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('IncludeInRejectsTotal', 'STbDefectReasons', 'ID = 100', 'CN'), True)
            strSQL = 'SELECT ID,TotalUnitsJosh,MaterialTotal FROM TblJosh WHERE JobID = ' + str(self.ID) + ' ORDER BY ID'
            RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            RstCursor.ActiveConnection = None
            if RstData:
                if self.UnitsProduced > 0 and self.Machine.IsOffline == False:
                    self.AddRejects(self.UnitsProduced, self.MaterialTotal, pRejectReasonID, False, VBGetMissingArgument(self.AddRejects, 4), VBGetMissingArgument(self.AddRejects, 5), VBGetMissingArgument(self.AddRejects, 6), VBGetMissingArgument(self.AddRejects, 7), IncludeInRejectsTotal)
            elif RstData:
                while not RstCursor.EOF:
                    if MdlADOFunctions.fGetRstValDouble(RstCursor.TotalUnitsJosh) > 0 and self.Machine.IsOffline == False:
                        self.AddRejects(MdlADOFunctions.fGetRstValDouble(RstCursor.TotalUnitsJosh), MdlADOFunctions.fGetRstValDouble(RstCursor.MaterialTotal), pRejectReasonID, False, VBGetMissingArgument(self.AddRejects, 4), VBGetMissingArgument(self.AddRejects, 5), VBGetMissingArgument(self.AddRejects, 6), MdlADOFunctions.fGetRstValLong(RstCursor.ID), IncludeInRejectsTotal)
                        if MdlADOFunctions.fGetRstValLong(RstCursor.ID) != self.ActiveJosh.ID:
                            self.Machine.Server.MachineJoshDetailsCalc(self.Machine.ID, MdlADOFunctions.fGetRstValLong(RstCursor.ID), 1, 0)
                    RstCursor.MoveNext()
            RstCursor.close()
        self.SetupMaterialTotal = self.MaterialTotal
        
        if not ( self.OpenEvent is None ) :
            if self.Machine.SetupEventIDOnSetupEnd == 2:
                self.OpenEvent.EndEvent(True, pTechnicianUserID)
            else:
                self.OpenEvent.EndEvent(False, pTechnicianUserID)
        self.OpenEvent = None
        self.Machine.NewJob = False
        
        if not ( self.OpenWorkingEvent is None ) :
            self.OpenWorkingEvent.EndEvent
        self.OpenWorkingEvent = None
        
        if self.PConfigID != 0 and self.IsPConfigMain == True:
            for tVariant in self.PConfigJobs:
                tJob = tVariant
                tJob.EndSetUp(pRejectReasonID, pTechnicianUserID, pFromEndJob)
            
            self.Machine.FireEventTriggeredTasks(3)
        
        if self.Status == 10 and self.Machine.IsOffline == False:
            tMaterialCalc = False
        else:
            tMaterialCalc = True
        self.DetailsCalc(True, tMaterialCalc)
        
        if not pFromEndJob:
            if self.PConfigParentJob is None:
                self.Machine.MachineStop = False
                self.Machine.CalculateStatus
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.EndSetUp:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
            
        RstCursor = None
        tJob = None

    def AddRejects(self, pAmount, pWeight, pReasonID, pUpdateExistingRecord, pAutomaticRejectUpdate=False, pRejectReasonOption=0, pAddAmountOrWeightToCurrentRecord=False, pSpecificJoshID=0, pIncludeInRejectsTotal=True):
        strSQL = ''

        RstCursor = None

        tUnitWeight = 0.0

        tAmount = 0.0

        tWeight = 0.0

        tWaste = 0.0

        tRecordCriteria = ''

        tExistingRecordID = 0

        tExistingRecordAmount = 0.0

        tExistingReocrdWeight = 0.0

        tJoshID = 0

        tShiftID = 0

        tExistingRecordWeight = 0.0
        
        tUnitWeight = self.GetUnitWeight()
        
        if pSpecificJoshID != 0:
            tJoshID = pSpecificJoshID
            tShiftID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ShiftID', 'TblJosh', 'ID = ' + tJoshID, 'CN'))
        else:
            tJoshID = self.ActiveJosh.ID
            tShiftID = self.Machine.Server.CurrentShiftID
        
        if pWeight == 0:
            tWeight = pAmount * tUnitWeight
            tWeight = tWeight / 1000
        else:
            tWeight = pWeight
        tWaste = tWeight
        tAmount = pAmount
        if pUpdateExistingRecord == False:
            strSQL = 'INSERT INTO TblRejects'
            strSQL = strSQL + ' (ReasonID, JobID, MachineID, ProductID, MoldID, ReportTime, ShiftID, Amount, AutomaticRejectUpdate, Weight, JoshID, Waste, IncludeInRejectsTotal)'
            strSQL = strSQL + ' VALUES (' + pReasonID + ',' + str(self.ID) + ',' + self.Machine.ID + ',' + str(self.Product.ID) + ',' + self.Mold.ID + ',\'' + ShortDate(mdl_Common.NowGMT(), True, True) + '\',' + tShiftID + ',' + tAmount + ',' + IIf(pAutomaticRejectUpdate == True, 1, 0) + ',' + tWeight + ',' + tJoshID + ',' + tWaste + ',' + IIf(pIncludeInRejectsTotal == True, 1, 0) + ')'
            CN.Execute(strSQL)
        else:
            tRecordCriteria = 'JobID = ' + str(self.ID) + ' AND ReasonID = ' + pReasonID
            if pRejectReasonOption == 2:
                tRecordCriteria = tRecordCriteria + ' AND JoshID = ' + self.ActiveJosh.ID
            tExistingRecordID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblRejects', tRecordCriteria))
            if tExistingRecordID == 0:
                strSQL = 'INSERT INTO TblRejects'
                strSQL = strSQL + ' (ReasonID, JobID, MachineID, ProductID, MoldID, ReportTime, ShiftID, Amount, AutomaticRejectUpdate, Weight, JoshID, Waste, IncludeInRejectsTotal)'
                strSQL = strSQL + ' VALUES (' + pReasonID + ',' + str(self.ID) + ',' + self.Machine.ID + ',' + str(self.Product.ID) + ',' + self.Mold.ID + ',\'' + ShortDate(mdl_Common.NowGMT(), True, True) + '\',' + tShiftID + ',' + tAmount + ',' + IIf(pAutomaticRejectUpdate == True, 1, 0) + ',' + round(tWeight, 5) + ',' + tJoshID + ',' + round(tWaste, 5) + ',' + IIf(pIncludeInRejectsTotal == True, 1, 0) + ')'
                CN.Execute(strSQL)
            else:
                if pAddAmountOrWeightToCurrentRecord == True:
                    RstCursor = None
                    strSQL = 'SELECT Amount,Weight FROM TblRejects WHERE ID = ' + tExistingRecordID
                    RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                    RstCursor.ActiveConnection = None
                    if RstData:
                        tExistingRecordAmount = MdlADOFunctions.fGetRstValDouble(RstCursor.Amount)
                        tExistingRecordWeight = MdlADOFunctions.fGetRstValDouble(RstCursor.Weight)
                    RstCursor.close()
                    tAmount = tExistingRecordAmount + tAmount
                    tWeight = tExistingRecordWeight + tWeight
                tWaste = tWeight
                
                strSQL = 'UPDATE TblRejects'
                strSQL = strSQL + ' SET Amount = ' + tAmount + ', Weight = ' + round(tWeight, 5) + ', Waste = ' + round(tWaste, 5) + ', ReportTime = \'' + ShortDate(mdl_Common.NowGMT(), True, True) + '\', IncludeInRejectsTotal = ' + IIf(pAutomaticRejectUpdate == True, 1, 0)
                strSQL = strSQL + ' WHERE ID = ' + tExistingRecordID
                CN.Execute(strSQL)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.AddRejects:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
            
        RstCursor = None

    def GetUnitWeight(self):
        returnVal = None
        tParam = ControlParam()

        tUnitWeight = 0.0

        tProductWeight = 0.0
        
        if self.Status == 10:
            if self.Machine.GetParam('UnitWeight', tParam) == True:
                tUnitWeight = MdlADOFunctions.fGetRstValDouble(tParam.LastValue)
                if tUnitWeight == 0:
                    tUnitWeight = tParam.Mean
            else:
                if self.Machine.GetParam('ProductWeightLast', tParam) == True:
                    tProductWeight = MdlADOFunctions.fGetRstValDouble(tParam.LastValue)
                    if tProductWeight == 0:
                        tProductWeight = MdlADOFunctions.fGetRstValDouble(tParam.Mean)
                    tProductWeight = tProductWeight - self.Mold.Angus
                    tUnitWeight = tProductWeight / self.CavitiesActual
                else:
                    if self.Machine.GetParam('ProductWeight', tParam) == True:
                        tProductWeight = MdlADOFunctions.fGetRstValDouble(tParam.LastValue)
                        if tProductWeight == 0:
                            tProductWeight = MdlADOFunctions.fGetRstValDouble(tParam.Mean)
                        tProductWeight = tProductWeight - self.Mold.Angus
                        tUnitWeight = tProductWeight / self.CavitiesActual
                    else:
                        
                        tUnitWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, 'UnitWeight', 0, 0))
                        if tUnitWeight == 0:
                            tProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, 'ProductWeight', 0, 0))
                            tProductWeight = tProductWeight - self.Mold.Angus
                            tUnitWeight = round(tProductWeight / self.CavitiesActual, 5)
        else:
            tUnitWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, 'UnitWeight', 0, 0))
            if tUnitWeight == 0:
                tProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, 'ProductWeight', 0, 0))
                tProductWeight = tProductWeight - self.Mold.Angus
                tUnitWeight = round(tProductWeight / self.CavitiesActual, 5)
        returnVal = tUnitWeight
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetUnitWeight:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        return returnVal

    def CheckAutomaticSetupEnd(self):
        
        if self.Machine.NewJob:
            if self.MachineType.SetupEndCyclesSource == 1 and self.JobDef > 0 and self.JobDefSetUpEndGeneralCycles > 0:
                if self.JobDefSetUpEndGeneralCycles == 1:
                    
                    
                    if self.InjectionsCount >= 0:
                        self.EndSetUp(100)
                else:
                    if self.InjectionsCount >= self.JobDefSetUpEndGeneralCycles:
                        self.EndSetUp(100)
            elif self.MachineType.SetupEndCyclesSource == 2 and self.PlannedSetupType > 0 and self.SetupTypeSetUpEndGeneralCycles > 0:
                if self.SetupTypeSetUpEndGeneralCycles == 1:
                    
                    
                    if self.InjectionsCount >= 0:
                        self.EndSetUp(100)
                else:
                    if self.InjectionsCount >= self.SetupTypeSetUpEndGeneralCycles:
                        self.EndSetUp(100)
            else:
                if self.Machine.SetUpEndGeneralCycles > 0:
                    if self.Machine.SetUpEndGeneralCycles == 1:
                        
                        
                        if self.InjectionsCount >= 0:
                            self.EndSetUp(100)
                    else:
                        if self.InjectionsCount >= self.Machine.SetUpEndGeneralCycles:
                            self.EndSetUp(100)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CheckAutomaticSetupEnd:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def MaterialCalc(self):
        tVariant = None

        tChannel = Channel()

        tMaterialTotal = 0.0

        tMainMaterialTotal = 0.0

        tAdditiveMaterialTotal = 0.0

        tMaterialTotalMainPC = 0.0

        tMaterialTotalAdditivePC = 0.0

        tMainMaterialStandard = 0.0

        tMaterialTotalStandard = 0.0

        tAdditiveMaterialStandard = 0.0

        tMainMaterialStandardPC = 0.0

        tAdditiveMaterialStandardPC = 0.0

        tMaterialActualIndex = 0.0

        tMaterialStandardIndex = 0.0
        
        self.GetProductWeight
        for tVariant in self.ControllerChannels:
            tChannel = tVariant
            tChannel.Calc(MaterialCalcObjectType.FromJob, self, None)
            if tChannel.ChannelNum != 100:
                tMaterialTotal = tMaterialTotal + tChannel.GetTotalWeight(MaterialCalcObjectType.FromJob)
                tMaterialActualIndex = tMaterialActualIndex + tChannel.GetMaterialActualIndex(MaterialCalcObjectType.FromJob)
                tMaterialStandardIndex = tMaterialStandardIndex + tChannel.GetMaterialStandardIndex(MaterialCalcObjectType.FromJob)
                tMaterialTotalStandard = tMaterialTotalStandard + tChannel.GetTotalWeightStandard(MaterialCalcObjectType.FromJob)
                
                tMainMaterialTotal = tMainMaterialTotal + tChannel.GetRawMaterialTotalWeight(MaterialCalcObjectType.FromJob)
                tMainMaterialStandard = tMainMaterialStandard + tChannel.GetRawMaterialStandardWeight(MaterialCalcObjectType.FromJob)
                tMaterialTotalMainPC = tMaterialTotalMainPC + tChannel.GetRawMaterialPCTarget
                tMainMaterialStandardPC = tMainMaterialStandardPC + tChannel.GetRawMaterialPCTarget
                
                tMaterialTotalAdditivePC = tMaterialTotalAdditivePC + tChannel.GetAdditiveMaterialPCTarget
                tAdditiveMaterialStandardPC = tAdditiveMaterialStandardPC + tChannel.GetAdditiveMaterialPCTarget
                tAdditiveMaterialTotal = tAdditiveMaterialTotal + tChannel.GetAdditiveMaterialTotalWeight(MaterialCalcObjectType.FromJob)
                tAdditiveMaterialStandard = tAdditiveMaterialStandard + tChannel.GetAdditiveMaterialStandardWeight(MaterialCalcObjectType.FromJob)
        
        
        
        self.MaterialTotal = round(tMaterialTotal, 5)
        self.MaterialTotalMainPC = round(tMaterialTotalMainPC, 5)
        self.MaterialTotalAdditivePC = round(tMaterialTotalAdditivePC, 5)
        self.MainMaterialTotal = round(tMainMaterialTotal, 5)
        self.MainMaterialStandard = round(tMainMaterialStandard, 5)
        self.MainMaterialStandardPC = round(tMainMaterialStandardPC, 5)
        self.AdditiveMaterialTotal = round(tAdditiveMaterialTotal, 5)
        self.AdditiveMaterialStandard = round(tAdditiveMaterialStandard, 5)
        self.AdditiveMaterialStandardPC = round(tAdditiveMaterialStandardPC, 5)
        if self.MaterialTotal > 0:
            self.MainMaterialStandardCalcPC = round(self.MainMaterialTotal / self.MaterialTotal * 100, 5)
            self.AdditiveMaterialStandardCalcPC = round(self.AdditiveMaterialTotal / self.MaterialTotal * 100, 5)
        else:
            self.MainMaterialStandardCalcPC = 100
            self.AdditiveMaterialStandardCalcPC = 100
        self.MainMaterialStandardPCCalcC = round(self.MaterialTotalMainPC - self.MainMaterialStandardPC, 5)
        self.AdditiveMaterialStandardPCCalcC = round(self.MaterialTotalAdditivePC - self.AdditiveMaterialStandardPC, 5)
        if self.ProductionTimeMin > 0:
            self.MaterialConsumptionKgtoHour = round(( self.MainMaterialTotal + self.AdditiveMaterialTotal )  /  ( self.ProductionTimeMin / 60 ), 10)
        else:
            self.MaterialConsumptionKgtoHour = 0
        if self.CyclesNetActual != 0:
            self.CycleWeightActualAvg = round(( self.MainMaterialTotal + self.AdditiveMaterialTotal )  / self.CyclesNetActual, 10)
        else:
            self.CycleWeightActualAvg = 0
        self.MaterialActualIndex = round(tMaterialActualIndex, 5)
        self.MaterialStandardIndex = round(tMaterialStandardIndex, 5)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.MaterialCalc:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        tChannel = None

    def CalcCycleTimeParams(self):
        
        if self.SetUpEnd != 0:
            if self.Machine.MonitorSetupWorkingTime or not self.Machine.AddRejectsOnSetupEnd:
                if ( self.InjectionsCount )  > 0:
                    self.CycleTimeAvg = round(self.ProductionTimeMin /  ( self.InjectionsCount - self.InjectionsCountStart )  * 60, 5)
                    
                    
            else:
                if ( self.InjectionsCount - self.SetUpEndInjectionsCount )  > 0:
                    self.CycleTimeAvg = round(self.ProductionTimeMin /  ( self.InjectionsCount - self.SetUpEndInjectionsCount )  * 60, 5)
                    
                    
        else:
            if self.Machine.MonitorSetupWorkingTime:
                if ( self.InjectionsCount - self.InjectionsCountStart )  > 0:
                    
                    
                    self.CycleTimeAvg = round(self.ProductionTimeMin /  ( self.InjectionsCount - self.InjectionsCountStart )  * 60, 5)
                    
                    
            else:
                if ( self.InjectionsCount - self.InjectionsCountStart )  > 0:
                    
                    
                    
                    
                    self.CycleTimeAvg = self.CycleTimeStandard
                    
                    
        
        
        
        
        
        
        
        
        
        
        
        
        
        if self.CycleTimeAvgSMean > 0:
            self.CycleTimeAvgDiff = self.CycleTimeAvgSMean - self.CycleTimeStandard
        else:
            self.CycleTimeAvgDiff = self.CycleTimeAvg - self.CycleTimeStandard
        if self.CycleTimeStandard != 0:
            self.CycleTimeAvgDiffPC = round(self.CycleTimeAvgDiff / self.CycleTimeStandard * 100, 5)
        else:
            self.CycleTimeAvgDiffPC = 0
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcCycleTimeParams:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def CalcEffectiveData(self):
        
        self.EffectiveDurationMin = self.DurationMin * self.PConfigPC / 100
        self.EffectiveDownTimeMin = self.DownTimeMin * self.PConfigPC / 100
        self.EffectiveInActiveTimeMin = self.ActiveTimeMin * self.PConfigPC / 100
        self.EffectiveActiveTimeMin = self.ActiveTimeMin * self.PConfigPC / 100
        self.EffectiveProductionTimeMin = self.ProductionTimeMin * self.PConfigPC / 100
        self.EffectiveSetupDurationMin = self.SetupDuration * self.PConfigPC / 100
        if self.UnitsProduced != 0:
            self.EffectiveCycleTime = self.EffectiveProductionTimeMin / self.UnitsProduced
        else:
            self.EffectiveCycleTime = self.CycleTimeStandard
        self.EffectiveWeight = self.ProductWeightAvg / self.PConfigUnits
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcEffectiveData:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def CalcTimes(self):
        tCycleTimeForTimeLeftHR = 0.0
        
        if self.Machine.ID == 38:
            tCycleTimeForTimeLeftHR = tCycleTimeForTimeLeftHR
        
        if self.Status == 10:
            
            self.DurationMin = MdlADOFunctions.fGetRstValLong(round(( DateDiff('s', self.StartTime, mdl_Common.NowGMT()) )  / 60, 5))
        self.CalcTimesFromDB
        self.ActiveTimeMin = self.DurationMin - self.InActiveTimeMin
        self.ProductionTimeMin = self.ActiveTimeMin - self.DownTimeMin
        
        
        if self.Status == 10:
            if not self.OpenEvent is None:
                if self.OpenEvent.ID > 0:
                    
                    self.ProductionTimeMin = self.ProductionTimeMin - MdlADOFunctions.fGetRstValLong(round(( DateDiff('s', self.OpenEvent.EventTime, mdl_Common.NowGMT()) )  / 60, 5))
        if self.ProductionTimeMin < 0:
            self.ProductionTimeMin = 0
        if self.ActiveTimeMin < 0:
            self.ActiveTimeMin = 0
        
        if self.DurationMin != 0:
            self.ProductionUsabilityPC = self.ProductionTimeMin / self.DurationMin * 100
            self.InActiveTimePC = self.InActiveTimeMin / self.DurationMin * 100
            self.ActiveTimePC = self.ActiveTimeMin / self.DurationMin * 100
        else:
            self.ProductionUsabilityPC = 0
            self.InActiveTimePC = 0
            self.ActiveTimePC = 0
        if self.ActiveTimeMin != 0:
            self.DownTimePC = self.DownTimeMin / self.ActiveTimeMin * 100
            self.ProductionTimePC = self.ProductionTimeMin / self.ActiveTimeMin * 100
        else:
            self.DownTimePC = 0
            self.ProductionTimePC = 0
        
        
        if self.Machine.NewJob:
            self.SetUpProductionTimeMin = self.ProductionTimeMin
            self.SetUpDownTimeMin = self.DownTimeMin
        else:
            
            self.SetUpDownTimeMin = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('DownTimeMin', 'ViewRTJobSetupEvents', 'ID = ' + str(self.ID), 'CN'))
        self.CalcEngineTimesFromDB
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcTimes:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def __CalcTimeLeftHr(self):
        tCycleTimeForTimeLeftHR = 0.0
        
        
        if (self.Machine.Server.SystemVariables.CycleTimeCalc == CycleTimeCalcOption.Last):
            tCycleTimeForTimeLeftHR = self.CycleTimeLast
        elif (self.Machine.Server.SystemVariables.CycleTimeCalc == CycleTimeCalcOption.Avg50):
            tCycleTimeForTimeLeftHR = self.CycleTimeAvgSMean
        elif (self.Machine.Server.SystemVariables.CycleTimeCalc == CycleTimeCalcOption.Standard):
            tCycleTimeForTimeLeftHR = self.CycleTimeStandard
        elif (self.Machine.Server.SystemVariables.CycleTimeCalc == CycleTimeCalcOption.Avg):
            tCycleTimeForTimeLeftHR = self.CycleTimeAvg
        else:
            tCycleTimeForTimeLeftHR = self.CycleTimeStandard
        if self.Machine.NewJob == True:
            tCycleTimeForTimeLeftHR = self.CycleTimeStandard
        
        if tCycleTimeForTimeLeftHR == 0:
            tCycleTimeForTimeLeftHR = self.CycleTimeStandard
        
        if tCycleTimeForTimeLeftHR == 0:
            tCycleTimeForTimeLeftHR = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, 'CycleTime', 0, 0))
        self.TimeLeftHr = round(tCycleTimeForTimeLeftHR * self.UnitsProducedLeft /  ( 60 * self.PConfigUnits ), 5)
        if self.TimeLeftHr < 0:
            self.TimeLeftHr = 0
        if self.PConfigID == 0 and  ( self.PConfigID != 0 and self.IsPConfigMain == True ) :
            self.Machine.TimeLeftHr = self.TimeLeftHr
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcTimeLeftHr:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def __CalcTimesFromDB(self):
        strSQL = ''

        RstCursor = None
        
        strSQL = 'SELECT DownTimeMin,InActiveTimeMin FROM ViewRTJobEvents WHERE ID = ' + str(self.ID)
        RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        RstCursor.ActiveConnection = None
        if RstData:
            self.DownTimeMin = MdlADOFunctions.fGetRstValLong(RstCursor.DownTimeMin)
            self.InActiveTimeMin = MdlADOFunctions.fGetRstValLong(RstCursor.InActiveTimeMin)
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
                
            MdlGlobal.RecordError(type(self).__name__ + '.CalcTimesFromDB:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        RstCursor = None

    def CalcEfficiencies(self):
        
        if self.ID == 20383:
            self.CycleTimeEfficiency = self.CycleTimeEfficiency
        
        if ( self.Machine.ProductionModeCalcEfficiencies and self.Machine.ProductionModeID > 1 ) or ( self.Machine.ProductionModeID == 1 and  ( ( self.Machine.ProductionModeCalcEfficiencies and self.JobDef == 0 )  or  ( self.JobDef > 0 and self.JobDefCalcEfficiencies ) ) ):
            if self.CycleTimeAvg != 0:
                self.CycleTimeEfficiency = round(self.CycleTimeStandard / self.CycleTimeAvg, 5)
            else:
                self.CycleTimeEfficiency = 0
        else:
            self.CycleTimeEfficiency = 1
        
        if ( self.Machine.ProductionModeCalcEfficiencies and self.Machine.ProductionModeID > 1 ) or ( self.Machine.ProductionModeID == 1 and  ( ( self.Machine.ProductionModeCalcEfficiencies and self.JobDef == 0 )  or  ( self.JobDef > 0 and self.JobDefCalcEfficiencies ) ) ):
            if self.UnitsProduced != 0:
                self.RejectsEfficiency = round(( self.UnitsProduced - self.RejectsForEfficiency )  / self.UnitsProduced, 5)
            else:
                self.RejectsEfficiency = 1
        else:
            self.RejectsEfficiency = 1
        
        
        if self.ActiveTimeMin != 0:
            self.DownTimeEfficiency = round(( self.ProductionTimeMin / self.ActiveTimeMin ), 5)
        else:
            self.DownTimeEfficiency = 0
        
        if self.DurationMin != 0:
            self.DownTimeEfficiencyOEE = round(( self.ProductionTimeMin / self.DurationMin ), 5)
        else:
            self.DownTimeEfficiencyOEE = 0
        
        if ( self.Machine.ProductionModeCalcEfficiencies and self.Machine.ProductionModeID > 1 ) or ( self.Machine.ProductionModeID == 1 and  ( ( self.Machine.ProductionModeCalcEfficiencies and self.JobDef == 0 )  or  ( self.JobDef > 0 and self.JobDefCalcEfficiencies ) ) ):
            if self.PConfigID == 0:
                self.CavitiesEfficiency = round(self.CavitiesActual / self.CavitiesStandard, 5)
                self.CavitiesPC = round(( self.CavitiesActual / self.CavitiesStandard )  * 100, 5)
            else:
                self.CavitiesEfficiency = 1
                self.CavitiesPC = 100
        else:
            self.CavitiesEfficiency = 1
            self.CavitiesPC = 100
        self.EfficiencyTotal = 0
        self.PEE = 0
        
        if self.CavitiesEfficiency > 0 and self.Department.CavitiesEffFactor > 0:
            self.EfficiencyTotal = round(( self.CavitiesEfficiency )  * self.Department.CavitiesEffFactor, 5)
            self.PEE = round(( self.CavitiesEfficiency )  * self.Department.CavitiesEffFactor, 5)
        elif self.Department.CavitiesEffFactor == 0:
            self.CavitiesEfficiency = 1
        if self.RejectsEfficiency > 0 and self.Department.RejectsEffFactor > 0:
            if self.EfficiencyTotal > 0:
                self.EfficiencyTotal = round(self.EfficiencyTotal * self.RejectsEfficiency * self.Department.RejectsEffFactor, 5)
            else:
                self.EfficiencyTotal = round(self.RejectsEfficiency * self.Department.RejectsEffFactor, 5)
            if self.PEE > 0:
                self.PEE = round(self.PEE * self.RejectsEfficiency * self.Department.RejectsEffFactor, 5)
            else:
                self.PEE = round(self.RejectsEfficiency * self.Department.RejectsEffFactor, 5)
        elif self.Department.RejectsEffFactor == 0:
            self.RejectsEfficiency = 1
        if self.CycleTimeEfficiency > 0 and self.Department.CycleTimeEffFactor > 0:
            if self.EfficiencyTotal > 0:
                self.EfficiencyTotal = round(self.EfficiencyTotal * self.CycleTimeEfficiency * self.Department.CycleTimeEffFactor, 5)
            else:
                self.EfficiencyTotal = round(self.CycleTimeEfficiency * self.Department.CycleTimeEffFactor, 5)
            if self.PEE > 0:
                self.PEE = round(self.PEE * self.CycleTimeEfficiency * self.Department.CycleTimeEffFactor, 5)
            else:
                self.PEE = round(self.CycleTimeEfficiency * self.Department.CycleTimeEffFactor, 5)
        elif self.Department.CycleTimeEffFactor == 0:
            self.CycleTimeEfficiency = 1
        if self.Department.MachineTimeEffFactor > 0:
            if self.EfficiencyTotal > 0:
                self.EfficiencyTotal = round(self.EfficiencyTotal * self.DownTimeEfficiencyOEE * self.Department.MachineTimeEffFactor, 5)
            else:
                self.EfficiencyTotal = round(self.DownTimeEfficiencyOEE * self.Department.MachineTimeEffFactor, 5)
            if self.PEE > 0:
                self.PEE = round(self.PEE * self.DownTimeEfficiency * self.Department.MachineTimeEffFactor, 5)
            else:
                self.PEE = round(self.DownTimeEfficiency * self.Department.MachineTimeEffFactor, 5)
        elif self.Department.MachineTimeEffFactor == 0:
            self.DownTimeEfficiency = 1
            self.DownTimeEfficiencyOEE = 1
        
        if ( self.MaterialRecipeIndexProduct * self.CyclesNetActual )  > 0 and  ( self.MaterialRecipeIndexJob * self.CyclesNetActual )  > 0:
            
            self.TotalMaterialEfficiencyTheoretical = round(( self.MaterialRecipeIndexProduct )  /  ( self.MaterialRecipeIndexJob ), 10)
        else:
            self.TotalMaterialEfficiencyTheoretical = 1
        
        if self.MaterialActualIndex != 0:
            self.TotalMaterialEfficiencyActual = round(( self.MaterialStandardIndex / self.MaterialActualIndex ), 10)
        else:
            self.TotalMaterialEfficiencyActual = 0
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if ( self.Department.EquipmentRelativePortion + self.Department.MaterialRelativePortion )  != 0:
            self.TotalEquipmentMaterialEfficency = ( ( self.TotalMaterialEfficiencyActual * self.Department.MaterialRelativePortion )  +  ( self.EfficiencyTotal * self.Department.EquipmentRelativePortion ) )  /  ( self.Department.EquipmentRelativePortion + self.Department.MaterialRelativePortion )
        else:
            self.TotalEquipmentMaterialEfficency = 1
        if self.TotalEquipmentMaterialEfficency <= 0:
            self.TotalEquipmentMaterialEfficency = 1
        if self.EfficiencyTotal > 2:
            self.EfficiencyTotal = 2
        if self.PEE > 2:
            self.PEE = 2
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcEfficiencies:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
            

    def CalcRejects(self):
        strSQL = ''

        RstCursor = None
        
        strSQL = 'SELECT * FROM ViewRTJobRejects WHERE ID = ' + str(self.ID)
        RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        RstCursor.ActiveConnection = None
        if RstData:
            self.RejectsTotal = MdlADOFunctions.fGetRstValDouble(RstCursor.RejectsTotal)
            self.RejectsReported = MdlADOFunctions.fGetRstValDouble(RstCursor.RejectsReported)
            self.TotalWasteKg = MdlADOFunctions.fGetRstValDouble(RstCursor.TotalWasteKg)
            self.RejectsForEfficiency = MdlADOFunctions.fGetRstValDouble(RstCursor.RejectsForEfficiency)
            self.RejectsForConsumption = MdlADOFunctions.fGetRstValDouble(RstCursor.RejectsForConsumption)
            self.QuantityAdjustmentUnits = MdlADOFunctions.fGetRstValDouble(RstCursor.QuantityAdjustmentUnits)
        RstCursor.close()
        self.ReportedRejectsDiff = self.RejectsRead - self.RejectsTotal
        if self.ReportedRejectsDiff < 0:
            self.ReportedRejectsDiff = 0
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.CalcRejects:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        RstCursor = None

    def CalcOriginalJobData(self, pInjectionsDiff):
        
        
        
        
        
        self.OriginalUnitsProducedOK = self.OriginalUnitsProducedOK + self.UnitsProducedOKDiff
        self.UnitsProducedOKDiff = 0
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcOriginalJobData:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def CalcUnits(self, pInjectionsDiff):
        MachinePEETarget = 0.0

        tSetupDuration = 0.0
        
        
        if self.Machine.IsOffline == False:
            self.UnitsProduced = self.UnitsProduced +  ( pInjectionsDiff * self.CavitiesActual )
        
        self.UnitsProducedOKDiff = ( self.UnitsProduced - self.RejectsTotal )  - self.UnitsProducedOK
        
        
        self.UnitsProducedOK = self.UnitsProduced - self.RejectsTotal + self.QuantityAdjustmentUnits
        
        self.UnitsProducedLeft = round(self.UnitsTarget - self.UnitsProducedOK, 5)
        if self.Machine.Server.SystemVariables.UnitsProducedLeftZero == True and self.UnitsProducedLeft < 0:
            self.UnitsProducedLeft = 0
        
        self.UnitsProducedPC = round(self.UnitsProducedOK / self.UnitsTarget * 100, 5)
        if self.UnitsProduced != 0:
            self.RejectsPC = round(self.RejectsTotal / self.UnitsProduced * 100, 5)
        
        if self.Machine.AddRejectsOnSetupEnd and self.Machine.NewJob:
            self.UnitsProducedTheoretically = 0
            self.UnitsProducedTheoreticallyPC = 0
        else:
            if self.Machine.AddRejectsOnSetupEnd:
                tSetupDuration = self.SetupDuration
            else:
                tSetupDuration = 0
            MachinePEETarget = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('PEETarget', 'TblMachines', 'ID = ' + self.Machine.ID, 'CN'))
            if MachinePEETarget < 0.1 or MachinePEETarget > 2:
                MachinePEETarget = 1
            if self.CycleTimeStandard == 0 or self.CavitiesActual == 0:
                self.UnitsProducedTheoretically = 0
            else:
                self.UnitsProducedTheoretically = round(( ( self.ActiveTimeMin - tSetupDuration )  /  ( ( self.CycleTimeStandard / 60 )  / self.CavitiesActual ) )  * MachinePEETarget, 2)
            if self.UnitsProducedTheoretically != 0:
                self.UnitsProducedTheoreticallyPC = round(self.UnitsProducedOK / self.UnitsProducedTheoretically * 100, 5)
            else:
                self.UnitsProducedTheoreticallyPC = 0
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcUnits:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
            

    def __UpdateMachineControlParams(self):
        
        if self.Status == 10:
            self.Machine.SetFieldValue('UnitsProducedOK', str(self.UnitsProducedOK))
            self.Machine.SetFieldValue('UnitsTarget', str(self.UnitsTarget))
            self.Machine.SetFieldValue('TotalUnitsProducedOK', str(self.OriginalUnitsProducedOK))
            self.Machine.SetFieldValue('MoldCavities', str(self.CavitiesActual))
            self.Machine.SetFieldValue('CyclesTarget', str(self.UnitsProducedLeft / self.CavitiesActual))
            self.Machine.SetFieldValue('TimeLeftHr', str(self.TimeLeftHr))
            self.Machine.SetFieldValue('CycleTime', str(self.Machine.CycleTime))
            self.Machine.SetFieldValue('CyclesTargetPC', str(self.UnitsProducedPC))
            self.Machine.SetFieldValue('UnitsProduced', str(self.UnitsProduced))
            if self.Machine.IsOffline == True:
                self.Machine.SetFieldValue('TotalCycles', str(self.InjectionsCount))
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.UpdateMachineControlParams:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def CheckFilters(self):
        returnVal = None
        
        returnVal = False
        if not self.Machine.IgnoreCycleTimeFilter:
            if ( self.Machine.CycleTime / self.CycleTimeStandard )  < self.Machine.CycleFilterLValue or  ( self.Machine.CycleTime / self.CycleTimeStandard )  > self.Machine.CycleFilterHValue:
                self.CyclesDroped = self.CyclesDroped + self.InjectionsDiff
                returnVal = False
            else:
                returnVal = True
        else:
            returnVal = True
        self.CyclesNetActual = ( self.InjectionsCount - self.InjectionsCountStart )  - self.CyclesDroped
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CheckFilters:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        return returnVal

    def Update(self):
        strSQL = ''

        strTitle = ''
        
        strTitle = 'UPDATE TblJob '
        strSQL = 'SET '
        
        strSQL = strSQL + ' InjectionsCount = ' + self.InjectionsCount
        strSQL = strSQL + ' ,InjectionsCountLast = ' + self.InjectionsCountLast
        strSQL = strSQL + ' ,InjectionsCountStart = ' + self.InjectionsCountStart
        strSQL = strSQL + ' ,UnitsProduced = ' + self.UnitsProduced
        strSQL = strSQL + ' ,UnitsProducedOK = ' + self.UnitsProducedOK
        strSQL = strSQL + ' ,UnitsProducedLeft = ' + self.UnitsProducedLeft
        strSQL = strSQL + ' ,UnitsProducedPC = ' + self.UnitsProducedPC
        strSQL = strSQL + ' ,UnitsProducedTheoretically = ' + self.UnitsProducedTheoretically
        strSQL = strSQL + ' ,UnitsProducedTheoreticallyPC = ' + self.UnitsProducedTheoreticallyPC
        strSQL = strSQL + ' ,QuantityAdjustmentUnits = ' + self.QuantityAdjustmentUnits
        strSQL = strSQL + ' ,CyclesDroped = ' + self.CyclesDroped
        strSQL = strSQL + ' ,CyclesNetActual = ' + self.CyclesNetActual
        if self.CavitiesActual != 0:
            strSQL = strSQL + ' ,CyclesTarget = ' + CDbl(self.UnitsProducedLeft / CDbl(self.CavitiesActual))
        strSQL = strSQL + ' ,SetUpEndInjectionsCount = ' + self.SetUpEndInjectionsCount
        strSQL = strSQL + ' ,SetUpEndActiveTimeMin = ' + self.SetUpEndActiveTimeMin
        
        strSQL = strSQL + ' ,SetUpEndAutoRejects = ' + self.SetUpEndAutoRejects
        
        strSQL = strSQL + ' ,UnitsReportedOK = ' + self.UnitsReportedOK
        strSQL = strSQL + ' ,UnitsReportedOKDiff = ' + self.UnitsReportedOKDiff
        strSQL = strSQL + ' ,UnitsReportedOKDiffPC = ' + self.UnitsReportedOKDiffPC
        
        strSQL = strSQL + ' ,RejectsTotal = ' + self.RejectsTotal
        strSQL = strSQL + ' ,RejectsPC = ' + self.RejectsPC
        strSQL = strSQL + ' ,TotalWasteKg = ' + self.TotalWasteKg
        strSQL = strSQL + ' ,RejectsRead = ' + self.RejectsRead
        strSQL = strSQL + ' ,RejectsReported = ' + self.RejectsReported
        strSQL = strSQL + ' ,ReportedRejectsDiff = ' + self.ReportedRejectsDiff
        
        strSQL = strSQL + ' ,AutoRejects = ' + self.AutoRejects
        
        strSQL = strSQL + ' ,CavitiesActual = ' + self.CavitiesActual
        strSQL = strSQL + ' ,CavitiesStandard = ' + self.CavitiesStandard
        strSQL = strSQL + ' ,CavitiesPC = ' + self.CavitiesPC
        strSQL = strSQL + ' ,CavitiesEfficiency = ' + IIf(self.CavitiesEfficiency == - 999999999, 'NULL', self.CavitiesEfficiency)
        
        strSQL = strSQL + ' ,CycleTimeAvg = ' + self.CycleTimeAvg
        strSQL = strSQL + ' ,CycleTimeAvgSMean = ' + self.CycleTimeAvgSMean
        strSQL = strSQL + ' ,CycleTimeLast = ' + self.CycleTimeLast
        strSQL = strSQL + ' ,CycleTimeStandard = ' + self.CycleTimeStandard
        strSQL = strSQL + ' ,CycleTimeAvgDiff = ' + self.CycleTimeAvgDiff
        strSQL = strSQL + ' ,CycleTimeAvgDiffPC = ' + self.CycleTimeAvgDiffPC
        
        strSQL = strSQL + ' ,EffectiveActiveTimeMin = ' + self.EffectiveActiveTimeMin
        strSQL = strSQL + ' ,EffectiveCycleTime = ' + self.EffectiveCycleTime
        strSQL = strSQL + ' ,EffectiveDownTimeMin = ' + self.EffectiveDownTimeMin
        strSQL = strSQL + ' ,EffectiveDurationMin = ' + self.EffectiveDurationMin
        strSQL = strSQL + ' ,EffectiveInActiveTimeMin = ' + self.EffectiveInActiveTimeMin
        strSQL = strSQL + ' ,EffectiveProductionTimeMin = ' + self.EffectiveProductionTimeMin
        strSQL = strSQL + ' ,EffectiveSetupDurationMin = ' + self.EffectiveSetupDurationMin
        strSQL = strSQL + ' ,EffectiveWeight = ' + self.EffectiveWeight
        
        strSQL = strSQL + ' ,CycleTimeEfficiency = ' + IIf(self.CycleTimeEfficiency == - 999999999, 'NULL', self.CycleTimeEfficiency)
        strSQL = strSQL + ' ,RejectsEfficiency = ' + IIf(self.RejectsEfficiency == - 999999999, 'NULL', self.RejectsEfficiency)
        strSQL = strSQL + ' ,DownTimeEfficiency = ' + IIf(self.DownTimeEfficiency == - 999999999, 'NULL', self.DownTimeEfficiency)
        strSQL = strSQL + ' ,DownTimeEfficiencyOEE = ' + IIf(self.DownTimeEfficiencyOEE == - 999999999, 'NULL', self.DownTimeEfficiencyOEE)
        if IsDoubleNull(self.CycleTimeEfficiency) or IsDoubleNull(self.RejectsEfficiency) or IsDoubleNull(self.CavitiesEfficiency) or IsDoubleNull(self.DownTimeEfficiency) or IsDoubleNull(self.DownTimeEfficiencyOEE):
            strSQL = strSQL + ' ,EfficiencyTotal = NULL'
            strSQL = strSQL + ' ,PEE = NULL'
        else:
            strSQL = strSQL + ' ,EfficiencyTotal = ' + IIf(self.EfficiencyTotal == - 999999999, 'NULL', self.EfficiencyTotal)
            strSQL = strSQL + ' ,PEE = ' + IIf(self.PEE == - 999999999, 'NULL', self.PEE)
        strSQL = strSQL + ' ,TotalMaterialEfficiencyTheoretical = ' + self.TotalMaterialEfficiencyTheoretical
        strSQL = strSQL + ' ,TotalMaterialEfficiencyActual = ' + self.TotalMaterialEfficiencyActual
        strSQL = strSQL + ' ,TotalEquipmentMaterialEfficency = ' + self.TotalEquipmentMaterialEfficency
        
        strSQL = strSQL + ' ,DurationMin = ' + self.DurationMin
        strSQL = strSQL + ' ,ActiveTimeMin = ' + self.ActiveTimeMin
        strSQL = strSQL + ' ,ActiveTimePC = ' + self.ActiveTimePC
        strSQL = strSQL + ' ,DownTimeMin = ' + self.DownTimeMin
        strSQL = strSQL + ' ,SetUpDownTimeMin = ' + self.SetUpDownTimeMin
        strSQL = strSQL + ' ,DownTimePC = ' + self.DownTimePC
        strSQL = strSQL + ' ,InActiveTimeMin = ' + self.InActiveTimeMin
        strSQL = strSQL + ' ,InActiveTimePC = ' + self.InActiveTimePC
        strSQL = strSQL + ' ,ProductionTimeMin = ' + self.ProductionTimeMin
        strSQL = strSQL + ' ,SetUpProductionTimeMin = ' + self.SetUpProductionTimeMin
        strSQL = strSQL + ' ,ProductionTimePC = ' + self.ProductionTimePC
        strSQL = strSQL + ' ,ProductionUsabilityPC = ' + self.ProductionUsabilityPC
        strSQL = strSQL + ' ,TimeLeftHr = ' + self.TimeLeftHr
        strSQL = strSQL + ' ,EngineTimeMin = ' + self.EngineTimeMin
        
        strSQL = strSQL + ' ,OriginalUnitsTarget = ' + self.OriginalUnitsTarget
        strSQL = strSQL + ' ,OriginalUnitsProducedOK = ' + self.OriginalUnitsProducedOK
        
        strSQL = strSQL + ' ,ProductWeightLast = ' + self.ProductWeightLast
        strSQL = strSQL + ' ,ProductWeightAvg = ' + self.ProductWeightAvg
        strSQL = strSQL + ' ,ProductWeightStandard = ' + self.ProductWeightStandard
        strSQL = strSQL + ' ,ProductRecipeWeight= ' + self.ProductRecipeWeight
        strSQL = strSQL + ' ,ProductWeightDiff = ' + self.ProductWeightDiff
        strSQL = strSQL + ' ,ProductWeightDiffPC = ' + self.ProductWeightDiffPC
        strSQL = strSQL + ' ,ProductWeightPC = ' + self.ProductWeightPC
        
        strSQL = strSQL + ' ,MaterialTotal = ' + self.MaterialTotal
        strSQL = strSQL + ' ,MaterialTotalMainPC = ' + self.MaterialTotalMainPC
        strSQL = strSQL + ' ,MaterialTotalAdditivePC = ' + self.MaterialTotalAdditivePC
        strSQL = strSQL + ' ,MainMaterialTotal = ' + self.MainMaterialTotal
        strSQL = strSQL + ' ,MainMaterialStandard = ' + self.MainMaterialStandard
        strSQL = strSQL + ' ,MainMaterialStandardPC = ' + self.MainMaterialStandardPC
        strSQL = strSQL + ' ,MainMaterialStandardCalcPC = ' + self.MainMaterialStandardCalcPC
        strSQL = strSQL + ' ,MainMaterialStandardPCCalcC = ' + self.MainMaterialStandardPCCalcC
        strSQL = strSQL + ' ,AdditiveMaterialTotal = ' + self.AdditiveMaterialTotal
        strSQL = strSQL + ' ,AdditiveMaterialStandard = ' + self.AdditiveMaterialStandard
        strSQL = strSQL + ' ,AdditiveMaterialStandardPC = ' + self.AdditiveMaterialStandardPC
        strSQL = strSQL + ' ,AdditiveMaterialStandardCalcPC = ' + self.AdditiveMaterialStandardCalcPC
        strSQL = strSQL + ' ,AdditiveMaterialStandardPCCalcC = ' + self.AdditiveMaterialStandardPCCalcC
        strSQL = strSQL + ' ,MaterialConsumptionKgtoHour = ' + self.MaterialConsumptionKgtoHour
        strSQL = strSQL + ' ,CycleWeightActualAvg = ' + self.CycleWeightActualAvg
        strSQL = strSQL + ' ,MaterialActualIndex= ' + self.MaterialActualIndex
        strSQL = strSQL + ' ,MaterialStandardIndex= ' + self.MaterialStandardIndex
        strSQL = strSQL + ' ,ValidationLog = \'' + self.ValidationLog + '\''
        strSQL = strSQL + ' ,SetupMaterialTotal = ' + self.SetupMaterialTotal
        strSQL = strSQL + ' ,StartTime = \'' + ShortDate(self.StartTime, True, True, True) + '\''
        if GlobalVariables.IsDate(self.SetUpEnd) and self.SetUpEnd != 0:
            strSQL = strSQL + ' ,SetUpEnd = \'' + ShortDate(self.SetUpEnd, True, True, True) + '\''
            strSQL = strSQL + ' ,SetupDuration= ' + self.SetupDuration
        if self.NextJobMaterialFlowStart != 0:
            strSQL = strSQL + ' ,NextJobMaterialFlowStart = \'' + ShortDate(self.NextJobMaterialFlowStart, True, True, True) + '\''
        strSQL = strSQL + ' WHERE ID = ' + str(self.ID)
        CN.Execute(strTitle + strSQL)
        if self.Status == 10:
            strTitle = 'UPDATE TblJobCurrent '
            CN.Execute(strTitle + strSQL)
            
            strSQL = 'UPDATE TblMachines SET MoldEndTime = ' + self.Machine.MoldEndTime + ' WHERE ID = ' + self.Machine.ID
            CN.Execute(strSQL)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.Update:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        strSQL = vbNullString

    def GetProductWeight(self):
        tParam = ControlParam()

        tTotalDistance = 0.0

        tWeightDistanceRatio = 0.0
        
        if self.Status == 10:
            if self.Machine.GetParam('ProductWeightLast', tParam) == True:
                self.ProductWeightLast = MdlADOFunctions.fGetRstValDouble(tParam.LastValue)
                if tParam.IsSPCValue == True:
                    self.ProductWeightAvg = tParam.SMean
                else:
                    if self.Machine.GetParam('TotalDistance', tParam) == True:
                        if tParam.IsSPCValue == True:
                            tTotalDistance = round(MdlADOFunctions.fGetRstValDouble(tParam.LastValue), 5)
                            tWeightDistanceRatio = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, 'WeightDistanceRatio', 0, 0))
                            if tTotalDistance > 0 and tWeightDistanceRatio > 0:
                                self.ProductWeightAvg = round(tTotalDistance * tWeightDistanceRatio, 5)
            else:
                if self.PConfigID == 0 or  ( self.PConfigID != 0 and self.MachineType.PConfigSonsRefRecipeSource == FromPConfigParent ) :
                    if self.Machine.GetParam('ProductWeight', tParam) == True:
                        self.ProductWeightLast = MdlADOFunctions.fGetRstValDouble(tParam.LastValue)
                        self.ProductWeightStandard = MdlADOFunctions.fGetRstValDouble(tParam.Mean)
                        if tParam.IsSPCValue == True:
                            self.ProductWeightAvg = round(MdlADOFunctions.fGetRstValDouble(tParam.SMean), tParam.Precision)
                        if self.ProductWeightAvg == 0:
                            self.ProductWeightAvg = self.ProductWeightLast
            self.ProductWeightDiff = round(self.ProductWeightAvg - self.ProductWeightStandard, 5)
            if self.ProductWeightStandard != 0:
                self.ProductWeightDiffPC = round(self.ProductWeightDiff / self.ProductWeightStandard * 100, 3)
                self.ProductWeightPC = round(self.ProductWeightAvg / self.ProductWeightStandard * 100, 3)
            else:
                self.ProductWeightDiffPC = 0
                self.ProductWeightPC = 100
            self.ProductWeightDiff = round(self.ProductWeightAvg - self.ProductWeightStandard, 5)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetProductWeight:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def GetCycleTime(self):
        tParam = ControlParam()
        
        if self.Status == 10:
            if self.Machine.GetParam('CycleTime', tParam) == True:
                self.CycleTimeStandard = tParam.Mean
                if self.Machine.CalcCycleTime == True:
                    self.CycleTimeLast = MdlADOFunctions.fGetRstValDouble(self.Machine.CycleTime)
                else:
                    self.CycleTimeLast = MdlADOFunctions.fGetRstValDouble(tParam.LastValue)
                if tParam.IsSPCValue == True:
                    self.CycleTimeAvgSMean = round(MdlADOFunctions.fGetRstValDouble(tParam.SMean), 5)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.GetCycleTime:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    
    def AddAlarm(self, pAlarm):
        try:
            self.OpenAlarms[str(pAlarm.ID)] = pAlarm

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.AddAlarm:', str(0), error.args[0], 'JobID:' + str(self.ID) + '. AlarmID: ' + str(pAlarm.ID))

    def CreateJoshForNewShift(self):
        strSQL = ''

        RstCursor = None

        tJosh = Josh()

        tNewJoshID = 0

        strTitle = ''

        tNow = None

        tMaterialID = 0

        tRecipeMaterialID = 0

        tChannel = Channel()

        tVariant = None

        tMachine = self.Machine()
        
        tNow = mdl_Common.NowGMT()
        
        
        strSQL = 'SELECT * FROM TblJosh WHERE ID = 0'
        RstCursor.Open(strSQL, CN, adOpenDynamic, adLockOptimistic)
        RstCursor.AddNew()
        RstCursor.JobID = self.ID
        RstCursor.ShiftID = self.Machine.Server.CurrentShiftID
        RstCursor.ShiftDefID = self.Machine.Server.CurrentShift.ShiftDefID
        RstCursor.ShiftManagerID = self.Machine.Server.CurrentShift.ManagerID
        RstCursor.StartTime = tNow
        RstCursor.Department = self.Department.ID
        RstCursor.ControllerID = self.Machine.ControllerID
        RstCursor.UnitsTargetJob = self.UnitsTarget
        RstCursor.MachineID = self.Machine.ID
        RstCursor.MachineType = self.Machine.TypeId
        RstCursor.ProductID = self.Product.ID
        RstCursor.MoldID = self.Mold.ID
        RstCursor.OrderID = self.ActiveJosh.OrderID
        RstCursor.UnitsProducedJob = self.UnitsProduced
        RstCursor.UnitsProducedOK = 0
        RstCursor.UnitsProducedPCJob = self.UnitsProducedPC
        RstCursor.JoshStartUnits = self.UnitsProduced
        RstCursor.TotalUnitsJosh = 0
        RstCursor.InjectionsCount = 0
        RstCursor.InjectionsCountLast = 0
        RstCursor.InjectionsCountStart = self.InjectionsCount
        RstCursor.InjectionsCountDiff = 0
        if self.CavitiesStandard > 0 and self.CavitiesActual > 0:
            RstCursor.CavitiesStandard = self.CavitiesStandard
            RstCursor.CavitiesActual = self.CavitiesActual
        else:
            self.GetUnitsInCycle
            RstCursor.CavitiesStandard = self.CavitiesStandard
            RstCursor.CavitiesActual = self.CavitiesActual
        if self.CavitiesStandard > 0:
            RstCursor.CavitiesPC = self.CavitiesActual / self.CavitiesStandard * 100
        else:
            RstCursor.CavitiesPC = 100
        RstCursor.Status = 10
        if not self.Machine.DisconnectWorkerOnShiftChange and not self.ActiveJosh is None:
            RstCursor.WorkerID = self.ActiveJosh.WorkerID
        RstCursor.JoshStartUnitsProducedLeft = self.UnitsProducedLeft
        if not self.ActiveJosh is None:
            RstCursor.EndOfLine = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('TOP 1 EndOfLine', 'TblJosh WITH (NOLOCK)', 'JobID = ' + str(self.ID) + ' ORDER BY ID DESC', 'CN'), False)
        RstCursor.UpNone
        tNewJoshID = RstCursor.ID
        RstCursor.close()
        
        strSQL = 'SELECT * FROM TblJoshCurrent WHERE ID = ' + tNewJoshID
        RstCursor.Open(strSQL, CN, adOpenForwardOnly, adLockOptimistic)
        if RstData:
            RstCursor.AddNew()
            RstCursor.ID = tNewJoshID
        RstCursor.JobID = self.ID
        RstCursor.ShiftID = self.Machine.Server.CurrentShiftID
        RstCursor.ShiftDefID = self.Machine.Server.CurrentShift.ShiftDefID
        RstCursor.ShiftManagerID = self.Machine.Server.CurrentShift.ManagerID
        RstCursor.StartTime = ShortDate(tNow, True, True, True)
        RstCursor.Department = self.Department.ID
        RstCursor.ControllerID = self.Machine.ControllerID
        RstCursor.UnitsTargetJob = self.UnitsTarget
        RstCursor.MachineID = self.Machine.ID
        RstCursor.MachineType = self.Machine.TypeId
        RstCursor.ProductID = self.Product.ID
        RstCursor.MoldID = self.Mold.ID
        RstCursor.OrderID = self.ActiveJosh.OrderID
        RstCursor.UnitsProducedJob = self.UnitsProduced
        RstCursor.UnitsProducedOK = 0
        RstCursor.UnitsProducedPCJob = self.UnitsProducedPC
        RstCursor.JoshStartUnits = self.UnitsProduced
        RstCursor.TotalUnitsJosh = 0
        RstCursor.InjectionsCount = 0
        RstCursor.InjectionsCountLast = 0
        RstCursor.InjectionsCountStart = self.InjectionsCount
        RstCursor.InjectionsCountDiff = 0
        RstCursor.CavitiesStandard = self.CavitiesStandard
        RstCursor.CavitiesActual = self.CavitiesActual
        RstCursor.CavitiesPC = self.CavitiesActual / self.CavitiesStandard * 100
        RstCursor.Status = 10
        if not self.Machine.DisconnectWorkerOnShiftChange:
            RstCursor.WorkerID = self.ActiveJosh.WorkerID
        RstCursor.JoshStartUnitsProducedLeft = self.UnitsProducedLeft
        RstCursor.UpNone
        RstCursor.close()
        
        
        if not self.ActiveJosh is None and not self.Machine.DisconnectWorkerOnShiftChange:
            if self.ActiveJosh.ID == 0:
                GoTo(JoshWorkersWhile)
            strSQL = 'SELECT * FROM TblJoshWorkers Where JoshID = ' + self.ActiveJosh.ID
            
            RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            RstCursor.ActiveConnection = None
            while not RstCursor.EOF:
                if RstCursor.State == 0:
                    
                    pass
                strSQL = 'INSERT INTO TblJoshWorkers'
                strSQL = strSQL + '('
                strSQL = strSQL + 'JoshID'
                strSQL = strSQL + ',MachineID'
                strSQL = strSQL + ',JobID'
                strSQL = strSQL + ',UserID'
                strSQL = strSQL + ',WorkerID'
                strSQL = strSQL + ',HeadJoshWorker'
                strSQL = strSQL + ',WorkerName'
                strSQL = strSQL + ')'
                strSQL = strSQL + ' VALUES '
                strSQL = strSQL + '('
                strSQL = strSQL + tNewJoshID
                strSQL = strSQL + ',' + self.Machine.ID
                strSQL = strSQL + ',' + str(self.ID)
                strSQL = strSQL + ',' + RstCursor.UserID
                strSQL = strSQL + ',\'' + RstCursor.WorkerID + '\''
                strSQL = strSQL + ',' + IIf(MdlADOFunctions.fGetRstValBool(RstCursor.HeadJoshWorker, False) == False, 0, 1)
                strSQL = strSQL + ',\'' + RstCursor.WorkerName + '\''
                strSQL = strSQL + ')'
                CN.Execute(strSQL)
                RstCursor.MoveNext()
            RstCursor.close()
        
        if not self.ActiveJosh is None:
            if self.ActiveJosh.ID == 0:
                GoTo(TblJoshMaterialsWhile)
            strSQL = 'SELECT * FROM TblJoshMaterial Where JoshID = ' + self.ActiveJosh.ID
            RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            RstCursor.ActiveConnection = None
            while not RstCursor.EOF:
                if RstCursor.State == 0:
                    
                    pass
                
                tMaterialID = MdlADOFunctions.fGetRstValLong(RstCursor.Material)
                tRecipeMaterialID = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, 'Material ID', MdlADOFunctions.fGetRstValLong(RstCursor.ChannelNum), MdlADOFunctions.fGetRstValLong(RstCursor.SplitNum)))
                if tMaterialID == tRecipeMaterialID and tMaterialID != 0 and tRecipeMaterialID != 0:
                    strTitle = 'INSERT INTO TblJoshMaterial '
                    strSQL = '('
                    strSQL = strSQL + 'JobID'
                    strSQL = strSQL + ',ChannelNum'
                    strSQL = strSQL + ',SplitNum'
                    strSQL = strSQL + ',ShiftID'
                    strSQL = strSQL + ',ShiftDefID'
                    strSQL = strSQL + ',JoshID'
                    strSQL = strSQL + ',JoshStart'
                    strSQL = strSQL + ',Material'
                    strSQL = strSQL + ',JoshAmountStart'
                    strSQL = strSQL + ',MaterialPC'
                    strSQL = strSQL + ',MaterialPCStandad'
                    strSQL = strSQL + ',MaterialTypeID'
                    strSQL = strSQL + ',MachineID'
                    strSQL = strSQL + ',UnitWeight'
                    strSQL = strSQL + ',ProductID'
                    strSQL = strSQL + ',MaterialClassID'
                    strSQL = strSQL + ',MaterialBatch'
                    strSQL = strSQL + ',InventoryID'
                    strSQL = strSQL + ')'
                    strSQL = strSQL + ' VALUES '
                    strSQL = strSQL + '('
                    strSQL = strSQL + str(self.ID)
                    strSQL = strSQL + ',' + RstCursor.ChannelNum
                    strSQL = strSQL + ',' + RstCursor.SplitNum
                    strSQL = strSQL + ',' + self.Machine.Server.CurrentShift.ID
                    strSQL = strSQL + ',' + self.Machine.Server.CurrentShift.ShiftDefID
                    strSQL = strSQL + ',' + tNewJoshID
                    strSQL = strSQL + ',\'' + ShortDate(tNow, True, True, True) + '\''
                    strSQL = strSQL + ',' + MdlADOFunctions.fGetRstValLong(RstCursor.Material)
                    strSQL = strSQL + ',' + MdlADOFunctions.fGetRstValDouble(RstCursor.JobAmount)
                    strSQL = strSQL + ',' + MdlADOFunctions.fGetRstValDouble(RstCursor.MaterialPC)
                    strSQL = strSQL + ',' + MdlADOFunctions.fGetRstValDouble(RstCursor.MaterialPCStandad)
                    strSQL = strSQL + ',' + MdlADOFunctions.fGetRstValLong(RstCursor.MaterialTypeID)
                    strSQL = strSQL + ',' + self.Machine.ID
                    strSQL = strSQL + ',' + self.GetUnitWeight
                    strSQL = strSQL + ',' + self.Product.ID
                    strSQL = strSQL + ',' + MdlADOFunctions.fGetRstValLong(RstCursor.MaterialClassID)
                    strSQL = strSQL + ',\'' + MdlADOFunctions.fGetRstValString(RstCursor.MaterialBatch) + '\''
                    strSQL = strSQL + ',' + MdlADOFunctions.fGetRstValLong(RstCursor.InventoryID)
                    strSQL = strSQL + ')'
                    CN.Execute(strTitle + strSQL)
                    
                    strTitle = 'INSERT INTO TblJoshCurrentMaterial '
                    CN.Execute(strTitle + strSQL)
                RstCursor.MoveNext()
            RstCursor.close()
        
        if not self.OpenEvent is None:
            if self.OpenEvent.RootEventID == 0:
                if self.Machine.NewJob:
                    if self.Machine.SetupEventIDOnShiftEnd == 1:
                        self.OpenEvent.CloseAndCreateForNewShift(self.Machine.Server.CurrentShiftID, False, 0, True)
                    else:
                        self.OpenEvent.CloseAndCreateForNewShift(self.Machine.Server.CurrentShiftID, True, 0, True)
                else:
                    self.OpenEvent.CloseAndCreateForNewShift(self.Machine.Server.CurrentShiftID, True, 0, True)
            else:
                
                strSQL = 'SELECT MachineID, EndTime FROM TblEvent WITH (NOLOCK) WHERE ID = ' + self.OpenEvent.RootEventID
                RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                RstCursor.ActiveConnection = None
                if RstData:
                    tMachine = self.Machine.Server.Machines.Item(str(RstCursor.MachineID))
                    if tMachine.ActiveJob.OpenEvent is None and IsEmptyOrNull(RstCursor.EndTime):
                        if self.Machine.NewJob:
                            if self.Machine.SetupEventIDOnShiftEnd == 1:
                                self.OpenEvent.CloseAndCreateForNewShift(self.Machine.Server.CurrentShiftID, False, self.OpenEvent.RootEventID, True)
                            else:
                                self.OpenEvent.CloseAndCreateForNewShift(self.Machine.Server.CurrentShiftID, True, self.OpenEvent.RootEventID, True)
                        else:
                            self.OpenEvent.CloseAndCreateForNewShift(self.Machine.Server.CurrentShiftID, True, self.OpenEvent.RootEventID, True)
        
        if not self.OpenWorkingEvent is None:
            self.OpenWorkingEvent.CloseAndCreateForNewShift(self.Machine.Server.CurrentShiftID)
        
        if not self.OpenEngineEvent is None:
            self.OpenEngineEvent.CloseAndCreateForNewShift(self.Machine.Server.CurrentShiftID)
        
        self.ActiveJosh.EndJosh
        self.ActiveJosh = None
        
        for tVariant in self.ControllerChannels:
            tChannel = tVariant
            tChannel.ResetJoshCounters
        tJosh = Josh()
        tJosh.Init(self, tNewJoshID)
        
        self.ActiveJosh = tJosh
        self.Machine.ActiveJosh = tJosh
        self.Machine.ActiveJoshID = tJosh.ID
        
        if not self.OpenEvent is None:
            self.OpenEvent.Josh = tJosh
            self.OpenEvent.Update
        
        if not self.OpenWorkingEvent is None:
            self.OpenWorkingEvent.Josh = tJosh
            self.OpenWorkingEvent.Update
        
        if not self.OpenEngineEvent is None:
            self.OpenEngineEvent.Josh = tJosh
            self.OpenEngineEvent.Update
        self.Machine.FireEventTriggeredTasks(4)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.CreateJoshForNewShift:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
            
            
        RstCursor = None

    def CalcUnitsReportedOK(self):
        tUnitsReportedOK = 0.0

        tUnitsReportedOKDiff = 0.0
        
        if self.Machine.ReportRejectsUnReported == True:
            tUnitsReportedOK = self.UnitsReportedOK
        else:
            tUnitsReportedOK = self.UnitsProducedOK
        self.UnitsReportedOK = tUnitsReportedOK
        tUnitsReportedOKDiff = round(self.UnitsProducedOK - self.UnitsReportedOK, 5)
        if self.UnitsReportedOK != 0:
            self.UnitsReportedOKDiffPC = round(tUnitsReportedOKDiff / self.UnitsReportedOK * 100, 5)
        else:
            self.UnitsReportedOKDiffPC = 0
        
        if self.Machine.ReportRejectsUnReported == True and  ( self.UnitsReportedOKDiff != tUnitsReportedOKDiff ) :
            self.UnitsReportedOKDiff = tUnitsReportedOKDiff
            self.AddRejects(self.UnitsReportedOKDiff, 0, 500, True, VBGetMissingArgument(self.AddRejects, 4), VBGetMissingArgument(self.AddRejects, 5), False, VBGetMissingArgument(self.AddRejects, 7), False)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcUnitsReportedOK:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def InitMoldChangeDetails(self):
        strSQL = ''
        RstCursor = None

        try:        
            strSQL = 'SELECT TOP 1 MachineJobOrder FROM TblJob'
            strSQL = strSQL + ' WHERE MachineID = ' + str(self.Machine.ID)
            strSQL = strSQL + ' AND MoldID <> ' + str(self.Mold.ID)
            strSQL = strSQL + ' AND MachineJobOrder IS NOT NULL'
            strSQL = strSQL + ' AND Status IN (2,3,11)'
            strSQL = strSQL + ' ORDER BY MachineJobOrder'

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.MoldChangeFirstOtherMoldMachineJobOrder = MdlADOFunctions.fGetRstValLong(RstData.MachineJobOrder)
            RstCursor.close()

            if self.MoldChangeFirstOtherMoldMachineJobOrder == 0:
                self.MoldChangeFirstOtherMoldMachineJobOrder = 1000

            if (self.Machine.MoldEndTimeCalcOption == 1):
                strSQL = 'SELECT SUM(TimeLeftHr) AS TimeLeftHr FROM TblJob'
                strSQL = strSQL + ' WHERE Status IN(3,11,' + str(self.Machine.MoldEndTimeStatusOption) + ')'
                strSQL = strSQL + ' AND MoldID = ' + str(self.Mold.ID)
                strSQL = strSQL + ' AND MachineID = ' + str(self.Machine.ID)
                strSQL = strSQL + ' AND PConfigParentID = 0'
                strSQL = strSQL + ' AND MachineJobOrder < ' + str(self.MoldChangeFirstOtherMoldMachineJobOrder)

                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstData:
                    self.MoldChangeTimeLeftHr = MdlADOFunctions.fGetRstValDouble(RstData.TimeLeftHr)
                RstCursor.close()
            elif (self.Machine.MoldEndTimeCalcOption == 2):
                strSQL = 'SELECT SUM(TimeLeftHr) AS TimeLeftHr FROM TblJob'
                strSQL = strSQL + ' WHERE Status IN(3,11,' + str(self.Machine.MoldEndTimeStatusOption) + ')'
                strSQL = strSQL + ' AND MoldID = ' + str(self.Mold.ID)
                strSQL = strSQL + ' AND MachineID = ' + str(self.Machine.ID)
                strSQL = strSQL + ' AND PConfigParentID = 0'

                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstData:
                    self.MoldChangeTimeLeftHr = MdlADOFunctions.fGetRstValDouble(RstData.TimeLeftHr)
                RstCursor.close()

            elif (self.Machine.MoldEndTimeCalcOption == 3):
                strSQL = 'SELECT SUM(UnitsTarget) AS UnitsTarget, SUM(UnitsProducedOK) AS UnitsProducedOK FROM TblJob'
                strSQL = strSQL + ' WHERE Status IN(3,11,' + str(self.Machine.MoldEndTimeStatusOption) + ')'
                strSQL = strSQL + ' AND MoldID = ' + str(self.Mold.ID)
                strSQL = strSQL + ' AND MachineID = ' + str(self.Machine.ID)
                strSQL = strSQL + ' AND PConfigParentID = 0'
                strSQL = strSQL + ' AND MachineJobOrder < ' + str(self.MoldChangeFirstOtherMoldMachineJobOrder)

                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstData:
                    self.MoldChangeUnitsTarget = MdlADOFunctions.fGetRstValDouble(RstData.UnitsTarget)
                    self.MoldChangeUnitsProducedOK = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedOK)
                RstCursor.close()

            elif (self.Machine.MoldEndTimeCalcOption == 4):
                strSQL = 'SELECT SUM(UnitsTarget) AS UnitsTarget, SUM(UnitsProducedOK) AS UnitsProducedOK FROM TblJob'
                strSQL = strSQL + ' WHERE Status IN(3,11,' + str(self.Machine.MoldEndTimeStatusOption) + ')'
                strSQL = strSQL + ' AND MoldID = ' + str(self.Mold.ID)
                strSQL = strSQL + ' AND MachineID = ' + str(self.Machine.ID)
                strSQL = strSQL + ' AND PConfigParentID = 0'

                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstData:
                    self.MoldChangeUnitsTarget = MdlADOFunctions.fGetRstValDouble(RstData.UnitsTarget)
                    self.MoldChangeUnitsProducedOK = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedOK)
                RstCursor.close()
            else:
                strSQL = 'SELECT SUM(TimeLeftHr) AS TimeLeftHr FROM TblJob'
                strSQL = strSQL + ' WHERE Status IN(3,11,' + str(self.Machine.MoldEndTimeStatusOption) + ')'
                strSQL = strSQL + ' AND MoldID = ' + str(self.Mold.ID)
                strSQL = strSQL + ' AND MachineID = ' + str(self.Machine.ID)
                strSQL = strSQL + ' AND PConfigParentID = 0'
                strSQL = strSQL + ' AND MachineJobOrder < ' + str(self.MoldChangeFirstOtherMoldMachineJobOrder)

                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstData:
                    self.MoldChangeTimeLeftHr = MdlADOFunctions.fGetRstValDouble(RstData.TimeLeftHr)
                RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                    
                MdlGlobal.RecordError(type(self).__name__ + '.InitMoldChangeDetails:', str(0), error.args[0], 'JobID:' + str(self.ID))

        RstCursor = None

    def CalcMoldChangeDetails(self):
        tMoldEndDuration = 0.0
        
        if (self.Machine.MoldEndTimeCalcOption == 1) or (self.Machine.MoldEndTimeCalcOption == 2):
            self.Machine.MoldEndTime = self.TimeLeftHr + self.MoldChangeTimeLeftHr
        elif (self.Machine.MoldEndTimeCalcOption == 3) or (self.Machine.MoldEndTimeCalcOption == 4):
            tMoldEndDuration = ( self.MoldChangeUnitsTarget - self.MoldChangeUnitsProducedOK )  * self.CycleTimeAvg /  ( self.CavitiesActual * 60 )
            self.Machine.MoldEndTime = self.TimeLeftHr + tMoldEndDuration
        else:
            self.Machine.MoldEndTime = self.TimeLeftHr + self.MoldChangeTimeLeftHr
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcMoldChangeDetails:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def PrintRecordToHistory(self, pActionID, pParameterName='', pPreviousValue='', pCurrentValue=''):
        strSQL = ''
        
        strSQL = 'INSERT TblJobHistory '
        strSQL = strSQL + '('
        strSQL = strSQL + 'JobID'
        strSQL = strSQL + ',UserID'
        strSQL = strSQL + ',ChangeDate'
        strSQL = strSQL + ',StartTimeTarget'
        strSQL = strSQL + ',EndTimeTarget'
        strSQL = strSQL + ',EndTimeRequest'
        strSQL = strSQL + ',UnitsTarget'
        strSQL = strSQL + ',ActionID'
        strSQL = strSQL + ',MachineID'
        strSQL = strSQL + ',ProductID'
        strSQL = strSQL + ',MoldID'
        strSQL = strSQL + ',Department'
        strSQL = strSQL + ',Status'
        strSQL = strSQL + ',ProductWeight'
        strSQL = strSQL + ',UnitWeight'
        strSQL = strSQL + ',ERPJobDef'
        strSQL = strSQL + ',FieldName'
        strSQL = strSQL + ',PreviousValue'
        strSQL = strSQL + ',CurrentValue'
        strSQL = strSQL + ')'
        strSQL = strSQL + ' SELECT ID AS JobID, 0 AS UserID, \'' + ShortDate(mdl_Common.NowGMT, True, True, True) + '\' AS ChangeDate,'
        strSQL = strSQL + ' StartTimeTarget, EndTimeTarget, EndTimeRequest, UnitsTarget, \'' + pActionID + '\' AS ActionID, MachineID, ProductID,'
        strSQL = strSQL + ' MoldID, Department, Status, ' + self.ProductWeightStandard + ' AS ProductWeight, ' + str(self.GetUnitWeight) + ' AS UnitWeight, ERPJobDef,'
        strSQL = strSQL + ' \'' + pParameterName + '\' AS FieldName, \'' + pPreviousValue + '\' AS PreviousValue, \'' + pCurrentValue + '\' AS CurrentValue'
        strSQL = strSQL + ' FROM TblJob'
        strSQL = strSQL + ' WHERE ID = ' + str(self.ID)
        CN.Execute(strSQL)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.PrintRecordToHistory', str(0), error.args[0], 'JobID: ' + str(self.ID))
            Err.Clear()

    def EndJob(self):
        tVariant = None

        tChannel = Channel()

        tChildJob = Job()

        tVariant2 = None

        tSplit = ChannelSplit()
        
        if self.SetUpEnd == '00:00:00':
            self.EndSetUp(100, VBGetMissingArgument(self.EndSetUp, 1), True)
        else:
            if not self.OpenEvent is None:
                self.OpenEvent.EndEvent(True)
                self.OpenEvent = None
                if self.PConfigID != 0 and self.IsPConfigMain == True:
                    for tVariant in self.PConfigJobs:
                        tChildJob = tVariant
                        tChildJob.OpenEvent.EndEvent(True)
                        tChildJob.OpenEvent = None
                
            
            if not self.OpenWorkingEvent is None:
                self.OpenWorkingEvent.EndEvent
                self.OpenWorkingEvent = None
                if self.PConfigID != 0 and self.IsPConfigMain == True:
                    for tVariant in self.PConfigJobs:
                        tChildJob = tVariant
                        tChildJob.OpenWorkingEvent.EndEvent
                        tChildJob.OpenWorkingEvent = None
            
            if not self.OpenEngineEvent is None:
                self.OpenEngineEvent.EndEvent
                self.OpenEngineEvent = None
                if self.PConfigID != 0 and self.IsPConfigMain == True:
                    for tVariant in self.PConfigJobs:
                        tChildJob = tVariant
                        tChildJob.OpenEngineEvent.EndEvent
                        tChildJob.OpenEngineEvent = None
        
        for tVariant in self.ControllerChannels:
            tChannel = tVariant
            tChannel.ValidateAmount(self.ActiveJosh.DurationMin, FromJosh)
            tChannel.ValidateAmount(self.DurationMin, FromJob)
        self.DetailsCalc(True, False)
        
        if not self.ActiveJosh is None:
            self.ActiveJosh.EndJosh
            
            if self.PConfigID != 0 and self.IsPConfigMain == True:
                for tVariant in self.PConfigJobs:
                    tChildJob = tVariant
                    if not tChildJob.ActiveJosh is None:
                        tChildJob.ActiveJosh.EndJosh
                        tChildJob.ActiveJosh = None
        
        for tVariant in self.ControllerChannels:
            tChannel = tVariant
            if not tChannel.Splits is None:
                for tVariant2 in tChannel.Splits:
                    tSplit = tVariant2
                    tChannel.Splits.Remove(( str(tSplit.SplitNum) ))
                    tSplit.MaterialID = None
                    tSplit.MaterialBatch = None
                    tSplit.MaterialPCTarget = None
                    tSplit.MaterialPC = None
                    tSplit.TotalWeight = None
                    tSplit.ForecastWeight = None
                    tSplit = None
            tChannel.Splits = None
            tChannel.MaterialID = None
            tChannel.MaterialPCTarget = None
            tChannel.MaterialPC = None
            tChannel.MaterialBatch = None
            tChannel.TotalWeight = None
            tChannel.ForecastWeight = None
            self.ControllerChannels.Remove(( str(tChannel.ChannelNum) ))
            tChannel = None
        self.RemoveAllAlarms
        self.RunValidations(EndOfJob)
        self.Update
        self.Machine.FireEventTriggeredTasks(2)
        self.ControllerChannels = None
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.EndJob', str(0), error.args[0], 'JobID: ' + str(self.ID))
            Err.Clear()

    def GetRefRecipeProductWeight(self):
        tRefRecipeProductWeight = 0.0
        
        try:
            if (self.RecipeRefType == 1):
                tRefRecipeProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(self.Product.ID, 'ProductWeight', 0, 0))
            elif (self.RecipeRefType == 2):
                tRefRecipeProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.RecipeRefJob, 'ProductWeight', 0, 0))
            elif (self.RecipeRefType == 6):
                tRefRecipeProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtils.fGetRecipeValueStandard(self.RecipeRefStandardID, 'ProductWeight', 0, 0, self.Product.ID))
            self.RefRecipeProductWeight = tRefRecipeProductWeight

        except:
            pass

    def GetRefRecipeUnitWeight(self):
        tValue = ''
        tRefRecipeUnitWeight = 0.0
        tMoldID = 0
        tCavities = 0.0
        tRefRecipeProductWeight = 0.0
        
        try:
            if (self.RecipeRefType == 1):
                tValue = MdlUtilsH.fGetRecipeValueProduct(self.Product.ID, 'UnitWeight', 0, 0)
                if tValue != '':
                    tRefRecipeUnitWeight = MdlADOFunctions.fGetRstValDouble(tValue)
                    if tRefRecipeUnitWeight == 0:
                        tRefRecipeProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(self.Product.ID, 'ProductWeight', 0, 0))
                        tMoldID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MoldID', 'TblProductMolds', 'ProductID = ' + str(self.Product.ID) + ' ORDER BY Priority', 'CN'))
                        if tMoldID != 0:
                            tCavities = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('Cavities', 'TblMolds', 'ID = ' + str(tMoldID), 'CN'))
                            if tCavities != 0:
                                tRefRecipeUnitWeight = round(tRefRecipeProductWeight / tCavities, 0)
                            else:
                                tRefRecipeUnitWeight = tRefRecipeProductWeight
                        else:
                            tRefRecipeUnitWeight = tRefRecipeProductWeight
                else:
                    tRefRecipeProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(self.Product.ID, 'ProductWeight', 0, 0))
                    tMoldID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MoldID', 'TblProductMolds', 'ProductID = ' + str(self.Product.ID) + ' ORDER BY Priority', 'CN'))
                    if tMoldID != 0:
                        tCavities = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('Cavities', 'TblMolds', 'ID = ' + str(tMoldID), 'CN'))
                        if tCavities != 0:
                            tRefRecipeUnitWeight = round(tRefRecipeProductWeight / tCavities, 0)
                        else:
                            tRefRecipeUnitWeight = tRefRecipeProductWeight
                    else:
                        tRefRecipeUnitWeight = tRefRecipeProductWeight
            elif (self.RecipeRefType == 2):
                tValue = MdlUtilsH.fGetRecipeValueJob(self.RecipeRefJob, 'UnitWeight', 0, 0)
                if tValue != '':
                    tRefRecipeUnitWeight = MdlADOFunctions.fGetRstValDouble(tValue)
                    if tRefRecipeUnitWeight == 0:
                        tRefRecipeProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.RecipeRefJob, 'ProductWeight', 0, 0))
                        
                        tCavities = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('CavitiesActual', 'TblJob', 'ID = ' + str(self.RecipeRefJob), 'CN'))
                        if tCavities != 0:
                            tRefRecipeUnitWeight = round(tRefRecipeProductWeight / tCavities, 0)
                        else:
                            tRefRecipeUnitWeight = tRefRecipeProductWeight
                else:
                    tRefRecipeProductWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.RecipeRefJob, 'ProductWeight', 0, 0))
            elif (self.RecipeRefType == 6):
                tValue = MdlUtils.fGetRecipeValueStandard(self.RecipeRefStandardID, 'UnitWeight', 0, 0, self.Product.ID)
                if tValue != '':
                    tRefRecipeUnitWeight = MdlADOFunctions.fGetRstValDouble(tValue)
                    if tRefRecipeUnitWeight == 0:
                        tRefRecipeProductWeight = MdlUtils.fGetRecipeValueStandard(self.RecipeRefStandardID, 'ProductWeight', 0, 0, self.Product.ID)
                        tMoldID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MoldID', 'TblProductRecipeStandards', 'StandardID = ' + str(self.RecipeRefStandardID), 'CN'))
                        if tMoldID != 0:
                            tCavities = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('Cavities', 'TblMolds', 'ID = ' + str(tMoldID), 'CN'))
                            if tCavities != 0:
                                tRefRecipeUnitWeight = round(tRefRecipeProductWeight / tCavities, 0)
                            else:
                                tRefRecipeUnitWeight = tRefRecipeProductWeight
                else:
                    tRefRecipeProductWeight = MdlUtils.fGetRecipeValueStandard(self.RecipeRefStandardID, 'ProductWeight', 0, 0, self.Product.ID)
                    tMoldID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MoldID', 'TblProductRecipeStandards', 'StandardID = ' + str(self.RecipeRefStandardID), 'CN'))
                    if tMoldID != 0:
                        tCavities = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('Cavities', 'TblMolds', 'ID = ' + str(tMoldID), 'CN'))
                        if tCavities != 0:
                            tRefRecipeUnitWeight = round(tRefRecipeProductWeight / tCavities, 0)
                        else:
                            tRefRecipeUnitWeight = tRefRecipeProductWeight
            self.RefRecipeUnitWeight = tRefRecipeUnitWeight

        except:
            pass

    def GetParametersForOfflineJob(self):
        strSQL = ''

        RstCursor = None
        
        strSQL = 'SELECT Status,InjectionsCount,InjectionsCountLast,UnitsProduced FROM TblJob WHERE ID = ' + str(self.ID)
        RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        RstCursor.ActiveConnection = None
        if RstData:
            if MdlADOFunctions.fGetRstValDouble(RstCursor.Status) == 10:
                if MdlADOFunctions.fGetRstValDouble(RstCursor.InjectionsCount) != self.InjectionsCount:
                    self.InjectionsCount = MdlADOFunctions.fGetRstValDouble(RstCursor.InjectionsCount)
                    self.InjectionsCountLast = MdlADOFunctions.fGetRstValDouble(RstCursor.InjectionsCountLast)
                    self.InjectionsDiff = self.InjectionsCount - self.InjectionsCountLast
                    self.UnitsProduced = self.InjectionsCount * self.CavitiesActual
                else:
                    self.UnitsProduced = self.InjectionsCount * self.CavitiesActual
                    self.InjectionsCountLast = self.InjectionsCount
                    self.InjectionsDiff = 0
            else:
                self.InjectionsCount = MdlADOFunctions.fGetRstValDouble(RstCursor.InjectionsCount)
                self.InjectionsCountLast = MdlADOFunctions.fGetRstValDouble(RstCursor.InjectionsCountLast)
                self.InjectionsDiff = self.InjectionsCount - self.InjectionsCountLast
                self.UnitsProduced = self.InjectionsCount * self.CavitiesActual
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
                
            Err.Clear()
        RstCursor = None

    
    def RunValidations(self, pValidationTimingType, pJosh=None):
        tVariant = None

        tValidation = Validation()

        tValidationID = 0

        tJosh = Josh()
        
        if IsMissing(pJosh):
            if not self.ActiveJosh is None:
                tJosh = self.ActiveJosh
        else:
            if not pJosh is None:
                tJosh = pJosh
        for tVariant in self.Machine.Validations:
            tValidation = tVariant
            tValidationID = tValidation.ID
            if tValidation.ValidationTiming == pValidationTimingType:
                tValidation.Validate(self, tJosh)
        if Err.Number != 0:
            MdlGlobal.RecordError(type(self).__name__ + '.RunValidations:', str(0), error.args[0], 'JobID:' + str(self.ID) + '. ValidationID:' + tValidationID)
            Err.Clear()
        tJosh = None
        tValidation = None
        tVariant = None

    def RemoveAllAlarms(self):
        strSQL = ''

        Counter = 0

        tAlarm = Alarm()

        tParam = ControlParam()
        
        
        strSQL = ''
        strSQL = strSQL + 'UPDATE TblEvent SET AlarmDismissed = 1' + vbCrLf
        strSQL = strSQL + 'WHERE ID IN(' + vbCrLf
        strSQL = strSQL + 'SELECT EventID FROM TblAlarms WHERE EventID <> 0 AND JobID = ' + str(self.ID)
        strSQL = strSQL + ')'
        CN.Execute(strSQL)
        strSQL = 'DELETE FROM TblAlarms WHERE JobID = ' + str(self.ID)
        CN.Execute(strSQL)
        if not self.OpenAlarms is None:
            for Counter in vbForRange(1, self.OpenAlarms.Count):
                tAlarm = self.OpenAlarms.Item(Counter)
                
                if self.Machine.GetParam(tAlarm.ParameterName, tParam) == True:
                    tParam.Alarms = {}
                self.OpenAlarms.Remove(( Counter ))
                tAlarm = None
            self.OpenAlarms = None
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.RunValidations:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        tAlarm = None

    def GetUnitsInCycle(self, PRst=None):
        tMachineID = 0
        tUnitsInCycleType = 0
        tUnitsInCycle = 0.0
        tStandardUnitsInCycle = 0.0
        tTableName = ''
        tFieldName = ''
        tStandardTableName = ''
        tStandardFieldName = ''
        strSQL = ''
        RstCursor = None
        tRefID = 0
                
        if PRst and MdlADOFunctions.fGetRstValString(PRst.CavitiesActual) != "0" and MdlADOFunctions.fGetRstValString(PRst.CavitiesStandard) != "0":
            if MdlADOFunctions.fGetRstValString(PRst.CavitiesActual) != '' and MdlADOFunctions.fGetRstValString(PRst.CavitiesStandard) != '' and MdlADOFunctions.fGetRstValString(PRst.CavitiesActual) != '0' and MdlADOFunctions.fGetRstValString(PRst.CavitiesStandard) != '0' and MdlADOFunctions.fGetRstValString(PRst.CavitiesActual) != '0.00' and MdlADOFunctions.fGetRstValString(PRst.CavitiesStandard) != '0.00':
                self.CavitiesActual = MdlADOFunctions.fGetRstValDouble(PRst.CavitiesActual)
                self.CavitiesStandard = MdlADOFunctions.fGetRstValDouble(PRst.CavitiesStandard)
                return
        tMachineID = self.Machine.ID
        tUnitsInCycleType = self.Machine.UnitsInCycleType
        if tUnitsInCycleType == 0:
            tUnitsInCycleType = 1
            tTableName = 'TblMolds'
            tFieldName = 'CavitiesCurrent'
            tStandardTableName = 'TblMolds'
            tStandardFieldName = 'Cavities'
        else:
            strSQL = 'SELECT TableName, FieldName, StandardTableName, StandardFieldName FROM STblMachineUnitsInCycleTypes WHERE ID = ' + tUnitsInCycleType
            RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            RstCursor.ActiveConnection = None
            if RstData:
                tTableName = MdlADOFunctions.fGetRstValString(RstCursor.TableName)
                tFieldName = MdlADOFunctions.fGetRstValString(RstCursor.FieldName)
                tStandardTableName = MdlADOFunctions.fGetRstValString(RstCursor.StandardTableName)
                tStandardFieldName = MdlADOFunctions.fGetRstValString(RstCursor.StandardFieldName)
            RstCursor.close()
        
        if (tTableName == 'TblMolds'):
            tRefID = self.Mold.ID
            tUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue(tFieldName, tTableName, 'ID = ' + tRefID, 'CN'))
        elif (tTableName == 'TblProduct'):
            tRefID = self.Product.ID
            tUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue(tFieldName, tTableName, 'ID = ' + tRefID, 'CN'))
        elif (tTableName == 'TblProductRecipe'):
            tRefID = self.ProductID
            tUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(tRefID, tFieldName, 0, 0))
        elif (tTableName == 'TblProductRecipeJob'):
            tUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, tFieldName, 0, 0))
        
        if tStandardTableName != '' and tStandardFieldName != '':
            if (tStandardTableName == 'TblMolds'):
                tRefID = self.Mold.ID
                
                tStandardUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue(tStandardFieldName, tStandardTableName, 'ID = ' + tRefID, 'CN'))
            elif (tStandardTableName == 'TblProduct'):
                tRefID = self.Product.ID
                
                tStandardUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue(tStandardFieldName, tStandardTableName, 'ID = ' + tRefID, 'CN'))
            elif (tStandardTableName == 'TblProductRecipe'):
                tRefID = self.ProductID
                
                tStandardUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(tRefID, tStandardFieldName, 0, 0))
            elif (tStandardTableName == 'TblProductRecipeJob'):
                
                tStandardUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.ID, tStandardFieldName, 0, 0))
        else:
            tStandardUnitsInCycle = tUnitsInCycle
        if tUnitsInCycle == 0:
            tUnitsInCycle = 1
        if tStandardUnitsInCycle == 0:
            tStandardUnitsInCycle = tUnitsInCycle
        self.CavitiesActual = tUnitsInCycle
        self.CavitiesStandard = tStandardUnitsInCycle
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
        RstCursor = None

    def AddMaterialFlowFromLastJob(self):
        strSQL = ''

        RstCursor = None

        tChannel = Channel()

        tSplit = ChannelSplit()

        tLastJobID = 0
        
        self.GetProductWeight
        strSQL = 'SELECT * FROM TblMachineMaterialFlow WHERE MachineID = ' + self.Machine.ID
        RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        RstCursor.ActiveConnection = None
        while not RstCursor.EOF:
            tLastJobID = MdlADOFunctions.fGetRstValLong(RstCursor.JobID)
            tChannel = self.ControllerChannels.Item(str(RstCursor.ChannelNum))
            if not tChannel is None:
                if MdlADOFunctions.fGetRstValLong(RstCursor.SplitNum) == 0:
                    AddMaterialFlowAmountToChannel(self, tChannel, MdlADOFunctions.fGetRstValDouble(RstCursor.value), FromJob)
                    AddMaterialFlowAmountToChannel(self, tChannel, MdlADOFunctions.fGetRstValDouble(RstCursor.value), FromJosh)
                else:
                    tSplit = tChannel.Splits.Item(str(RstCursor.SplitNum))
                    if not tSplit is None:
                        AddMaterialFlowAmountToSplit(self, tSplit, MdlADOFunctions.fGetRstValDouble(RstCursor.value), FromJob)
                        AddMaterialFlowAmountToSplit(self, tSplit, MdlADOFunctions.fGetRstValDouble(RstCursor.value), FromJosh)
            RstCursor.MoveNext()
        RstCursor.close()
        self.PrintRecordToHistory(500, 'JobID', str(tLastJobID))
        strSQL = 'UPDATE TblMachineMaterialFlow SET Value = NULL, InitialValue = NULL, JobID = NULL WHERE MachineID = ' + self.Machine.ID
        CN.Execute(strSQL)
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
        RstCursor = None

    def ReportInventoryItem(self, pValuesDiff, pEffectiveAmount=- 1, pLabelID=0):
        strSQL = ''

        tBatch = ''

        tAmount = 0

        tEffectiveAmount = 0.0

        tJobID = 0

        tJoshID = 0

        tInventoryBatchOption = InventoryBatchOption()

        tBatchNum = 0

        tERPJobID = ''

        tUnitsReportedOkFrom = UnitsReportedOKFromOption()

        tCatalogID = ''

        tMaterialID = 0

        tProductID = 0

        tShiftID = 0

        tInventoryID = 0

        i = 0

        tWareHouseID = 0

        tClientID = 0

        tWareHouseLocationID = 0

        tBoxUnits = 0.0

        tAmountFullBoxes = 0.0

        strFields = ''

        strValues = ''

        NewRowFlag = False

        RstValue = None

        RstData = None

        tDataPrepared = False

        tStatus = 0

        tReportInventoryItemAsSetUpReject = False

        tAddPackageTypeToInventoryBatch = False

        tPackageTypeID = 0

        tWhere = ''

        tAddToActivePallet = False

        tNumeratorID = 0

        tMinQueueID = 0

        tDefaultStatus = 0
        
        
        tInventoryBatchOption = self.Machine.Server.SystemVariables.InventoryBatchOption
        tUnitsReportedOkFrom = self.Machine.Server.SystemVariables.UnitsReportedOKFrom
        tAddPackageTypeToInventoryBatch = self.Machine.Server.SystemVariables.AddPackageTypeToInventoryBatch
        tDefaultStatus = self.Machine.Server.SystemVariables.InventoryStatusOnCreation
        if tDefaultStatus == 0:
            tDefaultStatus = 1
        pValuesDiff = pValuesDiff
        for i in vbForRange(1, pValuesDiff):
            tDataPrepared = False
            
            if self.Machine.NewJob == True:
                tReportInventoryItemAsSetUpReject = self.MachineType.ReportInventoryItemAsSetUpReject
                if tReportInventoryItemAsSetUpReject == True:
                    tStatus = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'STblInventoryStatus', 'SysName = N\'Reject\'', 'CN'))
                else:
                    tStatus = tDefaultStatus
            else:
                tStatus = tDefaultStatus
            if pEffectiveAmount == - 1:
                tEffectiveAmount = self.CavitiesActual
            else:
                tEffectiveAmount = pEffectiveAmount
            if self.PConfigID == 0:
                tWhere = 'WHERE ID = ' + str(self.ID)
            else:
                tWhere = 'WHERE ID = ' + str(self.ID) + ' OR PConfigParentID = ' + str(self.ID)
            tMinQueueID = AddToLabelsQueue(pLabelID, tWhere, 1, self)
            if ProcessCurrentLabelSession(self, pLabelID, tEffectiveAmount, tStatus, tMinQueueID):
                tDataPrepared = True
            if not self.Machine.AutoPrintLabel:
                DeleteLabelData(self.ID)
            GoTo(NextItem)
            
            tBatchNum = GetLabelNumerator(pLabelID, self.ID, tNumeratorID)
            if tBatchNum == - 1:
                if (tUnitsReportedOkFrom == UnitsReportedOKFromOption.Box):
                    tBatchNum = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('PackageBatchNum', 'TblJob', 'ID = ' + str(self.ID), 'CN'))
                elif (tUnitsReportedOkFrom == UnitsReportedOKFromOption.Pallet):
                    tBatchNum = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('PalletBatchNum', 'TblJob', 'ID = ' + str(self.ID), 'CN'))
            if tAddPackageTypeToInventoryBatch == True:
                tPackageTypeID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('DefaultPackageType', 'MetaTblLabels', 'ID = ' + pLabelID, 'MetaCN'))
                if (tInventoryBatchOption == JobID):
                    if tPackageTypeID != 0:
                        tBatch = self.ID + '.' + str(tPackageTypeID) + '.' + str(tBatchNum)
                    else:
                        tBatch = self.ID + '.' + '1' + '.' + str(tBatchNum)
                elif (tInventoryBatchOption == JoshID):
                    if tPackageTypeID != 0:
                        tBatch = self.ActiveJosh.ID + '.' + str(tPackageTypeID) + '.' + str(tBatchNum)
                    else:
                        tBatch = self.ActiveJosh.ID + '.' + '1' + '.' + str(tBatchNum)
                elif (tInventoryBatchOption == ERPJobID):
                    tERPJobID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('ERPJobID', 'TblJob', 'ID = ' + str(self.ID), 'CN'))
                    if tERPJobID != '':
                        if tPackageTypeID != 0:
                            tBatch = tERPJobID + '.' + str(tPackageTypeID) + '.' + str(tBatchNum)
                        else:
                            tBatch = tERPJobID + '.' + '1' + '.' + str(tBatchNum)
                    else:
                        if tPackageTypeID != 0:
                            tBatch = self.ID + '.' + str(tPackageTypeID) + '.' + str(tBatchNum)
                        else:
                            tBatch = self.ID + '.' + '1' + '.' + str(tBatchNum)
            else:
                if (tInventoryBatchOption == JobID):
                    tBatch = self.ID + '.' + str(tBatchNum)
                elif (tInventoryBatchOption == JoshID):
                    tBatch = self.ActiveJosh.ID + '.' + str(tBatchNum)
                elif (tInventoryBatchOption == ERPJobID):
                    tERPJobID = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('ERPJobID', 'TblJob', 'ID = ' + str(self.ID), 'CN'))
                    if tERPJobID != '':
                        tBatch = tERPJobID + '.' + str(tBatchNum)
                    else:
                        tBatch = self.ID + '.' + str(tBatchNum)
            tJobID = self.ID
            tJoshID = self.ActiveJosh.ID
            tProductID = self.ProductID
            tCatalogID = self.Product.CatalogID
            if tCatalogID != '':
                tMaterialID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblMaterial', 'CatalogID=\'' + tCatalogID + '\'', 'CN'))
            else:
                tMaterialID = 0
            tShiftID = self.Machine.Server.CurrentShiftID
            tWareHouseID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('DefaultWareHouse', 'TblMachines', 'ID = ' + self.Machine.ID, 'CN'))
            tWareHouseLocationID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('DefaultWareHouseLocationID', 'TblMachines', 'ID = ' + self.Machine.ID, 'CN'))
            tClientID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ClientID', 'TblJob', 'ID = ' + str(self.ID), 'CN'))
            
            strFields = ''
            strValues = ''
            if tDataPrepared == True:
                strSQL = 'SELECT FieldName, Value FROM MetaTblLabelFieldValues WHERE UserID = 0 AND LabelID = ' + pLabelID
                RstValue.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
                RstValue.ActiveConnection = None
                strSQL = 'SELECT TOP 1 * FROM TblInventory'
                RstData.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                RstData.ActiveConnection = None
                while not RstValue.EOF:
                    if CheckIfRstFieldExists(RstData, RstValue.FieldName) == True:
                        strFields = strFields + ',' + RstValue.FieldName + ' '
                        strValues = strValues + ',\'' + RstValue.value + '\''
                    RstValue.MoveNext()
                RstValue.Close()
                RstData.Close()
            strSQL = 'INSERT INTO TblInventory'
            strSQL = strSQL + ' ('
            if InStr(strFields, ',CatalogID ') == 0:
                strSQL = strSQL + 'CatalogID,'
            if InStr(strFields, ',JobID ') == 0:
                strSQL = strSQL + 'JobID,'
            if InStr(strFields, ',JoshID ') == 0:
                strSQL = strSQL + 'JoshID,'
            if InStr(strFields, ',PackageTypeID ') == 0:
                if tPackageTypeID != 0:
                    strSQL = strSQL + 'PackageTypeID,'
            if InStr(strFields, ',PackageBatchNum ') == 0:
                strSQL = strSQL + 'PackageBatchNum,'
            if InStr(strFields, ',Batch ') == 0:
                strSQL = strSQL + 'Batch,'
            if InStr(strFields, ',MaterialID ') == 0:
                strSQL = strSQL + 'MaterialID,'
            if InStr(strFields, ',ProductID ') == 0:
                strSQL = strSQL + 'ProductID,'
            if InStr(strFields, ',ClientID ') == 0:
                strSQL = strSQL + 'ClientID,'
            if InStr(strFields, ',ShiftID ') == 0:
                strSQL = strSQL + 'ShiftID,'
            if InStr(strFields, ',Amount ') == 0:
                strSQL = strSQL + 'Amount,'
            if InStr(strFields, ',CatalogID ') == 0:
                strSQL = strSQL + 'EffectiveAmount,'
            if InStr(strFields, ',OriginalAmount ') == 0:
                strSQL = strSQL + 'OriginalAmount,'
            if InStr(strFields, ',EffectiveOriginalAmount ') == 0:
                strSQL = strSQL + 'EffectiveOriginalAmount,'
            if InStr(strFields, ',Date ') == 0:
                strSQL = strSQL + 'Date,'
            if InStr(strFields, ',LastUpdate ') == 0:
                strSQL = strSQL + 'LastUpdate,'
            if InStr(strFields, ',Status ') == 0:
                strSQL = strSQL + 'Status,'
            if InStr(strFields, ',WareHouseID ') == 0:
                strSQL = strSQL + 'WareHouseID'
            strSQL = strSQL + strFields
            strSQL = strSQL + ') '
            strSQL = strSQL + vbCrLf
            strSQL = strSQL + 'VALUES '
            strSQL = strSQL + '('
            if InStr(strFields, ',CatalogID ') == 0:
                strSQL = strSQL + '\'' + tCatalogID + '\','
            if InStr(strFields, ',JobID ') == 0:
                strSQL = strSQL + tJobID + ','
            if InStr(strFields, ',JoshID ') == 0:
                strSQL = strSQL + tJoshID + ','
            if InStr(strFields, ',PackageTypeID ') == 0:
                if tPackageTypeID != 0:
                    strSQL = strSQL + tPackageTypeID + ','
            if InStr(strFields, ',PackageBatchNum ') == 0:
                strSQL = strSQL + tBatchNum + ','
            if InStr(strFields, ',Batch ') == 0:
                strSQL = strSQL + '\'' + tBatch + '\','
            if InStr(strFields, ',MaterialID ') == 0:
                strSQL = strSQL + tMaterialID + ','
            if InStr(strFields, ',ProductID ') == 0:
                strSQL = strSQL + tProductID + ','
            if InStr(strFields, ',ClientID ') == 0:
                strSQL = strSQL + tClientID + ','
            if InStr(strFields, ',ShiftID ') == 0:
                strSQL = strSQL + tShiftID + ','
            if InStr(strFields, ',Amount ') == 0:
                strSQL = strSQL + '1' + ','
            if InStr(strFields, ',EffectiveAmount ') == 0:
                strSQL = strSQL + tEffectiveAmount + ','
            if InStr(strFields, ',OriginalAmount ') == 0:
                strSQL = strSQL + '1' + ','
            if InStr(strFields, ',EffectiveOriginalAmount ') == 0:
                strSQL = strSQL + tEffectiveAmount + ','
            if InStr(strFields, ',Date ') == 0:
                strSQL = strSQL + '\'' + Format(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn') + '\','
            if InStr(strFields, ',LastUpdate ') == 0:
                strSQL = strSQL + '\'' + Format(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn') + '\','
            if InStr(strFields, ',Status ') == 0:
                strSQL = strSQL + tStatus + ','
            if InStr(strFields, ',WareHouseID ') == 0:
                strSQL = strSQL + tWareHouseID
            strSQL = strSQL + strValues
            strSQL = strSQL + ')'
            CN.Execute(strSQL)
            tInventoryID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('TOP 1 ID', 'TblInventory', 'JobID = ' + tJobID + ' ORDER BY ID DESC', 'CN'))
            AddInventoryHistoryRecord(tInventoryID, 1)
            CreateInventoryTrace(tInventoryID, self.ActiveJosh.ID)
            if tAddToActivePallet:
                AddInventoryItemToActivePallet(tInventoryID, self.Machine)
            if (tUnitsReportedOkFrom == UnitsReportedOKFromOption.Box):
                
                strFields = ''
                strValues = ''
                if tDataPrepared == True:
                    strSQL = 'SELECT FieldName, Value FROM MetaTblLabelFieldValues WHERE UserID = 0 AND LabelID = ' + pLabelID
                    RstValue.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
                    RstValue.ActiveConnection = None
                    strSQL = 'SELECT TOP 1 * FROM TblPackages'
                    RstData.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                    RstData.ActiveConnection = None
                    while not RstValue.EOF:
                        if CheckIfRstFieldExists(RstData, RstValue.FieldName) == True:
                            strFields = strFields + ',' + RstValue.FieldName + ' '
                            strValues = strValues + ',\'' + RstValue.value + '\''
                        RstValue.MoveNext()
                    RstValue.Close()
                    RstData.Close()
                strSQL = 'INSERT INTO TblPackages'
                strSQL = strSQL + ' ('
                if InStr(strFields, ',ProductID ') == 0:
                    strSQL = strSQL + 'ProductID,'
                if InStr(strFields, ',ClientID ') == 0:
                    strSQL = strSQL + 'ClientID,'
                if InStr(strFields, ',BoxUnits ') == 0:
                    strSQL = strSQL + 'BoxUnits,'
                if InStr(strFields, ',Date ') == 0:
                    strSQL = strSQL + 'Date,'
                if InStr(strFields, ',Shift ') == 0:
                    strSQL = strSQL + 'Shift,'
                if InStr(strFields, ',JobID ') == 0:
                    strSQL = strSQL + 'JobID,'
                if InStr(strFields, ',PackageBatchNum ') == 0:
                    strSQL = strSQL + 'PackageBatchNum,'
                if InStr(strFields, ',PackageTypeID ') == 0:
                    if tPackageTypeID != 0:
                        strSQL = strSQL + 'PackageTypeID,'
                if InStr(strFields, ',CatalogID ') == 0:
                    strSQL = strSQL + 'CatalogID'
                strSQL = strSQL + strFields
                strSQL = strSQL + ') '
                strSQL = strSQL + vbCrLf
                strSQL = strSQL + 'VALUES '
                strSQL = strSQL + '('
                if InStr(strFields, ',ProductID ') == 0:
                    strSQL = strSQL + tProductID + ','
                if InStr(strFields, ',ClientID ') == 0:
                    strSQL = strSQL + tClientID + ','
                if InStr(strFields, ',BoxUnits ') == 0:
                    strSQL = strSQL + tEffectiveAmount + ','
                if InStr(strFields, ',Date ') == 0:
                    strSQL = strSQL + '\'' + Format(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn') + '\','
                if InStr(strFields, ',Shift ') == 0:
                    strSQL = strSQL + tShiftID + ','
                if InStr(strFields, ',JobID ') == 0:
                    strSQL = strSQL + tJobID + ','
                if InStr(strFields, ',PackageBatchNum ') == 0:
                    strSQL = strSQL + tBatchNum + ','
                if InStr(strFields, ',PackageTypeID ') == 0:
                    if tPackageTypeID != 0:
                        strSQL = strSQL + tPackageTypeID + ','
                if InStr(strFields, ',CatalogID ') == 0:
                    strSQL = strSQL + '\'' + tCatalogID + '\''
                strSQL = strSQL + strValues
                strSQL = strSQL + ')'
                CN.Execute(strSQL)
            elif (tUnitsReportedOkFrom == UnitsReportedOKFromOption.Pallet):
                tBoxUnits = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('BoxUnits', 'TblProduct', 'ID = ' + self.ProductID, 'CN'))
                tAmountFullBoxes = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('PalletBoxes', 'TblProduct', 'ID = ' + self.ProductID, 'CN'))
                
                strFields = ''
                strValues = ''
                if tDataPrepared == True:
                    strSQL = 'SELECT FieldName, Value FROM MetaTblLabelFieldValues WHERE UserID = 0 AND LabelID = ' + pLabelID
                    RstValue.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
                    RstValue.ActiveConnection = None
                    strSQL = 'SELECT TOP 1 * FROM TblPallete'
                    RstData.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                    RstData.ActiveConnection = None
                    while not RstValue.EOF:
                        if CheckIfRstFieldExists(RstData, RstValue.FieldName) == True:
                            strFields = strFields + ',' + RstValue.FieldName + ' '
                            strValues = strValues + ',\'' + RstValue.value + '\''
                        RstValue.MoveNext()
                    RstValue.Close()
                    RstData.Close()
                strSQL = 'INSERT INTO TblPallete'
                strSQL = strSQL + ' ('
                if InStr(strFields, ',ProductID ') == 0:
                    strSQL = strSQL + 'ProductID,'
                if InStr(strFields, ',ClientID ') == 0:
                    strSQL = strSQL + 'ClientID,'
                if InStr(strFields, ',Amount ') == 0:
                    strSQL = strSQL + 'Amount,'
                if InStr(strFields, ',BoxUnits ') == 0:
                    strSQL = strSQL + 'BoxUnits,'
                if InStr(strFields, ',AmountFullBoxes ') == 0:
                    strSQL = strSQL + 'AmountFullBoxes,'
                if InStr(strFields, ',Date ') == 0:
                    strSQL = strSQL + 'Date,'
                if InStr(strFields, ',ShiftID ') == 0:
                    strSQL = strSQL + 'ShiftID,'
                if InStr(strFields, ',JobID ') == 0:
                    strSQL = strSQL + 'JobID,'
                if InStr(strFields, ',JoshID ') == 0:
                    strSQL = strSQL + 'JoshID,'
                if InStr(strFields, ',PalletBatchNum ') == 0:
                    strSQL = strSQL + 'PalletBatchNum,'
                if InStr(strFields, ',PackageTypeID ') == 0:
                    if tPackageTypeID != 0:
                        strSQL = strSQL + 'PackageTypeID,'
                if InStr(strFields, ',CatalogID ') == 0:
                    strSQL = strSQL + 'CatalogID'
                strSQL = strSQL + strFields
                strSQL = strSQL + ') '
                strSQL = strSQL + vbCrLf
                strSQL = strSQL + 'VALUES '
                strSQL = strSQL + '('
                if InStr(strFields, ',ProductID ') == 0:
                    strSQL = strSQL + tProductID + ','
                if InStr(strFields, ',ClientID ') == 0:
                    strSQL = strSQL + tClientID + ','
                if InStr(strFields, ',Amount ') == 0:
                    strSQL = strSQL + '1' + ','
                if InStr(strFields, ',BoxUnits ') == 0:
                    strSQL = strSQL + tBoxUnits + ','
                if InStr(strFields, ',AmountFullBoxes ') == 0:
                    strSQL = strSQL + tAmountFullBoxes + ','
                if InStr(strFields, ',Date ') == 0:
                    strSQL = strSQL + '\'' + Format(mdl_Common.NowGMT(), 'yyyy-mm-dd HH:nn') + '\','
                if InStr(strFields, ',ShiftID ') == 0:
                    strSQL = strSQL + tShiftID + ','
                if InStr(strFields, ',JobID ') == 0:
                    strSQL = strSQL + tJobID + ','
                if InStr(strFields, ',JoshID ') == 0:
                    strSQL = strSQL + tJoshID + ','
                if InStr(strFields, ',PalletBatchNum ') == 0:
                    strSQL = strSQL + tBatchNum + ','
                if InStr(strFields, ',PackageTypeID ') == 0:
                    if tPackageTypeID != 0:
                        strSQL = strSQL + tPackageTypeID + ','
                if InStr(strFields, ',CatalogID ') == 0:
                    strSQL = strSQL + '\'' + tCatalogID + '\''
                strSQL = strSQL + strValues
                strSQL = strSQL + ')'
                CN.Execute(strSQL)
            if (tUnitsReportedOkFrom == UnitsReportedOKFromOption.Box):
                strSQL = 'UPDATE TblJob SET PackageBatchNum = ' +  ( tBatchNum + 1 )  + ' WHERE ID = ' + tJobID
                CN.Execute(strSQL)
                strSQL = 'UPDATE TblJobCurrent SET PackageBatchNum = ' +  ( tBatchNum + 1 )  + ' WHERE ID = ' + tJobID
                CN.Execute(strSQL)
            elif (tUnitsReportedOkFrom == UnitsReportedOKFromOption.Pallet):
                strSQL = 'UPDATE TblJob SET PalletBatchNum = ' +  ( tBatchNum + 1 )  + ' WHERE ID = ' + tJobID
                CN.Execute(strSQL)
                strSQL = 'UPDATE TblJobCurrent SET PalletBatchNum = ' +  ( tBatchNum + 1 )  + ' WHERE ID = ' + tJobID
                CN.Execute(strSQL)
            self.UnitsReportedOK = self.UnitsReportedOK + tEffectiveAmount
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.ReportInventoryItem:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def Terminate(self):
        tVariant = None

        tVariant2 = None

        tChannel = Channel()

        tSplit = ChannelSplit()
        
        
        for tVariant in self.ControllerChannels:
            tChannel = tVariant
            if not tChannel.Splits is None:
                for tVariant2 in tChannel.Splits:
                    tSplit = tVariant2
                    tChannel.Splits.Remove(( str(tSplit.SplitNum) ))
                    tSplit.MaterialID = None
                    tSplit.MaterialBatch = None
                    tSplit.MaterialPCTarget = None
                    tSplit.MaterialPC = None
                    tSplit.TotalWeight = None
                    tSplit.ForecastWeight = None
                    tSplit = None
            tChannel.Splits = None
            tChannel.MaterialID = None
            tChannel.MaterialPCTarget = None
            tChannel.MaterialPC = None
            tChannel.MaterialBatch = None
            tChannel.TotalWeight = None
            tChannel.ForecastWeight = None
            self.ControllerChannels.Remove(( str(tChannel.ChannelNum) ))
            tChannel = None
        if Err.Number != 0:
            Err.Clear()
        tVariant = None
        tVariant2 = None

    def __del__(self):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        if Err.Number != 0:
            Err.Clear()
            

    def LoadAlarms(self):
        tControlParam = None
        tAlarm = None
        
        try:
            if self.Status == 10:
                for tControlParam in self.Machine.CParams.values():
                    if tControlParam.ErrorAlarmActive:
                        if not tControlParam.Alarms is None:
                            for tAlarm in tControlParam.Alarms.values():
                                self.AddAlarm(tAlarm)

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.LoadAlarms:', str(0), error.args[0], 'JobID:' + str(self.ID))

    def Refresh(self):
        strSQL = ''

        RstCursor = None

        tVariant = None

        tJob = Job()

        jdRstCursor = None
        
        strSQL = 'SELECT * FROM TblJob WHERE ID = ' + str(self.ID)
        RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        RstCursor.ActiveConnection = None
        if RstData:
            if MdlADOFunctions.fGetRstValString(RstCursor.StartTime) != '':
                self.StartTime = RstCursor.StartTime
            if MdlADOFunctions.fGetRstValString(RstCursor.EndTime) != '':
                self.EndTime = RstCursor.EndTime
            if MdlADOFunctions.fGetRstValString(RstCursor.SetUpStart) != '':
                self.SetUpStart = RstCursor.SetUpStart
            if MdlADOFunctions.fGetRstValString(RstCursor.SetUpEnd) != '':
                self.SetUpEnd = RstCursor.SetUpEnd
                self.Machine.NewJob = False
                self.SetUpEndInjectionsCount = MdlADOFunctions.fGetRstValDouble(RstCursor.SetUpEndInjectionsCount)
                
                self.SetUpEndAutoRejects = MdlADOFunctions.fGetRstValDouble(RstCursor.SetUpEndAutoRejects)
            else:
                self.Machine.NewJob = True
            
            self.AutoRejects = MdlADOFunctions.fGetRstValDouble(RstCursor.AutoRejects)
            self.SetupDuration = MdlADOFunctions.fGetRstValLong(RstCursor.SetupDuration)
            self.ProductID = MdlADOFunctions.fGetRstValLong(RstCursor.ProductID)
            self.Product = GetOrCreateProduct(self.Machine.Server, self.ProductID)
            self.MoldID = MdlADOFunctions.fGetRstValLong(RstCursor.MoldID)
            self.Mold = GetOrCreateMold(self.Machine.Server, self.MoldID)
            self.GetUnitsInCycle(RstCursor)
            self.MachineID = MdlADOFunctions.fGetRstValLong(RstCursor.MachineID)
            self.DepartmentID = MdlADOFunctions.fGetRstValLong(RstCursor.Department)
            self.Department = GetOrCreateDepartment(self.Machine.Server, self.DepartmentID)
            self.MachineType = GetOrCreateMachineType(self.Machine.Server, MdlADOFunctions.fGetRstValLong(RstCursor.MachineType))
            self.InjectionsCount = MdlADOFunctions.fGetRstValDouble(RstCursor.InjectionsCount)
            self.InjectionsCountLast = MdlADOFunctions.fGetRstValDouble(RstCursor.InjectionsCountLast)
            self.InjectionsCountStart = MdlADOFunctions.fGetRstValDouble(RstCursor.InjectionsCountStart)
            self.UnitsTarget = MdlADOFunctions.fGetRstValDouble(RstCursor.UnitsTarget)
            self.UnitsProduced = MdlADOFunctions.fGetRstValDouble(RstCursor.UnitsProduced)
            self.UnitsProducedOK = MdlADOFunctions.fGetRstValDouble(RstCursor.UnitsProducedOK)
            self.UnitsProducedLeft = MdlADOFunctions.fGetRstValDouble(RstCursor.UnitsProducedLeft)
            self.UnitsProducedTheoretically = MdlADOFunctions.fGetRstValDouble(RstCursor.UnitsProducedTheoretically)
            self.UnitsProducedTheoreticallyPC = MdlADOFunctions.fGetRstValDouble(RstCursor.UnitsProducedTheoreticallyPC)
            self.QuantityAdjustmentUnits = MdlADOFunctions.fGetRstValDouble(RstCursor.QuantityAdjustmentUnits)
            self.DurationMin = MdlADOFunctions.fGetRstValLong(RstCursor.DurationMin)
            self.DownTimeMin = MdlADOFunctions.fGetRstValLong(RstCursor.DownTimeMin)
            self.InActiveTimeMin = MdlADOFunctions.fGetRstValLong(RstCursor.InActiveTimeMin)
            self.OriginalJobID = MdlADOFunctions.fGetRstValLong(RstCursor.OriginalJobID)
            self.OriginalUnitsTarget = MdlADOFunctions.fGetRstValDouble(RstCursor.OriginalUnitsTarget)
            self.OriginalUnitsProducedOK = MdlADOFunctions.fGetRstValDouble(RstCursor.OriginalUnitsProducedOK)
            self.ProductWeightAvg = MdlADOFunctions.fGetRstValDouble(RstCursor.ProductWeightAvg)
            self.ProductWeightStandard = MdlADOFunctions.fGetRstValDouble(RstCursor.ProductWeightStandard)
            self.ProductRecipeWeight = MdlADOFunctions.fGetRstValDouble(RstCursor.ProductRecipeWeight)
            if self.ProductRecipeWeight == 0:
                self.ProductRecipeWeight = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(self.Product.ID, 'ProductWeight', 0, 0))
            self.CycleTimeStandard = MdlADOFunctions.fGetRstValDouble(RstCursor.CycleTimeStandard)
            self.CycleTimeAvg = MdlADOFunctions.fGetRstValDouble(RstCursor.CycleTimeAvg)
            self.Status = MdlADOFunctions.fGetRstValLong(RstCursor.Status)
            self.EngineTimeMin = MdlADOFunctions.fGetRstValLong(RstCursor.EngineTimeMin)
            
            self.PConfigID = MdlADOFunctions.fGetRstValLong(RstCursor.PConfigID)
            self.PConfigPC = MdlADOFunctions.fGetRstValDouble(RstCursor.PConfigPC)
            
            self.PConfigUnits = MdlADOFunctions.fGetRstValDouble(RstCursor.PConfigUnits)
            self.PConfigJobID = MdlADOFunctions.fGetRstValLong(RstCursor.PConfigJobID)
            self.PConfigParentID = MdlADOFunctions.fGetRstValLong(RstCursor.PConfigParentID)
            self.IsPConfigMain = MdlADOFunctions.fGetRstValBool(RstCursor.IsPConfigMain, True)
            self.PConfigIsMaterialCount = MdlADOFunctions.fGetRstValBool(RstCursor.PConfigIsMaterialCount, True)
            self.PConfigIsChannel100Count = MdlADOFunctions.fGetRstValBool(RstCursor.PConfigIsChannel100Count, True)
            self.PConfigIsSpecialMaterialCount = MdlADOFunctions.fGetRstValBool(RstCursor.PConfigIsSpecialMaterialCount, True)
            
            self.JobDef = MdlADOFunctions.fGetRstValLong(RstCursor.ERPJobDef)
            if self.JobDef > 0:
                strSQL = 'SELECT * FROM STblJobDefinitions WHERE ID = ' + self.JobDef
                jdRstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                jdRstCursor.ActiveConnection = None
                if jdRstData:
                    self.JobDefCalcEfficiencies = MdlADOFunctions.fGetRstValBool(( jdRstCursor.CalcEfficiencies ), True)
                    self.JobDefDisableProductionTime = MdlADOFunctions.fGetRstValBool(( jdRstCursor.DisableProductionTime ), False)
                    self.JobDefSetUpEndGeneralCycles = MdlADOFunctions.fGetRstValDouble(jdRstCursor.SetUpEndGeneralCycles)
                jdRstCursor.close()
            
            self.RecipeRefType = MdlADOFunctions.fGetRstValLong(RstCursor.RecipeRefType)
            self.RecipeRefJob = MdlADOFunctions.fGetRstValLong(RstCursor.RecipeRefJob)
            self.RecipeRefStandardID = MdlADOFunctions.fGetRstValLong(RstCursor.RecipeRefStandardID)
            self.GetRefRecipeProductWeight
            self.GetRefRecipeUnitWeight
            if self.RecipeRefStandardID != 0:
                self.ProductStandardRecipeWeight = MdlADOFunctions.fGetRstValDouble(MdlUtils.fGetRecipeValueStandard(self.RecipeRefStandardID, 'ProductWeight', 0, 0, self.Product.ID))
            self.MaterialRecipeIndexJob = MdlADOFunctions.fGetRstValDouble(RstCursor.MaterialRecipeIndexJob)
            self.MaterialRecipeIndexProduct = MdlADOFunctions.fGetRstValDouble(RstCursor.MaterialRecipeIndexProduct)
            self.UnitsReportedOK = MdlADOFunctions.fGetRstValDouble(RstCursor.UnitsReportedOK)
            
            self.GetOpenEvent
            
            self.GetOpenWorkingEvent
            
            self.GetOpenEngineEvent
            
            self.ProductWeightStandard = MdlADOFunctions.fGetRstValDouble(RstCursor.ProductWeightStandard)
            self.ProductWeightAvg = MdlADOFunctions.fGetRstValDouble(RstCursor.ProductWeightAvg)
            self.ProductWeightLast = MdlADOFunctions.fGetRstValDouble(RstCursor.ProductWeightLast)
            self.ProductRecipeWeight = MdlADOFunctions.fGetRstValDouble(RstCursor.ProductRecipeWeight)
            
            if self.PConfigID > 0 and self.IsPConfigMain == False:
                self.Status = self.PConfigParentJob.Status
            
            
            if self.PConfigID != 0 and self.MachineType.PConfigSonsRefRecipeSource == PConfigSonsRefRecipeSourceOption.FromProductRecipe:
                self.ProductWeightStandard = MdlUtilsH.fGetRecipeValueJob(self.ID, 'ProductWeight', 0, 0)
                self.ProductWeightLast = self.ProductWeightStandard
                self.ProductWeightAvg = self.ProductWeightStandard
            
            if self.PConfigID > 0 and self.IsPConfigMain == True:
                for tVariant in self.PConfigJobs:
                    tJob = tVariant
                    tJob.Refresh
            
            self.ValidationLog = MdlADOFunctions.fGetRstValString(RstCursor.ValidationLog)
            
            if GlobalVariables.IsDate(RstCursor.NextJobMaterialFlowStart):
                self.NextJobMaterialFlowStart = datetime.strptime(RstCursor.NextJobMaterialFlowStart, '%d/%m/%Y %H:%M:%S')
        RstCursor.close()
        
        if self.Status == 10 and  ( self.PConfigID == 0 or  ( self.PConfigID != 0 and self.IsPConfigMain == True ) ) :
            self.InitMachineControlParams
            self.InitMoldChangeDetails
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.Refresh:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()

    def __CalcEngineTimesFromDB(self):
        strSQL = ''

        RstCursor = None
        
        strSQL = 'SELECT EngineTimeMin FROM ViewRTJobEngineEvents WHERE ID = ' + str(self.ID)
        RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        RstCursor.ActiveConnection = None
        if RstData:
            self.EngineTimeMin = MdlADOFunctions.fGetRstValLong(RstCursor.EngineTimeMin)
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
                
            MdlGlobal.RecordError(type(self).__name__ + '.CalcEngineTimesFromDB:', str(0), error.args[0], 'JobID:' + str(self.ID))
            Err.Clear()
        RstCursor = None


    def setEngineTimeMin(self, value):
        self.__mEngineTimeMin = value

    def getEngineTimeMin(self):
        returnVal = None
        returnVal = self.__mEngineTimeMin
        return returnVal
    EngineTimeMin = property(fset=setEngineTimeMin, fget=getEngineTimeMin)


    
    def setOpenEngineEvent(self, value):
        self.__mOpenEngineEvent = value

    def getOpenEngineEvent(self):
        returnVal = None
        returnVal = self.__mOpenEngineEvent
        return returnVal
    OpenEngineEvent = property(fset=setOpenEngineEvent, fget=getOpenEngineEvent)


    def setQuantityAdjustmentUnits(self, value):
        self.__mQuantityAdjustmentUnits = value

    def getQuantityAdjustmentUnits(self):
        returnVal = None
        returnVal = self.__mQuantityAdjustmentUnits
        return returnVal
    QuantityAdjustmentUnits = property(fset=setQuantityAdjustmentUnits, fget=getQuantityAdjustmentUnits)


    def setSetupTypeSetUpEndGeneralCycles(self, value):
        self.__mSetupTypeSetUpEndGeneralCycles = value

    def getSetupTypeSetUpEndGeneralCycles(self):
        returnVal = None
        returnVal = self.__mSetupTypeSetUpEndGeneralCycles
        return returnVal
    SetupTypeSetUpEndGeneralCycles = property(fset=setSetupTypeSetUpEndGeneralCycles, fget=getSetupTypeSetUpEndGeneralCycles)


    def setPlannedSetupType(self, value):
        self.__mPlannedSetupType = value

    def getPlannedSetupType(self):
        returnVal = None
        returnVal = self.__mPlannedSetupType
        return returnVal
    PlannedSetupType = property(fset=setPlannedSetupType, fget=getPlannedSetupType)


    def setERPJobIndexKey(self, value):
        self.__mERPJobIndexKey = value

    def getERPJobIndexKey(self):
        returnVal = None
        returnVal = self.__mERPJobIndexKey
        return returnVal
    ERPJobIndexKey = property(fset=setERPJobIndexKey, fget=getERPJobIndexKey)


    def setJobDefSetUpEndGeneralCycles(self, value):
        self.__mJobDefSetUpEndGeneralCycles = value

    def getJobDefSetUpEndGeneralCycles(self):
        returnVal = None
        returnVal = self.__mJobDefSetUpEndGeneralCycles
        return returnVal
    JobDefSetUpEndGeneralCycles = property(fset=setJobDefSetUpEndGeneralCycles, fget=getJobDefSetUpEndGeneralCycles)


    def setJobDefDisableProductionTime(self, value):
        self.__mJobDefDisableProductionTime = value

    def getJobDefDisableProductionTime(self):
        returnVal = None
        returnVal = self.__mJobDefDisableProductionTime
        return returnVal
    JobDefDisableProductionTime = property(fset=setJobDefDisableProductionTime, fget=getJobDefDisableProductionTime)


    def setJobDefCalcEfficiencies(self, value):
        self.__mJobDefCalcEfficiencies = value

    def getJobDefCalcEfficiencies(self):
        returnVal = None
        returnVal = self.__mJobDefCalcEfficiencies
        return returnVal
    JobDefCalcEfficiencies = property(fset=setJobDefCalcEfficiencies, fget=getJobDefCalcEfficiencies)


    def setJobDef(self, value):
        self.__mJobDef = value

    def getJobDef(self):
        returnVal = None
        returnVal = self.__mJobDef
        return returnVal
    JobDef = property(fset=setJobDef, fget=getJobDef)


    def setUnitsProducedTheoreticallyPC(self, value):
        self.__mUnitsProducedTheoreticallyPC = value

    def getUnitsProducedTheoreticallyPC(self):
        returnVal = None
        returnVal = self.__mUnitsProducedTheoreticallyPC
        return returnVal
    UnitsProducedTheoreticallyPC = property(fset=setUnitsProducedTheoreticallyPC, fget=getUnitsProducedTheoreticallyPC)


    def setUnitsProducedTheoretically(self, value):
        self.__mUnitsProducedTheoretically = value

    def getUnitsProducedTheoretically(self):
        returnVal = None
        returnVal = self.__mUnitsProducedTheoretically
        return returnVal
    UnitsProducedTheoretically = property(fset=setUnitsProducedTheoretically, fget=getUnitsProducedTheoretically)


    def setSetUpProductionTimeMin(self, value):
        self.__mSetUpProductionTimeMin = value

    def getSetUpProductionTimeMin(self):
        returnVal = None
        returnVal = self.__mSetUpProductionTimeMin
        return returnVal
    SetUpProductionTimeMin = property(fset=setSetUpProductionTimeMin, fget=getSetUpProductionTimeMin)


    def setSetUpDownTimeMin(self, value):
        self.__mSetUpDownTimeMin = value

    def getSetUpDownTimeMin(self):
        returnVal = None
        returnVal = self.__mSetUpDownTimeMin
        return returnVal
    SetUpDownTimeMin = property(fset=setSetUpDownTimeMin, fget=getSetUpDownTimeMin)


    def setAutoRejects(self, value):
        self.__mAutoRejects = value

    def getAutoRejects(self):
        returnVal = None
        returnVal = self.__mAutoRejects
        return returnVal
    AutoRejects = property(fset=setAutoRejects, fget=getAutoRejects)


    def setSetUpEndAutoRejects(self, value):
        self.__mSetUpEndAutoRejects = value

    def getSetUpEndAutoRejects(self):
        returnVal = None
        returnVal = self.__mSetUpEndAutoRejects
        return returnVal
    SetUpEndAutoRejects = property(fset=setSetUpEndAutoRejects, fget=getSetUpEndAutoRejects)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    def setLastJobID(self, value):
        self.__mLastJobID = value

    def getLastJobID(self):
        returnVal = None
        returnVal = self.__mLastJobID
        return returnVal
    LastJobID = property(fset=setLastJobID, fget=getLastJobID)


    def setProductID(self, value):
        self.__mProductID = value

    def getProductID(self):
        returnVal = None
        returnVal = self.__mProductID
        return returnVal
    ProductID = property(fset=setProductID, fget=getProductID)


    
    def setProduct(self, value):
        self.__mProduct = value

    def getProduct(self):
        returnVal = None
        returnVal = self.__mProduct
        return returnVal
    Product = property(fset=setProduct, fget=getProduct)


    
    def setActiveJosh(self, value):
        self.__mActiveJosh = value

    def getActiveJosh(self):
        returnVal = None
        returnVal = self.__mActiveJosh
        return returnVal
    ActiveJosh = property(fset=setActiveJosh, fget=getActiveJosh)


    
    def setMoldID(self, value):
        self.__mMoldID = value

    def getMoldID(self):
        returnVal = None
        returnVal = self.__mMoldID
        return returnVal
    MoldID = property(fset=setMoldID, fget=getMoldID)


    
    def setMold(self, value):
        self.__mMold = value

    def getMold(self):
        returnVal = None
        returnVal = self.__mMold
        return returnVal
    Mold = property(fset=setMold, fget=getMold)


    def setMachineID(self, value):
        self.__mMachineID = value

    def getMachineID(self):
        returnVal = None
        returnVal = self.__mMachineID
        return returnVal
    MachineID = property(fset=setMachineID, fget=getMachineID)


    
    def setMachine(self, value):
        self.__mMachine = value

    def getMachine(self):
        returnVal = None
        returnVal = self.__mMachine
        return returnVal
    Machine = property(fset=setMachine, fget=getMachine)


    def setDepartmentID(self, value):
        self.__mDepartmentID = value

    def getDepartmentID(self):
        returnVal = None
        returnVal = self.__mDepartmentID
        return returnVal
    DepartmentID = property(fset=setDepartmentID, fget=getDepartmentID)


    
    def setDepartment(self, value):
        self.__mDepartment = value

    def getDepartment(self):
        returnVal = None
        returnVal = self.__mDepartment
        return returnVal
    Department = property(fset=setDepartment, fget=getDepartment)


    
    def setMachineType(self, value):
        self.__mMachineType = value

    def getMachineType(self):
        returnVal = None
        returnVal = self.__mMachineType
        return returnVal
    MachineType = property(fset=setMachineType, fget=getMachineType)


    def setStatus(self, value):
        self.__mStatus = value

    def getStatus(self):
        returnVal = None
        returnVal = self.__mStatus
        return returnVal
    Status = property(fset=setStatus, fget=getStatus)


    def setMachineStatus(self, value):
        self.__mMachineStatus = value

    def getMachineStatus(self):
        returnVal = None
        returnVal = self.__mMachineStatus
        return returnVal
    MachineStatus = property(fset=setMachineStatus, fget=getMachineStatus)


    def setStartTimeTarget(self, value):
        self.__mStartTimeTarget = value

    def getStartTimeTarget(self):
        returnVal = None
        returnVal = self.__mStartTimeTarget
        return returnVal
    StartTimeTarget = property(fset=setStartTimeTarget, fget=getStartTimeTarget)


    def setStartTime(self, value):
        self.__mStartTime = value

    def getStartTime(self):
        returnVal = None
        returnVal = self.__mStartTime
        return returnVal
    StartTime = property(fset=setStartTime, fget=getStartTime)


    def setEndTimeTarget(self, value):
        self.__mEndTimeTarget = value

    def getEndTimeTarget(self):
        returnVal = None
        returnVal = self.__mEndTimeTarget
        return returnVal
    EndTimeTarget = property(fset=setEndTimeTarget, fget=getEndTimeTarget)


    def setEndTime(self, value):
        self.__mEndTime = value

    def getEndTime(self):
        returnVal = None
        returnVal = self.__mEndTime
        return returnVal
    EndTime = property(fset=setEndTime, fget=getEndTime)


    def setSetUpStart(self, value):
        self.__mSetUpStart = value

    def getSetUpStart(self):
        returnVal = None
        returnVal = self.__mSetUpStart
        return returnVal
    SetUpStart = property(fset=setSetUpStart, fget=getSetUpStart)


    def setSetUpEnd(self, value):
        self.__mSetUpEnd = value

    def getSetUpEnd(self):
        returnVal = None
        returnVal = self.__mSetUpEnd
        return returnVal
    SetUpEnd = property(fset=setSetUpEnd, fget=getSetUpEnd)


    def setSetUpEndInjectionsCount(self, value):
        self.__mSetUpEndInjectionsCount = value

    def getSetUpEndInjectionsCount(self):
        returnVal = None
        returnVal = self.__mSetUpEndInjectionsCount
        return returnVal
    SetUpEndInjectionsCount = property(fset=setSetUpEndInjectionsCount, fget=getSetUpEndInjectionsCount)


    def setSetUpEndActiveTimeMin(self, value):
        self.__mSetUpEndActiveTimeMin = value

    def getSetUpEndActiveTimeMin(self):
        returnVal = None
        returnVal = self.__mSetUpEndActiveTimeMin
        return returnVal
    SetUpEndActiveTimeMin = property(fset=setSetUpEndActiveTimeMin, fget=getSetUpEndActiveTimeMin)


    def setTimeLeftHr(self, value):
        self.__mTimeLeftHr = value

    def getTimeLeftHr(self):
        returnVal = None
        returnVal = self.__mTimeLeftHr
        return returnVal
    TimeLeftHr = property(fset=setTimeLeftHr, fget=getTimeLeftHr)


    def setDurationMin(self, value):
        self.__mDurationMin = value

    def getDurationMin(self):
        returnVal = None
        returnVal = self.__mDurationMin
        return returnVal
    DurationMin = property(fset=setDurationMin, fget=getDurationMin)


    def setInActiveTimeMin(self, value):
        self.__mInActiveTimeMin = value

    def getInActiveTimeMin(self):
        returnVal = None
        returnVal = self.__mInActiveTimeMin
        return returnVal
    InActiveTimeMin = property(fset=setInActiveTimeMin, fget=getInActiveTimeMin)


    def setInActiveTimePC(self, value):
        self.__mInActiveTimePC = value

    def getInActiveTimePC(self):
        returnVal = None
        returnVal = self.__mInActiveTimePC
        return returnVal
    InActiveTimePC = property(fset=setInActiveTimePC, fget=getInActiveTimePC)


    def setActiveTimeMin(self, value):
        self.__mActiveTimeMin = value

    def getActiveTimeMin(self):
        returnVal = None
        returnVal = self.__mActiveTimeMin
        return returnVal
    ActiveTimeMin = property(fset=setActiveTimeMin, fget=getActiveTimeMin)


    def setActiveTimePC(self, value):
        self.__mActiveTimePC = value

    def getActiveTimePC(self):
        returnVal = None
        returnVal = self.__mActiveTimePC
        return returnVal
    ActiveTimePC = property(fset=setActiveTimePC, fget=getActiveTimePC)


    def setProductionTimeMin(self, value):
        self.__mProductionTimeMin = value

    def getProductionTimeMin(self):
        returnVal = None
        returnVal = self.__mProductionTimeMin
        return returnVal
    ProductionTimeMin = property(fset=setProductionTimeMin, fget=getProductionTimeMin)


    def setProductionTimePC(self, value):
        self.__mProductionTimePC = value

    def getProductionTimePC(self):
        returnVal = None
        returnVal = self.__mProductionTimePC
        return returnVal
    ProductionTimePC = property(fset=setProductionTimePC, fget=getProductionTimePC)


    def setProductionUsabilityPC(self, value):
        self.__mProductionUsabilityPC = value

    def getProductionUsabilityPC(self):
        returnVal = None
        returnVal = self.__mProductionUsabilityPC
        return returnVal
    ProductionUsabilityPC = property(fset=setProductionUsabilityPC, fget=getProductionUsabilityPC)


    def setDownTimeMin(self, value):
        self.__mDownTimeMin = value

    def getDownTimeMin(self):
        returnVal = None
        returnVal = self.__mDownTimeMin
        return returnVal
    DownTimeMin = property(fset=setDownTimeMin, fget=getDownTimeMin)


    def setDownTimePC(self, value):
        self.__mDownTimePC = value

    def getDownTimePC(self):
        returnVal = None
        returnVal = self.__mDownTimePC
        return returnVal
    DownTimePC = property(fset=setDownTimePC, fget=getDownTimePC)


    def setEffectiveDurationMin(self, value):
        self.__mEffectiveDurationMin = value

    def getEffectiveDurationMin(self):
        returnVal = None
        returnVal = self.__mEffectiveDurationMin
        return returnVal
    EffectiveDurationMin = property(fset=setEffectiveDurationMin, fget=getEffectiveDurationMin)


    def setEffectiveDownTimeMin(self, value):
        self.__mEffectiveDownTimeMin = value

    def getEffectiveDownTimeMin(self):
        returnVal = None
        returnVal = self.__mEffectiveDownTimeMin
        return returnVal
    EffectiveDownTimeMin = property(fset=setEffectiveDownTimeMin, fget=getEffectiveDownTimeMin)


    def setEffectiveInActiveTimeMin(self, value):
        self.__mEffectiveInActiveTimeMin = value

    def getEffectiveInActiveTimeMin(self):
        returnVal = None
        returnVal = self.__mEffectiveInActiveTimeMin
        return returnVal
    EffectiveInActiveTimeMin = property(fset=setEffectiveInActiveTimeMin, fget=getEffectiveInActiveTimeMin)


    def setEffectiveActiveTimeMin(self, value):
        self.__mEffectiveActiveTimeMin = value

    def getEffectiveActiveTimeMin(self):
        returnVal = None
        returnVal = self.__mEffectiveActiveTimeMin
        return returnVal
    EffectiveActiveTimeMin = property(fset=setEffectiveActiveTimeMin, fget=getEffectiveActiveTimeMin)


    def setEffectiveProductionTimeMin(self, value):
        self.__mEffectiveProductionTimeMin = value

    def getEffectiveProductionTimeMin(self):
        returnVal = None
        returnVal = self.__mEffectiveProductionTimeMin
        return returnVal
    EffectiveProductionTimeMin = property(fset=setEffectiveProductionTimeMin, fget=getEffectiveProductionTimeMin)


    def setEffectiveSetupDurationMin(self, value):
        self.__mEffectiveSetupDurationMin = value

    def getEffectiveSetupDurationMin(self):
        returnVal = None
        returnVal = self.__mEffectiveSetupDurationMin
        return returnVal
    EffectiveSetupDurationMin = property(fset=setEffectiveSetupDurationMin, fget=getEffectiveSetupDurationMin)


    def setCycleTimeEfficiency(self, value):
        self.__mCycleTimeEfficiency = value

    def getCycleTimeEfficiency(self):
        returnVal = None
        returnVal = self.__mCycleTimeEfficiency
        return returnVal
    CycleTimeEfficiency = property(fset=setCycleTimeEfficiency, fget=getCycleTimeEfficiency)


    def setRejectsEfficiency(self, value):
        self.__mRejectsEfficiency = value

    def getRejectsEfficiency(self):
        returnVal = None
        returnVal = self.__mRejectsEfficiency
        return returnVal
    RejectsEfficiency = property(fset=setRejectsEfficiency, fget=getRejectsEfficiency)


    def setDownTimeEfficiency(self, value):
        self.__mDownTimeEfficiency = value

    def getDownTimeEfficiency(self):
        returnVal = None
        returnVal = self.__mDownTimeEfficiency
        return returnVal
    DownTimeEfficiency = property(fset=setDownTimeEfficiency, fget=getDownTimeEfficiency)


    def setDownTimeEfficiencyOEE(self, value):
        self.__mDownTimeEfficiencyOEE = value

    def getDownTimeEfficiencyOEE(self):
        returnVal = None
        returnVal = self.__mDownTimeEfficiencyOEE
        return returnVal
    DownTimeEfficiencyOEE = property(fset=setDownTimeEfficiencyOEE, fget=getDownTimeEfficiencyOEE)


    def setPConfigUnits(self, value):
        self.__mPConfigUnits = value

    def getPConfigUnits(self):
        returnVal = None
        if self.PConfigID == 0:
            returnVal = self.__mCavitiesActual
        else:
            returnVal = self.__mPConfigUnits
        return returnVal
    PConfigUnits = property(fset=setPConfigUnits, fget=getPConfigUnits)


    def setPConfigPC(self, value):
        self.__mPConfigPC = value

    def getPConfigPC(self):
        returnVal = None
        if self.PConfigID == 0:
            returnVal = 100
        else:
            returnVal = self.__mPConfigPC
        return returnVal
    PConfigPC = property(fset=setPConfigPC, fget=getPConfigPC)


    def setPConfigID(self, value):
        self.__mPConfigID = value

    def getPConfigID(self):
        returnVal = None
        returnVal = self.__mPConfigID
        return returnVal
    PConfigID = property(fset=setPConfigID, fget=getPConfigID)


    def setPConfigJobID(self, value):
        self.__mPConfigJobID = value

    def getPConfigJobID(self):
        returnVal = None
        returnVal = self.__mPConfigJobID
        return returnVal
    PConfigJobID = property(fset=setPConfigJobID, fget=getPConfigJobID)


    def setIsPConfigMain(self, value):
        self.__mIsPConfigMain = value

    def getIsPConfigMain(self):
        returnVal = None
        returnVal = self.__mIsPConfigMain
        return returnVal
    IsPConfigMain = property(fset=setIsPConfigMain, fget=getIsPConfigMain)


    def setPConfigIsMaterialCount(self, value):
        self.__mPConfigIsMaterialCount = value

    def getPConfigIsMaterialCount(self):
        returnVal = None
        returnVal = self.__mPConfigIsMaterialCount
        return returnVal
    PConfigIsMaterialCount = property(fset=setPConfigIsMaterialCount, fget=getPConfigIsMaterialCount)


    def setPConfigIsChannel100Count(self, value):
        self.__mPConfigIsChannel100Count = value

    def getPConfigIsChannel100Count(self):
        returnVal = None
        returnVal = self.__mPConfigIsChannel100Count
        return returnVal
    PConfigIsChannel100Count = property(fset=setPConfigIsChannel100Count, fget=getPConfigIsChannel100Count)


    def setPConfigIsSpecialMaterialCount(self, value):
        self.__mPConfigIsSpecialMaterialCount = value

    def getPConfigIsSpecialMaterialCount(self):
        returnVal = None
        returnVal = self.__mPConfigIsSpecialMaterialCount
        return returnVal
    PConfigIsSpecialMaterialCount = property(fset=setPConfigIsSpecialMaterialCount, fget=getPConfigIsSpecialMaterialCount)


    def setPConfigParentID(self, value):
        self.__mPConfigParentID = value

    def getPConfigParentID(self):
        returnVal = None
        returnVal = self.__mPConfigParentID
        return returnVal
    PConfigParentID = property(fset=setPConfigParentID, fget=getPConfigParentID)


    def setPConfigRelation(self, value):
        self.__mPConfigRelation = value

    def getPConfigRelation(self):
        returnVal = None
        returnVal = self.__mPConfigRelation
        return returnVal
    PConfigRelation = property(fset=setPConfigRelation, fget=getPConfigRelation)


    
    def setPConfigParentJob(self, value):
        self.__mPConfigParentJob = value

    def getPConfigParentJob(self):
        returnVal = None
        returnVal = self.__mPConfigParentJob
        return returnVal
    PConfigParentJob = property(fset=setPConfigParentJob, fget=getPConfigParentJob)


    def setSetupDuration(self, value):
        self.__mSetupDuration = value

    def getSetupDuration(self):
        returnVal = None
        returnVal = self.__mSetupDuration
        return returnVal
    SetupDuration = property(fset=setSetupDuration, fget=getSetupDuration)


    def setEffectiveCycleTime(self, value):
        self.__mEffectiveCycleTime = value

    def getEffectiveCycleTime(self):
        returnVal = None
        returnVal = self.__mEffectiveCycleTime
        return returnVal
    EffectiveCycleTime = property(fset=setEffectiveCycleTime, fget=getEffectiveCycleTime)


    def setEffectiveWeight(self, value):
        self.__mEffectiveWeight = value

    def getEffectiveWeight(self):
        returnVal = None
        returnVal = self.__mEffectiveWeight
        return returnVal
    EffectiveWeight = property(fset=setEffectiveWeight, fget=getEffectiveWeight)


    def setProductWeightAvg(self, value):
        self.__mProductWeightAvg = value

    def getProductWeightAvg(self):
        returnVal = None
        returnVal = self.__mProductWeightAvg
        return returnVal
    ProductWeightAvg = property(fset=setProductWeightAvg, fget=getProductWeightAvg)


    def setProductWeightDiff(self, value):
        self.__mProductWeightDiff = value

    def getProductWeightDiff(self):
        returnVal = None
        returnVal = self.__mProductWeightDiff
        return returnVal
    ProductWeightDiff = property(fset=setProductWeightDiff, fget=getProductWeightDiff)


    def setProductWeightDiffPC(self, value):
        self.__mProductWeightDiffPC = value

    def getProductWeightDiffPC(self):
        returnVal = None
        returnVal = self.__mProductWeightDiffPC
        return returnVal
    ProductWeightDiffPC = property(fset=setProductWeightDiffPC, fget=getProductWeightDiffPC)


    def setProductWeightPC(self, value):
        self.__mProductWeightPC = value

    def getProductWeightPC(self):
        returnVal = None
        returnVal = self.__mProductWeightPC
        return returnVal
    ProductWeightPC = property(fset=setProductWeightPC, fget=getProductWeightPC)


    def setProductWeightStandard(self, value):
        self.__mProductWeightStandard = value

    def getProductWeightStandard(self):
        returnVal = None
        returnVal = self.__mProductWeightStandard
        return returnVal
    ProductWeightStandard = property(fset=setProductWeightStandard, fget=getProductWeightStandard)


    def setProductWeightLast(self, value):
        self.__mProductWeightLast = value

    def getProductWeightLast(self):
        returnVal = None
        returnVal = self.__mProductWeightLast
        return returnVal
    ProductWeightLast = property(fset=setProductWeightLast, fget=getProductWeightLast)


    def setProductRecipeWeight(self, value):
        self.__mProductRecipeWeight = value

    def getProductRecipeWeight(self):
        returnVal = None
        returnVal = self.__mProductRecipeWeight
        return returnVal
    ProductRecipeWeight = property(fset=setProductRecipeWeight, fget=getProductRecipeWeight)


    def setProductStandardRecipeWeight(self, value):
        self.__mProductStandardRecipeWeight = value

    def getProductStandardRecipeWeight(self):
        returnVal = None
        returnVal = self.__mProductStandardRecipeWeight
        return returnVal
    ProductStandardRecipeWeight = property(fset=setProductStandardRecipeWeight, fget=getProductStandardRecipeWeight)


    def setCycleTimeAvg(self, value):
        self.__mCycleTimeAvg = value

    def getCycleTimeAvg(self):
        returnVal = None
        returnVal = self.__mCycleTimeAvg
        return returnVal
    CycleTimeAvg = property(fset=setCycleTimeAvg, fget=getCycleTimeAvg)


    def setCycleTimeAvgDiff(self, value):
        self.__mCycleTimeAvgDiff = value

    def getCycleTimeAvgDiff(self):
        returnVal = None
        returnVal = self.__mCycleTimeAvgDiff
        return returnVal
    CycleTimeAvgDiff = property(fset=setCycleTimeAvgDiff, fget=getCycleTimeAvgDiff)


    def setCycleTimeAvgDiffPC(self, value):
        self.__mCycleTimeAvgDiffPC = value

    def getCycleTimeAvgDiffPC(self):
        returnVal = None
        returnVal = self.__mCycleTimeAvgDiffPC
        return returnVal
    CycleTimeAvgDiffPC = property(fset=setCycleTimeAvgDiffPC, fget=getCycleTimeAvgDiffPC)


    def setCycleTimeAvgSMean(self, value):
        self.__mCycleTimeAvgSMean = value

    def getCycleTimeAvgSMean(self):
        returnVal = None
        returnVal = self.__mCycleTimeAvgSMean
        return returnVal
    CycleTimeAvgSMean = property(fset=setCycleTimeAvgSMean, fget=getCycleTimeAvgSMean)


    def setCycleTimeStandard(self, value):
        self.__mCycleTimeStandard = value

    def getCycleTimeStandard(self):
        returnVal = None
        returnVal = self.__mCycleTimeStandard
        return returnVal
    CycleTimeStandard = property(fset=setCycleTimeStandard, fget=getCycleTimeStandard)


    def setCycleTimeLast(self, value):
        self.__mCycleTimeLast = value

    def getCycleTimeLast(self):
        returnVal = None
        returnVal = self.__mCycleTimeLast
        return returnVal
    CycleTimeLast = property(fset=setCycleTimeLast, fget=getCycleTimeLast)


    def setUnitsTarget(self, value):
        self.__mUnitsTarget = value

    def getUnitsTarget(self):
        returnVal = None
        returnVal = self.__mUnitsTarget
        return returnVal
    UnitsTarget = property(fset=setUnitsTarget, fget=getUnitsTarget)


    def setUnitsProduced(self, value):
        self.__mUnitsProduced = value

    def getUnitsProduced(self):
        returnVal = None
        returnVal = self.__mUnitsProduced
        return returnVal
    UnitsProduced = property(fset=setUnitsProduced, fget=getUnitsProduced)


    def setUnitsProducedOK(self, value):
        self.__mUnitsProducedOK = value

    def getUnitsProducedOK(self):
        returnVal = None
        returnVal = self.__mUnitsProducedOK
        return returnVal
    UnitsProducedOK = property(fset=setUnitsProducedOK, fget=getUnitsProducedOK)


    def setUnitsProducedLeft(self, value):
        self.__mUnitsProducedLeft = value

    def getUnitsProducedLeft(self):
        returnVal = None
        returnVal = self.__mUnitsProducedLeft
        return returnVal
    UnitsProducedLeft = property(fset=setUnitsProducedLeft, fget=getUnitsProducedLeft)


    def setUnitsProducedPC(self, value):
        self.__mUnitsProducedPC = value

    def getUnitsProducedPC(self):
        returnVal = None
        returnVal = self.__mUnitsProducedPC
        return returnVal
    UnitsProducedPC = property(fset=setUnitsProducedPC, fget=getUnitsProducedPC)


    def setUnitsReportedOK(self, value):
        self.__mUnitsReportedOK = value

    def getUnitsReportedOK(self):
        returnVal = None
        returnVal = self.__mUnitsReportedOK
        return returnVal
    UnitsReportedOK = property(fset=setUnitsReportedOK, fget=getUnitsReportedOK)


    def setUnitsReportedOKDiff(self, value):
        self.__mUnitsReportedOKDiff = value

    def getUnitsReportedOKDiff(self):
        returnVal = None
        returnVal = self.__mUnitsReportedOKDiff
        return returnVal
    UnitsReportedOKDiff = property(fset=setUnitsReportedOKDiff, fget=getUnitsReportedOKDiff)


    def setUnitsReportedOKDiffPC(self, value):
        self.__mUnitsReportedOKDiffPC = value

    def getUnitsReportedOKDiffPC(self):
        returnVal = None
        returnVal = self.__mUnitsReportedOKDiffPC
        return returnVal
    UnitsReportedOKDiffPC = property(fset=setUnitsReportedOKDiffPC, fget=getUnitsReportedOKDiffPC)


    def setUnitsProducedOKDiff(self, value):
        self.__mUnitsProducedOKDiff = value

    def getUnitsProducedOKDiff(self):
        returnVal = None
        returnVal = self.__mUnitsProducedOKDiff
        return returnVal
    UnitsProducedOKDiff = property(fset=setUnitsProducedOKDiff, fget=getUnitsProducedOKDiff)


    def setCavitiesEfficiency(self, value):
        self.__mCavitiesEfficiency = value

    def getCavitiesEfficiency(self):
        returnVal = None
        returnVal = self.__mCavitiesEfficiency
        return returnVal
    CavitiesEfficiency = property(fset=setCavitiesEfficiency, fget=getCavitiesEfficiency)


    def setCavitiesPC(self, value):
        self.__mCavitiesPC = value

    def getCavitiesPC(self):
        returnVal = None
        returnVal = self.__mCavitiesPC
        return returnVal
    CavitiesPC = property(fset=setCavitiesPC, fget=getCavitiesPC)


    def setCavitiesStandard(self, value):
        self.__mCavitiesStandard = value

    def getCavitiesStandard(self):
        returnVal = None
        returnVal = self.__mCavitiesStandard
        return returnVal
    CavitiesStandard = property(fset=setCavitiesStandard, fget=getCavitiesStandard)


    def setCavitiesActual(self, value):
        self.__mCavitiesActual = value

    def getCavitiesActual(self):
        returnVal = None
        if self.PConfigID != 0:
            returnVal = self.PConfigUnits
        else:
            returnVal = self.__mCavitiesActual
        return returnVal
    CavitiesActual = property(fset=setCavitiesActual, fget=getCavitiesActual)


    def setEfficiencyTotal(self, value):
        self.__mEfficiencyTotal = value

    def getEfficiencyTotal(self):
        returnVal = None
        returnVal = self.__mEfficiencyTotal
        return returnVal
    EfficiencyTotal = property(fset=setEfficiencyTotal, fget=getEfficiencyTotal)


    def setPEE(self, value):
        self.__mPEE = value

    def getPEE(self):
        returnVal = None
        returnVal = self.__mPEE
        return returnVal
    PEE = property(fset=setPEE, fget=getPEE)


    def setTotalMaterialEfficiencyActual(self, value):
        self.__mTotalMaterialEfficiencyActual = value

    def getTotalMaterialEfficiencyActual(self):
        returnVal = None
        returnVal = self.__mTotalMaterialEfficiencyActual
        return returnVal
    TotalMaterialEfficiencyActual = property(fset=setTotalMaterialEfficiencyActual, fget=getTotalMaterialEfficiencyActual)


    def setTotalMaterialEfficiencyTheoretical(self, value):
        self.__mTotalMaterialEfficiencyTheoretical = value

    def getTotalMaterialEfficiencyTheoretical(self):
        returnVal = None
        returnVal = self.__mTotalMaterialEfficiencyTheoretical
        return returnVal
    TotalMaterialEfficiencyTheoretical = property(fset=setTotalMaterialEfficiencyTheoretical, fget=getTotalMaterialEfficiencyTheoretical)


    def setTotalEquipmentMaterialEfficency(self, value):
        self.__mTotalEquipmentMaterialEfficency = value

    def getTotalEquipmentMaterialEfficency(self):
        returnVal = None
        returnVal = self.__mTotalEquipmentMaterialEfficency
        return returnVal
    TotalEquipmentMaterialEfficency = property(fset=setTotalEquipmentMaterialEfficency, fget=getTotalEquipmentMaterialEfficency)


    def setOriginalJobID(self, value):
        self.__mOriginalJobID = value

    def getOriginalJobID(self):
        returnVal = None
        returnVal = self.__mOriginalJobID
        return returnVal
    OriginalJobID = property(fset=setOriginalJobID, fget=getOriginalJobID)


    def setOriginalUnitsProducedOK(self, value):
        self.__mOriginalUnitsProducedOK = value

    def getOriginalUnitsProducedOK(self):
        returnVal = None
        returnVal = self.__mOriginalUnitsProducedOK
        return returnVal
    OriginalUnitsProducedOK = property(fset=setOriginalUnitsProducedOK, fget=getOriginalUnitsProducedOK)


    def setOriginalUnitsTarget(self, value):
        self.__mOriginalUnitsTarget = value

    def getOriginalUnitsTarget(self):
        returnVal = None
        returnVal = self.__mOriginalUnitsTarget
        return returnVal
    OriginalUnitsTarget = property(fset=setOriginalUnitsTarget, fget=getOriginalUnitsTarget)


    def setInjectionsCount(self, value):
        self.__mInjectionsCount = value

    def getInjectionsCount(self):
        returnVal = None
        returnVal = self.__mInjectionsCount
        return returnVal
    InjectionsCount = property(fset=setInjectionsCount, fget=getInjectionsCount)


    def setInjectionsCountLast(self, value):
        self.__mInjectionsCountLast = value

    def getInjectionsCountLast(self):
        returnVal = None
        returnVal = self.__mInjectionsCountLast
        return returnVal
    InjectionsCountLast = property(fset=setInjectionsCountLast, fget=getInjectionsCountLast)


    def setInjectionsCountStart(self, value):
        self.__mInjectionsCountStart = value

    def getInjectionsCountStart(self):
        returnVal = None
        returnVal = self.__mInjectionsCountStart
        return returnVal
    InjectionsCountStart = property(fset=setInjectionsCountStart, fget=getInjectionsCountStart)


    def setInjectionsDiff(self, value):
        self.__mInjectionsDiff = value

    def getInjectionsDiff(self):
        returnVal = None
        returnVal = self.__mInjectionsDiff
        return returnVal
    InjectionsDiff = property(fset=setInjectionsDiff, fget=getInjectionsDiff)


    def setRejectsReported(self, value):
        self.__mRejectsReported = value

    def getRejectsReported(self):
        returnVal = None
        returnVal = self.__mRejectsReported
        return returnVal
    RejectsReported = property(fset=setRejectsReported, fget=getRejectsReported)


    def setReportedRejectsDiff(self, value):
        self.__mReportedRejectsDiff = value

    def getReportedRejectsDiff(self):
        returnVal = None
        returnVal = self.__mReportedRejectsDiff
        return returnVal
    ReportedRejectsDiff = property(fset=setReportedRejectsDiff, fget=getReportedRejectsDiff)


    def setCyclesDroped(self, value):
        self.__mCyclesDroped = value

    def getCyclesDroped(self):
        returnVal = None
        returnVal = self.__mCyclesDroped
        return returnVal
    CyclesDroped = property(fset=setCyclesDroped, fget=getCyclesDroped)


    def setCyclesNetActual(self, value):
        self.__mCyclesNetActual = value

    def getCyclesNetActual(self):
        returnVal = None
        returnVal = self.__mCyclesNetActual
        return returnVal
    CyclesNetActual = property(fset=setCyclesNetActual, fget=getCyclesNetActual)


    def setRejectsTotal(self, value):
        self.__mRejectsTotal = value

    def getRejectsTotal(self):
        returnVal = None
        returnVal = self.__mRejectsTotal
        return returnVal
    RejectsTotal = property(fset=setRejectsTotal, fget=getRejectsTotal)


    def setRejectsForEfficiency(self, value):
        self.__mRejectsForEfficiency = value

    def getRejectsForEfficiency(self):
        returnVal = None
        returnVal = self.__mRejectsForEfficiency
        return returnVal
    RejectsForEfficiency = property(fset=setRejectsForEfficiency, fget=getRejectsForEfficiency)


    def setRejectsForConsumption(self, value):
        self.__mRejectsForConsumption = value

    def getRejectsForConsumption(self):
        returnVal = None
        returnVal = self.__mRejectsForConsumption
        return returnVal
    RejectsForConsumption = property(fset=setRejectsForConsumption, fget=getRejectsForConsumption)


    def setRejectsPC(self, value):
        self.__mRejectsPC = value

    def getRejectsPC(self):
        returnVal = None
        returnVal = self.__mRejectsPC
        return returnVal
    RejectsPC = property(fset=setRejectsPC, fget=getRejectsPC)


    def setRejectsRead(self, value):
        self.__mRejectsRead = value

    def getRejectsRead(self):
        returnVal = None
        returnVal = self.__mRejectsRead
        return returnVal
    RejectsRead = property(fset=setRejectsRead, fget=getRejectsRead)


    def setTotalWasteKg(self, value):
        self.__mTotalWasteKg = value

    def getTotalWasteKg(self):
        returnVal = None
        returnVal = self.__mTotalWasteKg
        return returnVal
    TotalWasteKg = property(fset=setTotalWasteKg, fget=getTotalWasteKg)


    def setTotalCycles(self, value):
        self.__mTotalCycles = value

    def getTotalCycles(self):
        returnVal = None
        returnVal = self.__mTotalCycles
        return returnVal
    TotalCycles = property(fset=setTotalCycles, fget=getTotalCycles)


    def setMaterialTotal(self, value):
        self.__mMaterialTotal = value

    def getMaterialTotal(self):
        returnVal = None
        returnVal = self.__mMaterialTotal
        return returnVal
    MaterialTotal = property(fset=setMaterialTotal, fget=getMaterialTotal)


    def setSetupMaterialTotal(self, value):
        self.__mSetupMaterialTotal = value

    def getSetupMaterialTotal(self):
        returnVal = None
        returnVal = self.__mSetupMaterialTotal
        return returnVal
    SetupMaterialTotal = property(fset=setSetupMaterialTotal, fget=getSetupMaterialTotal)


    def setMaterialTotalMainPC(self, value):
        self.__mMaterialTotalMainPC = value

    def getMaterialTotalMainPC(self):
        returnVal = None
        returnVal = self.__mMaterialTotalMainPC
        return returnVal
    MaterialTotalMainPC = property(fset=setMaterialTotalMainPC, fget=getMaterialTotalMainPC)


    def setMaterialTotalAdditivePC(self, value):
        self.__mMaterialTotalAdditivePC = value

    def getMaterialTotalAdditivePC(self):
        returnVal = None
        returnVal = self.__mMaterialTotalAdditivePC
        return returnVal
    MaterialTotalAdditivePC = property(fset=setMaterialTotalAdditivePC, fget=getMaterialTotalAdditivePC)


    def setMainMaterialTotal(self, value):
        self.__mMainMaterialTotal = value

    def getMainMaterialTotal(self):
        returnVal = None
        returnVal = self.__mMainMaterialTotal
        return returnVal
    MainMaterialTotal = property(fset=setMainMaterialTotal, fget=getMainMaterialTotal)


    def setMainMaterialStandard(self, value):
        self.__mMainMaterialStandard = value

    def getMainMaterialStandard(self):
        returnVal = None
        returnVal = self.__mMainMaterialStandard
        return returnVal
    MainMaterialStandard = property(fset=setMainMaterialStandard, fget=getMainMaterialStandard)


    def setMainMaterialStandardPC(self, value):
        self.__mMainMaterialStandardPC = value

    def getMainMaterialStandardPC(self):
        returnVal = None
        returnVal = self.__mMainMaterialStandardPC
        return returnVal
    MainMaterialStandardPC = property(fset=setMainMaterialStandardPC, fget=getMainMaterialStandardPC)


    def setMainMaterialStandardCalcPC(self, value):
        self.__mMainMaterialStandardCalcPC = value

    def getMainMaterialStandardCalcPC(self):
        returnVal = None
        returnVal = self.__mMainMaterialStandardCalcPC
        return returnVal
    MainMaterialStandardCalcPC = property(fset=setMainMaterialStandardCalcPC, fget=getMainMaterialStandardCalcPC)


    def setMainMaterialStandardPCCalcC(self, value):
        self.__mMainMaterialStandardPCCalcC = value

    def getMainMaterialStandardPCCalcC(self):
        returnVal = None
        returnVal = self.__mMainMaterialStandardPCCalcC
        return returnVal
    MainMaterialStandardPCCalcC = property(fset=setMainMaterialStandardPCCalcC, fget=getMainMaterialStandardPCCalcC)


    def setAdditiveMaterialTotal(self, value):
        self.__mAdditiveMaterialTotal = value

    def getAdditiveMaterialTotal(self):
        returnVal = None
        returnVal = self.__mAdditiveMaterialTotal
        return returnVal
    AdditiveMaterialTotal = property(fset=setAdditiveMaterialTotal, fget=getAdditiveMaterialTotal)


    def setAdditiveMaterialStandard(self, value):
        self.__mAdditiveMaterialStandard = value

    def getAdditiveMaterialStandard(self):
        returnVal = None
        returnVal = self.__mAdditiveMaterialStandard
        return returnVal
    AdditiveMaterialStandard = property(fset=setAdditiveMaterialStandard, fget=getAdditiveMaterialStandard)


    def setAdditiveMaterialStandardPC(self, value):
        self.__mAdditiveMaterialStandardPC = value

    def getAdditiveMaterialStandardPC(self):
        returnVal = None
        returnVal = self.__mAdditiveMaterialStandardPC
        return returnVal
    AdditiveMaterialStandardPC = property(fset=setAdditiveMaterialStandardPC, fget=getAdditiveMaterialStandardPC)


    def setAdditiveMaterialStandardCalcPC(self, value):
        self.__mAdditiveMaterialStandardCalcPC = value

    def getAdditiveMaterialStandardCalcPC(self):
        returnVal = None
        returnVal = self.__mAdditiveMaterialStandardCalcPC
        return returnVal
    AdditiveMaterialStandardCalcPC = property(fset=setAdditiveMaterialStandardCalcPC, fget=getAdditiveMaterialStandardCalcPC)


    def setAdditiveMaterialStandardPCCalcC(self, value):
        self.__mAdditiveMaterialStandardPCCalcC = value

    def getAdditiveMaterialStandardPCCalcC(self):
        returnVal = None
        returnVal = self.__mAdditiveMaterialStandardPCCalcC
        return returnVal
    AdditiveMaterialStandardPCCalcC = property(fset=setAdditiveMaterialStandardPCCalcC, fget=getAdditiveMaterialStandardPCCalcC)


    def setMaterialConsumptionKgtoHour(self, value):
        self.__mMaterialConsumptionKgtoHour = value

    def getMaterialConsumptionKgtoHour(self):
        returnVal = None
        returnVal = self.__mMaterialConsumptionKgtoHour
        return returnVal
    MaterialConsumptionKgtoHour = property(fset=setMaterialConsumptionKgtoHour, fget=getMaterialConsumptionKgtoHour)


    def setCycleWeightActualAvg(self, value):
        self.__mCycleWeightActualAvg = value

    def getCycleWeightActualAvg(self):
        returnVal = None
        returnVal = self.__mCycleWeightActualAvg
        return returnVal
    CycleWeightActualAvg = property(fset=setCycleWeightActualAvg, fget=getCycleWeightActualAvg)


    def setMaterialActualIndex(self, value):
        self.__mMaterialActualIndex = value

    def getMaterialActualIndex(self):
        returnVal = None
        returnVal = self.__mMaterialActualIndex
        return returnVal
    MaterialActualIndex = property(fset=setMaterialActualIndex, fget=getMaterialActualIndex)


    def setMaterialStandardIndex(self, value):
        self.__mMaterialStandardIndex = value

    def getMaterialStandardIndex(self):
        returnVal = None
        returnVal = self.__mMaterialStandardIndex
        return returnVal
    MaterialStandardIndex = property(fset=setMaterialStandardIndex, fget=getMaterialStandardIndex)


    
    def setOpenWorkingEvent(self, value):
        self.__mOpenWorkingEvent = value

    def getOpenWorkingEvent(self):
        returnVal = None
        returnVal = self.__mOpenWorkingEvent
        return returnVal
    OpenWorkingEvent = property(fset=setOpenWorkingEvent, fget=getOpenWorkingEvent)


    
    def setOpenEvent(self, value):
        self.__mOpenEvent = value

    def getOpenEvent(self):
        returnVal = None
        returnVal = self.__mOpenEvent
        return returnVal
    OpenEvent = property(fset=setOpenEvent, fget=getOpenEvent)


    def setOpenAlarms(self, value):
        self.__mOpenAlarms = value

    def getOpenAlarms(self):
        returnVal = None
        returnVal = self.__mOpenAlarms
        return returnVal
    OpenAlarms = property(fset=setOpenAlarms, fget=getOpenAlarms)


    def setPConfigJobs(self, value):
        self.__mPConfigJobs = value

    def getPConfigJobs(self):
        returnVal = None
        returnVal = self.__mPConfigJobs
        return returnVal
    PConfigJobs = property(fset=setPConfigJobs, fget=getPConfigJobs)


    def setRecipeRefType(self, value):
        self.__mRecipeRefType = value

    def getRecipeRefType(self):
        returnVal = None
        returnVal = self.__mRecipeRefType
        return returnVal
    RecipeRefType = property(fset=setRecipeRefType, fget=getRecipeRefType)


    def setRecipeRefJob(self, value):
        self.__mRecipeRefJob = value

    def getRecipeRefJob(self):
        returnVal = None
        returnVal = self.__mRecipeRefJob
        return returnVal
    RecipeRefJob = property(fset=setRecipeRefJob, fget=getRecipeRefJob)


    def setRecipeRefStandardID(self, value):
        self.__mRecipeRefStandardID = value

    def getRecipeRefStandardID(self):
        returnVal = None
        returnVal = self.__mRecipeRefStandardID
        return returnVal
    RecipeRefStandardID = property(fset=setRecipeRefStandardID, fget=getRecipeRefStandardID)


    def setMaterialRecipeIndexJob(self, value):
        self.__mMaterialRecipeIndexJob = value

    def getMaterialRecipeIndexJob(self):
        returnVal = None
        returnVal = self.__mMaterialRecipeIndexJob
        return returnVal
    MaterialRecipeIndexJob = property(fset=setMaterialRecipeIndexJob, fget=getMaterialRecipeIndexJob)


    def setMaterialRecipeIndexProduct(self, value):
        self.__mMaterialRecipeIndexProduct = value

    def getMaterialRecipeIndexProduct(self):
        returnVal = None
        returnVal = self.__mMaterialRecipeIndexProduct
        return returnVal
    MaterialRecipeIndexProduct = property(fset=setMaterialRecipeIndexProduct, fget=getMaterialRecipeIndexProduct)


    def setControllerChannels(self, value):
        self.__mControllerChannels = value

    def getControllerChannels(self):
        returnVal = None
        returnVal = self.__mControllerChannels
        return returnVal
    ControllerChannels = property(fset=setControllerChannels, fget=getControllerChannels)


    def setMoldChangeFirstOtherMoldMachineJobOrder(self, value):
        self.__mMoldChangeFirstOtherMoldMachineJobOrder = value

    def getMoldChangeFirstOtherMoldMachineJobOrder(self):
        returnVal = None
        returnVal = self.__mMoldChangeFirstOtherMoldMachineJobOrder
        return returnVal
    MoldChangeFirstOtherMoldMachineJobOrder = property(fset=setMoldChangeFirstOtherMoldMachineJobOrder, fget=getMoldChangeFirstOtherMoldMachineJobOrder)


    def setMoldChangeTimeLeftHr(self, value):
        self.__mMoldChangeTimeLeftHr = value

    def getMoldChangeTimeLeftHr(self):
        returnVal = None
        returnVal = self.__mMoldChangeTimeLeftHr
        return returnVal
    MoldChangeTimeLeftHr = property(fset=setMoldChangeTimeLeftHr, fget=getMoldChangeTimeLeftHr)


    def setMoldChangeUnitsTarget(self, value):
        self.__mMoldChangeUnitsTarget = value

    def getMoldChangeUnitsTarget(self):
        returnVal = None
        returnVal = self.__mMoldChangeUnitsTarget
        return returnVal
    MoldChangeUnitsTarget = property(fset=setMoldChangeUnitsTarget, fget=getMoldChangeUnitsTarget)


    def setMoldChangeUnitsProducedOK(self, value):
        self.__mMoldChangeUnitsProducedOK = value

    def getMoldChangeUnitsProducedOK(self):
        returnVal = None
        returnVal = self.__mMoldChangeUnitsProducedOK
        return returnVal
    MoldChangeUnitsProducedOK = property(fset=setMoldChangeUnitsProducedOK, fget=getMoldChangeUnitsProducedOK)


    def setRefRecipeProductWeight(self, value):
        self.__mRefRecipeProductWeight = value

    def getRefRecipeProductWeight(self):
        returnVal = None
        returnVal = self.__mRefRecipeProductWeight
        return returnVal
    RefRecipeProductWeight = property(fset=setRefRecipeProductWeight, fget=getRefRecipeProductWeight)


    def setRefRecipeUnitWeight(self, value):
        self.__mRefRecipeUnitWeight = value

    def getRefRecipeUnitWeight(self):
        returnVal = None
        returnVal = self.__mRefRecipeUnitWeight
        return returnVal
    RefRecipeUnitWeight = property(fset=setRefRecipeUnitWeight, fget=getRefRecipeUnitWeight)


    def setValidationLog(self, value):
        self.__mValidationLog = value

    def getValidationLog(self):
        returnVal = None
        returnVal = self.__mValidationLog
        return returnVal
    ValidationLog = property(fset=setValidationLog, fget=getValidationLog)


    def setNextJobMaterialFlowStart(self, value):
        self.__mNextJobMaterialFlowStart = value

    def getNextJobMaterialFlowStart(self):
        returnVal = None
        returnVal = self.__mNextJobMaterialFlowStart
        return returnVal
    NextJobMaterialFlowStart = property(fset=setNextJobMaterialFlowStart, fget=getNextJobMaterialFlowStart)

