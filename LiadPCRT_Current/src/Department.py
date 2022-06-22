from lib2to3.pytree import Base
import MdlADOFunctions
import MdlConnection
import MdlGlobal

class Department:
    __mID = 0
    __mShiftCalendarID = 0
    __mCycleTimeEffFactor = 0.0
    __mMachineTimeEffFactor = 0.0
    __mRejectsEffFactor = 0.0
    __mCavitiesEffFactor = 0.0
    __mMachines = {}
    __mMaterialRelativePortion = 0.0
    __mEquipmentRelativePortion = 0.0

    
    def Init(self, pServer, pDepartmentID):
        strSQL = ''

        try:
            strSQL = 'SELECT * FROM STblDepartments Where ID = ' + str(pDepartmentID)
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()
            
            if RstCursor.arraysize == 1:
                self.ID = pDepartmentID
                self.ShiftCalendarID = MdlADOFunctions.fGetRstValLong(RstData.ShiftCalendarID)
                if RstData.CavitiesEffFactor is None:
                    self.CavitiesEffFactor = pServer.SystemVariables.CavitiesEffFactor
                else:
                    self.CavitiesEffFactor = MdlADOFunctions.fGetRstValDouble(RstData.CavitiesEffFactor)
                if RstData.CycleTimeEffFactor is None:
                    self.CycleTimeEffFactor = pServer.SystemVariables.CycleTimeEffFactor
                else:
                    self.CycleTimeEffFactor = MdlADOFunctions.fGetRstValDouble(RstData.CycleTimeEffFactor)
                if RstData.MachineTimeEffFactor is None:
                    self.MachineTimeEffFactor = pServer.SystemVariables.MachineTimeEffFactor
                else:
                    self.MachineTimeEffFactor = MdlADOFunctions.fGetRstValDouble(RstData.MachineTimeEffFactor)
                if RstData.RejectsEffFactor is None:
                    self.RejectsEffFactor = pServer.SystemVariables.RejectsEffFactor
                else:
                    self.RejectsEffFactor = MdlADOFunctions.fGetRstValDouble(RstData.RejectsEffFactor)
                self.MaterialRelativePortion = MdlADOFunctions.fGetRstValDouble(RstData.MaterialRelativePortion)
                if self.MaterialRelativePortion == 0:
                    self.MaterialRelativePortion = 1
                self.EquipmentRelativePortion = MdlADOFunctions.fGetRstValDouble(RstData.EquipmentRelativePortion)
                if self.EquipmentRelativePortion == 0:
                    self.EquipmentRelativePortion = 1
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                    
                MdlGlobal.RecordError(type(self) + '.Init:', str(0), error.args[0], 'DepartmentID:' + str(pDepartmentID))
        RstCursor = None

    
    def AddMachine(self, pMachine):
        try:
            self.Machines.Add(pMachine, str(pMachine.ID))
        
        except BaseException as error:
            MdlGlobal.RecordError(type(self) + '.AddMachine:', str(0), error.args[0], 'DepartmentID:' + str(self.ID) + '. MachineID: ' + str(pMachine.ID))


    def __del__(self):
        Counter = 0
        for Counter in range(1, self.__mMachines.Count):
            self.__mMachines.Remove(Counter)
        self.__mMachines = None


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


    def setCycleTimeEffFactor(self, value):
        self.__mCycleTimeEffFactor = value

    def getCycleTimeEffFactor(self):
        returnVal = None
        returnVal = self.__mCycleTimeEffFactor
        return returnVal
    CycleTimeEffFactor = property(fset=setCycleTimeEffFactor, fget=getCycleTimeEffFactor)


    def setMachineTimeEffFactor(self, value):
        self.__mMachineTimeEffFactor = value

    def getMachineTimeEffFactor(self):
        returnVal = None
        returnVal = self.__mMachineTimeEffFactor
        return returnVal
    MachineTimeEffFactor = property(fset=setMachineTimeEffFactor, fget=getMachineTimeEffFactor)


    def setRejectsEffFactor(self, value):
        self.__mRejectsEffFactor = value

    def getRejectsEffFactor(self):
        returnVal = None
        returnVal = self.__mRejectsEffFactor
        return returnVal
    RejectsEffFactor = property(fset=setRejectsEffFactor, fget=getRejectsEffFactor)


    def setCavitiesEffFactor(self, value):
        self.__mCavitiesEffFactor = value

    def getCavitiesEffFactor(self):
        returnVal = None
        returnVal = self.__mCavitiesEffFactor
        return returnVal
    CavitiesEffFactor = property(fset=setCavitiesEffFactor, fget=getCavitiesEffFactor)


    def setMachines(self, value):
        self.__mMachines = value

    def getMachines(self):
        returnVal = None
        returnVal = self.__mMachines
        return returnVal
    Machines = property(fset=setMachines, fget=getMachines)


    def setMaterialRelativePortion(self, value):
        self.__mMaterialRelativePortion = value

    def getMaterialRelativePortion(self):
        returnVal = None
        returnVal = self.__mMaterialRelativePortion
        return returnVal
    MaterialRelativePortion = property(fset=setMaterialRelativePortion, fget=getMaterialRelativePortion)


    def setEquipmentRelativePortion(self, value):
        self.__mEquipmentRelativePortion = value

    def getEquipmentRelativePortion(self):
        returnVal = None
        returnVal = self.__mEquipmentRelativePortion
        return returnVal
    EquipmentRelativePortion = property(fset=setEquipmentRelativePortion, fget=getEquipmentRelativePortion)
