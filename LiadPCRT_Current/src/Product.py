import MdlADOFunctions
import MdlGlobal
import MdlConnection
import MdlServer

class Product:
    __mID = 0
    __mMachineType = None
    __mCatalogID = ''
    __mActivePalletCreationModeID = 0

    def Init(self, pProductID):
        strSQL = ''
        RstCursor = None
        
        try:
            strSQL = 'SELECT ID,MachineType,CatalogID,ActivePalletCreationModeID FROM TblProduct WHERE ID = ' + str(pProductID)

            RstCursor = MdlConnection.CN.cursor()
            RstCursor.execute(strSQL)
            RstData = RstCursor.fetchone()

            if RstCursor.arraysize == 1:
                self.ID = pProductID
                self.MachineType = MdlServer.GetOrCreateMachineType(MdlMain.LeaderSVR, MdlADOFunctions.fGetRstValLong(RstData.MachineType))
                self.CatalogID = MdlADOFunctions.fGetRstValString(RstData.CatalogID)
                self.ActivePalletCreationModeID = MdlADOFunctions.fGetRstValLong(RstData.ActivePalletCreationModeID)
            RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                    
                MdlGlobal.RecordError(type(self) + '.Init:', str(0), error.args[0], 'ProductID:' + str(pProductID))
        RstCursor = None


    def setActivePalletCreationModeID(self, value):
        self.__mActivePalletCreationModeID = value

    def getActivePalletCreationModeID(self):
        returnVal = None
        returnVal = self.__mActivePalletCreationModeID
        return returnVal
    ActivePalletCreationModeID = property(fset=setActivePalletCreationModeID, fget=getActivePalletCreationModeID)


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


    def setCatalogID(self, value):
        self.__mCatalogID = value

    def getCatalogID(self):
        returnVal = None
        returnVal = self.__mCatalogID
        return returnVal
    CatalogID = property(fset=setCatalogID, fget=getCatalogID)

