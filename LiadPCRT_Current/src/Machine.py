import MdlADOFunctions
import MdlConnection

class Machine:
    __mID = 0
    __mTypeID = ''
    __mLName = ''
    __mEName = ''
    __mDescr = ''
    __mMachineType = 0
    __mStatus = ''
    __mActiveJobID = 0
    # __mActiveJob = Job()
    # __mActiveJosh = Josh()
    __mActiveJoshID = 0
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
    # __mResetTotals = Collection()
    # __mUpdateAddress = ControlParam()
    # __mUpdateResetAddress = ControlParam()
    __mLastShrinkTime = None
    __mJobStartTime = ''
    __mShrinkDataInterval = 0
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
    # __mControllerChannels = Collection()
    # __mBatchTrigerP = ControlParam()
    # __mBatchUpdateP = ControlParam()
    # __mOPCServer = OPCServer()
    # __mCParams = Collection()
    # __mOPCGroupGeneral = OPCGroup()
    __mHasBatchParams = False
    __mBatchTrigerSet = False
    __mBatchTrigerField = ''
    __mBatchUpdateField = ''
    __mBatchReadTable = ''
    __mCParamsServerHandles = 0
    __mCParamsErrors = 0
    __mBTServerHandles = 0
    __mBTErrors = 0
    mIOCancelID = 0
    # mIOGroup = OPCGroup()
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
    # __mStatusParam = ControlParam()
    # __mRejectsParam = ControlParam()
    __mStatusParamSet = False
    __mReadFailCount = 0
    __mReadWaitCount = 0
    __mRejectsParamSet = False
    __mRejects = 0
    __mTimeLeftHr = 0
    __mTotalCyclesAutoAdvance = False
    __mWeightDistanceRatioReset = False
    __mAlarmsActive = False
    __mAlarmsParams = ''
    __mAlarmsParamCount = 0
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
    __mPConfigJobs = 0
    __mPConfigJobsInjections = 0
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
    # __mServer = Server()
    # __mMainList = Collection()
    # __mControllerList = Collection()
    # __mChannelList = Collection()
    # mTaskTriggers = Collection()
    __mMainListXML = ''
    __mControllerXML = ''
    __mChannelXML = ''
    __mDSIsActive = False
    __mManualRead = False
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
    # __mValidations = Collection()
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
    TypeId = property(fset=setTypeId, fget=getTypeId)


    
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
        if str(self.__mActiveMoldID).isnumeric():
            returnVal = self.__mActiveMoldID
        return returnVal
    ActiveMoldID = property(fset=setActiveMoldID, fget=getActiveMoldID)


    
    def setLastMoldID(self, the_mLastMoldID):
        self.__mLastMoldID = the_mLastMoldID

    def getLastMoldID(self):
        returnVal = None
        if str(self.__mLastMoldID).isnumeric():
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


    def INITMachine(self, MachineID, vOpcServer):
        returnVal = None
        strSQL = ''
        RstCursor = None
        validateRstCursor = None
        PRstCursor = None
        rVal = 0
        strGroupName = ''
        ChannelSplits = 0
        temp = ''
        # tControllerChannel = Channel()
        returnVal = False
        mUPDController = False
        mOPCServer = vOpcServer

        if MachineID == 2:
            returnVal = self.INITMachine()
        strSQL = 'Select * From TblMachines Where ID = ' + str(MachineID)

        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstData = RstCursor.fetchone()
        
        if RstData:
            mID = MachineID
            mTypeID = MdlADOFunctions.fGetRstValLong(RstData.TypeID)
            mLName = '' + RstData.MachineLName
            mEName = '' + RstData.MachineName
            mDepartment = MdlADOFunctions.fGetRstValLong(RstData.Department)
            mControllerDefID = MdlADOFunctions.fGetRstValLong(RstData.ControllerDefID)
            mControllerID = MdlADOFunctions.fGetRstValLong(RstData.ControllerID)
            mMachineSize = MdlADOFunctions.fGetRstValDouble(RstData.MachineSize)
            mMachineLoad = MdlADOFunctions.fGetRstValDouble(RstData.MachineLoad)
            mDownHourCost = MdlADOFunctions.fGetRstValDouble(RstData.DownHourCost)
            mWorkHourCost = MdlADOFunctions.fGetRstValDouble(RstData.WorkHourCost)
            mRunJobDetailsCalc = MdlADOFunctions.fGetRstValBool(RstData.RunJobDetailsCalc, True)
            mAlertOnStopSuction = MdlADOFunctions.fGetRstValBool(RstData.AlertOnStopSuction, False)
            mStopSignalExist = MdlADOFunctions.fGetRstValBool(RstData.StopSignalExist, False)
            mCycleFilterHValue = MdlADOFunctions.fGetRstValDouble(RstData.CycleFilterHValue)
            mCycleFilterLValue = MdlADOFunctions.fGetRstValDouble(RstData.CycleFilterLValue)
            mMaxCycleTime = MdlADOFunctions.fGetRstValDouble(RstData.MaxCycleTime)
            mCalcCycleTime = MdlADOFunctions.fGetRstValBool(RstData.CalcCycleTime, False)
            mMaterialCalc = MdlADOFunctions.fGetRstValBool(RstData.MaterialCalc, True)
            mReseTotalCycles = MdlADOFunctions.fGetRstValBool(RstData.ReseTotalCycles, False)
            mAlarmFile = '' + RstData.AlarmFile
            mAutoAlarmClerance = MdlADOFunctions.fGetRstValBool(RstData.AutoAlarmClearance, True)
            mStopSignal = MdlADOFunctions.fGetRstValLong(RstData.StopSignal)
            mStopCyclesCount = MdlADOFunctions.fGetRstValDouble(RstData.StopCyclesCount)
            mCycleTimeFilter = MdlADOFunctions.fGetRstValBool(RstData.CycleTimeFilter, True)
            mIPCProductWeightCountRatio = MdlADOFunctions.fGetRstValDouble(RstData.IPCProductWeightCountRatio)
            SetUpEndGeneralCycles = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndGeneralCycles)
            mSetUpEndProductWeightCycles = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndProductWeightCycles)
            mSetUpEndCycleTimeCycles = MdlADOFunctions.fGetRstValDouble(RstData.SetUpEndCycleTimeCycles)
            mSetUpEndPWCTRelation = MdlADOFunctions.fGetRstValLong(RstData.SetUpEndPWCTRelation)
            mAutoJobStartTimeCyclesWork = MdlADOFunctions.fGetRstValDouble(RstData.AutoJobStartTimeCyclesWork)
            mAutoJobStartOnUnitsOverTarget = MdlADOFunctions.fGetRstValDouble(RstData.AutoJobStartOnUnitsOverTarget)
            mTotalCyclesAutoAdvance = MdlADOFunctions.fGetRstValBool(RstData.TotalCyclesAutoAdvance, False)
            mWeightDistanceRatioReset = MdlADOFunctions.fGetRstValBool(RstData.WeightDistanceRatioReset, False)
            mMachineType = MdlADOFunctions.fGetRstValLong(RstData.TypeId)
            mManualRead = MdlADOFunctions.fGetRstValBool(RstData.ManualRead, False)
            mEnableAlarmsDuringSetup = MdlADOFunctions.fGetRstValBool(RstData.EnableAlarmsDuringSetup, False)
            mEnableAlarmsDuringMachineStop = MdlADOFunctions.fGetRstValBool(RstData.EnableAlarmsDuringMachineStop, False)
            
            mSetupEventIDOnSetupEnd = MdlADOFunctions.fGetRstValLong(RstData.SetupEventIDOnSetupEnd)
            mSetupEventIDOnShiftEnd = MdlADOFunctions.fGetRstValLong(RstData.SetupEventIDOnShiftEnd)
            mReportRejectsUnReported = MdlADOFunctions.fGetRstValBool(RstData.ReportRejectsUnReported, False)
            mMoldEndTimeStatusOption = MdlADOFunctions.fGetRstValLong(RstData.MoldEndTimeStatusOption)
            mMoldEndTimeCalcOption = MdlADOFunctions.fGetRstValLong(RstData.MoldEndTimeCalcOption)
            mIsOffline = MdlADOFunctions.fGetRstValBool(RstData.IsOffline, False)
            mAddRejectsOnSetupEnd = MdlADOFunctions.fGetRstValBool(RstData.AddRejectsOnSetupEnd, True)
            mCalcChannel100MaterialByCavity = MdlADOFunctions.fGetRstValBool(RstData.CalcChannel100MaterialByCavity, True)
            mDynamicWareHouseLocation = MdlADOFunctions.fGetRstValBool(RstData.DynamicWareHouseLocation, False)
            mAllowAutoRejectsOnSetup = MdlADOFunctions.fGetRstValBool(RstData.AllowAutoRejectsOnSetup, True)
            mConnectedByOPC = MdlADOFunctions.fGetRstValBool(RstData.ConnectedByOPC, True)
            mMonitorSetupWorkingTime = MdlADOFunctions.fGetRstValBool(RstData.MonitorSetupWorkingTime, False)
            temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CycleTimeEffFactor', 'STblDepartments', 'ID = ' + str(mDepartment), 'CN'))
            if temp == '':
                temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'CycleTimeEffFactor\'', 'CN'))
                if temp == '':
                    temp = 1
            mCycleTimeEffFactor = MdlADOFunctions.fGetRstValDouble(temp)
            temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('MachineTimeEffFactor', 'STblDepartments', 'ID = ' + str(mDepartment), 'CN'))
            if temp == '':
                temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'MachineTimeEffFactor\'', 'CN'))
                if temp == '':
                    temp = 1
            mMachineTimeEffFactor = MdlADOFunctions.fGetRstValDouble(temp)
            temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('RejectsEffFactor', 'STblDepartments', 'ID = ' + str(mDepartment), 'CN'))
            if temp == '':
                temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'RejectsEffFactor\'', 'CN'))
                if temp == '':
                    temp = 1
            mRejectsEffFactor = MdlADOFunctions.fGetRstValDouble(temp)
            temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CavitiesEffFactor', 'STblDepartments', 'ID = ' + str(mDepartment), 'CN'))
            if temp == '':
                temp = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'CavitiesEffFactor\'', 'CN'))
                if temp == '':
                    temp = 1
            mCavitiesEffFactor = MdlADOFunctions.fGetRstValDouble(temp)
            mDSIsActive = MdlADOFunctions.fGetRstValBool(RstData.DSIsActive, False)
            mStartCalcAfterDelayInSeconds = MdlADOFunctions.fGetRstValLong(RstData.StartCalcAfterDelayInSeconds)
            mUnitsInCycleType = MdlADOFunctions.fGetRstValLong(RstData.UnitsInCycleType)
            if mUnitsInCycleType == 0:
                mUnitsInCycleType = 1
            mLocationBatchChangeSetupModeID = MdlADOFunctions.fGetRstValLong(RstData.LocationBatchChangeSetupModeID)
            mLocationBatchChangeSetupValue = MdlADOFunctions.fGetRstValDouble(RstData.LocationBatchChangeSetupValue)
            mActivePalletInventoryID = MdlADOFunctions.fGetRstValLong(RstData.ActivePalletInventoryID)
            mAutoPrintLabel = MdlADOFunctions.fGetRstValBool(RstData.AutoPrintLabel, False)
            mUpdateAddressOnJobActive = MdlADOFunctions.fGetRstValBool(RstData.UpdateAddressOnJobActive, False)
            mActivePalletCreationModeID = MdlADOFunctions.fGetRstValLong(RstData.ActivePalletCreationModeID)
            mProductionModeID = MdlADOFunctions.fGetRstValLong(RstData.ProductionModeID)
            if mProductionModeID == 0:
                mProductionModeID = 1
            
            strSQL = 'SELECT * FROM STblProductionModes WHERE ID = ' + mProductionModeID

            PRstCursor = MdlConnection.CN.cursor()
            PRstCursor.execute(strSQL)
            PRstData = PRstCursor.fetchone()

            if PRstData:
                mProductionModeReasonID = MdlADOFunctions.fGetRstValLong(PRstData.EventReasonID)
                mProductionModeGroupReasonID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('EventGroupID', 'STblEventDesr', 'ID = ' + mProductionModeReasonID))
                mProductionModeDisableProductionTime = MdlADOFunctions.fGetRstValBool(PRstData.DisableProductionTime, False)
                mProductionModeCalcEfficiencies = MdlADOFunctions.fGetRstValBool(PRstData.CalcEfficiencies, False)
                mProductionModeOverCalendarEvent = MdlADOFunctions.fGetRstValBool(PRstData.OverCalendarEvent, True)
            PRstCursor.close()
            
            mMachineStopSetting = MdlADOFunctions.fGetRstValLong(RstData.MachineStopSetting)
            if mMachineStopSetting == 0:
                mMachineStopSetting = 1
            mMachineStopSettingSetPoint = MdlADOFunctions.fGetRstValDouble(RstData.MachineStopSettingSetPoint)
            mDefaultCycleTime = MdlADOFunctions.fGetRstValDouble(RstData.DefaultCycleTime)
            if mDefaultCycleTime == 0:
                mDefaultCycleTime = 30
            
            if MdlADOFunctions.fGetRstValString(RstData.StatusLastChangeTime) != '':
                mStatusLastChangeTime = RstData.StatusLastChangeTime
            mDisconnectWorkerOnShiftChange = MdlADOFunctions.fGetRstValBool(RstData.DisconnectWorkerOnShiftChange, False)
            mContinueEventReasonOnShiftChange = MdlADOFunctions.fGetRstValBool(RstData.ContinueEventReasonOnShiftChange, True)
            mActiveCalendarEvent = MdlADOFunctions.fGetRstValBool(RstData.ActiveCalendarEvent, False)
            mActiveCalendarEventProductionModeID = MdlADOFunctions.fGetRstValLong(RstData.ActiveCalendarEventProductionModeID)
            mEngineSignal = MdlADOFunctions.fGetRstValLong(RstData.EngineSignal)
            mEngineSignalExist = MdlADOFunctions.fGetRstValBool(RstData.EngineSignalExist, False)
            mReportStopReasonByOpenCall = MdlADOFunctions.fGetRstValBool(RstData.ReportStopReasonByOpenCall, False)
        else:
            raise Exception('No records in TblMachines.')
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
            mRejectsReadOption = '' + MdlADOFunctions.fGetRstValString(RstData.RejectsRead)
            mUnitsReportedOKOption = '' + MdlADOFunctions.fGetRstValString(RstData.UnitsReportedOK)
        RstCursor.close()
        
        strSQL = 'Select * From TblControllers Where ID = ' + mControllerID

        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstData = RstCursor.fetchone()

        if str(RstData.BatchIDTag)  != '' and  str(RstData.BatchReadTable)  != '':
            mHasBatchParams = True
            mBatchReadTable = '' + RstData.BatchReadTable
            mBatchTrigerField = '' + RstData.BatchIDTag
            mBatchUpdateField = '' + RstData.BatchIDTagW
        else:
            mHasBatchParams = False
        if str(RstData.Job).isnumeric():
            
            strSQL = 'Select ID From TblJobCurrent Where ID = ' + MdlADOFunctions.fGetRstValLong(RstData.Job) + ' AND MachineID = ' + str(self.ID)

            validateRstCursor = MdlConnection.CN.cursor()
            validateRstCursor.execute(strSQL)
            validateRstData = validateRstCursor.fetchone()

            if validateRstData:
                self.ActiveJobID = RstData.Job
            else:
                self.ActiveJobID = 0
            validateRst.close()

        if str(RstData.Job).isnumeric() and Server.CurrentShiftID > 0:
            strSQL = 'Select ID From TblJoshCurrent Where JobID = ' + MdlADOFunctions.fGetRstValLong(RstData.Job) + ' AND MachineID = ' + str(self.ID) + ' AND ShiftID = ' + Server.CurrentShiftID
            validateRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            validateRst.ActiveConnection = None
            if not validateRst.EOF:
                self.ActiveJoshID = validateRst.Fields("ID").Value
            else:
                self.ActiveJoshID = 0
            validateRst.close()
        mTotalWeight = MdlADOFunctions.fGetRstValDouble(RstData.TotalWeight)
        mTotalWeightLast = self.TotalWeight
        mTotalWeightDiff = 0
        if MdlADOFunctions.fGetRstValString(RstData.LastCalcTime) != '':
            self.LastCalcTime = ShortDate(RstData.LastCalcTime, True, True)
        RstCursor.close()
        strGroupName = 'M_' + mID + '_General'
        mOPCGroupGeneral = mOPCServer.OPCGroups.Add()
        mOPCGroupGeneral.IsActive = True
        mOPCGroupGeneral.IsSubscribed = True
        
        mOPCGroupGeneral.UpdateRate = GeneralGroupRefreshRate
        
        rVal = ControllerFieldsLoad(mControllerID)
        if self.ActiveJobID > 0:
            JobLoad(self.ActiveJobID, False, False, True)
            strSQL = 'Delete TblJobCurrent Where MachineID = ' + mID + ' AND ID <> ' + mActiveJobID + ' AND PConfigParentID <> ' + mActiveJobID
            CN.Execute(strSQL)
            
        if mActiveJobID > 0:
            fInitMachineTriggers(Me, mActiveJobID, True)
        else:
            fInitMachineTriggers(Me, VBGetMissingArgument(fInitMachineTriggers, 1), True)
        
        LoadMachineValidations(Me)
        
        CheckIfDosingSystem
        mUPDController = True
        mIgnoreCycleTimeFilter = False
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
        if validateRst.State != 0:
            validateRst.close()
        validateRst = None
        tControllerChannel = None
        
        return returnVal

