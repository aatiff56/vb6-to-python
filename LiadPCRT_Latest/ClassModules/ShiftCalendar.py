from Common import MdlADOFunctions as adoFunc
from LiadPCUnite.DataAccess import QueryExecutor as qe
from LiadPCUnite.BusinessLogic import SqlConnector as sc
from LiadPCUnite.Global import Logs
from datetime import datetime

class ShiftCalendar:
    sqlCntr = sc.SqlConnector()
    logger = Logs.Logger()

    Clockwise = 0
    CounterClockwise = 1
    mID = 0
    mLName = ''
    mEName = ''
    mSMRotationOrder = SMRotationOrderOption()
    mIsDefault = False
    mCurrentShift = Shift()
    mCurrentShiftDefID = 0
    mIsActive = False
    mSendSMSAlarmsFromMyRT = False
    mDepartments = Collection()
    mWindowsProcessID = 0
    mSQLReconnectInterval = 0
    mLastSQLReconnect = None

    def Init(self, pShiftCalendarID):
        try:
            strSQL = ''
            self.sqlCntr.OpenConnection()

            strSQL = 'SELECT * FROM STblShiftCalendar WHERE ID = ' + pShiftCalendarID
            Rst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            RstData = Rst.SelectAllData(strSQL)

            if RstData.RecordCount == 1:
                self.ID = pShiftCalendarID
                self.LName = adoFunc.fGetRstValString(
                    RstData["LName"])
                self.EName = adoFunc.fGetRstValString(
                    RstData["EName"])
                select_variable_0 = adoFunc.fGetRstValLong(
                    RstData["SMRotationOrder"])
                if (select_variable_0 == 1):
                    self.SMRotationOrder = self.Clockwise
                elif (select_variable_0 == 2):
                    self.SMRotationOrder = self.CounterClockwise
                else:
                    self.SMRotationOrder = self.Clockwise
                self.IsDefault = adoFunc.fGetRstValBool(
                    RstData["IsDefault"], False)
                self.IsActive = adoFunc.fGetRstValBool(
                    RstData["IsActive"], False)
                self.CurrentShiftDefID = adoFunc.fGetRstValLong(
                    RstData["CurrentShiftDefID"])
                self.SendSMSAlarmsFromMyRT = adoFunc.fGetRstValBool(
                    RstData["SendSMSAlarmsFromMyRT"], False)
                self.WindowsProcessID = adoFunc.fGetRstValLong(
                    RstData["WindowsProcessID"])
                self.SQLReconnectInterval = adoFunc.fGetRstValLong(
                    RstData["SQLReconnectInterval"])
                if self.SQLReconnectInterval == 0:
                    self.SQLReconnectInterval = 15
                self.LastSQLReconnect = datetime.now()
            RstData.Close()
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)

    def AddDepartment(self, pDepartment):
        try:
            self.Departments.Add(pDepartment, str(pDepartment.ID))
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(type(self) + '.AddDepartment:', error,
                              'ShiftCalendarID: ' + self.ID + '. DepartmentID: ' + pDepartment.ID)

    def UpdateWindowsProcessID(self):
        try:
            strSQL = 'UPDATE STblShiftCalendar SET Descr = NULL, WindowsProcessID = ' + \
                self.WindowsProcessID + ' WHERE ID = ' + self.ID
            CN.Execute(strSQL)

        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)

    def setID(self, value):
        self.mID = value

    def getID(self):
        fn_return_value = self.mID
        return fn_return_value
    ID = property(fset=setID, fget=getID)

    def setLName(self, value):
        self.mLName = value

    def getLName(self):
        fn_return_value = self.mLName
        return fn_return_value
    LName = property(fset=setLName, fget=getLName)

    def setEName(self, value):
        self.mEName = value

    def getEName(self):
        fn_return_value = self.mEName
        return fn_return_value
    EName = property(fset=setEName, fget=getEName)

    def setSMRotationOrder(self, value):
        self.mSMRotationOrder = value

    def getSMRotationOrder(self):
        fn_return_value = self.mSMRotationOrder
        return fn_return_value
    SMRotationOrder = property(
        fset=setSMRotationOrder, fget=getSMRotationOrder)

    def setIsDefault(self, value):
        self.mIsDefault = value

    def getIsDefault(self):
        fn_return_value = self.mIsDefault
        return fn_return_value
    IsDefault = property(fset=setIsDefault, fget=getIsDefault)

    def setCurrentShift(self, value):
        self.mCurrentShift = value

    def getCurrentShift(self):
        fn_return_value = self.mCurrentShift
        return fn_return_value
    CurrentShift = property(fset=setCurrentShift, fget=getCurrentShift)

    def setCurrentShiftDefID(self, value):
        self.mCurrentShiftDefID = value

    def getCurrentShiftDefID(self):
        fn_return_value = self.mCurrentShiftDefID
        return fn_return_value
    CurrentShiftDefID = property(
        fset=setCurrentShiftDefID, fget=getCurrentShiftDefID)

    def setIsActive(self, value):
        self.mIsActive = value

    def getIsActive(self):
        fn_return_value = self.mIsActive
        return fn_return_value
    IsActive = property(fset=setIsActive, fget=getIsActive)

    def setSendSMSAlarmsFromMyRT(self, value):
        self.mSendSMSAlarmsFromMyRT = value

    def getSendSMSAlarmsFromMyRT(self):
        fn_return_value = self.mSendSMSAlarmsFromMyRT
        return fn_return_value
    SendSMSAlarmsFromMyRT = property(
        fset=setSendSMSAlarmsFromMyRT, fget=getSendSMSAlarmsFromMyRT)

    def setDepartments(self, value):
        self.mDepartments = value

    def getDepartments(self):
        fn_return_value = self.mDepartments
        return fn_return_value
    Departments = property(fset=setDepartments, fget=getDepartments)

    def setSQLReconnectInterval(self, value):
        self.mSQLReconnectInterval = value

    def getSQLReconnectInterval(self):
        fn_return_value = self.mSQLReconnectInterval
        return fn_return_value
    SQLReconnectInterval = property(
        fset=setSQLReconnectInterval, fget=getSQLReconnectInterval)

    def setLastSQLReconnect(self, value):
        self.mLastSQLReconnect = value

    def getLastSQLReconnect(self):
        fn_return_value = self.mLastSQLReconnect
        return fn_return_value
    LastSQLReconnect = property(
        fset=setLastSQLReconnect, fget=getLastSQLReconnect)

    def setWindowsProcessID(self, value):
        self.mWindowsProcessID = value

    def getWindowsProcessID(self):
        fn_return_value = self.mWindowsProcessID
        return fn_return_value
    WindowsProcessID = property(
        fset=setWindowsProcessID, fget=getWindowsProcessID)
