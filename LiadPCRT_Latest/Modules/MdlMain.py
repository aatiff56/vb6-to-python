import sys
from ClassModules import ServerConn as serverConn
import MdlADOFunctions as adoFunctions
import mdl_Common as mdl_Common 
import registry as registry_values

gServerConn = None
# LeaderSVR = Server()
strCon = ""
strMetaCon = ""
strSchCN = ""
InRead = False
ReadCounter = 0
InWrite = False
WriteCounter = 0
ArrAppParams = []

print('started')


def MDIMain():
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
    if adoFunctions.fGetRstValLong(mdl_Common.QueryValue('emerald','RTCommandActivation')) > 0:
        boolRTCommandActivation = True
    if boolRTCommandActivation:
        ArrAppParams = registry_values.ArrAppPararms
        
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
    
    gServerConn = serverConn.ServerConn()
    
#     ServerStarted = gServerConn.StartServerConn(ArrAppParams)
#     LeaderSVR = gServerConn.Server
#     strInterval = QueryValue('SOFTWARE\\Emerald', 'UpdateRate')
#     if strInterval.isnumeric():
#         tmpInterval = strInterval
#         if int(strInterval) < 0:
#             tmpInterval = cntBaseInterval
#         if int(strInterval) > 600000:
#             tmpInterval = 600000
#     else:
#         tmpInterval = cntBaseInterval
#     ReadTimerInterval = tmpInterval
#     SetKeyValue('SOFTWARE\\Emerald', 'UpdateRate', CStr(ReadTimerInterval), REG_SZ)
#     LastResetTime = NowGMT
#     ResetTime = QueryValue('SOFTWARE\\Emerald', 'ResetTime')
#     if IsDate(ResetTime):
#         globalResetTime = ResetTime
#     else:
#         globalResetTime = '05:00'
#         SetKeyValue('SOFTWARE\\Emerald', 'ResetTime', CStr(globalResetTime), REG_SZ)
#     LeaderSVR.GeneralUpdateRateSet[0] = ReadTimerInterval
#     fConStrings(strCon, strMetaCon, strSchCN, ArrAppParams)
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

# def fConStrings(strCon, strMetaCon, strSChCon, Arr):
    
#     if not GetConnectionStrings(strCon, strMetaCon, strSChCon, Arr):
#         Err.Raise(1)
    
    
#     return fn_return_value


MDIMain()