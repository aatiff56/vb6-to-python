def GetRegValuesToConnection(strMCn, ArrParams, FromWeb=False):
    returnVal = None
    strRes = ""
    res = ""
    NameOfKey = ""
    AppID = 0
    CommandActivation = False
    returnVal = ''
    NameOfKey = 'SOFTWARE\\Emerald\\1'

    try:
        if not CreateNewKey(NameOfKey, HKEY_LOCAL_MACHINE):
            raise Exception("Couldn't create key '" + NameOfKey + "'.")
        res = QueryValue(NameOfKey, 'Provider')

        if res == '':
            SetRegValues(NameOfKey)
        if res == '':
            res = QueryValue(NameOfKey, 'Provider')
        strRes = 'Provider=' + res.strip() + ';'
        res = QueryValue(NameOfKey, 'Persist Security Info')
        strRes = strRes + 'Persist Security Info=' + res.strip() + ';'
        res = QueryValue('SOFTWARE\\Emerald', 'RTCommandActivation')
        if res == '' or res == '0' or FromWeb == True:
            CommandActivation = False
        else:
            CommandActivation = True

        if CommandActivation:
            if len(ArrParams) >= 0:
                res = ArrParams(2)
            else:
                res = ''
            if res == '':
                res = QueryValue(NameOfKey, 'Data Source')
            strRes = strRes + 'Data Source=' + res.strip() + ';'
            if len(ArrParams) >= 0:
                res = ArrParams(3)
            else:
                res = ''
            if res == '':
                res = QueryValue(NameOfKey, 'User ID')
            strRes = strRes + 'User ID=' + res.strip() + ';'
            if len(ArrParams) >= 0:
                res = ArrParams(4)
            else:
                res = ''
            if res == '':
                res = QueryValue(NameOfKey, 'Password')
                strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
            else:
                strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
            if len(ArrParams) >= 0:
                res = ArrParams(0)
            else:
                res = ''
            if res == '':
                res = QueryValue(NameOfKey, 'DataCatalog')
            strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
        else:
            res = QueryValue(NameOfKey, 'Data Source')
            strRes = strRes + 'Data Source=' + res.strip() + ';'
            res = QueryValue(NameOfKey, 'User ID')
            strRes = strRes + 'User ID=' + res.strip() + ';'
            res = QueryValue(NameOfKey, 'Password')
            strRes = strRes + 'Password=' + MdlConnection.PasswordDecipher(res) + ';'
            res = QueryValue(NameOfKey, 'DataCatalog')
            strRes = strRes + 'Initial Catalog=' + res.strip() + ';'
        res = QueryValue(NameOfKey, 'Data Provider')
        strRes = strRes + 'Data Provider=' + res.strip()
        returnVal = strRes

    except BaseException as error:
        MdlGlobal.RecordError('GetRegValuesToConnection', 0, error.args[0], strRes)
        
    return returnVal
