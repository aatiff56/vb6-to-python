from math import sqrt
import pyodbc
import winreg

HKEY_LOCAL_MACHINE = 0x80000002
HKEY_CURRENT_USER = 0x80000001
REG_OPTION_NON_VOLATILE = 0
KEY_ALL_ACCESS = 0x3F
KEY_SET_VALUE = 0x2
KEY_QUERY_VALUE = 0x1
REG_SZ = 1
REG_DWORD = 4
ERROR_NONE = 0
ERROR_BADDB = 1
ERROR_BADKEY = 2
ERROR_CANTOPEN = 3
ERROR_CANTREAD = 4
ERROR_CANTWRITE = 5
ERROR_OUTOFMEMORY = 6
ERROR_ARENA_TRASHED = 7
ERROR_ACCESS_DENIED = 8
ERROR_INVALID_PARAMETERS = 87
ERROR_NO_MORE_ITEMS = 259

# CN = [{}]
# MetaCn = [{}]
# ERPCN = [{}]
CN = None
MetaCn = None
ERPCN = None

strCon = "Driver={SQL Server};Server=.;Database=LiadData;Trusted_Connection=yes"
strMetaCon = "Driver={SQL Server};Server=.;Database=LiadMeta;Trusted_Connection=yes"
UserTimeOut = 0
    
def Open(connectionString):
    if type(connectionString) == type([]):
        return pyodbc.connect(connectionString[0], autocommit=True)
    else:
        return pyodbc.connect(connectionString, autocommit=True)


def Close(connection):
    connection.close()


def CreateNewKey(sNewKeyName, lPredefinedKey):
    keyCreated = False
    try:
        key = winreg.OpenKeyEx(lPredefinedKey, r"SOFTWARE\\Wow6432Node\\")
        newKey = winreg.CreateKey(key, sNewKeyName)
        if newKey:
            winreg.CloseKey(newKey)
        keyCreated = True

    except BaseException as error:
        print(error)
    return keyCreated


def SetKeyValue(sKeyName, sValueName, vValueSetting, lValueType):
    valueSet = False
    try:
        key = winreg.OpenKeyEx(HKEY_LOCAL_MACHINE, sKeyName)
        winreg.SetValueEx(key, sValueName, 0, lValueType, str(vValueSetting))
        if key:
            winreg.CloseKey(key)
            valueSet = True
    except BaseException as error:
        print(error)

    return valueSet


def SetValueEx(hKey, sValueName, lType, vValue):
    LValue: int
    try:
        sValue = ""
        select_variable_0 = lType
        if (select_variable_0 == REG_SZ):
            sValue = vValue + chr(0)
            return winreg.SetValueEx(hKey, sValueName, 0, lType, sValue, len(sValue))
        elif (select_variable_0 == REG_DWORD):
            LValue = vValue
            return winreg.SetValueEx(hKey, sValueName, 0, lType, LValue, 4)

    except BaseException as error:
        print(error)
        return None


def SetRegMetaValues():
    if not CreateNewKey('SOFTWARE\\WOW6432Node\\Emerald', HKEY_LOCAL_MACHINE):
        raise Exception("Incorrect function.")
    if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'Program', 'ColorSaveMS', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'MetaCatalog', 'LiadMeta', REG_SZ):
        raise Exception("Incorrect function.")

    if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'Provider', 'MSDataShape.1', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'Persist Security Info', 'True', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'Data Source', 'qwebsvr', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'User ID', 'SA', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'Password', PasswordCipher('hobit'), REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'Data Provider', 'SQLOLEDB.1', REG_SZ):
        raise Exception("Incorrect function.")


# def EightToTen(Source):
#     i = 0
#     figure = 0
#     res = 0

#     if int(Source) == 0:
#         fn_return_value = 0
#     else:
#         for i in range(0, len(Source) - 1):
#             # figure = mID(Source, len(Source) - i, 1)
#             figure = Source[len(Source) - i: 1]
#             res = res + figure * 8 ** i
#         fn_return_value = res
#     return fn_return_value


# def PasswordDecipher(Source):
#     result = ""
#     CryptCodeFrom = ""
#     CryptCodeTo = 0
#     CryptCode = 0
#     strRes = ""
#     i = 0
#     fn_return_value = 0

#     # result = mID(Source, 2, len(Source) - 2)
#     result = Source[2: len(Source) - 2]
#     for i in range(0, int(len(result) / 6 - 1)):
#         # CryptCodeFrom = mID(result, i * 6 + 1, 6)
#         CryptCodeFrom = result[i * 6 + 1: 6]
#         CryptCodeTo = EightToTen(CryptCodeFrom)

#         CryptCodeTo = CryptCodeTo - 54321

#         CryptCode = sqrt(CryptCodeTo)
#         strRes = strRes + chr(CryptCode)
#     fn_return_value = strRes
#     return fn_return_value


# def PasswordCipher(Source):
#     result = ""
#     CryptFigure: int
#     CryptCode: int
#     CryptCodeTo: int
#     strRes = ""
#     i: int

#     for i in range(0, len(Source) - 1):
#         # result = mID(Source, i + 1, 1)
#         result = Source[i + 1: 1]
#         CryptFigure = ord(result)

#         CryptCode = CryptFigure ** 2

#         CryptCode = CryptCode + 54321

#         CryptCodeTo = oct(CryptCode)
#         # strRes = strRes + Format(CryptCodeTo, '000000')
#         strRes = strRes + str.format(CryptCodeTo, '000000')
#     return  '{' + strRes + '}'


def SetRegVal(Rst, NameKey):
    if not SetKeyValue(NameKey, 'Program', 'ColorSaveMS', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'DataCatalog', Rst.Fields("InitialCatalog").Value, REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Provider', Rst.Fields("Provider").Value, REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Persist Security Info', Rst.Fields("PersistSecurityInfo").Value, REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Data Source', Rst.Fields("DataSource").Value, REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'User ID', Rst.Fields("UserID").Value, REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Password', PasswordCipher(Rst.Fields("Password").Value), REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Data Provider', Rst.Fields("DataProvider").Value, REG_SZ):
        raise Exception("Incorrect function.")


def SetRegValues(NameKey):
    if not SetKeyValue(NameKey, 'Program', 'ColorSaveMS', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'DataCatalog', 'LiadData', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Provider', 'MSDataShape.1', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Persist Security Info', 'True', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Data Source', 'qwebsvr', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'User ID', 'SA', REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Password', PasswordCipher('hobit'), REG_SZ):
        raise Exception("Incorrect function.")
    if not SetKeyValue(NameKey, 'Data Provider', 'SQLOLEDB.1', REG_SZ):
        raise Exception("Incorrect function.")


def SetUserTimeOut():
    # if not SetKeyValue('SOFTWARE\\WOW6432Node\\Emerald', 'UserTimeOut', '0', REG_SZ):
    #     raise Exception("Incorrect function.")
    return '0'
