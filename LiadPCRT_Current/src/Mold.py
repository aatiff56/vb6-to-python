import MdlADOFunctions
import MdlConnection
import MdlGlobal

class Mold:
    __mID = 0
    __mMachineType = None
    __mCavities = 0.0
    __mCavitiesCurrent = 0.0
    __mInjectionsCount = 0.0
    __mInjectionsForMaintenance = 0.0
    __mInjectionsMaintained = 0.0
    __mInjectionsForNextMaintenance = 0.0
    __mInjectionsCountForMaintenance = 0.0
    __mInjectionsForecastTotal = 0.0
    __mInjectionsUsagePC = 0.0
    __mAngus = 0.0

    def Init(self, pMoldID):
        strSQL = ''
        RstCursor = None

        try:
            strSQL = 'SELECT * FROM TblMolds Where ID = ' + str(pMoldID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.arraysize == 1:
                self.ID = pMoldID
                self.Cavities = MdlADOFunctions.fGetRstValDouble(RstData.Cavities)
                self.CavitiesCurrent = MdlADOFunctions.fGetRstValDouble(RstData.CavitiesCurrent)
                self.InjectionsCount = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCount)
                self.InjectionsCountForMaintenance = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsForMaintenance)
                self.InjectionsForNextMaintenance = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsForNextMaintenance)
                self.InjectionsMaintained = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsMaintained)
                self.InjectionsForecastTotal = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsForecastTotal)
                self.InjectionsUsagePC = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsUsagePC)
                self.Angus = MdlADOFunctions.fGetRstValDouble(RstData.Angus)
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                    
                MdlGlobal.RecordError(type(self).__name__ + '.Init:', str(0), error.args[0], 'MoldID:' + str(pMoldID))

            RstCursor = None


    def Refresh(self):
        strSQL = ''
        RstCursor = None
        try:
            strSQL = 'SELECT CavitiesCurrent FROM TblMolds WHERE ID = ' + str(self.ID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.arraysize == 1:
                self.CavitiesCurrent = MdlADOFunctions.fGetRstValDouble(RstData.CavitiesCurrent)
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
        RstCursor = None
        strSQL = ''


    def CalcInjections(self, pInjectionsDiff, pMachineID=0):
        strSQL = ''
        tInjectionsForNextMaintenance = 0.0
        InjectionsUsagePC = 0.0
        InjectionsCount = 0.0
        InjectionsForNextMaintenance = 0.0
        RstCursor = None

        try:
            tInjectionsForNextMaintenance = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('InjectionsForNextMaintenance', 'TblMolds', 'ID = ' + str(self.ID), 'CN'))
            self.InjectionsForNextMaintenance = tInjectionsForNextMaintenance
            self.InjectionsCount = self.InjectionsCount + pInjectionsDiff
            self.InjectionsForNextMaintenance = self.InjectionsForNextMaintenance - pInjectionsDiff
            if self.InjectionsForecastTotal != 0:
                self.InjectionsUsagePC = self.InjectionsCount / self.InjectionsForecastTotal * 100
            strSQL = 'UPDATE TblMolds SET InjectionsCount = ' + str(self.InjectionsCount) + ', InjectionsForNextMaintenance = ' + str(self.InjectionsForNextMaintenance)
            strSQL = strSQL + ' , InjectionsUsagePC = ' + str(self.InjectionsUsagePC) + ' WHERE ID = ' + str(self.ID)

            MdlConnection.CN.execute(strSQL)
            if pMachineID > 0:
                
                strSQL = 'Select InjectionsCount, InjectionsForNextMaintenance,InjectionsForecastTotal, InjectionsUsagePC From TblMachines Where ID=' + str(pMachineID)
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstData:
                    InjectionsCount = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsCount) + pInjectionsDiff
                    InjectionsForNextMaintenance = MdlADOFunctions.fGetRstValDouble(RstData.InjectionsForNextMaintenance) - pInjectionsDiff
                    if MdlADOFunctions.fGetRstValDouble(RstData.InjectionsForecastTotal) > 0:
                        InjectionsUsagePC = round(InjectionsCount / MdlADOFunctions.fGetRstValDouble(RstData.InjectionsForecastTotal) * 100, 3)
                RstCursor.close()

                strSQL = 'Update TblMachines Set InjectionsCount=' + str(InjectionsCount) + ', InjectionsForNextMaintenance = ' + str(InjectionsForNextMaintenance)
                strSQL = strSQL + ', InjectionsUsagePC = ' + str(InjectionsUsagePC)
                strSQL = strSQL + ' Where ID=' + str(pMachineID)
                MdlConnection.CN.execute(strSQL)

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                    
                MdlGlobal.RecordError(type(self) + '.CalcInjections:', str(0), error.args[0], 'MoldID:' + str(self.ID))

    def __del__(self):
        self.__mMachineType = None


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)
    

    def setMachineType(self, value):
        self.__mMachineType = value

    def getMachineType(self):
        returnVal = None
        returnVal = self.__mMachineType
        return returnVal
    MachineType = property(fset=setMachineType, fget=getMachineType)


    def setCavities(self, value):
        self.__mCavities = value

    def getCavities(self):
        returnVal = None
        returnVal = self.__mCavities
        return returnVal
    Cavities = property(fset=setCavities, fget=getCavities)


    def setCavitiesCurrent(self, value):
        self.__mCavitiesCurrent = value

    def getCavitiesCurrent(self):
        returnVal = None
        returnVal = self.__mCavitiesCurrent
        return returnVal
    CavitiesCurrent = property(fset=setCavitiesCurrent, fget=getCavitiesCurrent)


    def setInjectionsCount(self, value):
        self.__mInjectionsCount = value

    def getInjectionsCount(self):
        returnVal = None
        returnVal = self.__mInjectionsCount
        return returnVal
    InjectionsCount = property(fset=setInjectionsCount, fget=getInjectionsCount)


    def setInjectionsCountForMaintenance(self, value):
        self.__mInjectionsCountForMaintenance = value

    def getInjectionsCountForMaintenance(self):
        returnVal = None
        returnVal = self.__mInjectionsCountForMaintenance
        return returnVal
    InjectionsCountForMaintenance = property(fset=setInjectionsCountForMaintenance, fget=getInjectionsCountForMaintenance)


    def setInjectionsMaintained(self, value):
        self.__mInjectionsMaintained = value

    def getInjectionsMaintained(self):
        returnVal = None
        returnVal = self.__mInjectionsMaintained
        return returnVal
    InjectionsMaintained = property(fset=setInjectionsMaintained, fget=getInjectionsMaintained)


    def setInjectionsForNextMaintenance(self, value):
        self.__mInjectionsForNextMaintenance = value

    def getInjectionsForNextMaintenance(self):
        returnVal = None
        returnVal = self.__mInjectionsForNextMaintenance
        return returnVal
    InjectionsForNextMaintenance = property(fset=setInjectionsForNextMaintenance, fget=getInjectionsForNextMaintenance)


    def setInjectionsForecastTotal(self, value):
        self.__mInjectionsForecastTotal = value

    def getInjectionsForecastTotal(self):
        returnVal = None
        returnVal = self.__mInjectionsForecastTotal
        return returnVal
    InjectionsForecastTotal = property(fset=setInjectionsForecastTotal, fget=getInjectionsForecastTotal)


    def setInjectionsUsagePC(self, value):
        self.__mInjectionsUsagePC = value

    def getInjectionsUsagePC(self):
        returnVal = None
        returnVal = self.__mInjectionsUsagePC
        return returnVal
    InjectionsUsagePC = property(fset=setInjectionsUsagePC, fget=getInjectionsUsagePC)


    def setAngus(self, value):
        self.__mAngus = value

    def getAngus(self):
        returnVal = None
        returnVal = self.__mAngus
        return returnVal
    Angus = property(fset=setAngus, fget=getAngus)

