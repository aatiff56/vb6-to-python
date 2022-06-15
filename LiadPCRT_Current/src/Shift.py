from Common import MdlADOFunctions as adoFunc
from LiadPCUnite.DataAccess import QueryExecutor as qe
from LiadPCUnite.BusinessLogic import SqlConnector as sc
from LiadPCUnite.Global import Logs
from datetime import datetime

class Shift:
    mID: 0
    mShiftCalendarID = 0
    mShiftDefID = 0
    mStartTime = None
    mEndTime = None
    mManagerID = 0
    mIsWorkingShift = False

    sqlCntr = sc.SqlConnector()
    logger = Logs.Logger()

    def Init(self, pShiftID):
        try:
            strSQL = ''
            self.sqlCntr.OpenConnection()
            Rst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            strSQL = 'SELECT ID,ShiftCalendarID,ShiftDefID,ManagerID,StartTime,IsWorkingShift FROM TblShift WHERE ID = ' + pShiftID
            RstData = Rst.SelectAllData(strSQL)
            
            if RstData.RecordCount == 1:
                self.ID = pShiftID
                self.ShiftCalendarID = adoFunc.fGetRstValLong(RstData["ShiftCalendarID"])
                self.ShiftDefID = adoFunc.fGetRstValLong(RstData["ShiftDefID"])
                self.ManagerID = adoFunc.fGetRstValLong(RstData["ManagerID"])
                self.StartTime = RstData["StartTime"]
                self.IsWorkingShift = adoFunc.fGetRstValBool(RstData["IsWorkingShift"], True)
            RstData.Close()
            RstData = None
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)

    def Create(self, pShiftDefID):
        try:
            strSQL = ''
            SourceRst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            TargetRst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            tNewShiftID = 0
            WDayEng = ''
            WDayLoc = ''
            
            self.sqlCntr.OpenConnection()
            strSQL = 'SELECT * FROM TblShiftDef WHERE ID = ' + pShiftDefID
            SourceRstData = SourceRst.SelectAllData(strSQL)

            if SourceRstData.RecordCount == 1:
                strSQL = 'SELECT * FROM TblShift WHERE ID = 0'
                TargetRstData = TargetRst.SelectAllData(strSQL)
                if TargetRstData.RecordCount == 0:
                    TargetRstData.AddNew()
                    TargetRstData["ShiftCalendarID"] = SourceRstData["ShiftCalendarID"]
                    TargetRstData["ManagerID"] = adoFunc.fGetRstValLong(SourceRstData["ManagerUserID"])
                    TargetRstData["StartTime"] = datetime.now()
                    TargetRstData["wDay"] = SourceRstData["wDay"]
                    TargetRstData["ShiftName"] = SourceRstData["ShiftName"]
                    TargetRstData["Department"] = SourceRstData["Department"]
                    TargetRstData["ShiftDefID"] = pShiftDefID
                    WDayEng = adoFunc.fGetRstValString(adoFunc.GetSingleValue('WDayEng', 'tblWeekDays', 'ID=' + SourceRstData["wDay"], 'CN'))
                    WDayLoc = adoFunc.fGetRstValString(adoFunc.GetSingleValue('WDayLoc', 'tblWeekDays', 'ID=' + SourceRstData["wDay"], 'CN'))
                    TargetRstData["WDayEng"] = WDayEng
                    TargetRstData["WDayLoc"] = WDayLoc
                    TargetRstData["ShiftStatus"] = 1
                    TargetRstData["IsWorkingShift"] = adoFunc.fGetRstValBool(SourceRstData["IsWorkingShift"], True)
                    TargetRstData["PermanentWorkersHours"] = adoFunc.fGetRstValLong(SourceRstData["PermanentWorkersHours"])
                    TargetRstData.Update()
                    tNewShiftID = adoFunc.fGetRstValLong(TargetRstData["ID"])
                    TargetRstData.Close()
            SourceRstData.Close()
            self.Init(tNewShiftID)
            if self.ShiftCalendarID > 0:
                strSQL = 'Update STblShiftCalendar set CurrentShiftID = ' + tNewShiftID + ', CurrentShiftDefID = ' + pShiftDefID + ' Where ID = ' + self.ShiftCalendarID
                SourceRst.ManipulateData(strSQL)
                
                strSQL = 'Update STblSystemVariables set CurrentShiftID = ' + tNewShiftID + ', CurrentShiftDef = ' + pShiftDefID
                SourceRst.ManipulateData(strSQL)
            else:
                strSQL = 'Update STblSystemVariables set CurrentShiftID = ' + tNewShiftID + ', CurrentShiftDef = ' + pShiftDefID
                SourceRst.ManipulateData(strSQL)
            SourceRst = None
            TargetRst = None
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)

    def CloseShift(self, pNextShiftID):
        try:
            strSQL = ''
            Rst = qe.QueryExecutor(self.sqlCntr.GetConnection())
            self.sqlCntr.OpenConnection()
            strSQL = 'SELECT * FROM TblShift WHERE ID = ' + self.ID
            RstData = Rst.SelectAllData(strSQL)
                    
            if Rst.RecordCount == 1:
                Rst["EndTime"] = datetime.now()
                Rst["DurationHr"] = DateDiff('h', Rst["StartTime"], Rst["EndTime"])
                Rst["NextShiftID"] = pNextShiftID
                Rst["ShiftStatus"] = 2
                Rst.Update()
            Rst.Close()
            Rst = None
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)


    def setIsWorkingShift(self, value):
        self.mIsWorkingShift = value

    def getIsWorkingShift(self):
        fn_return_value = self.mIsWorkingShift
        return fn_return_value
    IsWorkingShift = property(fset=setIsWorkingShift, fget=getIsWorkingShift)

    def setID(self, value):
        self.mID = value

    def getID(self):
        fn_return_value = self.mID
        return fn_return_value
    ID = property(fset=setID, fget=getID)

    def setShiftCalendarID(self, value):
        self.mShiftCalendarID = value

    def getShiftCalendarID(self):
        fn_return_value = self.mShiftCalendarID
        return fn_return_value
    ShiftCalendarID = property(fset=setShiftCalendarID, fget=getShiftCalendarID)

    def setManagerID(self, value):
        self.mManagerID = value

    def getManagerID(self):
        fn_return_value = self.mManagerID
        return fn_return_value
    ManagerID = property(fset=setManagerID, fget=getManagerID)

    def setShiftDefID(self, value):
        self.mShiftDefID = value

    def getShiftDefID(self):
        fn_return_value = self.mShiftDefID
        return fn_return_value
    ShiftDefID = property(fset=setShiftDefID, fget=getShiftDefID)

    def setStartTime(self, value):
        self.mStartTime = value

    def getStartTime(self):
        fn_return_value = self.mStartTime
        return fn_return_value
    StartTime = property(fset=setStartTime, fget=getStartTime)

    def setEndTime(self, value):
        self.mEndTime = value

    def getEndTime(self):
        fn_return_value = self.mEndTime
        return fn_return_value
    EndTime = property(fset=setEndTime, fget=getEndTime)
