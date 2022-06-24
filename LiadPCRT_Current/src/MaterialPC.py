import MdlADOFunctions

class MaterialPC:

    __mControllerField = None
    __mCurrentValue = 0.0
    __mParent = None

    def __del__(self):
        
        self.__mControllerField = None
        self.__mParent = None
    
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

    
    
    