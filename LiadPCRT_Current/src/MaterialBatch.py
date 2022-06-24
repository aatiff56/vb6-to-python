import MdlADOFunctions
import MdlConnection
import MdlGlobal

class MaterialBatch:

    __mCurrentValue = ''
    __mEffectiveAmount = 0.0
    __mAmount = 0.0
    __mParent = None
    __mID = 0
    __mOriginalEffectiveAmount = 0.0
    __mWeight = 0.0
    __mGrossWeight = 0.0
    __mParentInventoryID = 0

    def __del__(self):
        
        self.__mParent = None

    def Refresh(self):
        strSQL = ''
        RstCursor = None

        try:
            if self.ID != 0:
                strSQL = 'SELECT Batch,EffectiveAmount,EffectiveOriginalAmount,Weight,GrossWeight,ParentInventoryID FROM TblInventory WHERE ID = ' + str(self.ID)
                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchone()

                if RstData:
                    self.EffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveAmount)
                    self.OriginalEffectiveAmount = MdlADOFunctions.fGetRstValDouble(RstData.EffectiveOriginalAmount)
                    self.CurrentValue = MdlADOFunctions.fGetRstValString(RstData.Batch)
                    self.Weight = MdlADOFunctions.fGetRstValDouble(RstData.Weight)
                    
                    self.GrossWeight = MdlADOFunctions.fGetRstValDouble(RstData.GrossWeight)
                    self.ParentInventoryID = MdlADOFunctions.fGetRstValLong(RstData.ParentInventoryID)
                RstCursor.close()

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)
                
            MdlGlobal.RecordError(type(self).__name__ + '.Refresh:', str(0), error.args[0], 'InventoryID:' + str(self.ID))
        RstCursor = None


    def setCurrentValue(self, value):
        self.__mCurrentValue = value

    def getCurrentValue(self):
        returnVal = None
        returnVal = self.__mCurrentValue
        return returnVal
    CurrentValue = property(fset=setCurrentValue, fget=getCurrentValue)


    def setEffectiveAmount(self, value):
        self.__mEffectiveAmount = value

    def getEffectiveAmount(self):
        returnVal = None
        returnVal = self.__mEffectiveAmount
        return returnVal
    EffectiveAmount = property(fset=setEffectiveAmount, fget=getEffectiveAmount)


    def setAmount(self, value):
        self.__mAmount = value

    def getAmount(self):
        returnVal = None
        returnVal = self.__mAmount
        return returnVal
    Amount = property(fset=setAmount, fget=getAmount)


    def setParent(self, value):
        self.__mParent = value

    def getParent(self):
        returnVal = None
        returnVal = self.__mParent
        return returnVal
    Parent = property(fset=setParent, fget=getParent)


    def setID(self, value):
        self.__mID = value

    def getID(self):
        returnVal = None
        returnVal = self.__mID
        return returnVal
    ID = property(fset=setID, fget=getID)


    def setOriginalEffectiveAmount(self, value):
        self.__mOriginalEffectiveAmount = value

    def getOriginalEffectiveAmount(self):
        returnVal = None
        returnVal = self.__mOriginalEffectiveAmount
        return returnVal
    OriginalEffectiveAmount = property(fset=setOriginalEffectiveAmount, fget=getOriginalEffectiveAmount)


    def setWeight(self, value):
        self.__mWeight = value

    def getWeight(self):
        returnVal = None
        returnVal = self.__mWeight
        return returnVal
    Weight = property(fset=setWeight, fget=getWeight)


    def setGrossWeight(self, value):
        self.__mGrossWeight = value

    def getGrossWeight(self):
        returnVal = None
        returnVal = self.__mGrossWeight
        return returnVal
    GrossWeight = property(fset=setGrossWeight, fget=getGrossWeight)


    def setParentInventoryID(self, value):
        self.__mParentInventoryID = value

    def getParentInventoryID(self):
        returnVal = None
        returnVal = self.__mParentInventoryID
        return returnVal
    ParentInventoryID = property(fset=setParentInventoryID, fget=getParentInventoryID)
