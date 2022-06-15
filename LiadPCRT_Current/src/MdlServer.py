import os

def fCheckForDuplicateRealTimes(pServer):
    try:    
        if pServer.ShiftCalendar.WindowsProcessID != 0:
            os.kill(pServer.ShiftCalendar.WindowsProcessID, 0)

    except BaseException as error:
        return False
    else:
        return True