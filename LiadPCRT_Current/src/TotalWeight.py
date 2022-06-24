from GlobalVariables import MaterialCalcObjectType

class TotalWeight:

    mControllerField = None
    mJobCurrentValue = 0
    mJoshCurrentValue = 0
    mJobStandardValue = 0
    mJoshStandardValue = 0
    mJobProductRecipeValue = 0
    mJoshProductRecipeValue = 0
    mJobProductStandardValue = 0
    mJoshProductStandardValue = 0
    mJobMaterialActualIndex = 0
    mJoshMaterialActualIndex = 0
    mJobMaterialStandardIndex = 0
    mJoshMaterialStandardIndex = 0
    mJobRecipeRefValue = 0
    mJoshRecipeRefValue = 0
    mParent = None
    mJobOtherMaterialsActualIndex = 0
    mJoshOtherMaterialsActualIndex = 0
    mJobOtherMaterialsAmount = 0
    mJoshOtherMaterialsAmount = 0
    mJobOtherMaterialsAmountStandard = 0
    mJoshOtherMaterialsAmountStandard = 0
    mJobMaterialFlowAmount = 0
    mJoshMaterialFlowAmount = 0

    def SetCurrentValue(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobCurrentValue = value
        else:
            self.mJoshCurrentValue = value

    def SetStandardValue(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobStandardValue = value
        else:
            self.mJoshStandardValue = value

    def SetProductStandardValue(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobProductStandardValue = value
        else:
            self.mJoshProductStandardValue = value

    def SetProductRecipeValue(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobProductRecipeValue = value
        else:
            self.mJoshProductRecipeValue = value

    def SetMaterialActualIndex(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobMaterialActualIndex = value
        else:
            self.mJoshMaterialActualIndex = value

    def SetMaterialStandardIndex(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobMaterialStandardIndex = value
        else:
            self.mJoshMaterialStandardIndex = value

    def SetRecipeRefValue(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobRecipeRefValue = value
        else:
            self.mJoshRecipeRefValue = value

    def SetOtherMaterialsActualIndex(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobOtherMaterialsActualIndex = value
        else:
            self.mJoshOtherMaterialsActualIndex = value

    def SetOtherMaterialsAmount(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobOtherMaterialsAmount = value
        else:
            self.mJoshOtherMaterialsAmount = value

    def SetOtherMaterialsAmountStandard(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobOtherMaterialsAmountStandard = value
        else:
            self.mJoshOtherMaterialsAmountStandard = value

    def SetMaterialFlowAmount(self, pMaterialCalcObjectType, value):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            self.mJobMaterialFlowAmount = value
        else:
            self.mJoshMaterialFlowAmount = value

    def __del__(self):
        
        self.mControllerField = None
        self.mParent = None


    
    def setControllerField(self, value):
        self.mControllerField = value

    def getControllerField(self):
        fn_return_value = self.mControllerField
        return fn_return_value
    ControllerField = property(fset=setControllerField, fget=getControllerField)


    def getMaterialActualIndex(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobMaterialActualIndex
        else:
            fn_return_value = self.mJoshMaterialActualIndex
        return fn_return_value
    MaterialActualIndex = property(fget=getMaterialActualIndex)


    def getMaterialStandardIndex(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobMaterialStandardIndex
        else:
            fn_return_value = self.mJoshMaterialStandardIndex
        return fn_return_value
    MaterialStandardIndex = property(fget=getMaterialStandardIndex)


    def getCurrentValue(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobCurrentValue
        else:
            fn_return_value = self.mJoshCurrentValue
        return fn_return_value
    CurrentValue = property(fget=getCurrentValue)


    def getStandardValue(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobStandardValue
        else:
            fn_return_value = self.mJoshStandardValue
        return fn_return_value
    StandardValue = property(fget=getStandardValue)


    def getProductRecipeValue(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobProductRecipeValue
        else:
            fn_return_value = self.mJoshProductRecipeValue
        return fn_return_value
    ProductRecipeValue = property(fget=getProductRecipeValue)


    def getProductStandardValue(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobProductStandardValue
        else:
            fn_return_value = self.mJoshProductStandardValue
        return fn_return_value
    ProductStandardValue = property(fget=getProductStandardValue)


    def getAmountDiff(self, pMaterialCalcObjectType):
        fn_return_value = round(self.CurrentValue(pMaterialCalcObjectType) - self.StandardValue(pMaterialCalcObjectType), 5)
        return fn_return_value
    AmountDiff = property(fget=getAmountDiff)


    def getAmountDiffPC(self, pMaterialCalcObjectType):
        if self.StandardValue(pMaterialCalcObjectType) > 0:
            fn_return_value = round(self.AmountDiff(pMaterialCalcObjectType) / self.StandardValue(pMaterialCalcObjectType) * 100, 3)
        else:
            fn_return_value = 0
        return fn_return_value
    AmountDiffPC = property(fget=getAmountDiffPC)


    def getAmountStandardPC(self, pMaterialCalcObjectType):
        if self.StandardValue(pMaterialCalcObjectType) > 0:
            fn_return_value = round(self.CurrentValue(pMaterialCalcObjectType) / self.StandardValue(pMaterialCalcObjectType) * 100, 3)
        else:
            fn_return_value = 100
        return fn_return_value
    AmountStandardPC = property(fget=getAmountStandardPC)


    def getAmountProductStandardPC(self, pMaterialCalcObjectType):
        if self.ProductRecipeValue(pMaterialCalcObjectType) > 0:
            fn_return_value = round(( self.CurrentValue(pMaterialCalcObjectType) / self.ProductRecipeValue(pMaterialCalcObjectType) * 100 ), 3)
        else:
            fn_return_value = 100
        return fn_return_value
    AmountProductStandardPC = property(fget=getAmountProductStandardPC)


    def getAmountProductStandardDiff(self, pMaterialCalcObjectType):
        fn_return_value = self.CurrentValue(pMaterialCalcObjectType) - self.ProductRecipeValue(pMaterialCalcObjectType)
        return fn_return_value
    AmountProductStandardDiff = property(fget=getAmountProductStandardDiff)


    def getAmountProductStandardDiffPC(self, pMaterialCalcObjectType):
        if self.ProductRecipeValue(pMaterialCalcObjectType) > 0:
            fn_return_value = round(( self.AmountProductStandardDiff(pMaterialCalcObjectType) / self.ProductRecipeValue(pMaterialCalcObjectType) * 100 ), 3)
        else:
            fn_return_value = 0
        return fn_return_value
    AmountProductStandardDiffPC = property(fget=getAmountProductStandardDiffPC)


    def getAmountStandardStandardPC(self, pMaterialCalcObjectType):
        if self.ProductStandardValue(pMaterialCalcObjectType) > 0:
            fn_return_value = round(( self.CurrentValue(pMaterialCalcObjectType) / self.ProductStandardValue(pMaterialCalcObjectType) * 100 ), 3)
        else:
            fn_return_value = 100
        return fn_return_value
    AmountStandardStandardPC = property(fget=getAmountStandardStandardPC)


    def getAmountStandardStandardDiff(self, pMaterialCalcObjectType):
        fn_return_value = self.CurrentValue(pMaterialCalcObjectType) - self.ProductStandardValue(pMaterialCalcObjectType)
        return fn_return_value
    AmountStandardStandardDiff = property(fget=getAmountStandardStandardDiff)


    def getAmountStandardStandardDiffPC(self, pMaterialCalcObjectType):
        if self.ProductStandardValue(pMaterialCalcObjectType) > 0:
            fn_return_value = round(( self.AmountProductStandardDiff(pMaterialCalcObjectType) / self.ProductStandardValue(pMaterialCalcObjectType) * 100 ), 3)
        else:
            fn_return_value = 0
        return fn_return_value
    AmountStandardStandardDiffPC = property(fget=getAmountStandardStandardDiffPC)

    def setParent(self, value):
        self.mParent = value

    def getParent(self):
        fn_return_value = self.mParent
        return fn_return_value
    Parent = property(fset=setParent, fget=getParent)


    def getRecipeRefValue(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobRecipeRefValue
        else:
            fn_return_value = self.mJoshRecipeRefValue
        return fn_return_value
    RecipeRefValue = property(fget=getRecipeRefValue)


    def getOtherMaterialsActualIndex(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobOtherMaterialsActualIndex
        else:
            fn_return_value = self.mJoshOtherMaterialsActualIndex
        return fn_return_value
    OtherMaterialsActualIndex = property(fget=getOtherMaterialsActualIndex)


    def getOtherMaterialsAmount(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobOtherMaterialsAmount
        else:
            fn_return_value = self.mJoshOtherMaterialsAmount
        return fn_return_value
    OtherMaterialsAmount = property(fget=getOtherMaterialsAmount)


    def getOtherMaterialsAmountStandard(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobOtherMaterialsAmountStandard
        else:
            fn_return_value = self.mJoshOtherMaterialsAmountStandard
        return fn_return_value
    OtherMaterialsAmountStandard = property(fget=getOtherMaterialsAmountStandard)


    def getMaterialFlowAmount(self, pMaterialCalcObjectType):
        if pMaterialCalcObjectType == MaterialCalcObjectType.FromJob:
            fn_return_value = self.mJobMaterialFlowAmount
        else:
            fn_return_value = self.mJoshMaterialFlowAmount
        return fn_return_value
    MaterialFlowAmount = property(fget=getMaterialFlowAmount)
