from Shift import Shift

import MdlADOFunctions
import MdlGlobal
import MdlConnection
import MdlServer
import MdlUtilsH

class Josh:
    __mID = 0
    __mJob = None
    __mShift = None
    __mShiftID = 0
    __mShiftDefID = 0
    __mShiftManagerID = 0
    __mStartTime = None
    __mEndTime = None
    __mDurationMin = 0.0
    __mDepartment = None
    __mControllerID = 0
    __mUnitsTargetJob = 0.0
    __mJobOrderNum = 0
    __mMachine = None
    __mMachineType = None
    __mProduct = None
    __mMold = None
    __mUnitsProducedJob = 0.0
    __mUnitsProducedOK = 0.0
    __mUnitsProducedPCJob = 0.0
    __mJoshStartUnits = 0.0
    __mTotalUnitsJosh = 0.0
    __mInjectionsCount = 0.0
    __mInjectionsCountLast = 0.0
    __mInjectionsCountDiff = 0.0
    __mInjectionsCountStart = 0.0
    __mDownTimeMin = 0
    __mDownTimePC = 0.0
    __mDownTimeEfficiency = 0.0
    __mDownTimeEfficiencyOEE = 0.0
    __mCycleTimeLast = 0.0
    __mCycleTimeAvg = 0.0
    __mCycleTimeStandard = 0.0
    __mCycleTimeAvgDiff = 0.0
    __mCycleTimeAvgDiffPC = 0.0
    __mCycleTimeEfficiency = 0.0
    __mRejectsTotal = 0.0
    __mRejectsPC = 0.0
    __mRejectsEfficiency = 0.0
    __mCavitiesStandard = 0.0
    __mCavitiesActual = 0.0
    __mCavitiesPC = 0.0
    __mEfficiencyTotal = 0.0
    __mPEE = 0.0
    __mCavitiesEfficiency = 0.0
    __mProductWeightLast = 0.0
    __mProductWeightAvg = 0.0
    __mProductWeightDiff = 0.0
    __mProductWeightDiffPC = 0.0
    __mProductWeightPC = 0.0
    __mProductWeightStandard = 0.0
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
    __mStatus = 0
    __mWorkerID = ''
    __mInActiveTimeMin = 0
    __mInActiveTimePC = 0.0
    __mActiveTimeMin = 0
    __mActiveTimePC = 0.0
    __mProductionTimeMin = 0
    __mProductionTimePC = 0.0
    __mProductionUsabilityPC = 0.0
    __mSetupDuration = 0.0
    __mEffectiveCycleTime = 0.0
    __mEffectiveWeight = 0.0
    __mMaterialRecipeIndexProduct = 0.0
    __mMaterialRecipeIndexJob = 0.0
    __mMaterialActualIndex = 0.0
    __mMaterialStandardIndex = 0.0
    __mTotalMaterialEfficiencyActual = 0.0
    __mTotalMaterialEfficiencyTheoretical = 0.0
    __mTotalEquipmentMaterialEfficency = 0.0
    __mMaterialConsumptionKgtoHour = 0.0
    __mCycleWeightActualAvg = 0.0
    __mCyclesDroped = 0.0
    __mCyclesNetActual = 0.0
    __mEffectiveDurationMin = 0.0
    __mEffectiveDownTimeMin = 0.0
    __mEffectiveInActiveTimeMin = 0.0
    __mEffectiveActiveTimeMin = 0.0
    __mEffectiveProductionTimeMin = 0.0
    __mEffectiveSetupDurationMin = 0.0
    __mCycleTimeAvgSMean = 0.0
    __mProductRecipeWeight = 0.0
    __mTotalWasteKg = 0.0
    __mRejectsRead = 0.0
    __mRejectsReported = 0.0
    __mRejectsForConsumption = 0.0
    __mRejectsForEfficiency = 0.0
    __mReportedRejectsDiff = 0.0
    __mUnitsReportedOK = 0.0
    __mUnitsReportedOKDiff = 0.0
    __mUnitsReportedOKDiffPC = 0.0
    __mOrderID = 0
    __mSetUpEndInjectionsCount = 0.0
    __mValidationLog = ''
    __mSetUpProductionTimeMin = 0.0
    __mSetUpDownTimeMin = 0.0
    __mUnitsProducedTheoretically = 0.0
    __mUnitsProducedTheoreticallyPC = 0.0
    __mRejectsTotalLine = 0.0
    __mRejectsEfficiencyLine = 0.0
    __mQuantityAdjustmentUnits = 0.0
    __mEngineTimeMin = 0.0

    
    def Init(self, pJob, pJoshID):
        strSQL = ''
        RstCursor = None
        tShift = None
        
        try:
            strSQL = 'SELECT * FROM TblJosh Where ID = ' + str(pJoshID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.ID = pJoshID
                self.Job = pJob
                self.Status = MdlADOFunctions.fGetRstValLong(RstData.Status)
                if MdlADOFunctions.fGetRstValLong(RstData.ShiftID) == self.Job.Machine.Server.CurrentShiftID:
                    if not self.Job.Machine.Server.CurrentShift is None:
                        self.Shift = self.Job.Machine.Server.CurrentShift
                    else:
                        tShift = Shift()
                        tShift.Init(MdlADOFunctions.fGetRstValLong(RstData.ShiftID))
                        self.Shift = tShift
                else:
                    tShift = Shift()
                    tShift.Init(MdlADOFunctions.fGetRstValLong(RstData.ShiftID))
                    self.Shift = tShift
                self.ShiftID = MdlADOFunctions.fGetRstValLong(RstData.ShiftID)
                self.ShiftDefID = MdlADOFunctions.fGetRstValLong(RstData.ShiftDefID)
                self.ShiftManagerID = MdlADOFunctions.fGetRstValLong(RstData.ShiftManagerID)
                self.StartTime = RstData.StartTime
                if MdlADOFunctions.fGetRstValString(RstData.EndTime) != '':
                    self.EndTime = RstData.EndTime
                self.DurationMin = MdlADOFunctions.fGetRstValLong(RstData.DurationMin)
                self.Department = MdlServer.GetOrCreateDepartment(self.Job.Machine.Server, MdlADOFunctions.fGetRstValLong(RstData.Department))
                self.ControllerID = MdlADOFunctions.fGetRstValLong(RstData.ControllerID)
                self.UnitsTargetJob = self.Job.UnitsTarget
                self.Machine = self.Job.Machine
                self.MachineType = MdlServer.GetOrCreateMachineType(self.Machine.Server, MdlADOFunctions.fGetRstValLong(RstData.MachineType))
                self.Product = MdlServer.GetOrCreateProduct(self.Machine.Server, MdlADOFunctions.fGetRstValLong(RstData.ProductID))
                self.Mold = MdlServer.GetOrCreateMold(self.Machine.Server, MdlADOFunctions.fGetRstValLong(RstData.MoldID))
                
                self.GetUnitsInCycle(RstData)
                if RstData.UnitsProducedJob is None:
                    self.UnitsProducedJob = self.Job.UnitsProduced
                else:
                    self.UnitsProducedJob = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedJob)
                self.UnitsProducedOK = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedOK)
                if RstData.UnitsProducedPCJob is None:
                    self.UnitsProducedPCJob = self.Job.UnitsProducedPC
                else:
                    self.UnitsProducedPCJob = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedPCJob)
                self.JoshStartUnits = MdlADOFunctions.fGetRstValDouble(RstData.JoshStartUnits)
                self.TotalUnitsJosh = MdlADOFunctions.fGetRstValDouble(RstData.TotalUnitsJosh)
                self.InjectionsCount = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCount)
                self.InjectionsCountLast = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCountLast)
                self.InjectionsCountStart = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCountStart)
                self.DownTimeMin = MdlADOFunctions.fGetRstValLong(RstData.DownTimeMin)
                self.SetUpDownTimeMin = MdlADOFunctions.fGetRstValLong(RstData.SetUpDownTimeMin)
                self.OrderID = MdlADOFunctions.fGetRstValLong(RstData.OrderID)
                self.CycleTimeStandard = MdlADOFunctions.fGetRstValDouble(RstData.CycleTimeStandard)
                self.UnitsReportedOK = MdlADOFunctions.fGetRstValDouble(RstData.UnitsReportedOK)
                
                self.MaterialRecipeIndexJob = MdlADOFunctions.fGetRstValDouble(RstData.MaterialRecipeIndexJob)
                self.MaterialRecipeIndexProduct = MdlADOFunctions.fGetRstValDouble(RstData.MaterialRecipeIndexProduct)
                self.SetUpEndInjectionsCount = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndInjectionsCount)
                
                self.UnitsProducedTheoretically = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedTheoretically)
                self.UnitsProducedTheoreticallyPC = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedTheoreticallyPC)
                self.QuantityAdjustmentUnits = MdlADOFunctions.fGetRstValDouble(RstData.QuantityAdjustmentUnits)
                
                self.WorkerID = MdlADOFunctions.fGetRstValString(RstData.WorkerID)
                if self.Status != 10:
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
                    self.SetupDuration = MdlADOFunctions.fGetRstValDouble(RstData.SetupDuration)
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
                    self.UnitsProducedPCJob = MdlADOFunctions.fGetRstValDouble(RstData.UnitsProducedPCJob)
                    
                    self.ProductWeightStandard = MdlADOFunctions.fGetRstValDouble(RstData.ProductWeightStandard)
                    self.ProductWeightAvg = MdlADOFunctions.fGetRstValDouble(RstData.ProductWeightAvg)
                    self.ProductWeightLast = MdlADOFunctions.fGetRstValDouble(RstData.ProductWeightLast)
                    self.ProductRecipeWeight = MdlADOFunctions.fGetRstValDouble(RstData.ProductRecipeWeight)
                
                self.ValidationLog = MdlADOFunctions.fGetRstValString(RstData.ValidationLog)
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.Init:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + str(self.Job.ID))
            
        Rst = None
        tShift = None

    def CheckFilters(self):
        returnVal = False

        try:
            if not self.Machine.IgnoreCycleTimeFilter:
                if ( self.Machine.CycleTime / self.CycleTimeStandard )  < self.Machine.CycleFilterLValue or  ( self.Machine.CycleTime / self.CycleTimeStandard )  > self.Machine.CycleFilterHValue:
                    self.CyclesDroped = self.CyclesDroped + self.InjectionsCountDiff
                    returnVal = False
                else:
                    returnVal = True
            else:
                returnVal = True
            self.CyclesNetActual = ( self.InjectionsCount - self.InjectionsCountStart )  - self.CyclesDroped

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CheckFilters:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            
        return returnVal

    def Update(self):
        strSQL = ''
        strTitle = ''

        try:
            strTitle = 'UPDATE TblJosh'
            strSQL = strSQL + ' SET'
            
            strSQL = strSQL + ' InjectionsCount = ' + self.InjectionsCount
            strSQL = strSQL + ' ,InjectionsCountLast = ' + self.InjectionsCountLast
            strSQL = strSQL + ' ,InjectionsCountDiff = ' + self.InjectionsCountDiff
            strSQL = strSQL + ' ,CyclesDroped = ' + self.CyclesDroped
            strSQL = strSQL + ' ,CyclesNetActual = ' + self.CyclesNetActual
            strSQL = strSQL + ' ,TotalUnitsJosh = ' + self.TotalUnitsJosh
            strSQL = strSQL + ' ,UnitsProducedOK = ' + self.UnitsProducedOK
            strSQL = strSQL + ' ,UnitsProducedJob = ' + self.UnitsProducedJob
            strSQL = strSQL + ' ,UnitsProducedPCJob = ' + self.UnitsProducedPCJob
            strSQL = strSQL + ' ,UnitsTargetJob = ' + self.Job.UnitsTarget
            strSQL = strSQL + ' ,UnitsReportedOK = ' + self.UnitsReportedOK
            strSQL = strSQL + ' ,UnitsReportedOKDiff = ' + self.UnitsReportedOKDiff
            strSQL = strSQL + ' ,UnitsReportedOKDiffPC = ' + self.UnitsReportedOKDiffPC
            strSQL = strSQL + ' ,UnitsProducedTheoretically = ' + self.UnitsProducedTheoretically
            strSQL = strSQL + ' ,UnitsProducedTheoreticallyPC = ' + self.UnitsProducedTheoreticallyPC
            strSQL = strSQL + ' ,QuantityAdjustmentUnits = ' + self.QuantityAdjustmentUnits
            strSQL = strSQL + ' ,CavitiesStandard = ' + self.CavitiesStandard
            strSQL = strSQL + ' ,CavitiesActual = ' + self.CavitiesActual
            strSQL = strSQL + ' ,CavitiesPC = ' + self.CavitiesPC
            
            strSQL = strSQL + ' ,CycleTimeStandard = ' + self.CycleTimeStandard
            strSQL = strSQL + ' ,CycleTimeAvg = ' + self.CycleTimeAvg
            strSQL = strSQL + ' ,CycleTimeAvgSMean = ' + self.CycleTimeAvgSMean
            strSQL = strSQL + ' ,CycleTimeLast = ' + self.CycleTimeLast
            strSQL = strSQL + ' ,CycleTimeAvgDiff = ' + self.CycleTimeAvgDiff
            strSQL = strSQL + ' ,CycleTimeAvgDiffPC = ' + self.CycleTimeAvgDiffPC
            
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
            
            strSQL = strSQL + ' ,EffectiveActiveTimeMin = ' + self.EffectiveActiveTimeMin
            strSQL = strSQL + ' ,EffectiveCycleTime = ' + self.EffectiveCycleTime
            strSQL = strSQL + ' ,EffectiveDownTimeMin = ' + self.EffectiveDownTimeMin
            strSQL = strSQL + ' ,EffectiveDurationMin = ' + self.EffectiveDurationMin
            strSQL = strSQL + ' ,EffectiveInActiveTimeMin = ' + self.EffectiveInActiveTimeMin
            strSQL = strSQL + ' ,EffectiveProductionTimeMin = ' + self.EffectiveProductionTimeMin
            strSQL = strSQL + ' ,EffectiveSetupDurationMin = ' + self.EffectiveSetupDurationMin
            strSQL = strSQL + ' ,EffectiveWeight = ' + self.EffectiveWeight
            
            if IsDoubleNull(self.CycleTimeEfficiency) or IsDoubleNull(self.RejectsEfficiency) or IsDoubleNull(self.CavitiesEfficiency) or IsDoubleNull(self.DownTimeEfficiency) or IsDoubleNull(self.DownTimeEfficiencyOEE):
                strSQL = strSQL + ' ,EfficiencyTotal = NULL'
                strSQL = strSQL + ' ,PEE = NULL'
            else:
                strSQL = strSQL + ' ,EfficiencyTotal = ' + IIf(round(self.EfficiencyTotal, 5) == - 999999999, 'NULL', round(self.EfficiencyTotal, 5))
                strSQL = strSQL + ' ,PEE = ' + IIf(round(self.PEE, 5) == - 999999999, 'NULL', round(self.PEE, 5))
            strSQL = strSQL + ' ,DownTimeEfficiency = ' + IIf(self.DownTimeEfficiency == - 999999999, 'NULL', self.DownTimeEfficiency)
            strSQL = strSQL + ' ,DownTimeEfficiencyOEE = ' + IIf(self.DownTimeEfficiencyOEE == - 999999999, 'NULL', self.DownTimeEfficiencyOEE)
            strSQL = strSQL + ' ,RejectsEfficiency = ' + IIf(self.RejectsEfficiency == - 999999999, 'NULL', self.RejectsEfficiency)
            strSQL = strSQL + ' ,CycleTimeEfficiency = ' + IIf(self.CycleTimeEfficiency == - 999999999, 'NULL', self.CycleTimeEfficiency)
            strSQL = strSQL + ' ,TotalMaterialEfficiencyTheoretical = ' + self.TotalMaterialEfficiencyTheoretical
            strSQL = strSQL + ' ,TotalMaterialEfficiencyActual = ' + self.TotalMaterialEfficiencyActual
            strSQL = strSQL + ' ,TotalEquipmentMaterialEfficency = ' + self.TotalEquipmentMaterialEfficency
            strSQL = strSQL + ' ,CavitiesEfficiency = ' + IIf(self.CavitiesEfficiency == - 999999999, 'NULL', self.CavitiesEfficiency)
            
            strSQL = strSQL + ' ,RejectsTotal = ' + self.RejectsTotal
            strSQL = strSQL + ' ,RejectsRead = ' + self.RejectsRead
            strSQL = strSQL + ' ,RejectsReported = ' + self.RejectsReported
            strSQL = strSQL + ' ,ReportedRejectsDiff = ' + self.ReportedRejectsDiff
            strSQL = strSQL + ' ,RejectsPC = ' + self.RejectsPC
            strSQL = strSQL + ' ,TotalWasteKg = ' + self.TotalWasteKg
            strSQL = strSQL + ' ,EngineTimeMin = ' + self.EngineTimeMin
            
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
            strSQL = strSQL + ' ,MaterialActualIndex = ' + self.MaterialActualIndex
            strSQL = strSQL + ' ,MaterialStandardIndex = ' + self.MaterialStandardIndex
            strSQL = strSQL + ' ,MaterialRecipeIndexProduct = ' + self.MaterialRecipeIndexProduct
            strSQL = strSQL + ' ,MaterialRecipeIndexJob = ' + self.MaterialRecipeIndexJob
            strSQL = strSQL + ' ,Status = ' + self.Status
            strSQL = strSQL + ' ,ProductWeightLast = ' + self.Job.ProductWeightLast
            strSQL = strSQL + ' ,ProductWeightAvg = ' + self.Job.ProductWeightAvg
            strSQL = strSQL + ' ,ProductWeightStandard = ' + self.Job.ProductWeightStandard
            strSQL = strSQL + ' ,ProductWeightDiff = ' + self.Job.ProductWeightDiff
            strSQL = strSQL + ' ,ProductWeightDiffPC = ' + self.Job.ProductWeightDiffPC
            strSQL = strSQL + ' ,ProductWeightPC = ' + self.Job.ProductWeightPC
            strSQL = strSQL + ' ,SetupDuration = ' + self.SetupDuration
            strSQL = strSQL + ' ,ValidationLog = \'' + self.ValidationLog + '\''
            strSQL = strSQL + ' ,SetUpEndInjectionsCount = ' + self.SetUpEndInjectionsCount
            if IsDate(self.EndTime) and CStr(self.EndTime) != '00:00:00':
                strSQL = strSQL + ' ,EndTime = \'' + ShortDate(self.EndTime, True, True, True) + '\''
            strSQL = strSQL + ' WHERE ID = ' + self.ID
            CN.Execute(strTitle + strSQL)
            if self.Status == 10:
                strTitle = 'UPDATE TblJoshCurrent'
                CN.Execute(strTitle + strSQL)

        except BaseException as error:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.Update:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            Err.Clear()
            
        strTitle = vbNullString
        strSQL = vbNullString

    def DetailsCalc(self, pCalcTimes, pCalcMaterial):
        try:        
            if self.Status == 10 and self.Machine.IsOffline == False:
                
                self.InjectionsCountDiff = self.Job.InjectionsDiff
                self.InjectionsCountLast = self.InjectionsCount
                self.InjectionsCount = self.InjectionsCount + self.InjectionsCountDiff
                self.GetCycleTime
            elif self.Machine.IsOffline == True:
                self.GetCycleTime
                self.GetParametersForOfflineJob
            if ( self.Machine.CycleTimeFilter == False )  or  ( self.Status != 10 ) :
                self.CalcRejects
                self.CalcUnits(self.InjectionsCountDiff)
                self.CalcUnitsReportedOK
                self.CyclesNetActual = self.InjectionsCount - self.CyclesDroped
            elif self.Machine.CycleTimeFilter == True:
                if self.Machine.IgnoreCycleTimeFilter == True:
                    self.CalcRejects
                    self.CalcUnits(self.InjectionsCountDiff)
                    self.CalcUnitsReportedOK
                    self.CyclesNetActual = self.InjectionsCount - self.CyclesDroped
                else:
                    if self.CheckFilters == True:
                        self.CalcRejects
                        self.CalcUnits(self.InjectionsCountDiff)
                        self.CalcUnitsReportedOK
            if pCalcTimes == True:
                self.CalcTimes
                self.CalcEffectiveData
                self.CalcCycleTimeParams
            if pCalcMaterial == True:
                self.MaterialCalc
            if pCalcTimes == True:
                self.CalcEfficiencies
            self.Update

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.DetailsCalc:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + IIf(not self.Job is None, self.Job.ID, ''))

    def GetCycleTime(self):
        tParam = ControlParam()

        try:
            if self.Status == 10:
                if self.Machine.GetParam('CycleTime', tParam) == True:
                    self.CycleTimeStandard = tParam.Mean
                    if self.Machine.CalcCycleTime == True:
                        self.CycleTimeLast = MdlADOFunctions.fGetRstValDouble(self.Machine.CycleTime)
                    else:
                        self.CycleTimeLast = MdlADOFunctions.fGetRstValDouble(tParam.LastValue)
                    if tParam.IsSPCValue == True:
                        self.CycleTimeAvgSMean = round(MdlADOFunctions.fGetRstValDouble(tParam.SMean), 5)
        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.GetCycleTime:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
        tParam = None

    def EndSetUp(self):
        try:
            self.SetupDuration = DateDiff('n', self.StartTime, self.Job.SetUpEnd)
        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.EndSetUp:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)

    def MaterialCalc(self):
        returnVal = None
        tVariant = Variant()
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

        try:
            for tVariant in self.Job.ControllerChannels:
                tChannel = tVariant
                tChannel.Calc(MaterialCalcObjectType.FromJosh, self.Job, self)
                if tChannel.ChannelNum != 100:
                    tMaterialTotal = tMaterialTotal + tChannel.GetTotalWeight(MaterialCalcObjectType.FromJosh)
                    tMaterialActualIndex = tMaterialActualIndex + tChannel.GetMaterialActualIndex(MaterialCalcObjectType.FromJosh)
                    tMaterialStandardIndex = tMaterialStandardIndex + tChannel.GetMaterialStandardIndex(MaterialCalcObjectType.FromJosh)
                    tMaterialTotalStandard = tMaterialTotalStandard + tChannel.GetTotalWeightStandard(MaterialCalcObjectType.FromJosh)
                    
                    tMainMaterialTotal = tMainMaterialTotal + tChannel.GetRawMaterialTotalWeight(MaterialCalcObjectType.FromJosh)
                    tMainMaterialStandard = tMainMaterialStandard + tChannel.GetRawMaterialStandardWeight(MaterialCalcObjectType.FromJosh)
                    tMaterialTotalMainPC = tMaterialTotalMainPC + tChannel.GetRawMaterialPCTarget
                    tMainMaterialStandardPC = tMainMaterialStandardPC + tChannel.GetRawMaterialPCTarget
                    
                    tMaterialTotalAdditivePC = tMaterialTotalAdditivePC + tChannel.GetAdditiveMaterialPCTarget
                    tAdditiveMaterialStandardPC = tAdditiveMaterialStandardPC + tChannel.GetAdditiveMaterialPCTarget
                    tAdditiveMaterialTotal = tAdditiveMaterialTotal + tChannel.GetAdditiveMaterialTotalWeight(MaterialCalcObjectType.FromJosh)
                    tAdditiveMaterialStandard = tAdditiveMaterialStandard + tChannel.GetAdditiveMaterialStandardWeight(MaterialCalcObjectType.FromJosh)
        
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
            self.MaterialActualIndex = tMaterialActualIndex
            self.MaterialStandardIndex = tMaterialStandardIndex
        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.MaterialCalc:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)

        tChannel = None
        return returnVal

    def CalcEffectiveData(self):
        try:
            self.EffectiveDurationMin = self.DurationMin * self.Job.PConfigPC / 100
            self.EffectiveDownTimeMin = self.DownTimeMin * self.Job.PConfigPC / 100
            self.EffectiveInActiveTimeMin = self.ActiveTimeMin * self.Job.PConfigPC / 100
            self.EffectiveActiveTimeMin = self.ActiveTimeMin * self.Job.PConfigPC / 100
            self.EffectiveProductionTimeMin = self.ProductionTimeMin * self.Job.PConfigPC / 100
            self.EffectiveSetupDurationMin = self.SetupDuration * self.Job.PConfigPC / 100
            if self.TotalUnitsJosh != 0:
                self.EffectiveCycleTime = self.EffectiveProductionTimeMin / self.TotalUnitsJosh
            else:
                self.EffectiveCycleTime = self.CycleTimeStandard
            self.EffectiveWeight = self.ProductWeightAvg / self.Job.PConfigUnits

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcEffectiveData:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            Err.Clear()

    def CalcRejects(self):
        strSQL = ''
        Rst = None

        try:
            strSQL = 'SELECT RejectsTotal,RejectsReported,TotalWasteKg,RejectsForEfficiency,RejectsForConsumption,QuantityAdjustmentUnits FROM ViewRTJoshRejects WHERE JobID = ' + self.Job.ID + ' AND ShiftID = ' + self.Shift.ID
            Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            Rst.ActiveConnection = None
            if RstData:
                self.RejectsTotal = MdlADOFunctions.fGetRstValDouble(RstData.RejectsTotal)
                self.RejectsReported = MdlADOFunctions.fGetRstValDouble(RstData.RejectsReported)
                self.TotalWasteKg = MdlADOFunctions.fGetRstValDouble(RstData.TotalWasteKg)
                self.RejectsForEfficiency = MdlADOFunctions.fGetRstValDouble(RstData.RejectsForEfficiency)
                self.RejectsForConsumption = MdlADOFunctions.fGetRstValDouble(RstData.RejectsForConsumption)
                self.QuantityAdjustmentUnits = MdlADOFunctions.fGetRstValDouble(RstData.QuantityAdjustmentUnits)
            RstCursor.close()
            self.ReportedRejectsDiff = self.RejectsRead - self.RejectsTotal
            if self.ReportedRejectsDiff < 0:
                self.ReportedRejectsDiff = 0

        except BaseException as error:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.CalcRejects:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            Err.Clear()
        Rst = None

    def CalcUnits(self, pInjectionsDiff):
        MachinePEETarget = 0.0
        tSetupDuration = 0.0

        try:
            if self.Machine.IsOffline == False:
                self.TotalUnitsJosh = self.TotalUnitsJosh +  ( pInjectionsDiff * self.CavitiesActual )
            
            self.UnitsProducedOK = self.TotalUnitsJosh - self.RejectsTotal + self.QuantityAdjustmentUnits
            if self.Status == 10:
                self.UnitsProducedJob = self.Job.UnitsProduced
                self.UnitsProducedPCJob = self.Job.UnitsProducedPC
            if self.TotalUnitsJosh != 0:
                self.RejectsPC = round(self.RejectsTotal / self.TotalUnitsJosh * 100, 5)
            else:
                self.RejectsPC = 0
            
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
                if self.Job.CycleTimeStandard == 0 or self.CavitiesActual == 0:
                    self.UnitsProducedTheoretically = 0
                else:
                    self.UnitsProducedTheoretically = round(( ( self.ActiveTimeMin - tSetupDuration )  /  ( ( self.Job.CycleTimeStandard / 60 )  / self.CavitiesActual ) )  * MachinePEETarget, 2)
                if self.UnitsProducedTheoretically != 0:
                    self.UnitsProducedTheoreticallyPC = round(self.UnitsProducedOK / self.UnitsProducedTheoretically * 100, 5)
                else:
                    self.UnitsProducedTheoreticallyPC = 0
            
            if self.Machine.LineID > 0:
                tMachine = self.Machine.Server.Machines.Item(CStr(self.Machine.LineFirstMachineID))
                FirstUnitsProduced = tMachine.ActiveJosh.TotalUnitsJosh
                tMachine = self.Machine.Server.Machines.Item(CStr(self.Machine.LineLastMachineID))
                LastUnitsProducedOK = tMachine.ActiveJosh.UnitsProducedOK

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcUnits:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            

    def __CalcTimesFromDB(self):
        strSQL = ''
        Rst = None

        try:
            strSQL = 'SELECT DownTimeMin,InActiveTimeMin FROM ViewRTJoshEvents WHERE JobID = ' + self.Job.ID + ' AND ShiftID = ' + self.Shift.ID
            Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            Rst.ActiveConnection = None
            if RstData:
                self.DownTimeMin = MdlADOFunctions.fGetRstValLong(RstData.DownTimeMin)
                self.InActiveTimeMin = MdlADOFunctions.fGetRstValLong(RstData.InActiveTimeMin)
            RstCursor.close()

        except BaseException as error:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.CalcTimesFromDB:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            Err.Clear()
        Rst = None

    def CalcTimes(self):
        try:
            if self.Status == 10 and self.Job.Status == 10:
                
                self.DurationMin = MdlADOFunctions.fGetRstValLong(round(( DateDiff('s', self.StartTime, NowGMT()) )  / 60, 5))
            self.CalcTimesFromDB
            self.ActiveTimeMin = self.DurationMin - self.InActiveTimeMin
            self.ProductionTimeMin = self.ActiveTimeMin - self.DownTimeMin
            
            
            if self.Status == 10:
                if not self.Job.OpenEvent is None:
                    if self.Job.OpenEvent.ID > 0:
                        
                        self.ProductionTimeMin = self.ProductionTimeMin - MdlADOFunctions.fGetRstValLong(round(( DateDiff('s', self.Job.OpenEvent.EventTime, NowGMT()) )  / 60, 5))
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
                
                self.SetUpDownTimeMin = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('DownTimeMin', 'ViewRTJoshSetupEvents', 'JobID = ' + self.Job.ID + ' AND ShiftID = ' + self.Shift.ID, 'CN'))
            self.CalcEngineTimesFromDB
        except BaseException as error:
            if not self.Job is None:
                MdlGlobal.RecordError(type(self).__name__ + '.DetailsCalc:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Machine.ActiveJobID)
            else:
                MdlGlobal.RecordError(type(self).__name__ + '.DetailsCalc:', str(0), error.args[0], 'JoshID: ' + self.ID)
            Err.Clear()

    def CalcEfficiencies(self):
        try:        
            if ( self.Machine.ProductionModeCalcEfficiencies and self.Machine.ProductionModeID > 1 ) or  ( self.Machine.ProductionModeID == 1 and  ( ( self.Machine.ProductionModeCalcEfficiencies and self.Job.JobDef == 0 )  or  ( self.Job.JobDef > 0 and self.Job.JobDefCalcEfficiencies ) ) ):
                if self.CycleTimeAvg != 0:
                    self.CycleTimeEfficiency = round(self.CycleTimeStandard / self.CycleTimeAvg, 5)
                else:
                    self.CycleTimeEfficiency = 0
            else:
                self.CycleTimeEfficiency = 1
            
            if ( self.Machine.ProductionModeCalcEfficiencies and self.Machine.ProductionModeID > 1 ) or ( self.Machine.ProductionModeID == 1 and  ( ( self.Machine.ProductionModeCalcEfficiencies and self.Job.JobDef == 0 )  or ( self.Job.JobDef > 0 and self.Job.JobDefCalcEfficiencies ) ) ):
                if self.TotalUnitsJosh != 0:
                    self.RejectsEfficiency = round(( self.TotalUnitsJosh - self.RejectsForEfficiency )  / self.TotalUnitsJosh, 5)
                else:
                    self.RejectsEfficiency = 1
            else:
                self.RejectsEfficiency = 1
            
            if ( self.Machine.ProductionModeCalcEfficiencies and self.Machine.ProductionModeID > 1 ) or ( self.Machine.ProductionModeID == 1 and  ( ( self.Machine.ProductionModeCalcEfficiencies and self.Job.JobDef == 0 )  or ( self.Job.JobDef > 0 and self.Job.JobDefCalcEfficiencies ) ) ):
                if self.Job.PConfigID == 0:
                    self.CavitiesPC = round(( self.CavitiesActual / self.CavitiesStandard )  * 100, 5)
                else:
                    self.CavitiesPC = 100
            else:
                self.CavitiesPC = 100
                        
            if self.ActiveTimeMin != 0:
                self.DownTimeEfficiency = round(( self.ProductionTimeMin / self.ActiveTimeMin ), 5)
            else:
                self.DownTimeEfficiency = 0
            
            if self.DurationMin != 0:
                self.DownTimeEfficiencyOEE = round(( self.ProductionTimeMin / self.DurationMin ), 5)
            else:
                self.DownTimeEfficiencyOEE = 0
            self.CavitiesEfficiency = round(self.CavitiesPC / 100, 5)
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
                self.TotalMaterialEfficiencyTheoretical = round(( self.MaterialRecipeIndexProduct * self.CyclesNetActual )  /  ( self.MaterialRecipeIndexJob * self.CyclesNetActual ), 10)
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
            
            self.UpdateEfficienciesTarget
        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcEfficiencies:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            Err.Clear()

    def EndJosh(self):
        strSQL = ''
        tVariant = Variant()
        tChannel = Channel()

        try:
            self.EndTime = NowGMT()
            self.DurationMin = DateDiff('n', self.StartTime, self.EndTime)
            if self.Machine.NewJob:
                self.SetupDuration = self.EffectiveDurationMin
            self.Status = 20
            
            for tVariant in self.Job.ControllerChannels:
                tChannel = tVariant
                tChannel.ValidateAmount(self.DurationMin, FromJosh)
            self.DetailsCalc(True, False)
            
            self.RunValidations(EndOfJosh)
            self.Update
            
            strSQL = 'UPDATE TblJoshMaterial'
            strSQL = strSQL + ' SET JoshEnd = \'' + ShortDate(NowGMT(), True, True, True) + '\''
            strSQL = strSQL + ' WHERE JoshID = ' + self.ID
            CN.Execute(strSQL)
            
            strSQL = 'DELETE TblJoshCurrent Where ID = ' + self.ID
            CN.Execute(strSQL)
            strSQL = 'DELETE TblJoshCurrentMaterial Where JoshID = ' + self.ID
            CN.Execute(strSQL)
        except BaseException as error:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.EndJosh:', str(0), error.args[0], 'JoshID: ' + self.ID)
            Err.Clear()

    def CalcCycleTimeParams(self):
        try:
            if self.Job.SetUpEnd != 0:
                if self.Machine.MonitorSetupWorkingTime or not self.Machine.AddRejectsOnSetupEnd:
                    if ( self.InjectionsCount )  > 0:
                        self.CycleTimeAvg = round(self.ProductionTimeMin /  ( self.InjectionsCount )  * 60, 5)
                else:
                    if ( self.InjectionsCount - self.SetUpEndInjectionsCount )  > 0:
                        self.CycleTimeAvg = round(self.ProductionTimeMin /  ( self.InjectionsCount - self.SetUpEndInjectionsCount )  * 60, 5)
            else:
                if self.Machine.MonitorSetupWorkingTime:
                    if ( self.InjectionsCount )  > 0:
                        self.CycleTimeAvg = round(self.ProductionTimeMin /  ( self.InjectionsCount )  * 60, 5)
                else:
                    if ( self.InjectionsCount )  > 0:
                        self.CycleTimeAvg = self.CycleTimeStandard
                        
            if self.CycleTimeAvgSMean > 0:
                self.CycleTimeAvgDiff = self.CycleTimeAvgSMean - self.CycleTimeStandard
            else:
                self.CycleTimeAvgDiff = self.CycleTimeAvg - self.CycleTimeStandard
            if self.CycleTimeStandard != 0:
                self.CycleTimeAvgDiffPC = round(self.CycleTimeAvgDiff / self.CycleTimeStandard * 100, 5)
            else:
                self.CycleTimeAvgDiffPC = 0

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcCycleTimeParams:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            Err.Clear()

    def CalcUnitsReportedOK(self):
        tUnitsReportedOK = 0.0
        tUnitsReportedOKDiff = 0.0

        try:
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
        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.CalcUnitsReportedOK:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            Err.Clear()

    def UpdateTimes(self):
        strSQL = ''
        self.CalcTimes

        try:
            self.DurationMin = DateDiff('n', self.StartTime, NowGMT())
            self.CalcTimesFromDB
            self.ActiveTimeMin = self.DurationMin - self.InActiveTimeMin
            self.ProductionTimeMin = self.ActiveTimeMin - self.DownTimeMin
            
            
            if self.Machine.NewJob:
                self.SetUpProductionTimeMin = self.ProductionTimeMin
                self.SetUpDownTimeMin = self.DownTimeMin
            
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
            strSQL = 'UPDATE TblJosh'
            strSQL = strSQL + ' SET DurationMin = ' + self.DurationMin
            strSQL = strSQL + ', DownTimeMin = ' + round(self.DownTimeMin, 5)
            strSQL = strSQL + ', SetUpDownTimeMin = ' + round(self.SetUpDownTimeMin, 5)
            strSQL = strSQL + ', InActiveTimeMin = ' + round(self.InActiveTimeMin, 5)
            strSQL = strSQL + ', ActiveTimeMin = ' + round(self.ActiveTimeMin, 5)
            strSQL = strSQL + ', ProductionTimeMin = ' + round(self.ProductionTimeMin, 5)
            strSQL = strSQL + ', SetUpProductionTimeMin = ' + round(self.SetUpProductionTimeMin, 5)
            strSQL = strSQL + ', DownTimePC = ' + round(self.DownTimePC, 5)
            strSQL = strSQL + ', ProductionTimePC = ' + round(self.ProductionTimePC, 5)
            strSQL = strSQL + ', ProductionUsabilityPC = ' + round(self.ProductionUsabilityPC, 5)
            strSQL = strSQL + ', InActiveTimePC = ' + round(self.InActiveTimePC, 5)
            strSQL = strSQL + ', ActiveTimePC = ' + round(self.ActiveTimePC, 5)
            strSQL = strSQL + ' WHERE ID = ' + self.ID
        except BaseException as error:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.UpdateTimes:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + '. JobID:' + self.Job.ID)
            Err.Clear()

    def RunValidations(self, pValidationTimingType):
        tVariant = Variant()
        tValidation = Validation()
        tValidationID = 0

        try:
            for tVariant in self.Machine.Validations:
                tValidation = tVariant
                tValidationID = tValidation.ID
                if tValidation.ValidationTiming == pValidationTimingType:
                    tValidation.Validate(self.Job, self)

        except BaseException as error:
            MdlGlobal.RecordError(type(self).__name__ + '.RunValidations:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + '. JobID:' + self.Job.ID + '. ValidationID:' + tValidationID)
            Err.Clear()

    def GetUnitsInCycle(self, PRstData=None):
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
        
        try:        
            if PRstData and MdlADOFunctions.fGetRstValString(PRstData.CavitiesActual) != "0" and MdlADOFunctions.fGetRstValString(PRstData.CavitiesStandard) != "0":
                if MdlADOFunctions.fGetRstValString(PRstData.CavitiesActual) != '' and MdlADOFunctions.fGetRstValString(PRstData.CavitiesStandard) != '' and MdlADOFunctions.fGetRstValString(PRstData.CavitiesActual) != '0' and MdlADOFunctions.fGetRstValString(PRstData.CavitiesStandard) != '0' and MdlADOFunctions.fGetRstValString(PRstData.CavitiesActual) != '0.00' and MdlADOFunctions.fGetRstValString(PRstData.CavitiesStandard) != '0.00':
                    self.CavitiesActual = MdlADOFunctions.fGetRstValDouble(PRstData.CavitiesActual)
                    self.CavitiesStandard = MdlADOFunctions.fGetRstValDouble(PRstData.CavitiesStandard)
                    
            tMachineID = self.Machine.ID
            tUnitsInCycleType = self.Machine.UnitsInCycleType
            if tUnitsInCycleType == 0:
                tUnitsInCycleType = 1
                tTableName = 'TblMolds'
                tFieldName = 'CavitiesCurrent'
                tStandardTableName = 'TblMolds'
                tStandardFieldName = 'Cavities'
            else:
                strSQL = 'SELECT TableName, FieldName, StandardTableName, StandardFieldName FROM STblMachineUnitsInCycleTypes WHERE ID = ' + str(tUnitsInCycleType)
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstData:
                    tTableName = MdlADOFunctions.fGetRstValString(RstData.TableName)
                    tFieldName = MdlADOFunctions.fGetRstValString(RstData.FieldName)
                    tStandardTableName = MdlADOFunctions.fGetRstValString(RstData.StandardTableName)
                    tStandardFieldName = MdlADOFunctions.fGetRstValString(RstData.StandardFieldName)
                RstCursor.close()
            
            if (tTableName == 'TblMolds'):
                tRefID = self.Mold.ID
                tUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue(tFieldName, tTableName, 'ID = ' + str(tRefID), 'CN'))
            elif (tTableName == 'TblProduct'):
                tRefID = self.Product.ID
                tUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue(tFieldName, tTableName, 'ID = ' + str(tRefID), 'CN'))
            elif (tTableName == 'TblProductRecipe'):
                tRefID = self.Product.ID
                tUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(tRefID, tFieldName, 0, 0))
            elif (tTableName == 'TblProductRecipeJob'):
                tUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.Job.ID, tFieldName, 0, 0))
            
            if tStandardTableName != '' and tStandardFieldName != '':
                if (tStandardTableName == 'TblMolds'):
                    tRefID = self.Mold.ID
                    
                    tStandardUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue(tStandardFieldName, tStandardTableName, 'ID = ' + str(tRefID), 'CN'))
                elif (tStandardTableName == 'TblProduct'):
                    tRefID = self.Product.ID
                    
                    tStandardUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue(tStandardFieldName, tStandardTableName, 'ID = ' + str(tRefID), 'CN'))
                elif (tStandardTableName == 'TblProductRecipe'):
                    tRefID = self.Product.ID
                    
                    tStandardUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueProduct(tRefID, tStandardFieldName, 0, 0))
                elif (tStandardTableName == 'TblProductRecipeJob'):
                    
                    tStandardUnitsInCycle = MdlADOFunctions.fGetRstValDouble(MdlUtilsH.fGetRecipeValueJob(self.Job.ID, tStandardFieldName, 0, 0))
            else:
                tStandardUnitsInCycle = tUnitsInCycle
            if tUnitsInCycle == 0:
                tUnitsInCycle = 1
            if tStandardUnitsInCycle == 0:
                tStandardUnitsInCycle = tUnitsInCycle
            self.CavitiesActual = tUnitsInCycle
            self.CavitiesStandard = tStandardUnitsInCycle

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
        RstCursor = None

    def GetParametersForOfflineJob(self):
        strSQL = ''

        RstCursor = None

        try:
            strSQL = 'SELECT TotalUnitsJosh,InjectionsCount,InjectionsCountLast FROM TblJosh WHERE ID = ' + self.ID
            RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            RstCursor.ActiveConnection = None
            if RstData:
                if self.InjectionsCount != MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCount):
                    self.InjectionsCount = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCount)
                    self.TotalUnitsJosh = self.InjectionsCount * self.CavitiesActual
                    self.InjectionsCountLast = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCountLast)
                    self.InjectionsCountDiff = self.InjectionsCount - self.InjectionsCountLast
                else:
                    self.TotalUnitsJosh = self.InjectionsCount * self.CavitiesActual
                    self.InjectionsCountLast = self.InjectionsCount
                    self.InjectionsCountDiff = 0
            RstCursor.close()

        except BaseException as error:
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

    def UpdateEfficienciesTarget(self):
        strSQL = ''

        RstCursor = None

        try:
            strSQL = 'SELECT * FROM TblMachines WHERE ID = ' + self.Machine.ID
            RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            RstCursor.ActiveConnection = None
            if RstData:
                strSQL = ''
                strSQL = strSQL + 'Update TblJosh' + vbCrLf
                strSQL = strSQL + 'SET' + vbCrLf
                strSQL = strSQL + 'CycleTimeEfficiencyTarget = ' + MdlADOFunctions.fGetRstValDouble(RstData.CycleTimeEfficiencyTarget) + vbCrLf
                strSQL = strSQL + ',RejectsEfficiencyTarget = ' + MdlADOFunctions.fGetRstValDouble(RstData.RejectsEfficiencyTarget) + vbCrLf
                strSQL = strSQL + ',CavitiesEfficiencyTarget = ' + MdlADOFunctions.fGetRstValDouble(RstData.CavitiesEfficiencyTarget) + vbCrLf
                strSQL = strSQL + ',DownTimeEfficiencyTarget = ' + MdlADOFunctions.fGetRstValDouble(RstData.DownTimeEfficiencyTarget) + vbCrLf
                strSQL = strSQL + ',DownTimeEfficiencyOEETarget = ' + MdlADOFunctions.fGetRstValDouble(RstData.DownTimeEfficiencyOEETarget) + vbCrLf
                strSQL = strSQL + ',PEETarget = ' + MdlADOFunctions.fGetRstValDouble(RstData.PEETarget) + vbCrLf
                strSQL = strSQL + ',OEETarget = ' + MdlADOFunctions.fGetRstValDouble(RstData.OEETarget) + vbCrLf
                strSQL = strSQL + ',ShiftUnitsTarget = ' + MdlADOFunctions.fGetRstValDouble(RstData.ShiftUnitsTarget) + vbCrLf
                strSQL = strSQL + 'Where ID = ' + self.ID
                CN.Execute(( strSQL ))
            RstCursor.close()
        except BaseException as error:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            Err.Clear()
        if RstCursor.State != 0:
            RstCursor.close()
        RstCursor = None

    def __CalcEngineTimesFromDB(self):
        strSQL = ''

        RstCursor = None

        try:
            strSQL = 'SELECT EngineTimeMin FROM ViewRTJoshEngineEvents WHERE JobID = ' + self.Job.ID + ' AND ShiftID = ' + self.Shift.ID
            RstCursor.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            RstCursor.ActiveConnection = None
            if RstData:
                self.EngineTimeMin = MdlADOFunctions.fGetRstValLong(RstData.EngineTimeMin)
            RstCursor.close()

        except BaseException as error:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.CalcEngineTimesFromDB:', str(0), error.args[0], 'JoshID: ' + str(self.ID) + ' JobID:' + self.Job.ID)
            Err.Clear()
        RstCursor = None

    def __del__(self):
        pass
            


    def setEngineTimeMin(self, value):
        self.__mEngineTimeMin = value

    def getEngineTimeMin(self):
        returnVal = None
        returnVal = self.__mEngineTimeMin
        return returnVal
    EngineTimeMin = property(fset=setEngineTimeMin, fget=getEngineTimeMin)


    def setQuantityAdjustmentUnits(self, value):
        self.__mQuantityAdjustmentUnits = value

    def getQuantityAdjustmentUnits(self):
        returnVal = None
        returnVal = self.__mQuantityAdjustmentUnits
        return returnVal
    QuantityAdjustmentUnits = property(fset=setQuantityAdjustmentUnits, fget=getQuantityAdjustmentUnits)


    def setRejectsTotalLine(self, value):
        self.__mRejectsTotalLine = value

    def getRejectsTotalLine(self):
        returnVal = None
        returnVal = self.__mRejectsTotalLine
        return returnVal
    RejectsTotalLine = property(fset=setRejectsTotalLine, fget=getRejectsTotalLine)


    def setRejectsEfficiencyLine(self, value):
        self.__mRejectsEfficiencyLine = value

    def getRejectsEfficiencyLine(self):
        returnVal = None
        returnVal = self.__mRejectsEfficiencyLine
        return returnVal
    RejectsEfficiencyLine = property(fset=setRejectsEfficiencyLine, fget=getRejectsEfficiencyLine)


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


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    
    def setJob(self, value):
        self.__mJob = value

    def getJob(self):
        returnVal = None
        returnVal = self.__mJob
        return returnVal
    Job = property(fset=setJob, fget=getJob)


    
    def setShift(self, value):
        self.__mShift = value

    def getShift(self):
        returnVal = None
        returnVal = self.__mShift
        return returnVal
    Shift = property(fset=setShift, fget=getShift)


    def setShiftID(self, value):
        self.__mShiftID = value

    def getShiftID(self):
        returnVal = None
        returnVal = self.__mShiftID
        return returnVal
    ShiftID = property(fset=setShiftID, fget=getShiftID)


    def setShiftDefID(self, value):
        self.__mShiftDefID = value

    def getShiftDefID(self):
        returnVal = None
        returnVal = self.__mShiftDefID
        return returnVal
    ShiftDefID = property(fset=setShiftDefID, fget=getShiftDefID)


    def setShiftManagerID(self, value):
        self.__mShiftManagerID = value

    def getShiftManagerID(self):
        returnVal = None
        returnVal = self.__mShiftManagerID
        return returnVal
    ShiftManagerID = property(fset=setShiftManagerID, fget=getShiftManagerID)


    def setStartTime(self, value):
        self.__mStartTime = value

    def getStartTime(self):
        returnVal = None
        returnVal = self.__mStartTime
        return returnVal
    StartTime = property(fset=setStartTime, fget=getStartTime)


    def setEndTime(self, value):
        self.__mEndTime = value

    def getEndTime(self):
        returnVal = None
        returnVal = self.__mEndTime
        return returnVal
    EndTime = property(fset=setEndTime, fget=getEndTime)


    def setDurationMin(self, value):
        self.__mDurationMin = value

    def getDurationMin(self):
        returnVal = None
        returnVal = self.__mDurationMin
        return returnVal
    DurationMin = property(fset=setDurationMin, fget=getDurationMin)


    
    def setDepartment(self, value):
        self.__mDepartment = value

    def getDepartment(self):
        returnVal = None
        returnVal = self.__mDepartment
        return returnVal
    Department = property(fset=setDepartment, fget=getDepartment)


    def setControllerID(self, value):
        self.__mControllerID = value

    def getControllerID(self):
        returnVal = None
        returnVal = self.__mControllerID
        return returnVal
    ControllerID = property(fset=setControllerID, fget=getControllerID)


    def setUnitsTargetJob(self, value):
        self.__mUnitsTargetJob = value

    def getUnitsTargetJob(self):
        returnVal = None
        returnVal = self.__mUnitsTargetJob
        return returnVal
    UnitsTargetJob = property(fset=setUnitsTargetJob, fget=getUnitsTargetJob)


    def setJobOrderNum(self, value):
        self.__mJobOrderNum = value

    def getJobOrderNum(self):
        returnVal = None
        returnVal = self.__mJobOrderNum
        return returnVal
    JobOrderNum = property(fset=setJobOrderNum, fget=getJobOrderNum)


    
    def setMachine(self, value):
        self.__mMachine = value

    def getMachine(self):
        returnVal = None
        returnVal = self.__mMachine
        return returnVal
    Machine = property(fset=setMachine, fget=getMachine)


    
    def setMachineType(self, value):
        self.__mMachineType = value

    def getMachineType(self):
        returnVal = None
        returnVal = self.__mMachineType
        return returnVal
    MachineType = property(fset=setMachineType, fget=getMachineType)


    
    def setProduct(self, value):
        self.__mProduct = value

    def getProduct(self):
        returnVal = None
        returnVal = self.__mProduct
        return returnVal
    Product = property(fset=setProduct, fget=getProduct)


    
    def setMold(self, value):
        self.__mMold = value

    def getMold(self):
        returnVal = None
        returnVal = self.__mMold
        return returnVal
    Mold = property(fset=setMold, fget=getMold)


    def setUnitsProducedJob(self, value):
        self.__mUnitsProducedJob = value

    def getUnitsProducedJob(self):
        returnVal = None
        returnVal = self.__mUnitsProducedJob
        return returnVal
    UnitsProducedJob = property(fset=setUnitsProducedJob, fget=getUnitsProducedJob)


    def setUnitsProducedOK(self, value):
        self.__mUnitsProducedOK = value

    def getUnitsProducedOK(self):
        returnVal = None
        returnVal = self.__mUnitsProducedOK
        return returnVal
    UnitsProducedOK = property(fset=setUnitsProducedOK, fget=getUnitsProducedOK)


    def setUnitsProducedPCJob(self, value):
        self.__mUnitsProducedPCJob = value

    def getUnitsProducedPCJob(self):
        returnVal = None
        returnVal = self.__mUnitsProducedPCJob
        return returnVal
    UnitsProducedPCJob = property(fset=setUnitsProducedPCJob, fget=getUnitsProducedPCJob)


    def setJoshStartUnits(self, value):
        self.__mJoshStartUnits = value

    def getJoshStartUnits(self):
        returnVal = None
        returnVal = self.__mJoshStartUnits
        return returnVal
    JoshStartUnits = property(fset=setJoshStartUnits, fget=getJoshStartUnits)


    def setTotalUnitsJosh(self, value):
        self.__mTotalUnitsJosh = value

    def getTotalUnitsJosh(self):
        returnVal = None
        returnVal = self.__mTotalUnitsJosh
        return returnVal
    TotalUnitsJosh = property(fset=setTotalUnitsJosh, fget=getTotalUnitsJosh)


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


    def setInjectionsCountDiff(self, value):
        self.__mInjectionsCountDiff = value

    def getInjectionsCountDiff(self):
        returnVal = None
        returnVal = self.__mInjectionsCountDiff
        return returnVal
    InjectionsCountDiff = property(fset=setInjectionsCountDiff, fget=getInjectionsCountDiff)


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


    def setCycleTimeLast(self, value):
        self.__mCycleTimeLast = value

    def getCycleTimeLast(self):
        returnVal = None
        returnVal = self.__mCycleTimeLast
        return returnVal
    CycleTimeLast = property(fset=setCycleTimeLast, fget=getCycleTimeLast)


    def setCycleTimeAvg(self, value):
        self.__mCycleTimeAvg = value

    def getCycleTimeAvg(self):
        returnVal = None
        returnVal = self.__mCycleTimeAvg
        return returnVal
    CycleTimeAvg = property(fset=setCycleTimeAvg, fget=getCycleTimeAvg)


    def setCycleTimeStandard(self, value):
        self.__mCycleTimeStandard = value

    def getCycleTimeStandard(self):
        returnVal = None
        returnVal = self.__mCycleTimeStandard
        return returnVal
    CycleTimeStandard = property(fset=setCycleTimeStandard, fget=getCycleTimeStandard)


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


    def setCycleTimeEfficiency(self, value):
        self.__mCycleTimeEfficiency = value

    def getCycleTimeEfficiency(self):
        returnVal = None
        returnVal = self.__mCycleTimeEfficiency
        return returnVal
    CycleTimeEfficiency = property(fset=setCycleTimeEfficiency, fget=getCycleTimeEfficiency)


    def setRejectsTotal(self, value):
        self.__mRejectsTotal = value

    def getRejectsTotal(self):
        returnVal = None
        returnVal = self.__mRejectsTotal
        return returnVal
    RejectsTotal = property(fset=setRejectsTotal, fget=getRejectsTotal)


    def setRejectsPC(self, value):
        self.__mRejectsPC = value

    def getRejectsPC(self):
        returnVal = None
        returnVal = self.__mRejectsPC
        return returnVal
    RejectsPC = property(fset=setRejectsPC, fget=getRejectsPC)


    def setRejectsEfficiency(self, value):
        self.__mRejectsEfficiency = value

    def getRejectsEfficiency(self):
        returnVal = None
        returnVal = self.__mRejectsEfficiency
        return returnVal
    RejectsEfficiency = property(fset=setRejectsEfficiency, fget=getRejectsEfficiency)


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
        if not self.Job is None:
            if self.Job.PConfigID != 0:
                returnVal = self.Job.PConfigUnits
            else:
                returnVal = self.__mCavitiesActual
        else:
            returnVal = self.__mCavitiesActual
        return returnVal
    CavitiesActual = property(fset=setCavitiesActual, fget=getCavitiesActual)


    def setCavitiesPC(self, value):
        self.__mCavitiesPC = value

    def getCavitiesPC(self):
        returnVal = None
        returnVal = self.__mCavitiesPC
        return returnVal
    CavitiesPC = property(fset=setCavitiesPC, fget=getCavitiesPC)


    def setCavitiesEfficiency(self, value):
        self.__mCavitiesEfficiency = value

    def getCavitiesEfficiency(self):
        returnVal = None
        returnVal = self.__mCavitiesEfficiency
        return returnVal
    CavitiesEfficiency = property(fset=setCavitiesEfficiency, fget=getCavitiesEfficiency)


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


    def setProductWeightLast(self, value):
        self.__mProductWeightLast = value

    def getProductWeightLast(self):
        returnVal = None
        returnVal = self.__mProductWeightLast
        return returnVal
    ProductWeightLast = property(fset=setProductWeightLast, fget=getProductWeightLast)


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


    def setMaterialTotal(self, value):
        self.__mMaterialTotal = value

    def getMaterialTotal(self):
        returnVal = None
        returnVal = self.__mMaterialTotal
        return returnVal
    MaterialTotal = property(fset=setMaterialTotal, fget=getMaterialTotal)


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


    def setStatus(self, value):
        self.__mStatus = value

    def getStatus(self):
        returnVal = None
        returnVal = self.__mStatus
        return returnVal
    Status = property(fset=setStatus, fget=getStatus)


    def setWorkerID(self, value):
        self.__mWorkerID = value

    def getWorkerID(self):
        returnVal = None
        returnVal = self.__mWorkerID
        return returnVal
    WorkerID = property(fset=setWorkerID, fget=getWorkerID)


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


    def setMaterialRecipeIndexProduct(self, value):
        self.__mMaterialRecipeIndexProduct = value

    def getMaterialRecipeIndexProduct(self):
        returnVal = None
        returnVal = self.__mMaterialRecipeIndexProduct
        return returnVal
    MaterialRecipeIndexProduct = property(fset=setMaterialRecipeIndexProduct, fget=getMaterialRecipeIndexProduct)


    def setMaterialRecipeIndexJob(self, value):
        self.__mMaterialRecipeIndexJob = value

    def getMaterialRecipeIndexJob(self):
        returnVal = None
        returnVal = self.__mMaterialRecipeIndexJob
        return returnVal
    MaterialRecipeIndexJob = property(fset=setMaterialRecipeIndexJob, fget=getMaterialRecipeIndexJob)


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


    def setCycleTimeAvgSMean(self, value):
        self.__mCycleTimeAvgSMean = value

    def getCycleTimeAvgSMean(self):
        returnVal = None
        returnVal = self.__mCycleTimeAvgSMean
        return returnVal
    CycleTimeAvgSMean = property(fset=setCycleTimeAvgSMean, fget=getCycleTimeAvgSMean)


    def setProductRecipeWeight(self, value):
        self.__mProductRecipeWeight = value

    def getProductRecipeWeight(self):
        returnVal = None
        returnVal = self.__mProductRecipeWeight
        return returnVal
    ProductRecipeWeight = property(fset=setProductRecipeWeight, fget=getProductRecipeWeight)


    def setTotalWasteKg(self, value):
        self.__mTotalWasteKg = value

    def getTotalWasteKg(self):
        returnVal = None
        returnVal = self.__mTotalWasteKg
        return returnVal
    TotalWasteKg = property(fset=setTotalWasteKg, fget=getTotalWasteKg)


    def setRejectsRead(self, value):
        self.__mRejectsRead = value

    def getRejectsRead(self):
        returnVal = None
        returnVal = self.__mRejectsRead
        return returnVal
    RejectsRead = property(fset=setRejectsRead, fget=getRejectsRead)


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


    def setOrderID(self, value):
        self.__mOrderID = value

    def getOrderID(self):
        returnVal = None
        returnVal = self.__mOrderID
        return returnVal
    OrderID = property(fset=setOrderID, fget=getOrderID)


    def setValidationLog(self, value):
        self.__mValidationLog = value

    def getValidationLog(self):
        returnVal = None
        returnVal = self.__mValidationLog
        return returnVal
    ValidationLog = property(fset=setValidationLog, fget=getValidationLog)


    def setSetUpEndInjectionsCount(self, value):
        self.__mSetUpEndInjectionsCount = value

    def getSetUpEndInjectionsCount(self):
        returnVal = None
        returnVal = self.__mSetUpEndInjectionsCount
        return returnVal
    SetUpEndInjectionsCount = property(fset=setSetUpEndInjectionsCount, fget=getSetUpEndInjectionsCount)
