from datetime import datetime
import MdlADOFunctions
import MdlConnection
import MdlGlobal

class SystemVariables:

    Last = 0
    Avg50 = 1
    Avg = 2
    Standard = 3    
    JobRecipe = 0
    ProductRecipe = 1
    JobID = 1
    JoshID = 2
    ERPJobID = 3
    OriginalJobID = 4    
    Box = 1
    Pallet = 2
    mUnitsProducedLeftZero = False
    # mCycleTimeCalc = CycleTimeCalcOption()
    # mTotalEquipmentMaterialEfficencyOption = TotalEquipmentMaterialEfficencyOption()
    mStartUnitsProducedFromZero = False
    # mFirstDayOfWeek = VbDayOfWeek()
    mChangeJobPath = ''
    mPrintLabelPath = ''
    mCycleTimeEffFactor = 0
    mMachineTimeEffFactor = 0
    mRejectsEffFactor = 0
    mCavitiesEffFactor = 0
    mAlarmStatusDuringSetup = False
    mAlarmDataPresented = False
    mHistoryIntervalMin = 0
    mHistoryEndIntervalMin = 0
    # mInventoryBatchOption = InventoryBatchOption()
    # mUnitsReportedOKFrom = UnitsReportedOKFromOption()
    mReportInventoryItemMinAmount = 0
    mAddPackageTypeToInventoryBatch = False
    mInventoryStatusOnCreation = 0
    mHistoryIntervalSec = 0
    mAllowEventReasonsWithNoDefinition = False

    def Init(self):
        try:
            strSQL = ''
            strSQL = 'SELECT * FROM STblSystemVariableFields'

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchall()

            for RstValue in RstData:
                select_variable_0 = MdlADOFunctions.fGetRstValString(RstValue.FieldName)
                if (select_variable_0 == 'CycleTimeCalc'):
                    select_variable_1 = MdlADOFunctions.fGetRstValString(RstValue.CValue.upper())
                    if (select_variable_1 == '50AVG'):
                        self.CycleTimeCalc = self.Avg50
                    elif (select_variable_1 == 'AVG'):
                        self.CycleTimeCalc = self.Avg
                    elif (select_variable_1 == 'STD'):
                        self.CycleTimeCalc = self.Standard
                    elif (select_variable_1 == 'LAST'):
                        self.CycleTimeCalc = self.Last
                elif (select_variable_0 == 'AlarmDataPresented'):
                    select_variable_2 = MdlADOFunctions.fGetRstValString('CValue').upper()
                    if (select_variable_2 == 'TRUE'):
                        self.AlarmDataPresented = True
                    elif (select_variable_2 == 'FALSE'):
                        self.AlarmDataPresented = False
                    else:
                        self.AlarmDataPresented = True
                elif (select_variable_0 == 'AlarmStatusDuringSetup'):
                    select_variable_3 = MdlADOFunctions.fGetRstValString('CValue').upper()
                    if (select_variable_3 == 'TRUE'):
                        self.AlarmStatusDuringSetup = True
                    elif (select_variable_3 == 'FALSE'):
                        self.AlarmStatusDuringSetup = False
                    else:
                        self.AlarmStatusDuringSetup = True
                elif (select_variable_0 == 'CavitiesEffFactor'):
                    self.CavitiesEffFactor = MdlADOFunctions.fGetRstValDouble(RstValue.CValue)
                elif (select_variable_0 == 'CycleTimeEffFactor'):
                    self.CycleTimeEffFactor = MdlADOFunctions.fGetRstValDouble(RstValue.CValue)
                elif (select_variable_0 == 'MachineTimeEffFactor'):
                    self.MachineTimeEffFactor = MdlADOFunctions.fGetRstValDouble(RstValue.CValue)
                elif (select_variable_0 == 'RejectsEffFactor'):
                    self.RejectsEffFactor = MdlADOFunctions.fGetRstValDouble(RstValue.CValue)
                elif (select_variable_0 == 'ChangeJobPath'):
                    self.ChangeJobPath = MdlADOFunctions.fGetRstValString(RstValue.CValue)
                elif (select_variable_0 == 'FirstDayOfWeek'):
                    select_variable_4 = MdlADOFunctions.fGetRstValString(RstValue.CValue.upper())
                    if (select_variable_4 == 'SUN'):
                        self.FirstDayOfWeek = 'Sunday'
                    elif (select_variable_4 == 'MON'):
                        self.FirstDayOfWeek = 'Monday'
                elif (select_variable_0 == 'UnitsProducedLeftZero'):
                    select_variable_5 = MdlADOFunctions.fGetRstValString('CValue').upper()
                    if (select_variable_5 == 'TRUE'):
                        self.UnitsProducedLeftZero = True
                    elif (select_variable_5 == 'FALSE'):
                        self.UnitsProducedLeftZero = False
                    else:
                        self.UnitsProducedLeftZero = True
                elif (select_variable_0 == 'StartUnitsProducedFromZero'):
                    select_variable_6 = MdlADOFunctions.fGetRstValString('CValue').upper()
                    if (select_variable_6 == 'TRUE'):
                        self.StartUnitsProducedFromZero = True
                    elif (select_variable_6 == 'FALSE'):
                        self.StartUnitsProducedFromZero = False
                    else:
                        self.StartUnitsProducedFromZero = True
                elif (select_variable_0 == 'HistoryEndIntervalMin'):
                    self.HistoryEndIntervalMin = MdlADOFunctions.fGetRstValLong(RstValue.CValue)
                elif (select_variable_0 == 'HistoryIntervalMin'):
                    self.HistoryIntervalMin = MdlADOFunctions.fGetRstValLong(RstValue.CValue)
                    if self.HistoryEndIntervalMin == 0:
                        self.HistoryEndIntervalMin = 15
                elif (select_variable_0 == 'TotalEquipmentMaterialEfficencyOption'):
                    select_variable_7 = MdlADOFunctions.fGetRstValString(RstValue.CValue.upper())
                    if (select_variable_7 == 'RECIPEJOB'):
                        self.TotalEquipmentMaterialEfficencyOption = self.JobRecipe
                    else:
                        self.TotalEquipmentMaterialEfficencyOption = self.ProductRecipe
                elif (select_variable_0 == 'InventoryBatchOption'):
                    select_variable_8 = MdlADOFunctions.fGetRstValString(RstValue.CValue.upper())
                    if (select_variable_8 == '1'):
                        self.InventoryBatchOption = self.JobID
                    elif (select_variable_8 == '2'):
                        self.InventoryBatchOption = self.JoshID
                    elif (select_variable_8 == '3'):
                        self.InventoryBatchOption = self.ERPJobID
                    elif (select_variable_8 == '4'):
                        self.InventoryBatchOption = self.OriginalJobID
                elif (select_variable_0 == 'UnitsReportedOKFrom'):
                    select_variable_9 = MdlADOFunctions.fGetRstValString(RstValue.CValue.upper())
                    if (select_variable_9 == 'BOX'):
                        self.UnitsReportedOKFrom = self.Box
                    elif (select_variable_9 == 'PALLET'):
                        self.UnitsReportedOKFrom = self.Pallet
                elif (select_variable_0 == 'ReportInventoryItemMinAmount'):
                    self.ReportInventoryItemMinAmount = MdlADOFunctions.fGetRstValDouble(RstValue.CValue)
                elif (select_variable_0 == 'AddPackageTypeToInventoryBatch'):
                    self.AddPackageTypeToInventoryBatch = MdlADOFunctions.fGetRstValBool(RstValue.CValue, False)
                elif (select_variable_0 == 'InventoryStatusOnCreation'):
                    self.InventoryStatusOnCreation = MdlADOFunctions.fGetRstValLong(RstValue.CValue)
                    if self.InventoryStatusOnCreation == 0:
                        self.InventoryStatusOnCreation = 1
                elif (select_variable_0 == 'HistoryIntervalSec'):
                    self.HistoryIntervalSec = MdlADOFunctions.fGetRstValLong(RstValue.CValue)
                elif (select_variable_0 == 'AllowEventReasonsWithNoDefinition'):
                    self.AllowEventReasonsWithNoDefinition = MdlADOFunctions.fGetRstValBool(RstValue.CValue, False)

            RstCursor.close()
            RstCursor = None
        
        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
            MdlGlobal.RecordError(str(type(self)) + '.Init', 0, error.args[0], '')


    def setAllowEventReasonsWithNoDefinition(self, value):
        self.mAllowEventReasonsWithNoDefinition = value

    def getAllowEventReasonsWithNoDefinition(self):
        fn_return_value = self.mAllowEventReasonsWithNoDefinition
        return fn_return_value
    AllowEventReasonsWithNoDefinition = property(fset=setAllowEventReasonsWithNoDefinition, fget=getAllowEventReasonsWithNoDefinition)


    def setHistoryIntervalSec(self, value):
        self.mHistoryIntervalSec = value

    def getHistoryIntervalSec(self):
        fn_return_value = self.mHistoryIntervalSec
        return fn_return_value
    HistoryIntervalSec = property(fset=setHistoryIntervalSec, fget=getHistoryIntervalSec)


    def setInventoryStatusOnCreation(self, value):
        self.mInventoryStatusOnCreation = value

    def getInventoryStatusOnCreation(self):
        fn_return_value = self.mInventoryStatusOnCreation
        return fn_return_value
    InventoryStatusOnCreation = property(fset=setInventoryStatusOnCreation, fget=getInventoryStatusOnCreation)


    def setReportInventoryItemMinAmount(self, value):
        self.mReportInventoryItemMinAmount = value

    def getReportInventoryItemMinAmount(self):
        fn_return_value = self.mReportInventoryItemMinAmount
        return fn_return_value
    ReportInventoryItemMinAmount = property(fset=setReportInventoryItemMinAmount, fget=getReportInventoryItemMinAmount)


    def setUnitsProducedLeftZero(self, value):
        self.mUnitsProducedLeftZero = value

    def getUnitsProducedLeftZero(self):
        fn_return_value = self.mUnitsProducedLeftZero
        return fn_return_value
    UnitsProducedLeftZero = property(fset=setUnitsProducedLeftZero, fget=getUnitsProducedLeftZero)


    def setCycleTimeCalc(self, value):
        self.mCycleTimeCalc = value

    def getCycleTimeCalc(self):
        fn_return_value = self.mCycleTimeCalc
        return fn_return_value
    CycleTimeCalc = property(fset=setCycleTimeCalc, fget=getCycleTimeCalc)


    def setTotalEquipmentMaterialEfficencyOption(self, value):
        self.mTotalEquipmentMaterialEfficencyOption = value

    def getTotalEquipmentMaterialEfficencyOption(self):
        fn_return_value = self.mTotalEquipmentMaterialEfficencyOption
        return fn_return_value
    TotalEquipmentMaterialEfficencyOption = property(fset=setTotalEquipmentMaterialEfficencyOption, fget=getTotalEquipmentMaterialEfficencyOption)


    def setStartUnitsProducedFromZero(self, value):
        self.mStartUnitsProducedFromZero = value

    def getStartUnitsProducedFromZero(self):
        fn_return_value = self.mStartUnitsProducedFromZero
        return fn_return_value
    StartUnitsProducedFromZero = property(fset=setStartUnitsProducedFromZero, fget=getStartUnitsProducedFromZero)


    def setFirstDayOfWeek(self, value):
        self.mFirstDayOfWeek = value

    def getFirstDayOfWeek(self):
        fn_return_value = self.mFirstDayOfWeek
        return fn_return_value
    FirstDayOfWeek = property(fset=setFirstDayOfWeek, fget=getFirstDayOfWeek)


    def setChangeJobPath(self, value):
        self.mChangeJobPath = value

    def getChangeJobPath(self):
        fn_return_value = self.mChangeJobPath
        return fn_return_value
    ChangeJobPath = property(fset=setChangeJobPath, fget=getChangeJobPath)


    def setPrintLabelPath(self, value):
        self.mPrintLabelPath = value

    def getPrintLabelPath(self):
        return self.mPrintLabelPath
    PrintLabelPath = property(fset=setPrintLabelPath, fget=getPrintLabelPath)


    def setCycleTimeEffFactor(self, value):
        self.mCycleTimeEffFactor = value

    def getCycleTimeEffFactor(self):
        fn_return_value = self.mCycleTimeEffFactor
        return fn_return_value
    CycleTimeEffFactor = property(fset=setCycleTimeEffFactor, fget=getCycleTimeEffFactor)


    def setMachineTimeEffFactor(self, value):
        self.mMachineTimeEffFactor = value

    def getMachineTimeEffFactor(self):
        fn_return_value = self.mMachineTimeEffFactor
        return fn_return_value
    MachineTimeEffFactor = property(fset=setMachineTimeEffFactor, fget=getMachineTimeEffFactor)


    def setRejectsEffFactor(self, value):
        self.mRejectsEffFactor = value

    def getRejectsEffFactor(self):
        fn_return_value = self.mRejectsEffFactor
        return fn_return_value
    RejectsEffFactor = property(fset=setRejectsEffFactor, fget=getRejectsEffFactor)


    def setCavitiesEffFactor(self, value):
        self.mCavitiesEffFactor = value

    def getCavitiesEffFactor(self):
        fn_return_value = self.mCavitiesEffFactor
        return fn_return_value
    CavitiesEffFactor = property(fset=setCavitiesEffFactor, fget=getCavitiesEffFactor)


    def setAlarmStatusDuringSetup(self, value):
        self.mAlarmStatusDuringSetup = value

    def getAlarmStatusDuringSetup(self):
        fn_return_value = self.mAlarmStatusDuringSetup
        return fn_return_value
    AlarmStatusDuringSetup = property(fset=setAlarmStatusDuringSetup, fget=getAlarmStatusDuringSetup)


    def setAlarmDataPresented(self, value):
        self.mAlarmDataPresented = value

    def getAlarmDataPresented(self):
        fn_return_value = self.mAlarmDataPresented
        return fn_return_value
    AlarmDataPresented = property(fset=setAlarmDataPresented, fget=getAlarmDataPresented)


    def setHistoryIntervalMin(self, value):
        self.mHistoryIntervalMin = value

    def getHistoryIntervalMin(self):
        fn_return_value = self.mHistoryIntervalMin
        return fn_return_value
    HistoryIntervalMin = property(fset=setHistoryIntervalMin, fget=getHistoryIntervalMin)


    def setHistoryEndIntervalMin(self, value):
        self.mHistoryEndIntervalMin = value

    def getHistoryEndIntervalMin(self):
        fn_return_value = self.mHistoryEndIntervalMin
        return fn_return_value
    HistoryEndIntervalMin = property(fset=setHistoryEndIntervalMin, fget=getHistoryEndIntervalMin)


    def setInventoryBatchOption(self, value):
        self.mInventoryBatchOption = value

    def getInventoryBatchOption(self):
        fn_return_value = self.mInventoryBatchOption
        return fn_return_value
    InventoryBatchOption = property(fset=setInventoryBatchOption, fget=getInventoryBatchOption)


    def setUnitsReportedOKFrom(self, value):
        self.mUnitsReportedOKFrom = value

    def getUnitsReportedOKFrom(self):
        fn_return_value = self.mUnitsReportedOKFrom
        return fn_return_value
    UnitsReportedOKFrom = property(fset=setUnitsReportedOKFrom, fget=getUnitsReportedOKFrom)


    def setAddPackageTypeToInventoryBatch(self, value):
        self.mAddPackageTypeToInventoryBatch = value

    def getAddPackageTypeToInventoryBatch(self):
        fn_return_value = self.mAddPackageTypeToInventoryBatch
        return fn_return_value
    AddPackageTypeToInventoryBatch = property(fset=setAddPackageTypeToInventoryBatch, fget=getAddPackageTypeToInventoryBatch)

    
