from datetime import datetime
from colorama import Fore
from ControlParam import ControlParam
from Job import Job
from Josh import Josh
from RTEvent import RTEvent

import mdl_Common
import MdlADOFunctions
import MdlConnection
import MdlUtilsH
import MdlGlobal
import MdlDataSample
import MdlRTControllerFieldActions
import MdlOnlineTasks
import MdlRTWorkOrder

class Machine:
    __mID = 0
    __mTypeID = ''
    __mLName = ''
    __mEName = ''
    __mDescr = ''
    __mMachineType = 0
    __mStatus = ''
    __mActiveJobID = 0
    __mActiveJob = None
    __mActiveJoshID = 0
    __mActiveJosh = None
    __mLastJobID = 0
    __mActiveLocalID = ''
    __mDepartment = 0
    __mControllerDefID = 0
    __mControllerID = 0
    __mIsActive = False
    __mIsActiveCalendar = False
    __mLocRow = 0
    __mLocCol = 0
    __mDisplayOrder = 0
    __mMachineSize = 0
    __mMachineLoad = 0
    __mDownHourCost = 0
    __mWorkHourCost = 0
    __mCurrentDownTime = 0
    __mCurrentDownTimeCost = 0
    __mActiveProductID = 0
    __mActiveProductLName = ''
    __mActiveProductEName = ''
    __mActiveMoldID = ''
    __mLastMoldID = 0
    __mActiveMoldLocalID = ''
    __mMoldCavities = 0
    __mMoldActiveCavities = 0
    __mResetTotals = []
    __mUpdateAddress = None
    __mUpdateResetAddress = None
    __mJobStartTime = ''
    __mShrinkDataInterval = 0
    __mLastShrinkTime = None
    __mMoldEndTime = 0
    __mMoldEndTimeStatusOption = 0
    __mMoldEndTimeCalcOption = 0
    __mUPDController = False
    __mRunJobDetailsCalc = False
    __mCycleFilterHValue = 0
    __mCycleFilterLValue = 0
    __mAlertOnStopSuction = False
    __mStopSignalExist = False
    __mStopSignal = 0
    __mStopCyclesCount = 0
    __mCycleTimeFilter = False
    __mMachineSignalStop = False
    __mCalcCycleTime = False
    __mReseTotalCycles = False
    __mMaxCycleTime = 0
    __mMaterialCalc = False
    __mIPCProductWeightCountRatio = 0
    __mSetUpEndGeneralCycles = 0
    __mSetUpEndProductWeightCycles = 0
    __mSetUpEndCycleTimeCycles = 0
    __mSetUpEndPWCTRelation = 0
    __mAutoJobStartTimeCyclesWork = 0
    __mAutoJobStartOnUnitsOverTarget = 0
    __mIsBatchUpdatePP = False
    __mIgnoreCycleTimeFilter = False
    __mEnableAlarmsDuringSetup = False
    __mEnableAlarmsDuringMachineStop = False
    __mSetupEventIDOnShiftEnd = 0
    __mSetupEventIDOnSetupEnd = 0
    __mProductWeight = 0
    __mIsOffline = False
    __mCalcChannel100MaterialByCavity = False
    __mMonitorSetupWorkingTime = False
    __mControllerChannels = []
    __mHasBatchParams = False
    __mBatchTrigerP = None
    __mBatchTrigerSet = False
    __mBatchTrigerField = ''
    __mBatchUpdateP = None
    __mBatchUpdateField = ''
    __mBatchReadTable = ''
    __mOPCServer = None
    __mCParams = {}
    __mOPCGroupGeneral = None
    __mCParamsServerHandles = []
    __mCParamsErrors = []
    __mBTServerHandles = []
    __mBTErrors = []
    mIOCancelID = 0
    mIOGroup = None
    mInGeneralRead = False
    mInBatchRead = False
    __mIOStatus = 0
    __mIOErrorCount = 0
    __mIODownCount = 0
    __mProgress = 0
    __mIOEnabled = False
    __mDownEventOn = False
    __mCycleTime = 0
    __mCycleTimeAvg = 0
    __mCycleTimeStandard = 0
    __mTotalCycles = 0
    __mTotalCyclesLast = 0
    __mTSCyclesInterval = 0
    __mNoProgressCount = 0
    __mLastProgressTime = None
    __mLastCalcTime = None
    __mLastIOTime = None
    __mMachineStop = False
    __mStatusParam = None
    __mStatusParamSet = False
    __mReadFailCount = 0
    __mReadWaitCount = 0
    __mRejectsParam = None
    __mRejectsParamSet = False
    __mRejects = 0
    __mTimeLeftHr = 0
    __mTotalCyclesAutoAdvance = False
    __mWeightDistanceRatioReset = False
    __mAlarmsActive = False
    __mAlarmsParams = []
    __mAlarmsParamCount = []
    __mAlarmsOnCount = 0
    __mAlarmFile = ''
    __mInControl = False
    __mNewJob = False
    __mAutoAlarmClerance = False
    __mCyclesDiff = 0
    __mCyclesDiffRead = 0
    __mCycleWeight = 0
    __mTotalWeight = 0
    __mTotalWeightLast = 0
    __mTotalWeightDiff = 0
    __mPConfigJobs = []
    __mPConfigJobsInjections = []
    __mPConfigLastJobIDProgressed = 0
    __mPConfigJobIDCyclesProgressed = 0
    __mPConfigJobsArrSize = 0
    __mRejectsRead = 0
    __mRejectsReadLast = 0
    __mRejectsReadDiff = 0
    __mAddRejectsOnSetupEnd = False
    __mRejectsReadOption = ''
    __mUnitsReportedOKOption = ''
    __mReportRejectsUnReported = False
    __mCycleTimeEffFactor = 0
    __mMachineTimeEffFactor = 0
    __mRejectsEffFactor = 0
    __mCavitiesEffFactor = 0
    __mServer = None
    __mMainList = {}
    __mMainListXML = ''
    __mControllerList = {}
    __mControllerXML = ''
    __mChannelList = {}
    __mChannelXML = ''
    __mDSIsActive = False
    __mManualRead = False
    mTaskTriggers = []
    __cntTimerInterval = 10000
    __cntWriteTimerInterval = 600000
    __cntDeviceDisableIntervalSec = 300
    __cntDeviceEnableIntervalSec = 600
    __cntReadFailCount = 12
    __cntReadWaitCount = 60
    __cntStopCyclesCount = 2
    __cntSPCmaxCount = 100
    __cntSPCGroupSize = 7
    __cntShrinkDataInterval = 6
    __mCalcDelayPassed = False
    __mStartCalcAfterDelayInSeconds = 0
    __mUnitsInCycleType = 0
    __mValidations = []
    __mLocationBatchChangeSetupModeID = 0
    __mLocationBatchChangeSetupValue = 0
    __mActivePalletInventoryID = 0
    __mActivePalletCreationModeID = 0
    __mAutoPrintLabel = False
    __mIsDosingSystem = False
    __mDynamicWareHouseLocation = False
    __mUpdateAddressOnJobActive = False
    __mAllowAutoRejectsOnSetup = False
    __mConnectedByOPC = False
    __mProductionModeID = 0
    __mProductionModeReasonID = 0
    __mProductionModeGroupReasonID = 0
    __mProductionModeDisableProductionTime = False
    __mProductionModeCalcEfficiencies = False
    __mProductionModeOverCalendarEvent = False
    __mBatchReadLastRecord = None
    __mMachineStopSetting = 0
    __mMachineStopSettingSetPoint = 0
    __mDefaultCycleTime = 0
    __mStatusLastChangeTime = None
    __mLineID = 0
    __mRootEventAttachDurationMin = 0
    __mLineFirstMachineID = 0
    __mLineLastMachineID = 0
    __mDisconnectWorkerOnShiftChange = False
    __mContinueEventReasonOnShiftChange = False
    __mMachineSignalStopTimestamp = None
    __mActiveCalendarEvent = False
    __mActiveCalendarEventProductionModeID = 0
    __mEngineSignal = 0
    __mEngineSignalExist = False
    __mEngineSignalActive = False
    __mReportStopReasonByOpenCall = False
    __mTotalCycles = 0.0
    
    def INITMachine(self, MachineID, vOpcServer):
        returnVal = None
        strSQL = ''
        Rst = None
        rVal = 0
        strGroupName = ''
        ChannelSplits = 0
        validateRst = None
        temp = ''
        tControllerChannel = None
        PRst = None
        returnVal = False

        self.__mUPDController = False
        self.__mOPCServer = vOpcServer

        try:
            if MachineID == 2:
                returnVal = self.INITMachine()
            strSQL = 'Select * From TblMachines Where ID = ' + str(MachineID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.__mID = MachineID
                self.__mTypeID = MdlADOFunctions.fGetRstValLong(RstData.TypeID)
                self.__mLName = '' + RstData.MachineLName
                self.__mEName = '' + RstData.MachineName
                self.__mDepartment = MdlADOFunctions.fGetRstValLong(RstData.Department)
                self.__mControllerDefID = MdlADOFunctions.fGetRstValLong(RstData.ControllerDefID)
                self.__mControllerID = MdlADOFunctions.fGetRstValLong(RstData.ControllerID)
                self.__mMachineSize = MdlADOFunctions.fGetRstValDouble(RstData.MachineSize)
                self.__mMachineLoad = MdlADOFunctions.fGetRstValDouble(RstData.MachineLoad)
                self.__mDownHourCost = MdlADOFunctions.fGetRstValDouble(RstData.DownHourCost)
                self.__mWorkHourCost = MdlADOFunctions.fGetRstValDouble(RstData.WorkHourCost)
                self.__mRunJobDetailsCalc = MdlADOFunctions.fGetRstValBool(RstData.RunJobDetailsCalc, True)
                self.__mAlertOnStopSuction = MdlADOFunctions.fGetRstValBool(RstData.AlertOnStopSuction, False)
                self.__mStopSignalExist = MdlADOFunctions.fGetRstValBool(RstData.StopSignalExist, False)
                self.__mCycleFilterHValue = MdlADOFunctions.fGetRstValDouble(RstData.CycleFilterHValue)
                self.__mCycleFilterLValue = MdlADOFunctions.fGetRstValDouble(RstData.CycleFilterLValue)
                self.__mMaxCycleTime = MdlADOFunctions.fGetRstValDouble(RstData.MaxCycleTime)
                self.__mCalcCycleTime = MdlADOFunctions.fGetRstValBool(RstData.CalcCycleTime, False)
                self.__mMaterialCalc = MdlADOFunctions.fGetRstValBool(RstData.MaterialCalc, True)
                self.__mReseTotalCycles = MdlADOFunctions.fGetRstValBool(RstData.ReseTotalCycles, False)
                self.__mAlarmFile = str(RstData.AlarmFile)
                self.__mAutoAlarmClerance = MdlADOFunctions.fGetRstValBool(RstData.AutoAlarmClearance, True)
                self.__mStopSignal = MdlADOFunctions.fGetRstValLong(RstData.StopSignal)
                self.__mStopCyclesCount = MdlADOFunctions.fGetRstValDouble(RstData.StopCyclesCount)
                self.__mCycleTimeFilter = MdlADOFunctions.fGetRstValBool(RstData.CycleTimeFilter, True)
                self.__mIPCProductWeightCountRatio = MdlADOFunctions.fGetRstValDouble(RstData.IPCProductWeightCountRatio)
                self.SetUpEndGeneralCycles = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndGeneralCycles)
                self.__mSetUpEndProductWeightCycles = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndProductWeightCycles)
                self.__mSetUpEndCycleTimeCycles = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndCycleTimeCycles)
                self.__mSetUpEndPWCTRelation = MdlADOFunctions.fGetRstValLong(RstData.SetUpEndPWCTRelation)
                self.__mAutoJobStartTimeCyclesWork = MdlADOFunctions.fGetRstValDouble(RstData.AutoJobStartTimeCyclesWork)
                self.__mAutoJobStartOnUnitsOverTarget = MdlADOFunctions.fGetRstValDouble(RstData.AutoJobStartOnUnitsOverTarget)
                self.__mTotalCyclesAutoAdvance = MdlADOFunctions.fGetRstValBool(RstData.TotalCyclesAutoAdvance, False)
                self.__mWeightDistanceRatioReset = MdlADOFunctions.fGetRstValBool(RstData.WeightDistanceRatioReset, False)
                self.__mMachineType = MdlADOFunctions.fGetRstValLong(RstData.TypeID)
                self.__mManualRead = MdlADOFunctions.fGetRstValBool(RstData.ManualRead, False)
                self.__mEnableAlarmsDuringSetup = MdlADOFunctions.fGetRstValBool(RstData.EnableAlarmsDuringSetup, False)
                self.__mEnableAlarmsDuringMachineStop = MdlADOFunctions.fGetRstValBool(RstData.EnableAlarmsDuringMachineStop, False)
                
                self.__mSetupEventIDOnSetupEnd = MdlADOFunctions.fGetRstValLong(RstData.SetupEventIDOnSetupEnd)
                self.__mSetupEventIDOnShiftEnd = MdlADOFunctions.fGetRstValLong(RstData.SetupEventIDOnShiftEnd)
                self.__mReportRejectsUnReported = MdlADOFunctions.fGetRstValBool(RstData.ReportRejectsUnReported, False)
                self.__mMoldEndTimeStatusOption = MdlADOFunctions.fGetRstValLong(RstData.MoldEndTimeStatusOption)
                self.__mMoldEndTimeCalcOption = MdlADOFunctions.fGetRstValLong(RstData.MoldEndTimeCalcOption)
                self.__mIsOffline = MdlADOFunctions.fGetRstValBool(RstData.IsOffline, False)
                self.__mAddRejectsOnSetupEnd = MdlADOFunctions.fGetRstValBool(RstData.AddRejectsOnSetupEnd, True)
                self.__mCalcChannel100MaterialByCavity = MdlADOFunctions.fGetRstValBool(RstData.CalcChannel100MaterialByCavity, True)
                self.__mDynamicWareHouseLocation = MdlADOFunctions.fGetRstValBool(RstData.DynamicWareHouseLocation, False)
                self.__mAllowAutoRejectsOnSetup = MdlADOFunctions.fGetRstValBool(RstData.AllowAutoRejectsOnSetup, True)
                self.__mConnectedByOPC = MdlADOFunctions.fGetRstValBool(RstData.ConnectedByOPC, True)
                self.__mMonitorSetupWorkingTime = MdlADOFunctions.fGetRstValBool(RstData.MonitorSetupWorkingTime, False)
                temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CycleTimeEffFactor', 'STblDepartments', 'ID = ' + str(self.__mDepartment), 'CN'))
                if temp == '':
                    temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'CycleTimeEffFactor\'', 'CN'))
                    if temp == '':
                        temp = 1
                self.__mCycleTimeEffFactor = MdlADOFunctions.fGetRstValDouble(temp)
                temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('MachineTimeEffFactor', 'STblDepartments', 'ID = ' + str(self.__mDepartment), 'CN'))
                if temp == '':
                    temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'MachineTimeEffFactor\'', 'CN'))
                    if temp == '':
                        temp = 1
                self.__mMachineTimeEffFactor = MdlADOFunctions.fGetRstValDouble(temp)
                temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('RejectsEffFactor', 'STblDepartments', 'ID = ' + str(self.__mDepartment), 'CN'))
                if temp == '':
                    temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'RejectsEffFactor\'', 'CN'))
                    if temp == '':
                        temp = 1
                self.__mRejectsEffFactor = MdlADOFunctions.fGetRstValDouble(temp)
                temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CavitiesEffFactor', 'STblDepartments', 'ID = ' + str(self.__mDepartment), 'CN'))
                if temp == '':
                    temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'CavitiesEffFactor\'', 'CN'))
                    if temp == '':
                        temp = 1
                self.__mCavitiesEffFactor = MdlADOFunctions.fGetRstValDouble(temp)
                self.__mDSIsActive = MdlADOFunctions.fGetRstValBool(RstData.DSIsActive, False)
                self.__mStartCalcAfterDelayInSeconds = MdlADOFunctions.fGetRstValLong(RstData.StartCalcAfterDelayInSeconds)
                self.__mUnitsInCycleType = MdlADOFunctions.fGetRstValLong(RstData.UnitsInCycleType)
                if self.__mUnitsInCycleType == 0:
                    self.__mUnitsInCycleType = 1
                self.__mLocationBatchChangeSetupModeID = MdlADOFunctions.fGetRstValLong(RstData.LocationBatchChangeSetupModeID)
                self.__mLocationBatchChangeSetupValue = MdlADOFunctions.fGetRstValDouble(RstData.LocationBatchChangeSetupValue)
                self.__mActivePalletInventoryID = MdlADOFunctions.fGetRstValLong(RstData.ActivePalletInventoryID)
                self.__mAutoPrintLabel = MdlADOFunctions.fGetRstValBool(RstData.AutoPrintLabel, False)
                self.__mUpdateAddressOnJobActive = MdlADOFunctions.fGetRstValBool(RstData.UpdateAddressOnJobActive, False)
                self.__mActivePalletCreationModeID = MdlADOFunctions.fGetRstValLong(RstData.ActivePalletCreationModeID)
                self.__mProductionModeID = MdlADOFunctions.fGetRstValLong(RstData.ProductionModeID)
                if self.__mProductionModeID == 0:
                    self.__mProductionModeID = 1
                
                strSQL = 'SELECT * FROM STblProductionModes WHERE ID = ' + str(self.__mProductionModeID)
                PRstCursor = MdlConnection.CN.cursor()
                PRstCursor.execute(strSQL)
                PRstData = PRstCursor.fetchone()

                if PRstData:
                    self.__mProductionModeReasonID = MdlADOFunctions.fGetRstValLong(PRstData.EventReasonID)
                    self.__mProductionModeGroupReasonID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('EventGroupID', 'STblEventDesr', 'ID = ' + str(self.__mProductionModeReasonID)))
                    self.__mProductionModeDisableProductionTime = MdlADOFunctions.fGetRstValBool(PRstData.DisableProductionTime, False)
                    self.__mProductionModeCalcEfficiencies = MdlADOFunctions.fGetRstValBool(PRstData.CalcEfficiencies, False)
                    self.__mProductionModeOverCalendarEvent = MdlADOFunctions.fGetRstValBool(PRstData.OverCalendarEvent, True)
                PRstCursor.close()

                self.__mMachineStopSetting = MdlADOFunctions.fGetRstValLong(RstData.MachineStopSetting)
                if self.__mMachineStopSetting == 0:
                    self.__mMachineStopSetting = 1
                self.__mMachineStopSettingSetPoint = MdlADOFunctions.fGetRstValDouble(RstData.MachineStopSettingSetPoint)
                self.__mDefaultCycleTime = MdlADOFunctions.fGetRstValDouble(RstData.DefaultCycleTime)
                if self.__mDefaultCycleTime == 0:
                    self.__mDefaultCycleTime = 30
                
                if MdlADOFunctions.fGetRstValString(RstData.StatusLastChangeTime) != '':
                    self.__mStatusLastChangeTime = RstData.StatusLastChangeTime
                self.__mDisconnectWorkerOnShiftChange = MdlADOFunctions.fGetRstValBool(RstData.DisconnectWorkerOnShiftChange, False)
                self.__mContinueEventReasonOnShiftChange = MdlADOFunctions.fGetRstValBool(RstData.ContinueEventReasonOnShiftChange, True)
                self.__mActiveCalendarEvent = MdlADOFunctions.fGetRstValBool(RstData.ActiveCalendarEvent, False)
                self.__mActiveCalendarEventProductionModeID = MdlADOFunctions.fGetRstValLong(RstData.ActiveCalendarEventProductionModeID)
                self.__mEngineSignal = MdlADOFunctions.fGetRstValLong(RstData.EngineSignal)
                self.__mEngineSignalExist = MdlADOFunctions.fGetRstValBool(RstData.EngineSignalExist, False)
                self.__mReportStopReasonByOpenCall = MdlADOFunctions.fGetRstValBool(RstData.ReportStopReasonByOpenCall, False)
            else:
                raise Exception("No data found.")
            RstCursor.close()
            
            
            strSQL = 'SELECT TOP 1 * FROM ViewRTLinesMachines WHERE MachineID = ' + str(self.ID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.LineID = MdlADOFunctions.fGetRstValLong(RstData.LineID)
                self.RootEventAttachDurationMin = MdlADOFunctions.fGetRstValLong(RstData.RootEventAttachDurationMin)
                self.LineFirstMachineID = MdlADOFunctions.fGetRstValLong(RstData.FirstMachineID)
                self.LineLastMachineID = MdlADOFunctions.fGetRstValLong(RstData.LastMachineID)
                if self.RootEventAttachDurationMin == 0:
                    
                    self.RootEventAttachDurationMin = MdlADOFunctions.fGetRstValLong(RstData.LineRootEventAttachDurationMin)
            RstCursor.close()
            
            strSQL = 'Select RejectsRead, UnitsReportedOK From StblUnitsConfigurationTable Where MachineID = ' + str(MachineID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.__mRejectsReadOption = '' + MdlADOFunctions.fGetRstValString(RstData.RejectsRead)
                self.__mUnitsReportedOKOption = '' + MdlADOFunctions.fGetRstValString(RstData.UnitsReportedOK)
            RstCursor.close()
            
            strSQL = 'Select * From TblControllers Where ID = ' + str(self.__mControllerID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if str(RstData.BatchIDTag)  != '' and  str(RstData.BatchReadTable)  != '':
                self.__mHasBatchParams = True
                self.__mBatchReadTable = str(RstData.BatchReadTable)
                self.__mBatchTrigerField = str(RstData.BatchIDTag)
                self.__mBatchUpdateField = str(RstData.BatchIDTagW)
            else:
                self.__mHasBatchParams = False
            if str(RstData.Job).isnumeric():
                strSQL = 'Select ID From TblJobCurrent Where ID = ' + str(MdlADOFunctions.fGetRstValLong(RstData.Job)) + ' AND MachineID = ' + str(self.ID)

                validateRstCursor = MdlConnection.CN.cursor()
                validateRstCursor.execute(strSQL)
                validateRstData = validateRstCursor.fetchone()

                if validateRstData:
                    self.ActiveJobID = RstData.Job
                else:
                    self.ActiveJobID = 0
                validateRstCursor.close()
            if str(RstData.Job).isnumeric() and self.Server.CurrentShiftID > 0:
                strSQL = 'Select ID From TblJoshCurrent Where JobID = ' + str(MdlADOFunctions.fGetRstValLong(RstData.Job)) + ' AND MachineID = ' + str(self.ID) + ' AND ShiftID = ' + str(self.Server.CurrentShiftID)

                validateRstCursor = MdlConnection.CN.cursor()
                validateRstCursor.execute(strSQL)
                validateRstData = validateRstCursor.fetchone()

                if validateRstData:
                    self.ActiveJoshID = validateRstData.ID
                else:
                    self.ActiveJoshID = 0
                validateRstCursor.close()

            self.__mTotalWeight = MdlADOFunctions.fGetRstValDouble(RstData.TotalWeight)
            self.__mTotalWeightLast = self.TotalWeight
            self.__mTotalWeightDiff = 0
            if MdlADOFunctions.fGetRstValString(RstData.LastCalcTime) != '':
                self.LastCalcTime = MdlUtilsH.ShortDate(RstData.LastCalcTime, True, True)
            RstCursor.close()
            strGroupName = 'M_' + str(self.__mID) + '_General'

            # self.__mOPCGroupGeneral = self.__mOPCServer.OPCGroups.Add()
            # self.__mOPCGroupGeneral.IsActive = True
            # self.__mOPCGroupGeneral.IsSubscribed = True            
            # self.__mOPCGroupGeneral.UpdateRate = GeneralGroupRefreshRate
            
            print(Fore.GREEN + 'Loading Controller Fields.')
            rVal = self.__ControllerFieldsLoad(self.__mControllerID)

            if self.ActiveJobID > 0:
                self.JobLoad(self.ActiveJobID, False, False, True)
                strSQL = 'Delete TblJobCurrent Where MachineID = ' + str(self.__mID) + ' AND ID <> ' + self.__mActiveJobID + ' AND PConfigParentID <> ' + self.__mActiveJobID
                MdlConnection.CN.execute(strSQL)
                
                            
            if self.__mActiveJobID > 0:
                MdlOnlineTasks.fInitMachineTriggers(self, self.__mActiveJobID, True)
            else:
                MdlOnlineTasks.fInitMachineTriggers(self, VBGetMissingArgument(MdlOnlineTasks.fInitMachineTriggers, 1), True)
            
            LoadMachineValidations(self)
            
            CheckIfDosingSystem
            self.__mUPDController = True
            self.__mIgnoreCycleTimeFilter = False
            returnVal = True

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

        if RstCursor:
            RstCursor.close()
        RstCursor = None

        if validateRstCursor:
            validateRstCursor.close()
        validateRstCursor = None
        tControllerChannel = None
        
        return returnVal
        

    def __init__(self):
        self.__mBatchTrigerSet = False
        self.__mAlarmsParams = []
        self.__mAlarmsParamCount = []
        self.__mAlarmsActive = True
        self.__mStatusParamSet = False
        self.__mIOStatus = 1
        self.__mStatus = 1
        self.__mMachineSignalStop = False
        self.__mEngineSignalActive = False
        self.__mLastProgressTime = mdl_Common.NowGMT()
        self.__mLastIOTime = mdl_Common.NowGMT()
        self.__mLastShrinkTime = mdl_Common.NowGMT()
        self.__mIOEnabled = True
        self.__mNewJob = False
        self.__mLastCalcTime = mdl_Common.NowGMT()

    def __del__(self):
        Counter = 0

        temp = ''
        
        for Counter in range(0, self.__mCParams.Count):
            self.__mCParams.Item[Counter] = None
            self.__mCParams.Remove(Counter)
        
        temp = self.__mOPCGroupGeneral.Name
        self.__mOPCGroupGeneral.IsActive = False
        self.__mOPCGroupGeneral.IsSubscribed = False
        self.__mOPCServer.OPCGroups.Remove(temp)
        self.__mOPCGroupGeneral = None
        if self.__mBatchTrigerSet == True:
            temp = self.__mBatchTrigerP.BatchGroup.Name
            self.__mBatchTrigerP.BatchGroup.IsActive = False
            self.__mBatchTrigerP.BatchGroup.IsSubscribed = False
            self.__mOPCServer.OPCGroups.Remove(temp)
            

    def __ControllerFieldsLoad(self, CsID):
        strSQL = ''
        temp = ''
        strItemID = ''
        strGroupName = ''
        Rst = None
        tControlParam = None
        vParam = [None]
        ParamFound = False
        rVal = 0
        Counter = 0
        rParam = None
        returnVal = False

        try:
            strSQL = 'Select * From TblControllerFields Where ControllerID = ' + str(CsID) + ' AND BatchRead = 0 ORDER BY ChannelID, ID'
            
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()

            for RstData in RstValues:
                tControlParam = ControlParam()
                tControlParam.ID = RstData.ID
                tControlParam.ChannelID = MdlADOFunctions.fGetRstValLong(RstData.ChannelID)
                tControlParam.ChannelNum = MdlADOFunctions.fGetRstValLong(RstData.ChannelNum)
                tControlParam.CVarAddress = str(RstData.TagAddress)
                tControlParam.FieldID = RstData.ID
                tControlParam.FName = str(RstData.FieldName)
                tControlParam.LName = str(RstData.LName)
                tControlParam.EName = str(RstData.EName)
                tControlParam.SyncWrite = MdlADOFunctions.fGetRstValBool(RstData.SyncWrite, False)
                tControlParam.TagName = str(RstData.CiTagName)
                tControlParam.CalcFunction = str(RstData.CalcFunction)
                tControlParam.ChannelNum = str(RstData.ChannelNum)
                tControlParam.RawZero = MdlADOFunctions.fGetRstValDouble(RstData.RawZero)
                tControlParam.RawFull = MdlADOFunctions.fGetRstValDouble(RstData.RawFull)
                tControlParam.ScaledZero = MdlADOFunctions.fGetRstValDouble(RstData.ScaleZero)
                tControlParam.ScaledFull = MdlADOFunctions.fGetRstValDouble(RstData.ScaleFull)
                tControlParam.DirectRead = MdlADOFunctions.fGetRstValBool(RstData.DirectRead, False)
                tControlParam.FieldDataType = MdlADOFunctions.fGetRstValLong(RstData.FieldDataType)
                tControlParam.CitectDeviceType = MdlADOFunctions.fGetRstValLong(RstData.CitectDeviceType)
                tControlParam.AlarmCycleAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmCylceAcknowledge, False)
                tControlParam.AlarmPerminentAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmPerminentAcknowledge, False)
                
                tControlParam.SourceTableName = str(RstData.SourceTableName)
                tControlParam.SourceFieldName = str(RstData.SourceFieldName)
                tControlParam.SourceStrWhere = str(RstData.SourceStrWhere)
                
                tControlParam.RejectReasonID = MdlADOFunctions.fGetRstValLong(RstData.RejectReasonID)
                tControlParam.RejectReasonOption = MdlADOFunctions.fGetRstValLong(RstData.RejectReasonOption)
                
                tControlParam.RejectReasonDirectRead = MdlADOFunctions.fGetRstValBool(RstData.RejectReasonDirectRead, False)
                
                if tControlParam.RejectReasonID != 0:
                    tControlParam.RejectsIncludeInRejectsTotal = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('IncludeInRejectsTotal', 'STbDefectReasons', 'ID = ' + str(tControlParam.RejectReasonID), 'CN'), True)
                tControlParam.ChangeJobOnValueChanged = MdlADOFunctions.fGetRstValBool(RstData.ChangeJobOnValueChanged, False)
                tControlParam.PrintLabelID = MdlADOFunctions.fGetRstValLong(RstData.PrintLabelID)
                tControlParam.PrintLabelMachineID = MdlADOFunctions.fGetRstValLong(RstData.PrintLabelMachineID)
                tControlParam.CalcStringExpression = MdlADOFunctions.fGetRstValString(RstData.CalcStringExpression)
                
                tControlParam.ValidateValue = MdlADOFunctions.fGetRstValBool(RstData.ValidateValue, False)
                tControlParam.MinValueUnitsPerMin = MdlADOFunctions.fGetRstValDouble(RstData.MinValueUnitsPerMin)
                tControlParam.MaxValueUnitsPerMin = MdlADOFunctions.fGetRstValDouble(RstData.MaxValueUnitsPerMin)
                tControlParam.ForceValueTimeout = MdlADOFunctions.fGetRstValDouble(RstData.ForceValueTimeout)
                if tControlParam.ForceValueTimeout == 0:
                    tControlParam.ForceValueTimeout = 5
                tControlParam.PrevValidValue = MdlADOFunctions.fGetRstValString(RstData.CurrentValidValue)
                tControlParam.LastValidValue = MdlADOFunctions.fGetRstValString(RstData.CurrentValidValue)
                if MdlADOFunctions.fGetRstValString(RstData.ValidValueSampleTime) != '':
                    tControlParam.LastValidSampleTime = RstData.ValidValueSampleTime
                tControlParam.StartCalcAfterDelayInSeconds = MdlADOFunctions.fGetRstValLong(RstData.StartCalcAfterDelayInSeconds)
                if tControlParam.RawZero != tControlParam.RawFull:
                    tControlParam.CalcScalingRatio()
                if str(RstData.FPrecision).isnumeric():
                    tControlParam.Precision = RstData.FPrecision
                else:
                    tControlParam.Precision = 0
                tControlParam.RoundType = MdlADOFunctions.fGetRstValLong(RstData.RoundType)
                if RstData.AlarmFile:
                    tControlParam.AlarmFile = RstData.AlarmFile
                else:
                    tControlParam.AlarmFile = ''
                tControlParam.InMainTable = RstData.InMainTable
                if RstData.CreateNC == True:
                    tControlParam.IgnoreAlarmAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.IgnoreAlarmAcknowledge, False)
                    tControlParam.ErrorAlarmActive = True
                    if RstData.AlarmType > 0:
                        tControlParam.AlarmActiveVoice = True
                    if RstData.AlarmArea > 0:
                        tControlParam.AlarmArea = RstData.AlarmArea
                    else:
                        tControlParam.AlarmArea = 0
                    if MdlADOFunctions.fGetRstValBool(RstData.SendSMSOnAlarm, False):
                        tControlParam.SendSMSOnAlarm = True
                    else:
                        tControlParam.SendSMSOnAlarm = False
                    tControlParam.SendEmailOnAlarm = MdlADOFunctions.fGetRstValBool(RstData.SendEmailOnAlarm, False)
                    if RstData.AlarmPriv:
                        tControlParam.ErrorCountAlarm = RstData.AlarmPriv
                    else:
                        tControlParam.ErrorCountAlarm = MdlGlobal.cntErrorCountAlarm
                    
                    tControlParam.AlarmFileReplayInterval = MdlADOFunctions.fGetRstValLong(RstData.AlarmFileReplayInterval)
                    tControlParam.AlarmMinimumDuration = MdlADOFunctions.fGetRstValLong(RstData.AlarmMinimumDuration)
                    tControlParam.EnableAlarmsDuringSetup = MdlADOFunctions.fGetRstValBool(RstData.EnableAlarmsDuringSetup, True)
                    tControlParam.SendPushOnAlarm = MdlADOFunctions.fGetRstValBool(RstData.SendPushOnAlarm, False)
                else:
                    tControlParam.ErrorAlarmActive = False
                
                tControlParam.PropertyID = MdlADOFunctions.fGetRstValLong(RstData.MachinePropertyID)
                
                if RstData.CitectDeviceType == 1:
                    strItemID = '' + RstData.OPCTagName
                    tControlParam.OPCItem = self.__mOPCGroupGeneral.OPCItems.AddItem(strItemID, tControlParam.ID * 10)
                    tControlParam.OPCItemHandle = tControlParam.ID * 10
                    self.__mCParamsServerHandles = []
                    self.__mCParamsServerHandles[self.__mOPCGroupGeneral.OPCItems.Count] = tControlParam.OPCItem.ServerHandle
                    self.__mCParamsErrors = []
                self.__mCParams[str(tControlParam.FName)] = tControlParam
                tControlParam.pMachine = self
                
                if tControlParam.FName == 'TotalCycles':
                    tControlParam.LastValue = tControlParam.LastValidValue
                
                if MdlADOFunctions.fGetRstValLong(RstData.CitectDeviceType) == 1 and not  ( str(RstData.TagWriteAddress) == '0' or str(RstData.TagWriteAddress) == '' ) :
                    tControlParam.WriteTag = True
                    strItemID = '' + RstData.OPCTagNameW
                    tControlParam.OPCItemW = self.__mOPCGroupGeneral.OPCItems.AddItem(strItemID, tControlParam.ID * 10 + 1)
                    tControlParam.OPCItemWHandle = tControlParam.ID * 10 + 1
                    self.__mCParamsServerHandles = []
                    self.__mCParamsServerHandles[self.__mOPCGroupGeneral.OPCItems.Count] = tControlParam.OPCItem.ServerHandle
                    self.__mCParamsErrors = []
                
                if MdlADOFunctions.fGetRstValLong(RstData.CitectDeviceType) == 1 and not  (str(RstData.SPOPCTagName) == '0' or str(RstData.SPOPCTagName) == '' ) :                    
                    strItemID = str(RstData.SPOPCTagName)
                    tControlParam.SPOPCItem = self.__mOPCGroupGeneral.OPCItems.AddItem(strItemID, tControlParam.ID * 10 + 2)
                    tControlParam.SPOPCItemHandle = tControlParam.ID * 10 + 2
                    self.__mCParamsServerHandles = []
                    self.__mCParamsServerHandles[self.__mOPCGroupGeneral.OPCItems.Count] = tControlParam.OPCItem.ServerHandle
                    self.__mCParamsErrors = []
                if MdlADOFunctions.fGetRstValLong(RstData.CitectDeviceType) == 1 and not  (str(RstData.SPLOPCTagName) == '0' or str(RstData.SPLOPCTagName) == '' ) :
                    
                    strItemID = '' + RstData.SPLOPCTagName
                    tControlParam.SPLOPCItem = self.__mOPCGroupGeneral.OPCItems.AddItem(strItemID, tControlParam.ID * 10 + 2)
                    tControlParam.SPOPCItemHandle = tControlParam.ID * 10 + 3
                    self.__mCParamsServerHandles = []
                    self.__mCParamsServerHandles[self.__mOPCGroupGeneral.OPCItems.Count] = tControlParam.OPCItem.ServerHandle
                    self.__mCParamsErrors = []
                if MdlADOFunctions.fGetRstValLong(RstData.CitectDeviceType) == 1 and not  (str(RstData.SPHOPCTagName) == '0' or str(RstData.SPHOPCTagName) == '' ) :
                    
                    strItemID = '' + RstData.SPHOPCTagName
                    tControlParam.SPHOPCItem = self.__mOPCGroupGeneral.OPCItems.AddItem(strItemID, tControlParam.ID * 10 + 2)
                    tControlParam.SPHOPCItemHandle = tControlParam.ID * 10 + 4
                    self.__mCParamsServerHandles = []
                    self.__mCParamsServerHandles[self.__mOPCGroupGeneral.OPCItems.Count] = tControlParam.OPCItem.ServerHandle
                    self.__mCParamsErrors = []
                if self.__mHasBatchParams == True:
                    
                    if RstData.FieldName == self.__mBatchTrigerField:
                        self.__mBatchTrigerP = tControlParam
                        self.__mBatchTrigerSet = True
                        strGroupName = 'M_' + str(self.__mID) + '_BatchTrigger'
                        
                        tControlParam.BatchGroupCreate
                        tControlParam.BatchTable = self.__mBatchReadTable
                    if self.__mBatchUpdateField != '' and RstData.FieldName == self.__mBatchUpdateField:
                        self.__mBatchUpdateP = tControlParam
                
                if RstData.IsSPCValue == True:
                    tControlParam.IsSPCValue = True
                    if RstData.SPCSamplesMaxCount > 0:
                        tControlParam.SPCSamplesMaxCount = RstData.SPCSamplesMaxCount
                    else:
                        tControlParam.SPCSamplesMaxCount = self.__cntSPCmaxCount
                    if RstData.SPCGroupSize > 0:
                        tControlParam.SPCGroupSize = RstData.SPCGroupSize
                    else:
                        tControlParam.SPCGroupSize = self.__cntSPCGroupSize
                    if ( '' + RstData.SPCTable )  != '':
                        tControlParam.SPCTable = RstData.SPCTable
                
                if (RstData.FieldName == 'ResetTotalsAddress'):
                    self.__mResetTotals.append(tControlParam)
                    
                elif (RstData.FieldName == 'UpdateAddress'):
                    self.__mUpdateAddress = tControlParam
                elif (RstData.FieldName == 'UpdateResetAddress'):
                    self.__mUpdateResetAddress = tControlParam
                elif (RstData.FieldName == 'Status'):
                    self.__mStatusParam = tControlParam
                    self.__mStatusParamSet = True
                    self.__mStatusParam.LastValue = 1
                elif (RstData.FieldName == 'MachineID'):
                    tControlParam.LastValue = self.__mID
                elif (RstData.FieldName == 'Rejects'):
                    self.__mRejectsParam = tControlParam
                    self.__mRejectsParamSet = True
                if tControlParam.CitectDeviceType == 3:
                    tControlParam.LastValue = MdlADOFunctions.fGetRstValString(RstData.CurrentValue)
                tControlParam.ReportInventoryItemOnChange = MdlADOFunctions.fGetRstValLong(RstData.ReportInventoryItemOnChange)
                tControlParam.EffectiveAmountFieldName = MdlADOFunctions.fGetRstValString(RstData.EffectiveAmountFieldName)
                tControlParam.ControllerFieldTypeID = MdlADOFunctions.fGetRstValLong(RstData.ControllerFieldTypeID)
                tControlParam.ReportInventoryItemOnChangeInterval = MdlADOFunctions.fGetRstValLong(RstData.ReportInventoryItemOnChangeInterval)
                tControlParam.UpdateActivePallet = MdlADOFunctions.fGetRstValBool(RstData.UpdateActivePallet, False)
                tControlParam.ConversionID = MdlADOFunctions.fGetRstValLong(RstData.ConversionID)
                tControlParam.CheckValidateValue.Init(tControlParam)
                
                
                tControlParam.CalcByDiff = MdlADOFunctions.fGetRstValBool(RstData.CalcByDiff, False)
                tControlParam.dReadValue = MdlADOFunctions.fGetRstValString(RstData.dReadValue)
                tControlParam.dLastValidValue = MdlADOFunctions.fGetRstValString(RstData.dLastValidValue)
                tControlParam.dPrevValue = MdlADOFunctions.fGetRstValString(RstData.dPrevValue)
                tControlParam.dDiffValue = MdlADOFunctions.fGetRstValString(RstData.dDiffValue)
                tControlParam.dResetSuspect = MdlADOFunctions.fGetRstValBool(RstData.dResetSuspect, False)
                
                tControlParam.ExternalUpdate = MdlADOFunctions.fGetRstValBool(RstData.ExternalUpdate, False)
                
                if MdlADOFunctions.fGetRstValString(RstData.dLastReadTime) != '':
                    tControlParam.dLastReadTime = RstData.dLastReadTime
                
                tControlParam.CalcByDiffValidate = MdlADOFunctions.fGetRstValBool(RstData.CalcByDiffValidate, False)
                
                tControlParam.BufferEnabled = MdlADOFunctions.fGetRstValBool(RstData.BufferEnabled, False)
                tControlParam.CalcMainDataOnBuffer = MdlADOFunctions.fGetRstValBool(RstData.CalcMainDataOnBuffer, False)
                tControlParam.CalcByDiffWithScaling = MdlADOFunctions.fGetRstValBool(RstData.CalcByDiffWithScaling, False)
                tControlParam.CalcByDiffScalingRound = MdlADOFunctions.fGetRstValBool(RstData.CalcByDiffScalingRound, False)
                tControlParam.dLowLimit = MdlADOFunctions.fGetRstValDouble(RstData.dLowLimit)
                tControlParam.dHighLimit = MdlADOFunctions.fGetRstValDouble(RstData.dHighLimit)
                tControlParam.ChangeJobOnValueChangedSourceTable = MdlADOFunctions.fGetRstValString(RstData.ChangeJobOnValueChangedSourceTable)
                tControlParam.ChangeJobOnValueChangedSourceField = MdlADOFunctions.fGetRstValString(RstData.ChangeJobOnValueChangedSourceField)
                if MdlADOFunctions.fGetRstValBool(RstData.ResetTotalsValue, False) == True:
                    self.__mResetTotals.append(tControlParam)
                
                
            RstCursor.close()
            if self.__mHasBatchParams == True and self.__mBatchTrigerSet == True:
                self.__mBatchTrigerP.BatchParams = {}
                
                strSQL = 'Select * From TblControllerFields Where ControllerID = ' + str(CsID) + ' AND FieldDataType IN(1,3,4,5) AND BatchRead <> 0'
                
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstValues = RstCursor.fetchall()

                for RstData in RstValues:
                    tControlParam = ControlParam()
                    tControlParam.ChannelID = MdlADOFunctions.fGetRstValLong(RstData.ChannelNum)
                    tControlParam.CVarAddress = RstData.TagAddress
                    tControlParam.FieldID = RstData.ID
                    tControlParam.FName = RstData.FieldName
                    tControlParam.LName = RstData.LName
                    tControlParam.EName = RstData.EName
                    tControlParam.SyncWrite = MdlADOFunctions.fGetRstValBool(RstData.SyncWrite, False)
                    tControlParam.TagName = RstData.CiTagName
                    tControlParam.CalcFunction = RstData.CalcFunction
                    tControlParam.ChannelNum = RstData.ChannelNum
                    tControlParam.RawZero = MdlADOFunctions.fGetRstValDouble(RstData.RawZero)
                    tControlParam.RawFull = MdlADOFunctions.fGetRstValDouble(RstData.RawFull)
                    tControlParam.ScaledZero = MdlADOFunctions.fGetRstValDouble(RstData.ScaleZero)
                    tControlParam.ScaledFull = MdlADOFunctions.fGetRstValDouble(RstData.ScaleFull)
                    tControlParam.DirectRead = MdlADOFunctions.fGetRstValBool(RstData.DirectRead, False)
                    tControlParam.FieldDataType = MdlADOFunctions.fGetRstValLong(RstData.FieldDataType)
                    tControlParam.CitectDeviceType = MdlADOFunctions.fGetRstValLong(RstData.CitectDeviceType)
                    tControlParam.AlarmCycleAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmCylceAcknowledge, False)
                    tControlParam.AlarmPerminentAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmPerminentAcknowledge, False)
                    
                    tControlParam.SourceTableName = RstData.SourceTableName
                    tControlParam.SourceFieldName = RstData.SourceFieldName
                    tControlParam.SourceStrWhere = RstData.SourceStrWhere
                    
                    tControlParam.RejectReasonID = MdlADOFunctions.fGetRstValLong(RstData.RejectReasonID)
                    tControlParam.RejectReasonOption = MdlADOFunctions.fGetRstValLong(RstData.RejectReasonOption)
                    
                    tControlParam.RejectReasonDirectRead = MdlADOFunctions.fGetRstValBool(RstData.RejectReasonDirectRead, False)
                    
                    if tControlParam.RejectReasonID != 0:
                        tControlParam.RejectsIncludeInRejectsTotal = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('IncludeInRejectsTotal', 'STbDefectReasons', 'ID = ' + str(tControlParam.RejectReasonID), 'CN'), True)
                    
                    tControlParam.ValidateValue = MdlADOFunctions.fGetRstValBool(RstData.ValidateValue, False)
                    tControlParam.MinValueUnitsPerMin = MdlADOFunctions.fGetRstValDouble(RstData.MinValueUnitsPerMin)
                    tControlParam.MaxValueUnitsPerMin = MdlADOFunctions.fGetRstValDouble(RstData.MaxValueUnitsPerMin)
                    tControlParam.ForceValueTimeout = MdlADOFunctions.fGetRstValDouble(RstData.ForceValueTimeout)
                    if tControlParam.ForceValueTimeout == 0:
                        tControlParam.ForceValueTimeout = 5
                    tControlParam.PrevValidValue = MdlADOFunctions.fGetRstValString(RstData.CurrentValidValue)
                    tControlParam.LastValidValue = MdlADOFunctions.fGetRstValString(RstData.CurrentValidValue)
                    if MdlADOFunctions.fGetRstValString(RstData.ValidValueSampleTime) != '':
                        tControlParam.LastValidSampleTime = RstData.ValidValueSampleTime
                    tControlParam.StartCalcAfterDelayInSeconds = MdlADOFunctions.fGetRstValLong(RstData.StartCalcAfterDelayInSeconds)
                    if tControlParam.RawZero != tControlParam.RawFull:
                        tControlParam.CalcScalingRatio()
                    if str(RstData.FPrecision).isnumeric():
                        tControlParam.Precision = RstData.FPrecision
                    else:
                        tControlParam.Precision = 0
                    tControlParam.RoundType = MdlADOFunctions.fGetRstValLong(RstData.RoundType)
                    if RstData.AlarmFile:
                        tControlParam.AlarmFile = RstData.AlarmFile
                    else:
                        tControlParam.AlarmFile = ''
                    tControlParam.InMainTable = RstData.InMainTable
                    if RstData.CreateNC == True:
                        tControlParam.IgnoreAlarmAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.IgnoreAlarmAcknowledge, False)
                        tControlParam.ErrorAlarmActive = True
                        if RstData.AlarmType > 0:
                            tControlParam.AlarmActiveVoice = True
                        if MdlADOFunctions.fGetRstValBool(RstData.SendSMSOnAlarm, False):
                            tControlParam.SendSMSOnAlarm = True
                        else:
                            tControlParam.SendSMSOnAlarm = False
                        tControlParam.SendEmailOnAlarm = MdlADOFunctions.fGetRstValBool(RstData.SendEmailOnAlarm, False)
                        if MdlADOFunctions.fGetRstValLong(RstData.AlarmArea) > 0:
                            tControlParam.AlarmArea = MdlADOFunctions.fGetRstValLong(RstData.AlarmArea)
                        else:
                            tControlParam.AlarmArea = 0
                        if RstData.AlarmPriv:
                            tControlParam.ErrorCountAlarm = RstData.AlarmPriv
                        else:
                            tControlParam.ErrorCountAlarm = MdlGlobal.cntErrorCountAlarm
                        
                        tControlParam.AlarmFileReplayInterval = MdlADOFunctions.fGetRstValLong(RstData.AlarmFileReplayInterval)
                        tControlParam.AlarmMinimumDuration = MdlADOFunctions.fGetRstValLong(RstData.AlarmMinimumDuration)
                        tControlParam.EnableAlarmsDuringSetup = MdlADOFunctions.fGetRstValBool(RstData.EnableAlarmsDuringSetup, True)
                        tControlParam.SendPushOnAlarm = MdlADOFunctions.fGetRstValBool(RstData.SendPushOnAlarm, False)
                    else:
                        tControlParam.ErrorAlarmActive = False
                    
                    tControlParam.PropertyID = MdlADOFunctions.fGetRstValLong(RstData.MachinePropertyID)
                    tControlParam.ID = RstData.ID
                    
                    if ( RstData.CitectDeviceType == 1 )  and  ( RstData.FieldDataType != 4 )  and  ( RstData.FieldDataType != 5 ) :
                        strItemID = RstData.OPCTagName
                        tControlParam.OPCItem = self.__mBatchTrigerP.BatchGroup.OPCItems.AddItem(strItemID, tControlParam.ID * 10)
                        tControlParam.OPCItemHandle = tControlParam.ID * 10
                        
                        self.__mBatchTrigerP.BatchAddParamToList(tControlParam)
                        self.__mCParams.Add(tControlParam, str(tControlParam.FName))
                        
                        if not ( RstData.SPOPCTagName == '0' or RstData.SPOPCTagName == '' ) :
                            
                            strItemID = RstData.SPOPCTagName
                            tControlParam.SPOPCItem = self.__mOPCGroupGeneral.OPCItems.AddItem(strItemID, tControlParam.ID * 10 + 2)
                            tControlParam.SPOPCItemHandle = tControlParam.ID * 10 + 2
                            self.__mCParamsServerHandles = []
                            self.__mCParamsServerHandles[self.__mOPCGroupGeneral.OPCItems.Count] = tControlParam.OPCItem.ServerHandle
                            self.__mCParamsErrors = []
                        
                        if not ( RstData.SPLOPCTagName == '0' or RstData.SPLOPCTagName == '' ) :
                            
                            strItemID = RstData.SPLOPCTagName
                            tControlParam.SPLOPCItem = self.__mOPCGroupGeneral.OPCItems.AddItem(strItemID, tControlParam.ID * 10 + 2)
                            tControlParam.SPLOPCItemHandle = tControlParam.ID * 10 + 3
                            self.__mCParamsServerHandles = []
                            self.__mCParamsServerHandles[self.__mOPCGroupGeneral.OPCItems.Count] = tControlParam.OPCItem.ServerHandle
                            self.__mCParamsErrors = []
                        
                        if not ( RstData.SPHOPCTagName == '0' or RstData.SPHOPCTagName == '' ) :
                            
                            strItemID = RstData.SPHOPCTagName
                            tControlParam.SPHOPCItem = self.__mOPCGroupGeneral.OPCItems.AddItem(strItemID, tControlParam.ID * 10 + 2)
                            tControlParam.SPHOPCItemHandle = tControlParam.ID * 10 + 4
                            self.__mCParamsServerHandles = []
                            self.__mCParamsServerHandles[self.__mOPCGroupGeneral.OPCItems.Count] = tControlParam.OPCItem.ServerHandle
                            self.__mCParamsErrors = []
                    else:
                        if RstData.BatchRead == 1:
                            print(Fore.GREEN + "Adding Batch Param to List")
                            self.__mBatchTrigerP.BatchAddParamToList(tControlParam)
                            self.__mCParams[str(tControlParam.FName)] = tControlParam
                        else:
                            self.__mCParams[str(tControlParam.FName)] = tControlParam
                    tControlParam.pMachine = self
                    if RstData.IsSPCValue == True:
                        tControlParam.IsSPCValue = True
                        if RstData.SPCSamplesMaxCount > 0:
                            tControlParam.SPCSamplesMaxCount = RstData.SPCSamplesMaxCount
                        else:
                            tControlParam.SPCSamplesMaxCount = self.__cntSPCmaxCount
                        if RstData.SPCGroupSize > 0:
                            tControlParam.SPCGroupSize = RstData.SPCGroupSize
                        else:
                            tControlParam.SPCGroupSize = self.__cntSPCGroupSize
                        if ( '' + RstData.SPCTable )  != '':
                            tControlParam.SPCTable = RstData.SPCTable
                    tControlParam.ControllerFieldTypeID = MdlADOFunctions.fGetRstValLong(RstData.ControllerFieldTypeID)
                    print(Fore.GREEN + "Initializing Validate Value.")
                    tControlParam.CheckValidateValue.Init(tControlParam)
                    
                    
                    tControlParam.CalcByDiff = MdlADOFunctions.fGetRstValBool(RstData.CalcByDiff, False)
                    tControlParam.dReadValue = MdlADOFunctions.fGetRstValString(RstData.dReadValue)
                    tControlParam.dLastValidValue = MdlADOFunctions.fGetRstValString(RstData.dLastValidValue)
                    tControlParam.dPrevValue = MdlADOFunctions.fGetRstValString(RstData.dPrevValue)
                    tControlParam.dDiffValue = MdlADOFunctions.fGetRstValString(RstData.dDiffValue)
                    tControlParam.dResetSuspect = MdlADOFunctions.fGetRstValBool(RstData.dResetSuspect, False)
                    
                    tControlParam.ExternalUpdate = MdlADOFunctions.fGetRstValBool(RstData.ExternalUpdate, False)
                    
                    if MdlADOFunctions.fGetRstValString(RstData.dLastReadTime) != '':
                        tControlParam.dLastReadTime = RstData.dLastReadTime
                    
                    tControlParam.CalcByDiffValidate = MdlADOFunctions.fGetRstValBool(RstData.CalcByDiffValidate, False)
                    
                    tControlParam.BufferEnabled = MdlADOFunctions.fGetRstValBool(RstData.BufferEnabled, False)
                    tControlParam.CalcMainDataOnBuffer = MdlADOFunctions.fGetRstValBool(RstData.CalcMainDataOnBuffer, False)
                    tControlParam.CalcByDiffWithScaling = MdlADOFunctions.fGetRstValBool(RstData.CalcByDiffWithScaling, False)
                    tControlParam.CalcByDiffScalingRound = MdlADOFunctions.fGetRstValBool(RstData.CalcByDiffScalingRound, False)
                    tControlParam.dLowLimit = MdlADOFunctions.fGetRstValDouble(RstData.dLowLimit)
                    tControlParam.dHighLimit = MdlADOFunctions.fGetRstValDouble(RstData.dHighLimit)
                    
                    tControlParam.BatchTable = RstData.BatchTableName
                    tControlParam.BatchTableHistory = MdlADOFunctions.fGetRstValBool(RstData.BatchTableHistory, False)
                    tControlParam.BatchTableHistoryOnMachineStop = MdlADOFunctions.fGetRstValBool(RstData.BatchTableHistoryOnMachineStop, True)

                    print(Fore.GREEN + "Adding Batch Table.")
                    self.__mBatchTrigerP.AddBatchTable(tControlParam.BatchTable)
                    
                RstCursor.close()

            if len(self.__mCParams) == 0:
                raise Exception("Control params are empty.")
            

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()

            strSQL = 'Select * From TblControllerFields Where ControllerID = ' + str(self.__mControllerID) + ' AND AssertOnMainPage > 0 Order BY AssertOnMainPage'
            for RstData in RstValues:
                temp = RstData.FieldName
                ParamFound = False
                if self.GetParam(temp, vParam) == True:
                    self.__mMainList[vParam[0].FName] = vParam[0]
            RstCursor.close()
            
            strSQL = 'Select * From TblControllerFields Where ControllerID = ' + str(self.__mControllerID) + ' AND  AssertOnControllerPage > 0 Order BY AssertOnControllerPage'
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()

            for RstData in RstValues:
                temp = RstData.FieldName
                ParamFound = False
                if self.GetParam(temp, vParam) == True:
                    self.__mControllerList[vParam[0].FName] = vParam[0]
            RstCursor.close()
            
            strSQL = 'Select * From TblControllerFields Where ControllerID = ' + str(self.__mControllerID) + ' AND  AssertOnChannelPage > 0 Order BY AssertOnChannelPage'
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()

            for RstData in RstValues:
                temp = RstData.FieldName
                ParamFound = False
                if self.GetParam(temp, vParam) == True:
                    self.__mChannelList[vParam[0].FName] = vParam[0]
            RstCursor.close()
            
            print(Fore.GREEN + "Loading Conditional Controller Fields.")
            self.LoadConditionalControllerFields()
            print(Fore.GREEN + "Initializing Machine Data Samples.")
            MdlDataSample.fInitMachineDataSamples(self)
            print(Fore.GREEN + "Loading Machine Controller Field Actions.")
            MdlRTControllerFieldActions.fLoadMachineControllerFieldActions(self)
            returnVal = True
        
        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
            MdlGlobal.RecordError('LeaderRT:ControllerFieldsLoad', str(0), error.agrs[0], 'ControllerID = ' + str(CsID))
            
        # if RstCursor:
        #     RstCursor.close()
        RstCursor = None

        tControlParam = None
        rParam = None
        vParam = None
        return returnVal

    def fReadGeneralGroup(self):
        returnVal = None
        CancelID = 0

        ItemsCount = 0

        TransID = 0

        temp = ''

        sValues = []
        
        if self.__mIOEnabled == True:
            ItemsCount = self.__mOPCGroupGeneral.OPCItems.Count
            TransID = int(self.__mID) * 10
            CancelID = TransID
            
            self.mIOCancelID = CancelID            
            self.mInGeneralRead = True
            self.mIOGroup = self.__mOPCGroupGeneral
            self.__mOPCGroupGeneral.AsyncRead(ItemsCount, self.__mCParamsServerHandles, self.__mCParamsErrors, TransID, CancelID)
        
        self.CalculateStatus()
        return returnVal

    def fReadMainData(self, ManualEntry=False, WriteData=False, pIgnoreCycleTimeFilter=False):
        returnVal = None
        rVal = 0

        LDStat = False

        temp = ''

        Counter = 0

        tEventID = 0

        tEventGroupID = 0

        tVariant = Variant()

        tChildJob = None

        strSQL = None
        ActivateProductionMode = False

        ActivateProductionModeID = 0
        
        
        returnVal = False
        if self.ID == 38:
            rVal = rVal
        
        
        if self.CalcDelayPassed == False:
            if not self.ActiveJob is None:
                if DateDiff('s', self.ActiveJob.StartTime, mdl_Common.NowGMT()) >= self.StartCalcAfterDelayInSeconds and DateDiff('s', self.Server.StartTime, mdl_Common.NowGMT()) >= self.StartCalcAfterDelayInSeconds:
                    self.CalcDelayPassed = True
                else:
                    returnVal = True
                    GoTo(WriteData)
        if pIgnoreCycleTimeFilter == True:
            self.IgnoreCycleTimeFilter = True
        else:
            self.IgnoreCycleTimeFilter = False
        
        
        
        if ManualEntry == False:
            
            for Counter in range(0, self.__mCParams.Count):
                LDStat = self.__mCParams.Item(Counter).GetListData()
            self.__mIsBatchUpdatePP = False
            if self.__mBatchTrigerSet == True:
                
                if self.__mBatchUpdateField == '':
                    if ( MdlADOFunctions.fGetRstValLong(self.__mBatchTrigerP.LastValue) > 0 )  and self.Status != 0:
                        self.__mBatchTrigerP.BatchReadValues(False)
                else:
                    if MdlADOFunctions.fGetRstValLong(self.__mBatchTrigerP.LastValue) > 0 and  ( ( MdlADOFunctions.fGetRstValLong(self.__mBatchTrigerP.LastValue) > MdlADOFunctions.fGetRstValLong(self.__mBatchUpdateP.WriteValue) )  or  ( MdlADOFunctions.fGetRstValLong(self.__mBatchUpdateP.WriteValue) > MdlADOFunctions.fGetRstValLong(self.__mBatchTrigerP.LastValue) ) )  and MdlADOFunctions.fGetRstValLong(self.__mActiveJobID) > 0:
                        
                        self.__mBatchTrigerP.BatchReadValues(True)
                    
                    if MdlADOFunctions.fGetRstValLong(self.__mBatchTrigerP.LastValue) > 0 and  ( ( MdlADOFunctions.fGetRstValLong(self.__mBatchTrigerP.LastValue) == MdlADOFunctions.fGetRstValLong(self.__mBatchUpdateP.WriteValue) )  and  ( MdlADOFunctions.fGetRstValLong(self.__mBatchUpdateP.WriteValue) > MdlADOFunctions.fGetRstValLong(self.__mBatchUpdateP.LastValue) ) )  and MdlADOFunctions.fGetRstValLong(self.__mActiveJobID) > 0:
                        self.__mBatchTrigerP.BatchReadValues(True)
        
        
        
        
        if not ( self.ActiveJob is None )  and WriteData == True:
            
            
            self.CalculateStatus()
            self.fWriteMainData()
            
        elif not ( self.ActiveJob is None ) :
            fCalculateParams
            self.CalculateStatus()
            
        elif  ( self.ActiveJob is None ) :
            self.CalculateStatus()
        
        
        WriteProdutionParametersToHistory
        
        
        
        if not self.ActiveJob is None:
            if not self.ActiveJob.OpenEvent is None:
                if self.NewJob == False or  ( self.NewJob == True and self.SetupEventIDOnSetupEnd == 2 ) :
                    if fCheckForActiveCalendarEvent(self, mdl_Common.NowGMT()(), tEventID, tEventGroupID, ActivateProductionMode, ActivateProductionModeID):
                        
                        
                        if ( not self.ActiveJob.OpenEvent.IsCalendarEvent or self.ActiveJob.OpenEvent.EventID != tEventID )  and  ( self.ProductionModeID == 1 or  ( self.ProductionModeID > 1 and not self.ProductionModeOverCalendarEvent ) ) :
                            
                            if self.Server.SplitActiveEvent(self.ID, VBGetMissingArgument(self.Server.SplitActiveEvent, 1), self.ActiveJob.OpenEvent.ID, VBGetMissingArgument(self.Server.SplitActiveEvent, 3), False):
                                self.ActiveJob.OpenEvent.EventID = tEventID
                                self.ActiveJob.OpenEvent.EventGroup = tEventGroupID
                                self.ActiveJob.OpenEvent.IsCalendarEvent = True
                                self.ActiveJob.OpenEvent.RootEventID = 0
                                self.ActiveJob.OpenEvent.Update
                                self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                                
                                if ActivateProductionMode and ActivateProductionModeID > 0:
                                    self.ActiveCalendarEvent = True
                                    self.ActiveCalendarEventProductionModeID = ActivateProductionModeID
                                    strSQL = 'UPDATE TblMachines SET ActiveCalendarEvent = 1, ActiveCalendarEventProductionModeID = ' + self.ActiveCalendarEventProductionModeID + ' WHERE ID = ' + self.ID
                                    MdlConnection.CN.execute(strSQL)
                                else:
                                    self.ActiveCalendarEvent = False
                                    self.ActiveCalendarEventProductionModeID = 0
                                    strSQL = 'UPDATE TblMachines SET ActiveCalendarEvent = 0, ActiveCalendarEventProductionModeID = ' + self.ActiveCalendarEventProductionModeID + ' WHERE ID = ' + self.ID
                                    MdlConnection.CN.execute(strSQL)
                                
                                if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                                    for tVariant in self.ActiveJob.PConfigJobs:
                                        tChildJob = tVariant
                                        tChildJob.OpenEvent.EventID = tEventID
                                        tChildJob.OpenEvent.EventGroup = tEventGroupID
                                        tChildJob.OpenEvent.IsCalendarEvent = True
                                        tChildJob.OpenEvent.RootEventID = 0
                                        tChildJob.OpenEvent.Update
                    else:
                        
                        if self.ActiveJob.OpenEvent.IsCalendarEvent:
                            
                            if self.Server.SplitActiveEvent(self.ID, VBGetMissingArgument(self.Server.SplitActiveEvent, 1), self.ActiveJob.OpenEvent.ID, VBGetMissingArgument(self.Server.SplitActiveEvent, 3), False):
                                
                                if self.ProductionModeReasonID != 0:
                                    tEventID = self.ProductionModeReasonID
                                    tEventGroupID = self.ProductionModeGroupReasonID
                                else:
                                    tEventID = 0
                                    tEventGroupID = 6
                                self.ActiveJob.OpenEvent.EventID = tEventID
                                self.ActiveJob.OpenEvent.EventGroup = tEventGroupID
                                self.ActiveJob.OpenEvent.IsCalendarEvent = False
                                
                                strSQL = ''
                                strSQL = strSQL + 'UPDATE TblEvent SET' + vbCrLf
                                strSQL = strSQL + 'Event = ' + self.ActiveJob.OpenEvent.EventID + ',' + vbCrLf
                                strSQL = strSQL + 'EventGroup = ' + self.ActiveJob.OpenEvent.EventGroup + ',' + vbCrLf
                                strSQL = strSQL + 'IsCalendarEvent = 0'
                                strSQL = strSQL + 'WHERE ID = ' + self.ActiveJob.OpenEvent.ID
                                MdlConnection.CN.execute(( strSQL ))
                                self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                                
                                if self.ActiveCalendarEvent and self.ActiveCalendarEventProductionModeID > 0:
                                    
                                    dictRequest.Add('MachineID', self.ID)
                                    dictRequest.Add('ProductionModeID', self.ActiveCalendarEventProductionModeID)
                                    CallAPIRequest('SetProductionModeForMachine', dictRequest)
                                    self.ActiveCalendarEvent = False
                                    self.ActiveCalendarEventProductionModeID = 0
                                    strSQL = 'UPDATE TblMachines SET ActiveCalendarEvent = 0, ActiveCalendarEventProductionModeID = ' + self.ActiveCalendarEventProductionModeID + ' WHERE ID = ' + self.ID
                                    MdlConnection.CN.execute(strSQL)
                                
                                if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                                    for tVariant in self.ActiveJob.PConfigJobs:
                                        tChildJob = tVariant
                                        tChildJob.OpenEvent.EventID = tEventID
                                        tChildJob.OpenEvent.EventGroup = tEventGroupID
                                        tChildJob.OpenEvent.IsCalendarEvent = False
                                        tChildJob.OpenEvent.Update
        
        fCheckMachineTriggers(self)
        returnVal = True
        if Err.Number != 0:
            RecordError('Machine:fReadMainData', '' + Err.Number, '' + Err.Description, 'MID = ' + self.str(__mID))
            Err.Clear()
            
        
        return returnVal

    def fWriteMainData(self, pCalcMaterial=True):
        returnVal = None
        rVal = 0

        LDStat = False

        temp = ''

        Counter = 0

        ChannelNum = 0

        strControllerSQL = ''

        strMainSQL = ''

        strChannelSQL = ''

        MainFields = ''

        MainVals = ''

        CnlFields = ''

        CnlVals = ''

        strSetParams = ''

        CurrentShiftID = 0

        CalcMat = False

        strSQL = ''

        res = 0

        SetupEndStateAfterAutomaticReload = ''

        SkeepedMessage = False

        tParam = None
        
        returnVal = False
        if self.__mIOStatus == 0 and self.__mManualRead == False and self.IsOffline == False:
            return returnVal
        if self.ID == 38:
            self.__mManualRead = self.__mManualRead
        ShrinkData(False)
        for Counter in range(0, self.__mCParams.Count):
            if self.__mCParams(Counter).InMainTable == True:
                temp = self.__mCParams(Counter).LastValue
                if temp == '':
                    temp = 'NULL'
                if self.__mCParams(Counter).ChannelID > 0:
                    if self.__mCParams(Counter).ChannelNum > 0 and self.__mCParams(Counter).ChannelNum != ChannelNum:
                        
                        CnlFields = CnlFields + ', ControllerID, MachineID, ChannelID, ChannelNum, LastReadTime'
                        CnlVals = CnlVals + ', ' + str(self.__mControllerID) + ', ' + str(self.__mID) + ', ' + self.__mCParams(Counter).ChannelID + ', ' + ChannelNum + ', \'' + ShortDate(mdl_Common.NowGMT(), True, True) + '\''
                        
                        
                        CnlFields = ''
                        CnlVals = ''
                        strChannelSQL = ''
                        if strSetParams != '':
                            strSetParams = Right(strSetParams, Len(strSetParams) - 2)
                            strChannelSQL = 'Update TblControllerChannels SET ' + strSetParams + ' Where ControllerID = ' + str(self.__mControllerID) + ' AND ChannelNum = ' + ChannelNum
                            MdlConnection.CN.execute(strChannelSQL)
                        strSetParams = ''
                        strChannelSQL = ''
                        ChannelNum = self.__mCParams(Counter).ChannelNum
                    CnlFields = CnlFields + ', ' + Right(self.__mCParams(Counter).FName, Len(self.__mCParams(Counter).FName) - 4)
                    CnlVals = CnlVals + ', ' + temp
                    strSetParams = strSetParams + ', ' + Right(self.__mCParams(Counter).FName, Len(self.__mCParams(Counter).FName) - Len('Cnl' + str(CDbl(ChannelNum - 1)))) + ' = ' + temp
                else:
                    strControllerSQL = strControllerSQL + ', ' + self.__mCParams(Counter).FName + ' = ' + temp
                    MainFields = MainFields + ', ' + self.__mCParams(Counter).FName
                    MainVals = MainVals + ', ' + temp
        
        strControllerSQL = 'Update TblControllers SET LastReadTime = \'' + ShortDate(mdl_Common.NowGMT(), True, True) + '\' ' + strControllerSQL
        strControllerSQL = strControllerSQL + ' Where ID = ' + self.__mControllerID
        MdlConnection.CN.execute(strControllerSQL)
        
        MainFields = 'ControllerID, LastReadTime' + MainFields
        MainVals = self.__mControllerID + ', \'' + ShortDate(mdl_Common.NowGMT(), True, True) + '\' ' + MainVals
        
        if ChannelNum > 0 and strSetParams != '':
            strSetParams = Right(strSetParams, Len(strSetParams) - 2)
            strChannelSQL = 'Update TblControllerChannels SET ' + strSetParams + ' Where ControllerID = ' + str(self.__mControllerID) + ' AND ChannelNum = ' + ChannelNum
            MdlConnection.CN.execute(strChannelSQL)
        self.UpdateMachineStatus
        
        if not ( self.ActiveJob is None )  and  ( self.TotalCycles - self.TotalCyclesLast )  >= 0:
            if self.CalcCycleTime == True:
                fCalcCycleTime(self)
            
            self.CalcAutomaticRejects
            
            if self.RunJobDetailsCalc == True:
                
                self.ActiveJob.DetailsCalc(True, pCalcMaterial)
            
            strControllerSQL = 'Update TblControllers SET LastCalcTime = \'' + ShortDate(self.LastCalcTime, True, True) + '\' Where ID = ' + self.__mControllerID
            MdlConnection.CN.execute(strControllerSQL)
        
        returnVal = True
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:fWriteMainData', '' + Err.Number, '' + Err.Description, 'MID = ' + self.str(__mID))
            Err.Clear()
            
        tParam = None
        return returnVal

    def CalcAutomaticRejects(self):
        tCounter = 0

        tParam = None

        LDStat = False
        
        for tCounter in range(0, self.__mCParams.Count):
            tParam = self.__mCParams(tCounter)
            if tParam.RejectReasonID > 0:
                LDStat = self.__mCParams.Item(tCounter).CalcRejectsRead()
        if Err.Number != 0:
            RecordError('Machine:CalcAutomaticRejects', '' + Err.Number, '' + Err.Description, 'MachineID = ' + self.ID)
            Err.Clear()

    def UpdateMachineStatus(self):
        strSQL = ''
        
        
        strSQL = 'Update TblMachines Set MachineStatus = ' + self.Status + ', NoProgressCount = ' + self.__mNoProgressCount + ' Where ID=' + self.ID
        MdlConnection.CN.execute(strSQL)
        if not IsNull(self.ActiveJobID) and  ( self.ActiveJobID != 0 ) :
            strSQL = 'Update TblJob Set MachineStatus = ' + self.Status + ' Where ID = ' + self.ActiveJobID
            MdlConnection.CN.execute(strSQL)
            strSQL = 'Update TblJobCurrent Set MachineStatus = ' + self.Status + ' Where ID = ' + self.ActiveJobID
            MdlConnection.CN.execute(strSQL)
        if not ( self.ActiveJob is None ) :
            self.ActiveJob.MachineStatus = int(self.__mStatus)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:UpdateMachineStatus', '' + Err.Number, '' + Err.Description, 'MachineID = ' + self.ID)
            Err.Clear()

    def UpdateParamLimits(self, FName, dMean, dPUCL, dPLCL, dQUCL, dQLCL, UpdateRecipe=False):
        returnVal = None
        Counter = 0

        temp = False

        FieldFound = False
        
        returnVal = False
        temp = False
        FieldFound = False
        for Counter in range(0, self.__mCParams.Count):
            if self.__mCParams.Item(Counter).FName == FName:
                temp = self.__mCParams.Item(Counter).UpdateLimits(dMean, dPUCL, dPLCL, dQUCL, dQLCL, UpdateRecipe)
                FieldFound = True
        if FieldFound == False and self.__mHasBatchParams == True:            
            temp = self.__mBatchTrigerP.BatchParams.Item(FName).UpdateLimits(dMean, dPUCL, dPLCL, dQUCL, dQLCL, UpdateRecipe)
        if (FName == 'CycleTime'):
            self.__mCycleTimeStandard = dMean
        
        if FieldFound == True:
            returnVal = temp
        return returnVal

    def IOStatus(self):
        returnVal = None
        strRes = ''

        strCommand = ''
        if self.ID == 38:
            strRes = strRes
        if DateDiff('s', self.__mLastIOTime, mdl_Common.NowGMT()) >= self.__cntDeviceDisableIntervalSec:
            returnVal = 0
        else:
            returnVal = 1
        return returnVal

    def CalculateStatus(self):
        returnVal = None
        strSQL = ''

        ProgressCount = 0

        StopCount = 0

        tParam = None

        EventID = 0

        EventGroupID = 0

        tEvent = RTEvent()

        tVariant = Variant()

        tChildJob = None

        tWorkingEvent = None

        Rst = None

        tEngineEvent = RTEngineEvent()

        ActiveServiceCall = False
        
        
        if self.__mStopCyclesCount > 0:
            StopCount = self.__mStopCyclesCount
        else:
            StopCount = self.__cntStopCyclesCount
        if self.ID == 69:
            StopCount = StopCount

        if self.__mActiveJobID == 0:
            self.__mStatus = 0
            GoTo(CalculateStatusWrite)
        
        self.__mIOStatus = self.IOStatus()
        self.__mTotalCyclesAutoAdvance = self.TotalCyclesAutoAdvance
        if self.__mIOStatus == 1 or self.__mTotalCyclesAutoAdvance:
            
            self.__mIOErrorCount = 0
            self.__mIODownCount = 0
            self.__mIOEnabled = True
            if self.__mDownEventOn == True:
                self.__mDownEventOn = False
            
            if not self.ActiveJob.OpenEvent is None:
                if self.ActiveJob.OpenEvent.EventGroup == 1 and self.ActiveJob.OpenEvent.EventID == 18:
                    if not self.BatchTrigerP is None:
                        
                        if ( self.BatchTrigerP.CitectDeviceType == 1 and self.BatchTrigerP.Quality != 0 )  or self.ConnectedByOPC == False:
                            
                            self.ActiveJob.OpenEvent.EndEvent(False)
                            self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                            self.ActiveJob.OpenEvent = None
                            if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                                for tVariant in self.ActiveJob.PConfigJobs:
                                    tChildJob = tVariant
                                    tChildJob.OpenEvent.EndEvent(True)
                                    tChildJob.OpenEvent = None
                            self.MachineStop = False
        else:
            if self.IsOffline == False:
                self.__mStatus = 4
                
                if not self.ActiveJob.OpenEvent is None:
                    if self.ActiveJob.OpenEvent.EventID != 18 and self.ActiveJob.OpenEvent.EventID != 100 and self.ProductionModeID < 2 and not self.ActiveJob.OpenEvent.IsCalendarEvent:
                        if DateDiff('n', self.ActiveJob.OpenEvent.EventTime, mdl_Common.NowGMT()) <= 1:
                            self.ActiveJob.OpenEvent.EventID = 18
                            self.ActiveJob.OpenEvent.EventGroup = 1
                            strSQL = ''
                            strSQL = strSQL + 'UPDATE TblEvent SET' + vbCrLf
                            strSQL = strSQL + 'Event = 18,' + vbCrLf
                            strSQL = strSQL + 'EventGroup = 1' + vbCrLf
                            strSQL = strSQL + 'WHERE ID = ' + self.ActiveJob.OpenEvent.ID
                            MdlConnection.CN.execute(( strSQL ))
                        else:
                            self.ActiveJob.OpenEvent.EndEvent(True)
                            self.ActiveJob.OpenEvent = None
                            if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                                for tVariant in self.ActiveJob.PConfigJobs:
                                    tChildJob = tVariant
                                    tChildJob.OpenEvent.EndEvent(True)
                                    tChildJob.OpenEvent = None
                            tEvent = RTEvent()
                            tEvent.Create(self, 1, 18, '', self.ActiveJob)
                            self.ActiveJob.OpenEvent = tEvent
                        self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                    
                    self.__mNoProgressCount = DateDiff('s', self.__mLastProgressTime, mdl_Common.NowGMT())
                    if GetParam('NoProgressCount', tParam) == True:
                        tParam.LastValue = self.__mNoProgressCount
                        self.__mCParams.Item('NoProgressCount').GetListData
                    GoTo(CalculateStatusWrite)
                
        if (self.TotalCycles > self.TotalCyclesLast or  ( self.__mStopSignalExist == True and self.__mMachineSignalStop == False and self.__mIOStatus == 1 )) and  ( ( not self.ProductionModeDisableProductionTime and self.ProductionModeID > 1 ) or  ( self.ProductionModeID == 1 and  ( not self.ProductionModeDisableProductionTime or  ( self.ActiveJob.JobDef > 0 and not self.ActiveJob.JobDefDisableProductionTime )))) :
            self.__mNoProgressCount = 0
            if GetParam('NoProgressCount', tParam) == True:
                tParam.LastValue = self.__mNoProgressCount
                self.__mCParams.Item('NoProgressCount').GetListData
            self.__mProgress = self.__mProgress + DateDiff('s', self.__mLastProgressTime, mdl_Common.NowGMT())
            self.__mLastProgressTime = mdl_Common.NowGMT()
            
            
            
            if ( self.__mMachineStop == True or not self.ActiveJob.OpenEvent is None )  and  ( self.NewJob == False or self.MonitorSetupWorkingTime ) :
                if not ( self.ActiveJob.OpenEvent is None ) :
                    
                    self.ActiveJob.OpenEvent.EndEvent(True, VBGetMissingArgument(self.ActiveJob.OpenEvent.EndEvent, 1), self.MachineSignalStopTimestamp)
                    self.ActiveJob.OpenEvent = None
                    self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                    if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                        for tVariant in self.ActiveJob.PConfigJobs:
                            tChildJob = tVariant
                            
                            tChildJob.OpenEvent.EndEvent(True, VBGetMissingArgument(tChildJob.OpenEvent.EndEvent, 1), self.MachineSignalStopTimestamp)
                            tChildJob.OpenEvent = None
                
                self.IgnoreCycleTimeFilter = True
            
            
            if self.__mMachineStop == True and self.NewJob == True and self.MonitorSetupWorkingTime == False:
                self.IgnoreCycleTimeFilter = True
            self.__mMachineStop = False
            if AlarmOnProgressInterval > 0:
                if self.__mProgress >=  ( self.__mCycleTimeStandard * AlarmOnProgressInterval ) :
                    if self.__mNewJob == True:
                        self.__mNewJob = False
                        self.ActiveJob.EndSetUp(100)
                        self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                    
            else:
                if self.NewJob == True and self.MonitorSetupWorkingTime == False:
                    if self.ActiveJob.OpenEvent is None:
                        tEvent = RTEvent()
                        tEvent.Create(self, 10, 100, 'Setup', self.ActiveJob)
                        self.ActiveJob.OpenEvent = tEvent
                        self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
        else:            
            self.__mNoProgressCount = DateDiff('s', self.__mLastProgressTime, mdl_Common.NowGMT())
            if GetParam('NoProgressCount', tParam) == True:
                tParam.LastValue = self.__mNoProgressCount
                self.__mCParams.Item('NoProgressCount').GetListData
            
            if CheckNoProgressCount or ( self.ProductionModeDisableProductionTime and self.ProductionModeID > 1 ) or  ( self.ProductionModeID == 1 and  ( self.ProductionModeDisableProductionTime or  ( self.ActiveJob.JobDef > 0 and self.ActiveJob.JobDefDisableProductionTime))):
                self.__mStatus = 3
                if self.__mStatusParamSet == True:
                    self.__mStatusParam.LastValue = self.__mStatus
                self.__mMachineStop = self.__mCParams.Item('Status').GetListData()
                
                self.__mMachineStop = True
                self.__mMachineSignalStop = True
                self.__mMachineStop = True
                self.__mProgress = 0
                
                
                if self.NewJob == False:
                    
                    if self.IsOffline == False:
                        
                        ActiveServiceCall = False
                        if self.ReportStopReasonByOpenCall and self.ProductionModeID < 2:
                            strSQL = ''
                            strSQL = strSQL + 'SELECT TOP 1 EventGroupID, EventReasonID' + vbCrLf
                            strSQL = strSQL + 'FROM ViewNotificationsOpenCalls' + vbCrLf
                            strSQL = strSQL + 'WHERE SentTime >= DateAdd(d, -7, CONVERT(VarChar(10), GETDATE(), 121))' + vbCrLf
                            strSQL = strSQL + 'AND SourceMachineID = ' + self.ID + ' AND EventReasonID > 0' + vbCrLf
                            strSQL = strSQL + 'ORDER BY SentTime DESC'
                            Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                            Rst.ActiveConnection = None
                            if Rst.RecordCount == 1:
                                ActiveServiceCall = True
                            else:
                                ActiveServiceCall = False
                            RstCursor.close()
                        if self.GetParam('LastEventID', tParam) == True and self.ProductionModeID < 2 and not ActiveServiceCall:
                            if MdlADOFunctions.fGetRstValLong(tParam.LastValue) != 0 and tParam.IOStatus == 1:
                                EventID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('EventID', 'STblEventDesrControllerValues', 'MachineID = ' + self.ID + ' AND ControllerValue = ' + MdlADOFunctions.fGetRstValLong(tParam.LastValue), 'CN'))
                                if EventID != 0:
                                    EventGroupID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('EventGroupID', 'STblEventDesr', 'ID = ' + EventID, 'CN'))
                                    if self.ActiveJob.OpenEvent is None:
                                        tEvent = RTEvent()
                                        
                                        tEvent.Create(self, EventGroupID, EventID, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), VBGetMissingArgument(tEvent.Create, 6), self.MachineSignalStopTimestamp)
                                        self.ActiveJob.OpenEvent = tEvent
                                        self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                                    else:
                                        self.ActiveJob.OpenEvent.EventID = EventID
                                        self.ActiveJob.OpenEvent.EventGroup = EventGroupID
                                        strSQL = ''
                                        strSQL = strSQL + 'UPDATE TblEvent SET' + vbCrLf
                                        strSQL = strSQL + 'Event = ' + EventID + ',' + vbCrLf
                                        strSQL = strSQL + 'EventGroup = ' + EventGroupID + vbCrLf
                                        strSQL = strSQL + 'WHERE ID = ' + self.ActiveJob.OpenEvent.ID
                                        MdlConnection.CN.execute(( strSQL ))
                                else:
                                    self.GetStopReasonAndCreateEvent
                            else:
                                self.GetStopReasonAndCreateEvent
                        else:
                            if self.ActiveJob.OpenEvent is None:
                                tEvent = RTEvent()
                                
                                if not self.BatchTrigerP is None:
                                    
                                    if ( self.BatchTrigerP.CitectDeviceType == 1 and self.BatchTrigerP.Quality == 0 )  or  ( self.ConnectedByOPC == False and self.IOStatus() == 0 ) :
                                        
                                        if self.ProductionModeReasonID != 0 and self.ProductionModeID > 1:
                                            tEvent.Create(self, self.ProductionModeGroupReasonID, self.ProductionModeReasonID, '', self.ActiveJob)
                                        else:
                                            tEvent.Create(self, 1, 18, '', self.ActiveJob)
                                    else:
                                        self.GetStopReasonAndCreateEvent
                                else:
                                    self.GetStopReasonAndCreateEvent
                                if not tEvent is None:
                                    if tEvent.ID > 0:
                                        self.ActiveJob.OpenEvent = tEvent
                                        self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                        
                else:
                    if self.ActiveJob.OpenEvent is None:
                        tEvent = RTEvent()
                        tEvent.Create(self, 10, 100, 'Setup', self.ActiveJob)
                        self.ActiveJob.OpenEvent = tEvent
                        self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
            else:
                if self.__mMachineStop == False:
                    self.__mNoProgressCount = 0
                    if GetParam('NoProgressCount', tParam) == True:
                        tParam.LastValue = self.__mNoProgressCount
                        self.__mCParams.Item('NoProgressCount').GetListData
                else:
                    if self.GetParam('LastEventID', tParam) == True and self.NewJob == False and self.ProductionModeID < 2:
                        if MdlADOFunctions.fGetRstValLong(tParam.LastValue) != 0 and tParam.IOStatus == 1:
                            EventID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('EventID', 'STblEventDesrControllerValues', 'MachineID = ' + self.ID + ' AND ControllerValue = ' + MdlADOFunctions.fGetRstValLong(tParam.LastValue), 'CN'))
                            if EventID != 0:
                                EventGroupID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('EventGroupID', 'STblEventDesr', 'ID = ' + EventID, 'CN'))
                                if not self.ActiveJob.OpenEvent is None:
                                    self.ActiveJob.OpenEvent.EventID = EventID
                                    self.ActiveJob.OpenEvent.EventGroup = EventGroupID
                                    strSQL = ''
                                    strSQL = strSQL + 'UPDATE TblEvent SET' + vbCrLf
                                    strSQL = strSQL + 'Event = ' + EventID + ',' + vbCrLf
                                    strSQL = strSQL + 'EventGroup = ' + EventGroupID + vbCrLf
                                    strSQL = strSQL + 'WHERE ID = ' + self.ActiveJob.OpenEvent.ID
                                    MdlConnection.CN.execute(( strSQL ))
        
        if self.__mMachineStop == True:
            self.__mStatus = 3
            self.__mMachineSignalStop = True
            GoTo(CalculateStatusWrite)
        
        
        if self.AlarmsOnCount > 0 and self.NewJob == False:
            self.__mStatus = 2
            self.__mMachineSignalStop = False
            GoTo(CalculateStatusWrite)
        self.__mStatus = 1
        self.__mMachineSignalStop = False
        if self.__mStatusParamSet == True:
            self.__mStatusParam.LastValue = self.__mStatus
            
            self.UpdateMachineStatus
        
        if self.ActiveJob is None:
            return returnVal
        if (self.__mStatus == 0) or (self.__mStatus == 3) or (self.__mStatus == 4) or (self.__mStatus == 6) or (self.__mStatus == 7) or (self.__mStatus == 8):
            if not self.ActiveJob.OpenWorkingEvent is None:
                
                self.ActiveJob.OpenWorkingEvent.EndEvent()
                self.ActiveJob.OpenWorkingEvent = None
                if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                    for tVariant in self.ActiveJob.PConfigJobs:
                        tChildJob = tVariant
                        tChildJob.OpenWorkingEvent.EndEvent
                        tChildJob.OpenWorkingEvent = None
        elif (self.__mStatus == 1) or (self.__mStatus == 2) or (self.__mStatus == 5):
            if self.ActiveJob.OpenEvent is None:
                if self.ActiveJob.OpenWorkingEvent is None:
                    
                    tWorkingEvent = RTWorkingEvent()
                    tWorkingEvent.Create(self, CalculateEventDistributionID, '', self.ActiveJob)
                    self.ActiveJob.OpenWorkingEvent = tWorkingEvent
                    self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
                else:
                    
                    if self.ActiveJob.OpenWorkingEvent.EventDistributionID != CalculateEventDistributionID:
                        
                        self.ActiveJob.OpenWorkingEvent.EndEvent()
                        self.ActiveJob.OpenWorkingEvent = None
                        if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                            for tVariant in self.ActiveJob.PConfigJobs:
                                tChildJob = tVariant
                                tChildJob.OpenWorkingEvent.EndEvent
                                tChildJob.OpenWorkingEvent = None
                        
                        tWorkingEvent = RTWorkingEvent()
                        tWorkingEvent.Create(self, CalculateEventDistributionID, '', self.ActiveJob)
                        self.ActiveJob.OpenWorkingEvent = tWorkingEvent
                        self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
            else:
                self.__mStatus = self.__mStatus
        
        if self.EngineSignalExist:
            if self.EngineSignalActive:
                if self.ActiveJob.OpenEngineEvent is None:
                    tEngineEvent = RTEngineEvent()
                    tEngineEvent.Create(self, '', self.ActiveJob)
                    self.ActiveJob.OpenEngineEvent = tEngineEvent
            else:
                if not self.ActiveJob.OpenEngineEvent is None:
                    self.ActiveJob.OpenEngineEvent.EndEvent()
                    self.ActiveJob.OpenEngineEvent = None
                    if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                        for tVariant in self.ActiveJob.PConfigJobs:
                            tChildJob = tVariant
                            tChildJob.OpenEngineEvent.EndEvent
                            tChildJob.OpenEngineEvent = None
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:CalculateStatus', '' + Err.Number, '' + Err.Description, 'MachineID = ' + self.str(__mID))
            Err.Clear()
            
            
        tParam = None
        tEvent = None
        tVariant = None
        tChildJob = None
        if Rst.State == 1:
            RstCursor.close()
        Rst = None
        return returnVal


    def setReportStopReasonByOpenCall(self, value):
        self.__mReportStopReasonByOpenCall = value

    def getReportStopReasonByOpenCall(self):
        returnVal = None
        returnVal = self.__mReportStopReasonByOpenCall
        return returnVal
    ReportStopReasonByOpenCall = property(fset=setReportStopReasonByOpenCall, fget=getReportStopReasonByOpenCall)


    def setEngineSignalActive(self, value):
        self.__mEngineSignalActive = value

    def getEngineSignalActive(self):
        returnVal = None
        returnVal = self.__mEngineSignalActive
        return returnVal
    EngineSignalActive = property(fset=setEngineSignalActive, fget=getEngineSignalActive)


    def setEngineSignalExist(self, value):
        self.__mEngineSignalExist = value

    def getEngineSignalExist(self):
        returnVal = None
        returnVal = self.__mEngineSignalExist
        return returnVal
    EngineSignalExist = property(fset=setEngineSignalExist, fget=getEngineSignalExist)


    def setEngineSignal(self, value):
        self.__mEngineSignal = value

    def getEngineSignal(self):
        returnVal = None
        returnVal = self.__mEngineSignal
        return returnVal
    EngineSignal = property(fset=setEngineSignal, fget=getEngineSignal)


    def setActiveCalendarEventProductionModeID(self, value):
        self.__mActiveCalendarEventProductionModeID = value

    def getActiveCalendarEventProductionModeID(self):
        returnVal = None
        returnVal = self.__mActiveCalendarEventProductionModeID
        return returnVal
    ActiveCalendarEventProductionModeID = property(fset=setActiveCalendarEventProductionModeID, fget=getActiveCalendarEventProductionModeID)


    def setActiveCalendarEvent(self, value):
        self.__mActiveCalendarEvent = value

    def getActiveCalendarEvent(self):
        returnVal = None
        returnVal = self.__mActiveCalendarEvent
        return returnVal
    ActiveCalendarEvent = property(fset=setActiveCalendarEvent, fget=getActiveCalendarEvent)


    def setMachineSignalStopTimestamp(self, value):
        self.__mMachineSignalStopTimestamp = value

    def getMachineSignalStopTimestamp(self):
        returnVal = None
        returnVal = self.__mMachineSignalStopTimestamp
        return returnVal
    MachineSignalStopTimestamp = property(fset=setMachineSignalStopTimestamp, fget=getMachineSignalStopTimestamp)


    def setContinueEventReasonOnShiftChange(self, value):
        self.__mContinueEventReasonOnShiftChange = value

    def getContinueEventReasonOnShiftChange(self):
        returnVal = None
        returnVal = self.__mContinueEventReasonOnShiftChange
        return returnVal
    ContinueEventReasonOnShiftChange = property(fset=setContinueEventReasonOnShiftChange, fget=getContinueEventReasonOnShiftChange)


    def setDisconnectWorkerOnShiftChange(self, value):
        self.__mDisconnectWorkerOnShiftChange = value

    def getDisconnectWorkerOnShiftChange(self):
        returnVal = None
        returnVal = self.__mDisconnectWorkerOnShiftChange
        return returnVal
    DisconnectWorkerOnShiftChange = property(fset=setDisconnectWorkerOnShiftChange, fget=getDisconnectWorkerOnShiftChange)


    def setProductionModeOverCalendarEvent(self, value):
        self.__mProductionModeOverCalendarEvent = value

    def getProductionModeOverCalendarEvent(self):
        returnVal = None
        returnVal = self.__mProductionModeOverCalendarEvent
        return returnVal
    ProductionModeOverCalendarEvent = property(fset=setProductionModeOverCalendarEvent, fget=getProductionModeOverCalendarEvent)


    def setLineFirstMachineID(self, value):
        self.__mLineFirstMachineID = value

    def getLineFirstMachineID(self):
        returnVal = None
        returnVal = self.__mLineFirstMachineID
        return returnVal
    LineFirstMachineID = property(fset=setLineFirstMachineID, fget=getLineFirstMachineID)


    def setLineLastMachineID(self, value):
        self.__mLineLastMachineID = value

    def getLineLastMachineID(self):
        returnVal = None
        returnVal = self.__mLineLastMachineID
        return returnVal
    LineLastMachineID = property(fset=setLineLastMachineID, fget=getLineLastMachineID)


    def setRootEventAttachDurationMin(self, value):
        self.__mRootEventAttachDurationMin = value

    def getRootEventAttachDurationMin(self):
        returnVal = None
        returnVal = self.__mRootEventAttachDurationMin
        return returnVal
    RootEventAttachDurationMin = property(fset=setRootEventAttachDurationMin, fget=getRootEventAttachDurationMin)


    def setLineID(self, value):
        self.__mLineID = value

    def getLineID(self):
        returnVal = None
        returnVal = self.__mLineID
        return returnVal
    LineID = property(fset=setLineID, fget=getLineID)


    def setStatusLastChangeTime(self, value):
        self.__mStatusLastChangeTime = value

    def getStatusLastChangeTime(self):
        returnVal = None
        returnVal = self.__mStatusLastChangeTime
        return returnVal
    StatusLastChangeTime = property(fset=setStatusLastChangeTime, fget=getStatusLastChangeTime)


    def setDefaultCycleTime(self, value):
        self.__mDefaultCycleTime = value

    def getDefaultCycleTime(self):
        returnVal = None
        returnVal = self.__mDefaultCycleTime
        return returnVal
    DefaultCycleTime = property(fset=setDefaultCycleTime, fget=getDefaultCycleTime)


    def setProductionModeCalcEfficiencies(self, value):
        self.__mProductionModeCalcEfficiencies = value

    def getProductionModeCalcEfficiencies(self):
        returnVal = None
        returnVal = self.__mProductionModeCalcEfficiencies
        return returnVal
    ProductionModeCalcEfficiencies = property(fset=setProductionModeCalcEfficiencies, fget=getProductionModeCalcEfficiencies)


    def setProductionModeDisableProductionTime(self, value):
        self.__mProductionModeDisableProductionTime = value

    def getProductionModeDisableProductionTime(self):
        returnVal = None
        returnVal = self.__mProductionModeDisableProductionTime
        return returnVal
    ProductionModeDisableProductionTime = property(fset=setProductionModeDisableProductionTime, fget=getProductionModeDisableProductionTime)


    def setMachineStopSetting(self, value):
        self.__mMachineStopSetting = value

    def getMachineStopSetting(self):
        returnVal = None
        returnVal = self.__mMachineStopSetting
        return returnVal
    MachineStopSetting = property(fset=setMachineStopSetting, fget=getMachineStopSetting)


    def setMachineStopSettingSetPoint(self, value):
        self.__mMachineStopSettingSetPoint = value

    def getMachineStopSettingSetPoint(self):
        returnVal = None
        returnVal = self.__mMachineStopSettingSetPoint
        return returnVal
    MachineStopSettingSetPoint = property(fset=setMachineStopSettingSetPoint, fget=getMachineStopSettingSetPoint)


    def setBatchReadLastRecord(self, value):
        self.__mBatchReadLastRecord = value

    def getBatchReadLastRecord(self):
        returnVal = None
        returnVal = self.__mBatchReadLastRecord
        return returnVal
    BatchReadLastRecord = property(fset=setBatchReadLastRecord, fget=getBatchReadLastRecord)


    def setProductionModeID(self, value):
        self.__mProductionModeID = value

    def getProductionModeID(self):
        returnVal = None
        returnVal = self.__mProductionModeID
        return returnVal
    ProductionModeID = property(fset=setProductionModeID, fget=getProductionModeID)


    def setProductionModeReasonID(self, value):
        self.__mProductionModeReasonID = value

    def getProductionModeReasonID(self):
        returnVal = None
        returnVal = self.__mProductionModeReasonID
        return returnVal
    ProductionModeReasonID = property(fset=setProductionModeReasonID, fget=getProductionModeReasonID)


    def setProductionModeGroupReasonID(self, value):
        self.__mProductionModeGroupReasonID = value

    def getProductionModeGroupReasonID(self):
        returnVal = None
        returnVal = self.__mProductionModeGroupReasonID
        return returnVal
    ProductionModeGroupReasonID = property(fset=setProductionModeGroupReasonID, fget=getProductionModeGroupReasonID)


    def setMonitorSetupWorkingTime(self, value):
        self.__mMonitorSetupWorkingTime = value

    def getMonitorSetupWorkingTime(self):
        returnVal = None
        returnVal = self.__mMonitorSetupWorkingTime
        return returnVal
    MonitorSetupWorkingTime = property(fset=setMonitorSetupWorkingTime, fget=getMonitorSetupWorkingTime)


    def setConnectedByOPC(self, value):
        self.__mConnectedByOPC = value

    def getConnectedByOPC(self):
        returnVal = None
        returnVal = self.__mConnectedByOPC
        return returnVal
    ConnectedByOPC = property(fset=setConnectedByOPC, fget=getConnectedByOPC)


    def setAllowAutoRejectsOnSetup(self, value):
        self.__mAllowAutoRejectsOnSetup = value

    def getAllowAutoRejectsOnSetup(self):
        returnVal = None
        returnVal = self.__mAllowAutoRejectsOnSetup
        return returnVal
    AllowAutoRejectsOnSetup = property(fset=setAllowAutoRejectsOnSetup, fget=getAllowAutoRejectsOnSetup)


    def setDynamicWareHouseLocation(self, value):
        self.__mDynamicWareHouseLocation = value

    def getDynamicWareHouseLocation(self):
        returnVal = None
        returnVal = self.__mDynamicWareHouseLocation
        return returnVal
    DynamicWareHouseLocation = property(fset=setDynamicWareHouseLocation, fget=getDynamicWareHouseLocation)


    def setUpdateAddressOnJobActive(self, value):
        self.__mUpdateAddressOnJobActive = value

    def getUpdateAddressOnJobActive(self):
        returnVal = None
        returnVal = self.__mUpdateAddressOnJobActive
        return returnVal
    UpdateAddressOnJobActive = property(fset=setUpdateAddressOnJobActive, fget=getUpdateAddressOnJobActive)


    def setIsDosingSystem(self, value):
        self.__mIsDosingSystem = value

    def getIsDosingSystem(self):
        returnVal = None
        returnVal = self.__mIsDosingSystem
        return returnVal
    IsDosingSystem = property(fset=setIsDosingSystem, fget=getIsDosingSystem)


    def setAutoPrintLabel(self, value):
        self.__mAutoPrintLabel = value

    def getAutoPrintLabel(self):
        returnVal = None
        returnVal = self.__mAutoPrintLabel
        return returnVal
    AutoPrintLabel = property(fset=setAutoPrintLabel, fget=getAutoPrintLabel)


    def setActivePalletCreationModeID(self, value):
        self.__mActivePalletCreationModeID = value

    def getActivePalletCreationModeID(self):
        returnVal = None
        returnVal = self.__mActivePalletCreationModeID
        return returnVal
    ActivePalletCreationModeID = property(fset=setActivePalletCreationModeID, fget=getActivePalletCreationModeID)


    def setActivePalletInventoryID(self, value):
        self.__mActivePalletInventoryID = value

    def getActivePalletInventoryID(self):
        returnVal = None
        returnVal = self.__mActivePalletInventoryID
        return returnVal
    ActivePalletInventoryID = property(fset=setActivePalletInventoryID, fget=getActivePalletInventoryID)


    def setLocationBatchChangeSetupModeID(self, value):
        self.__mLocationBatchChangeSetupModeID = value

    def getLocationBatchChangeSetupModeID(self):
        returnVal = None
        returnVal = self.__mLocationBatchChangeSetupModeID
        return returnVal
    LocationBatchChangeSetupModeID = property(fset=setLocationBatchChangeSetupModeID, fget=getLocationBatchChangeSetupModeID)


    def setLocationBatchChangeSetupValue(self, value):
        self.LocationBatchChangeSetupValue = value

    def getLocationBatchChangeSetupValue(self):
        returnVal = None
        returnVal = self.__mLocationBatchChangeSetupValue
        return returnVal
    LocationBatchChangeSetupValue = property(fset=setLocationBatchChangeSetupValue, fget=getLocationBatchChangeSetupValue)


    def getCParams(self):
        returnVal = None
        returnVal = self.__mCParams
        return returnVal
    CParams = property(fget=getCParams)


    def setUnitsInCycleType(self, value):
        self.__mUnitsInCycleType = value

    def getUnitsInCycleType(self):
        returnVal = None
        returnVal = self.__mUnitsInCycleType
        return returnVal
    UnitsInCycleType = property(fset=setUnitsInCycleType, fget=getUnitsInCycleType)


    def setCalcDelayPassed(self, value):
        self.__mCalcDelayPassed = value

    def getCalcDelayPassed(self):
        returnVal = None
        if self.StartCalcAfterDelayInSeconds == 0:
            returnVal = True
        else:
            returnVal = self.__mCalcDelayPassed
        return returnVal
    CalcDelayPassed = property(fset=setCalcDelayPassed, fget=getCalcDelayPassed)


    def setValidations(self, value):
        self.__mValidations = value

    def getValidations(self):
        returnVal = None
        returnVal = self.__mValidations
        return returnVal
    Validations = property(fset=setValidations, fget=getValidations)


    def setStartCalcAfterDelayInSeconds(self, value):
        self.__mStartCalcAfterDelayInSeconds = value

    def getStartCalcAfterDelayInSeconds(self):
        returnVal = None
        returnVal = self.__mStartCalcAfterDelayInSeconds
        return returnVal
    StartCalcAfterDelayInSeconds = property(fset=setStartCalcAfterDelayInSeconds, fget=getStartCalcAfterDelayInSeconds)


    def setDSIsActive(self, value):
        self.__mDSIsActive = value

    def getDSIsActive(self):
        returnVal = None
        returnVal = self.__mDSIsActive
        return returnVal
    DSIsActive = property(fset=setDSIsActive, fget=getDSIsActive)


    def setControllerChannels(self, value):
        self.__mControllerChannels = value

    def getControllerChannels(self):
        returnVal = None
        returnVal = self.__mControllerChannels
        return returnVal
    ControllerChannels = property(fset=setControllerChannels, fget=getControllerChannels)


    
    def setRejectsRead(self, the_mRejectsRead):
        
        self.__mRejectsRead = the_mRejectsRead
        if self.__mRejectsRead > self.__mRejectsReadLast:
            self.__mRejectsReadDiff = self.__mRejectsRead - self.__mRejectsReadLast
        else:
            self.__mRejectsReadDiff = 0

    def getRejectsRead(self):
        returnVal = None
        
        returnVal = self.__mRejectsRead
        return returnVal
    RejectsRead = property(fset=setRejectsRead, fget=getRejectsRead)


    
    def setRejectsReadLast(self, the_mRejectsReadLast):
        
        self.__mRejectsReadLast = the_mRejectsReadLast
        if self.__mRejectsRead > self.__mRejectsReadLast:
            self.__mRejectsReadDiff = self.__mRejectsRead - self.__mRejectsReadLast
        else:
            self.__mRejectsReadDiff = 0

    def getRejectsReadLast(self):
        returnVal = None
        
        returnVal = self.__mRejectsReadLast
        return returnVal
    RejectsReadLast = property(fset=setRejectsReadLast, fget=getRejectsReadLast)


    
    def setRejectsReadOption(self, the_mRejectsReadOption):
        self.RejectsReadOption = the_mRejectsReadOption

    def getRejectsReadOption(self):
        returnVal = None
        returnVal = self.__mRejectsReadOption
        return returnVal
    RejectsReadOption = property(fset=setRejectsReadOption, fget=getRejectsReadOption)


    
    def setUnitsReportedOKOption(self, the_mUnitsReportedOKOption):
        self.UnitsReportedOKOption = the_mUnitsReportedOKOption

    def getUnitsReportedOKOption(self):
        returnVal = None
        returnVal = self.__mUnitsReportedOKOption
        return returnVal
    UnitsReportedOKOption = property(fset=setUnitsReportedOKOption, fget=getUnitsReportedOKOption)


    
    def setIgnoreCycleTimeFilter(self, the_mIgnoreCycleTimeFilter):
        self.__mIgnoreCycleTimeFilter = the_mIgnoreCycleTimeFilter

    def getIgnoreCycleTimeFilter(self):
        returnVal = None
        returnVal = self.__mIgnoreCycleTimeFilter
        return returnVal
    IgnoreCycleTimeFilter = property(fset=setIgnoreCycleTimeFilter, fget=getIgnoreCycleTimeFilter)


    
    def setMachineStop(self, value):
        self.__mMachineStop = value

    def getMachineStop(self):
        returnVal = None
        returnVal = self.__mMachineStop
        return returnVal
    MachineStop = property(fset=setMachineStop, fget=getMachineStop)


    
    def setEnableAlarmsDuringSetup(self, the_mEnableAlarmsDuringSetup):
        self.__mEnableAlarmsDuringSetup = the_mEnableAlarmsDuringSetup

    def getEnableAlarmsDuringSetup(self):
        returnVal = None
        returnVal = self.__mEnableAlarmsDuringSetup
        return returnVal
    EnableAlarmsDuringSetup = property(fset=setEnableAlarmsDuringSetup, fget=getEnableAlarmsDuringSetup)


    
    def setEnableAlarmsDuringMachineStop(self, the_mEnableAlarmsDuringMachineStop):
        self.__mEnableAlarmsDuringMachineStop = the_mEnableAlarmsDuringMachineStop

    def getEnableAlarmsDuringMachineStop(self):
        returnVal = None
        returnVal = self.__mEnableAlarmsDuringMachineStop
        return returnVal
    EnableAlarmsDuringMachineStop = property(fset=setEnableAlarmsDuringMachineStop, fget=getEnableAlarmsDuringMachineStop)


    
    def setIsOffline(self, the_mIsOffline):
        self.__mIsOffline = the_mIsOffline

    def getIsOffline(self):
        returnVal = None
        returnVal = self.__mIsOffline
        return returnVal
    IsOffline = property(fset=setIsOffline, fget=getIsOffline)


    
    def setCalcChannel100MaterialByCavity(self, the_mCalcChannel100MaterialByCavity):
        self.__mCalcChannel100MaterialByCavity = the_mCalcChannel100MaterialByCavity

    def getCalcChannel100MaterialByCavity(self):
        returnVal = None
        returnVal = self.__mCalcChannel100MaterialByCavity
        return returnVal
    CalcChannel100MaterialByCavity = property(fset=setCalcChannel100MaterialByCavity, fget=getCalcChannel100MaterialByCavity)


    
    def setPConfigJobs(self, x, y, the_mPConfigJobs):
        self.__mPConfigJobs[x, y] = the_mPConfigJobs

    def getPConfigJobs(self, x, y):
        returnVal = None
        returnVal = self.__mPConfigJobs(x, y)
        return returnVal
    PConfigJobs = property(fset=setPConfigJobs, fget=getPConfigJobs)


    
    def setPConfigJobsInjections(self, x, y, the_mPConfigJobsInjections):
        self.__mPConfigJobsInjections[x, y] = the_mPConfigJobsInjections

    def getPConfigJobsInjections(self, x, y):
        returnVal = None
        returnVal = self.__mPConfigJobsInjections(x, y)
        return returnVal
    PConfigJobsInjections = property(fset=setPConfigJobsInjections, fget=getPConfigJobsInjections)


    
    def setPConfigLastJobIDProgressed(self, the_mPConfigLastJobIDProgressed):
        self.__mPConfigLastJobIDProgressed = the_mPConfigLastJobIDProgressed

    def getPConfigLastJobIDProgressed(self):
        returnVal = None
        returnVal = self.__mPConfigLastJobIDProgressed
        return returnVal
    PConfigLastJobIDProgressed = property(fset=setPConfigLastJobIDProgressed, fget=getPConfigLastJobIDProgressed)


    def setAlarmsOnCount(self, value):
        self.__mAlarmsOnCount = value

    def getAlarmsOnCount(self):
        returnVal = None
        if not self.ActiveJob is None:
            if not self.ActiveJob.OpenAlarms is None:
                returnVal = self.ActiveJob.OpenAlarms.Count
            else:
                returnVal = 0
        else:
            returnVal = self.__mAlarmsOnCount
        return returnVal
    AlarmsOnCount = property(fset=setAlarmsOnCount, fget=getAlarmsOnCount)


    
    def setPConfigJobsArrSize(self, the_mPConfigJobsArrSize):
        self.__mPConfigJobsArrSize = the_mPConfigJobsArrSize

    def getPConfigJobsArrSize(self):
        returnVal = None
        returnVal = self.__mPConfigJobsArrSize
        return returnVal
    PConfigJobsArrSize = property(fset=setPConfigJobsArrSize, fget=getPConfigJobsArrSize)


    
    def setPConfigJobIDCyclesProgressed(self, the_mPConfigJobIDCyclesProgressed):
        self.__mPConfigJobIDCyclesProgressed = the_mPConfigJobIDCyclesProgressed

    def getPConfigJobIDCyclesProgressed(self):
        returnVal = None
        returnVal = self.__mPConfigJobIDCyclesProgressed
        return returnVal
    PConfigJobIDCyclesProgressed = property(fset=setPConfigJobIDCyclesProgressed, fget=getPConfigJobIDCyclesProgressed)


    
    def setTotalCyclesAutoAdvance(self, the_mTotalCyclesAutoAdvance):
        self.__mTotalCyclesAutoAdvance = the_mTotalCyclesAutoAdvance

    def getTotalCyclesAutoAdvance(self):
        returnVal = None
        returnVal = self.__mTotalCyclesAutoAdvance
        return returnVal
    TotalCyclesAutoAdvance = property(fset=setTotalCyclesAutoAdvance, fget=getTotalCyclesAutoAdvance)


    
    def setWeightDistanceRatioReset(self, the_mWeightDistanceRatioReset):
        self.__mWeightDistanceRatioReset = the_mWeightDistanceRatioReset

    def getWeightDistanceRatioReset(self):
        returnVal = None
        returnVal = self.__mWeightDistanceRatioReset
        return returnVal
    WeightDistanceRatioReset = property(fset=setWeightDistanceRatioReset, fget=getWeightDistanceRatioReset)


    
    def setManualRead(self, the_mManualRead):
        self.__mManualRead = the_mManualRead

    def getManualRead(self):
        returnVal = None
        returnVal = self.__mManualRead
        return returnVal
    ManualRead = property(fset=setManualRead, fget=getManualRead)


    
    def setIsBatchUpdatePP(self, the_mIsBatchUpdatePP):
        self.__mIsBatchUpdatePP = the_mIsBatchUpdatePP

    def getIsBatchUpdatePP(self):
        returnVal = None
        returnVal = self.__mIsBatchUpdatePP
        return returnVal
    IsBatchUpdatePP = property(fset=setIsBatchUpdatePP, fget=getIsBatchUpdatePP)


    
    def setUPDController(self, the_mUPDController):
        self.__mUPDController = the_mUPDController

    def getUPDController(self):
        returnVal = None
        returnVal = self.__mUPDController
        return returnVal
    UPDController = property(fset=setUPDController, fget=getUPDController)


    
    def setReportRejectsUnReported(self, the_mReportRejectsUnReported):
        self.__mReportRejectsUnReported = the_mReportRejectsUnReported

    def getReportRejectsUnReported(self):
        returnVal = None
        returnVal = self.__mReportRejectsUnReported
        return returnVal
    ReportRejectsUnReported = property(fset=setReportRejectsUnReported, fget=getReportRejectsUnReported)


    
    def setRunJobDetailsCalc(self, the_mRunJobDetailsCalc):
        self.__mRunJobDetailsCalc = the_mRunJobDetailsCalc

    def getRunJobDetailsCalc(self):
        returnVal = None
        returnVal = self.__mRunJobDetailsCalc
        return returnVal
    RunJobDetailsCalc = property(fset=setRunJobDetailsCalc, fget=getRunJobDetailsCalc)


    
    def setAlertOnStopSuction(self, the_mAlertOnStopSuction):
        self.__mAlertOnStopSuction = the_mAlertOnStopSuction

    def getAlertOnStopSuction(self):
        returnVal = None
        returnVal = self.__mAlertOnStopSuction
        return returnVal
    AlertOnStopSuction = property(fset=setAlertOnStopSuction, fget=getAlertOnStopSuction)


    
    def setCalcCycleTime(self, the_mCalcCycleTime):
        self.__mCalcCycleTime = the_mCalcCycleTime

    def getCalcCycleTime(self):
        returnVal = None
        returnVal = self.__mCalcCycleTime
        return returnVal
    CalcCycleTime = property(fset=setCalcCycleTime, fget=getCalcCycleTime)


    
    def setReseTotalCycles(self, the_mReseTotalCycles):
        self.__mReseTotalCycles = the_mReseTotalCycles

    def getReseTotalCycles(self):
        returnVal = None
        returnVal = self.__mReseTotalCycles
        return returnVal
    ReseTotalCycles = property(fset=setReseTotalCycles, fget=getReseTotalCycles)


    
    def setMaxCycleTime(self, the_mMaxCycleTime):
        self.__mMaxCycleTime = the_mMaxCycleTime

    def getMaxCycleTime(self):
        returnVal = None
        returnVal = self.__mMaxCycleTime
        return returnVal
    MaxCycleTime = property(fset=setMaxCycleTime, fget=getMaxCycleTime)


    
    def setProductWeight(self, the_mProductWeight):
        self.__mProductWeight = the_mProductWeight

    def getProductWeight(self):
        returnVal = None
        returnVal = self.__mProductWeight
        return returnVal
    ProductWeight = property(fset=setProductWeight, fget=getProductWeight)


    
    def setStopSignalExist(self, the_mStopSignalExist):
        self.__mStopSignalExist = the_mStopSignalExist

    def getStopSignalExist(self):
        returnVal = None
        returnVal = self.__mStopSignalExist
        return returnVal
    StopSignalExist = property(fset=setStopSignalExist, fget=getStopSignalExist)


    
    def setStopSignal(self, the_mStopSignal):
        self.__mStopSignal = the_mStopSignal

    def getStopSignal(self):
        returnVal = None
        returnVal = self.__mStopSignal
        return returnVal
    StopSignal = property(fset=setStopSignal, fget=getStopSignal)


    
    def setStopCyclesCount(self, the_mStopCyclesCount):
        self.__mStopCyclesCount = the_mStopCyclesCount

    def getStopCyclesCount(self):
        returnVal = None
        returnVal = self.__mStopCyclesCount
        return returnVal
    StopCyclesCount = property(fset=setStopCyclesCount, fget=getStopCyclesCount)


    
    def setCycleTimeFilter(self, the_mCycleTimeFilter):
        self.__mCycleTimeFilter = the_mCycleTimeFilter

    def getCycleTimeFilter(self):
        returnVal = None
        returnVal = self.__mCycleTimeFilter
        return returnVal
    CycleTimeFilter = property(fset=setCycleTimeFilter, fget=getCycleTimeFilter)


    
    def setIPCProductWeightCountRatio(self, the_mIPCProductWeightCountRatio):
        self.__mIPCProductWeightCountRatio = the_mIPCProductWeightCountRatio

    def getIPCProductWeightCountRatio(self):
        returnVal = None
        returnVal = self.__mIPCProductWeightCountRatio
        return returnVal
    IPCProductWeightCountRatio = property(fset=setIPCProductWeightCountRatio, fget=getIPCProductWeightCountRatio)


    
    def setSetUpEndGeneralCycles(self, the_mSetUpEndGeneralCycles):
        self.__mSetUpEndGeneralCycles = the_mSetUpEndGeneralCycles

    def getSetUpEndGeneralCycles(self):
        returnVal = None
        returnVal = self.__mSetUpEndGeneralCycles
        return returnVal
    SetUpEndGeneralCycles = property(fset=setSetUpEndGeneralCycles, fget=getSetUpEndGeneralCycles)


    
    def setSetUpEndProductWeightCycles(self, the_mSetUpEndProductWeightCycles):
        self.__mSetUpEndProductWeightCycles = the_mSetUpEndProductWeightCycles

    def getSetUpEndProductWeightCycles(self):
        returnVal = None
        returnVal = self.__mSetUpEndProductWeightCycles
        return returnVal
    SetUpEndProductWeightCycles = property(fset=setSetUpEndProductWeightCycles, fget=getSetUpEndProductWeightCycles)


    
    def setSetUpEndCycleTimeCycles(self, the_mSetUpEndCycleTimeCycles):
        self.__mSetUpEndCycleTimeCycles = the_mSetUpEndCycleTimeCycles

    def getSetUpEndCycleTimeCycles(self):
        returnVal = None
        returnVal = self.__mSetUpEndCycleTimeCycles
        return returnVal
    SetUpEndCycleTimeCycles = property(fset=setSetUpEndCycleTimeCycles, fget=getSetUpEndCycleTimeCycles)


    
    def setSetUpEndPWCTRelation(self, the_mSetUpEndPWCTRelation):
        self.__mSetUpEndPWCTRelation = the_mSetUpEndPWCTRelation

    def getSetUpEndPWCTRelation(self):
        returnVal = None
        returnVal = self.__mSetUpEndPWCTRelation
        return returnVal
    SetUpEndPWCTRelation = property(fset=setSetUpEndPWCTRelation, fget=getSetUpEndPWCTRelation)


    
    def setSetupEventIDOnSetupEnd(self, the_mSetupEventIDOnSetupEnd):
        self.__mSetupEventIDOnSetupEnd = the_mSetupEventIDOnSetupEnd

    def getSetupEventIDOnSetupEnd(self):
        returnVal = None
        returnVal = self.__mSetupEventIDOnSetupEnd
        return returnVal
    SetupEventIDOnSetupEnd = property(fset=setSetupEventIDOnSetupEnd, fget=getSetupEventIDOnSetupEnd)


    
    def setSetupEventIDOnShiftEnd(self, the_mSetupEventIDOnShiftEnd):
        self.__mSetupEventIDOnShiftEnd = the_mSetupEventIDOnShiftEnd

    def getSetupEventIDOnShiftEnd(self):
        returnVal = None
        returnVal = self.__mSetupEventIDOnShiftEnd
        return returnVal
    SetupEventIDOnShiftEnd = property(fset=setSetupEventIDOnShiftEnd, fget=getSetupEventIDOnShiftEnd)


    
    def setProgress(self, the_mProgress):
        self.__mProgress = the_mProgress

    def getProgress(self):
        returnVal = None
        returnVal = self.__mProgress
        return returnVal
    Progress = property(fset=setProgress, fget=getProgress)


    
    def setAutoJobStartTimeCyclesWork(self, the_mAutoJobStartTimeCyclesWork):
        self.__mAutoJobStartTimeCyclesWork = the_mAutoJobStartTimeCyclesWork

    def getAutoJobStartTimeCyclesWork(self):
        returnVal = None
        returnVal = self.__mAutoJobStartTimeCyclesWork
        return returnVal
    AutoJobStartTimeCyclesWork = property(fset=setAutoJobStartTimeCyclesWork, fget=getAutoJobStartTimeCyclesWork)


    
    def setAutoJobStartOnUnitsOverTarget(self, the_mAutoJobStartOnUnitsOverTarget):
        self.__mAutoJobStartOnUnitsOverTarget = the_mAutoJobStartOnUnitsOverTarget

    def getAutoJobStartOnUnitsOverTarget(self):
        returnVal = None
        returnVal = self.__mAutoJobStartOnUnitsOverTarget
        return returnVal
    AutoJobStartOnUnitsOverTarget = property(fset=setAutoJobStartOnUnitsOverTarget, fget=getAutoJobStartOnUnitsOverTarget)


    
    def setMachineSignalStop(self, the_mMachineSignalStop):
        self.__mMachineSignalStop = the_mMachineSignalStop

    def getMachineSignalStop(self):
        returnVal = None
        returnVal = self.__mMachineSignalStop
        return returnVal
    MachineSignalStop = property(fset=setMachineSignalStop, fget=getMachineSignalStop)


    
    def setMaterialCalc(self, the_mMaterialCalc):
        self.__mMaterialCalc = the_mMaterialCalc

    def getMaterialCalc(self):
        returnVal = None
        returnVal = self.__mMaterialCalc
        return returnVal
    MaterialCalc = property(fset=setMaterialCalc, fget=getMaterialCalc)


    
    def setCycleFilterHValue(self, the_mCycleFilterHValue):
        self.__mCycleFilterHValue = the_mCycleFilterHValue

    def getCycleFilterHValue(self):
        returnVal = None
        returnVal = self.__mCycleFilterHValue
        return returnVal
    CycleFilterHValue = property(fset=setCycleFilterHValue, fget=getCycleFilterHValue)


    
    def setCycleFilterLValue(self, the_mCycleFilterLValue):
        self.__mCycleFilterLValue = the_mCycleFilterLValue

    def getCycleFilterLValue(self):
        returnVal = None
        returnVal = self.__mCycleFilterLValue
        return returnVal
    CycleFilterLValue = property(fset=setCycleFilterLValue, fget=getCycleFilterLValue)


    
    def setID(self, the_mID):
        self.__mID = the_mID

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    
    def setTypeId(self, the_mTypeId):
        self.__mTypeID = the_mTypeId

    def getTypeId(self):
        returnVal = None
        returnVal = self.__mTypeID
        return returnVal
    TypeID = property(fset=setTypeId, fget=getTypeId)


    
    def setLName(self, the_mLName):
        self.__mLName = the_mLName

    def getLName(self):
        returnVal = None
        returnVal = self.__mLName
        return returnVal
    LName = property(fset=setLName, fget=getLName)


    
    def setEName(self, the_mEName):
        self.__mEName = the_mEName

    def getEName(self):
        returnVal = None
        returnVal = self.__mEName
        return returnVal
    EName = property(fset=setEName, fget=getEName)


    
    def setDescr(self, the_mDescr):
        self.__mDescr = the_mDescr

    def getDescr(self):
        returnVal = None
        returnVal = self.__mDescr
        return returnVal
    Descr = property(fset=setDescr, fget=getDescr)


    
    def setMachineType(self, the_mMachineType):
        self.__mMachineType = the_mMachineType

    def getMachineType(self):
        returnVal = None
        returnVal = self.__mMachineType
        return returnVal
    MachineType = property(fset=setMachineType, fget=getMachineType)


    
    def setStatus(self, the_mStatus):
        self.__mStatus = the_mStatus

    def getStatus(self):
        returnVal = None
        if self.__mStatus == '':
            self.__mStatus = 1
        returnVal = self.__mStatus
        return returnVal
    Status = property(fset=setStatus, fget=getStatus)


    
    def setActiveJobID(self, the_mActiveJobID):
        self.__mActiveJobID = the_mActiveJobID

    def getActiveJobID(self):
        returnVal = None
        returnVal = self.__mActiveJobID
        return returnVal
    ActiveJobID = property(fset=setActiveJobID, fget=getActiveJobID)


    
    def setActiveJob(self, value):
        self.__mActiveJob = value

    def getActiveJob(self):
        returnVal = None
        returnVal = self.__mActiveJob
        return returnVal
    ActiveJob = property(fset=setActiveJob, fget=getActiveJob)


    
    def setActiveJoshID(self, the_mActiveJoshID):
        self.__mActiveJoshID = the_mActiveJoshID

    def getActiveJoshID(self):
        returnVal = None
        returnVal = self.__mActiveJoshID
        return returnVal
    ActiveJoshID = property(fset=setActiveJoshID, fget=getActiveJoshID)


    
    def setActiveJosh(self, value):
        self.__mActiveJosh = value

    def getActiveJosh(self):
        returnVal = None
        returnVal = self.__mActiveJosh
        return returnVal
    ActiveJosh = property(fset=setActiveJosh, fget=getActiveJosh)


    
    def setCycleTimeEffFactor(self, the_mCycleTimeEffFactor):
        self.__mCycleTimeEffFactor = the_mCycleTimeEffFactor

    def getCycleTimeEffFactor(self):
        returnVal = None
        returnVal = self.__mCycleTimeEffFactor
        return returnVal
    CycleTimeEffFactor = property(fset=setCycleTimeEffFactor, fget=getCycleTimeEffFactor)


    
    def setMachineTimeEffFactor(self, the_mMachineTimeEffFactor):
        self.__mMachineTimeEffFactor = the_mMachineTimeEffFactor

    def getMachineTimeEffFactor(self):
        returnVal = None
        returnVal = self.__mMachineTimeEffFactor
        return returnVal
    MachineTimeEffFactor = property(fset=setMachineTimeEffFactor, fget=getMachineTimeEffFactor)


    
    def setRejectsEffFactor(self, the_mRejectsEffFactor):
        self.__mRejectsEffFactor = the_mRejectsEffFactor

    def getRejectsEffFactor(self):
        returnVal = None
        returnVal = self.__mRejectsEffFactor
        return returnVal
    RejectsEffFactor = property(fset=setRejectsEffFactor, fget=getRejectsEffFactor)


    
    def setCavitiesEffFactor(self, the_mCavitiesEffFactor):
        self.__mCavitiesEffFactor = the_mCavitiesEffFactor

    def getCavitiesEffFactor(self):
        returnVal = None
        returnVal = self.__mCavitiesEffFactor
        return returnVal
    CavitiesEffFactor = property(fset=setCavitiesEffFactor, fget=getCavitiesEffFactor)


    
    def setLastJobID(self, the_mLastJobID):
        self.__mLastJobID = the_mLastJobID

    def getLastJobID(self):
        returnVal = None
        returnVal = self.__mLastJobID
        return returnVal
    LastJobID = property(fset=setLastJobID, fget=getLastJobID)


    
    def setMoldEndTimeStatusOption(self, the_mMoldEndTimeStatusOption):
        self.__mMoldEndTimeStatusOption = the_mMoldEndTimeStatusOption

    def getMoldEndTimeStatusOption(self):
        returnVal = None
        returnVal = self.__mMoldEndTimeStatusOption
        return returnVal
    MoldEndTimeStatusOption = property(fset=setMoldEndTimeStatusOption, fget=getMoldEndTimeStatusOption)


    
    def setMoldEndTimeCalcOption(self, the_mMoldEndTimeCalcOption):
        self.__mMoldEndTimeCalcOption = the_mMoldEndTimeCalcOption

    def getMoldEndTimeCalcOption(self):
        returnVal = None
        returnVal = self.__mMoldEndTimeCalcOption
        return returnVal
    MoldEndTimeCalcOption = property(fset=setMoldEndTimeCalcOption, fget=getMoldEndTimeCalcOption)


    
    def setMoldEndTime(self, the_mMoldEndTime):
        self.__mMoldEndTime = the_mMoldEndTime

    def getMoldEndTime(self):
        returnVal = None
        returnVal = self.__mMoldEndTime
        return returnVal
    MoldEndTime = property(fset=setMoldEndTime, fget=getMoldEndTime)


    
    def setDepartment(self, the_mDepartment):
        self.__mDepartment = the_mDepartment

    def getDepartment(self):
        returnVal = None
        returnVal = self.__mDepartment
        return returnVal
    Department = property(fset=setDepartment, fget=getDepartment)


    
    def setControllerDefID(self, the_mControllerDefID):
        self.__mControllerDefID = the_mControllerDefID

    def getControllerDefID(self):
        returnVal = None
        returnVal = self.__mControllerDefID
        return returnVal
    ControllerDefID = property(fset=setControllerDefID, fget=getControllerDefID)


    
    def setControllerID(self, the_mControllerID):
        self.__mControllerID = the_mControllerID

    def getControllerID(self):
        returnVal = None
        returnVal = self.__mControllerID
        return returnVal
    ControllerID = property(fset=setControllerID, fget=getControllerID)


    
    def setIsActive(self, the_mIsActive):
        self.__mIsActive = the_mIsActive

    def getIsActive(self):
        returnVal = None
        returnVal = self.__mIsActive
        return returnVal
    IsActive = property(fset=setIsActive, fget=getIsActive)


    
    def setIsActiveCalendar(self, the_mIsActiveCalendar):
        self.__mIsActiveCalendar = the_mIsActiveCalendar

    def getIsActiveCalendar(self):
        returnVal = None
        returnVal = self.__mIsActiveCalendar
        return returnVal
    IsActiveCalendar = property(fset=setIsActiveCalendar, fget=getIsActiveCalendar)


    
    def setAddRejectsOnSetupEnd(self, the_mAddRejectsOnSetupEnd):
        self.__mAddRejectsOnSetupEnd = the_mAddRejectsOnSetupEnd

    def getAddRejectsOnSetupEnd(self):
        returnVal = None
        returnVal = self.__mAddRejectsOnSetupEnd
        return returnVal
    AddRejectsOnSetupEnd = property(fset=setAddRejectsOnSetupEnd, fget=getAddRejectsOnSetupEnd)


    
    def setLocRow(self, the_mLocRow):
        self.__mLocRow = the_mLocRow

    def getLocRow(self):
        returnVal = None
        returnVal = self.__mLocRow
        return returnVal
    LocRow = property(fset=setLocRow, fget=getLocRow)


    
    def setLocCol(self, the_mLocCol):
        self.__mLocCol = the_mLocCol

    def getLocCol(self):
        returnVal = None
        returnVal = self.__mLocCol
        return returnVal
    LocCol = property(fset=setLocCol, fget=getLocCol)


    
    def setDisplayOrder(self, the_mDisplayOrder):
        self.__mDisplayOrder = the_mDisplayOrder

    def getDisplayOrder(self):
        returnVal = None
        returnVal = self.__mDisplayOrder
        return returnVal
    DisplayOrder = property(fset=setDisplayOrder, fget=getDisplayOrder)


    
    def setMachineLoad(self, the_mMachineLoad):
        self.__mMachineLoad = the_mMachineLoad

    def getMachineLoad(self):
        returnVal = None
        returnVal = self.__mMachineLoad
        return returnVal
    MachineLoad = property(fset=setMachineLoad, fget=getMachineLoad)


    
    def setDownHourCost(self, the_mDownHourCost):
        self.__mDownHourCost = the_mDownHourCost

    def getDownHourCost(self):
        returnVal = None
        returnVal = self.__mDownHourCost
        return returnVal
    DownHourCost = property(fset=setDownHourCost, fget=getDownHourCost)


    
    def setWorkHourCost(self, the_mWorkHourCost):
        self.__mWorkHourCost = the_mWorkHourCost

    def getWorkHourCost(self):
        returnVal = None
        returnVal = self.__mWorkHourCost
        return returnVal
    WorkHourCost = property(fset=setWorkHourCost, fget=getWorkHourCost)


    
    def setCurrentDownTime(self, the_mCurrentDownTime):
        self.__mCurrentDownTime = the_mCurrentDownTime

    def getCurrentDownTime(self):
        returnVal = None
        returnVal = self.__mCurrentDownTime
        return returnVal
    CurrentDownTime = property(fset=setCurrentDownTime, fget=getCurrentDownTime)


    
    def setCurrentDownTimeCost(self, the_mCurrentDownTimeCost):
        self.__mCurrentDownTimeCost = the_mCurrentDownTimeCost

    def getCurrentDownTimeCost(self):
        returnVal = None
        returnVal = self.__mCurrentDownTimeCost
        return returnVal
    CurrentDownTimeCost = property(fset=setCurrentDownTimeCost, fget=getCurrentDownTimeCost)


    
    def setActiveMoldID(self, the_mActiveMoldID):
        self.__mActiveMoldID = the_mActiveMoldID

    def getActiveMoldID(self):
        returnVal = None
        if IsNumeric(self.__mActiveMoldID):
            returnVal = self.__mActiveMoldID
        return returnVal
    ActiveMoldID = property(fset=setActiveMoldID, fget=getActiveMoldID)


    
    def setLastMoldID(self, the_mLastMoldID):
        self.__mLastMoldID = the_mLastMoldID

    def getLastMoldID(self):
        returnVal = None
        if IsNumeric(self.__mLastMoldID):
            returnVal = self.__mLastMoldID
        return returnVal
    LastMoldID = property(fset=setLastMoldID, fget=getLastMoldID)


    
    def setActiveProductID(self, the_mActiveProductID):
        self.__mActiveProductID = the_mActiveProductID

    def getActiveProductID(self):
        returnVal = None
        returnVal = self.__mActiveProductID
        return returnVal
    ActiveProductID = property(fset=setActiveProductID, fget=getActiveProductID)


    
    def setActiveProductLName(self, the_mActiveProductLName):
        self.__mActiveProductLName = the_mActiveProductLName

    def getActiveProductLName(self):
        returnVal = None
        returnVal = self.__mActiveProductLName
        return returnVal
    ActiveProductLName = property(fset=setActiveProductLName, fget=getActiveProductLName)


    
    def setActiveProductEName(self, the_mActiveProductEName):
        self.__mActiveProductEName = the_mActiveProductEName

    def getActiveProductEName(self):
        returnVal = None
        returnVal = self.__mActiveProductEName
        return returnVal
    ActiveProductEName = property(fset=setActiveProductEName, fget=getActiveProductEName)


    def getBatchTrigerP(self):
        returnVal = None
        returnVal = self.__mBatchTrigerP
        return returnVal
    BatchTrigerP = property(fget=getBatchTrigerP)


    def getBatchUpdateP(self):
        returnVal = None
        returnVal = self.__mBatchUpdateP
        return returnVal
    BatchUpdateP = property(fget=getBatchUpdateP)


    def setServer(self, vServer):
        self.__mServer = vServer

    def getServer(self):
        returnVal = None
        returnVal = self.__mServer
        return returnVal
    Server = property(fset=setServer, fget=getServer)


    def setNewJob(self, the_mNewJob):
        self.__mNewJob = the_mNewJob

    def getNewJob(self):
        returnVal = None
        if not self.ActiveJob is None:
            if self.ActiveJob.SetUpEnd != 0:
                returnVal = False
            else:
                returnVal = True
        else:
            returnVal = self.__mNewJob
        return returnVal
    NewJob = property(fset=setNewJob, fget=getNewJob)


    def setTimeLeftHr(self, the_TimeLeftHr):
        self.__mTimeLeftHr = the_TimeLeftHr

    def getTimeLeftHr(self):
        returnVal = None
        returnVal = self.__mTimeLeftHr
        return returnVal
    TimeLeftHr = property(fset=setTimeLeftHr, fget=getTimeLeftHr)


    def ParamVal(self, strParamName):
        returnVal = None
        tParam = None
        
        if self.GetParam(strParamName, tParam) == True:
            returnVal = tParam.LastValue
        return returnVal

    def fCalculateParams(self):
        returnVal = None
        Counter = 0
        
        returnVal = False
        for Counter in range(0, self.__mCParams.Count):
            self.__mCParams.Item(Counter).CalcParam
        returnVal = True
        return returnVal

    def XMLMainCalc(self):
        returnVal = None
        strXML = ''

        strSpecial = ''

        Counter = 0

        tParam = None
        
        for Counter in range(0, self.__mMainList.Count):
            tParam = self.__mMainList.Item(Counter)
            strXML = strXML + tParam.GetXML
        strSpecial = strSpecial + '<AlarmsActive>' + str(self.__mAlarmsActive) + '</AlarmsActive>' + vbCrLf
        strSpecial = strSpecial + '<AlarmsOn>' + str(self.AlarmsOnCount) + '</AlarmsOn>' + vbCrLf
        strSpecial = strSpecial + '<ControllerDefID>' + self.__mControllerDefID + '</ControllerDefID>' + vbCrLf
        strSpecial = strSpecial + '<NoProgressCount>' + str(self.__mNoProgressCount) + '</NoProgressCount>' + vbCrLf
        if not self.ActiveJob is None:
            strSpecial = strSpecial + '<TimeLeftHr>' + str(self.ActiveJob.TimeLeftHr) + '</TimeLeftHr>' + vbCrLf
        else:
            strSpecial = strSpecial + '<TimeLeftHr>' + str(self.__mTimeLeftHr) + '</TimeLeftHr>' + vbCrLf
        strSpecial = strSpecial + '<MoldEndTime>' + str(self.__mMoldEndTime) + '</MoldEndTime>' + vbCrLf
        strSpecial = strSpecial + '<NewJob>' + str(self.NewJob) + '</NewJob>' + vbCrLf
        
        strSpecial = strSpecial + '<IsActiveCalendar>' + str(self.__mIsActiveCalendar) + '</IsActiveCalendar>' + vbCrLf
        
        
        strSpecial = strSpecial + '<dLastReadTime>' + str(self.__mCParams.Item('TotalCycles').dLastReadTime) + '</dLastReadTime>' + vbCrLf
        self.__mMainListXML = '<Machine' + str(self.__mID) + '>' + vbCrLf + strSpecial + strXML + '</Machine' + str(self.__mID) + '>' + vbCrLf
        strSpecial = ''
        if Err.Number != 0:
            RecordError('Machine:XMLMainCalc', str(Err.Number), Err.Description, '')
            Err.Clear()
            
        return returnVal

    def XMLMain(self):
        returnVal = None
        
        returnVal = self.__mMainListXML
        return returnVal

    def XMLCalcAll(self):
        returnVal = None
        
        returnVal = False
        self.XMLMainCalc()
        self.XMLControllerCalc()
        self.XMLChannelCalc()
        
        returnVal = True
        return returnVal

    def XMLControllerCalc(self):
        returnVal = None
        strXML = ''

        strSpecial = ''

        strSQL = ''

        Counter = 0

        tParam = None

        Rst = None
        
        for Counter in range(0, self.__mControllerList.Count):
            tParam = self.__mControllerList.Item(Counter)
            strXML = strXML + tParam.GetXML
        strSpecial = strSpecial + '<AlarmsActive>' + str(self.__mAlarmsActive) + '</AlarmsActive>' + vbCrLf
        strSpecial = strSpecial + '<AlarmsOn>' + str(self.AlarmsOnCount) + '</AlarmsOn>' + vbCrLf
        strSpecial = strSpecial + '<NoProgressCount>' + str(self.__mNoProgressCount) + '</NoProgressCount>' + vbCrLf
        strSpecial = strSpecial + '<MoldEndTime>' + str(self.__mMoldEndTime) + '</MoldEndTime>' + vbCrLf
        strSpecial = strSpecial + '<NewJob>' + str(self.NewJob) + '</NewJob>' + vbCrLf
        
        strSpecial = strSpecial + '<IsActiveCalendar>' + str(self.__mIsActiveCalendar) + '</IsActiveCalendar>' + vbCrLf
        self.__mControllerXML = XmlHeader + vbCrLf + '<Machine ID=\'' + str(self.__mID) + '\'>' + vbCrLf + strSpecial + strXML + '</Machine>' + vbCrLf
        strSQL = 'Select MachineXML, IsActiveCalendar From TblMachines Where ID  = ' + self.ID
        Rst.Open(strSQL, CN, adOpenForwardOnly, adLockPessimistic)
        self.IsActiveCalendar = MdlADOFunctions.fGetRstValBool(RstData.IsActiveCalendar, True)
        RstData.MachineXML = self.__mControllerXML
        Rst.Update()
        RstCursor.close()
        strSpecial = ''
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:XMLControllerCalc', str(Err.Number), Err.Description, '')
            Err.Clear()
            
        if Rst.State != 0:
            RstCursor.close()
        Rst = None
        return returnVal

    def XMLController(self):
        returnVal = None
        
        returnVal = self.__mControllerXML
        return returnVal

    def XMLChannelCalc(self):
        returnVal = None
        strXML = ''

        strSQL = ''

        Counter = 0

        tParam = None

        Rst = None
        
        for Counter in range(0, self.__mChannelList.Count):
            tParam = self.__mChannelList.Item(Counter)
            strXML = strXML + tParam.GetXML
        self.__mChannelXML = XmlHeader + vbCrLf + '<MachineChannel>' + vbCrLf + strXML + vbCrLf + '</MachineChannel>' + vbCrLf
        strSQL = 'Select ChannelXML From TblMachines Where ID  = ' + self.ID
        Rst.Open(strSQL, CN, adOpenForwardOnly, adLockPessimistic)
        RstData.ChannelXML = self.__mChannelXML
        Rst.Update()
        RstCursor.close()
        strXML = ''
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:XMLChannelCalc', str(Err.Number), Err.Description, '')
            Err.Clear()
            
        if Rst.State != 0:
            RstCursor.close()
        Rst = None
        return returnVal

    def XMLChannel(self):
        returnVal = None
        
        returnVal = self.__mChannelXML
        return returnVal

    def XMLAlarmCalc(self):
        returnVal = None
        strXML = ''

        strSQL = ''

        Counter = 0

        tParam = None

        Rst = None

        temp = ''

        strSpecial = ''

        AlarmsXML = ''

        Status = ''

        Limit = 0
        
        for Counter in range(0, self.__mAlarmsOnCount):
            if self.__mAlarmsParamCount(Counter) > 0:
                temp = self.__mAlarmsParams(Counter)
                if self.GetParam(temp, tParam) == True:
                    
                    strXML = strXML + tParam.AlarmXML()
        
        AlarmsXML = XmlHeader + vbCrLf + '<Alarms>' + vbCrLf + strSpecial + strXML + '</Alarms>' + vbCrLf
        
        strSQL = 'Select AlarmsXML From TblMachines Where ID  = ' + self.ID
        Rst.Open(strSQL, CN, adOpenForwardOnly, adLockPessimistic)
        RstData.AlarmsXML = AlarmsXML
        Rst.Update()
        RstCursor.close()
        strXML = ''
        AlarmsXML = ''
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:XMLAlarmCalc', str(Err.Number), Err.Description, '')
            Err.Clear()
            
        if Rst.State != 0:
            RstCursor.close()
        Rst = None
        return returnVal

    def JobLoad(self, JobID, ResetTotals, UpdateController=True, FromINITMachine=False, pFromActivateJob=True):
        returnVal = None
        TRst = None
        Rst = None
        strSQL = ''
        strTemp = ''
        temp = ''
        tParam = None
        i = 0
        strUCL = ''
        strLCL = ''
        strMean = ''
        strQUCL = ''
        strQLCL = ''
        UnitsTarget = ''
        UnitsProduced = 0
        Counter = 0
        CurrentShiftID = ''
        rParam = None
        MainDSID = 0
        DSIsActive = False
        DSActiveDemand = False
        DirectBatchBlender = False
        DownloadRecipeDirectly = False
        ErrCounter = 0
        WDRatioReset = False
        tJob = None
        tJosh = None
        tEvent = None
        tChannel = None
        tVariant = None
        tJoshID = 0
        tChildJob = None
        Counter2 = None
        tBatchParam = None
        ErrCounter = 0

        try:
            if self.ID == 38:
                ErrCounter = ErrCounter

            print('Enter Function JobLoad: JobID=' + str(JobID) + ' | ' + str(mdl_Common.NowGMT()))
            strSQL = 'Select MainDSID, DSIsActive, DSActiveDemand, DirectBatchBlender, DownloadRecipeDirectly From TblMachines Where ID = ' + str(self.__mID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            MainDSID = MdlADOFunctions.fGetRstValLong(RstData.MainDSID)
            DSIsActive = MdlADOFunctions.fGetRstValBool(RstData.DSIsActive, False)
            DSActiveDemand = MdlADOFunctions.fGetRstValBool(RstData.DSActiveDemand, False)
            DirectBatchBlender = MdlADOFunctions.fGetRstValBool(RstData.DirectBatchBlender, False)
            DownloadRecipeDirectly = MdlADOFunctions.fGetRstValBool(RstData.DownloadRecipeDirectly, False)
            RstCursor.close()

            if ResetTotals == True:
                self.fClearControllerFields()
                if self.__mCParams.Item('TotalCycles').FieldDataType == 5:
                    strSQL = 'Update TblControllerFields Set CurrentValue = \'0\' Where MachineID = ' + str(self.__mID) + ' AND FieldName = \'TotalCycles\''
                    MdlConnection.CN.execute(strSQL)
                    self.SetFieldValue('TotalCycles', str(0))
                
                for tParam in self.__mCParams:
                    if tParam.CalcByDiff == True:
                        strSQL = 'Update TblControllerFields Set CurrentValue = \'0\' Where MachineID = ' + str(self.__mID) + ' AND FieldName = \'' + str(tParam.FName) + '\''
                        MdlConnection.CN.execute(strSQL)
                        self.SetFieldValue(tParam.FName, str(0))
                
                MdlOnlineTasks.fResetMachineTriggers(self)
                if JobID > 0:
                    MdlOnlineTasks.MdlOnlineTasks.fInitMachineTriggers(self, JobID, FromINITMachine)
                
                self.fResetDataSamples()
                self.fRemoveDynamicDataSamples()
            if JobID == 0:
                
                if not self.ActiveJob is None:
                    self.ActiveJob.EndJob
                if self.__mActiveJobID != 0:
                    self.__mLastJobID = self.__mActiveJobID
                
                self.ActiveJob = None
                self.ActiveJosh = None
                self.ActiveJobID = 0
                self.ActiveJoshID = 0
                self.Status = 0
                self.MachineSignalStop = False
                self.EngineSignalActive = False
                self.__mNoProgressCount = 0
                if self.GetParam('NoProgressCount', tParam) == True:
                    tParam.LastValue = self.__mNoProgressCount
                    self.__mCParams.Item('NoProgressCount').GetListData
                self.SetFieldValue('Status', str(self.Status))
                self.ActiveJobID = 0
                self.SetFieldValue('WorkOrder', str(self.ActiveJobID))
                self.MoldEndTime = 0
                self.ActiveMoldID = 0
                self.SetFieldValue('MoldID', str(self.ActiveMoldID))
                self.ActiveProductID = 0
                self.MoldActiveCavities = 0
                self.SetFieldValue('MoldCavities', str(self.MoldActiveCavities))
                self.MoldCavities = 0
                self.Rejects = 0
                self.TotalCycles = 0
                self.TotalCyclesLast = 0
                
                self.RejectsRead = 0
                self.RejectsReadLast = 0
                self.CyclesDiff = 0
                self.PConfigJobIDCyclesProgressed = 0
                self.PConfigLastJobIDProgressed = 0
                self.__mPConfigJobs = []
                self.__mPConfigJobsInjections = []
                self.SetFieldValue('TotalCycles', str(self.TotalCycles))
                self.SetFieldValidValue('TotalCycles', str(self.TotalCycles))
                for Counter in range(0, self.__mCParams.Count):
                    tParam = self.__mCParams(Counter)
                    tParam.UpdateLimits('', '', '', '', '')
                    if tParam.FName == 'TotalCycles':
                        tParam.LastValue = tParam.LastValue
                    else:
                        if tParam.CitectDeviceType != 1:
                            tParam.LastValue = ''
                            tParam.LastValidValue = ''
                    if tParam.RejectReasonID > 0:
                        tParam.RejectsA = 0
                        tParam.RejectsALast = 0
                    if tParam.AlarmPerminentAcknowledge == True and pFromActivateJob:
                        tParam.AlarmPerminentAcknowledge = False
                        strSQL = 'Update TblControllerFields SET AlarmPerminentAcknowledge = 0 Where ControllerID = ' + str(self.__mControllerID) + ' AND FieldName = \'' + str(tParam.FName) + '\''
                        MdlConnection.CN.execute(strSQL)
                    if tParam.AlarmCycleAcknowledge == True and pFromActivateJob:
                        tParam.AlarmCycleAcknowledge = False
                        strSQL = 'Update TblControllerFields SET AlarmCylceAcknowledge = 0 Where ControllerID = ' + str(self.__mControllerID) + ' AND FieldName = \'' + str(tParam.FName) + '\''
                        MdlConnection.CN.execute(strSQL)
                    
                    if FromINITMachine == False and  ( 'TTLW' in tParam.FName or 'TotalWeight' in tParam.FName ) and tParam.CitectDeviceType == 1 and tParam.ValidateValue == True:
                        tParam.LastValidValue = '0'
                    if not tParam.BatchParams is None:
                        for Counter2 in range(0, tParam.BatchParams.Count):
                            tBatchParam = tParam.BatchParams(Counter2)
                            if tBatchParam.FName == 'Cnl1MainMatTTLW1':
                                tBatchParam.FName = tBatchParam.FName
                            if FromINITMachine == False and  ( 'TTLW' in tBatchParam.FName or 'TotalWeight' in tBatchParam.FName ) and tBatchParam.DirectRead == True and tBatchParam.ValidateValue == True:
                                tBatchParam.LastValidValue = '0'
                    if tParam.StartCalcAfterDelayInSeconds == 0:
                        tParam.CalcDelayPassed = True
                    else:
                        tParam.CalcDelayPassed = False
                tParam = None
                
                self.ResetTotals
                if self.AlertOnStopSuction:
                    self.SetFieldValue('Cnl1CreateNewBatch', '1')
                if MainDSID > 0 and DSIsActive == True:
                    if DSActiveDemand == True:
                        self.SetFieldValue('Cnl1IsActive', '1')
                    else:
                        self.SetFieldValue('Cnl1IsActive', '0')
                print('Exit Function JobLoad: JobID=' + str(JobID) + ' | ' + mdl_Common.NowGMT())
                return returnVal
            returnVal = False
            
            if pFromActivateJob or FromINITMachine:
                tJob = Job()
                tJob.Init(self, JobID, True, FromINITMachine)                
            else:
                tJob = self.ActiveJob                
                tJob.Refresh()
                
            self.ActiveJob = tJob
            self.ActiveJoshID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblJoshCurrent', 'JobID = ' + str(JobID) + ' AND ShiftID = ' + str(self.Server.CurrentShiftID), 'CN'))
            tJosh = Josh()
            tJosh.Init(tJob, self.ActiveJoshID)

            self.ActiveJob.ActiveJosh = tJosh
            self.ActiveJobID = self.ActiveJob.ID
            self.ActiveJosh = tJosh
            self.ActiveJoshID = self.ActiveJosh.ID
            self.ActiveJob.InitControllerChannels(self.ActiveJosh.ID, pFromActivateJob)
            if self.ActiveJob.PConfigID != 0:
                for tVariant in self.ActiveJob.PConfigJobs:
                    tJob = tVariant
                    tJoshID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblJoshCurrent', 'JobID = ' + tJob.ID + ' AND ShiftID = ' + self.Server.CurrentShiftID, 'CN'))
                    if tJoshID != 0:
                        tJosh = Josh()
                        tJosh.Init(tJob, tJoshID)
                        tJob.ActiveJosh = tJosh
                        tJob.InitControllerChannels(tJoshID, pFromActivateJob)
            self.TotalCycles = self.ActiveJob.InjectionsCount
            print(Fore.GREEN + 'MachineID=' + str(self.ID) + ' ActiveJob.TotalCycles = ' + str(self.ActiveJob.InjectionsCount) + ' | ' + str(mdl_Common.NowGMT()))
            if FromINITMachine == True:
                self.TotalCyclesLast = self.ActiveJob.InjectionsCount
            else:
                self.TotalCyclesLast = self.ActiveJob.InjectionsCountLast
            if self.StartCalcAfterDelayInSeconds == 0:
                self.CalcDelayPassed = True
            else:
                self.CalcDelayPassed = False
            UnitsTarget = self.ActiveJob.UnitsTarget
            self.SetFieldValue('UnitsTarget', UnitsTarget)
            
            temp = MdlADOFunctions.GetSingleValue('MoldEndTime', 'TblMachines', 'ID=' + str(self.__mID))
            if temp != '':
                self.__mMoldEndTime = int(temp)
            strSQL = 'Select * From TblControllerFields Where ControllerID = ' + str(self.__mControllerID)

            TRstCursor = MdlConnection.CN.cursor()
            TRstCursor.execute(strSQL)
            TRstValues = TRstCursor.fetchall()

            for TRstData in TRstValues:
                temp = TRstData.FieldName
                if self.GetParam(temp, tParam) == True:
                    if not FromINITMachine and pFromActivateJob:
                        tParam.FirstReadInCurrentJob = True
                    
                    if pFromActivateJob and tParam.ErrorAlarmActive:
                        tParam.Alarms = []
                    
                    if (temp == 'WorkOrder'):
                        strSQL = 'Update TblControllerFields SET TargetValue = \'' + str(JobID) + '\' Where ControllerID = ' + str(self.__mControllerID) + ' AND FieldName = \'' + temp + '\''
                        MdlConnection.CN.execute(strSQL)
                        
                        self.__mActiveJobID = JobID
                        tParam.LastValue = JobID
                    elif (temp == 'CycleTime'):
                        self.__mCycleTimeStandard = MdlADOFunctions.fGetRstValDouble(TRstData.TargetValue)
                        
                    elif (temp == 'UnitsTarget'):
                        
                        tParam.LastValue = UnitsTarget
                    
                    strUCL = '' + MdlADOFunctions.fGetRstValDouble(TRstData.HValue)
                    strLCL = '' + MdlADOFunctions.fGetRstValDouble(TRstData.LValue)
                    strQUCL = '' + MdlADOFunctions.fGetRstValDouble(TRstData.HHValue)
                    strQLCL = '' + MdlADOFunctions.fGetRstValDouble(TRstData.LLValue)
                    strMean = '' + TRstData.TargetValue
                    if tParam.FName == 'TotalCycles':
                        tParam.FName = tParam.FName
                    
                    if ( ( strMean != '' and UpdateController == True )  or  ( TRstData.CitectDeviceType != 1 ) )  and  ( TRstData.CitectDeviceType != 3 ) :
                        if TRstData.ChannelNum == 1:
                            if 'Feeder' in tParam.FName or 'MainMatPC' in tParam.FName or tParam.FName == 'Cnl1IsActive':
                                if ( MainDSID > 0 and DSIsActive == True )  or  ( MainDSID == 0 ) :
                                    if not ( FromINITMachine and not tParam.WriteConditionalControllerField is None ) :
                                        pass
                                if 'MainMatPC' in tParam.FName:
                                    if ( MainDSID > 0 and DSIsActive == False )  and  ( tParam.DirectRead == False ) :
                                        if not ( FromINITMachine and not tParam.WriteConditionalControllerField is None ) :
                                            pass
                            else:
                                if not ( FromINITMachine and not tParam.WriteConditionalControllerField is None ) :
                                    pass
                        else:
                            if not ( FromINITMachine and not tParam.WriteConditionalControllerField is None ) :
                                pass
                        
                        if not ( tParam.CitectDeviceType == 1 ) :
                            tParam.LastValue = strMean
                    if tParam.IsSPCValue:
                        tParam.UpdateLimits(strMean, strUCL, strLCL, strQUCL, strQLCL, True)
                    else:
                        tParam.UpdateLimits(strMean, strUCL, strLCL, strQUCL, strQLCL)
                    
                    if tParam.RejectReasonID > 0 and self.__mActiveJobID > 0:                    
                        strSQL = 'SELECT SUM(Amount) as RejectsAmount FROM TblRejects Where JobID = ' + str(self.__mActiveJobID) + ' AND ReasonID =' + str(tParam.RejectReasonID)

                        RstCursor = MdlConnection.CN.cursor()
                        RstCursor.execute(strSQL)
                        RstData = RstCursor.fetchone()

                        tParam.RejectsA = MdlADOFunctions.fGetRstValLong(RstData.RejectsAmount)
                        RstCursor.close()
                        
                        tParam.RejectsALast = tParam.RejectsA

            TRstCursor.close()
            if ResetTotals() == True:
                if UpdateController == True:
                    for i in range(0, self.__mResetTotals.Count):
                        rParam = self.__mResetTotals.Item(i)
                        rParam.LastValue = 1
                self.ResetTotals
                if MainDSID > 0:
                    self.SetFieldValue('Cnl1NewJob', '1')
                if ( ( DirectBatchBlender == True )  or  ( DownloadRecipeDirectly == True ) )  and DSIsActive == True:
                    self.SetFieldValue('Cnl1NewJob', '1')
                    self.SetFieldValue('Cnl1IsActive', '1')
                strSQL = 'Update TblControllers Set TotalCycles = 0, TotalWeight = 0, TotalWeightLast = 0, AdditiveTotalWeight = 0, CyclesTargetPC = 0, UnitsProduced = 0, UnitsProducedOK = 0, TotalCyclesReadCurrent = 0 Where ID = ' + str(self.ControllerID)
                MdlConnection.CN.execute(strSQL)
                strSQL = 'Update TblControllerChannels Set TotalWeight = 0, TotalWeightLast = 0 Where ControllerID = ' + str(self.ControllerID)
                MdlConnection.CN.execute(strSQL)
            
            self.SetFieldValue('Cnl1CreateNewBatch', '1')
            
            if ( ( DirectBatchBlender == True )  or  ( DownloadRecipeDirectly == True ) )  and DSIsActive == True:                
                self.SetFieldValue('Cnl1IsActive', '1')

            if MainDSID > 0 and DSIsActive == True:
                if DSActiveDemand == True:
                    self.SetFieldValue('Cnl1IsActive', '1')
                else:
                    self.SetFieldValue('Cnl1IsActive', '0')

            if MainDSID > 0 and DSIsActive == False:
                self.SetFieldValue('Cnl1IsActive', '0')
            temp = 'MachineID'

            if self.GetParam(temp, tParam) == True:
                tParam = self.__mCParams.Item(temp)
                tParam.LastValue = self.__mID

            if self.UpdateAddressOnJobActive == True:
                if UpdateController == True and pFromActivateJob == True:                    
                    self.__mUpdateAddress.LastValue = 1
            else:
                if UpdateController == True:
                    self.__mUpdateAddress.LastValue = 1
            strSQL = 'Select SetUPEnd, PConfigID From TblJob Where ID = ' + str(JobID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if JobID > 0 and ResetTotals() == True:
                if RstData.SetUpEnd:
                    self.__mNewJob = False
                else:                    
                    if self.MonitorSetupWorkingTime == False:
                        if self.ActiveJob.OpenEvent is None:
                            tEvent = RTEvent()
                            tEvent.Create(self, 10, 100, 'Setup', self.ActiveJob)
                            self.ActiveJob.OpenEvent = tEvent
                            
                            if not self.ActiveJob.OpenWorkingEvent is None:
                                self.ActiveJob.OpenWorkingEvent.EndEvent()
                                self.ActiveJob.OpenWorkingEvent = None
                                if self.ActiveJob.PConfigID != 0 and self.ActiveJob.IsPConfigMain == True:
                                    for tVariant in self.ActiveJob.PConfigJobs:
                                        tChildJob = tVariant
                                        tChildJob.OpenWorkingEvent.EndEvent
                                        tChildJob.OpenWorkingEvent = None
                    self.__mNewJob = True
                if MdlADOFunctions.fGetRstValLong(RstData.PConfigID) > 0:
                    MdlRTWorkOrder.fJobPConfigSubDetailsUpdate(JobID)
            RstCursor.close()
            if FromINITMachine:
                if not self.ActiveJob is None:
                    if self.ActiveJob.NextJobMaterialFlowStart != 0:
                        self.InitMachineMaterialFlowAfterStartup(self.ActiveJob)
            
            self.FireEventTriggeredTasks(1)
            if FromINITMachine == False and pFromActivateJob:
                
                self.CreateActivePallet(2, self.ActiveJob.MachineType.ActivePalletCreationBy)

            returnVal = True

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError('JobLoad', str(0), error.agrs[0], 'temp = ' + str(temp) + ' ;JobID = ' + str(JobID) + ' ;MachineID = ' + str(self.__mID) + ' ;ErrCounter = ' + str(ErrCounter))
                        
            if ErrCounter > 30:
                return returnVal
            else:
                ErrCounter = ErrCounter + 1
                
        if TRst.State != 0:
            TRst.close()
        TRst = None
        if Rst.State != 0:
            RstCursor.close()

        Rst = None
        tParam = None
        rParam = None
        tBatchParam = None
        tJob = None
        tJosh = None
        tEvent = None
        tChannel = None
        tChildJob = None
        return returnVal

    def GetFieldValue(self, FieldName, ValType='LastValue'):
        returnVal = None
        tParam = None
        
        if self.GetParam(FieldName, tParam) == False:
            return returnVal
        if (ValType == 'LastValue'):
            returnVal = tParam.LastValue
        elif (ValType == 'STDEV'):
            returnVal = tParam.STDEV
        elif (ValType == 'MEAN'):
            returnVal = tParam.Mean
        elif (ValType == 'SMEAN'):
            returnVal = tParam.SMean
        elif (ValType == 'UCL'):
            returnVal = tParam.UCL
        elif (ValType == 'PUCL'):
            returnVal = tParam.PUCL
        elif (ValType == 'QUCL'):
            returnVal = tParam.QUCL
        elif (ValType == 'LCL'):
            returnVal = tParam.LCL
        elif (ValType == 'PLCL'):
            returnVal = tParam.PLCL
        elif (ValType == 'QLCL'):
            returnVal = tParam.QLCL
        elif (ValType == 'CalcFunction'):
            returnVal = tParam.CalcFunction
        elif (ValType == 'RawZero'):
            returnVal = tParam.RawZero
        elif (ValType == 'RawFull'):
            returnVal = tParam.RawFull
        elif (ValType == 'ScaledZero'):
            returnVal = tParam.ScaledZero
        elif (ValType == 'ScaledFull'):
            returnVal = tParam.ScaledFull
        elif (ValType == 'AlarmCycleAcknowledge'):
            returnVal = tParam.AlarmCycleAcknowledge
        elif (ValType == 'AlarmPerminentAcknowledge'):
            returnVal = tParam.AlarmPerminentAcknowledge
            
            
        
        return returnVal

    def SetFieldValue(self, FieldName, strValue):        
        try:
            self.__mCParams[FieldName].LastValue = strValue
            return True

        except:
            return False

    def SetFieldLValue(self, FieldName, pValue):        
        try:
            self.__mCParams.Item[FieldName].PLCL = pValue
            return True
        except:
            return False

    def SetFieldHValue(self, FieldName, pValue):
        returnVal = None
        
        returnVal = False
        self.__mCParams.Item[FieldName].PUCL = pValue
        returnVal = True
        if Err.Number != 0:
            Err.Clear()
        return returnVal

    def SetFieldValidValue(self, FieldName, strValue):
        returnVal = None
        
        returnVal = False
        self.__mCParams.Item[FieldName].LastValidValue = strValue
        returnVal = True
        if Err.Number != 0:
            Err.Clear()
        return returnVal

    def GetParam(self, FieldName, vParam):
        returnVal = False
        tParam = None
        bParam = None
        Counter = 0
        BCounter = 0
        BatchCount = 0
        
        try:
            for tParam in self.__mCParams.values():
                if tParam.FName == FieldName:
                    vParam[0] = tParam
                    returnVal = True
                    return returnVal

                if not ( tParam.BatchParams is None ):
                    BatchCount = len(tParam.BatchParams)
                    if BatchCount > 0:
                        for bParam in self.__mCParams.values():
                            if bParam.FName == FieldName:
                                vParam[0] = bParam
                                returnVal = True
                                return returnVal
        except BaseException as error:
            tParam = None
            bParam = None

        return returnVal

    def ShrinkData(self, IgnoreInterval):
        returnVal = None
        StartTime = ''

        EndTime = ''

        Counter = 0
        
        if self.ActiveJob is None:
            return returnVal
        if IgnoreInterval == False:
            if DateDiff('n', self.__mLastShrinkTime, mdl_Common.NowGMT()) < 3:
                return returnVal
        if self.__mCParams.Count > 0:
            for Counter in range(0, self.__mCParams.Count):
                
                
                self.__mCParams.Item(Counter).ShrinkData(self.ActiveJob.ID, str(self.__mActiveLocalID), self.__mID, int(self.ActiveJob.Mold.ID), self.ActiveJob.Product.ID, StartTime, EndTime, self.__mStatus)
        if self.__mBatchTrigerSet == True:
            
            self.__mBatchTrigerP.ShrinkData(self.ActiveJob.ID, str(self.__mActiveLocalID), self.__mID, int(self.ActiveJob.Mold.ID), self.ActiveJob.Product.ID, StartTime, EndTime, self.__mStatus)
            if self.__mBatchTrigerP.BatchParams.Count > 0:
                for Counter in range(0, self.__mBatchTrigerP.BatchParams.Count):
                    
                    self.__mBatchTrigerP.BatchParams.Item(Counter).ShrinkData(self.ActiveJob.ID, str(self.__mActiveLocalID), self.__mID, int(self.ActiveJob.Mold.ID), self.ActiveJob.Product.ID, StartTime, EndTime, self.__mStatus)
        self.__mLastShrinkTime = mdl_Common.NowGMT()
        if Err.Number != 0:
            RecordError('Machine:ShrinkData', '' + Err.Number, '' + Err.Description, 'MID = ' + self.str(__mID))
            Err.Clear()
            
        return returnVal

    
    def CalcJobData(self, CalcDuration):
        returnVal = None
        tCalcDuration = False
        
        returnVal = False
        if CalcDuration == 0:
            tCalcDuration = False
        else:
            tCalcDuration = True
        
        if not self.ActiveJob is None:
            self.ActiveJob.DetailsCalc(tCalcDuration, False)
        
        
        returnVal = True
        return returnVal

    def __ResetTotals(self):
        returnVal = None
        i = 0

        tParam = None
        
        returnVal = False
        self.__mProgress = 0
        self.__mTotalCycles = 0
        self.__mTotalCyclesLast = 0
        
        
        self.__mRejectsRead = 0
        self.__mRejectsReadLast = 0
        
        
        
        self.__mCyclesDiff = 0
        self.__mCyclesDiffRead = 0
        self.__mStatus = ''
        self.__mIOStatus = 1
        self.__mCurrentDownTime = 0
        self.__mIOErrorCount = 0
        self.__mIODownCount = 0
        self.__mNoProgressCount = 0
        if self.GetParam('NoProgressCount', tParam) == True:
            tParam.LastValue = self.__mNoProgressCount
            self.__mCParams.Item('NoProgressCount').GetListData
        self.__mMachineStop = False
        self.__mMachineSignalStop = False
        self.__mEngineSignalActive = False
        self.__mReadFailCount = 0
        self.__mReadWaitCount = 0
        
        self.__mAlarmsActive = True
        self.__mNewJob = True
        self.__mInControl = False
        
        self.SetFieldValue('UnitsProduced', '0')
        self.SetFieldValue('UnitsProducedOK', '0')
        
        
        
        self.TotalWeight = 0
        self.TotalWeightLast = 0
        
        self.CycleWeight = 0
        returnVal = True
        return returnVal

    def AggFunction(self, FunctionName, Fields, BatchOnly):
        returnVal = None
        tParam = None

        bParam = None

        Counter = 0

        BCounter = 0

        BatchCount = 0

        ArrVals = []

        ArrValsCount = 0

        BatchParams = []
        
        for Counter in range(0, self.__mCParams.Count):
            tParam = self.__mCParams.Item(Counter)
            if BatchOnly == False:
                if InStr(Fields, tParam.FName) >= 1:
                    if IsNumeric(tParam.LastValue):
                        ArrValsCount = ArrValsCount + 1
                        ArrVals = []
                        ArrVals[ArrValsCount] = tParam.LastValue
                
                
            else:
                for BCounter in range(0, self.__mBatchTrigerP.BatchParams.Count):
                    bParam = self.__mBatchTrigerP.BatchParams.Item(BCounter)
                    if InStr(Fields, bParam.FName) >= 1:
                        if IsNumeric(bParam.LastValue):
                            ArrValsCount = ArrValsCount + 1
                            ArrVals = []
                            ArrVals[ArrValsCount] = bParam.LastValue
        if ArrValsCount == 0:
            return returnVal
        if (FunctionName == 'Min'):
            returnVal = fMin(ArrVals, ArrValsCount)
        elif (FunctionName == 'Max'):
            returnVal = fMax(ArrVals, ArrValsCount)
        elif (FunctionName == 'AVG'):
            returnVal = fAVG(ArrVals, ArrValsCount)
        elif (FunctionName == 'SUM'):
            returnVal = fSum(ArrVals, ArrValsCount)
        elif (FunctionName == 'STDEV'):
            returnVal = fSTDev(ArrVals, ArrValsCount)
        return returnVal

    def IOCancel(self):
        
        
        
        
        
        
        pass

    def ManualEntryCalc(self):
        returnVal = None
        
        returnVal = False
        fReadMainData(True, True)
        
        returnVal = True
        return returnVal

    def fClearControllerFields(self):
        returnVal = None
        Rst = None

        strSQL = ''
        
        returnVal = False
        strSQL = 'Update TblControllers Set TotalCycles=0, TotalCycles_W=0'
        strSQL = strSQL + ', TotalCyclesLast=0, TotalWeight=0, TotalWeightLast=0, AdditiveTotalWeight=0'
        strSQL = strSQL + ', PlastificationTime=0, ProductWeight=0, ProductWeight_W=0, UnitsProduced=0, UnitsProducedOK=0'
        strSQL = strSQL + ' Where ID = ' + self.__mControllerID
        MdlConnection.CN.execute(strSQL)
        self.TotalCycles = 0
        self.TotalCyclesLast = 0
        self.TotalWeight = 0
        self.TotalWeightLast = 0
        self.CycleWeight = 0
        strSQL = 'Update TblControllerChannels Set TotalWeight=0, TotalWeightLast=0 Where ControllerID = ' + self.__mControllerID
        MdlConnection.CN.execute(strSQL)
        returnVal = True
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
        if Rst.State != 0:
            RstCursor.close()
        Rst = None
        return returnVal

    def TotalWeightChannelLet(self, the_mTotalWeightChannel, ChannelNum, UpdateTable, UpdateLast):
        returnVal = None
        CPName = ''

        strSQL = ''

        tParam = None
        
        if ChannelNum > 0:
            CPName = 'Cnl' + ChannelNum + 'TotalWeight'
            if self.GetParam(CPName, tParam) == True:
                if not ( tParam.OPCItemHandle > 0 ) :
                    tParam.LastValue = the_mTotalWeightChannel
            if UpdateTable == True:
                if UpdateLast == True:
                    strSQL = 'Update TblControllerChannels SET TotalWeight = ' + the_mTotalWeightChannel + ' WHERE ControllerID = ' + str(self.__mControllerID) + ' AND ChannelNum = ' + ChannelNum
                else:
                    strSQL = 'Update TblControllerChannels SET TotalWeight = ' + the_mTotalWeightChannel + ',TotalWeightLast = ' + the_mTotalWeightChannel + ' WHERE ControllerID = ' + str(self.__mControllerID) + ' AND ChannelNum = ' + ChannelNum
                MdlConnection.CN.execute(strSQL)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
        return returnVal

    def __UpdateControllerFieldsParam(self, CsID, MachineID, WebAlarmAcknowledge=False):
        returnVal = None
        strSQL = ''

        temp = ''

        strItemID = ''

        strGroupName = ''

        Rst = None

        tControlParam = None

        vParam = None

        ParamFound = False

        rVal = 0
        
        
        returnVal = False
        strSQL = 'Select * From TblControllerFields Where ControllerID = ' + CsID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        while not Rst.EOF:
            if not WebAlarmAcknowledge:
                if not IsNull(RstData.CalcFunction):
                    self.__mCParams.Item[RstData.FieldName].CalcFunction = RstData.CalcFunction
                if not IsNull(RstData.RawZero):
                    self.__mCParams.Item[RstData.FieldName].RawZero = MdlADOFunctions.fGetRstValDouble(RstData.RawZero)
                if not IsNull(RstData.RawFull):
                    self.__mCParams.Item[RstData.FieldName].RawFull = MdlADOFunctions.fGetRstValDouble(RstData.RawFull)
                if not IsNull(RstData.ScaleZero):
                    self.__mCParams.Item[RstData.FieldName].ScaledZero = MdlADOFunctions.fGetRstValDouble(RstData.ScaleZero)
                if not IsNull(RstData.ScaleFull):
                    self.__mCParams.Item[RstData.FieldName].ScaledFull = MdlADOFunctions.fGetRstValDouble(RstData.ScaleFull)
                if not IsNull(RstData.AlarmCylceAcknowledge):
                    self.__mCParams.Item[RstData.FieldName].AlarmCycleAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmCylceAcknowledge, False)
                    
                if not IsNull(RstData.AlarmPerminentAcknowledge):
                    self.__mCParams.Item[RstData.FieldName].AlarmPerminentAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmPerminentAcknowledge, False)
                    
            if not IsNull(RstData.AlarmCylceAcknowledge):
                self.__mCParams.Item[RstData.FieldName].AlarmCycleAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmCylceAcknowledge, False)
                
            if not IsNull(RstData.AlarmPerminentAcknowledge):
                self.__mCParams.Item[RstData.FieldName].AlarmPerminentAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmPerminentAcknowledge, False)
                
            Rst.MoveNext()
        RstCursor.close()
        returnVal = True
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:UpdateControllerFieldsParam', str(Err.Number), Err.Description, 'ControllerID = ' + CsID)
            Err.Clear()
            
        if Rst.State != 0:
            RstCursor.close()
        Rst = None
        return returnVal

    def ResetMachineTotalFields(self):
        returnVal = None
        tmp = None
        
        returnVal = False
        for tmp in self.__mResetTotals:
            tmp.LastValue = 1
        returnVal = True
        if Err.Number != 0:
            RecordError('ResetMachineTotalFields', Err.Number, Err.Description, 'Machine = ' + self.ID)
        return returnVal

    def SaveJobsQueue(self):
        returnVal = None
        strSQL = ''

        SRst = None

        JRst = None

        ControllerFieldName = ''

        ControllerFieldPrefix = ''

        JobsToQueue = 0

        i = 0

        strCriteria = 0

        JobID = 0

        FieldValue = ''
        
        JobsToQueue = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineQueueJobsNum', 'TblMachines', 'ID = ' + self.ID, 'CN'))
        if JobsToQueue > 0:
            strSQL = 'Select TOP ' + JobsToQueue + ' ID, ProductID From TblJob Where MachineID = ' + self.ID + ' ORDER BY MachineJobOrder'
            JRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            JRst.ActiveConnection = None
            while not JRst.EOF:
                i = i + 1
                strSQL = 'Select * From STblMachineQueueParameters Where MachineID = ' + self.ID
                SRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                SRst.ActiveConnection = None
                while not SRst.EOF:
                    ControllerFieldName = Replace(MdlADOFunctions.fGetRstValString(SRst.Fields("ControllerFieldName").Value), '[QN]', str(i))
                    select_4 = MdlADOFunctions.fGetRstValString(SRst.Fields("SourceTableName").Value)
                    if (select_4 == 'TblProductRecipe'):
                        FieldValue = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('FValue', SRst.Fields("SourceTableName").Value, 'ChannelNum = ' + MdlADOFunctions.fGetRstValLong(SRst.Fields("SourceChannelNum").Value) + ' AND SplitNum = ' + MdlADOFunctions.fGetRstValLong(SRst.Fields("SourceSplitNum").Value) + ' AND PropertyID = ' + MdlADOFunctions.fGetRstValLong(SRst.Fields("SourcePropertyID").Value) + ' AND ProductID = ' + JRst.Fields("ProductID").Value, 'CN'))
                    elif (select_4 == 'TblProductRecipeJob'):
                        FieldValue = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('FValue', SRst.Fields("SourceTableName").Value, 'ChannelNum = ' + MdlADOFunctions.fGetRstValLong(SRst.Fields("SourceChannelNum").Value) + ' AND SplitNum = ' + MdlADOFunctions.fGetRstValLong(SRst.Fields("SourceSplitNum").Value) + ' AND PropertyID = ' + MdlADOFunctions.fGetRstValLong(SRst.Fields("SourcePropertyID").Value) + ' AND JobID = ' + JRst.Fields("ID").Value, 'CN'))
                    else:
                        FieldValue = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue(SRst.Fields("SourceField").Value, SRst.Fields("sourceTable").Value, 'ID = ' + JRst.Fields("ID").Value, 'CN'))
                    self.SetFieldValue(ControllerFieldName, FieldValue)
                    SRst.MoveNext()
                SRst.close()
                JRst.MoveNext()
            JRst.close()
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            Err.Clear()
            
        return returnVal

    def fResetDataSamples(self):
        returnVal = None
        tParam = None

        tDataSample = DataSample()
        
        returnVal = False
        for tParam in self.__mCParams:
            if tParam.DataSamples.Count > 0:
                for tDataSample in tParam.DataSamples:
                    tDataSample.Reset
        returnVal = True
        if Err.Number != 0:
            Err.Clear()
        tParam = None
        tDataSample = None
        return returnVal

    
    def CreateAlarm(self, pControlParam):
        returnVal = None
        tVariant = Variant()

        tAlarm = Alarm()

        tFound = False
        
        if not ( self.ActiveJob is None ) :
            for tVariant in pControlParam.Alarms:
                tAlarm = tVariant
                if tAlarm.ParamID == pControlParam.ID:
                    tFound = True
                    tAlarm.Update
                    
                    if not pControlParam.AlarmCycleAcknowledge and not pControlParam.AlarmPerminentAcknowledge:
                        if pControlParam.AlarmFile != '' and pControlParam.AlarmFileReplayInterval > 0:
                            if pControlParam.AlarmFileLastPlay != 0:
                                if DateDiff('n', pControlParam.AlarmFileLastPlay, mdl_Common.NowGMT()) >= pControlParam.AlarmFileReplayInterval:
                                    self.Server.WMPlayFile(pControlParam.AlarmFile, self.ID, self.ActiveJobID, True)
                                    pControlParam.AlarmFileLastPlay = mdl_Common.NowGMT()()
            if pControlParam.AlarmPerminentAcknowledge == True:
                return returnVal
            
            if self.EnableAlarmsDuringMachineStop == False and  ( self.MachineStop == True ) :
                return returnVal
            if self.EnableAlarmsDuringSetup == False and self.NewJob == True:
                return returnVal
            
            if pControlParam.EnableAlarmsDuringSetup == False and self.NewJob == True:
                return returnVal
            
            if self.ProductionModeID > 1:
                return returnVal
            if not tFound:
                tAlarm = Alarm()
                tAlarm.Create(pControlParam)
                self.ActiveJob.AddAlarm(tAlarm)
                pControlParam.AddAlarm(tAlarm)
                self.AlarmsOnCount = self.AlarmsOnCount + 1
                if pControlParam.AlarmFile != '':
                    
                    self.Server.WMPlayFile(pControlParam.AlarmFile, self.ID, self.ActiveJobID)
                    pControlParam.AlarmFileLastPlay = mdl_Common.NowGMT()()
                
                if pControlParam.SendSMSOnAlarm == True:
                    
                    FillSMSAlarmQue(self.ControllerID, pControlParam.FName, True, pControlParam.PLCL, pControlParam.LastValue, pControlParam.PUCL)
                    
                
                if pControlParam.SendPushOnAlarm:
                    self.LaunchParameterSystemAlarm(pControlParam)
        if Err.Number != 0:
            Err.Clear()
        return returnVal

    
    def CancelAlarm(self, pControlParam, pAlarmCycleAcknowledge=False):
        returnVal = None
        tVariant = Variant()

        tAlarm = Alarm()
        
        if pControlParam.AlarmCycleAcknowledge == True:
            pControlParam.AlarmCycleAcknowledge = False
        if self.AutoAlarmClerance == True or pAlarmCycleAcknowledge == True:
            for tVariant in pControlParam.Alarms:
                tAlarm = tVariant
                tAlarm.Delete
                pControlParam.Alarms.Remove(str(tAlarm.ID))
                self.ActiveJob.OpenAlarms.Remove(str(tAlarm.ID))
                self.AlarmsOnCount = self.AlarmsOnCount - 1
        if Err.Number != 0:
            Err.Clear()
        return returnVal

    def UpdateAlarmsFromDB(self):
        strSQL = ''

        Rst = None

        tParam = None
        
        strSQL = 'SELECT ID,FieldName,AlarmCylceAcknowledge,AlarmPerminentAcknowledge FROM TblControllerFields WHERE CreateNC <> 0 AND ControllerID = ' + self.ControllerID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        while not Rst.EOF:
            if self.GetParam(RstData.FieldName, tParam) == True:
                if tParam.AlarmCycleAcknowledge == False and MdlADOFunctions.fGetRstValBool(RstData.AlarmCylceAcknowledge, False) == True:
                    self.CancelAlarm(tParam, True)
                    
                    tParam.AlarmFileLastPlay = 0
                    tParam.AlarmFirstDetected = 0
                if tParam.AlarmPerminentAcknowledge == False and MdlADOFunctions.fGetRstValBool(RstData.AlarmPerminentAcknowledge, False) == True:
                    self.CancelAlarm(tParam, True)
                    
                    tParam.AlarmFileLastPlay = 0
                    tParam.AlarmFirstDetected = 0
                tParam.AlarmCycleAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmCylceAcknowledge, False)
                tParam.AlarmPerminentAcknowledge = MdlADOFunctions.fGetRstValBool(RstData.AlarmPerminentAcknowledge, False)
            Rst.MoveNext()
        RstCursor.close()
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            Err.Clear()
        Rst = None
        tParam = None

    def StartMaterialFlow(self, pJob):
        strSQL = ''

        Rst = None

        tDataSample = DataSample()

        tControlParam = None

        tChannel = Channel()

        tSplit = ChannelSplit()

        tInitialValue = 0
        
        strSQL = 'SELECT ID, ChannelNum, SplitNum, InitialValue, JobID FROM TblMachineMaterialFlow WHERE MachineID = ' + self.ID + ' ORDER BY ChannelNum'
        Rst.Open(strSQL, CN, adOpenDynamic, adLockOptimistic)
        while not Rst.EOF:
            tChannel = pJob.ControllerChannels.Item(str(RstData.ChannelNum))
            if not tChannel is None:
                if ( MdlADOFunctions.fGetRstValLong(RstData.SplitNum) == 0 and tChannel.SplitsCounter == 0 )  or  ( MdlADOFunctions.fGetRstValLong(RstData.SplitNum) > 0 and tChannel.SplitsCounter > 0 ) :
                    if tChannel.SplitsCounter == 0:
                        if not tChannel.TotalWeight.ControllerField is None:
                            if tChannel.TotalWeight.ControllerField.CitectDeviceType == 1:
                                tDataSample = DataSample()
                                tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tChannel.TotalWeight.ControllerField.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), mdl_Common.NowGMT(), 'TblMachineMaterialFlow', 'Values', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                tChannel.TotalWeight.ControllerField.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                tInitialValue = tChannel.TotalWeight.ControllerField.LastValidValue
                                RstData.JobID = pJob.ID
                                RstData.InitialValue = tInitialValue
                                Rst.Update()
                                tChannel.MaterialFlowForNextJob = True
                            else:
                                tControlParam = None
                                if self.GetParam('TotalCycles', tControlParam) == True:
                                    tDataSample = DataSample()
                                    
                                    tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), mdl_Common.NowGMT(), 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                    tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                    tInitialValue = tControlParam.LastValidValue
                                    RstData.JobID = pJob.ID
                                    RstData.InitialValue = tInitialValue
                                    Rst.Update()
                                    tChannel.MaterialFlowForNextJob = True
                        else:
                            tControlParam = None
                            if self.GetParam('TotalCycles', tControlParam) == True:
                                tDataSample = DataSample()
                                
                                tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), mdl_Common.NowGMT(), 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                tInitialValue = tControlParam.LastValidValue
                                RstData.JobID = pJob.ID
                                RstData.InitialValue = tInitialValue
                                Rst.Update()
                                tChannel.MaterialFlowForNextJob = True
                    else:
                        tSplit = tChannel.Splits.Item(str(RstData.SplitNum))
                        if not tSplit is None:
                            if not tSplit.TotalWeight.ControllerField is None:
                                if tSplit.TotalWeight.ControllerField.CitectDeviceType == 1:
                                    tDataSample = DataSample()
                                    
                                    tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tSplit.TotalWeight.ControllerField.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), mdl_Common.NowGMT(), 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                    tSplit.TotalWeight.ControllerField.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                    tInitialValue = tSplit.TotalWeight.ControllerField.LastValidValue
                                    RstData.JobID = pJob.ID
                                    RstData.InitialValue = tInitialValue
                                    Rst.Update()
                                    tSplit.MaterialFlowForNextJob = True
                                else:
                                    tControlParam = None
                                    if self.GetParam('TotalCycles', tControlParam) == True:
                                        tDataSample = DataSample()
                                        
                                        tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), mdl_Common.NowGMT(), 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                        tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                        tInitialValue = tControlParam.LastValidValue
                                        RstData.JobID = pJob.ID
                                        RstData.InitialValue = tInitialValue
                                        Rst.Update()
                                        tSplit.MaterialFlowForNextJob = True
                            else:
                                tControlParam = None
                                if self.GetParam('TotalCycles', tControlParam) == True:
                                    tDataSample = DataSample()
                                    
                                    tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), mdl_Common.NowGMT(), 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                    tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                    tInitialValue = tControlParam.LastValidValue
                                    RstData.JobID = pJob.ID
                                    RstData.InitialValue = tInitialValue
                                    Rst.Update()
                                    tSplit.MaterialFlowForNextJob = True
            Rst.MoveNext()
        RstCursor.close()
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            Err.Clear()
        Rst = None

    def InitMachineMaterialFlowAfterStartup(self, pJob):
        strSQL = ''

        Rst = None

        tChannel = Channel()

        tSplit = ChannelSplit()

        tControlParam = None

        tDataSample = DataSample()
        
        strSQL = 'SELECT ID, ChannelNum, SplitNum, InitialValue FROM TblMachineMaterialFlow WHERE MachineID = ' + self.ID + ' ORDER BY ChannelNum'
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        while not Rst.EOF:
            tChannel = pJob.ControllerChannels.Item(str(RstData.ChannelNum))
            if not tChannel is None:
                if ( MdlADOFunctions.fGetRstValLong(RstData.SplitNum) == 0 and tChannel.SplitsCounter == 0 ) or ( MdlADOFunctions.fGetRstValLong(RstData.SplitNum) > 0 and tChannel.SplitsCounter > 0 ) :
                    if tChannel.SplitsCounter == 0:
                        tControlParam = None
                        if not tChannel.TotalWeight.ControllerField is None:
                            tControlParam = tChannel.TotalWeight.ControllerField
                            if tControlParam.CitectDeviceType == 1:
                                tDataSample = DataSample()
                                
                                tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), pJob.NextJobMaterialFlowStart, 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                tDataSample.AddValue(RstData.InitialValue, pJob.NextJobMaterialFlowStart)
                                tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                tChannel.MaterialFlowForNextJob = True
                            else:
                                tControlParam = None
                                if self.GetParam('TotalCycles', tControlParam) == True:
                                    tDataSample = DataSample()
                                    
                                    tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), pJob.NextJobMaterialFlowStart, 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                    tDataSample.AddValue(RstData.InitialValue, pJob.NextJobMaterialFlowStart)
                                    tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                    tChannel.MaterialFlowForNextJob = True
                        else:
                            tControlParam = None
                            if self.GetParam('TotalCycles', tControlParam) == True:
                                tDataSample = DataSample()
                                
                                tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), pJob.NextJobMaterialFlowStart, 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                tDataSample.AddValue(RstData.InitialValue, pJob.NextJobMaterialFlowStart)
                                tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                tChannel.MaterialFlowForNextJob = True
                    else:
                        tSplit = tChannel.Splits(str(RstData.SplitNum))
                        if not tSplit.TotalWeight.ControllerField is None:
                            tControlParam = None
                            tControlParam = tSplit.TotalWeight.ControllerField
                            if tControlParam.CitectDeviceType == 1:
                                tDataSample = DataSample()
                                
                                tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), pJob.NextJobMaterialFlowStart, 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                tDataSample.AddValue(RstData.InitialValue, pJob.NextJobMaterialFlowStart)
                                tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                tSplit.MaterialFlowForNextJob = True
                            else:
                                tControlParam = None
                                if self.GetParam('TotalCycles', tControlParam) == True:
                                    tDataSample = DataSample()
                                    
                                    tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), pJob.NextJobMaterialFlowStart, 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                    tDataSample.AddValue(RstData.InitialValue, pJob.NextJobMaterialFlowStart)
                                    tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                    tSplit.MaterialFlowForNextJob = True
                        else:
                            tControlParam = None
                            if self.GetParam('TotalCycles', tControlParam) == True:
                                tDataSample = DataSample()
                                
                                tDataSample.InitDynamic(self, MdlADOFunctions.fGetRstValLong(( RstData.ID )  * - 1), tControlParam.FName, DS_SpecificTimestamp, DS_Diff, VBGetMissingArgument(tDataSample.InitDynamic, 5), VBGetMissingArgument(tDataSample.InitDynamic, 6), pJob.NextJobMaterialFlowStart, 'TblMachineMaterialFlow', 'Value', 'ID = ' + MdlADOFunctions.fGetRstValLong(RstData.ID))
                                tDataSample.AddValue(RstData.InitialValue, pJob.NextJobMaterialFlowStart)
                                tControlParam.DataSamples.Add(tDataSample, str(tDataSample.ID))
                                tSplit.MaterialFlowForNextJob = True
            Rst.MoveNext()
        RstCursor.close()
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            Err.Clear()
        Rst = None

    def fRemoveDynamicDataSamples(self):
        returnVal = None
        tParam = None

        tDataSample = DataSample()
        
        returnVal = False
        for tParam in self.__mCParams:
            if tParam.DataSamples.Count > 0:
                for tDataSample in tParam.DataSamples:
                    if tDataSample.ID < 0:
                        tParam.DataSamples.Remove(str(tDataSample.ID))
        returnVal = True
        if Err.Number != 0:
            Err.Clear()
        tParam = None
        tDataSample = None
        return returnVal

    def LoadConditionalControllerFields(self):
        strSQL = ''
        Rst = None
        tControlParam = [None]
        tConditionalControlParam = [None]
        
        try:
            strSQL = 'SELECT FieldName,WriteConditionalControllerField,WriteConditionalMinValue,WriteConditionalMaxValue '
            strSQL = strSQL + 'FROM TblControllerFields '
            strSQL = strSQL + 'WHERE MachineID = ' + str(self.ID) + ' AND WriteConditionalControllerField IS NOT NULL'

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstValues = RstCursor.fetchall()
            
            for RstData in RstValues:
                if self.GetParam(MdlADOFunctions.fGetRstValString(RstData.FieldName), tControlParam):
                    if self.GetParam(MdlADOFunctions.fGetRstValString(RstData.WriteConditionalControllerField), tConditionalControlParam):
                        tControlParam.WriteConditionalControllerField = tConditionalControlParam
                        tControlParam.WriteConditionalMinValue = MdlADOFunctions.fGetRstValDouble(RstData.WriteConditionalMinValue)
                        tControlParam.WriteConditionalMaxValue = MdlADOFunctions.fGetRstValDouble(RstData.WriteConditionalMaxValue)

            RstCursor.close()
        
        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self) + '.LoadConditionalControllerFields:', str(0), error.args[0], 'MachineID: ' + str(self.ID))
        
        RstCursor = None


    def FireEventTriggeredTasks(self, PEventTypeID):
        tTaskTrigger = TaskTrigger()

        tVariant = Variant()
        
        for tVariant in self.mTaskTriggers:
            tTaskTrigger = tVariant
            if tTaskTrigger.PEventTypeID == PEventTypeID:
                if tTaskTrigger.CheckInterval == True:
                    tTaskTrigger.FireTrigger()
        if Err.Number != 0:
            RecordError(TypeName(self) + '.FireEventTriggeredTasks:', Err.Number, Err.Description, 'MachineID: ' + self.ID + '. EventTypeID: ' + PEventTypeID)
            Err.Clear()

    def CheckIfDosingSystem(self):
        strSQL = ''

        Rst = None
        
        strSQL = 'SELECT ID FROM TblDS WHERE MachineID = ' + self.ID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        if Rst.RecordCount > 0:
            self.IsDosingSystem = True
        RstCursor.close()
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError(TypeName(self) + '.CheckIfDosingSystem:', Err.Number, Err.Description, 'MachineID: ' + self.ID)
            Err.Clear()
        Rst = None

    def CreateActivePallet(self, pActivePalletCreationModeID, pActivePalletCreationBy):
        tNewInventoryID = 0
        
        if (pActivePalletCreationBy == 1):
            if self.ActivePalletCreationModeID == pActivePalletCreationModeID:
                
                if self.ActivePalletInventoryID != 0:
                    CloseActivePalletInventoryItem(self)
                CreateActivePalletInventortyItem(self)
        elif (pActivePalletCreationBy == 2):
            if self.ActiveJob.Product.ActivePalletCreationModeID == pActivePalletCreationModeID:
                
                if self.ActivePalletInventoryID != 0:
                    CloseActivePalletInventoryItem(self)
                CreateActivePalletInventortyItem(self)
        
        self.FireEventTriggeredTasks(5)
        if Err.Number != 0:
            RecordError(TypeName(self) + '.CreateActivePallet:', Err.Number, Err.Description, 'MachineID: ' + self.ID)
            Err.Clear()

    def WriteProdutionParametersToHistory(self):
        returnVal = None
        Counter = 0

        RID = 0

        TCount = 0

        strSQL = ''

        strFields = ''

        strVals = ''

        tParam = None

        CycleTimeSMean = 0

        ShiftID = 0

        strINSERT = ''

        tVariant = Variant()

        tControlParam = None

        BatchParams = Dictionary()

        Rst = None

        SourceFieldName = ''

        FieldName = ''

        SourceTableName = ''

        value = Variant()

        ColumnExist = 0
        
        if self.ActiveJob is None:
            returnVal = True
            return returnVal
        if self.BatchReadLastRecord != 0:
            if self.Server.SystemVariables.HistoryIntervalSec > 0:
                if DateDiff('s', self.BatchReadLastRecord, mdl_Common.NowGMT()()) < self.Server.SystemVariables.HistoryIntervalSec:
                    return returnVal
            else:
                if DateDiff('n', self.BatchReadLastRecord, mdl_Common.NowGMT()()) < self.Server.SystemVariables.HistoryIntervalMin:
                    return returnVal
        else:
            self.BatchReadLastRecord = mdl_Common.NowGMT()()
            return returnVal
        returnVal = False
        strSQL = 'SELECT * FROM STblMachineParametersGraphs'
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        while not Rst.EOF:
            SourceTableName = MdlADOFunctions.fGetRstValString(RstData.SourceTableName)
            SourceFieldName = MdlADOFunctions.fGetRstValString(RstData.SourceFieldName)
            FieldName = MdlADOFunctions.fGetRstValString(RstData.FieldName)
            ColumnExist = 0
            ColumnExist = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('COUNT(COLUMN_NAME)', 'INFORMATION_SCHEMA.COLUMNS', 'TABLE_NAME = \'TblMachineParametersHistory\' AND COLUMN_NAME = \'' + FieldName + '\'', 'CN'))
            if ColumnExist == 0:
                strSQL = ''
                strSQL = strSQL + 'ALTER TABLE TblMachineParametersHistory' + vbCrLf
                strSQL = strSQL + 'ADD ' + FieldName + ' float'
                MdlConnection.CN.execute(( strSQL ))
            select_6 = UCase(SourceTableName)
            if (select_6 == 'TBLJOB'):
                value = CallByName(self.ActiveJob, SourceFieldName, VbGet)
            elif (select_6 == 'TBLJOSH'):
                value = CallByName(self.ActiveJosh, SourceFieldName, VbGet)
            elif (select_6 == 'TBLMACHINES'):
                value = CallByName(self, SourceFieldName, VbGet)
            else:
                value = MdlADOFunctions.GetSingleValue(SourceFieldName, SourceTableName, MdlADOFunctions.fGetRstValString(RstData.SourceStrWhere), 'CN')
            BatchParams.Add(FieldName, value)
            Rst.MoveNext()
        RstCursor.close()
        strINSERT = 'INSERT INTO TblMachineParametersHistory'
        strINSERT = strINSERT + ' ('
        strINSERT = strINSERT + ' JobID'
        strINSERT = strINSERT + ' ,MoldID'
        strINSERT = strINSERT + ' ,MachineID'
        strINSERT = strINSERT + ' ,ProductID'
        strINSERT = strINSERT + ' ,RecordTime'
        strINSERT = strINSERT + ' ,ShiftID'
        strINSERT = strINSERT + ' ,ShiftStartTime'
        if not BatchParams is None:
            for tVariant in BatchParams.keys:
                strINSERT = strINSERT + ' ,' + tVariant
        strINSERT = strINSERT + ') '
        
        strINSERT = strINSERT + ' VALUES '
        strINSERT = strINSERT + ' ('
        strINSERT = strINSERT + self.ActiveJob.ID
        strINSERT = strINSERT + ', ' + self.ActiveJob.Mold.ID
        strINSERT = strINSERT + ', ' + self.ID
        strINSERT = strINSERT + ', ' + self.ActiveJob.Product.ID
        strINSERT = strINSERT + ', \'' + ShortDate(mdl_Common.NowGMT()(), True, True, True) + '\''
        strINSERT = strINSERT + ', ' + self.Server.CurrentShiftID
        strINSERT = strINSERT + ', \'' + ShortDate(self.Server.CurrentShift.StartTime, True, True, True) + '\''
        if not BatchParams is None:
            for tVariant in BatchParams.keys:
                
                
                
                
                
                
                if BatchParams.Item(tVariant) != '':
                    if (tVariant == 'PEE') or (tVariant == 'EfficiencyTotal'):
                        if IsDoubleNull(self.ActiveJosh.CycleTimeEfficiency) or IsDoubleNull(self.ActiveJosh.RejectsEfficiency) or IsDoubleNull(self.ActiveJosh.CavitiesEfficiency) or IsDoubleNull(self.ActiveJosh.DownTimeEfficiency) or IsDoubleNull(self.ActiveJosh.DownTimeEfficiencyOEE):
                            strINSERT = strINSERT + ',NULL'
                        else:
                            strINSERT = strINSERT + ',' + IIf(Round(BatchParams.Item(tVariant), 5) == - 999999999, 'NULL', Round(BatchParams.Item(tVariant), 5))
                    elif (tVariant == 'CycleTimeEfficiency') or (tVariant == 'RejectsEfficiency') or (tVariant == 'CavitiesEfficiency') or (tVariant == 'DownTimeEfficiency') or (tVariant == 'DownTimeEfficiencyOEE'):
                        strINSERT = strINSERT + ',' + IIf(Round(BatchParams.Item(tVariant), 5) == - 999999999, 'NULL', Round(BatchParams.Item(tVariant), 5))
                    elif (tVariant == 'TotalCycles') or (tVariant == 'UnitsProducedTheoretically') or (tVariant == 'UnitsProducedTheoreticallyPC'):
                        if ( self.MachineStop or self.IOStatus == 0 ) :
                            strINSERT = strINSERT + ',NULL'
                        else:
                            strINSERT = strINSERT + ',' + BatchParams.Item(tVariant)
                    else:
                        strINSERT = strINSERT + ',' + BatchParams.Item(tVariant)
                else:
                    strINSERT = strINSERT + ',NULL'
                
        strINSERT = strINSERT + ') '
        
        MdlConnection.CN.execute(strINSERT)
        
        self.BatchReadLastRecord = mdl_Common.NowGMT()()
        returnVal = True
        if Err.Number != 0:
            
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('LeaderRT:WriteProdutionParametersToHistory', str(Err.Number), Err.Description, '')
            Err.Clear()
        tParam = None
        tVariant = None
        tControlParam = None
        strINSERT = vbNullString
        return returnVal

    def LaunchSystemAlarms(self):
        returnVal = None
        saRst = None

        PRst = None

        tSQL = ''

        MachineName = ''

        CompareValue = 0

        AlarmName = ''

        CurrentValue = 0

        MessageText = ''

        ActiveOnProductionMode = False

        MessageKeysValues = ''

        WorkingShift = False

        ActiveOnNonWorkingShift = False

        RepeatEveryShift = False
        
        returnVal = False
        
        
        
        
        
        
        
        
        
        
        
        MachineName = self.EName
        tSQL = 'SELECT * FROM ViewShiftMachineProductionDetailsFixed WHERE MachineID = ' + self.ID
        PRst.Open(tSQL, CN, adOpenStatic, adLockReadOnly)
        PRst.ActiveConnection = None
        if PRst.RecordCount == 0:
            PRstCursor.close()
            PRst = None
            return returnVal
        WorkingShift = MdlADOFunctions.fGetRstValBool(PRstData.WorkingShift, True)
        tSQL = 'SELECT * FROM STblSystemAlarms WHERE IsActive<>0 AND ID <> 12'
        saRst.Open(tSQL, CN, adOpenStatic, adLockReadOnly)
        saRst.ActiveConnection = None
        while not saRst.EOF:
            ActiveOnProductionMode = MdlADOFunctions.fGetRstValBool(saRst.Fields("ActiveOnProductionMode").Value, False)
            ActiveOnNonWorkingShift = MdlADOFunctions.fGetRstValBool(saRst.Fields("ActiveOnNonWorkingShift").Value, False)
            RepeatEveryShift = MdlADOFunctions.fGetRstValBool(saRst.Fields("RepeatEveryShift").Value, True)
            if not ActiveOnProductionMode and self.ProductionModeID > 1:
                GoTo(ContinueLoop)
            if not ActiveOnNonWorkingShift and not WorkingShift:
                GoTo(ContinueLoop)
            AlarmName = MdlADOFunctions.fGetRstValString(saRst.Fields("Name").Value)
            CompareValue = MdlADOFunctions.fGetRstValDouble(saRst.Fields("CompareValue").Value)
            if MdlADOFunctions.fGetRstValString(saRst.Fields("CompareValue").Value) == '' and MdlADOFunctions.fGetRstValString(saRst.Fields("CompareField").Value) != '':
                CompareValue = MdlADOFunctions.fGetRstValDouble(PRst.Fields(MdlADOFunctions.fGetRstValString(saRst.Fields("CompareField").Value)).value)
            CurrentValue = MdlADOFunctions.fGetRstValDouble(PRst.Fields(MdlADOFunctions.fGetRstValString(AlarmName)).value)
            if CurrentValue > CompareValue:
                MessageText = MdlADOFunctions.fGetRstValString(saRst.Fields("MessageText").Value)
                MessageText = Replace(MessageText, '{MachineName}', MachineName)
                MessageText = Replace(MessageText, '{CompareValue}', CompareValue)
                
                MessageKeysValues = ''
                MessageKeysValues = MessageKeysValues + '{'
                MessageKeysValues = MessageKeysValues + 'Name' + ';' + AlarmName
                MessageKeysValues = MessageKeysValues + ';' + 'MachineName' + ';' + MachineName
                MessageKeysValues = MessageKeysValues + ';' + 'CompareValue' + ';' + CompareValue
                MessageKeysValues = MessageKeysValues + ';' + 'MachineID' + ';' + self.ID
                MessageKeysValues = MessageKeysValues + ';' + 'DepartmentID' + ';' + self.Department
                
                
                
                MessageKeysValues = MessageKeysValues + '}'
                
                self.CreateSystemAlarm(MdlADOFunctions.fGetRstValLong(saRst.Fields("ID").Value), CurrentValue, MessageText, MessageKeysValues, 0, RepeatEveryShift)
                
            else:
                
                if not RepeatEveryShift:
                    tSQL = 'DELETE FROM TblSystemAlarms WHERE SystemAlarmID = ' + MdlADOFunctions.fGetRstValLong(saRst.Fields("ID").Value) + ' AND MachineID = ' + self.ID
                    MdlConnection.CN.execute(( tSQL ))
            saRst.MoveNext()
        saRst.close()
        returnVal = True
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            Err.Clear()
        if saRst.State != 0:
            saRst.close()
        if PRst.State != 0:
            PRstCursor.close()
        saRst = None
        PRst = None
        return returnVal

    def CreateSystemAlarm(self, SystemAlarmID, CurrentValue, MessageText, MessageKeysValues, TemplateID, RepeatEveryShift=True, ControllerFieldID=0):
        returnVal = None
        strSQL = ''

        Rst = None

        AlarmExists = False
        
        returnVal = False
        AlarmExists = False
        if ControllerFieldID == 0:
            if RepeatEveryShift:
                strSQL = 'SELECT * FROM TblSystemAlarms WHERE TemplateID = ' + TemplateID + ' AND MachineID = ' + self.ID + ' AND ShiftID = ' + self.Server.CurrentShiftID + ' AND SystemAlarmID = ' + SystemAlarmID
            else:
                strSQL = 'SELECT * FROM TblSystemAlarms WHERE TemplateID = ' + TemplateID + ' AND MachineID = ' + self.ID + ' AND SystemAlarmID = ' + SystemAlarmID
            Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            Rst.ActiveConnection = None
            if Rst.RecordCount != 0:
                AlarmExists = True
            RstCursor.close()
        if not AlarmExists:
            strSQL = 'INSERT INTO TblSystemAlarms '
            strSQL = strSQL + '('
            strSQL = strSQL + 'MachineID'
            strSQL = strSQL + ',ShiftID'
            strSQL = strSQL + ',JobID'
            strSQL = strSQL + ',SystemAlarmID'
            strSQL = strSQL + ',TemplateID'
            strSQL = strSQL + ',AlarmTime'
            strSQL = strSQL + ',CurrentValue'
            strSQL = strSQL + ',MessageText'
            strSQL = strSQL + ',MessageKeysValues'
            if ControllerFieldID > 0:
                strSQL = strSQL + ',ControllerFieldID'
            strSQL = strSQL + ')'
            strSQL = strSQL + ' VALUES '
            strSQL = strSQL + '('
            strSQL = strSQL + self.ID
            if RepeatEveryShift:
                strSQL = strSQL + ', ' + self.Server.CurrentShiftID
            else:
                strSQL = strSQL + ', 0'
            strSQL = strSQL + ', ' + self.ActiveJob.ID
            strSQL = strSQL + ', ' + SystemAlarmID
            strSQL = strSQL + ', ' + TemplateID
            strSQL = strSQL + ', \'' + ShortDate(mdl_Common.NowGMT()(), True, True) + '\''
            strSQL = strSQL + ', ' + CurrentValue
            strSQL = strSQL + ', \'' + strFixBadChars(MessageText) + '\''
            strSQL = strSQL + ', \'' + Replace(MessageKeysValues, '\'', '\'\'') + '\''
            
            if ControllerFieldID > 0:
                strSQL = strSQL + ', ' + ControllerFieldID
            strSQL = strSQL + ')'
            MdlConnection.CN.execute(strSQL)
        returnVal = True
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            Err.Clear()
        if Rst.State != 0:
            RstCursor.close()
        Rst = None
        return returnVal

    def CalculateEventDistributionID(self):
        returnVal = None
        tEventDistributionID = 0
        
        if self.NewJob:
            tEventDistributionID = 3
        elif self.ProductionModeID > 1:
            tEventDistributionID = 8
        elif self.Status == 2:
            tEventDistributionID = 7
        else:
            tEventDistributionID = 1
        returnVal = tEventDistributionID
        if Err.Number != 0:
            Err.Clear()
        return returnVal

    def CheckNoProgressCount(self):
        returnVal = None
        StopCount = 0
        
        returnVal = False
        
        if self.__mStopCyclesCount > 0:
            StopCount = self.__mStopCyclesCount
        else:
            StopCount = self.__cntStopCyclesCount
        if (self.MachineStopSetting == 1):
            if self.ProductionModeID == 1:
                
                if ( ( self.__mNoProgressCount >= CDbl(( self.__mCycleTimeStandard * StopCount )) )  and self.__mMachineStop == False )  or  ( self.__mMachineSignalStop == True and self.__mStopSignalExist == True ) :
                    returnVal = True
            else:
                
                if ( ( self.__mNoProgressCount >= CDbl(( self.__mDefaultCycleTime * StopCount )) )  and self.__mMachineStop == False )  or  ( self.__mMachineSignalStop == True and self.__mStopSignalExist == True ) :
                    returnVal = True
        elif (self.MachineStopSetting == 2):
            if ( ( self.__mNoProgressCount >= self.__mMachineStopSettingSetPoint )  and self.__mMachineStop == False ) :
                returnVal = True
            
            
        else:
            
            if ( ( self.__mNoProgressCount >= CDbl(( self.__mCycleTimeStandard * StopCount )) )  and self.__mMachineStop == False )  or  ( self.__mMachineSignalStop == True and self.__mStopSignalExist == True ) :
                returnVal = True
        if Err.Number != 0:
            Err.Clear()
        return returnVal
    
    def LaunchParameterSystemAlarm(self, pParam):
        returnVal = None
        saRst = None

        PRst = None

        tSQL = ''

        MachineName = ''

        CompareValue = 0

        AlarmName = ''

        CurrentValue = 0

        MessageText = ''

        ActiveOnProductionMode = False

        MessageKeysValues = ''

        WorkingShift = False

        ActiveOnNonWorkingShift = False

        RepeatEveryShift = False

        TemplateID = 0
        
        returnVal = False
        
        
        
        
        
        
        
        
        
        
        
        MachineName = self.EName
        
        
        
        
        
        
        
        WorkingShift = self.Server.CurrentShift.IsWorkingShift
        
        
        tSQL = 'SELECT * FROM ViewSTblSystemAlarmsForUserTemplatesDef WHERE IsActive<>0 AND SystemAlarmID = 12 ORDER BY TemplateID'
        saRst.Open(tSQL, CN, adOpenStatic, adLockReadOnly)
        saRst.ActiveConnection = None
        while not saRst.EOF:
            ActiveOnProductionMode = MdlADOFunctions.fGetRstValBool(saRst.Fields("ActiveOnProductionMode").Value, False)
            ActiveOnNonWorkingShift = MdlADOFunctions.fGetRstValBool(saRst.Fields("ActiveOnNonWorkingShift").Value, False)
            RepeatEveryShift = MdlADOFunctions.fGetRstValBool(saRst.Fields("RepeatEveryShift").Value, True)
            TemplateID = MdlADOFunctions.fGetRstValLong(saRst.Fields("TemplateID").Value)
            if not ActiveOnProductionMode and self.ProductionModeID > 1:
                GoTo(ContinueLoop)
            if not ActiveOnNonWorkingShift and not WorkingShift:
                GoTo(ContinueLoop)
            AlarmName = MdlADOFunctions.fGetRstValString(saRst.Fields("Name").Value)
            
            
            
            
            CurrentValue = MdlADOFunctions.fGetRstValDouble(pParam.LastValue)
            MessageText = MdlADOFunctions.fGetRstValString(saRst.Fields("MessageText").Value)
            MessageText = Replace(MessageText, '{MachineName}', MachineName)
            MessageText = Replace(MessageText, '{CompareValue}', CurrentValue)
            MessageText = Replace(MessageText, '{ParameterName}', pParam.EName)
            
            MessageKeysValues = ''
            MessageKeysValues = MessageKeysValues + '{'
            MessageKeysValues = MessageKeysValues + 'Name' + ';' + AlarmName
            MessageKeysValues = MessageKeysValues + ';' + 'MachineName' + ';' + MachineName
            MessageKeysValues = MessageKeysValues + ';' + 'CompareValue' + ';' + CurrentValue
            MessageKeysValues = MessageKeysValues + ';' + 'MachineID' + ';' + self.ID
            MessageKeysValues = MessageKeysValues + ';' + 'DepartmentID' + ';' + self.Department
            MessageKeysValues = MessageKeysValues + ';' + 'ParameterLName' + ';' + Replace(pParam.LName, Chr(34), '')
            MessageKeysValues = MessageKeysValues + ';' + 'ParameterEName' + ';' + Replace(pParam.EName, Chr(34), '')
            MessageKeysValues = MessageKeysValues + ';' + 'FieldName' + ';' + pParam.FName
            
            
            
            MessageKeysValues = MessageKeysValues + '}'
            
            
            self.CreateSystemAlarm(MdlADOFunctions.fGetRstValLong(saRst.Fields("SystemAlarmID").Value), CurrentValue, MessageText, MessageKeysValues, TemplateID, RepeatEveryShift, pParam.ID)
            
            saRst.MoveNext()
        saRst.close()
        returnVal = True
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            Err.Clear()
        if saRst.State != 0:
            saRst.close()
        if PRst.State != 0:
            PRstCursor.close()
        saRst = None
        PRst = None
        return returnVal

    # def UpdateMachineStatusTime(self, pDate=datetime.strptime('00:00:00')):
    def UpdateMachineStatusTime(self, pDate=None):
        strSQL = ''
        
        if pDate != datetime.strptime('00:00:00', "%d %B, %Y"):
            self.StatusLastChangeTime = pDate
        strSQL = 'Update TblMachines Set StatusLastChangeTime = \'' + MdlUtilsH.ShortDate(self.StatusLastChangeTime, True, True, True) + '\' Where ID=' + self.ID
        MdlConnection.CN.execute(strSQL)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:UpdateMachineStatusTime', '' + Err.Number, '' + Err.Description, 'MachineID = ' + self.ID)
            Err.Clear()

    def UpdateShiftMachineCycleTime(self, ShiftID, FirstCycle=False, LastCycle=False):
        ExistsID = 0

        strSQL = ''
        
        strSQL = ''
        
        if ShiftID == 0:
            return
        else:
            ExistsID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblShiftMachineData', 'ShiftID = ' + ShiftID + ' AND MachineID = ' + self.ID, 'CN'))
            if ExistsID == 0:
                
                strSQL = ''
                strSQL = strSQL + 'INSERT INTO TblShiftMachineData' + vbCrLf
                strSQL = strSQL + '(' + vbCrLf
                strSQL = strSQL + 'ShiftID' + vbCrLf
                strSQL = strSQL + ',MachineID' + vbCrLf
                if FirstCycle:
                    strSQL = strSQL + ',FirstCycleTime' + vbCrLf
                if LastCycle:
                    strSQL = strSQL + ',LastCycleTime' + vbCrLf
                strSQL = strSQL + ') VALUES (' + vbCrLf
                strSQL = strSQL + ShiftID + vbCrLf
                strSQL = strSQL + ',' + self.ID + vbCrLf
                if FirstCycle:
                    strSQL = strSQL + ',\'' + Format(mdl_Common.NowGMT()(), 'yyyy-mm-dd HH:nn:ss') + '\'' + vbCrLf
                if LastCycle:
                    strSQL = strSQL + ',\'' + Format(mdl_Common.NowGMT()(), 'yyyy-mm-dd HH:nn:ss') + '\'' + vbCrLf
                strSQL = strSQL + ')'
                MdlConnection.CN.execute(( strSQL ))
            else:
                
                if FirstCycle:
                    strSQL = ''
                    strSQL = strSQL + 'UPDATE TblShiftMachineData' + vbCrLf
                    strSQL = strSQL + 'SET' + vbCrLf
                    strSQL = strSQL + 'FirstCycleTime = \'' + Format(mdl_Common.NowGMT()(), 'yyyy-mm-dd HH:nn:ss') + '\'' + vbCrLf
                    strSQL = strSQL + 'WHERE FirstCycleTime IS NULL AND ID = ' + ExistsID
                    MdlConnection.CN.execute(( strSQL ))
                if LastCycle:
                    strSQL = ''
                    strSQL = strSQL + 'UPDATE TblShiftMachineData' + vbCrLf
                    strSQL = strSQL + 'SET' + vbCrLf
                    strSQL = strSQL + 'LastCycleTime = \'' + Format(mdl_Common.NowGMT()(), 'yyyy-mm-dd HH:nn:ss') + '\'' + vbCrLf
                    strSQL = strSQL + 'WHERE ID = ' + ExistsID
                    MdlConnection.CN.execute(( strSQL ))
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:UpdateShiftMachineCycleTime', '' + Err.Number, '' + Err.Description, 'MachineID = ' + self.ID + ', ShiftID = ' + ShiftID)
            Err.Clear()
            

    def GetStopReasonAndCreateEvent(self):
        strSQL = ''

        tEvent = RTEvent()

        Rst = None

        EventID = 0

        EventGroupID = 0
        
        
        
        
        
        
        if self.ActiveJob.OpenEvent is None:
            tEvent = RTEvent()
            
            if self.ProductionModeReasonID != 0:
                tEvent.Create(self, self.ProductionModeGroupReasonID, self.ProductionModeReasonID, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), VBGetMissingArgument(tEvent.Create, 6), self.MachineSignalStopTimestamp)
                
            elif self.ReportStopReasonByOpenCall:
                strSQL = ''
                strSQL = strSQL + 'SELECT TOP 1 EventGroupID, EventReasonID' + vbCrLf
                strSQL = strSQL + 'FROM ViewNotificationsOpenCalls' + vbCrLf
                strSQL = strSQL + 'WHERE SentTime >= DateAdd(d, -7, CONVERT(VarChar(10), GETDATE(), 121))' + vbCrLf
                strSQL = strSQL + 'AND SourceMachineID = ' + self.ID + ' AND EventReasonID > 0' + vbCrLf
                strSQL = strSQL + 'ORDER BY SentTime DESC'
                Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                Rst.ActiveConnection = None
                if Rst.RecordCount == 1:
                    EventID = MdlADOFunctions.fGetRstValLong(RstData.EventReasonID)
                    EventGroupID = MdlADOFunctions.fGetRstValLong(RstData.EventGroupID)
                    tEvent.Create(self, EventGroupID, EventID, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), VBGetMissingArgument(tEvent.Create, 6), self.MachineSignalStopTimestamp)
                else:
                    
                    if self.LineID > 0 and self.RootEventAttachDurationMin > 0:
                        RstCursor.close()
                        GoTo(EventFromLine)
                    else:
                        tEvent.Create(self, 6, 0, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), VBGetMissingArgument(tEvent.Create, 6), self.MachineSignalStopTimestamp)
                RstCursor.close()
                
                
            elif self.LineID > 0 and self.RootEventAttachDurationMin > 0:
                
                strSQL = ''
                strSQL = ''
                strSQL = strSQL + 'SELECT TOP 1 e.ID,Parent.ID AS ParentID,e.EventGroup,e.Event, Parent.EventGroup AS ParentEventGroup, Parent.Event AS ParentEvent,' + vbCrLf
                strSQL = strSQL + '(CASE WHEN ISNULL(e.Duration,0) < 0 THEN 0 ELSE (CASE WHEN e.EndTime IS NULL THEN DATEDIFF(n, e.EventTime, GETDATE()) ELSE e.Duration END) END) AS Duration,' + vbCrLf
                strSQL = strSQL + '(CASE WHEN ISNULL(Parent.Duration,0) < 0 THEN 0 ELSE (CASE WHEN Parent.EndTime IS NULL THEN DATEDIFF(n, Parent.EventTime, GETDATE()) ELSE Parent.Duration END) END) AS ParentDuration,' + vbCrLf
                strSQL = strSQL + 'e.RootEventID,Parent.EndTime AS ParentEndTime, DATEDIFF(n,Parent.EndTime,GETDATE()) AS TimeSinceParent' + vbCrLf
                strSQL = strSQL + 'FROM TblEvent e WITH (NOLOCK) LEFT OUTER JOIN' + vbCrLf
                strSQL = strSQL + '    TblEvent Parent WITH (NOLOCK) ON Parent.PConfigParentID = 0 AND e.RootEventID = Parent.ID' + vbCrLf
                strSQL = strSQL + 'Where e.EventGroup <> 20 AND e.PConfigParentID = 0 And e.Event <> 18 And e.IsCalendarEvent = 0' + vbCrLf
                strSQL = strSQL + 'AND (e.EndTime IS NULL)' + vbCrLf
                strSQL = strSQL + 'AND e.MachineID IN(SELECT MachineID FROM ViewLinesMachines WHERE ProductionModeID = 1 AND LineID = ' + self.LineID + ')' + vbCrLf
                strSQL = strSQL + 'AND e.JobID IN(SELECT ID FROM TblJobCurrent WITH (NOLOCK) WHERE ERPJobIndexKey = \'' + self.ActiveJob.ERPJobIndexKey + '\')' + vbCrLf
                strSQL = strSQL + 'ORDER BY e.RootEventID, e.ID DESC'
                Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                Rst.ActiveConnection = None
                if Rst.RecordCount == 1:
                    
                    if MdlADOFunctions.fGetRstValLong(RstData.RootEventID) == 0:
                        EventID = MdlADOFunctions.fGetRstValLong(RstData.event)
                        EventGroupID = MdlADOFunctions.fGetRstValLong(RstData.EventGroup)
                        tEvent.Create(self, EventGroupID, EventID, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), MdlADOFunctions.fGetRstValLong(RstData.ID), self.MachineSignalStopTimestamp)
                        
                    elif MdlADOFunctions.fGetRstValLong(RstData.TimeSinceParent) <= self.RootEventAttachDurationMin:
                        EventID = MdlADOFunctions.fGetRstValLong(RstData.ParentEvent)
                        EventGroupID = MdlADOFunctions.fGetRstValLong(RstData.ParentEventGroup)
                        tEvent.Create(self, EventGroupID, EventID, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), MdlADOFunctions.fGetRstValLong(RstData.ParentID), self.MachineSignalStopTimestamp)
                    else:
                        tEvent.Create(self, 6, 0, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), VBGetMissingArgument(tEvent.Create, 6), self.MachineSignalStopTimestamp)
                else:
                    tEvent.Create(self, 6, 0, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), VBGetMissingArgument(tEvent.Create, 6), self.MachineSignalStopTimestamp)
                RstCursor.close()
            else:
                tEvent.Create(self, 6, 0, '', self.ActiveJob, VBGetMissingArgument(tEvent.Create, 5), VBGetMissingArgument(tEvent.Create, 6), self.MachineSignalStopTimestamp)
            self.ActiveJob.OpenEvent = tEvent
            self.UpdateMachineStatusTime(mdl_Common.NowGMT()())
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.close()
                MetaCn.Open()
                Err.Clear()
                
            RecordError('Machine:GetStopReasonAndCreateEvent', '' + Err.Number, '' + Err.Description, 'MachineID = ' + self.ID + ', JobID = ' + self.ActiveJob.ID)
            Err.Clear()
            
            if Rst.State == 1:
                RstCursor.close()
        tEvent = None
        Rst = None


    def setReportStopReasonByOpenCall(self, value):
        self.__mReportStopReasonByOpenCall = value

    def getReportStopReasonByOpenCall(self):
        returnVal = None
        returnVal = self.__mReportStopReasonByOpenCall
        return returnVal
    ReportStopReasonByOpenCall = property(fset=setReportStopReasonByOpenCall, fget=getReportStopReasonByOpenCall)


    def setEngineSignalActive(self, value):
        self.__mEngineSignalActive = value

    def getEngineSignalActive(self):
        returnVal = None
        returnVal = self.__mEngineSignalActive
        return returnVal
    EngineSignalActive = property(fset=setEngineSignalActive, fget=getEngineSignalActive)


    def setEngineSignalExist(self, value):
        self.__mEngineSignalExist = value

    def getEngineSignalExist(self):
        returnVal = None
        returnVal = self.__mEngineSignalExist
        return returnVal
    EngineSignalExist = property(fset=setEngineSignalExist, fget=getEngineSignalExist)

    def setTotalCycles(self, value):
        self.__mTotalCycles = value

    def getTotalCycles(self):
        returnVal = None
        returnVal = self.__mTotalCycles
        return returnVal
    TotalCycles = property(fset=setTotalCycles, fget=getTotalCycles)


    def setTotalWeight(self, the_mTotalWeight):
        strSQL = ''
        tParam = None
        self.__mTotalWeight = the_mTotalWeight

        try:
            if self.__mTotalWeight > mTotalWeightLast:
                mTotalWeightDiff = self.__mTotalWeight - mTotalWeightLast
            else:
                if self.IsOffline:
                    mTotalWeightDiff = self.__mTotalWeight - mTotalWeightLast
                else:
                    mTotalWeightDiff = 0
            strSQL = 'Update TblControllers Set TotalWeight = ' + str(self.__mTotalWeight) + ' Where ID = ' + str(self.__mControllerID)
            MdlConnection.CN.execute(strSQL)
            if GetParam('TotalWeight', tParam) == True:
                if not ( tParam.OPCItemHandle > 0 ) :
                    tParam.LastValue = the_mTotalWeight

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)

    def getTotalWeight(self):
        returnVal = None
        returnVal = self.__mTotalWeight
        return returnVal
    TotalWeight = property(fset=setTotalWeight, fget=getTotalWeight)

