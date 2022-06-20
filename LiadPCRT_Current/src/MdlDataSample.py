import MdlConnection
import DataSample

def fInitMachineDataSamples(pMachine):
    strSQL = ''
    mDataSample = None
    mControlParam = None
    RstCursor = None
    returnVal = False

    try:
        strSQL = 'Select * From TblDataSamples Where MachineID = ' + str(pMachine.ID)
        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstValues = RstCursor.fetchall()

        for RstData in RstValues:
            mDataSample = DataSample.DataSample()
            mDataSample.Init(pMachine, RstData.ID)
            
            if not pMachine.GetParam(RstData.ControllerFieldName, mControlParam):                    
                pass
            else:
                mControlParam.DataSamples.Add(mDataSample, str(mDataSample.ID))
        RstCursor.close()
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


