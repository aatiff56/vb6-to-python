import datetime
import MdlConnection

# def fGetRstValLong(rstVal):
#     rstVal = str(rstVal)
    
#     if rstVal == '':
#         raise Exception("Incorrect function.")
#     if rstVal.isnumeric():
#         return int(rstVal)
#     else:
#         return 0

def fGetRstValLong(rstVal):    
    if rstVal == '':
        raise Exception("Incorrect function.")
    try:
        return int(rstVal)
    except:
        return 0


def fGetRstValString(rstVal):
    if rstVal:
        return str(rstVal)
    else:
        return ''


# def fGetRstValDouble(rstVal):
#     returnVal = 0
#     # rstVal = str(rstVal)

#     if rstVal == '':
#         raise Exception("Incorrect function.")

#     if rstVal.isnumeric():
#         returnVal = float(rstVal)
#         if not rstVal.isnumeric():
#             if rstVal == True:
#                 returnVal = 1
#     return returnVal


def fGetRstValDouble(rstVal):
    if rstVal == '':
        raise Exception("Incorrect function.")
    try:
        return float(rstVal)
    except:
        return 0


def fGetRstValBool(rstVal, DefaultVal):
    returnVal = DefaultVal
    rstVal = str(rstVal)

    if rstVal == '':
        raise Exception("Cannot convert empty string to boolean.")
    if rstVal == True:
        returnVal = True
    if rstVal == False:
        returnVal = False
    if rstVal.lower() == 'true' or rstVal == '1' or rstVal == '-1':
        returnVal = True
    if rstVal.lower() == 'false' or rstVal == '0':
        returnVal = False
    return returnVal


def GetSingleValue(FieldName, RecordSource, where, tCon='CN'):
    try:
        dbCursor = None #Rst
        returnVal = None
        strSQL = ""
    
        strSQL = 'Select ' + FieldName + ' as rqstFld From ' + RecordSource + ' Where ' + where
        if tCon == 'CN':
            dbCursor = MdlConnection.CN.cursor()
        else:
            if tCon == 'ERPCN':
                dbCursor = MdlConnection.ERPCN.cursor()
            else:
                dbCursor = MdlConnection.MetaCn.cursor()

        dbCursor.execute(strSQL)
        val = dbCursor.fetchone()
        if val:
            returnVal = val.rqstFld

        if dbCursor:
            dbCursor.close()
        dbCursor = None

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

    return returnVal


def fGetDateTimeFormat(DateTime=datetime.time(12, 0, 0), UseMyDate=False):
    try:
        TS = datetime.date()
        thisYear = 0
        thisMonth = 0
        oldDay = 0
        someHour = 0
        thisMinute = 0
        thisSecond = 0

        if DateTime != datetime.time(12, 0, 0) and UseMyDate == True:
            TS = DateTime
        else:
            TS = datetime.datetime.now()
        thisYear = TS.year
        thisMonth = TS.month
        oldDay = TS.day
        someHour = TS.hour
        thisMinute = TS.minute
        thisSecond = TS.second
        returnVal = 'CONVERT(DATETIME, \'' + thisYear + '-' + thisMonth + '-' + \
            oldDay + ' ' + someHour + ':' + thisMinute + ':' + thisSecond + '\', 102)'
        return returnVal

    except BaseException as error:
        print(error)
        return ''
