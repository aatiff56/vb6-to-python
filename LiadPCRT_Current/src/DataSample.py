import enum
from datetime import datetime
from datetime import timedelta

import MdlADOFunctions
import mdl_Common
import MdlConnection
import MdlGlobal
import ControlParam


class DataSampleIntervalUnit(enum.Enum):
    DS_Minute = 1
    DS_Hour = 2
    DS_Day = 3
    DS_Week = 4
    DS_Month = 5
    DS_Quarter = 6
    DS_Year = 7
    DS_SpecificTimestamp = 8

class DataSampleAggFunction(enum.Enum):
    DS_Sum = 1
    DS_Avg = 2
    DS_Max = 3
    DS_Min = 4
    DS_Count = 5
    DS_Diff = 6

class DataSample:
    __mAggFunction = DataSampleAggFunction
    __mIntervalUnit = DataSampleIntervalUnit
    __mIntervalAmount = 0
    __mControlParam = None
    __mDestinationControlParam = None
    __mDataCollection = {}
    __mFinalValue = ''
    __mID = 0
    __mInterval = ''
    __mSpecificTimeStamp = datetime.now().date
    __mDestinationTableName = ''
    __mDestinationFieldName = ''
    __mDestinationCriteria = ''
    __mMinLimitFactor = 0.0
    __mMaxLimitFactor = 0.0
    __mCheckLimits = False
    __mAddValueOnMachineStop = False


    def AddValue(self, value, TimeStamp=None):        
        try:
            if self.AddValueOnMachineStop == True:
                if self.CheckLimits:
                    if ( MdlADOFunctions.fGetRstValDouble(value) >=  ( self.ControlParam.Mean * self.MinLimitFactor ) )  and  ( MdlADOFunctions.fGetRstValDouble(value) <=  ( self.ControlParam.Mean * self.MaxLimitFactor ) ) :
                        if TimeStamp is None or TimeStamp == 0:
                            self.__mDataCollection.Add(float(mdl_Common.NowGMT()), value)
                        else:
                            self.__mDataCollection.Add(float(TimeStamp), value)
                else:
                    if TimeStamp is None or TimeStamp == 0:
                        self.__mDataCollection.Add(float(mdl_Common.NowGMT()), value)
                    else:
                        self.__mDataCollection.Add(float(TimeStamp), value)
            else:
                if self.ControlParam.pMachine.MachineStop == False:
                    if self.CheckLimits:
                        if ( MdlADOFunctions.fGetRstValDouble(value) >=  ( self.ControlParam.Mean * self.MinLimitFactor ) )  and  ( MdlADOFunctions.fGetRstValDouble(value) <=  ( self.ControlParam.Mean * self.MaxLimitFactor ) ) :
                            if TimeStamp is None or TimeStamp == 0:
                                self.__mDataCollection.Add(float(mdl_Common.NowGMT()), value)
                            else:
                                self.__mDataCollection.Add(float(TimeStamp), value)
                    else:
                        if TimeStamp is None or TimeStamp == 0:
                            self.__mDataCollection.Add(float(mdl_Common.NowGMT()), value)
                        else:
                            self.__mDataCollection.Add(float(TimeStamp), value)
        except:
            pass


    def RemoveValue(self, key):
        try:
            self.__mDataCollection.Remove(key)
        except:
            pass


    def CheckRelevantData(self):
        dblNow = 0.0
        dblMinValue = 0.0
        colValue = None
        keys = []
        SingleKey = None

        try:
            # dblNow = float(mdl_Common.NowGMT())
            dblNow = mdl_Common.NowGMT().timestamp()
            
            if (self.__mIntervalUnit == DataSampleIntervalUnit.DS_Minute):
                dblMinValue = (timedelta(minutes= -1 * self.__mIntervalAmount) + mdl_Common.NowGMT()).timestamp()
            elif (self.__mIntervalUnit == DataSampleIntervalUnit.DS_Hour):
                dblMinValue = (timedelta(hours= -1 * self.__mIntervalAmount) + mdl_Common.NowGMT()).timestamp()
            elif (self.__mIntervalUnit == DataSampleIntervalUnit.DS_Day):
                dblMinValue = (timedelta(days= -1 * self.__mIntervalAmount) + mdl_Common.NowGMT()).timestamp()
            elif (self.__mIntervalUnit == DataSampleIntervalUnit.DS_Week):
                dblMinValue = (timedelta(weeks= -1 * self.__mIntervalAmount) + mdl_Common.NowGMT()).timestamp()
            elif (self.__mIntervalUnit == DataSampleIntervalUnit.DS_Month):
                dblMinValue = (timedelta(months= -1 * self.__mIntervalAmount) + mdl_Common.NowGMT()).timestamp()
            elif (self.__mIntervalUnit == DataSampleIntervalUnit.DS_Quarter):
                dblMinValue = (timedelta(quaters= -4 * self.__mIntervalAmount) + mdl_Common.NowGMT()).timestamp()
            elif (self.__mIntervalUnit == DataSampleIntervalUnit.DS_Year):
                dblMinValue = (timedelta(years= -1 * self.__mIntervalAmount) + mdl_Common.NowGMT()).timestamp()
            elif (self.__mIntervalUnit == DataSampleIntervalUnit.DS_SpecificTimestamp):
                dblMinValue = (self.__mSpecificTimeStamp)
            
            keys = self.__mDataCollection.keys()
            for SingleKey in keys:
                if float(SingleKey) < dblMinValue:
                    self.RemoveValue(SingleKey)
                else:
                    break        
        except BaseException as error:
            pass


    def Calc(self):
        SingleValue = None
        strSQL = ''
        
        try:
            if (self.__mAggFunction == DataSampleAggFunction.DS_Sum):
                self.__mFinalValue = 0
                for SingleValue in self.__mDataCollection:
                    self.__mFinalValue = str(float(self.__mFinalValue) + float(SingleValue))
            elif (self.__mAggFunction == DataSampleAggFunction.DS_Max):
                self.__mFinalValue = 0
                for SingleValue in self.__mDataCollection.values():
                    if float(SingleValue) > float(self.__mFinalValue):
                        self.__mFinalValue = str(float(SingleValue))
            elif (self.__mAggFunction == DataSampleAggFunction.DS_Min):
                if len(self.__mDataCollection) > 0:
                    self.__mFinalValue = list(self.__mDataCollection.values())[0]
                    for SingleValue in self.__mDataCollection.values():
                        if float(SingleValue) < float(self.__mFinalValue):
                            self.__mFinalValue = str(float(SingleValue))
                else:
                    self.__mFinalValue = 0
            elif (self.__mAggFunction == DataSampleAggFunction.DS_Count):
                self.__mFinalValue = len(self.__mDataCollection)
            elif (self.__mAggFunction == DataSampleAggFunction.DS_Diff):
                if len(self.__mDataCollection) == 0:
                    self.__mFinalValue = 0
                elif len(self.__mDataCollection) == 1:
                    self.__mFinalValue = list(self.__mDataCollection.values())[0]
                else:
                    
                    if float(list(self.__mDataCollection.values())[len(self.__mDataCollection) - 1]) - float(list(self.__mDataCollection.values())[0]) < 0:
                        self.__mFinalValue = list(self.__mDataCollection.values())[0]
                    else:
                        self.__mFinalValue = str(float(list(self.__mDataCollection.values())[len(self.__mDataCollection) - 1]) - float(list(self.__mDataCollection.values())[0]))
            elif (self.__mAggFunction == DataSampleAggFunction.DS_Avg):
                if len(self.__mDataCollection) == 0:
                    self.__mFinalValue = 0
                else:
                    self.__mFinalValue = 0
                    for SingleValue in self.__mDataCollection.values():
                        self.__mFinalValue = str(float(self.__mFinalValue) + float(SingleValue))
                    self.__mFinalValue = str(float(self.__mFinalValue) / len(self.__mDataCollection))
            
            if not ( self.__mDestinationControlParam[0] is None ) :
                self.__mDestinationControlParam[0].LastValue = self.__mFinalValue
            
            if self.__mDestinationTableName and self.__mDestinationFieldName and self.__mDestinationCriteria:
                strSQL = 'UPDATE ' + self.__mDestinationTableName + ' SET ' + self.__mDestinationFieldName + ' = ' + str(self.__mFinalValue) + ' WHERE ' + str(self.__mDestinationCriteria)
                MdlConnection.CN.execute(strSQL)

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)


    def Init(self, pMachine, DataSampleID):
        returnVal = None
        strSQL = ''
        RstCursor = None
        vParam = [None]
        ControllerFieldName = ''
        DestinationControllerFieldName = ''

        try:
            strSQL = 'SELECT * FROM TblDataSamples WHERE ID = ' + str(DataSampleID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.__mID = MdlADOFunctions.fGetRstValLong(RstData.ID)
                ControllerFieldName = MdlADOFunctions.fGetRstValString(RstData.ControllerFieldName)
                DestinationControllerFieldName = MdlADOFunctions.fGetRstValString(RstData.DestinationControllerFieldName)
                self.__mIntervalAmount = MdlADOFunctions.fGetRstValLong(RstData.IntervalAmount)
                self.__mInterval = MdlADOFunctions.fGetRstValString(RstData.IntervalAmount)
                if MdlADOFunctions.fGetRstValString(RstData.MinLimitFactor) != '' and MdlADOFunctions.fGetRstValString(RstData.MaxLimitFactor) != '':
                    self.CheckLimits = True
                    self.__mMinLimitFactor = MdlADOFunctions.fGetRstValDouble(RstData.MinLimitFactor)
                    self.__mMaxLimitFactor = MdlADOFunctions.fGetRstValDouble(RstData.MaxLimitFactor)
                else:
                    self.CheckLimits = False
                self.__mAddValueOnMachineStop = MdlADOFunctions.fGetRstValBool(RstData.AddValueOnMachineStop, True)
                if (RstData.IntervalUnit == 1):
                    self.__mIntervalUnit = DataSampleIntervalUnit.DS_Year
                    self.__mInterval = self.__mInterval + 'y'
                elif (RstData.IntervalUnit == 2):
                    self.__mIntervalUnit = DataSampleIntervalUnit.DS_Quarter
                    self.__mInterval = self.__mInterval + 'q'
                elif (RstData.IntervalUnit == 3):
                    self.__mIntervalUnit = DataSampleIntervalUnit.DS_Month
                    self.__mInterval = self.__mInterval + 'm'
                elif (RstData.IntervalUnit == 4):
                    self.__mIntervalUnit = DataSampleIntervalUnit.DS_Week
                    self.__mInterval = self.__mInterval + 'w'
                elif (RstData.IntervalUnit == 5):
                    self.__mIntervalUnit = DataSampleIntervalUnit.DS_Day
                    self.__mInterval = self.__mInterval + 'd'
                elif (RstData.IntervalUnit == 6):
                    self.__mIntervalUnit = DataSampleIntervalUnit.DS_Hour
                    self.__mInterval = self.__mInterval + 'h'
                elif (RstData.IntervalUnit == 7):
                    self.__mIntervalUnit = DataSampleIntervalUnit.DS_Minute
                    self.__mInterval = self.__mInterval + 'n'
                if (RstData.AggFunction == 'Sum'):
                    self.__mAggFunction = DataSampleAggFunction.DS_Sum
                elif (RstData.AggFunction == 'Avg'):
                    self.__mAggFunction = DataSampleAggFunction.DS_Avg
                elif (RstData.AggFunction == 'Min'):
                    self.__mAggFunction = DataSampleAggFunction.DS_Min
                elif (RstData.AggFunction == 'Max'):
                    self.__mAggFunction = DataSampleAggFunction.DS_Max
                elif (RstData.AggFunction == 'Count'):
                    self.__mAggFunction = DataSampleAggFunction.DS_Count
                elif (RstData.AggFunction == 'Diff'):
                    self.__mAggFunction = DataSampleAggFunction.DS_Diff
            else:
                raise Exception("No data found.")
            RstCursor.close()
    
            if pMachine.GetParam(ControllerFieldName, vParam) == True:
                self.__mControlParam = vParam
            if DestinationControllerFieldName != '':
                if pMachine.GetParam(DestinationControllerFieldName, vParam) == True:
                    self.__mDestinationControlParam = vParam

        except BaseException as error:        
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError('LeaderRT:DataSample:Init()', str(0), error.args[0], 'MachineID: ' + str(pMachine.ID) + ', ControllerFieldName: ' + str(ControllerFieldName))

        RstCursor = None
        return returnVal

    def Reset(self):
        
        self.__mFinalValue = ''
        self.__mDataCollection.removeAll
        if Err.Number != 0:
            Err.Clear()

    def InitDynamic(self, pMachine, pid, pControllerFieldName, pIntervalUnit, pAggFunction, pDestinationControllerFieldName=None, pIntervalAmount=None, pSpecificTimeStamp=None, pDestinationTableName=None, pDestinationFieldName=None, pDestinationCriteria=None):
        vParam = self.ControlParam.ControlParam()
        
        self.__mID = pid
        self.__mIntervalUnit = pIntervalUnit
        self.__mAggFunction = pAggFunction
        self.__mInterval = 'Since' + str(Format(pSpecificTimeStamp, 'yyyymmddHHnn'))
        if pMachine.GetParam(pControllerFieldName, vParam) == True:
            self.__mControlParam = vParam
        if not pSpecificTimeStamp is None:
            self.__mSpecificTimeStamp = pSpecificTimeStamp
        if not pIntervalAmount is None:
            self.__mIntervalAmount = pIntervalAmount
        if not pDestinationTableName is None:
            self.__mDestinationTableName = pDestinationTableName
        if not pDestinationFieldName is None:
            self.__mDestinationFieldName = pDestinationFieldName
        if not pDestinationCriteria is None:
            self.__mDestinationCriteria = pDestinationCriteria
        if not pDestinationControllerFieldName is None:
            if pMachine.GetParam(pDestinationControllerFieldName, vParam) == True:
                self.__mDestinationControlParam = vParam
        if Err.Number != 0:
            Err.Clear()


    def __del__(self):
        self.__mControlParam = None
        self.__mDestinationControlParam = None
        self.__mDataCollection.clear()
        self.__mDataCollection = None


    def setMinLimitFactor(self, value):
        self.__mMinLimitFactor = value

    def getMinLimitFactor(self):
        returnVal = None
        returnVal = self.__mMinLimitFactor
        return returnVal
    MinLimitFactor = property(fset=setMinLimitFactor, fget=getMinLimitFactor)


    def setMaxLimitFactor(self, value):
        self.__mMaxLimitFactor = value

    def getMaxLimitFactor(self):
        returnVal = None
        returnVal = self.__mMaxLimitFactor
        return returnVal
    MaxLimitFactor = property(fset=setMaxLimitFactor, fget=getMaxLimitFactor)


    def setAddValueOnMachineStop(self, value):
        self.__mAddValueOnMachineStop = value

    def getAddValueOnMachineStop(self):
        returnVal = None
        returnVal = self.__mAddValueOnMachineStop
        return returnVal
    AddValueOnMachineStop = property(fset=setAddValueOnMachineStop, fget=getAddValueOnMachineStop)


    def setCheckLimits(self, value):
        self.__mCheckLimits = value

    def getCheckLimits(self):
        returnVal = None
        returnVal = self.__mCheckLimits
        return returnVal
    CheckLimits = property(fset=setCheckLimits, fget=getCheckLimits)


    def getInterval(self):
        returnVal = None
        returnVal = self.__mInterval
        return returnVal
    Interval = property(fget=getInterval)


    def __setIntervalUnit(self, value):
        self.__mIntervalUnit = value

    def __getIntervalUnit(self):
        returnVal = None
        returnVal = self.__mIntervalUnit
        return returnVal
    __IntervalUnit = property(fset=__setIntervalUnit, fget=__getIntervalUnit)


    def __setIntervalAmount(self, value):
        self.__mIntervalAmount = value

    def __getIntervalAmount(self):
        returnVal = None
        returnVal = self.__mIntervalAmount
        return returnVal
    __IntervalAmount = property(fset=__setIntervalAmount, fget=__getIntervalAmount)


    
    def setControlParam(self, value):
        self.__mControlParam = value

    def getControlParam(self):
        returnVal = None
        returnVal = self.__mControlParam
        return returnVal
    ControlParam = property(fset=setControlParam, fget=getControlParam)


    
    def setDestinationControlParam(self, value):
        self.__mDestinationControlParam = value

    def getDestinationControlParam(self):
        returnVal = None
        returnVal = self.__mDestinationControlParam
        return returnVal
    DestinationControlParam = property(fset=setDestinationControlParam, fget=getDestinationControlParam)


    def __setAggFunction(self, value):
        self.__mAggFunction = value

    def __getAggFunction(self):
        returnVal = None
        returnVal = self.__mAggFunction
        return returnVal
    __AggFunction = property(fset=__setAggFunction, fget=__getAggFunction)


    def setFinalValue(self, value):
        self.__mFinalValue = value

    def getFinalValue(self):
        returnVal = None
        returnVal = self.__mFinalValue
        return returnVal
    FinalValue = property(fset=setFinalValue, fget=getFinalValue)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)

    
