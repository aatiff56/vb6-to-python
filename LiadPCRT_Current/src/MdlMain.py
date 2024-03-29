# import sys
from ServerConn import ServerConn
from colorama import Fore

import GlobalVariables
import MdlGlobal
import MdlADOFunctions
import mdl_Common
import registry

gServerConn = None
# LeaderSVR = None # Kept in GlobalVaraibles.py 
strCon = ""
strMetaCon = ""
strSchCN = ['']
InRead = False
ReadCounter = 0
InWrite = False
WriteCounter = 0
ArrAppParams = []

def Main():
    tRes = False 
    strInterval = ''
    tmpInterval = 0
    ResetTime = ''
    SCName = ''
    DBName = ''
    i = 0
    boolRTCommandActivation = False
    ServerStarted = False

    boolRTCommandActivation = False
    if MdlADOFunctions.fGetRstValLong(mdl_Common.QueryValue('emerald','RTCommandActivation')) > 0:
        boolRTCommandActivation = True
    if boolRTCommandActivation:
        ArrAppParams = registry.ArrAppPararms
        # sys.argv
        
    else:
        ArrAppParams = []
        ArrAppParams[0] = ''
        ArrAppParams[1] = ''
        ArrAppParams[2] = ''
        ArrAppParams[3] = ''
        ArrAppParams[4] = ''
        ArrAppParams[5] = '0'
    AllowClose = False
    
    gServerConn = ServerConn()    
    print(Fore.GREEN + 'Starting server.')
    ServerStarted = gServerConn.StartServerConn(ArrAppParams, strSchCN)
    GlobalVariables.LeaderSVR = gServerConn.Server
    strInterval = mdl_Common.QueryValue('Emerald', 'UpdateRate')
    if GlobalVariables.IsNumeric(strInterval):
        tmpInterval = strInterval
        if int(strInterval) < 0:
            tmpInterval = MdlGlobal.cntBaseInterval
        if int(strInterval) > 600000:
            tmpInterval = 600000
    else:
        tmpInterval = MdlGlobal.cntBaseInterval
    ReadTimerInterval = tmpInterval
    # mdl_Common.SetKeyValue('SOFTWARE\\Emerald', 'UpdateRate', str(ReadTimerInterval), REG_SZ)
    LastResetTime =  mdl_Common.NowGMT()
    ResetTime = mdl_Common.QueryValue('Emerald', 'ResetTime')
    if GlobalVariables.IsDate(ResetTime):
        globalResetTime = ResetTime
    else:
        globalResetTime = '05:00'
        # mdl_Common.SetKeyValue('SOFTWARE\\Emerald', 'ResetTime', str(globalResetTime), REG_SZ)
    GlobalVariables.LeaderSVR.GeneralUpdateRateSet[0] = ReadTimerInterval
    fConStrings(strCon, strMetaCon, strSchCN, ArrAppParams)

#     AddIcon
#     if len(ArrAppParams) >= 0:
#         frmMain.Caption = 'LeaderRT: ' + ArrAppParams(0) + ' - Shift Calendar: ' + fGetRstValString(GetSingleValue('LName', 'STblShiftCalendar', 'ID = ' + ArrAppParams(5), 'CN'))
#     else:
#         frmMain.Caption = 'LeaderRT: ' + ArrAppParams(0)
#     if ServerStarted == False:
#         sys.exit(0)
#     frmMain.Visible = True
    

# def Terminate():
#     lhwndProcess = 0

#     PROCESS_ALL_ACCESS = 0x1F0FFF

#     PROCESS_TERMINATE = 0x1
    
#     DeleteIcon
        
#     LeaderSVR = None
#     if not InIDE:
#         lhwndProcess = OpenProcess(PROCESS_TERMINATE, 0, GetCurrentProcessId)
#         if lhwndProcess != 0:
            
#             TerminateProcess(lhwndProcess, 0)
#             CloseHandle(lhwndProcess)

# def Form_Load():
#     str = ""
#     pass
    

# def fGetNewLeaderX():
    
#     fn_return_value = False
#     fn_return_value = True
#     return fn_return_value

def fConStrings(strCon, strMetaCon, strSChCon, Arr):
    try:    
        if not mdl_Common.GetConnectionStrings(strCon, strMetaCon, strSChCon, Arr):
            raise Exception('Cannot get connection strings in fConStrings()')
        
    except BaseException as error:
        pass


Main()