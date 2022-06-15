
import re

PROCESS_QUERY_INFORMATION = 0x400
class LUID:
    def __init__(self):
        self.LowPart = 0
        self.HighPart = 0

class LUID_AND_ATTRIBUTES:
    def __init__(self):
        self.pLuid = LUID()
        self.Attributes = 0

class TOKEN_PRIVILEGES:
    def __init__(self):
        self.PrivilegeCount = 0
        self.TheLuid = LUID()
        self.Attributes = 0

def ProcessTerminate(lProcessID=None, lHwndWindow=None):
    lhwndProcess = 0
    lExitCode = 0
    lRetVal = 0
    lhThisProc = 0
    lhTokenHandle = 0
    tLuid = LUID()
    tTokenPriv = TOKEN_PRIVILEGES()
    tTokenPrivNew = TOKEN_PRIVILEGES()
    lBufferNeeded = 0
    PROCESS_ALL_ACCESS = 0x1F0FFF
    PROCESS_TERMINATE = 0x1
    ANYSIZE_ARRAY = 1
    TOKEN_ADJUST_PRIVILEGES = 0x20
    TOKEN_QUERY = 0x8
    SE_DEBUG_NAME = 'SeDebugPrivilege'
    SE_PRIVILEGE_ENABLED = 0x2

    if lHwndWindow:
        
        lRetVal = GetWindowThreadProcessId(lHwndWindow, lProcessID)
    if lProcessID:
        
        lhThisProc = GetCurrentProcess
        OpenProcessToken(lhThisProc, TOKEN_ADJUST_PRIVILEGES or TOKEN_QUERY, lhTokenHandle)
        LookupPrivilegeValue('', SE_DEBUG_NAME, tLuid)
        
        tTokenPriv.PrivilegeCount = 1
        tTokenPriv.TheLuid = tLuid
        tTokenPriv.Attributes = SE_PRIVILEGE_ENABLED
        
        AdjustTokenPrivileges(lhTokenHandle, False, tTokenPriv, len(tTokenPrivNew), tTokenPrivNew, lBufferNeeded)
        
        lhwndProcess = OpenProcess(PROCESS_TERMINATE, 0, lProcessID)
        if lhwndProcess:
            
            fn_return_value = CBool(TerminateProcess(lhwndProcess, lExitCode))
            CloseHandle(lhwndProcess)
    
    return fn_return_value

def IsProcessRunning(pid):
    hProcess = 0
    hProcess = OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid)
    CloseHandle(hProcess)
    fn_return_value = hProcess
    return fn_return_value

def GetLeaderMESProcessID():    
    fn_return_value = App.ThreadID
    return fn_return_value

def InIDE():
    s =  " " * 255
    GetModuleFileName(GetModuleHandle(''), s, len(s))
    fn_return_value = re.search('*VB6.EXE*', s.trim().upper())
    return fn_return_value
