import MdlConnection

def fInitMachineDataSamples(pMachine):
    strSQL = ""
    mDataSample = DataSample()
    mControlParam = ControlParam()
    dbCursor = None
    returnVal = False

    try:
        dbCursor = MdlConnection.CN.cursor()
 
        if dbCursor:
            strSQL = 'Select * From TblDataSamples Where MachineID = ' + pMachine.ID
            dbCursor.execute(strSQL)

            while dbCursor.next():
                val = dbCursor.fetchone()
                mDataSample = DataSample()
                mDataSample.Init(pMachine, val["ID"])
                
                if not pMachine.GetParam(val["ControllerFieldName"], mControlParam):                    
                    pass
                else:
                    mControlParam.DataSamples.Add(mDataSample, str(mDataSample.ID))
            dbCursor.close()
            returnVal = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
    return returnVal


