import MdlADOFunctions
import MdlConnection
import MdlGlobal

class Shift:
    __mID = 0
    __mShiftCalendarID = 0
    __mShiftDefID = 0
    __mStartTime = None
    __mEndTime = None
    __mManagerID = 0
    __mIsWorkingShift = False

    def Init(self, pShiftID):
        strSQL = ''
        RstCursor = None
        
        try:
            strSQL = 'SELECT ID,ShiftCalendarID,ShiftDefID,ManagerID,StartTime,IsWorkingShift FROM TblShift WHERE ID = ' + str(pShiftID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstData:
                self.ID = pShiftID
                self.ShiftCalendarID = MdlADOFunctions.fGetRstValLong(RstData.ShiftCalendarID)
                self.ShiftDefID = MdlADOFunctions.fGetRstValLong(RstData.ShiftDefID)
                self.ManagerID = MdlADOFunctions.fGetRstValLong(RstData.ManagerID)
                self.StartTime = RstData.StartTime
                self.IsWorkingShift = MdlADOFunctions.fGetRstValBool(RstData.IsWorkingShift, True)
            RstCursor.close()
        
        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.Init:', str(0), error.args[0], 'ShiftID: ' + str(pShiftID))
        RstCursor = None

    def Create(self, pShiftDefID):
        strSQL = ''
        SourceRst = None
        TargetRst = None
        tNewShiftID = 0
        WDayEng = ''
        WDayLoc = ''
       
        strSQL = 'SELECT * FROM TblShiftDef WHERE ID = ' + pShiftDefID
        SourceRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
        SourceRst.ActiveConnection = None
        if SourceRst.RecordCount == 1:
            strSQL = 'SELECT * FROM TblShift WHERE ID = 0'
            TargetRst.Open(strSQL, CN, adOpenDynamic, adLockOptimistic)
            if TargetRst.RecordCount == 0:
                TargetRst.AddNew()
                TargetRstData.ShiftCalendarID = SourceRstData.ShiftCalendarID
                TargetRstData.ManagerID = MdlADOFunctions.fGetRstValLong(SourceRstData.ManagerUserID)
                TargetRstData.StartTime = NowGMT()
                TargetRstData.wDay = SourceRstData.wDay
                TargetRstData.ShiftName = SourceRstData.ShiftName
                TargetRstData.Department = SourceRstData.Department
                TargetRstData.ShiftDefID = pShiftDefID
                WDayEng = fGetRstValString(GetSingleValue('WDayEng', 'tblWeekDays', 'ID=' + SourceRstData.wDay, 'CN'))
                WDayLoc = fGetRstValString(GetSingleValue('WDayLoc', 'tblWeekDays', 'ID=' + SourceRstData.wDay, 'CN'))
                TargetRstData.WDayEng = WDayEng
                TargetRstData.WDayLoc = WDayLoc
                TargetRstData.ShiftStatus = 1
                TargetRstData.IsWorkingShift = MdlADOFunctions.fGetRstValBool(SourceRstData.IsWorkingShift, True)
                TargetRstData.PermanentWorkersHours = MdlADOFunctions.fGetRstValLong(SourceRstData.PermanentWorkersHours)
                TargetRst.UpNone
                tNewShiftID = MdlADOFunctions.fGetRstValLong(TargetRstData.ID)
                TargetRst.Close()
        SourceRst.Close()
        Me.Init(tNewShiftID)
        if Me.ShiftCalendarID > 0:
            strSQL = 'Update STblShiftCalendar set CurrentShiftID = ' + tNewShiftID + ', CurrentShiftDefID = ' + pShiftDefID + ' Where ID = ' + Me.ShiftCalendarID
            CN.Execute(strSQL)
            
            strSQL = 'Update STblSystemVariables set CurrentShiftID = ' + tNewShiftID + ', CurrentShiftDef = ' + pShiftDefID
            CN.Execute(strSQL)
        else:
            strSQL = 'Update STblSystemVariables set CurrentShiftID = ' + tNewShiftID + ', CurrentShiftDef = ' + pShiftDefID
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
                
            MdlGlobal.RecordError(type(self).__name__ + '.Create:', str(0), error.args[0], 'ShiftDefID: ' + pShiftDefID)
            Err.Clear()
        SourceRst = None
        TargetRst = None

    def CloseShift(self, pNextShiftID):
        strSQL = ''
        RstCursor = None
        
        strSQL = 'SELECT * FROM TblShift WHERE ID = ' + Me.ID
        RstCursor.Open(strSQL, CN, adOpenForwardOnly, adLockPessimistic)
        if RstCursor.RecordCount == 1:
            RstData.EndTime = NowGMT()
            RstData.DurationHr = DateDiff('h', RstData.StartTime, RstData.EndTime)
            RstData.NextShiftID = pNextShiftID
            RstData.ShiftStatus = 2
            RstCursor.UpNone
        RstCursor.Close()
        if Err.Number != 0:
            if InStr(Err.Description, 'nnection') > 0:
                if CN.State == 1:
                    CN.Close()
                CN.Open()
                if MetaCn.State == 1:
                    MetaCn.Close()
                MetaCn.Open()
                Err.Clear()
                
            MdlGlobal.RecordError(type(self).__name__ + '.CloseShift:', str(0), error.args[0], 'ShiftID: ' + Me.ID + '. NextShiftID: ' + pNextShiftID)
            Err.Clear()
        RstCursor = None


    def setIsWorkingShift(self, value):
        self.__mIsWorkingShift = value

    def getIsWorkingShift(self):
        returnVal = None
        returnVal = self.__mIsWorkingShift
        return returnVal
    IsWorkingShift = property(fset=setIsWorkingShift, fget=getIsWorkingShift)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    def setShiftCalendarID(self, value):
        self.__mShiftCalendarID = value

    def getShiftCalendarID(self):
        returnVal = None
        returnVal = self.__mShiftCalendarID
        return returnVal
    ShiftCalendarID = property(fset=setShiftCalendarID, fget=getShiftCalendarID)


    def setManagerID(self, value):
        self.__mManagerID = value

    def getManagerID(self):
        returnVal = None
        returnVal = self.__mManagerID
        return returnVal
    ManagerID = property(fset=setManagerID, fget=getManagerID)


    def setShiftDefID(self, value):
        self.__mShiftDefID = value

    def getShiftDefID(self):
        returnVal = None
        returnVal = self.__mShiftDefID
        return returnVal
    ShiftDefID = property(fset=setShiftDefID, fget=getShiftDefID)


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

