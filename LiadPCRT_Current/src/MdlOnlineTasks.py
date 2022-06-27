from datetime import datetime
from datetime import timedelta
from TaskTrigger import TaskTrigger

import MdlADOFunctions
import MdlGlobal
import mdl_Common
import MdlConnection


def fInitMachineTriggers(pMachine, JobID=0, FromINITMachine=False):
    returnVal = False
    strSQL = ''
    RstCursor = None
    tmpTaskTrigger = None
    ProductGroup = 0
    ProductID = 0
    Counter = 0
    TriggerCount = 0
    MachineGroup = 0
    TriggerFound = False
    QualityGroup = 0
    
    try:
        if JobID == 0:
            TriggerCount = pMachine.mTaskTriggers.Count
            if TriggerCount > 0:
                for Counter in range(1, TriggerCount):
                    pMachine.mTaskTriggers = None
                    pMachine.mTaskTriggers.Remove(( Counter ))
        
        if not FromINITMachine:
            strSQL = 'Delete TblTaskTrigger Where MachineID = ' + str(pMachine.ID) + ' AND ResetOnNewJob <> 0'
            MdlConnection.CN.execute(strSQL)
        
        if JobID > 0:
            ProductID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductID', 'TblJob', 'ID = ' + str(JobID)))
            ProductGroup = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductGroup', 'TblProduct', 'ID = ' + str(ProductID)))
        else:
            if pMachine.ActiveJobID > 0:
                JobID = pMachine.ActiveJobID
                ProductID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductID', 'TblJob', 'ID = ' + str(JobID)))
                ProductGroup = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ProductGroup', 'TblProduct', 'ID = ' + str(ProductID)))
                QualityGroup = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('QualityGroup', 'TblProduct', 'ID = ' + str(ProductID)))
            else:
                ProductGroup = 0
        MachineGroup = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineGroupID', 'TblMachines', 'ID = ' + str(pMachine.ID)))
        
        strSQL = 'Select * '
        strSQL = strSQL + 'From TblTaskTriggerDef '
        strSQL = strSQL + 'Where ('
        strSQL = strSQL + ' MachineID = ' + str(pMachine.ID)
        if MachineGroup > 0:
            strSQL = strSQL + ' OR MachineGroup = ' + str(MachineGroup)
        if ProductID > 0:
            strSQL = strSQL + ' OR ProductID = ' + str(ProductID)
        if ProductGroup > 0:
            strSQL = strSQL + ' OR ProductGroup = ' + str(ProductGroup)
        if QualityGroup > 0:
            strSQL = strSQL + ' OR QualityGroup = ' + str(QualityGroup)
        strSQL = strSQL + ')'

        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstValues = RstCursor.fetchall()

        for RstData in RstValues:
            TriggerFound = False
            for tmpTaskTrigger in pMachine.mTaskTriggers:
                if tmpTaskTrigger.PTriggerDefID == RstData.ID:
                    TriggerFound = True
            if TriggerFound == False:
                tmpTaskTrigger = TaskTrigger()
                if tmpTaskTrigger.Init(RstData.TaskDefID, RstData.ID, pMachine) == True:
                    pMachine.mTaskTriggers.append(tmpTaskTrigger)
        RstCursor.close()
        returnVal = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
            
            if JobID > 0:
                MdlGlobal.RecordError('fInitMachineTriggers', str(0), error.args[0], 'Cant NOT init task trigger on machine ' + str(pMachine.ID) + ' AND Job ' + str(JobID))
            else:
                MdlGlobal.RecordError('fInitMachineTriggers', str(0), error.args[0], 'Can NOT init task trigger on machine ' + str(pMachine.ID))
        
    # if RstCursor:
    #     RstCursor.close()

    RstCursor = None
    return returnVal

def fResetMachineTriggers(pMachine):
    returnVal = False
    tmpTrigger = None
    RemoveIndexArray = []
    tmpIndex = 0
    removeCount = 0
    Counter = 0
    
    try:
        for tmpTrigger in pMachine.mTaskTriggers:
            tmpIndex = tmpIndex + 1
            if tmpTrigger.ResetOnNewJob == True or tmpTrigger.ResetOnNewJob == False:
                removeCount = removeCount + 1
                RemoveIndexArray = [None] * removeCount
                RemoveIndexArray[removeCount - 1] = tmpIndex
        for Counter in range(0, removeCount - 1):
            
            pMachine.mTaskTriggers.Remove(( RemoveIndexArray(Counter) ))
            pMachine.mTaskTriggers = None
            
        returnVal = True
    except:
        pass

    return returnVal


def fCheckMachineTriggers(pMachine):
    returnVal = None
    tmpTrigger = TaskTrigger()
    
    returnVal = False
    for tmpTrigger in pMachine.mTaskTriggers:
        if pMachine.ActiveJobID != 0:
            if ( tmpTrigger.PFireTriggerWhileSetup == True )  or  ( tmpTrigger.PFireTriggerWhileSetup == False and pMachine.NewJob == False and tmpTrigger.PIntervalType != 0 ) :
                if tmpTrigger.CheckInterval == True:
                    tmpTrigger.FireTrigger()
    returnVal = True
    return returnVal

def fGetNextTriggerDate(pSpecificWeekDay, pSpecificTime):
    returnVal = None
    tDate = None
    i = 0

    try:
        for i in range(0, 7):
            tDate = timedelta(days=i) + mdl_Common.NowGMT()

            if Weekday(tDate, vbSunday) == pSpecificWeekDay:
                if TimeGMT >= TimeValue(pSpecificTime):
                    if DateValue(tDate) == DateValue(mdl_Common.NowGMT()):
                        tDate = DateAdd('ww', 1, tDate)
                    tDate = CDate(DateValue(tDate) + ' ' + TimeValue(pSpecificTime))
                    returnVal = tDate
                    break
                else:
                    tDate = CDate(DateValue(tDate) + ' ' + TimeValue(pSpecificTime))
                    returnVal = tDate
                    break
    except BaseException as error:
        pass
    return returnVal


