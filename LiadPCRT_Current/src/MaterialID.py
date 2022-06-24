import MdlADOFunctions

class MaterialID:

    __mControllerField = None
    __mCurrentValue = 0.0
    __mParent = None
    __mMaterialClassID = 0
    __mMPGI = 0.0
    __mIsPConfigSpecialMaterial = False
    __mMaterialType = 0
    __mCalcInMaterialTotal = False
    __mIsRawMaterial = False
    __mIsAdditiveMaterial = False
    __mIsAccompanyingMaterial = False
    __mRefRecipeValue = 0.0
    __mRefRecipeMPGI = 0.0
    __mRefRecipeMaterialClassID = 0
    __mRefRecipeCalcInMaterialTotal = False

    def __del__(self):
        self.__mControllerField = None
        self.__mParent = None


    def setCalcInMaterialTotal(self, value):
        self.__mCalcInMaterialTotal = value

    def getCalcInMaterialTotal(self):
        returnVal = None
        returnVal = self.__mCalcInMaterialTotal
        return returnVal
    CalcInMaterialTotal = property(fset=setCalcInMaterialTotal, fget=getCalcInMaterialTotal)


    
    def setControllerField(self, value):
        self.__mControllerField = value

    def getControllerField(self):
        returnVal = None
        returnVal = self.__mControllerField
        return returnVal
    ControllerField = property(fset=setControllerField, fget=getControllerField)


    def setCurrentValue(self, value):
        if not ( self.ControllerField is None ) :
            
            self.__mCurrentValue = MdlADOFunctions.fGetRstValDouble(value)
        else:
            self.__mCurrentValue = MdlADOFunctions.fGetRstValDouble(value)

    def getCurrentValue(self):
        returnVal = None
        if not ( self.ControllerField is None ) :
            
            returnVal = self.__mCurrentValue
        else:
            returnVal = self.__mCurrentValue
        return returnVal
    CurrentValue = property(fset=setCurrentValue, fget=getCurrentValue)


    def setParent(self, value):
        self.__mParent = value

    def getParent(self):
        returnVal = None
        returnVal = self.__mParent
        return returnVal
    Parent = property(fset=setParent, fget=getParent)


    def setMaterialClassID(self, value):
        self.__mMaterialClassID = value

    def getMaterialClassID(self):
        returnVal = None
        returnVal = self.__mMaterialClassID
        return returnVal
    MaterialClassID = property(fset=setMaterialClassID, fget=getMaterialClassID)


    def setIsPConfigSpecialMaterial(self, value):
        self.__mIsPConfigSpecialMaterial = value

    def getIsPConfigSpecialMaterial(self):
        returnVal = None
        returnVal = self.__mIsPConfigSpecialMaterial
        return returnVal
    IsPConfigSpecialMaterial = property(fset=setIsPConfigSpecialMaterial, fget=getIsPConfigSpecialMaterial)


    def setMaterialType(self, value):
        self.__mMaterialType = value

    def getMaterialType(self):
        returnVal = None
        returnVal = self.__mMaterialType
        return returnVal
    MaterialType = property(fset=setMaterialType, fget=getMaterialType)


    def setMPGI(self, value):
        self.__mMPGI = value

    def getMPGI(self):
        returnVal = None
        returnVal = self.__mMPGI
        return returnVal
    MPGI = property(fset=setMPGI, fget=getMPGI)


    def setIsRawMaterial(self, value):
        self.__mIsRawMaterial = value

    def getIsRawMaterial(self):
        returnVal = None
        returnVal = self.__mIsRawMaterial
        return returnVal
    IsRawMaterial = property(fset=setIsRawMaterial, fget=getIsRawMaterial)


    def setIsAdditiveMaterial(self, value):
        self.__mIsAdditiveMaterial = value

    def getIsAdditiveMaterial(self):
        returnVal = None
        returnVal = self.__mIsAdditiveMaterial
        return returnVal
    IsAdditiveMaterial = property(fset=setIsAdditiveMaterial, fget=getIsAdditiveMaterial)


    def setIsAccompanyingMaterial(self, value):
        self.__mIsAccompanyingMaterial = value

    def getIsAccompanyingMaterial(self):
        returnVal = None
        returnVal = self.__mIsAccompanyingMaterial
        return returnVal
    IsAccompanyingMaterial = property(fset=setIsAccompanyingMaterial, fget=getIsAccompanyingMaterial)


    def setRefRecipeMPGI(self, value):
        self.__mRefRecipeMPGI = value

    def getRefRecipeMPGI(self):
        returnVal = None
        returnVal = self.__mRefRecipeMPGI
        return returnVal
    RefRecipeMPGI = property(fset=setRefRecipeMPGI, fget=getRefRecipeMPGI)


    def setRefRecipeValue(self, value):
        self.__mRefRecipeValue = MdlADOFunctions.fGetRstValDouble(value)

    def getRefRecipeValue(self):
        returnVal = None
        returnVal = self.__mRefRecipeValue
        return returnVal
    RefRecipeValue = property(fset=setRefRecipeValue, fget=getRefRecipeValue)


    def setRefRecipeCalcInMaterialTotal(self, value):
        self.__mRefRecipeCalcInMaterialTotal = value

    def getRefRecipeCalcInMaterialTotal(self):
        returnVal = None
        returnVal = self.__mRefRecipeCalcInMaterialTotal
        return returnVal
    RefRecipeCalcInMaterialTotal = property(fset=setRefRecipeCalcInMaterialTotal, fget=getRefRecipeCalcInMaterialTotal)


    def setRefRecipeMaterialClassID(self, value):
        self.__mRefRecipeMaterialClassID = value

    def getRefRecipeMaterialClassID(self):
        returnVal = None
        returnVal = self.__mRefRecipeMaterialClassID
        return returnVal
    RefRecipeMaterialClassID = property(fset=setRefRecipeMaterialClassID, fget=getRefRecipeMaterialClassID)

    
