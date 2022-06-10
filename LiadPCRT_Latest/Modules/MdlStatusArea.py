
class NOTIFYICONDATA:
    def __init__(self):
        self.cbSize = 0
        self.hwnd = 0
        self.uId = 0
        self.uFlags = 0
        self.uCallBackMessage = 0
        self.hIcon = 0
        self.szTip = ''

    NIM_ADD = 0x0
    NIM_MODIFY = 0x1
    NIM_DELETE = 0x2
    WM_MOUSEMOVE = 0x200
    NIF_MESSAGE = 0x1
    NIF_ICON = 0x2
    NIF_TIP = 0x4
    WM_LBUTTONDBLCLK = 0x203
    WM_LBUTTONDOWN = 0x201
    WM_LBUTTONUP = 0x202
    WM_RBUTTONDBLCLK = 0x206
    WM_RBUTTONDOWN = 0x204
    WM_RBUTTONUP = 0x205
    nid = NOTIFYICONDATA()

def AddIcon():
    nid.cbSize = len(nid)
    nid.hwnd = frmMain.hwnd
    nid.uId = vbNull
    nid.uFlags = NIF_ICON or NIF_TIP or NIF_MESSAGE
    nid.uCallBackMessage = WM_MOUSEMOVE
    nid.hIcon = frmMain.Icon
    nid.szTip = 'LeaderMES RealTime: ' + CN.Properties.Item(27).value + '\r\n' + 'Shift Calendar ID:' + LeaderSVR.SCID + vbNullChar
            
    Shell_NotifyIcon(NIM_ADD, nid)

def DeleteIcon():        
    Shell_NotifyIcon(NIM_DELETE, nid)



