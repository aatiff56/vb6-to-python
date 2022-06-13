# from datetime import datetime
# import winreg
# import MdlGlobal
# import MdlConnection
# import MdlADOFunctions
import registry as registry_values

# # strSChCon = ""
# # SQLDateOrder = 0
# # ExternalCn = None
# # SchCn = None
# # cntObjectType = '1'

# class SYSTEMTIME:
#     def __init__(self):
#         self.wYear = 0
#         self.wMonth = 0
#         self.wDayOfWeek = 0
#         self.wDay = 0
#         self.wHour = 0
#         self.wMinute = 0
#         self.wSecond = 0
#         self.wMilliseconds = 0

# class TIME_ZONE_INFORMATION:
#     def __init__(self):
#         self.Bias = 0
#         self.StandardName = 0
#         self.StandardDate = SYSTEMTIME()
#         self.StandardBias = 0
#         self.DaylightName = 0
#         self.DaylightDate = SYSTEMTIME()
#         self.DaylightBias = 0

# __TIME_ZONE_ID_INVALID = 0xFFFFFFFF
# __TIME_ZONE_ID_STANDARD = 1
# __TIME_ZONE_ID_UNKNOWN = 0
# __TIME_ZONE_ID_DAYLIGHT = 2
# __mServerGMT = 0
# GMTAdd = 0
# HKEY_LOCAL_MACHINE = 0x80000002
# HKEY_CURRENT_USER = 0x80000001
# REG_OPTION_NON_VOLATILE = 0
# KEY_ALL_ACCESS = 0x3F
# KEY_SET_VALUE = 0x2
# KEY_QUERY_VALUE = 0x1
# REG_DWORD = 4
# ERROR_NONE = 0
# ERROR_BADDB = 1
# ERROR_BADKEY = 2
# ERROR_CANTOPEN = 3
# ERROR_CANTREAD = 4
# ERROR_CANTWRITE = 5
# ERROR_OUTOFMEMORY = 6
# ERROR_ARENA_TRASHED = 7
# ERROR_ACCESS_DENIED = 8
# ERROR_INVALID_PARAMETERS = 87
# ERROR_NO_MORE_ITEMS = 259
# QCBooleanTrue = '1'
# MaxLabUsers = 75
# CnstConnectionTimeOut = 600
# strUserLoginUrl = 'QuallaEng.ASP?WCI=UserLogin&WCU=a'
# CntDefaultDisplayWidth = 800
# CntDefaultDisplayHeight = 600
# CntDefaultReportColWidth = 75

# QCDate = 1
# QCTime = 2
# QCInt = 3
# QCNum = 4
# QCString = 5
# QCBoolean = 6

# AddNew = 0
# SaveUpdate = 1
# Delete = 2

# class TReportTest:
#     def __init__(self):
#         self.ID = 0
#         self.TableName = ""
#         self.TestFields = 0
#         self.FieldsCount = 0
#         self.strSelect = ""
#         self.CheckStat = False
#         self.SievesTable = ""
#         self.SievesCount = 0

# class TReportTestField:
#     def __init__(self):
#         self.FName = ""
#         self.FType = QCType()
#         self.DisplayName = ""
#         self.StatField = False
#         self.StatFieldTableName = ""
#         self.ShowTested = False
#         self.ShowPassed = False
#         self.ShowMax = False
#         self.ShowMin = False
#         self.ShowAVG = False
#         self.ShowSTDEV = False
#         self.ColWidth = 0

# class Sieve:
#     def __init__(self):
#         self.SID = 0
#         self.InchName = ""
#         self.CMName = ""

# class TReportField:
#     def __init__(self):
#         self.FName = ""
#         self.TableName = ""
#         self.DisplayName = ""
#         self.Type = QCType()
#         self.ColWidth = 0
#         self.DigitsNumber = 0
#         self.Link = ""
#         self.LinkAddValue = False
#         self.LinkValueField = ""
#         self.LinkTarget = ""

# class JobButton:
#     def __init__(self):
#         self.ID = 0
#         self.Name = ""
#         self.value = ""
#         self.Class = ""
#         self.Enabled = False
#         self.ActionID = ""


# def strRemovePar(strSource, AddASCII, HtmlText):
#     Counter = 0
#     strNew = ""
#     temp = ""
    
#     try:
#         for Counter in range(1, len(strSource)):
#             temp = strSource[Counter: 1]
#             if HtmlText == True:
#                 if temp == chr(34):
#                     strNew = strNew + '&quot;'
#                 else:
#                     strNew = strNew + temp
#             else:
#                 if (temp == chr(34)):
#                     if AddASCII == True:
#                         strNew = strNew + chr(34) + ' & chr(34) & ' + chr(34)
#                 elif (temp == '\''):
#                     if AddASCII == True:
#                         strNew = strNew + chr(34) + ' & chr(39) & ' + chr(34)
#                 elif (temp == chr(12)):
#                     if AddASCII == True:
#                         strNew = strNew + chr(34) + ' & chr(12) & ' + chr(34)
#                 elif (temp == chr(13)):
#                     if AddASCII == True:
#                         strNew = strNew + chr(34) + ' & chr(12) & chr(13) & ' + chr(34)
#                     Counter = Counter + 1
#                 elif (temp == "\n"):
#                     if AddASCII == True:
#                         strNew = strNew + chr(34) + ' & chr(12) & chr(13) & ' + chr(34)
#                 else:
#                     strNew = strNew + temp
#         return strNew

#     except BaseException as error:
#         return ''

# def strRemoveBadChars(strSource):
#     temp = ""

#     try:        
#         temp = strSource.replace(chr(34), '')
#         temp = temp.replace('\'', '')
#         temp = temp.replace(',', '')
#         temp = temp.replace('%', '')
#         temp = temp.replace('')
#         temp = temp.replace('^', '')
#         temp = temp.replace('`', '')
#         return temp

#     except BaseException as error:
#         return ''


# def AddPar(value, RemovePar=False, HtmlText=False):
#     returnVal = None
    
#     if RemovePar == False:
#         returnVal = chr(34) + value + chr(34)
#     else:
#         if value.find(chr(39)) > 0 or value.find(chr(34)) > 0 or value.find(chr(12)) > 0 or value.find(chr(13)) > 0:
#             returnVal = chr(34) + strRemovePar(str('' + value), True, HtmlText) + chr(34)
#         else:
#             returnVal = chr(34) + value + chr(34)
#     return returnVal


# def CreateNewKey(sNewKeyName, lPredefinedKey):
#     keyCreated = False
#     try:
#         key = winreg.OpenKeyEx(lPredefinedKey, r"SOFTWARE\\Wow6432Node\\")
#         newKey = winreg.CreateKey(key, sNewKeyName)
#         if newKey:
#             winreg.CloseKey(newKey)
#         keyCreated = True

#     except BaseException as error:
#         print(error)
#     return keyCreated


# def SetKeyValue(sKeyName, sValueName, vValueSetting, lValueType):
#     valueSet = False
#     try:
#         key = winreg.OpenKeyEx(HKEY_LOCAL_MACHINE, sKeyName)
#         winreg.SetValueEx(key, sValueName, 0, lValueType, str(vValueSetting))
#         if key:
#             winreg.CloseKey(key)
#             valueSet = True
#     except BaseException as error:
#         print(error)

#     return valueSet


def QueryValue(key_category, key_name):
    
    if(key_category == 'emerald'):
        return registry_values.Emerald[key_name]
    elif(key_category == 'one'):
        return registry_values.one[key_name]
    elif(key_category == 'erp'):
        return registry_values.ERP[key_name]
 
    # hKey = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, sKeyName)
    # value = winreg.QueryValueEx(hKey, sValueName)
    # if hKey:
    #     winreg.CloseKey(hKey)
    # return value[0]



# def SetValueEx(hKey, sValueName, lType, vValue):
#     LValue: int
#     try:
#         sValue = ""
#         select_variable_0 = lType
#         if (select_variable_0 == MdlConnection.REG_SZ):
#             sValue = vValue + chr(0)
#             return winreg.SetValueEx(hKey, sValueName, 0, lType, sValue, len(sValue))
#         elif (select_variable_0 == REG_DWORD):
#             LValue = vValue
#             return winreg.SetValueEx(hKey, sValueName, 0, lType, LValue, 4)

#     except BaseException as error:
#         print(error)
#         return None



# # def QueryValueEx(lhKey, szValueName, vValue):
# #     returnVal = None
# #     cch = 0
# #     lrc = 0
# #     lType = 0
# #     LValue = 0
# #     sValue = ""
    
# #     lrc = RegQueryValueExNULL(lhKey, szValueName, 0, lType, 0, cch)
# #     if lrc != ERROR_NONE:
# #         Error(5)

# #     if (lType == MdlConnection.REG_SZ):
# #         sValue = String(cch, 0)
# #         lrc = RegQueryValueExString(lhKey, szValueName, 0, lType, sValue, cch)
# #         if lrc == ERROR_NONE:
# #             vValue = Left(sValue, cch - 1)
# #         else:
# #             vValue = Empty
        
# #     elif (lType == REG_DWORD):
# #         lrc = RegQueryValueExLong(lhKey, szValueName, 0, lType, LValue, cch)
# #         if lrc == ERROR_NONE:
# #             vValue = LValue
# #     else:
        
# #         lrc = - 1
# #     returnVal = lrc
# #     return returnVal
    
# #     return returnVal


# def GetRegValuesToConnection(strMCn, ArrParams, FromWeb=False):
#     returnVal = None
#     strRes = ""
#     res = ""
#     NameOfKey = ""
#     AppID = 0
#     CommandActivation = False
#     returnVal = ''
#     NameOfKey = 'SOFTWARE\\Emerald\\1'

#     try:
#         if not CreateNewKey(NameOfKey, HKEY_LOCAL_MACHINE):
#             raise Exception("Couldn't create key '" + NameOfKey + "'.")
#         res = QueryValue(NameOfKey, 'Provider')
#         if res == '':
#             SetRegValues(NameOfKey)
#         if res == '':
#             res = QueryValue(NameOfKey, 'Provider')
#         strRes = 'Provider=' + res.strip() + ';'
#         res = QueryValue(NameOfKey, 'Persist Security Info')
#         strRes = strRes + 'Persist Security Info=' + res.strip() + ';'
#         res = QueryValue('SOFTWARE\\Emerald', 'RTCommandActivation')
#         if res == '' or res == '0' or FromWeb == True:
#             CommandActivation = False
#         else:
#             CommandActivation = True

#         if CommandActivation:
#             if len(ArrParams) >= 0:
#                 res = ArrParams(2)
#             else:
#                 res = ''
#             if res == '':
#                 res = QueryValue(NameOfKey, 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             if len(ArrParams) >= 0:
#                 res = ArrParams(3)
#             else:
#                 res = ''
#             if res == '':
#                 res = QueryValue(NameOfKey, 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             if len(ArrParams) >= 0:
#                 res = ArrParams(4)
#             else:
#                 res = ''
#             if res == '':
#                 res = QueryValue(NameOfKey, 'Password')
#                 strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#             else:
#                 strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#             if len(ArrParams) >= 0:
#                 res = ArrParams(0)
#             else:
#                 res = ''
#             if res == '':
#                 res = QueryValue(NameOfKey, 'DataCatalog')
#             strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
#         else:
#             res = QueryValue(NameOfKey, 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Password')
#             strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#             res = QueryValue(NameOfKey, 'DataCatalog')
#             strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
#         res = QueryValue(NameOfKey, 'Data Provider')
#         strRes = strRes + 'Data Provider=' + res.strip()
#         returnVal = strRes

#     except BaseException as error:
#         MdlGlobal.RecordError('GetRegValuesToConnection', 0, error.args[0], strRes)
        
#     return returnVal


# def GetRegValuesToSchConnection(strMCn):
#     returnVal = None
#     strRes = ""
#     res = ""
#     NameOfKey = ""
#     AppID = 0
#     returnVal = ''
#     NameOfKey = 'SOFTWARE\\Emerald\\1'

#     try:
#         if not CreateNewKey(NameOfKey, HKEY_LOCAL_MACHINE):
#             raise Exception("Couldn't create key '" + NameOfKey + "'.")
#         res = QueryValue(NameOfKey, 'Provider')
#         if res == '':
#             SetRegValues(NameOfKey)
#         if res == '':
#             res = QueryValue(NameOfKey, 'Provider')
#         strRes = 'Provider=' + res.strip() + ';'
#         res = QueryValue(NameOfKey, 'Persist Security Info')
#         strRes = strRes + 'Persist Security Info=' + res.strip() + ';'
#         res = QueryValue(NameOfKey, 'Data Source')
#         strRes = strRes + 'Data Source=' + res.strip() + ';'
#         res = QueryValue(NameOfKey, 'User ID')
#         strRes = strRes + 'User ID=' + res.strip() + ';'
#         res = QueryValue(NameOfKey, 'Password')
#         strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#         res = QueryValue(NameOfKey, 'SchDataCatalog')
#         strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
#         res = QueryValue(NameOfKey, 'Data Provider')
#         strRes = strRes + 'Data Provider=' + res.strip()
#         returnVal = strRes

#     except BaseException as error:
#         MdlGlobal.RecordError('GetRegValuesToSchConnection', 0, error.args[0], strRes)
    
#     return returnVal


# def GetRegValuesToERPConnection(strMCn):
#     returnVal = None
#     strRes = ""
#     res = ""
#     ERPType = ""
#     NameOfKey = ""
#     AppID = 0
#     returnVal = ''
#     NameOfKey = 'SOFTWARE\\Emerald\\1\\ERP'

#     try:
#         if not CreateNewKey(NameOfKey, HKEY_LOCAL_MACHINE):
#             raise Exception("Couldn't create key '" + NameOfKey + "'.")
#         res = QueryValue(NameOfKey, 'ERPType')
#         ERPType = res
#         if (ERPType == '2'):
#             res = QueryValue(NameOfKey, 'DataCatalog')
#             if res != '':
#                 strRes = strRes + 'DSN=' + res
#         elif (ERPType == '4'):
#             res = QueryValue(NameOfKey, 'Provider')
#             if res == '':
#                 SetRegValues(NameOfKey)
#             if res == '':
#                 res = QueryValue(NameOfKey, 'Provider')
#             strRes = 'Provider=' + res.strip() + ';'
            
#             res = QueryValue(NameOfKey, 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Password')
#             strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#             res = QueryValue(NameOfKey, 'DataCatalog')
            
#         elif (ERPType == '5'):
#             res = QueryValue(NameOfKey, 'Provider')
#             if res == '':
#                 SetRegValues(NameOfKey)
#             if res == '':
#                 res = QueryValue(NameOfKey, 'Provider')
#             strRes = 'Provider=' + res.strip() + ';'
            
#             res = QueryValue(NameOfKey, 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Password')
#             strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
            
#         elif (ERPType == '9'):
#             res = QueryValue(NameOfKey, 'Provider')
#             if res == '':
#                 SetRegValues(NameOfKey)
#             if res == '':
#                 res = QueryValue(NameOfKey, 'Provider')
#             strRes = 'Provider=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Password')
#             strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
            
#         elif (ERPType == '10'):
#             res = QueryValue(NameOfKey, 'Provider')
#             if res == '':
#                 SetRegValues(NameOfKey)
#             if res == '':
#                 res = QueryValue(NameOfKey, 'Provider')
#             strRes = 'Provider=' + res.strip() + ';'
            
#             res = QueryValue(NameOfKey, 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Force Translate')
#             strRes = strRes + 'Force Translate=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Password')
#             strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
            
#         else:
#             res = QueryValue(NameOfKey, 'Provider')
#             if res == '':
#                 SetRegValues(NameOfKey)
#             if res == '':
#                 res = QueryValue(NameOfKey, 'Provider')
#             strRes = 'Provider=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Persist Security Info')
#             strRes = strRes + 'Persist Security Info=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Password')
#             strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#             res = QueryValue(NameOfKey, 'DataCatalog')
#             strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
#             res = QueryValue(NameOfKey, 'Data Provider')
#             strRes = strRes + 'Data Provider=' + res.strip()
#         returnVal = strRes

#     except BaseException as error:
#         MdlGlobal.RecordError('GetRegValuesToERPConnection', 0, error.args[0], strRes)        
    
#     return returnVal


# def GetRegValuesToMetaConnection(Arr, FromWeb=False):
#     returnVal = None
#     strRes = ""
#     res = ""
#     CommandActivation = False
#     returnVal = ''

#     try:
#         res = QueryValue('SOFTWARE\\Emerald', 'Provider')
#         if res == '':
#             MdlConnection.SetRegMetaValues()
#         res = QueryValue('SOFTWARE\\Emerald', 'Provider')
#         strRes = 'Provider=' + res.strip() + ';'
#         res = QueryValue('SOFTWARE\\Emerald', 'Persist Security Info')
#         strRes = strRes + 'Persist Security Info=' + res.strip() + ';'
#         res = QueryValue('SOFTWARE\\Emerald', 'RTCommandActivation')
#         if res == '' or res == '0' or FromWeb == True:
#             CommandActivation = False
#         else:
#             CommandActivation = True
#         if CommandActivation:
#             if len(Arr) >= 0:
#                 res = Arr(2)
#             else:
#                 res = ''
#             if res == '':
#                 res = QueryValue('SOFTWARE\\Emerald', 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             if len(Arr) >= 0:
#                 res = Arr(3)
#             else:
#                 res = ''
#             if res == '':
#                 res = QueryValue('SOFTWARE\\Emerald', 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             if len(Arr) >= 0:
#                 res = Arr(4)
#             else:
#                 res = ''
#             if res == '':
#                 res = QueryValue('SOFTWARE\\Emerald', 'Password')
#                 strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#             else:
#                 strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#             if len(Arr) >= 0:
#                 res = Arr(1)
#             else:
#                 res = ''
#             if res == '':
#                 res = QueryValue('SOFTWARE\\Emerald', 'MetaCatalog')
#                 strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
#             else:
#                 strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
#         else:
#             res = QueryValue('SOFTWARE\\Emerald', 'Data Source')
#             strRes = strRes + 'Data Source=' + res.strip() + ';'
#             res = QueryValue('SOFTWARE\\Emerald', 'User ID')
#             strRes = strRes + 'User ID=' + res.strip() + ';'
#             res = QueryValue('SOFTWARE\\Emerald', 'Password')
#             strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
#             res = QueryValue('SOFTWARE\\Emerald', 'MetaCatalog')
#             strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
#         res = QueryValue('SOFTWARE\\Emerald', 'Data Provider')
#         strRes = strRes + 'Data Provider=' + res.strip()
#         returnVal = strRes

#     except BaseException as error:
#         MdlGlobal.RecordError('GetRegValuesToMetaConnection', 0, error.args[0], strRes)
        
#     return returnVal


# def EightToTen(Source):
#     returnVal = None
#     i = 0
#     figure = 0
#     res = 0

#     if int(Source) == 0:
#         returnVal = 0
#     else:
#         for i in range(0, len(Source) - 1):
#             figure = Source.find(len(Source) - i, 1)
#             res = res + figure * 8 ** i
#         returnVal = res
#     return returnVal


# def GetConnectionStrings(strCn, strMetaCn, strSChCon, ArrParams, strERPCon=VBMissingArgument, FromWeb=False):
#     res = ""
#     returnVal = False

#     try:
#         res = QueryValue('SOFTWARE\\Emerald\\1', 'SQLDateOrder')
#         if res == '':
#             SQLDateOrder = 1
#         else:
#             SQLDateOrder = MdlADOFunctions.fGetRstValLong(res)
#         res = QueryValue('SOFTWARE\\Emerald', 'UserTimeOut')
#         if res == '':
#             res = MdlConnection.SetUserTimeOut()
#         UserTimeOut = int(res)
#         strMetaCn = GetRegValuesToMetaConnection(ArrParams(), FromWeb)
#         strCn = GetRegValuesToConnection(strMetaCn, ArrParams(), FromWeb)
#         strSChCon = GetRegValuesToSchConnection(strMetaCn)
#         strERPCon = GetRegValuesToERPConnection(strMetaCn)
#         returnVal = True
    
#     except BaseException as error:
#         MdlGlobal.RecordError('GetConnectionStrings', 0, error.args[0], res)
        
#     return returnVal


# def GetTimeDifference():
#     returnVal = None
#     tz = TIME_ZONE_INFORMATION()
#     retcode = 0
#     Difference = 0
#     retcode = GetTimeZoneInformation(tz)
#     Difference = - tz.Bias * 60
#     returnVal = Difference
    
#     if retcode == __TIME_ZONE_ID_DAYLIGHT:
#         if tz.DaylightDate.wMonth != 0:
#             returnVal = Difference - tz.DaylightBias * 60
#     return returnVal


# def NowGMT():
#     returnVal = None
    
#     try:
#         if GMTAdd == 0:
#             returnVal = datetime.now()
#         else:
#             returnVal = DateAdd('n', ( GMTAdd ), datetime.now())

#     except BaseException as error:
#         returnVal = datetime.now()

#     return returnVal


# def TimeGMT():
#     returnVal = None
    
#     try:
#         if GMTAdd == 0:
#             returnVal = datetime.time()
#         else:
#             returnVal = TimeValue(NowGMT())

#     except BaseException as error:
#         returnVal = datetime.time()

#     return returnVal


# def DateGMT():
#     returnVal = None
    
#     try:
#         if GMTAdd == 0:
#             returnVal = datetime.date()
#         else:
#             returnVal = DateValue(NowGMT())

#     except BaseException as error:
#         returnVal = datetime.date()

#     return returnVal


# def SetRegVal(Rst, NameKey):
#     if not SetKeyValue(NameKey, 'Program', 'ColorSaveMS', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'DataCatalog', Rst.Fields("InitialCatalog").Value, MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Provider', Rst.Fields("Provider").Value, MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Persist Security Info', Rst.Fields("PersistSecurityInfo").Value, MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Data Source', Rst.Fields("DataSource").Value, MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'User ID', Rst.Fields("UserID").Value, MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Password', MdlConnection.PasswordCipher(Rst.Fields("Password").Value), MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Data Provider', Rst.Fields("DataProvider").Value, MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")


# def SetRegValues(NameKey):
    
#     if not SetKeyValue(NameKey, 'Program', 'ColorSaveMS', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'DataCatalog', 'LiadData', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'SchDataCatalog', 'PlanMate_Scheduling', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Provider', 'MSDataShape.1', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Persist Security Info', 'True', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Data Source', '127.0.0.1', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'User ID', 'SA', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Password', MdlConnection.PasswordCipher('hobit'), MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Data Provider', 'SQLOLEDB.1', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")


# def SetRegValuesERP(NameKey):
    
#     if not SetKeyValue(NameKey, 'Program', 'LeaderMES', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'DataCatalog', 'SAP', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Provider', 'MSDataShape.1', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Persist Security Info', 'True', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Data Source', '127.0.0.1', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'User ID', 'SA', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Password', MdlConnection.PasswordCipher(''), MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")
#     if not SetKeyValue(NameKey, 'Data Provider', 'SQLOLEDB.1', MdlConnection.REG_SZ):
#         raise Exception("Incorrect function.")


# def SetDBParam(UI, PW, DC, DS):

#     returnVal = False
#     if UI != '':
#         if not SetKeyValue('SOFTWARE\\Emerald\\1', 'User ID', UI, MdlConnection.REG_SZ):
#             raise Exception("Incorrect function.")
#     if PW != '':
#         if not SetKeyValue('SOFTWARE\\Emerald\\1', 'Password', PW, MdlConnection.REG_SZ):
#             raise Exception("Incorrect function.")
#     if DC != '':
#         if not SetKeyValue('SOFTWARE\\Emerald\\1', 'DataCatalog', DC, MdlConnection.REG_SZ):
#             raise Exception("Incorrect function.")
#     if DS != '':
#         if not SetKeyValue('SOFTWARE\\Emerald\\1', 'Data Source', DS, MdlConnection.REG_SZ):
#             raise Exception("Incorrect function.")
#     returnVal = True
#     return returnVal


# def __IsEmptyOrNull(pVariant):
#     returnVal = None
#     returnVal = True
#     if pVariant:
#         if str('' + pVariant.strip()) != '':
#             returnVal = False
#     return returnVal


# def __GetColumnDetails(pTableName, pColumnName, pDetail):
    
#     returnVal = ''
#     if not __IsEmptyOrNull(pTableName) and not __IsEmptyOrNull(pColumnName) and not __IsEmptyOrNull(pDetail):
#         returnVal = MdlADOFunctions.fGetRstValString(MdlADOFunctions.GetSingleValue(pDetail, 'INFORMATION_SCHEMA.COLUMNS', '(TABLE_NAME = \'' + pTableName + '\') AND (COLUMN_NAME = \'' + pColumnName + '\')'))
#     else:
#         returnVal = ''
#         return returnVal
#     return returnVal


# def InArray(pArr, pSearchTerm):
#     Current = None    
#     returnVal = False

#     try:
#         for Current in pArr:
#             if not __IsEmptyOrNull(Current):
#                 if Current == pSearchTerm:
#                     returnVal = True
#                     return returnVal

#     except BaseException as error:
#         pass
#     return returnVal


# def __RoundNum(pNumber, pNumOfDigits=0, pRoundOption=0):
#     returnVal = None
#     temp = ""
#     temp = pNumber

#     if (pRoundOption == 0):
#         temp = round(temp, pNumOfDigits)
#     elif (pRoundOption == 1):
#         if temp.find('.') > 0:
#             temp = temp.split('.')[0]
#             temp = MdlADOFunctions.fGetRstValDouble(temp) + 1
#     elif (pRoundOption == 2):
#         if temp.find('.') > 0:
#             temp = temp.split('.')[0]

#     returnVal = MdlADOFunctions.fGetRstValDouble(temp)
#     return returnVal


# def AddErrorToErrorString(ErrorString, ErrorText):
#     returnVal = '' + ErrorString

#     try:
#         if ErrorString == '':
#             ErrorString = ErrorText
#         else:
#             ErrorString = ErrorString + "\n" + ErrorText
#         returnVal = '' + ErrorString

#     except BaseException as error:
#         pass

#     return returnVal


# def GMTCalc():
#     returnVal = None
#     MultiTimeZoneLeaderServer = False
#     TargetDaylightSavingOn = False
#     ThisDBGMT = 0

#     try:
#         MultiTimeZoneLeaderServer = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('MultiTimeZoneLeaderServer', 'STblSystemVariables', 'ID > 0', 'CN'), False)
#         TargetDaylightSavingOn = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('ThisDBDaylightSavingOn', 'STblSystemVariables', 'ID > 0', 'CN'), False)
#         ThisDBGMT = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('ThisDBGMT', 'STblSystemVariables', 'ID > 0', 'CN'))
#         if MultiTimeZoneLeaderServer and ThisDBGMT > - 720.1 and ThisDBGMT < 720.1:
#             if TargetDaylightSavingOn:
#                 GMTAdd = ThisDBGMT + 60
#             else:
#                 GMTAdd = ThisDBGMT
#             GMTAdd = GMTAdd -  ( GetTimeDifference() / 60 )
#         else:
#             GMTAdd = 0
#         returnVal = GMTAdd

#     except BaseException as error:
#         pass

#     return returnVal


# def strFixBadChars(strSource):
#     returnVal = None
#     temp = ""
    
#     try:
#         temp = strSource.replace(chr(34), chr(34) + chr(34))
#         temp = temp.replace('\'', '\'\'')
#         temp = temp.replace(chr(13), '')
#         temp = temp.replace(chr(10), '')
#         temp = temp.replace(chr(0), '')
#         returnVal = temp

#     except BaseException as error:
#         returnVal = ''

#     return returnVal
