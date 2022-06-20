from math import sqrt
import MdlADOFunctions

class SPCSample:
    def __init__(self):
        self.value = 0.0
        self.XChecked = 0
        self.Sigma = 0.0
        self.STDEV = 0.0
        self.SMean = 0.0
        self.UCL = 0.0
        self.LCL = 0.0
        self.Mean = 0.0
        self.PUCL = 0.0
        self.PLCL = 0.0
        self.QUCL = 0.0
        self.QLCL = 0.0
        self.MeanDiff = 0.0
        self.MeanDiffSTDev = 0.0
        self.XMeanAbove = 0
        self.XMeanbelow = 0
        self.X1SAbove = 0
        self.X1SBelow = 0
        self.X2SAbove = 0
        self.X2SBelow = 0
        self.XUCLAbove = 0
        self.XLCLBelow = 0
        self.XOrderAsc = 0
        self.XOrderDesc = 0
        self.CP = 0.0
        self.CPK = 0.0

__cntMinStatGroup = 25

def fSTDev(ArrVals, ValsCount):
    returnVal = None
    dSumSqr = 0.0
    dSum = 0.0
    Counter = 0
    N = 0.0
    
    if ValsCount < 2:
        raise Exception('Values must be greater than 1.')

    for Counter in range(1, ValsCount):
        dSumSqr = ( ArrVals(Counter) ** 2 )  + dSumSqr
        dSum = dSum + ArrVals(Counter)
    N = ValsCount
    returnVal = sqrt(float(( ( N * dSumSqr )  -  ( dSum ** 2 ) )  /  ( N *  ( N - 1 ) )))
    return returnVal


def __fAVG(ArrVals, ValsCount):
    returnVal = None
    Counter = 0
    mSum = 0.0
    
    for Counter in range(1, ValsCount):
        mSum = mSum + ArrVals(Counter)
    returnVal = mSum / ValsCount
    return returnVal


def __fSMean(ArrVals, ValsCount, UCL, LCL):
    returnVal = None
    mSTDEV = 0.0
    tUCL = 0.0
    tLCL = 0.0
    Avg = 0.0
    temp = 0.0
    mSum = 0.0
    Counter = 0
    ValidsCount = 0
    Valids = []

    try:
        if ValsCount < 2:
            raise Exception('Values must be greater than 1.')

        mSTDEV = fSTDev(ArrVals, ValsCount)
        Avg = __fAVG(ArrVals, ValsCount)
        if mSTDEV > 0:
            tUCL = Avg +  ( 3 * mSTDEV )
            tLCL = Avg -  ( 3 * mSTDEV )
        else:
            tUCL = UCL
            tLCL = LCL

        for Counter in range(1, ValsCount):
            temp = ArrVals(Counter)
            if temp <= tUCL and temp >= tLCL:
                ValidsCount = ValidsCount + 1
                Valids = vbObjectInitialize((ValidsCount,), Variant, Valids)
                Valids[ValidsCount] = temp

        if ValidsCount > 2:
            mSTDEV = fSTDev(Valids, ValidsCount)
            returnVal = __fAVG(Valids, ValidsCount)
            if mSTDEV > 0:
                tUCL = __fSMean() +  ( 3 * mSTDEV )
                tLCL = __fSMean() -  ( 3 * mSTDEV )
            else:
                tUCL = UCL
                tLCL = LCL
        UCL = tUCL
        LCL = tLCL
    except:
        pass

    return returnVal



def __fCheckGroupStat(ArrVals, ValsCount, tSample):
    returnVal = None
    XMeanAbove = 0
    XMeanbelow = 0
    X1SAbove = 0
    X1SBelow = 0
    X2SAbove = 0
    X2SBelow = 0
    XUCLAbove = 0
    XLCLBelow = 0
    XOrderAsc = 0
    XOrderDesc = 0
    Counter = 0
    XOrderAsc = 0
    XOrderDesc = 0
    temp = ''

    for Counter in range(1, ValsCount):
        temp = ArrVals(Counter)
        
        if temp >= tSample.Mean:
            XMeanAbove = XMeanAbove + 1
        
        if temp <= tSample.Mean:
            XMeanbelow = XMeanbelow + 1
        
        if temp >= tSample.Mean + tSample.Sigma:
            X1SAbove = X1SAbove + 1
        
        if temp <= tSample.Mean - tSample.Sigma:
            X1SBelow = X1SBelow + 1
        
        if temp >= tSample.Mean +  ( 2 * tSample.Sigma ) :
            X2SAbove = X2SAbove + 1
        
        if temp <= tSample.Mean -  ( 2 * tSample.Sigma ) :
            X2SBelow = X2SBelow + 1
        
        if temp >= tSample.UCL:
            XUCLAbove = XUCLAbove + 1
        
        if temp <= tSample.LCL:
            XLCLBelow = XLCLBelow + 1
        if Counter > 1:
            if temp > temp == ArrVals(Counter - 1):
                XOrderAsc = XOrderAsc + 1
            if temp < temp == ArrVals(Counter - 1):
                XOrderDesc = XOrderDesc + 1
    tSample.XMeanAbove = XMeanAbove
    tSample.XMeanbelow = XMeanbelow
    tSample.X1SAbove = X1SAbove
    tSample.X1SBelow = X1SBelow
    tSample.X2SAbove = X2SAbove
    tSample.X2SBelow = X2SBelow
    tSample.XUCLAbove = XUCLAbove
    tSample.XLCLBelow = XLCLBelow    
    tSample.XOrderAsc = XOrderAsc    
    tSample.XOrderDesc = XOrderDesc
    
    return returnVal

def fMin(ArrVals, ValsCount):
    returnVal = None
    dMin = 0.0
    Counter = 0
    N = 0
    
    returnVal = ArrVals(1)
    if ValsCount < 2:
        raise Exception('Values must be greater than 1.')

    for Counter in range(1, ValsCount):
        if ArrVals(Counter) < fMin():
            returnVal = ArrVals(Counter)
    return returnVal

def fMinVal(Val1, val2):
    returnVal = None
    returnVal = Val1

    if val2 < fMinVal():
        returnVal = val2
    return returnVal

def fMax(ArrVals, ValsCount):
    returnVal = None
    dMax = 0.0
    Counter = 0
    N = 0

    returnVal = ArrVals(1)
    if ValsCount < 2:
        raise Exception('Values must be greater than 1.')
    for Counter in range(1, ValsCount):
        if ArrVals(Counter) > fMax():
           returnVal = ArrVals(Counter)
    return returnVal

def fSum(ArrVals, ValsCount):
    returnVal = None
    dSum = 0.0
    Counter = 0
    N = 0
   
    returnVal = ArrVals(1)
    if ValsCount < 2 or Counter in range(1, ValsCount):
        returnVal = fSum() + ArrVals(Counter)
        raise Exception('Values must be greater than 1.')

    return returnVal


def fRoundNum(pNumber, pNumOfDigits=0, pRoundOption=0):
    returnVal = None
    temp = pNumber

    if (pRoundOption == 0):
        temp = round(temp, pNumOfDigits)

    elif (pRoundOption == 1):
        if '.' in temp:
            temp = temp.split('.')[0]
            temp = MdlADOFunctions.fGetRstValDouble(temp) + 1

    elif (pRoundOption == 2):
        if '.' in temp:
            temp = temp.split('.')[0]
    returnVal = MdlADOFunctions.fGetRstValDouble(temp)
    return returnVal
