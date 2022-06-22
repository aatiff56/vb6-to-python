import enum
import MdlADOFunctions
import MdlConnection
import MdlGlobal

class PConfigSonsRefRecipeSourceOption(enum.Enum):
    FromPConfigParent = 0
    FromProductRecipe = 1

class MachineType:
    
    __mID = 0
    __mPConfigSonsRefRecipeSource = PConfigSonsRefRecipeSourceOption
    __mReportInventoryItemAsSetUpReject = False
    __mActivePalletCreationBy = 0
    __mMinEventDuration = 0
    __mMinEventReasonID = 0
    __mSetupEndCyclesSource = 0

    def Init(self, pMachineTypeID):
        strSQL = ''
        RstCursor = None
        
        try:
            strSQL = 'SELECT * FROM STblMachineTypes WHERE ID = ' + pMachineTypeID
            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.arraysize == 1:
                self.ID = pMachineTypeID
                select_0 = MdlADOFunctions.fGetRstValLong(RstData.PConfigSonsRefRecipeSource)
                if (select_0 == 0):
                    self.PConfigSonsRefRecipeSource = PConfigSonsRefRecipeSourceOption.FromPConfigParent
                elif (select_0 == 1):
                    self.PConfigSonsRefRecipeSource = PConfigSonsRefRecipeSourceOption.FromProductRecipe
                else:
                    self.PConfigSonsRefRecipeSource = PConfigSonsRefRecipeSourceOption.FromPConfigParent

                self.ReportInventoryItemAsSetUpReject = MdlADOFunctions.fGetRstValBool(RstData.ReportInventoryItemAsSetUpReject, False)
                self.ActivePalletCreationBy = MdlADOFunctions.fGetRstValLong(RstData.ActivePalletCreationBy)
                self.MinEventDuration = MdlADOFunctions.fGetRstValLong(RstData.MinEventDuration)
                self.MinEventReasonID = MdlADOFunctions.fGetRstValLong(RstData.MinEventReasonID)
                self.SetupEndCyclesSource = MdlADOFunctions.fGetRstValLong(RstData.SetupEndCyclesSource)
                if self.SetupEndCyclesSource == 0:
                    self.SetupEndCyclesSource = 1
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                    
            MdlGlobal.RecordError(type(self) + '.Init:', str(0), error.args[0], 'MachineTypeID:' + str(pMachineTypeID))
        RstCursor = None


    def setSetupEndCyclesSource(self, value):
        self.__mSetupEndCyclesSource = value

    def getSetupEndCyclesSource(self):
        returnVal = None
        returnVal = self.__mSetupEndCyclesSource
        return returnVal
    SetupEndCyclesSource = property(fset=setSetupEndCyclesSource, fget=getSetupEndCyclesSource)


    def setMinEventDuration(self, value):
        self.__mMinEventDuration = value

    def getMinEventDuration(self):
        returnVal = None
        returnVal = self.__mMinEventDuration
        return returnVal
    MinEventDuration = property(fset=setMinEventDuration, fget=getMinEventDuration)


    def setMinEventReasonID(self, value):
        self.__mMinEventReasonID = value

    def getMinEventReasonID(self):
        returnVal = None
        returnVal = self.__mMinEventReasonID
        return returnVal
    MinEventReasonID = property(fset=setMinEventReasonID, fget=getMinEventReasonID)


    def setActivePalletCreationBy(self, value):
        self.__mActivePalletCreationBy = value

    def getActivePalletCreationBy(self):
        returnVal = None
        returnVal = self.__mActivePalletCreationBy
        return returnVal
    ActivePalletCreationBy = property(fset=setActivePalletCreationBy, fget=getActivePalletCreationBy)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    def setPConfigSonsRefRecipeSource(self, value):
        self.__mPConfigSonsRefRecipeSource = value

    def getPConfigSonsRefRecipeSource(self):
        returnVal = None
        returnVal = self.__mPConfigSonsRefRecipeSource
        return returnVal
    PConfigSonsRefRecipeSource = property(fset=setPConfigSonsRefRecipeSource, fget=getPConfigSonsRefRecipeSource)


    def setReportInventoryItemAsSetUpReject(self, value):
        self.__mReportInventoryItemAsSetUpReject = value

    def getReportInventoryItemAsSetUpReject(self):
        returnVal = None
        returnVal = self.__mReportInventoryItemAsSetUpReject
        return returnVal
    ReportInventoryItemAsSetUpReject = property(fset=setReportInventoryItemAsSetUpReject, fget=getReportInventoryItemAsSetUpReject)
