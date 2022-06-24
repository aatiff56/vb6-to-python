import MdlADOFunctions

class MaterialPCTarget:

    __mControllerField = None
    __mCurrentValue = 0.0
    __mParent = None
    __mProductRecipeValue = 0.0
    __mProductStandardValue = 0.0
    __mRecipeRefValue = 0.0

    def __del__(self):
        self.__mControllerField = None
        self.__mParent = None


    def setProductRecipeValue(self, value):
        self.__mProductRecipeValue = value

    def getProductRecipeValue(self):
        returnVal = None
        returnVal = self.__mProductRecipeValue
        return returnVal
    ProductRecipeValue = property(fset=setProductRecipeValue, fget=getProductRecipeValue)


    def setProductStandardValue(self, value):
        self.__mProductStandardValue = value

    def getProductStandardValue(self):
        returnVal = None
        returnVal = self.__mProductStandardValue
        return returnVal
    ProductStandardValue = property(fset=setProductStandardValue, fget=getProductStandardValue)


    
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


    def setRecipeRefValue(self, value):
        self.__mRecipeRefValue = value

    def getRecipeRefValue(self):
        returnVal = None
        returnVal = self.__mRecipeRefValue
        return returnVal
    RecipeRefValue = property(fset=setRecipeRefValue, fget=getRecipeRefValue)

    
    
    