from datetime import datetime
from DataSample import DataSample
from GlobalVariables import IsNumeric

import numbers
import ValidateValue
import MdlADOFunctions
import mdl_Common
import MdlConnection
import MdlGlobal
import MdlStatistics

class ControlParam:

    __cntDeviceDisableIntervalSec = 300
    __mID = 0
    __mFName = ''
    __mLName = ''
    __mEName = ''
    __mFieldID = 0
    __mChannelID = 0
    __mChannelNum = 0
    __mPropertyID = 0
    __mLastValue = ''
    __mSPLastValue = ''
    __mSPLValue = ''
    __mSPHValue = ''
    __mWriteValue = ''
    __mLastSampleTime = None
    __mPrevSampleTime = None
    __mQuality = None
    __mTimeStamp = None
    __mPrecision = 0
    __mTagName = ''
    __mTagNameW = ''
    __mHasWriteTag = False
    __mCVarAddress = ''
    __mCalcFunction = ''
    __mStrVal = ''
    __mPrevValue = ''
    __mSPPrevValue = ''
    __mSPLPrevValue = ''
    __mSPHPrevValue = ''
    __mInMainTable = False
    __mPMachine = None
    mBoolSyncWriteErr = False
    RawZero = 0
    RawFull = 0
    ScaledZero = 0
    ScaledFull = 0
    ScaledA = 0
    ScaledB = 0
    __mSyncWrite = False
    __mFieldDataType = 0
    __mCitectDeviceType = 0
    __mDirectRead = False
    __mIsBatchTriger = False
    __mBatchTable = ''
    __mBatchParams = {}
    __mBatchUpdateParam = None
    __tserver = None
    __mInBatchRead = False
    __mBatchTablesCount = 0
    __mBatchTables = ''
    __mBatchTableHistory = False
    __mSourceTableName = ''
    __mSourceFieldName = ''
    __mSourceStrWhere = ''
    __mBatchTableHistoryOnMachineStop = False
    __mDataSamples = {}
    __mAlarms = {}
    __mActions = {}
    __mActionsAreValid = False
    __mIsSPCValue = False
    __mSPCTable = ''
    __mSPCSamplesMaxCount = 0
    __mSPCSamplesCount = 0
    __mSPCGroupSize = 0
    __mSMean = 0
    __mUCL = 0
    __mLCL = 0
    __mMean = 0
    __mPUCL = 0
    __mPLCL = 0
    __mQUCL = 0
    __mQLCL = 0
    __mSTDEV = 0
    __mErrorCount = 0
    __mErrorCountAlarm = 0
    __mErrorAlarmActive = False
    __mErrorAlarmActiveVoice = False
    __mErrorAlarmOn = False
    __mSendSMSOnAlarm = False
    __mLastAlarmValue = 0
    __mLastAlarmRef = ''
    __mLastAlarmLimit = 0
    __mAlarmFile = ''
    __mAlarmArea = 0
    __mAlarmPerminentAcknowledge = False
    __mAlarmCycleAcknowledge = False
    __mAlarmFirstDetected = None
    __mAlarmFileLastPlay = None
    __mAlarmFileReplayInterval = 0
    __mAlarmMinimumDuration = 0
    __mIgnoreAlarmAcknowledge = False
    __mEnableAlarmsDuringSetup = False
    __mSendPushOnAlarm = False
    __mOPCItem = None
    __mOPCItemHandle = 0
    __mSPOPCItem = None
    __mSPOPCItemHandle = 0
    __mOPCItemW = None
    __mSPLOPCItem = None
    __mSPLOPCItemHandle = 0
    __mSPHOPCItem = None
    __mSPHOPCItemHandle = 0
    __mOPCItemWHandle = 0
    __mOPCGroupHandle = 0
    __mBatchServerHandles = []
    __mBatchValues = []
    __mErrors = []
    __mBatchCounter = 0
    __mBatchReadFailCount = 0
    __mInRead = False
    __mInWrite = False
    __mBatchWriteFailCount = 0
    __mWriteServerHandles = []
    __mWriteValues = []
    __mWritevErrors = []
    __mXML = ''
    __mAlarmXML = ''
    __mBatchGroup = None
    __mBatchGroupHandle = 0
    __mOPCServer = None
    __mSPCVals = []
    __mRejectReasonID = 0
    __mRejectReasonOption = 0
    __mRejectsAReadCurrent = 0
    __mRejectsAReadLast = 0
    __mRejectsAReadDiff = 0
    __mRejectsA = 0
    __mRejectsALast = 0
    __mRejectsADiff = 0
    __mRejectsIncludeInRejectsTotal = False
    __mRejectReasonDirectRead = False
    __mChangeJobOnValueChanged = False
    __mPrintLabelID = 0
    __mPrintLabelMachineID = 0
    __mCalstringExpression = ''
    __mLastInventoryLabelBatch = ''
    __mChangeJobOnValueChangedSourceTable = ''
    __mChangeJobOnValueChangedSourceField = ''
    __mValidateValue = False
    __mMinValueUnitsPerMin = 0
    __mMaxValueUnitsPerMin = 0
    __mForceValueTimeout = 0
    __mLastValidValue = ''
    __mLastValidSampleTime = None
    __mPrevValidValue = ''
    __mFirstReadInCurrentJob = False
    __mCalcDelayPassed = False
    __mStartCalcAfterDelayInSeconds = 0
    __mBatchReadLastRecord = None
    __mLastRecordToTSPCHistoryTableTS = None
    __mReportInventoryItemOnChange = 0
    __mEffectiveAmountFieldName = ''
    __mReportInventoryItemOnChangeInterval = 0
    __mWriteConditionalControllerField = None
    __mWriteConditionalMinValue = 0
    __mWriteConditionalMaxValue = 0
    __mControllerFieldTypeID = 0
    __mRefReadControllerField = None
    __mRefWriteControllerField = None
    __mConversionID = 0
    __mUpdateActivePallet = False
    __mCheckValidateValue = ValidateValue.ValidateValue()
    __mOPCDataTypeID = 0
    __mCalcByDiff = False
    __mdReadValue = ''
    __mdLastValidValue = ''
    __mdPrevValue = ''
    __mdDiffValue = ''
    __mdResetSuspect = False
    __mExternalUpdate = False
    __mdLastReadTime = None
    __mCalcByDiffValidate = False
    __mdLastValidReadTime = None
    __mBufferEnabled = False
    __mCalcMainDataOnBuffer = False
    __mSendEmailOnAlarm = False
    __mRoundType = 0
    __mCalcByDiffWithScaling = False
    __mCalcByDiffScalingRound = 0
    __mdLowLimit = 0
    __mdHighLimit = 0
    __mIOStatus = 0
    __mLastIOTime = None

    def __init__(self):
        self.__mPrevValue = ''
        self.__mLastValue = ''
        self.__mIsBatchTriger = False
        self.__mInBatchRead = False
        self.__mHasWriteTag = False
        
        

    def __del__(self):
        Counter = 0
        
        if self.__mIsBatchTriger == True:
            for Counter in range(0, len(self.__mBatchParams)):
                del self.__mBatchParams[Counter]

        if self.__mIsBatchTriger == True:
            self.__mBatchGroup = None


    def GetListData(self, InnerLoop=False):
        returnVal = None
        rVal = 0

        Counter = 0

        tVal = None

        strSQL = ''

        Sigma = 0

        ToSigma = 0

        NewRead = False

        RejectsDiff = 0

        ChangeJobPath = ''

        PrintLabelPath = ''

        JobStatus = 0

        ReadTries = Integer()

        tMachine = Machine()

        tDataSample = DataSample()

        tActiveJobID = 0

        LabelGroupID = 0

        LabelDataParam = ControlParam()

        strLabelData = ''

        InventoryID = 0

        ProductID = 0

        JobID = 0

        tValuesDiff = 0

        tAlarmCanceled = False

        tPrevSampleTime = None

        tWareHouseLocationID = 0

        tWareHouseID = 0

        Rst = ADODB.Recordset()

        OnBuffer = False

        temp = ''
        
        returnVal = False
        NewRead = False
        
        
        if self.CalcDelayPassed == False:
            if not self.pMachine.ActiveJob is None:
                if DateDiff('s', self.pMachine.ActiveJob.StartTime, mdl_Common.NowGMT) >= self.StartCalcAfterDelayInSeconds and DateDiff('s', self.pMachine.Server.StartTime, mdl_Common.NowGMT) >= self.StartCalcAfterDelayInSeconds:
                    self.CalcDelayPassed = True
                else:
                    returnVal = True
                    return returnVal
        
        
        OnBuffer = False
        if InnerLoop == False and self.ExternalUpdate == True and self.BufferEnabled == True:
            strSQL = 'SELECT * FROM TblControllerFieldsUpdateBuffer WHERE ValueRead = 0 AND ControllerFieldID = ' + self.__mID + ' ORDER BY TimeStamp'
            Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            Rst.ActiveConnection = None
            while not Rst.EOF:
                OnBuffer = True
                strSQL = ''
                strSQL = 'UPDATE TblControllerFields SET dReadValue = \'' + MdlADOFunctions.fGetRstValString(Rst.Fields("value").Value) + '\' , dLastReadTime=\'' + ShortDate(Rst.Fields("TimeStamp").Value, True, True, True) + '\' WHERE ID = ' + self.__mID
                MdlConnection.CN.execute(( strSQL ))
                if self.__mFName == 'MachineStop':
                    self.pMachine.MachineSignalStopTimestamp = CDate(Rst.Fields("TimeStamp").Value)
                self.GetListData(True)
                strSQL = 'UPDATE TblControllerFieldsUpdateBuffer SET ValueRead = 1 WHERE ID = ' + MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
                MdlConnection.CN.execute(( strSQL ))
                if self.CalcMainDataOnBuffer:
                    
                    self.pMachine.fReadMainData(True, True)
                Rst.MoveNext()
            Rst.Close()
            if OnBuffer == True:
                returnVal = True
                return returnVal
        if self.__mFName == 'MachineStop' and self.BufferEnabled == False:
            self.pMachine.MachineSignalStopTimestamp = CDate('00:00:00')
        self.ActionsAreValid = True
        if self.Actions.Count > 0:
            fExecutePreActions(Me)
        if self.ControllerFieldTypeID == 2:
            self.RefReadControllerField.GetListData
            self.__mLastValue = self.RefReadControllerField.LastValue
            

            tVal = self.__mLastValue
            strSQL = 'Update TblControllerFields Set CurrentValue = \'' + self.__mLastValue + '\' Where ID = ' + self.__mID
            MdlConnection.CN.execute(strSQL)
            NewRead = True
        else:
            tPrevSampleTime = self.__mPrevSampleTime
            if self.__mOPCItemHandle == 0 or  ( self.__mCalcFunction != '0' and self.__mCalcFunction != '' ) :
                
                if self.__mdLastValidReadTime == CDate('00:00:00') and self.__mdLastReadTime > CDate('00:00:00'):
                    self.__mdLastValidReadTime = self.__mdLastReadTime
                
                
                self.CalcParam()
                
                NewRead = True
                if self.ConversionID != 0:
                    self.__mLastValue = GetValueFromConversion(self.ConversionID, self.__mLastValue)
                tVal = self.__mLastValue
                
                
                if self.CalcByDiff == True:
                    
                    
                    
                    self.SetCalcByDiff(tVal)
                    
                    if self.ScaledA != 0:
                        
                        tVal = ( tVal * self.ScaledA )  + self.ScaledB
                    if IsNumeric(tVal):
                        
                        tVal = str(MdlStatistics.fRoundNum(float(tVal), self.__mPrecision, self.__mRoundType))
                    self.__mLastValue = tVal
                    strSQL = 'Update TblControllerFields Set CurrentValue = \'' + self.__mLastValue + '\' Where ID = ' + self.__mID
                    MdlConnection.CN.execute(strSQL)
                else:
                    if self.ExternalUpdate == True:
                        self.__mdReadValue = '' + MdlADOFunctions.GetSingleValue('dReadValue', 'TblControllerFields', 'MachineID = ' + self.pMachine.ID + ' AND FieldName=\'' + self.FName + '\'', 'CN')
                        tVal = self.dReadValue
                        
                        if ( self.dLowLimit == self.dHighLimit )  or  ( self.dLowLimit >= 0 and tVal > self.dLowLimit and self.dHighLimit != 0 and tVal < self.dHighLimit ) :
                            if self.ScaledA != 0:
                                
                                tVal = ( tVal * self.ScaledA )  + self.ScaledB
                            if IsNumeric(tVal):
                                
                                tVal = str(MdlStatistics.fRoundNum(float(tVal), self.__mPrecision, self.__mRoundType))
                            self.__mLastValue = tVal
                            if self.ConversionID != 0:
                                self.__mLastValue = GetValueFromConversion(self.ConversionID, self.__mLastValue)
                            strSQL = 'Update TblControllerFields Set CurrentValue = \'' + self.__mLastValue + '\' Where ID = ' + self.__mID
                            MdlConnection.CN.execute(strSQL)
                            self.__mdLastReadTime = '' + MdlADOFunctions.GetSingleValue('dLastReadTime', 'TblControllerFields', 'MachineID = ' + self.pMachine.ID + ' AND FieldName=\'' + self.FName + '\'', 'CN')
                
                
                if self.FieldDataType != 5 or self.RejectReasonOption != 0:
                    
                    if self.__mLastSampleTime > CDate('00:00:00'):
                        self.__mPrevSampleTime = self.__mLastSampleTime
                    self.__mLastSampleTime = Now()
            else:
                self.__mOPCItem.Read(OPC_DS_CACHE, tVal, self.__mQuality, self.__mTimeStamp)
                
                if self.__mQuality != 0:
                    
                    
                    if self.CalcByDiff == True:
                        self.__mdReadValue = tVal
                        
                        if self.__mdLastValidReadTime == CDate('00:00:00') and self.__mdLastReadTime > CDate('00:00:00'):
                            self.__mdLastValidReadTime = self.__mdLastReadTime
                        self.__mdLastReadTime = mdl_Common.NowGMT()
                        self.SetCalcByDiff(tVal)
                    
                    if self.ScaledA != 0:
                        
                        tVal = ( tVal * self.ScaledA )  + self.ScaledB
                    if IsNumeric(tVal):
                        
                        tVal = str(MdlStatistics.fRoundNum(float(tVal), self.__mPrecision, self.__mRoundType))
                if self.__mLastValue != tVal and self.__mQuality != 0:
                    self.__mPrevSampleTime = self.__mLastSampleTime
                    self.__mLastSampleTime = Now()
                    self.__mPrevValue = self.__mLastValue
                if self.__mPrevSampleTime < self.__mLastSampleTime and self.__mQuality != 0:
                    NewRead = True
                    if ( self.pMachine.CalcCycleTime == False and self.pMachine.ReseTotalCycles == False )  or self.__mPrevSampleTime == 0:
                        self.__mPrevSampleTime = self.__mLastSampleTime

                    if IsNumeric(tVal):
                        
                        self.__mLastValue = str(MdlStatistics.fRoundNum(float(tVal), self.__mPrecision, self.__mRoundType))
                    else:
                        self.__mLastValue = tVal
                    if self.ConversionID != 0:
                        self.__mLastValue = GetValueFromConversion(self.ConversionID, self.__mLastValue)
                    strSQL = 'Update TblControllerFields Set CurrentValue = \'' + self.__mLastValue + '\' Where ID = ' + self.__mID
                    MdlConnection.CN.execute(strSQL)
                    
                    if not ( self.__mSPOPCItem is None ) :
                        self.__mSPOPCItem.Read(OPC_DS_CACHE, tVal, self.__mQuality, self.__mTimeStamp)
                        self.__mSPPrevValue = self.__mSPLastValue
                        if self.ScaledA != 0:
                            
                            tVal = ( tVal * self.ScaledA )  + self.ScaledB
                        
                        self.__mSPLastValue = str(MdlStatistics.fRoundNum(float(tVal), self.__mPrecision, self.__mRoundType))
                        strSQL = 'Update TblControllerFields Set SPCurrentValue = ' + self.__mSPLastValue + ' Where ID = ' + self.__mID
                        MdlConnection.CN.execute(strSQL)
                    
                    if not ( self.__mSPLOPCItem is None ) :
                        self.__mSPLOPCItem.Read(OPC_DS_CACHE, tVal, self.__mQuality, self.__mTimeStamp)
                        self.__mSPLPrevValue = self.__mSPLValue
                        if self.ScaledA != 0:
                            
                            tVal = ( tVal * self.ScaledA )  + self.ScaledB
                        
                        self.__mSPLValue = str(MdlStatistics.fRoundNum(float(tVal), self.__mPrecision, self.__mRoundType))
                        strSQL = 'Update TblControllerFields Set SPLValue = ' + self.__mSPLValue + ' Where ID = ' + self.__mID
                        MdlConnection.CN.execute(strSQL)
                    
                    if not ( self.__mSPHOPCItem is None ) :
                        self.__mSPHOPCItem.Read(OPC_DS_CACHE, tVal, self.__mQuality, self.__mTimeStamp)
                        self.__mSPHPrevValue = self.__mSPHValue
                        if self.ScaledA != 0:
                            
                            tVal = ( tVal * self.ScaledA )  + self.ScaledB
                        
                        self.__mSPHValue = str(MdlStatistics.fRoundNum(float(tVal), self.__mPrecision, self.__mRoundType))
                        strSQL = 'Update TblControllerFields Set SPHValue = ' + self.__mSPHValue + ' Where ID = ' + self.__mID
                        MdlConnection.CN.execute(strSQL)
        
        self.CheckValidateValue.AddValue(MdlADOFunctions.fGetRstValDouble(self.__mLastValue))
        if self.__mRejectReasonID > 0:
            self.__mRejectsAReadCurrent = float(self.__mLastValue)
        
        if self.ChangeJobOnValueChanged:
            if self.__mPrevValue != self.__mLastValue and self.__mLastValue != '0' and self.__mLastValue != '':

                if self.__mPMachine.ConnectedByOPC == False and self.ExternalUpdate == True and self.dLastReadTime > CDate('00:00:00'):
                    self.LastIOTime = self.dLastReadTime
                    tIOStatus = self.IOStatus
                else:
                    tIOStatus = self.__mPMachine.IOStatus
                if tIOStatus == 1:
                    if self.ChangeJobOnValueChangedSourceTable == '' or self.ChangeJobOnValueChangedSourceField == '':
                        self.ChangeJobOnValueChangedSourceTable = 'TblJob'
                        self.ChangeJobOnValueChangedSourceField = 'ERPJobID'
                    strSQL = ''
                    select_2 = str(self.ChangeJobOnValueChangedSourceTable).upper()
                    if (select_2 == 'TBLJOB'):
                        strSQL = ''
                        strSQL = strSQL + 'SELECT ID, Status FROM TblJob' + '\n'
                        strSQL = strSQL + 'WHERE Status IN(2,3,11) AND MachineID = ' + self.pMachine.ID + '\n'
                        strSQL = strSQL + 'AND ' + self.ChangeJobOnValueChangedSourceField + ' = \'' + self.__mLastValue + '\''
                    elif (select_2 == 'TBLPRODUCT'):
                        strSQL = ''
                        strSQL = strSQL + 'SELECT ID, Status FROM TblJob' + '\n'
                        strSQL = strSQL + 'WHERE Status IN(2,3,11) AND MachineID = ' + self.pMachine.ID + '\n'
                        strSQL = strSQL + 'AND ProductID IN(SELECT ID FROM TblProduct WHERE ' + self.ChangeJobOnValueChangedSourceField + ' = \'' + self.__mLastValue + '\')'
                    else:
                        strSQL = ''
                    if strSQL != '':
                        
                        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
                        Rst.ActiveConnection = None
                        if Rst.RecordCount == 1:
                            JobStatus = MdlADOFunctions.fGetRstValLong(Rst.Fields("Status").Value)
                            JobID = MdlADOFunctions.fGetRstValLong(Rst.Fields("ID").Value)
                            if JobStatus == 2 or JobStatus == 3 or JobStatus == 11:
                                dictRequest.Add('MachineID', self.pMachine.ID)
                                dictRequest.Add('JobID', JobID)
                                CallAPIRequest('ActivateJobForMachine', dictRequest)
                        elif Rst.RecordCount == 0:
                            MdlGlobal.RecordError('LeaderRT:ActivateJob', 0, 'No job was found!', 'Value: ' + self.__mLastValue)
                        else:
                            MdlGlobal.RecordError('LeaderRT:ActivateJob', 0, 'More than one job was found!', 'Value: ' + self.__mLastValue)
                        Rst.Close()
                else:
                    MdlGlobal.RecordError('LeaderRT:ActivateJob', 0, 'No Communication!', 'Value: ' + self.__mLastValue)
            if self.__mLastValue != self.__mPrevValue and tIOStatus != 0:
                self.__mPrevSampleTime = self.__mLastSampleTime
                self.__mLastSampleTime = Now()
                self.__mPrevValue = self.__mLastValue
        
        if self.PrintLabelID > 0:
            if self.__mPrevValue != self.__mLastValue and self.__mLastValue != 0:
                LabelGroupID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('LabelGroupID', 'MetaTblLabels', 'ID = ' + self.PrintLabelID, 'MetaCN'))
                if (LabelGroupID == 1):
                    VBFiles.writeText(None, LabelPath == MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'PrintLabelBatchFile\'', 'CN')), '\n')
                    if PrintLabelPath != '':
                        if self.__mPrintLabelMachineID != 0:
                            
                            tActiveJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblJobCurrent', 'MachineID = ' + self.__mPrintLabelMachineID))
                            ShellExecute(frmMain.hwnd, 'open', PrintLabelPath, self.__mPrintLabelID + ',' + tActiveJobID, '', vbNormalFocus)
                        else:
                            ShellExecute(frmMain.hwnd, 'open', PrintLabelPath, self.__mPrintLabelID + ',' + self.str(pMachine.ActiveJobID), '', vbNormalFocus)
                elif (LabelGroupID == 4):
                    VBFiles.writeText(None, LabelPath == MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('CValue', 'STblSystemVariableFields', 'FieldName = \'PrintInventoryLabelBatchFile\'', 'CN')), '\n')
                    if PrintLabelPath != '':
                        if self.pMachine.GetParam('Label' + self.PrintLabelID + 'Data', LabelDataParam):
                            LabelDataParam.GetListData
                            strLabelData = LabelDataParam.LastValue
                            strLabelData = CalstringExpressions(strLabelData, LabelDataParam.CalstringExpression)
                            if strLabelData != self.__mLastInventoryLabelBatch:
                                self.__mLastInventoryLabelBatch = strLabelData
                                InventoryID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblInventory', 'Batch = \'' + strLabelData + '\''))
                                if InventoryID != 0:
                                    JobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('JobID', 'TblInventory', 'ID = ' + InventoryID))
                                    ProductID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductID', 'TblInventory', 'ID = ' + InventoryID))
                                    ShellExecute(frmMain.hwnd, 'open', PrintLabelPath, self.__mPrintLabelID + ',' + InventoryID + ',' + ProductID + ',' + JobID, '', vbNormalFocus)
                                    
                                    
        if self.__mErrorAlarmActive == True and NewRead == True:
            tVal = float(self.__mLastValue)
            if ( self.__mFName == 'Status' ) :
                if ( self.pMachine.Status == 3 ) :
                    tVal = 3
            
            if ( ( tVal > self.__mPUCL )  and  ( self.__mPUCL != 0 ) )  or  ( ( tVal < self.__mPLCL )  and  ( self.__mPLCL != 0 ) )  and  ( self.__mPUCL != self.__mPLCL ) :
                
                if self.AlarmFirstDetected == 0:
                    self.AlarmFirstDetected = mdl_Common.NowGMT()
                if self.__mErrorCount == 0:
                    self.__mErrorAlarmOn = True
                    self.__mErrorCount = 1
                else:
                    if self.__mErrorCount <= self.__mErrorCountAlarm:
                        self.__mErrorCount = self.__mErrorCount + 1
                
                
                self.__mLastAlarmValue = self.__mLastValue
                if ( tVal > self.__mPUCL ) :
                    self.__mLastAlarmLimit = self.__mPUCL
                    self.__mLastAlarmRef = 'High'
                else:
                    self.__mLastAlarmLimit = self.__mPLCL
                    self.__mLastAlarmRef = 'Low'
                if self.AlarmMinimumDuration == 0:
                    if ( ( self.__mAlarmPerminentAcknowledge == False )  and  ( self.__mAlarmCycleAcknowledge == False ) )  or  ( self.__mIgnoreAlarmAcknowledge == True ) :
                        self.pMachine.CreateAlarm(Me)
                else:
                    if DateDiff('n', self.AlarmFirstDetected, mdl_Common.NowGMT) >= self.AlarmMinimumDuration:
                        if ( ( self.__mAlarmPerminentAcknowledge == False )  and  ( self.__mAlarmCycleAcknowledge == False ) )  or  ( self.__mIgnoreAlarmAcknowledge == True ) :
                            self.pMachine.CreateAlarm(Me)
                if self.__mIsSPCValue == True:
                    self.__mPMachine.Rejects = self.__mPMachine.Rejects + 1
            else:

                self.pMachine.CancelAlarm(Me, False)
                self.__mErrorCount = 0
                self.__mErrorAlarmOn = False
                self.AlarmCycleAcknowledge = False
                tAlarmCanceled = True
                
                self.AlarmFirstDetected = 0
                self.AlarmFileLastPlay = 0
            
            
            if not ( self.__mSPOPCItem is None ) :
                if self.__mSPPrevValue != '' and self.__mSPPrevValue != '0':
                    if self.__mSPLastValue != self.__mSPPrevValue:
                        if ( self.__mAlarmPerminentAcknowledge == False )  and  ( self.__mAlarmCycleAcknowledge == False ) :
                            
                            pass
            if not ( self.__mSPLOPCItem is None ) :
                if self.__mSPLPrevValue != '' and self.__mSPPrevValue != '0':
                    if self.__mSPLValue != self.__mSPLPrevValue:
                        if ( self.__mAlarmPerminentAcknowledge == False )  and  ( self.__mAlarmCycleAcknowledge == False ) :
                            
                            pass
            if not ( self.__mSPHOPCItem is None ) :
                if self.__mSPHPrevValue != '' and self.__mSPHPrevValue != '0':
                    if self.__mSPHValue != self.__mSPHPrevValue:
                        if ( self.__mAlarmPerminentAcknowledge == False )  and  ( self.__mAlarmCycleAcknowledge == False ) :
                            
                            pass
        if self.__mIsSPCValue == True:
            if IsNumeric(self.__mLastValue):
                self.__SPCValAdd(float(self.__mLastValue))
        
        if not ( self.__mDataSamples is None ) :
            if self.__mDataSamples.Count > 0:
                for tDataSample in self.__mDataSamples:
                    tDataSample.AddValue(( self.LastValue ))
        if self.ValidateValue:
            self.CheckIfValid
        else:
            self.PrevValidValue = self.LastValidValue
            self.LastValidValue = self.__mLastValue
            
            
            
            
        if self.ID == 3639:
            NewRead = NewRead
        
        
        
        if self.ReportInventoryItemOnChange != 0 and self.ActionsAreValid == True:
            if not self.pMachine.ActiveJob is None:
                if self.CheckLabelIntegrity(tValuesDiff):
                    if tValuesDiff > 0:
                        if self.ReportInventoryItemOnChangeInterval != 0:
                            if tValuesDiff > Abs(( DateDiff('s', tPrevSampleTime, self.LastSampleTime) / self.ReportInventoryItemOnChangeInterval )):
                                tValuesDiff = Abs(( DateDiff('s', tPrevSampleTime, self.LastSampleTime) / self.ReportInventoryItemOnChangeInterval ))
                        if self.ID == 6557:
                            NewRead = NewRead
                        if self.EffectiveAmountFieldName != '':
                            if self.pMachine.GetParam(self.EffectiveAmountFieldName, tEffectiveAmountControlParam) == True:
                                tEffectiveAmountControlParam.GetListData()
                                if IsNumeric(tEffectiveAmountControlParam.LastValue):
                                    
                                    if ( float(tEffectiveAmountControlParam.LastValue) / tValuesDiff )  >= self.pMachine.Server.SystemVariables.ReportInventoryItemMinAmount:
                                        
                                        self.pMachine.ActiveJob.ReportInventoryItem(tValuesDiff, float(tEffectiveAmountControlParam.LastValue), self.ReportInventoryItemOnChange)
                                else:
                                    self.pMachine.ActiveJob.ReportInventoryItem(tValuesDiff, VBGetMissingArgument(self.pMachine.ActiveJob.ReportInventoryItem, 1), self.ReportInventoryItemOnChange)
                            else:
                                self.pMachine.ActiveJob.ReportInventoryItem(tValuesDiff, VBGetMissingArgument(self.pMachine.ActiveJob.ReportInventoryItem, 1), self.ReportInventoryItemOnChange)
                        else:
                            self.pMachine.ActiveJob.ReportInventoryItem(tValuesDiff, VBGetMissingArgument(self.pMachine.ActiveJob.ReportInventoryItem, 1), self.ReportInventoryItemOnChange)
        
        if self.UpdateActivePallet == True:
            if not self.pMachine.ActiveJob is None:
                if self.CheckLabelIntegrity(tValuesDiff):
                    if tValuesDiff > 0:
                        
                        UpdatePalletForToolInventory(tValuesDiff, self.pMachine)
        
        strSQL = 'UPDATE TblControllerFields '
        strSQL = strSQL + ' SET CurrentValidValue = \'' + self.__mLastValidValue + '\','
        strSQL = strSQL + ' ValidValueSampleTime = \'' + ShortDate(self.__mLastValidSampleTime, True, True, True) + '\','
        strSQL = strSQL + ' LastValidValue = \'' + self.__mPrevValidValue + '\''
        if self.ErrorAlarmActive and tAlarmCanceled:
            strSQL = strSQL + ', '
            strSQL = strSQL + ' AlarmCylceAcknowledge = ' + IIf(self.AlarmCycleAcknowledge == True, '1', '0')
        strSQL = strSQL + ' WHERE ID = ' + self.__mID
        MdlConnection.CN.execute(strSQL)
        if (self.__mFName == 'TotalCycles'):
            if self.ValidateValue == False:
                if not ( self.FieldDataType == 1 and self.CitectDeviceType == 2 ) :
                    self.pMachine.TotalCyclesLast = self.pMachine.TotalCycles
                    self.pMachine.TotalCycles = float(self.__mLastValue)
            else:
                self.pMachine.TotalCyclesLast = self.pMachine.TotalCycles
                self.pMachine.TotalCycles = float(self.__mLastValidValue)
            if self.FirstReadInCurrentJob == True:
                if not self.pMachine.ActiveJob is None:
                    if self.pMachine.ActiveJob.InjectionsCountStart == 0:
                        
                        pass
            if ( self.Quality and 0xC0 )  or self.FieldDataType == 5 or  ( self.FieldDataType == 1 and self.CitectDeviceType == 2 and self.CalcFunction != '' ) :
                self.__mPMachine.LastIOTime = mdl_Common.NowGMT()
            
            if self.__mPMachine.ConnectedByOPC == False and self.ExternalUpdate == True and self.dLastReadTime > CDate('00:00:00'):
                self.__mPMachine.LastIOTime = self.dLastReadTime
            if self.pMachine.TotalCycles - self.pMachine.TotalCyclesLast - self.pMachine.ActiveJob.InjectionsCountStart > 0:
                self.pMachine.UpdateShiftMachineCycleTime(self.pMachine.Server.CurrentShiftID, True, True)
        elif (self.__mFName == 'UnitsProducedOK'):            
            pass
        elif (self.__mFName == 'WorkOrder'):
            self.__mPMachine.ActiveJobID = self.__mLastValue
        elif (self.__mFName == 'CycleTime'):
            self.__mPMachine.CycleTime = self.__mLastValue
            self.__mPMachine.CycleTimeAvg = self.__mSMean
        elif (self.__mFName == 'ErrorOn'):
            if tVal > 0:
                self.LastValue = '0'
                self.__mErrorCount = 0
                
        elif (self.__mFName == 'ProductWeightLast'):
            self.pMachine.CycleWeight = self.__mLastValue
        elif (self.__mFName == 'ProductWeight'):
            self.pMachine.ProductWeight = self.__mLastValue
        elif (self.__mFName == 'MachineStop'):
            if self.pMachine.ID == 3:
                self.__mErrorCount = self.__mErrorCount
            if self.__mLastValue != '':
                if int(self.__mLastValue) == self.__mPMachine.StopSignal:
                    self.__mPMachine.MachineSignalStop = True
                else:
                    self.__mPMachine.MachineSignalStop = False
                
            else:
                self.__mPMachine.MachineSignalStop = False
        elif (self.__mFName == 'WareHouseLocationID'):
            if self.__mLastValue and MdlADOFunctions.fGetRstValBool(self.pMachine.DynamicWareHouseLocation, False) == True:
                tWareHouseLocationID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblWareHouseLocations', 'ERPID = \'' + self.__mLastValue + '\''))
                
                tWareHouseID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('WareHouseID', 'TblWareHouseLocations', ' ID = ' + tWareHouseLocationID, 'CN'))
                if tWareHouseLocationID != 0:
                    
                    MdlConnection.CN.execute('Update TblMachines SET DefaultWareHouseLocationID = ' + tWareHouseLocationID + ', DefaultWareHouse = ' + tWareHouseID + ' WHERE ID = ' + self.pMachine.ID)
        elif (self.__mFName == 'LastEventID'):
            temp = '' + MdlADOFunctions.GetSingleValue('dLastReadTime', 'TblControllerFields', 'MachineID = ' + self.pMachine.ID + ' AND FieldName=\'' + self.FName + '\'', 'CN')
            if temp != '' and self.ExternalUpdate == True:
                self.__mdLastReadTime = CDate(temp)
            if self.FieldDataType == 1 and self.CitectDeviceType == 2 and self.CalcFunction != '' and self.CalcFunction != '0' and self.ExternalUpdate == False:
                self.LastIOTime = mdl_Common.NowGMT()
            if self.__mPMachine.ConnectedByOPC == False and self.ExternalUpdate == True and self.dLastReadTime > CDate('00:00:00'):
                self.LastIOTime = self.dLastReadTime
        elif (self.__mFName == 'MachineEngine'):
            if self.__mLastValue != '':
                if int(self.__mLastValue) == self.__mPMachine.EngineSignal:
                    
                    self.__mPMachine.EngineSignalActive = True
                else:
                    
                    self.__mPMachine.EngineSignalActive = False
            else:
                
                self.__mPMachine.EngineSignalActive = False
        if not self.ValidateValue:
            if self.FirstReadInCurrentJob == True:
                self.FirstReadInCurrentJob = False
        self.XMLCalc()
        
        returnVal = True
        if self.__mActions.Count > 0:
            fExecutePostActions(Me)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
        if Err.Number == 462:
            ReadTries = ReadTries + 1
            strSQL = 'SELECT OPCServerName, OPCServerIP From TblMachines Where ID = ' + self.pMachine.ID
            MRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
            if MRst.RecordCount == 1:
                if MdlADOFunctions.fGetRstValString(MRst.Fields("OPCServerName").Value) != '' and MdlADOFunctions.fGetRstValString(MRst.Fields("OPCServerIP").Value) != '':
                    self.pMachine.OPCServer.Disconnect()
                    self.pMachine.OPCServer.Connect(MdlADOFunctions.fGetRstValString(MRst.Fields("OPCServerName").Value), MdlADOFunctions.fGetRstValString(MRst.Fields("OPCServerIP").Value))
                else:
                    self.pMachine.OPCServer.Disconnect()
                    self.pMachine.OPCServer.Connect(MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('OPCServer', 'STblSystemVariables', 'ID = 1', 'CN')))
            MRst.Close()
            MRst = None
            if ReadTries <= 3:
                
                pass
            else:
                return returnVal
        
        tDataSample = None
        tMachine = None
        LabelDataParam = None
        return returnVal

    def BatchGroupCreate(self):
        returnVal = False
        rVal = 0
        strGroupName = ''

        try:
            strGroupName = 'M_' + str(self.pMachine.ID) + '_BatchGroup'
            # self.BatchGroup = self.pMachine.OPCServer.OPCGroups.Add()
            self.BatchGroup.IsActive = True
            self.BatchGroup.IsSubscribed = True
            
            self.BatchGroup.UpdateRate = 600000
            self.BatchGroupHandle = self.BatchGroup.ClientHandle
            self.__mIsBatchTriger = True
            returnVal = True

        except BaseException as error:
            pass

        return returnVal

    def BatchReadValues(self, IsBatchUpdateP=True):
        returnVal = None
        Counter = 0

        RID = 0

        TCount = 0

        strSQL = ''

        strFields = ''

        strVals = ''

        tParam = ControlParam()

        CycleTimeSMean = 0

        ShiftID = 0

        strINSERT = ''

        tVariant = None

        tControlParam = ControlParam()
        
        if self.pMachine.ActiveJob is None:
            returnVal = True
            return returnVal
        if not IsEmpty(self.__mPMachine.BatchUpdateP) and IsBatchUpdateP:
            self.__mPMachine.IsBatchUpdatePP = True
            self.__mPMachine.BatchUpdateP.LastValue = str(float(self.__mLastValue))
            if not self.__mPMachine.BatchUpdateP.mBoolSyncWriteErr:
                self.__mPMachine.BatchUpdateP.WriteValue = str(float(self.__mLastValue))
        if self.BatchReadLastRecord != 0:
            if self.pMachine.Server.SystemVariables.HistoryIntervalSec > 0:
                if DateDiff('s', self.BatchReadLastRecord, mdl_Common.NowGMT()) < self.pMachine.Server.SystemVariables.HistoryIntervalSec:
                    return returnVal
            else:
                if DateDiff('n', self.BatchReadLastRecord, mdl_Common.NowGMT()) < self.pMachine.Server.SystemVariables.HistoryIntervalMin:
                    return returnVal
        returnVal = False
        for TCount in range(1, self.__mBatchTablesCount):
            strINSERT = 'INSERT INTO ' + self.__mBatchTables(TCount) + 'History'
            strINSERT = strINSERT + ' ('
            strINSERT = strINSERT + ' Job'
            strINSERT = strINSERT + ' ,MoldID'
            strINSERT = strINSERT + ' ,MachineID'
            strINSERT = strINSERT + ' ,ProductID'
            strINSERT = strINSERT + ' ,RecordTime'
            strINSERT = strINSERT + ' ,ShiftID'
            strINSERT = strINSERT + ' ,ShiftStartTime'
            strINSERT = strINSERT + ' ,CycleTimeSMean'
            if not self.BatchParams is None:
                for tVariant in self.BatchParams:
                    tControlParam = tVariant
                    if tControlParam.BatchTable == self.__mBatchTables(TCount):
                        strINSERT = strINSERT + ' ,' + tControlParam.FName
            strINSERT = strINSERT + ') '
            
            strINSERT = strINSERT + ' VALUES '
            strINSERT = strINSERT + ' ('
            strINSERT = strINSERT + self.pMachine.ActiveJob.ID
            strINSERT = strINSERT + ', ' + self.pMachine.ActiveJob.Mold.ID
            strINSERT = strINSERT + ', ' + self.pMachine.ID
            strINSERT = strINSERT + ', ' + self.pMachine.ActiveJob.Product.ID
            strINSERT = strINSERT + ', \'' + ShortDate(mdl_Common.NowGMT(), True, True, True) + '\''
            strINSERT = strINSERT + ', ' + self.pMachine.Server.CurrentShiftID
            strINSERT = strINSERT + ', \'' + ShortDate(self.pMachine.Server.CurrentShift.StartTime, True, True, True) + '\''
            if self.pMachine.ActiveJob.CycleTimeAvgSMean != 0:
                strINSERT = strINSERT + ', ' + self.pMachine.ActiveJob.CycleTimeAvgSMean
            else:
                strINSERT = strINSERT + ', ' + self.pMachine.ActiveJob.CycleTimeStandard
            if not self.BatchParams is None:
                for tVariant in self.BatchParams:
                    tControlParam = tVariant
                    if tControlParam.BatchTable == self.__mBatchTables(TCount):
                        
                        
                        if not tControlParam.BatchTableHistoryOnMachineStop and  ( self.pMachine.MachineStop or self.pMachine.IOStatus == 0 ) :
                            strINSERT = strINSERT + ',NULL'
                        else:
                            if tControlParam.LastValue != '':
                                strINSERT = strINSERT + ',' + tControlParam.LastValue
                            else:
                                strINSERT = strINSERT + ',NULL'
            strINSERT = strINSERT + ') '
            
            MdlConnection.CN.execute(strINSERT)
            
            
            if Right(self.__mBatchTables(TCount), 3) == 'IPC':
                RID = MdlADOFunctions.fGetRstValLong(GetSingleValueOnlyOne('ID', self.__mBatchTables(TCount) + 'History', 'MachineID = ' + self.pMachine.ID + ' ORDER BY ID DESC', 'CN'))
                if RID != 0:
                    strSQL = 'SP' + self.__mBatchTables(TCount) + 'Calc @RID = ' + RID
                    MdlConnection.CN.execute(strSQL)
            self.BatchReadLastRecord = mdl_Common.NowGMT()
            self.__mInBatchRead = False
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
                
            MdlGlobal.RecordError('LeaderRT:BatchReadValues', str(Err.Number), Err.Description, '')
            Err.Clear()
        tParam = None
        tVariant = None
        tControlParam = None
        strINSERT = ''
        return returnVal

    def BatchAddParamToList(self, tParam):        
        returnVal = False
        self.__mBatchParams[tParam.FName] = tParam
        # self.__mBatchCounter = self.__mBatchGroup.OPCItems.Count
        self.__mBatchServerHandles = [None] * self.__mBatchCounter
        # self.__mBatchServerHandles[self.__mBatchCounter] = tParam.OPCItem.ServerHandle
        self.__mBatchValues = [None] * self.__mBatchCounter
        self.__mErrors = [None] * self.__mBatchCounter
        returnVal = True
        return returnVal

    def __SPCValAdd(self, SPCVal):
        returnVal = None
        valIndex = 0

        GrpSize = 0

        GrpStart = 0

        GrpValIndex = 0

        Counter = 0

        ArrGroup = vbObjectInitialize(objtype=Double)

        strSQL = ''

        strFields = ''

        strVals = ''
        
        returnVal = False
        
        
        
        if self.__mMean != 0:
            if ( SPCVal > self.__mMean * 10 or SPCVal < self.__mMean * 0.1 )  or  ( self.__mPMachine.Status > 2 )  or  ( self.__mPMachine.Status == 0 ) :
                return returnVal
            else:
                valIndex = self.__SPCListInsert(SPCVal)
        else:
            valIndex = self.__SPCListInsert(SPCVal)
        if valIndex == 0:
            Err.Raise(1)
        GrpSize = self.__mSPCGroupSize * 2 + 1
        
        if self.__mSPCGroupSize > 0 and valIndex >=  ( self.__mSPCGroupSize * 2 + 1 ) :
            
            ArrGroup = vbObjectInitialize((GrpSize,), Variant)
            
            GrpStart = 0
            
            for Counter in range(1, GrpSize):
                ArrGroup[Counter] = self.__mSPCVals(valIndex - Counter + 1).value
            self.__mSPCVals[valIndex].STDEV = fSTDev(ArrGroup, GrpSize)
            self.__mSTDEV = round(self.__mSPCVals(valIndex).STDEV, self.__mPrecision)
            self.__mSPCVals[valIndex].XChecked = GrpSize
            fCheckGroupStat(ArrGroup, GrpSize, self.__mSPCVals(valIndex))
            if self.__mSPCVals(valIndex).XOrderAsc >=  ( self.__mSPCGroupSize * 2 - 1 )  or self.__mSPCVals(valIndex).XOrderDesc >=  ( self.__mSPCGroupSize * 2 - 1 ) :
                
                pass
            
            
            self.UCL = self.__mSPCVals(valIndex).UCL
            self.LCL = self.__mSPCVals(valIndex).LCL
            
            if self.__mQUCL == 0 and self.__mSPCVals(valIndex).UCL != 0:
                self.__mQUCL = self.__mSPCVals(valIndex).UCL
            if self.__mQLCL == 0 and self.__mSPCVals(valIndex).LCL != 0:
                self.__mQLCL = self.__mSPCVals(valIndex).LCL
            self.__mSMean = self.__mSPCVals(valIndex).SMean
            
        
        if self.__mSPCTable != '':
            strFields = 'SampleTime, JobID, MachineID, ProductID, MoldID, Value, ValSTDEV, STMean, STUCL, STLCL, MEAN, PUCL, PLCL, QUCL, QLCL, AbovePUCL, BelowPUCL, XAboveMean, XBelowMean, XAscending, XDescending'
            strVals = '\'' + ShortDate(mdl_Common.NowGMT, True, True) + '\', ' + str(self.pMachine.ActiveJobID) + ', ' + self.pMachine.ID + ', ' + self.pMachine.ActiveProductID + ', ' + self.pMachine.ActiveMoldID + ', ' + self.__mLastValue + ', ' + self.__mSPCVals(valIndex).STDEV + ', ' + self.__mSMean + ', ' + self.UCL + ', ' + self.LCL + ', ' + self.__mMean + ', ' + self.__mPUCL + ', ' + self.__mPLCL + ', ' + self.__mQUCL + ', ' + self.__mQLCL + ', ' + self.__mSPCVals(valIndex).XUCLAbove + ', ' + self.__mSPCVals(valIndex).XLCLBelow + ', ' + self.__mSPCVals(valIndex).XMeanAbove + ', ' + self.__mSPCVals(valIndex).XMeanbelow + ', ' + self.__mSPCVals(valIndex).XOrderAsc + ', ' + self.__mSPCVals(valIndex).XOrderDesc
            strSQL = 'INSERT ' + self.__mSPCTable + '(' + strFields + ') VALUES (' + strVals + ')'
            MdlConnection.CN.execute(strSQL)
        strSQL = 'Update TblControllerFields Set StatSTDev = ' + self.__mSTDEV + ', StatSMean = ' + self.__mSMean + ', HValue = ' + self.__mPUCL + ', HHValue = ' + self.__mQUCL + ', LValue = ' + self.__mPLCL + ', LLValue = ' + self.__mQLCL + ' Where ID = ' + self.__mID
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
                
            MdlGlobal.RecordError('LeaderRT:ErrSPCValAdd', str(Err.Number), Err.Description, '')
            Err.Clear()
        return returnVal

    def __SPCListInsert(self, SPCVal):
        returnVal = None
        Counter = 0

        tmean = 0

        tUCL = 0

        tLCL = 0

        ArrVals = vbObjectInitialize(objtype=Double)

        mSigma = 0
        
        
        if self.__mSPCSamplesCount < self.__mSPCSamplesMaxCount:
            self.__mSPCVals = vbObjectInitialize((self.__mSPCSamplesCount + 1,), Variant, self.__mSPCVals)
            self.__mSPCSamplesCount = self.__mSPCSamplesCount + 1
            self.__mSPCVals[self.__mSPCSamplesCount].value = SPCVal
            returnVal = self.__mSPCSamplesCount
        else:
            for Counter in range(1, self.__mSPCSamplesCount - 1):
                self.__mSPCVals[Counter] = self.__mSPCVals(Counter + 1)
            self.__mSPCVals[Counter].value = SPCVal
            returnVal = Counter
        if self.__mSPCSamplesCount < self.__mSPCSamplesMaxCount:
            return returnVal
        ArrVals = vbObjectInitialize((self.__mSPCSamplesMaxCount,), Variant)
        for Counter in range(1, ( self.__mSPCSamplesMaxCount )):
            ArrVals[Counter] = self.__mSPCVals(self.__mSPCSamplesCount - Counter + 1).value
        tUCL = self.__mPUCL
        tLCL = self.__mPLCL
        tmean = fSMean(ArrVals, self.__mSPCSamplesMaxCount, tUCL, tLCL)
        if tmean > 0:
            self.__mSMean = round(tmean, self.__mPrecision)
        else:
            self.__mSMean = self.__mMean
        self.__mUCL = round(tUCL, self.__mPrecision)
        self.__mLCL = round(tLCL, self.__mPrecision)
        
        self.__mSPCVals[self.__mSPCSamplesCount].SMean = round(self.__mSMean, self.__mPrecision)
        self.__mSPCVals[self.__mSPCSamplesCount].UCL = round(self.__mUCL, self.__mPrecision)
        self.__mSPCVals[self.__mSPCSamplesCount].LCL = round(self.__mLCL, self.__mPrecision)
        self.__mSPCVals[self.__mSPCSamplesCount].Mean = round(self.__mMean, self.__mPrecision)
        self.__mSPCVals[self.__mSPCSamplesCount].PUCL = round(self.__mPUCL, self.__mPrecision)
        self.__mSPCVals[self.__mSPCSamplesCount].PLCL = round(self.__mPLCL, self.__mPrecision)
        self.__mSPCVals[self.__mSPCSamplesCount].QUCL = round(self.__mQUCL, self.__mPrecision)
        self.__mSPCVals[self.__mSPCSamplesCount].QLCL = round(self.__mQLCL, self.__mPrecision)
        self.__mSPCVals[self.__mSPCSamplesCount].MeanDiff = self.__mSPCVals(self.__mSPCSamplesCount).value - self.__mMean
        
        mSigma = ( self.__mUCL - self.__mSMean )  / 3
        self.__mSPCVals[self.__mSPCSamplesCount].Sigma = mSigma
        self.__mSPCVals[self.__mSPCSamplesCount].MeanDiffSTDev = self.__mSPCVals(self.__mSPCSamplesCount).MeanDiff / mSigma
        if self.__mMean == 0:
            self.__mMean = self.SMean
        
        if self.__mPUCL == 0 or self.__mPLCL == 0:
            
            
            self.__mSPCVals[self.__mSPCSamplesCount].PUCL = self.__mUCL
            self.__mSPCVals[self.__mSPCSamplesCount].QUCL = self.__mQUCL
            
            
            self.__mSPCVals[self.__mSPCSamplesCount].PLCL = self.__mLCL
            self.__mSPCVals[self.__mSPCSamplesCount].QLCL = self.__mQLCL
            self.UpdateLimits(str(self.__mMean), round(self.__mUCL, self.__mPrecision), round(self.__mLCL, self.__mPrecision), round(self.__mQUCL, self.__mPrecision), round(self.__mQLCL, self.__mPrecision), True)
        return returnVal

    def UpdateLimits(self, dMean, dPUCL, dPLCL, dQUCL, dQLCL, UpdateRecipe=False, pFromJobLoad=False):
        returnVal = False
        strSQL = ''

        try:            
            if IsNumeric(dMean):
                self.__mMean = dMean
            if IsNumeric(dPUCL):
                self.__mPUCL = dPUCL
            if IsNumeric(dPLCL):
                self.__mPLCL = dPLCL
            if IsNumeric(dQUCL):
                self.__mQUCL = dQUCL
            if IsNumeric(dQLCL):
                self.__mQLCL = dQLCL
            
            if pFromJobLoad:
                if IsNumeric(dMean):
                    self.__mLastValue = dMean
            if self.__mPropertyID > 0 and UpdateRecipe == True:
                strSQL = 'UPDATE TblProductRecipeJob SET HValue = ' + self.__mPUCL + ', LValue = ' + self.__mPLCL + ', HHValue = ' + self.__mQUCL + ', LLValue = ' + self.__mQLCL
                if self.__mMean != 0:
                    strSQL = strSQL + ', FValue = ' + self.__mMean
                strSQL = strSQL + ' Where PropertyID = ' + str(self.__mPropertyID) + ' And  JobID = ' + str(self.__mPMachine.ActiveJobID)
                MdlConnection.CN.execute(strSQL)
                
                strSQL = 'Update TblControllerFields Set TargetValue = ' + self.__mMean + ', HValue = ' + self.__mPUCL + ', HHValue = ' + self.__mQUCL + ', LValue = ' + self.__mPLCL + ', LLValue = ' + self.__mQLCL + ' Where ID = ' + str(self.__mID)
                MdlConnection.CN.execute(strSQL)
            self.XMLCalc()
            returnVal = True

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError('ControlParam:UpdateLimits', str(0), error.args[0], '')
            
        return returnVal

    def CalcParam(self):
        returnVal = None
        Valid = False

        strTemp = ''

        Counter = 0
        
        returnVal = False
        Valid = False
        if self.__mCalcFunction != '' and self.__mCalcFunction != '0':
            
            if self.FName == 'TotalCycles' and self.pMachine.TotalCyclesAutoAdvance:
                if not self.pMachine.ActiveJob is None:
                    if self.pMachine.NoProgressCount() >= self.pMachine.ActiveJob.CycleTimeStandard:
                        strTemp = CalcMachineExpression(self.__mCalcFunction, self.__mPMachine, Valid)
                        if Valid == True:
                            if IsNumeric(strTemp):
                                
                                strTemp = MdlStatistics.fRoundNum(strTemp, self.__mPrecision, self.__mRoundType)
                            self.__mPrevValue = self.__mLastValue
                            self.LastValue = strTemp
            else:
                strTemp = CalcMachineExpression(self.__mCalcFunction, self.__mPMachine, Valid)
                if Valid == True:
                    if IsNumeric(strTemp):
                        
                        strTemp = MdlStatistics.fRoundNum(strTemp, self.__mPrecision, self.__mRoundType)
                    self.__mPrevValue = self.__mLastValue
                    self.LastValue = strTemp
                    
                    
                    
        else:
            if self.__mFieldDataType == 4 or self.__mFieldDataType == 5:
                strTemp = self.__mLastValue
                self.__mPrevValue = self.__mLastValue
                self.LastValue = strTemp
        if self.__mBatchParams.Count > 0:
            for Counter in range(1, self.__mBatchParams.Count):
                self.__mBatchParams.Item(Counter).CalcParam
        returnVal = True
        return returnVal

    def AlarmAcknowledge(self):
        returnVal = None
        
        returnVal = False
        self.__mErrorCount = 0
        self.__mErrorAlarmOn = False
        
        self.AlarmFileLastPlay = 0
        self.AlarmFirstDetected = 0
        returnVal = True
        if Err.Number != 0:
            Err.Clear()
        return returnVal


    def GetXML(self):       
        try:
            return self.__mXML
        except:
            return ''

    def XMLCalc(self):
        strXML = ''
        strValue = ''
        strStatus = ''
        GrpValIndex = 0
        tDataSample = None

        try:        
            if isinstance(self.__mLastValue, numbers.Number):
                strValue = round(float(self.__mLastValue), self.__mPrecision)
                if isinstance(self.__mPUCL, numbers.Number):
                    if float(self.__mLastValue) > float(self.__mPUCL):
                        strStatus = 'High'
                if isinstance(self.__mPLCL, numbers.Number):
                    if float(self.__mLastValue) < float(self.__mPLCL):
                        strStatus = 'Low'
                if strStatus == '':
                    strStatus = 'OK'
            else:
                strStatus = 'null'
                if self.__mLastValue != '':
                    strValue = '<![CDATA[' + str(self.__mLastValue).strip()[0: 255] + ']]>'
                    
            strXML = strXML + '<' + str(self.__mFName) + '>' + str(strValue) + '</' + str(self.__mFName) + '>' + '\n'
            strXML = strXML + '<' + str(self.__mFName) + 'PUCL' + '>' + str(self.__mPUCL) + '</' + str(self.__mFName) + 'PUCL' + '>' + '\n'
            strXML = strXML + '<' + str(self.__mFName) + 'PLCL' + '>' + str(self.__mPLCL) + '</' + str(self.__mFName) + 'PLCL' + '>' + '\n'
            strXML = strXML + '<' + str(self.__mFName) + 'Mean' + '>' + str(self.__mMean) + '</' + str(self.__mFName) + 'Mean' + '>' + '\n'
            strXML = strXML + '<' + str(self.__mFName) + 'Status' + '>' + strStatus + '</' + str(self.__mFName) + 'Status' + '>' + '\n'
            
            if not ( self.__mSPOPCItem is None ) :
                strXML = strXML + '<' + str(self.__mFName) + 'SetPoint' + '>' + str(self.__mSPLastValue) + '</' + str(self.__mFName) + 'SetPoint' + '>' + '\n'
            if not ( self.__mSPLOPCItem is None ) :
                strXML = strXML + '<' + str(self.__mFName) + 'SetPointLValue' + '>' + str(self.__mSPLValue) + '</' + str(self.__mFName) + 'SetPointLValue' + '>' + '\n'
            if not ( self.__mSPHOPCItem is None ) :
                strXML = strXML + '<' + str(self.__mFName) + 'SetPointHValue' + '>' + str(self.__mSPHValue) + '</' + str(self.__mFName) + 'SetPointHValue' + '>' + '\n'
            
            if self.__mErrorAlarmActive == True:
                strXML = strXML + '<' + str(self.__mFName) + 'AlarmCycleAcknowledge' + '>' + str(self.__mAlarmCycleAcknowledge) + '</' + str(self.__mFName) + 'AlarmCycleAcknowledge' + '>' + '\n'
                strXML = strXML + '<' + str(self.__mFName) + 'AlarmPerminentAcknowledge' + '>' + str(self.__mAlarmPerminentAcknowledge) + '</' + str(self.__mFName) + 'AlarmPerminentAcknowledge' + '>' + '\n'
            
            if self.__mDataSamples:
                if len(self.__mDataSamples) > 0:
                    for tDataSample in self.__mDataSamples.values():
                        tDataSample.CheckRelevantData()
                        tDataSample.Calc()
                        strXML = strXML + '<' + str(self.__mFName) + 'DataSampleInterval' + str(tDataSample.Interval) + '>' + str(tDataSample.FinalValue) + ' </' + str(self.__mFName) + 'DataSampleInterval' + str(tDataSample.Interval) + '>' + '\n'
            if self.__mIsSPCValue == True:
                if self.__mSPCGroupSize > 1:
                    GrpValIndex = self.__mSPCGroupSize - 1
                strXML = strXML + '<' + str(self.__mFName) + 'STDev' + '>' + str(self.__mSTDEV) + '</' + str(self.__mFName) + 'STDev' + '>' + '\n'
            self.__mXML = strXML

    
        except BaseException as error:
            MdlGlobal.RecordError('ControlParam:XMLCalc', str(0), error.args[0], '')
            
        strXML = ''


    def fShrinkBatchData(self, Job, LocalID, ProductID, MachineID, MoldID, StartTime, EndTime):
        returnVal = None
        Counter = 0

        strSQL = ''

        strSelect = ''

        strValues = ''

        strFields = ''

        temp = ''

        strINSERT = ''

        Rst = ADODB.Recordset()
        
        if self.__mBatchTable == '':
            return returnVal
        for Counter in range(1, self.__mBatchParams.Count):
            temp = self.__mBatchParams.Item(Counter).FName
            strSelect = strSelect + ', AVG(' + temp + ') AS ' + temp
        strSelect = 'Max(RecordTime) AS RecordTime ' + strSelect
        
        strSQL = 'Select ' + strSelect + ' From ' + self.__mBatchTable + ' Where MachineID = ' + self.__mPMachine.ID + ' AND RecordTime >= \'' + ShortDate(StartTime, False, True) + '\' AND RecordTime <= \'' + ShortDate(EndTime, False, True) + '\''
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        for Counter in range(1, self.__mBatchParams.Count):
            temp = self.__mBatchParams.Item(Counter).FName
            strFields = strFields + ', ' + temp
            if not IsNull(Rst.Fields(temp).value):
                strValues = strValues + ', ' + Rst.Fields(temp).value
            else:
                strValues = strValues + ', NULL'
        Rst.Close()
        strSQL = 'Delete ' + self.__mBatchTable + ' Where MachineID = ' + MachineID + ' AND RecordTime >= \'' + ShortDate(StartTime, False, True) + '\' AND RecordTime < \'' + ShortDate(EndTime, False, True) + '\' AND Compacted = 0'
        MdlConnection.CN.execute(strSQL)
        strFields = '(Job, LocalID, ProductID, MachineID, MoldID, RecordTime, Compacted ' + strFields + ')'
        
        strValues = '(' + Job + ' , ' + LocalID + ' , ' + ProductID + ', ' + MachineID + ', ' + MoldID + ',\'' + ShortDate(EndTime, False, True) + '\',1' + strValues + ')'
        strINSERT = 'Insert ' + self.__mBatchTable + strFields + ' VALUES' + strValues
        MdlConnection.CN.execute(strINSERT)
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError('LeaderRT:fShrinkBatchData', str(Err.Number), Err.Description, '')
            Err.Clear()
        if Rst.State != 0:
            Rst.Close()
        Rst = None
        return returnVal

    def fShrinkSPCData(self, JobID, LocalID, MachineID, MoldID, ProductID, StartTime, EndTime):
        returnVal = None
        strSQL = ''

        strSelect = ''

        strValues = ''

        strFields = ''

        temp = ''

        strINSERT = ''

        Rst = ADODB.Recordset()
        
        if self.__mSPCTable == '':
            return returnVal
        strSQL = 'Select AVG(Value) AS Value, AVG(ValSTDEV) AS ValSTDEV, AVG(STMean) AS STMean, AVG(STUCL) AS STUCL ' + ', AVG(STLCL) AS STLCL, AVG(MEAN) MEAN, AVG(PUCL) AS PUCL, AVG(PLCL) AS PLCL, AVG(QUCL) AS QUCL, AVG(QLCL) AS QLCL ' + ', Max(SampleTime) AS SampleTime From ' + self.__mSPCTable
        strSQL = strSQL + ' Where MachineID = ' + self.__mPMachine.ID
        Rst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        Rst.ActiveConnection = None
        strValues = '\'' + ShortDate(Rst.Fields("SampleTime").Value, True, True) + '\', ' + Rst.Fields("value").Value + ', ' + Rst.Fields("ValSTDEV").Value + ', ' + Rst.Fields("STMean").Value + ', ' + Rst.Fields("stUCL").Value + ', ' + Rst.Fields("stLCL").Value + ', ' + Rst.Fields("Mean").Value + ', ' + Rst.Fields("PUCL").Value + ', ' + Rst.Fields("PLCL").Value + ', ' + Rst.Fields("QUCL").Value + ', ' + Rst.Fields("QLCL").Value
        Rst.Close()
        strSQL = 'Delete ' + self.__mSPCTable + ' Where MachineID = ' + MachineID + ' AND SampleTime >= \'' + ShortDate(StartTime, True, True) + '\' AND SampleTime <= \'' + ShortDate(EndTime, True, True) + '\''
        MdlConnection.CN.execute(strSQL)
        strFields = '(JobID, MachineID, MoldID, ProductID, SampleTime, Value, ValSTDEV, STMean, STUCL, STLCL, MEAN, PUCL, PLCL, QUCL, QLCL)'
        strValues = '(' + JobID + ', ' + MachineID + ', ' + MoldID + ', ' + ProductID + ', ' + strValues + ')'
        strINSERT = 'Insert ' + self.__mSPCTable + strFields + ' VALUES' + strValues
        MdlConnection.CN.execute(strINSERT)
        strSQL = ''
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError('LeaderRT:fShrinkSPCData', str(Err.Number), Err.Description, '')
            Err.Clear()
        if Rst.State != 0:
            Rst.Close()
        Rst = None
        return returnVal

    def ShrinkData(self, JobID, LocalID, MachineID, MoldID, ProductID, StartTime, EndTime, MachineCurrentStatus='1'):
        returnVal = None
        tempTS = None

        TCount = 0

        tempSqlTS = ''
        
        returnVal = False

        if self.__mIsSPCValue == True and CInt(MachineCurrentStatus) < 3:
            
            fMoveTableToHistory(self.__mSPCTable, 'SampleTime', 'JobID', 60, 15, MachineID, self.ID, 'TSPC')
        returnVal = True
        if Err.Number != 0:
            MdlGlobal.RecordError('LeaderRT:ShrinkData', str(Err.Number), Err.Description, '')
            Err.Clear()
        return returnVal

    def AlarmXML(self):
        returnVal = None
        
        returnVal = self.__mAlarmXML
        return returnVal

    def AlarmXMLCalc(self):
        returnVal = None
        strXML = ''
        
        
        strXML = strXML + '<Alarm>' + '\n'
        strXML = strXML + '<Field><![CDATA[' + self.__mFName + ']]></Field>'
        strXML = strXML + '<LName><![CDATA[' + self.__mLName + ']]></LName>'
        strXML = strXML + '<EName><![CDATA[' + self.__mEName + ']]></EName>'
        strXML = strXML + '<LastValue><![CDATA[' + self.__mLastAlarmValue + ']]></LastValue>'
        strXML = strXML + '<Status><![CDATA[' + self.__mLastAlarmRef + ']]></Status>'
        strXML = strXML + '<Limit><![CDATA[' + self.__mLastAlarmLimit + ']]></Limit>'
        strXML = strXML + '</Alarm>' + '\n'
        
        self.__mAlarmXML = strXML
        if Err.Number != 0:
            MdlGlobal.RecordError('ControlParam:AlarmXMLCalc', str(Err.Number), Err.Description, '')
            Err.Clear()
            
        return returnVal

    def BatchAsyncRead(self):
        CancelID = 0

        ItemsCount = 0

        TransID = 0

        temp = ''
        
        
        ItemsCount = self.__mBatchGroup.OPCItems.Count
        TransID = int(self.__mID) * 10 + 2
        CancelID = TransID
        
        
        
        self.__mInRead = True
        
        
        self.__mPMachine.mIOCancelID = CancelID
        self.__mPMachine.mIOGroup = self.__mBatchGroup
        self.__mPMachine.mInBatchRead = True
        
        self.__mBatchGroup.AsyncRead(self.__mBatchCounter, self.__mBatchServerHandles, self.__mErrors, TransID, CancelID)

    def CalcScalingRatio(self):
        
        if ( self.RawFull - self.RawZero )  == 0:
            self.ScaledA = 1
            self.ScaledB = 0
        else:
            self.ScaledA = ( self.ScaledFull - self.ScaledZero )  /  ( self.RawFull - self.RawZero )
            self.ScaledB = self.ScaledZero - self.ScaledA * self.RawZero

    def AddBatchTable(self, sTableName):
        Counter = 0
        returnVal = False
        
        try:
            if sTableName == '':
                return returnVal
            
            if self.__mBatchTablesCount == 0:
                self.__mBatchTablesCount = 1
                self.__mBatchTables = [None]
                self.__mBatchTables[0] = sTableName
                returnVal = True
                return returnVal
            else:
                for Counter in range(0, self.__mBatchTablesCount):
                    if self.__mBatchTables[Counter] == sTableName:
                        return returnVal
            
            self.__mBatchTablesCount = self.__mBatchTablesCount + 1
            self.__mBatchTables = [None] * self.__mBatchTablesCount
            self.__mBatchTables[self.__mBatchTablesCount] = sTableName
            returnVal = True

        except:
            pass

        return returnVal

    def CalcRejectsRead(self):
        returnVal = None
        strSQL = ''

        LastAVGCycleTime = 0

        StandardCycleTime = 0

        RejectsDiff = 0

        tAllowAutoRejectsOnSetup = False
        
        returnVal = False
        
        if IsDate(self.pMachine.ActiveJob.SetUpEnd) and self.pMachine.ActiveJob.SetUpEnd != 0:
            tAllowAutoRejectsOnSetup = True
        else:
            tAllowAutoRejectsOnSetup = MdlADOFunctions.fGetRstValBool(self.pMachine.AllowAutoRejectsOnSetup, True)
        if self.__mLastSampleTime >= self.__mPrevSampleTime and self.__mLastSampleTime > CDate('00:00:00') and self.__mPrevSampleTime > CDate('00:00:00'):
            
            if self.RejectReasonDirectRead == True and self.RejectReasonOption == 1:
                
                self.pMachine.ActiveJob.AutoRejects = self.__mRejectsAReadCurrent
                if not self.pMachine.ActiveJob is None and self.__mRejectsAReadCurrent != 0:
                    if self.__mRejectReasonOption == 1:
                        self.pMachine.ActiveJob.AddRejects(self.__mRejectsAReadCurrent, 0, self.__mRejectReasonID, True, True, self.__mRejectReasonOption, False, VBGetMissingArgument(self.pMachine.ActiveJob.AddRejects, 7), self.__mRejectsIncludeInRejectsTotal)
                returnVal = True
            else:
                if MdlADOFunctions.fGetRstValBool(self.pMachine.AllowAutoRejectsOnSetup, True) == False:
                    self.__mRejectsAReadCurrent = self.__mRejectsAReadCurrent - self.pMachine.ActiveJob.SetUpEndAutoRejects
                if self.__mRejectsAReadCurrent < self.__mRejectsAReadLast:
                    self.__mRejectsAReadLast = 0
                    returnVal = False
                    self.__mPrevSampleTime = self.__mLastSampleTime
                else:
                    
                    self.__mRejectsAReadDiff = round(self.__mRejectsAReadCurrent - self.__mRejectsAReadLast, 5)
                    
                    if self.__mRejectsAReadDiff > 0 and self.__mRejectsAReadLast > 0 and self.__mPMachine.ActiveJobID > 0 and self.__mPMachine.TotalCycles > 0:
                        self.__mRejectsA = self.__mRejectsA + self.__mRejectsAReadDiff
                    else:
                        if self.__mRejectsAReadDiff > 0 and self.__mRejectsAReadLast == 0 and self.__mPMachine.ActiveJobID > 0 and self.__mPMachine.TotalCycles > 0:
                            if ( self.__mRejectsAReadCurrent - self.__mRejectsA )  > 0:
                                self.__mRejectsA = self.__mRejectsA +  ( self.__mRejectsAReadCurrent - self.__mRejectsA )
                        
                    
                    
                    self.pMachine.ActiveJob.AutoRejects = self.__mRejectsAReadCurrent
                    if tAllowAutoRejectsOnSetup == False:
                        self.__mRejectsAReadLast = self.__mRejectsAReadCurrent
                        self.__mRejectsALast = self.__mRejectsA
                    
                    self.__mRejectsADiff = round(self.__mRejectsA - self.__mRejectsALast, 5)
                    
                    self.__mPMachine.RejectsRead = self.__mPMachine.RejectsRead + self.__mRejectsADiff
                    if not self.pMachine.ActiveJob is None:
                        self.pMachine.ActiveJob.RejectsRead = self.pMachine.RejectsRead
                        if not self.pMachine.ActiveJob.ActiveJosh is None:
                            self.pMachine.ActiveJob.ActiveJosh.RejectsRead = self.pMachine.ActiveJob.ActiveJosh.RejectsRead + self.__mRejectsADiff
                    if not self.pMachine.ActiveJob is None and self.__mRejectsADiff != 0:
                        if self.__mRejectReasonOption > 0:
                            
                            self.pMachine.ActiveJob.AddRejects(self.__mRejectsADiff, 0, self.__mRejectReasonID, True, True, self.__mRejectReasonOption, True, VBGetMissingArgument(self.pMachine.ActiveJob.AddRejects, 7), self.__mRejectsIncludeInRejectsTotal)
                        else:
                            
                            self.pMachine.ActiveJob.AddRejects(self.__mRejectsADiff, 0, self.__mRejectReasonID, False, True, self.__mRejectReasonOption, VBGetMissingArgument(self.pMachine.ActiveJob.AddRejects, 6), VBGetMissingArgument(self.pMachine.ActiveJob.AddRejects, 7), self.__mRejectsIncludeInRejectsTotal)
                        self.__mRejectsAReadLast = self.__mRejectsAReadCurrent
                        self.__mRejectsALast = self.__mRejectsA
                    returnVal = True
        else:
            returnVal = False
        if Err.Number != 0:
            MdlGlobal.RecordError('LeaderRT:CalcRejectsRead', str(Err.Number), Err.Description, 'JobID:' + self.__mPMachine.ActiveJobID + ';Machine:' + self.__mPMachine.ID)
            Err.Clear()
        return returnVal

    
    def AddAlarm(self, pAlarm):
        
        self.Alarms.Add(pAlarm, str(pAlarm.ID))
        if Err.Number != 0:
            Err.Clear()

    def CheckIfValid(self):
        tValueDiff = 0

        tTimeDiff = 0

        tTimeProportion = 0
        
        
        
        
        if not self.pMachine.ActiveJob is None:
            
            if self.CitectDeviceType == 1 and self.Quality == 0:
                return
            if self.LastValidValue == '':
                self.LastValidValue = self.__mLastValue
                self.__mLastValidSampleTime = self.__mLastSampleTime
            
            if ( MdlADOFunctions.fGetRstValDouble(self.__mLastValue) < MdlADOFunctions.fGetRstValDouble(self.LastValidValue) )  or  ( self.CheckValidateValue.LastValidationPast == False ) :
                tValueDiff = self.CheckValidateValue.CheckValues(Me)
            else:
                tValueDiff = MdlADOFunctions.fGetRstValDouble(self.__mLastValue) - MdlADOFunctions.fGetRstValDouble(self.LastValidValue)
            if tValueDiff == 0:
                return
            
            tTimeDiff = MdlADOFunctions.fGetRstValDouble(Abs(DateDiff('s', self.LastValidSampleTime, self.__mLastSampleTime)))
            tTimeDiff = ( tTimeDiff / 60 )
            if tTimeDiff != 0:
                if ( Abs(tValueDiff / tTimeDiff) )  <= self.MaxValueUnitsPerMin and  ( Abs(tValueDiff / tTimeDiff) )  >= self.MinValueUnitsPerMin:
                    
                    
                    if tValueDiff != 0:
                        if self.FirstReadInCurrentJob == True:
                            self.FirstReadInCurrentJob = False
                            self.PrevValidValue = '0'
                        else:
                            self.PrevValidValue = self.LastValidValue
                        self.LastValidValue = self.__mLastValue
                    else:
                        self.PrevValidValue = self.LastValidValue
                else:
                    MdlGlobal.RecordError('ControlParam.CheckIfValid:', '0', '', 'FieldName:' + self.FName + '. MachineID:' + self.pMachine.ID + '. JobID:' + str(self.pMachine.ActiveJobID) + '. Value was not valid. Last Valid Value: ' + self.LastValidValue + '. Invalid Value:' + self.__mLastValue + '. TimeDiff(Min):' + tTimeDiff)
            else:
                self.PrevValidValue = self.LastValidValue

        if Err.Number != 0:
            Err.Clear()

    def CheckWriteCondition(self):
        returnVal = None
        
        if self.WriteConditionalControllerField is None:
            returnVal = True
            return returnVal
        else:
            self.WriteConditionalControllerField.GetListData
            if MdlADOFunctions.fGetRstValDouble(self.WriteConditionalControllerField.LastValue) > self.WriteConditionalMinValue and MdlADOFunctions.fGetRstValDouble(self.WriteConditionalControllerField.LastValue) < self.WriteConditionalMaxValue:
                returnVal = True
            else:
                returnVal = False
        if Err.Number != 0:
            Err.Clear()
        return returnVal

    
    def CheckLabelIntegrity(self, pValuesDiff):
        returnVal = None
        
        returnVal = False
        
        if self.CitectDeviceType == 1:
            if Right(self.OPCItem.ItemID, 8) == '@Boolean':
                if MdlADOFunctions.fGetRstValBool(self.__mLastValidValue, False) == True:
                    returnVal = True
                    pValuesDiff = self.pMachine.ActiveJob.CavitiesActual
            else:
                if MdlADOFunctions.fGetRstValLong(self.__mLastValidValue) > 0:
                    if self.__mPrevValidValue != self.__mLastValidValue:
                        returnVal = True
                        pValuesDiff = MdlADOFunctions.fGetRstValLong(self.__mLastValidValue) - MdlADOFunctions.fGetRstValLong(self.__mPrevValidValue)
                        
        else:
            
            if MdlADOFunctions.fGetRstValLong(self.__mLastValidValue) > 0:
                if self.__mPrevValidValue != self.__mLastValidValue:
                    returnVal = True
                    pValuesDiff = MdlADOFunctions.fGetRstValLong(self.__mLastValidValue) - MdlADOFunctions.fGetRstValLong(self.__mPrevValidValue)
                    
        if Err.Number != 0:
            Err.Clear()
        return returnVal

    
    def SetCalcByDiff(self, pVal):
        returnVal = None
        strSQL = ''

        tReadValue = 0

        tPrevValue = 0

        tLastValidValue = 0

        tDiffValue = 0

        oldReadValue = 0

        oldPrevValue = 0

        oldLastValidValue = 0

        oldDiffValue = 0
        
        returnVal = False
        if self.ID == 3639:
            strSQL = strSQL
        
        tReadValue = round(MdlADOFunctions.fGetRstValDouble(self.dReadValue), 5)
        tPrevValue = round(MdlADOFunctions.fGetRstValDouble(self.dPrevValue), 5)
        tLastValidValue = round(MdlADOFunctions.fGetRstValDouble(self.dLastValidValue), 5)
        tDiffValue = round(MdlADOFunctions.fGetRstValDouble(self.dDiffValue), 5)
        
        if self.CalcByDiffWithScaling:
            
            oldReadValue = tReadValue
            if self.ScaledA != 0:
                
                tReadValue = ( tReadValue * self.ScaledA )  + self.ScaledB
            if IsNumeric(tReadValue):
                
                tReadValue = str(MdlStatistics.fRoundNum(float(tReadValue), self.__mCalcByDiffScalingRound, self.__mRoundType))
            
            oldPrevValue = tPrevValue
            if self.ScaledA != 0:
                
                tPrevValue = ( tPrevValue * self.ScaledA )  + self.ScaledB
            if IsNumeric(tPrevValue):
                
                tPrevValue = str(MdlStatistics.fRoundNum(float(tPrevValue), self.__mCalcByDiffScalingRound, self.__mRoundType))
            
            oldLastValidValue = tLastValidValue
            if self.ScaledA != 0:
                
                tLastValidValue = ( tLastValidValue * self.ScaledA )  + self.ScaledB
            if IsNumeric(tLastValidValue):
                
                tLastValidValue = str(MdlStatistics.fRoundNum(float(tLastValidValue), self.__mCalcByDiffScalingRound, self.__mRoundType))
            
            oldDiffValue = tDiffValue
            if self.ScaledA != 0:
                
                tDiffValue = ( tDiffValue * self.ScaledA )  + self.ScaledB
            if IsNumeric(tDiffValue):
                
                tDiffValue = str(MdlStatistics.fRoundNum(float(tDiffValue), self.__mCalcByDiffScalingRound, self.__mRoundType))
        
        
        
        
        if tReadValue >= tLastValidValue and tReadValue >= 0:
            
            if self.CalcByDiffValidate:
                if not self.ReadValueIsValid(tReadValue, tLastValidValue):
                    self.dResetSuspect = True
            if self.dResetSuspect == True:
                if tPrevValue == 0:
                    tPrevValue = tReadValue
                    oldPrevValue = oldReadValue
                    tDiffValue = 0
                    oldDiffValue = 0
                else:
                    self.__mdResetSuspect = False
                    
                    
                    tDiffValue = 0
                    oldDiffValue = 0
                    tPrevValue = tReadValue
                    oldPrevValue = oldReadValue
                    tLastValidValue = tReadValue
                    oldLastValidValue = oldReadValue
            else:
                tPrevValue = tLastValidValue
                oldPrevValue = oldLastValidValue
                tDiffValue = tReadValue - tLastValidValue
                oldDiffValue = oldReadValue - oldLastValidValue
                tLastValidValue = tReadValue
                oldLastValidValue = oldReadValue
        else:
            if tReadValue == 0:
                tPrevValue = tReadValue
                oldPrevValue = oldReadValue
                tDiffValue = 0
                oldDiffValue = 0
                
            else:
                self.__mdResetSuspect = True
                if ( tPrevValue == 0 or tReadValue >= tPrevValue )  and tReadValue > 0:
                    
                    
                    if self.CalcByDiffValidate and not self.ReadValueIsValid(tReadValue, 0):
                        tDiffValue = 0
                        oldDiffValue = 0
                    else:
                        tDiffValue = tReadValue
                        oldDiffValue = oldReadValue
                    tPrevValue = tReadValue
                    oldPrevValue = oldReadValue
                    tLastValidValue = tReadValue
                    oldLastValidValue = oldReadValue
                    self.__mdResetSuspect = False
                else:
                    tDiffValue = 0
                    oldDiffValue = 0
                    tPrevValue = tReadValue
                    oldPrevValue = oldReadValue
        
        if tDiffValue < 0:
            tDiffValue = 0
        if oldDiffValue < 0:
            oldDiffValue = 0
        
        if self.CalcByDiffWithScaling:
            tReadValue = oldReadValue
            tPrevValue = oldPrevValue
            tLastValidValue = oldLastValidValue
            tDiffValue = oldDiffValue
        
        
        if self.ScaledA == 0:
            self.ScaledA = 1
        pVal = round(MdlADOFunctions.fGetRstValDouble(( MdlADOFunctions.fGetRstValDouble(self.__mLastValue) - self.ScaledB )  / self.ScaledA), 5) + tDiffValue
        
        self.__mdReadValue = MdlADOFunctions.fGetRstValString(tReadValue)
        self.__mdPrevValue = MdlADOFunctions.fGetRstValString(tPrevValue)
        self.__mdLastValidValue = MdlADOFunctions.fGetRstValString(tLastValidValue)
        self.__mdDiffValue = MdlADOFunctions.fGetRstValString(tDiffValue)
        
        if self.dResetSuspect == False and self.__mdReadValue != self.__mdPrevValue:
            self.dLastValidReadTime = self.dLastReadTime
        strSQL = ''
        strSQL = strSQL + 'UPDATE TblControllerFields SET '
        if self.ExternalUpdate == False:
            strSQL = strSQL + 'dReadValue = \'' + self.dReadValue + '\', '
            strSQL = strSQL + 'dLastReadTime = \'' + ShortDate(self.dLastReadTime, True, True, True) + '\', '
        strSQL = strSQL + 'dPrevValue = \'' + self.dPrevValue + '\', '
        strSQL = strSQL + 'dLastValidValue = \'' + self.dLastValidValue + '\', '
        strSQL = strSQL + 'dDiffValue = \'' + self.dDiffValue + '\', '
        if self.dResetSuspect == True:
            strSQL = strSQL + 'dResetSuspect = 1 '
        else:
            strSQL = strSQL + 'dResetSuspect = 0 '
        strSQL = strSQL + 'WHERE ID = ' + self.__mID
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
                
            MdlGlobal.RecordError('SetCalcByDiff', Err.Number, Err.Description, 'MachineID: ' + self.pMachine.ID + ', FieldName: ' + self.FName)
            Err.Clear()
        return returnVal

    def ReadValueIsValid(self, pReadValue, pLastValidValue):
        returnVal = None
        tValueDiff = 0

        tTimeDiff = 0
        
        returnVal = False
        if self.MinValueUnitsPerMin == 0 and self.MaxValueUnitsPerMin == 0:
            returnVal = True
            return returnVal
        tValueDiff = pReadValue - pLastValidValue
        if tValueDiff == 0:
            returnVal = True
            return returnVal
        tTimeDiff = round(MdlADOFunctions.fGetRstValDouble(Abs(DateDiff('s', self.__mdLastValidReadTime, self.__mdLastReadTime))), 5)
        tTimeDiff = round(( tTimeDiff / 60 ), 5)
        if tTimeDiff != 0:
            if not ( ( Abs(tValueDiff / tTimeDiff) )  >= self.MinValueUnitsPerMin and  ( Abs(tValueDiff / tTimeDiff) )  <= self.MaxValueUnitsPerMin ) :
                returnVal = False
                return returnVal
        returnVal = True
        if Err.Number != 0:
            MdlGlobal.RecordError('ControlParam:ReadValueIsValid', Err.Number, Err.Description, 'MachineID: ' + self.pMachine.ID + ', FieldName: ' + self.FName)
            Err.Clear()
        return returnVal

    def IOStatus(self):
        returnVal = None
        strRes = ''

        strCommand = ''
        
        if DateDiff('s', self.__mLastIOTime, mdl_Common.NowGMT) >= self.__cntDeviceDisableIntervalSec:
            self.__mIOStatus = 0
        else:
            self.__mIOStatus = 1
        returnVal = self.__mIOStatus
        return returnVal


    def setChangeJobOnValueChangedSourceTable(self, value):
        self.__mChangeJobOnValueChangedSourceTable = value

    def getChangeJobOnValueChangedSourceTable(self):
        returnVal = None
        returnVal = self.__mChangeJobOnValueChangedSourceTable
        return returnVal
    ChangeJobOnValueChangedSourceTable = property(fset=setChangeJobOnValueChangedSourceTable, fget=getChangeJobOnValueChangedSourceTable)


    def setChangeJobOnValueChangedSourceField(self, value):
        self.__mChangeJobOnValueChangedSourceField = value

    def getChangeJobOnValueChangedSourceField(self):
        returnVal = None
        returnVal = self.__mChangeJobOnValueChangedSourceField
        return returnVal
    ChangeJobOnValueChangedSourceField = property(fset=setChangeJobOnValueChangedSourceField, fget=getChangeJobOnValueChangedSourceField)


    
    def setLastIOTime(self, value):
        self.__mLastIOTime = value

    def getLastIOTime(self):
        returnVal = None
        returnVal = self.__mLastIOTime
        return returnVal
    LastIOTime = property(fset=setLastIOTime, fget=getLastIOTime)


    def setdLowLimit(self, value):
        self.__mdLowLimit = value

    def getdLowLimit(self):
        returnVal = None
        returnVal = self.__mdLowLimit
        return returnVal
    dLowLimit = property(fset=setdLowLimit, fget=getdLowLimit)


    def setdHighLimit(self, value):
        self.__mdHighLimit = value

    def getdHighLimit(self):
        returnVal = None
        returnVal = self.__mdHighLimit
        return returnVal
    dHighLimit = property(fset=setdHighLimit, fget=getdHighLimit)


    def setCalcByDiffScalingRound(self, value):
        self.__mCalcByDiffScalingRound = value

    def getCalcByDiffScalingRound(self):
        returnVal = None
        returnVal = self.__mCalcByDiffScalingRound
        return returnVal
    CalcByDiffScalingRound = property(fset=setCalcByDiffScalingRound, fget=getCalcByDiffScalingRound)


    def setCalcByDiffWithScaling(self, value):
        self.__mCalcByDiffWithScaling = value

    def getCalcByDiffWithScaling(self):
        returnVal = None
        returnVal = self.__mCalcByDiffWithScaling
        return returnVal
    CalcByDiffWithScaling = property(fset=setCalcByDiffWithScaling, fget=getCalcByDiffWithScaling)


    def setSendPushOnAlarm(self, value):
        self.__mSendPushOnAlarm = value

    def getSendPushOnAlarm(self):
        returnVal = None
        returnVal = self.__mSendPushOnAlarm
        return returnVal
    SendPushOnAlarm = property(fset=setSendPushOnAlarm, fget=getSendPushOnAlarm)


    def setRoundType(self, value):
        self.__mRoundType = value

    def getRoundType(self):
        returnVal = None
        returnVal = self.__mRoundType
        return returnVal
    RoundType = property(fset=setRoundType, fget=getRoundType)


    def setSendEmailOnAlarm(self, value):
        self.__mSendEmailOnAlarm = value

    def getSendEmailOnAlarm(self):
        returnVal = None
        returnVal = self.__mSendEmailOnAlarm
        return returnVal
    SendEmailOnAlarm = property(fset=setSendEmailOnAlarm, fget=getSendEmailOnAlarm)


    def setCalcMainDataOnBuffer(self, value):
        self.__mCalcMainDataOnBuffer = value

    def getCalcMainDataOnBuffer(self):
        returnVal = None
        returnVal = self.__mCalcMainDataOnBuffer
        return returnVal
    CalcMainDataOnBuffer = property(fset=setCalcMainDataOnBuffer, fget=getCalcMainDataOnBuffer)


    def setBufferEnabled(self, value):
        self.__mBufferEnabled = value

    def getBufferEnabled(self):
        returnVal = None
        returnVal = self.__mBufferEnabled
        return returnVal
    BufferEnabled = property(fset=setBufferEnabled, fget=getBufferEnabled)


    def setEnableAlarmsDuringSetup(self, value):
        self.__mEnableAlarmsDuringSetup = value

    def getEnableAlarmsDuringSetup(self):
        returnVal = None
        returnVal = self.__mEnableAlarmsDuringSetup
        return returnVal
    EnableAlarmsDuringSetup = property(fset=setEnableAlarmsDuringSetup, fget=getEnableAlarmsDuringSetup)


    def setdLastValidReadTime(self, value):
        self.__mdLastValidReadTime = value

    def getdLastValidReadTime(self):
        returnVal = None
        returnVal = self.__mdLastValidReadTime
        return returnVal
    dLastValidReadTime = property(fset=setdLastValidReadTime, fget=getdLastValidReadTime)


    def setCalcByDiffValidate(self, value):
        self.__mCalcByDiffValidate = value

    def getCalcByDiffValidate(self):
        returnVal = None
        returnVal = self.__mCalcByDiffValidate
        return returnVal
    CalcByDiffValidate = property(fset=setCalcByDiffValidate, fget=getCalcByDiffValidate)


    def setBatchTableHistoryOnMachineStop(self, value):
        self.__mBatchTableHistoryOnMachineStop = value

    def getBatchTableHistoryOnMachineStop(self):
        returnVal = None
        returnVal = self.__mBatchTableHistoryOnMachineStop
        return returnVal
    BatchTableHistoryOnMachineStop = property(fset=setBatchTableHistoryOnMachineStop, fget=getBatchTableHistoryOnMachineStop)


    def setRejectReasonDirectRead(self, value):
        self.__mRejectReasonDirectRead = value

    def getRejectReasonDirectRead(self):
        returnVal = None
        returnVal = self.__mRejectReasonDirectRead
        return returnVal
    RejectReasonDirectRead = property(fset=setRejectReasonDirectRead, fget=getRejectReasonDirectRead)


    def setdLastReadTime(self, value):
        self.__mdLastReadTime = value

    def getdLastReadTime(self):
        returnVal = None
        returnVal = self.__mdLastReadTime
        return returnVal
    dLastReadTime = property(fset=setdLastReadTime, fget=getdLastReadTime)


    def setExternalUpdate(self, value):
        self.__mExternalUpdate = value

    def getExternalUpdate(self):
        returnVal = None
        returnVal = self.__mExternalUpdate
        return returnVal
    ExternalUpdate = property(fset=setExternalUpdate, fget=getExternalUpdate)


    def setCalcByDiff(self, value):
        self.__mCalcByDiff = value

    def getCalcByDiff(self):
        returnVal = None
        returnVal = self.__mCalcByDiff
        return returnVal
    CalcByDiff = property(fset=setCalcByDiff, fget=getCalcByDiff)


    def setdReadValue(self, value):
        self.__mdReadValue = value

    def getdReadValue(self):
        returnVal = None
        returnVal = self.__mdReadValue
        return returnVal
    dReadValue = property(fset=setdReadValue, fget=getdReadValue)


    def setdLastValidValue(self, value):
        self.__mdLastValidValue = value

    def getdLastValidValue(self):
        returnVal = None
        returnVal = self.__mdLastValidValue
        return returnVal
    dLastValidValue = property(fset=setdLastValidValue, fget=getdLastValidValue)


    def setdPrevValue(self, value):
        self.__mdPrevValue = value

    def getdPrevValue(self):
        returnVal = None
        returnVal = self.__mdPrevValue
        return returnVal
    dPrevValue = property(fset=setdPrevValue, fget=getdPrevValue)


    def setdDiffValue(self, value):
        self.__mdDiffValue = value

    def getdDiffValue(self):
        returnVal = None
        returnVal = self.__mdDiffValue
        return returnVal
    dDiffValue = property(fset=setdDiffValue, fget=getdDiffValue)


    def setdResetSuspect(self, value):
        self.__mdResetSuspect = value

    def getdResetSuspect(self):
        returnVal = None
        returnVal = self.__mdResetSuspect
        return returnVal
    dResetSuspect = property(fset=setdResetSuspect, fget=getdResetSuspect)


    def setOPCDataTypeID(self, value):
        self.__mOPCDataTypeID = value

    def getOPCDataTypeID(self):
        return self.__mOPCDataTypeID
    OPCDataTypeID = property(fset=setOPCDataTypeID, fget=getOPCDataTypeID)


    def setCheckValidateValue(self, value):
        self.__mCheckValidateValue = value

    def getCheckValidateValue(self):
        return self.__mCheckValidateValue
    CheckValidateValue = property(fset=setCheckValidateValue, fget=getCheckValidateValue)

    
    def setUpdateActivePallet(self, the_mApdateActivePallet):
        self.__mUpdateActivePallet = the_mApdateActivePallet

    def getUpdateActivePallet(self):
        return self.__mUpdateActivePallet
    UpdateActivePallet = property(fset=setUpdateActivePallet, fget=getUpdateActivePallet)


    
    def setConversionID(self, value):
        self.__mConversionID = value

    def getConversionID(self):
        returnVal = None
        returnVal = self.__mConversionID
        return returnVal
    ConversionID = property(fset=setConversionID, fget=getConversionID)


    def setReportInventoryItemOnChangeInterval(self, value):
        self.__mReportInventoryItemOnChangeInterval = value

    def getReportInventoryItemOnChangeInterval(self):
        returnVal = None
        returnVal = self.__mReportInventoryItemOnChangeInterval
        return returnVal
    ReportInventoryItemOnChangeInterval = property(fset=setReportInventoryItemOnChangeInterval, fget=getReportInventoryItemOnChangeInterval)


    def setActionsAreValid(self, value):
        self.__mActionsAreValid = value

    def getActionsAreValid(self):
        returnVal = None
        returnVal = self.__mActionsAreValid
        return returnVal
    ActionsAreValid = property(fset=setActionsAreValid, fget=getActionsAreValid)


    def setIgnoreAlarmAcknowledge(self, value):
        self.__mIgnoreAlarmAcknowledge = value

    def getIgnoreAlarmAcknowledge(self):
        returnVal = None
        returnVal = self.__mIgnoreAlarmAcknowledge
        return returnVal
    IgnoreAlarmAcknowledge = property(fset=setIgnoreAlarmAcknowledge, fget=getIgnoreAlarmAcknowledge)


    def setControllerFieldTypeID(self, value):
        self.__mControllerFieldTypeID = value

    def getControllerFieldTypeID(self):
        returnVal = None
        returnVal = self.__mControllerFieldTypeID
        return returnVal
    ControllerFieldTypeID = property(fset=setControllerFieldTypeID, fget=getControllerFieldTypeID)


    def setRefReadControllerField(self, value):
        self.__mRefReadControllerField = value

    def getRefReadControllerField(self):
        returnVal = None
        returnVal = self.__mRefReadControllerField
        return returnVal
    RefReadControllerField = property(fset=setRefReadControllerField, fget=getRefReadControllerField)


    def setRefWriteControllerField(self, value):
        self.__mRefWriteControllerField = value

    def getRefWriteControllerField(self):
        returnVal = None
        returnVal = self.__mRefWriteControllerField
        return returnVal
    RefWriteControllerField = property(fset=setRefWriteControllerField, fget=getRefWriteControllerField)


    def setWriteConditionalControllerField(self, value):
        self.__mWriteConditionalControllerField = value

    def getWriteConditionalControllerField(self):
        returnVal = None
        returnVal = self.__mWriteConditionalControllerField
        return returnVal
    WriteConditionalControllerField = property(fset=setWriteConditionalControllerField, fget=getWriteConditionalControllerField)


    def setWriteConditionalMinValue(self, value):
        self.__mWriteConditionalMinValue = value

    def getWriteConditionalMinValue(self):
        returnVal = None
        returnVal = self.__mWriteConditionalMinValue
        return returnVal
    WriteConditionalMinValue = property(fset=setWriteConditionalMinValue, fget=getWriteConditionalMinValue)


    def setWriteConditionalMaxValue(self, value):
        self.__mWriteConditionalMaxValue = value

    def getWriteConditionalMaxValue(self):
        returnVal = None
        returnVal = self.__mWriteConditionalMaxValue
        return returnVal
    WriteConditionalMaxValue = property(fset=setWriteConditionalMaxValue, fget=getWriteConditionalMaxValue)


    def setAlarmMinimumDuration(self, value):
        self.__mAlarmMinimumDuration = value

    def getAlarmMinimumDuration(self):
        returnVal = None
        returnVal = self.__mAlarmMinimumDuration
        return returnVal
    AlarmMinimumDuration = property(fset=setAlarmMinimumDuration, fget=getAlarmMinimumDuration)


    def setAlarmFileReplayInterval(self, value):
        self.__mAlarmFileReplayInterval = value

    def getAlarmFileReplayInterval(self):
        returnVal = None
        returnVal = self.__mAlarmFileReplayInterval
        return returnVal
    AlarmFileReplayInterval = property(fset=setAlarmFileReplayInterval, fget=getAlarmFileReplayInterval)


    def setReportInventoryItemOnChange(self, value):
        self.__mReportInventoryItemOnChange = value

    def getReportInventoryItemOnChange(self):
        returnVal = None
        returnVal = self.__mReportInventoryItemOnChange
        return returnVal
    ReportInventoryItemOnChange = property(fset=setReportInventoryItemOnChange, fget=getReportInventoryItemOnChange)


    def setEffectiveAmountFieldName(self, value):
        self.__mEffectiveAmountFieldName = value

    def getEffectiveAmountFieldName(self):
        returnVal = None
        returnVal = self.__mEffectiveAmountFieldName
        return returnVal
    EffectiveAmountFieldName = property(fset=setEffectiveAmountFieldName, fget=getEffectiveAmountFieldName)


    def setBatchReadLastRecord(self, value):
        self.__mBatchReadLastRecord = value

    def getBatchReadLastRecord(self):
        returnVal = None
        returnVal = self.__mBatchReadLastRecord
        return returnVal
    BatchReadLastRecord = property(fset=setBatchReadLastRecord, fget=getBatchReadLastRecord)


    def setLastRecordToTSPCHistoryTableTS(self, value):
        self.__mLastRecordToTSPCHistoryTableTS = value

    def getLastRecordToTSPCHistoryTableTS(self):
        returnVal = None
        returnVal = self.__mLastRecordToTSPCHistoryTableTS
        return returnVal
    LastRecordToTSPCHistoryTableTS = property(fset=setLastRecordToTSPCHistoryTableTS, fget=getLastRecordToTSPCHistoryTableTS)


    def setFirstReadInCurrentJob(self, value):
        self.__mFirstReadInCurrentJob = value

    def getFirstReadInCurrentJob(self):
        returnVal = None
        returnVal = self.__mFirstReadInCurrentJob
        return returnVal
    FirstReadInCurrentJob = property(fset=setFirstReadInCurrentJob, fget=getFirstReadInCurrentJob)


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


    def setStartCalcAfterDelayInSeconds(self, value):
        self.__mStartCalcAfterDelayInSeconds = value

    def getStartCalcAfterDelayInSeconds(self):
        returnVal = None
        returnVal = self.__mStartCalcAfterDelayInSeconds
        return returnVal
    StartCalcAfterDelayInSeconds = property(fset=setStartCalcAfterDelayInSeconds, fget=getStartCalcAfterDelayInSeconds)


    def setLastValidSampleTime(self, value):
        self.__mLastValidSampleTime = value

    def getLastValidSampleTime(self):
        returnVal = None
        returnVal = self.__mLastValidSampleTime
        return returnVal
    LastValidSampleTime = property(fset=setLastValidSampleTime, fget=getLastValidSampleTime)


    def setPrevValidValue(self, value):
        self.__mPrevValidValue = value

    def getPrevValidValue(self):
        returnVal = None
        returnVal = self.__mPrevValidValue
        return returnVal
    PrevValidValue = property(fset=setPrevValidValue, fget=getPrevValidValue)


    def setLastValidValue(self, value):
        self.__mLastValidValue = value
        self.__mLastValidSampleTime = self.__mLastSampleTime

    def getLastValidValue(self):
        returnVal = None
        returnVal = self.__mLastValidValue
        return returnVal
    LastValidValue = property(fset=setLastValidValue, fget=getLastValidValue)


    def setForceValueTimeout(self, value):
        self.__mForceValueTimeout = value

    def getForceValueTimeout(self):
        returnVal = None
        returnVal = self.__mForceValueTimeout
        return returnVal
    ForceValueTimeout = property(fset=setForceValueTimeout, fget=getForceValueTimeout)


    def setMaxValueUnitsPerMin(self, value):
        self.__mMaxValueUnitsPerMin = value

    def getMaxValueUnitsPerMin(self):
        returnVal = None
        returnVal = self.__mMaxValueUnitsPerMin
        return returnVal
    MaxValueUnitsPerMin = property(fset=setMaxValueUnitsPerMin, fget=getMaxValueUnitsPerMin)


    def setMinValueUnitsPerMin(self, value):
        self.__mMinValueUnitsPerMin = value

    def getMinValueUnitsPerMin(self):
        returnVal = None
        returnVal = self.__mMinValueUnitsPerMin
        return returnVal
    MinValueUnitsPerMin = property(fset=setMinValueUnitsPerMin, fget=getMinValueUnitsPerMin)


    def setValidateValue(self, value):
        self.__mValidateValue = value

    def getValidateValue(self):
        returnVal = None
        returnVal = self.__mValidateValue
        return returnVal
    ValidateValue = property(fset=setValidateValue, fget=getValidateValue)


    
    def setRejectsAReadCurrent(self, the_mRejectsAReadCurrent):
        
        self.__mRejectsAReadCurrent = the_mRejectsAReadCurrent
        if self.__mRejectsAReadCurrent > self.__mRejectsAReadLast:
            self.__mRejectsAReadDiff = self.__mRejectsAReadCurrent - self.__mRejectsAReadLast
        else:
            self.__mRejectsAReadDiff = 0

    def getRejectsAReadCurrent(self):
        returnVal = None
        
        returnVal = self.__mRejectsAReadCurrent
        return returnVal
    RejectsAReadCurrent = property(fset=setRejectsAReadCurrent, fget=getRejectsAReadCurrent)


    
    def setRejectsAReadLast(self, the_mRejectsAReadLast):
        
        self.__mRejectsAReadLast = the_mRejectsAReadLast
        if self.__mRejectsAReadCurrent > self.__mRejectsAReadLast:
            self.__mRejectsAReadDiff = self.__mRejectsAReadCurrent - self.__mRejectsAReadLast
        else:
            self.__mRejectsAReadDiff = 0

    def getRejectsAReadLast(self):
        returnVal = None
        
        returnVal = self.__mRejectsAReadLast
        return returnVal
    RejectsAReadLast = property(fset=setRejectsAReadLast, fget=getRejectsAReadLast)


    
    def setRejectsA(self, the_mRejectsA):
        
        self.__mRejectsA = the_mRejectsA
        if self.__mRejectsA > self.__mRejectsALast:
            self.__mRejectsADiff = self.__mRejectsA - self.__mRejectsALast
        else:
            self.__mRejectsADiff = 0

    def getRejectsA(self):
        returnVal = None
        
        returnVal = self.__mRejectsA
        return returnVal
    RejectsA = property(fset=setRejectsA, fget=getRejectsA)


    
    def setRejectsALast(self, the_mRejectsALast):
        
        self.__mRejectsALast = the_mRejectsALast
        if self.__mRejectsA > self.__mRejectsALast:
            self.__mRejectsADiff = self.__mRejectsA - self.__mRejectsALast
        else:
            self.__mRejectsADiff = 0

    def getRejectsALast(self):
        returnVal = None
        
        returnVal = self.__mRejectsALast
        return returnVal
    RejectsALast = property(fset=setRejectsALast, fget=getRejectsALast)


    def setRejectsADiff(self, the_mRejectsADiff):
        self.__mRejectsADiff = the_mRejectsADiff

    def getRejectsADiff(self):
        returnVal = None
        returnVal = self.__mRejectsADiff
        return returnVal
    RejectsADiff = property(fset=setRejectsADiff, fget=getRejectsADiff)


    def setRejectsAReadDiff(self, the_mRejectsAReadDiff):
        self.__mRejectsAReadDiff = the_mRejectsAReadDiff

    def getRejectsAReadDiff(self):
        returnVal = None
        returnVal = self.__mRejectsAReadDiff
        return returnVal
    RejectsAReadDiff = property(fset=setRejectsAReadDiff, fget=getRejectsAReadDiff)


    
    def setRejectReasonID(self, the_mRejectReasonID):
        self.__mRejectReasonID = the_mRejectReasonID

    def getRejectReasonID(self):
        returnVal = None
        returnVal = self.__mRejectReasonID
        return returnVal
    RejectReasonID = property(fset=setRejectReasonID, fget=getRejectReasonID)


    
    def setRejectsIncludeInRejectsTotal(self, value):
        self.__mRejectsIncludeInRejectsTotal = value

    def getRejectsIncludeInRejectsTotal(self):
        returnVal = None
        returnVal = self.__mRejectsIncludeInRejectsTotal
        return returnVal
    RejectsIncludeInRejectsTotal = property(fset=setRejectsIncludeInRejectsTotal, fget=getRejectsIncludeInRejectsTotal)


    
    def setRejectReasonOption(self, the_mRejectReasonOption):
        self.__mRejectReasonOption = the_mRejectReasonOption

    def getRejectReasonOption(self):
        returnVal = None
        returnVal = self.__mRejectReasonOption
        return returnVal
    RejectReasonOption = property(fset=setRejectReasonOption, fget=getRejectReasonOption)


    
    def setID(self, the_mID):
        self.__mID = the_mID

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    def getPUCL(self):
        returnVal = None
        returnVal = self.__mPUCL
        return returnVal
    PUCL = property(fget=getPUCL)


    def getPLCL(self):
        returnVal = None
        returnVal = self.__mPLCL
        return returnVal
    PLCL = property(fget=getPLCL)


    def getSMean(self):
        returnVal = None
        returnVal = self.__mSMean
        return returnVal
    SMean = property(fget=getSMean)


    
    def setUCL(self, the_mUCL):
        self.__mUCL = the_mUCL

    def getUCL(self):
        returnVal = None
        returnVal = self.__mUCL
        return returnVal
    UCL = property(fset=setUCL, fget=getUCL)


    
    def setLCL(self, the_mLCL):
        self.__mLCL = the_mLCL

    def getLCL(self):
        returnVal = None
        returnVal = self.__mLCL
        return returnVal
    LCL = property(fset=setLCL, fget=getLCL)


    def setMean(self, value):
        self.__mMean = value

    def getMean(self):
        returnVal = None
        returnVal = self.__mMean
        return returnVal
    Mean = property(fset=setMean, fget=getMean)


    def getQUCL(self):
        returnVal = None
        returnVal = self.__mQUCL
        return returnVal
    QUCL = property(fget=getQUCL)


    def getQLCL(self):
        returnVal = None
        returnVal = self.__mQLCL
        return returnVal
    QLCL = property(fget=getQLCL)


    def getSTDEV(self):
        returnVal = None
        returnVal = self.__mSTDEV
        return returnVal
    STDEV = property(fget=getSTDEV)


    
    def setFName(self, the_mFName):
        self.__mFName = the_mFName

    def getFName(self):
        returnVal = None
        returnVal = self.__mFName
        return returnVal
    FName = property(fset=setFName, fget=getFName)


    
    def setSPLastValue(self, the_mSPLastValue):
        self.__mSPLastValue = the_mSPLastValue

    def getSPLastValue(self):
        returnVal = None
        returnVal = self.__mSPLastValue
        return returnVal
    SPLastValue = property(fset=setSPLastValue, fget=getSPLastValue)


    
    def setSPLValue(self, the_mSPLValue):
        self.__mSPLValue = the_mSPLValue

    def getSPLValue(self):
        returnVal = None
        returnVal = self.__mSPLValue
        return returnVal
    SPLValue = property(fset=setSPLValue, fget=getSPLValue)


    
    def setSPHValue(self, the_mSPHValue):
        self.__mSPHValue = the_mSPHValue

    def getSPHValue(self):
        returnVal = None
        returnVal = self.__mSPHValue
        return returnVal
    SPHValue = property(fset=setSPHValue, fget=getSPHValue)


    
    def setSyncWrite(self, the_mSyncWrite):
        self.__mSyncWrite = the_mSyncWrite

    def getSyncWrite(self):
        returnVal = None
        returnVal = self.__mSyncWrite
        return returnVal
    SyncWrite = property(fset=setSyncWrite, fget=getSyncWrite)


    
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


    
    def setFieldID(self, the_mFieldID):
        self.__mFieldID = the_mFieldID

    def getFieldID(self):
        returnVal = None
        returnVal = self.__mFieldID
        return returnVal
    FieldID = property(fset=setFieldID, fget=getFieldID)


    
    def setChannelID(self, the_mChannelID):
        self.__mChannelID = the_mChannelID

    def getChannelID(self):
        returnVal = None
        returnVal = self.__mChannelID
        return returnVal
    ChannelID = property(fset=setChannelID, fget=getChannelID)


    
    def setChannelNum(self, the_mChannelNum):
        self.__mChannelNum = the_mChannelNum

    def getChannelNum(self):
        returnVal = None
        returnVal = self.__mChannelNum
        return returnVal
    ChannelNum = property(fset=setChannelNum, fget=getChannelNum)


    def getQuality(self):
        returnVal = None
        if self.RefReadControllerField is None:
            returnVal = self.__mQuality
        else:
            returnVal = self.RefReadControllerField.Quality
        return returnVal
    Quality = property(fget=getQuality)


    
    def setLastValue(self, the_mLastValue):
        ItemsCount = 0
        TransID = 0
        CancelID = 0
        strSQL = ''
        temp = ''
        SyncWErrIndex = 0
        SourceDataType = ''
        
        try:
            if self.ControllerFieldTypeID == 2:
                self.RefWriteControllerField.LastValue = the_mLastValue
                self.EndOfWrite()
                return

            if self.ID == 7733:
                strSQL = strSQL
            self.mBoolSyncWriteErr = False
            
            if self.__mOPCItemHandle > 0 and self.__mPMachine.ManualRead == False:
                ItemsCount = 1
                TransID = self.__mID
                CancelID = self.__mID * 10
                self.__mWriteServerHandles = [None, None]
                self.__mWriteValues = [None, None]
                if self.ScaledA != 0 and  ( the_mLastValue != '' ) :
                    
                    self.__mWriteValues[1] = ( the_mLastValue - self.ScaledB )  / self.ScaledA
                else:
                    self.__mWriteValues[1] = the_mLastValue
                self.__mWritevErrors = [None, None]
                self.__mPMachine.mIOCancelID = CancelID
                if self.__mHasWriteTag == True:
                    CancelID = CancelID + 1
                    
                    self.__mWriteServerHandles[1] = self.OPCItemW.ServerHandle
                    self.__mPMachine.mIOGroup = self.__mOPCItemW.Parent
                    if self.pMachine.UPDController == True and self.__mFieldDataType < 3:
                        if self.CheckWriteCondition():
                            if self.SyncWrite:
                                self.__mOPCItemW.Parent.SyncWrite(ItemsCount, self.__mWriteServerHandles, self.__mWriteValues, self.__mWritevErrors)
                            else:
                                self.__mOPCItemW.Parent.AsyncWrite(ItemsCount, self.__mWriteServerHandles, self.__mWriteValues, self.__mWritevErrors, TransID, CancelID)
                else:
                    if self.pMachine.UPDController == True and self.__mFieldDataType < 3:
                        self.__mWriteServerHandles[1] = self.OPCItem.ServerHandle
                        self.__mPMachine.mIOGroup = self.__mOPCItem.Parent
                        if self.CheckWriteCondition():
                            if self.pMachine.IsBatchUpdatePP == True:
                                if self.FName == self.pMachine.BatchUpdateP.FName:
                                    self.__mOPCItem.Parent.SyncWrite(ItemsCount, self.__mWriteServerHandles, self.__mWriteValues, self.__mWritevErrors)
                                    if self.__mWritevErrors(1) != 0:
                                        self.mBoolSyncWriteErr = True
                                else:
                                    if self.SyncWrite:
                                        self.__mOPCItem.Parent.SyncWrite(ItemsCount, self.__mWriteServerHandles, self.__mWriteValues, self.__mWritevErrors)
                                    else:
                                        self.__mOPCItem.Parent.AsyncWrite(ItemsCount, self.__mWriteServerHandles, self.__mWriteValues, self.__mWritevErrors, TransID, CancelID)
                            else:
                                if self.SyncWrite:
                                    self.__mOPCItem.Parent.SyncWrite(ItemsCount, self.__mWriteServerHandles, self.__mWriteValues, self.__mWritevErrors)
                                else:
                                    self.__mOPCItem.Parent.AsyncWrite(ItemsCount, self.__mWriteServerHandles, self.__mWriteValues, self.__mWritevErrors, TransID, CancelID)
                self.__mLastValue = the_mLastValue
            else:
                if self.__mFieldDataType == 4:
                    select_0 = str(self.__mSourceTableName).upper()
                    if (select_0 == 'TBLJOB') or (select_0 == 'VIEWTBLJOB') or (select_0 == 'TBLJOBCURRENT') or (select_0 == 'VIEWRTTBLJOBCURRENT'):
                        temp = '' + MdlADOFunctions.GetSingleValue(self.__mSourceFieldName, self.__mSourceTableName, 'ID=' + str(self.pMachine.ActiveJobID), 'CN')
                    elif (select_0 == 'TBLJOSH') or (select_0 == 'VIEWTBLJOSH') or (select_0 == 'TBLJOSHCURRENT') or (select_0 == 'VIEWRTTBLJOSHCURRENT'):
                        temp = '' + MdlADOFunctions.GetSingleValue(self.__mSourceFieldName, self.__mSourceTableName, 'JobID=' + str(self.pMachine.ActiveJobID) + ' AND ShiftID=' + str(self.__mPMachine.Server.CurrentShiftID), 'CN')
                    elif (select_0 == 'TBLPRODUCT'):
                        
                        temp = '' + MdlADOFunctions.GetSingleValue(self.__mSourceFieldName, self.__mSourceTableName, 'ID=' + str(self.pMachine.ActiveJob.ProductID), 'CN')
                        
                    elif (select_0 == 'TBLMOLDS'):
                        temp = '' + MdlADOFunctions.GetSingleValue(self.__mSourceFieldName, self.__mSourceTableName, 'ID=' + str(self.pMachine.ActiveJob.MoldID), 'CN')
                    elif (select_0 == 'TBLPRODUCTRECIPEJOB'):
                        temp = '' + MdlADOFunctions.GetSingleValue(self.__mSourceFieldName, self.__mSourceTableName, 'JobID=' + str(self.pMachine.ActiveJobID) + ' AND PropertyID = ' + str(self.PropertyID), 'CN')
                    elif (select_0 == 'TBLJOBMATERIAL'):
                        if self.__mSourceStrWhere == '':
                            temp = '' + MdlADOFunctions.GetSingleValue('SUM(' + self.__mSourceFieldName + ')', self.__mSourceTableName, 'Job=' + str(self.pMachine.ActiveJobID), 'CN')
                        else:
                            temp = '' + MdlADOFunctions.GetSingleValue('SUM(' + self.__mSourceFieldName + ')', self.__mSourceTableName, 'Job=' + str(self.pMachine.ActiveJobID) + ' AND ' + self.__mSourceStrWhere, 'CN')
                    elif (select_0 == 'TBLMACHINES'):
                        temp = '' + MdlADOFunctions.GetSingleValue(self.__mSourceFieldName, self.__mSourceTableName, 'ID=' + str(self.pMachine.ActiveJob.MachineID), 'CN')
                    else:
                        temp = '' + MdlADOFunctions.GetSingleValue(self.__mSourceFieldName, self.__mSourceTableName, self.__mSourceStrWhere, 'CN')
                        if temp == '':
                            temp = the_mLastValue
                    SourceDataType = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue('DATA_TYPE', 'INFORMATION_SCHEMA.COLUMNS', 'TABLE_NAME = \'' + str(self.__mSourceTableName) + '\' AND COLUMN_NAME = \'' + str(self.__mSourceFieldName) + '\'', 'CN'))
                    if isinstance(temp, numbers.Number) and SourceDataType != 'nvarchar':
                        
                        self.__mLastValue = MdlStatistics.fRoundNum(temp, self.__mPrecision, self.__mRoundType)
                    else:
                        self.__mLastValue = mdl_Common.strFixBadChars(temp)
                else:
                    if self.__mFieldDataType == 5:
                        temp = '' + MdlADOFunctions.GetSingleValue('CurrentValue', 'TblControllerFields', 'MachineID = ' + str(self.pMachine.ID) + ' AND FieldName=\'' + str(self.FName) + '\'', 'CN')
                        if temp != '':
                            if isinstance(temp, numbers.Number):
                                if self.__mCalcByDiff == True:
                                    
                                    if round(MdlADOFunctions.fGetRstValDouble(self.__mdReadValue), 10) != round(MdlADOFunctions.fGetRstValDouble(self.__mdPrevValue), 10):
                                        self.__mPrevSampleTime = self.__mLastSampleTime
                                        self.__mLastSampleTime = mdl_Common.NowGMT()
                                else:
                                    if MdlADOFunctions.fGetRstValString(MdlStatistics.fRoundNum(temp, self.__mPrecision, self.__mRoundType)) != self.__mLastValue:
                                        self.__mPrevSampleTime = self.__mLastSampleTime
                                        self.__mLastSampleTime = mdl_Common.NowGMT()
                                
                                self.__mLastValue = MdlStatistics.fRoundNum(temp, self.__mPrecision, self.__mRoundType)
                            else:
                                self.__mLastValue = temp
                    else:
                        if isinstance(the_mLastValue, numbers.Number):
                            
                            self.__mLastValue = MdlStatistics.fRoundNum(the_mLastValue, self.__mPrecision, self.__mRoundType)
                        else:
                            self.__mLastValue = the_mLastValue
                
                if self.__mCalcByDiff == True:
                    self.__mdReadValue = '' + MdlADOFunctions.GetSingleValue('dReadValue', 'TblControllerFields', 'MachineID = ' + str(self.pMachine.ID) + ' AND FieldName=\'' + str(self.FName) + '\'', 'CN')
                    
                    temp = '' + MdlADOFunctions.GetSingleValue('dLastReadTime', 'TblControllerFields', 'MachineID = ' + str(self.pMachine.ID) + ' AND FieldName=\'' + str(self.FName) + '\'', 'CN')
                    if temp != '' and self.ExternalUpdate == True:
                        self.__mdLastReadTime = datetime.strptime(temp, '%d/%m/%y %H:%M:%S')
            
            self.EndOfWrite()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                    
                MdlGlobal.RecordError('ControlParam:LastValue', str(0), error.args[0], 'Machine: ' + str(self.__mPMachine.ID) + ', Field: ' + str(self.__mFName) + ', Value: ' + str(the_mLastValue))

    
    def EndOfWrite(self):
        if (self.__mFName == 'TotalCycles'):
            if self.__mLastValue != '':
                if self.FieldDataType != 5:
                    self.pMachine.TotalCyclesLast = self.pMachine.TotalCycles
                    self.pMachine.TotalCycles = float(self.__mLastValue)
                
        elif (self.__mFName == 'UnitsProducedOK'):
            if self.__mLastValue != '':
                self.__mPMachine.ActiveJob.UnitsProducedOK = float(self.__mLastValue)
            else:
                self.__mPMachine.ActiveJob.UnitsProducedOK = 0
        elif (self.__mFName == 'MachineStop'):
            if self.__mLastValue != '':
                if int(self.__mLastValue) == self.__mPMachine.StopSignal:
                    self.__mPMachine.MachineSignalStop = True
                else:
                    self.__mPMachine.MachineSignalStop = False                
            else:
                self.__mPMachine.MachineSignalStop = False
                
        elif (self.__mFName == 'WorkOrder'):
            if self.__mLastValue != '':
                self.__mPMachine.ActiveJobID = int(self.__mLastValue)
            else:
                self.__mPMachine.ActiveJobID = 0
                
        elif (self.__mFName == 'CycleTime'):
            if self.__mLastValue != '':
                self.__mPMachine.CycleTime = round(float(self.__mLastValue), 2)
            else:
                self.__mPMachine.CycleTime = 0

        elif (self.__mFName == 'MachineEngine'):
            if self.__mLastValue != '':
                if int(self.__mLastValue) == self.__mPMachine.EngineSignal:
                    self.__mPMachine.EngineSignalActive = True
                else:
                    self.__mPMachine.EngineSignalActive = False
            else:
                self.__mPMachine.EngineSignalActive = False

        if not ( self.__mCitectDeviceType == 0 and self.__mFieldDataType == 5 ) :
            if self.__mLastValue == '':
                strSQL = 'Update TblControllerFields Set CurrentValue = NULL Where ID = ' + str(self.__mID)
            else:
                strSQL = 'Update TblControllerFields Set CurrentValue = N\'' + str(self.__mLastValue) + '\' Where ID = ' + str(self.__mID)
            MdlConnection.CN.execute(strSQL)
        self.XMLCalc()
            

    def getLastValue(self):
        returnVal = None
        returnVal = self.__mLastValue
        return returnVal
    LastValue = property(fset=setLastValue, fget=getLastValue)


    def setPrevValue(self, the_mPrevValue):
        self.__mPrevValue = the_mPrevValue

    def getPrevValue(self):
        returnVal = None
        returnVal = self.__mPrevValue
        return returnVal
    PrevValue = property(fset=setPrevValue, fget=getPrevValue)


    def setWriteValue(self, the_mWriteValue):
        self.__mWriteValue = the_mWriteValue

    def getWriteValue(self):
        returnVal = None
        returnVal = self.__mWriteValue
        return returnVal
    WriteValue = property(fset=setWriteValue, fget=getWriteValue)


    
    def setPrecision(self, the_mPrecision):
        self.__mPrecision = the_mPrecision

    def getPrecision(self):
        returnVal = None
        returnVal = self.__mPrecision
        return returnVal
    Precision = property(fset=setPrecision, fget=getPrecision)


    
    def setLastSampleTime(self, the_mLastSampleTime):
        self.__mLastSampleTime = the_mLastSampleTime

    def getLastSampleTime(self):
        returnVal = None
        returnVal = self.__mLastSampleTime
        return returnVal
    LastSampleTime = property(fset=setLastSampleTime, fget=getLastSampleTime)


    
    def setPrevSampleTime(self, the_mPrevSampleTime):
        self.__mPrevSampleTime = the_mPrevSampleTime

    def getPrevSampleTime(self):
        returnVal = None
        returnVal = self.__mPrevSampleTime
        return returnVal
    PrevSampleTime = property(fset=setPrevSampleTime, fget=getPrevSampleTime)


    
    def setTagName(self, the_mTagName):
        self.__mTagName = the_mTagName

    def getTagName(self):
        returnVal = None
        returnVal = self.__mTagName
        return returnVal
    TagName = property(fset=setTagName, fget=getTagName)


    def getTagNameW(self):
        returnVal = None
        returnVal = self.__mTagNameW
        return returnVal
    TagNameW = property(fget=getTagNameW)


    def setWriteTag(self, vWriteTag):
        self.__mHasWriteTag = vWriteTag
        if vWriteTag == True:
            self.__mTagNameW = self.__mTagName + '_W'
        else:
            self.__mTagNameW = ''
    WriteTag = property(fset=setWriteTag)


    
    def setCVarAddress(self, the_mCVarAddress):
        self.__mCVarAddress = the_mCVarAddress

    def getCVarAddress(self):
        returnVal = None
        returnVal = self.__mCVarAddress
        return returnVal
    CVarAddress = property(fset=setCVarAddress, fget=getCVarAddress)


    
    def setCalcFunction(self, the_mCalcFunction):
        self.__mCalcFunction = the_mCalcFunction

    def getCalcFunction(self):
        returnVal = None
        returnVal = self.__mCalcFunction
        return returnVal
    CalcFunction = property(fset=setCalcFunction, fget=getCalcFunction)


    def getBatchGroup(self):
        returnVal = None
        returnVal = self.__mBatchGroup
        return returnVal
    BatchGroup = property(fget=getBatchGroup)


    
    def setOPCItemHandle(self, the_mOPCItemHandle):
        self.__mOPCItemHandle = the_mOPCItemHandle

    def getOPCItemHandle(self):
        returnVal = None
        returnVal = self.__mOPCItemHandle
        return returnVal
    OPCItemHandle = property(fset=setOPCItemHandle, fget=getOPCItemHandle)


    
    def setOPCItemWHandle(self, the_mOPCItemWHandle):
        self.__mOPCItemWHandle = the_mOPCItemWHandle

    def getOPCItemWHandle(self):
        returnVal = None
        returnVal = self.OPCItemWHandle
        return returnVal
    OPCItemWHandle = property(fset=setOPCItemWHandle, fget=getOPCItemWHandle)


    
    def setSPOPCItemHandle(self, the_mSPOPCItemHandle):
        self.__mSPOPCItemHandle = the_mSPOPCItemHandle

    def getSPOPCItemHandle(self):
        returnVal = None
        returnVal = self.__mSPOPCItemHandle
        return returnVal
    SPOPCItemHandle = property(fset=setSPOPCItemHandle, fget=getSPOPCItemHandle)


    
    def setSPLOPCItemHandle(self, the_mSPLOPCItemHandle):
        self.__mSPLOPCItemHandle = the_mSPLOPCItemHandle

    def getSPLOPCItemHandle(self):
        returnVal = None
        returnVal = self.__mSPLOPCItemHandle
        return returnVal
    SPLOPCItemHandle = property(fset=setSPLOPCItemHandle, fget=getSPLOPCItemHandle)


    
    def setSPHOPCItemHandle(self, the_mSPHOPCItemHandle):
        self.__mSPHOPCItemHandle = the_mSPHOPCItemHandle

    def getSPHOPCItemHandle(self):
        returnVal = None
        returnVal = self.__mSPHOPCItemHandle
        return returnVal
    SPHOPCItemHandle = property(fset=setSPHOPCItemHandle, fget=getSPHOPCItemHandle)


    
    def setBatchTable(self, the_mBatchTable):
        self.__mBatchTable = the_mBatchTable

    def getBatchTable(self):
        returnVal = None
        returnVal = self.__mBatchTable
        return returnVal
    BatchTable = property(fset=setBatchTable, fget=getBatchTable)


    
    def setSourceTableName(self, the_mSourceTableName):
        self.__mSourceTableName = the_mSourceTableName

    def getSourceTableName(self):
        returnVal = None
        returnVal = self.__mSourceTableName
        return returnVal
    SourceTableName = property(fset=setSourceTableName, fget=getSourceTableName)


    
    def setSourceFieldName(self, the_mSourceFieldName):
        self.__mSourceFieldName = the_mSourceFieldName

    def getSourceFieldName(self):
        returnVal = None
        returnVal = self.__mSourceFieldName
        return returnVal
    SourceFieldName = property(fset=setSourceFieldName, fget=getSourceFieldName)


    
    def setSourceStrWhere(self, the_mSourceStrWhere):
        self.__mSourceStrWhere = the_mSourceStrWhere

    def getSourceStrWhere(self):
        returnVal = None
        returnVal = self.__mSourceStrWhere
        return returnVal
    SourceStrWhere = property(fset=setSourceStrWhere, fget=getSourceStrWhere)


    def setBatchParams(self, the_mBatchParams):
        self.__mBatchParams = the_mBatchParams

    def getBatchParams(self):
        returnVal = None
        returnVal = self.__mBatchParams
        return returnVal
    BatchParams = property(fset=setBatchParams, fget=getBatchParams)


    def setDataSamples(self, the_mDataSamples):
        self.__mDataSamples = the_mDataSamples

    def getDataSamples(self):
        return self.__mDataSamples
    DataSamples = property(fset=setDataSamples, fget=getDataSamples)


    def setAlarms(self, value):
        self.__mAlarms = value

    def getAlarms(self):
        returnVal = None
        returnVal = self.__mAlarms
        return returnVal
    Alarms = property(fset=setAlarms, fget=getAlarms)


    def setActions(self, the_mActions):
        self.__mActions = the_mActions

    def getActions(self):
        returnVal = None
        returnVal = self.__mActions
        return returnVal
    Actions = property(fset=setActions, fget=getActions)


    
    def setDirectRead(self, the_mDirectRead):
        self.__mDirectRead = the_mDirectRead

    def getDirectRead(self):
        returnVal = None
        returnVal = self.__mDirectRead
        return returnVal
    DirectRead = property(fset=setDirectRead, fget=getDirectRead)


    
    def setIsSPCValue(self, the_mIsSPCValue):
        self.__mIsSPCValue = the_mIsSPCValue

    def getIsSPCValue(self):
        returnVal = None
        returnVal = self.__mIsSPCValue
        return returnVal
    IsSPCValue = property(fset=setIsSPCValue, fget=getIsSPCValue)


    
    def setFieldDataType(self, the_mFieldDataType):
        self.__mFieldDataType = the_mFieldDataType

    def getFieldDataType(self):
        returnVal = None
        returnVal = self.__mFieldDataType
        return returnVal
    FieldDataType = property(fset=setFieldDataType, fget=getFieldDataType)


    
    def setCitectDeviceType(self, the_mCitectDeviceType):
        self.__mCitectDeviceType = the_mCitectDeviceType

    def getCitectDeviceType(self):
        returnVal = None
        returnVal = self.__mCitectDeviceType
        return returnVal
    CitectDeviceType = property(fset=setCitectDeviceType, fget=getCitectDeviceType)


    
    def setSPCTable(self, the_mSPCTable):
        self.__mSPCTable = the_mSPCTable

    def getSPCTable(self):
        returnVal = None
        returnVal = self.__mSPCTable
        return returnVal
    SPCTable = property(fset=setSPCTable, fget=getSPCTable)


    
    def setSPCSamplesMaxCount(self, the_mSPCSamplesMaxCount):
        self.__mSPCSamplesMaxCount = the_mSPCSamplesMaxCount

    def getSPCSamplesMaxCount(self):
        returnVal = None
        returnVal = self.__mSPCSamplesMaxCount
        return returnVal
    SPCSamplesMaxCount = property(fset=setSPCSamplesMaxCount, fget=getSPCSamplesMaxCount)


    
    def setSPCGroupSize(self, the_mSPCGroupSize):
        self.__mSPCGroupSize = the_mSPCGroupSize

    def getSPCGroupSize(self):
        returnVal = None
        returnVal = self.__mSPCGroupSize
        return returnVal
    SPCGroupSize = property(fset=setSPCGroupSize, fget=getSPCGroupSize)


    
    def setPropertyID(self, the_mPropertyID):
        self.__mPropertyID = the_mPropertyID

    def getPropertyID(self):
        returnVal = None
        returnVal = self.__mPropertyID
        return returnVal
    PropertyID = property(fset=setPropertyID, fget=getPropertyID)


    
    def setInMainTable(self, the_mInMainTable):
        self.__mInMainTable = the_mInMainTable

    def getInMainTable(self):
        returnVal = None
        returnVal = self.__mInMainTable
        return returnVal
    InMainTable = property(fset=setInMainTable, fget=getInMainTable)


    
    def setErrorAlarmActive(self, the_mErrorAlarmActive):
        self.__mErrorAlarmActive = the_mErrorAlarmActive

    def getErrorAlarmActive(self):
        returnVal = None
        returnVal = self.__mErrorAlarmActive
        return returnVal
    ErrorAlarmActive = property(fset=setErrorAlarmActive, fget=getErrorAlarmActive)


    
    def setAlarmActiveVoice(self, the_mErrorAlarmActivevoice):
        self.__mErrorAlarmActiveVoice = the_mErrorAlarmActivevoice

    def getAlarmActiveVoice(self):
        returnVal = None
        returnVal = self.__mErrorAlarmActiveVoice
        return returnVal
    AlarmActiveVoice = property(fset=setAlarmActiveVoice, fget=getAlarmActiveVoice)


    
    def setSendSMSOnAlarm(self, the_mSendSMSOnAlarm):
        self.__mSendSMSOnAlarm = the_mSendSMSOnAlarm

    def getSendSMSOnAlarm(self):
        returnVal = None
        returnVal = self.__mSendSMSOnAlarm
        return returnVal
    SendSMSOnAlarm = property(fset=setSendSMSOnAlarm, fget=getSendSMSOnAlarm)


    
    def setAlarmCycleAcknowledge(self, the_mAlarmCycleAcknowledge):
        self.__mAlarmCycleAcknowledge = the_mAlarmCycleAcknowledge

    def getAlarmCycleAcknowledge(self):
        returnVal = None
        returnVal = self.__mAlarmCycleAcknowledge
        return returnVal
    AlarmCycleAcknowledge = property(fset=setAlarmCycleAcknowledge, fget=getAlarmCycleAcknowledge)


    
    def setAlarmPerminentAcknowledge(self, the_mAlarmPerminentAcknowledge):
        self.__mAlarmPerminentAcknowledge = the_mAlarmPerminentAcknowledge

    def getAlarmPerminentAcknowledge(self):
        returnVal = None
        returnVal = self.__mAlarmPerminentAcknowledge
        return returnVal
    AlarmPerminentAcknowledge = property(fset=setAlarmPerminentAcknowledge, fget=getAlarmPerminentAcknowledge)


    
    def setpMachine(self, the_mPMachine):
        self.__mPMachine = the_mPMachine

    def getpMachine(self):
        returnVal = None
        returnVal = self.__mPMachine
        return returnVal
    pMachine = property(fset=setpMachine, fget=getpMachine)


    
    def setAlarmFile(self, the_mAlarmFile):
        self.__mAlarmFile = the_mAlarmFile

    def getAlarmFile(self):
        returnVal = None
        returnVal = self.__mAlarmFile
        return returnVal
    AlarmFile = property(fset=setAlarmFile, fget=getAlarmFile)


    
    def setAlarmArea(self, the_mAlarmArea):
        self.__mAlarmArea = the_mAlarmArea

    def getAlarmArea(self):
        returnVal = None
        returnVal = self.__mAlarmArea
        return returnVal
    AlarmArea = property(fset=setAlarmArea, fget=getAlarmArea)


    
    def setAlarmFirstDetected(self, the_mAlarmFirstDetected):
        self.__mAlarmFirstDetected = the_mAlarmFirstDetected

    def getAlarmFirstDetected(self):
        returnVal = None
        returnVal = self.__mAlarmFirstDetected
        return returnVal
    AlarmFirstDetected = property(fset=setAlarmFirstDetected, fget=getAlarmFirstDetected)


    
    def setAlarmFileLastPlay(self, the_mAlarmFileLastPlay):
        self.__mAlarmFileLastPlay = the_mAlarmFileLastPlay

    def getAlarmFileLastPlay(self):
        returnVal = None
        returnVal = self.__mAlarmFileLastPlay
        return returnVal
    AlarmFileLastPlay = property(fset=setAlarmFileLastPlay, fget=getAlarmFileLastPlay)


    
    def setChangeJobOnValueChanged(self, the_mChangeJobOnValueChanged):
        self.__mChangeJobOnValueChanged = the_mChangeJobOnValueChanged

    def getChangeJobOnValueChanged(self):
        returnVal = None
        returnVal = self.__mChangeJobOnValueChanged
        return returnVal
    ChangeJobOnValueChanged = property(fset=setChangeJobOnValueChanged, fget=getChangeJobOnValueChanged)


    
    def setPrintLabelID(self, the_mPrintLabelID):
        self.__mPrintLabelID = the_mPrintLabelID

    def getPrintLabelID(self):
        returnVal = None
        VBFiles.writeText(None, LabelID == self.__mPrintLabelID, '\n')
        return returnVal
    PrintLabelID = property(fset=setPrintLabelID, fget=getPrintLabelID)


    
    def setCalstringExpression(self, the_mCalstringExpression):
        self.__mCalstringExpression = the_mCalstringExpression

    def getCalstringExpression(self):
        returnVal = None
        returnVal = self.__mCalstringExpression
        return returnVal
    CalstringExpression = property(fset=setCalstringExpression, fget=getCalstringExpression)


    
    def setPrintLabelMachineID(self, the_mPrintLabelMachineID):
        self.__mPrintLabelMachineID = the_mPrintLabelMachineID

    def getPrintLabelMachineID(self):
        returnVal = None
        VBFiles.writeText(None, LabelMachineID == self.__mPrintLabelMachineID, '\n')
        return returnVal
    PrintLabelMachineID = property(fset=setPrintLabelMachineID, fget=getPrintLabelMachineID)


    
    def setOPCItem(self, the_mOPCItem):
        self.__mOPCItem = the_mOPCItem

    def getOPCItem(self):
        returnVal = None
        returnVal = self.__mOPCItem
        return returnVal
    OPCItem = property(fset=setOPCItem, fget=getOPCItem)


    
    def setSPOPCItem(self, the_mSPOPCItem):
        self.__mSPOPCItem = the_mSPOPCItem

    def getSPOPCItem(self):
        returnVal = None
        returnVal = self.__mSPOPCItem
        return returnVal
    SPOPCItem = property(fset=setSPOPCItem, fget=getSPOPCItem)


    
    def setSPLOPCItem(self, the_mSPLOPCItem):
        self.__mSPLOPCItem = the_mSPLOPCItem

    def getSPLOPCItem(self):
        returnVal = None
        returnVal = self.__mSPLOPCItem
        return returnVal
    SPLOPCItem = property(fset=setSPLOPCItem, fget=getSPLOPCItem)


    
    def setSPHOPCItem(self, the_mSPHOPCItem):
        self.__mSPHOPCItem = the_mSPHOPCItem

    def getSPHOPCItem(self):
        returnVal = None
        returnVal = self.__mSPHOPCItem
        return returnVal
    SPHOPCItem = property(fset=setSPHOPCItem, fget=getSPHOPCItem)


    
    def setOPCItemW(self, the_mOPCItemW):
        self.__mOPCItemW = the_mOPCItemW

    def getOPCItemW(self):
        returnVal = None
        returnVal = self.__mOPCItemW
        return returnVal
    OPCItemW = property(fset=setOPCItemW, fget=getOPCItemW)


    def setBatchUpdateParam(self, tBatchUpdateParam):
        
        self.__mBatchUpdateParam = tBatchUpdateParam
    BatchUpdateParam = property(fset=setBatchUpdateParam)


    def getAlarmDescription(self):
        returnVal = None
        
        if IsNumeric(self.__mLastAlarmValue):
            if IsNumeric(self.__mLastAlarmLimit):
                if round(float(self.__mLastAlarmValue), 1) > float(self.__mLastAlarmLimit):
                    returnVal = 'value:' + self.__mLastAlarmValue + ' > ' + self.__mLastAlarmLimit
                    return returnVal
            if IsNumeric(self.__mLastAlarmLimit):
                if round(float(self.__mLastAlarmValue), 1) < float(self.__mLastAlarmLimit):
                    returnVal = 'value:' + self.__mLastAlarmValue + ' < ' + self.__mLastAlarmLimit
                    return returnVal
        if self.AlarmDescription == '':
            returnVal = 'value:' + round(float(self.__mLastAlarmValue), 1)
        if Err.Number != 0:
            Err.Clear()
        return returnVal
    AlarmDescription = property(fget=getAlarmDescription)


    def setBatchTableHistory(self, theBatchTableHistory):
        self.__mBatchTableHistory = theBatchTableHistory

    def getBatchTableHistory(self):
        returnVal = None
        returnVal = self.__mBatchTableHistory
        return returnVal
    BatchTableHistory = property(fset=setBatchTableHistory, fget=getBatchTableHistory)


    def setErrorCountAlarm(self, the_mErrorCountAlarm):
        self.__mErrorCountAlarm = the_mErrorCountAlarm

    def getErrorCountAlarm(self):
        returnVal = None
        returnVal = self.__mErrorCountAlarm
        return returnVal
    ErrorCountAlarm = property(fset=setErrorCountAlarm, fget=getErrorCountAlarm)
