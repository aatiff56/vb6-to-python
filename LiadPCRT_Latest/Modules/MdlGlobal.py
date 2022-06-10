import enum
import MdlConnection
from datetime import datetime

class OPCDATASOURCE(enum.Enum):
    OPC_DS_CACHE = 1
    OPC_DS_DEVICE = 2

AllowClose = False
strConn = ""
lngShiftCounter = 0
lngWriteCounter = 0
lngReadCounter = 0
lngShiftLeap = 0
lngWriteLeap = 0
lngReadLeap = 0
cntBaseInterval = 2000
ReadTimerInterval = 0
globalResetTime = None
LastResetTime = None
gServer = None
cntErrorCountAlarm = 3
AlarmOnProgressInterval = 0
cntMinStatGroup = 25
strEncoding = ""
strXMLHeader = ""
GeneralGroupRefreshRate = None


def RecordError(FName, ErrNum, ErrDescr, Descr, AppName='LeaderRT'):
    try:
        strSQL = ""
        dbCursor = None #Rst
        RID = 0

        if 'nnection' in ErrDescr:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

        errDesc = FName + '; Err: ' + ErrNum + ' - ' + ErrDescr + '; ' + Descr
        strSQL = 'Insert Into STblErrors (AppName, ErrorDescr, ErrorTime) Values (' + AppName + ', ' + errDesc + ', ' + datetime.now() + ")"
        dbCursor.execute(strSQL)
        RID = dbCursor.fetchone()[0]        
        if RID > 10000:
            strSQL = 'Delete STblErrors Where ID < ' +  ( RID - 10000 )
            dbCursor.Execute(strSQL)

    except BaseException as error:
        pass

    if dbCursor:
        dbCursor.close()
    dbCursor = None
