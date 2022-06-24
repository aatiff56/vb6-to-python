class ForecastWeight:

    __mJobAmount = 0.0
    __mJobAmountLeft = 0.0
    __mParent = None

    def __del__(self):
        self.__mParent = None


    def setParent(self, value):
        self.__mParent = value

    def getParent(self):
        returnVal = None
        returnVal = self.__mParent
        return returnVal
    Parent = property(fset=setParent, fget=getParent)


    def setJobAmount(self, value):
        self.__mJobAmount = value

    def getJobAmount(self):
        returnVal = None
        returnVal = self.__mJobAmount
        return returnVal
    JobAmount = property(fset=setJobAmount, fget=getJobAmount)


    def setJobAmountLeft(self, value):
        self.__mJobAmountLeft = value

    def getJobAmountLeft(self):
        returnVal = None
        returnVal = self.__mJobAmountLeft
        return returnVal
    JobAmountLeft = property(fset=setJobAmountLeft, fget=getJobAmountLeft)
