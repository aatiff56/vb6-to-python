from colorama import Fore
from ControlParam import ControlParam
from DataSample import DataSample

import MdlConnection

def fInitMachineDataSamples(pMachine):
    strSQL = ''
    mDataSample = None
    mControlParam = [None]
    RstCursor = None
    returnVal = False

    try:
        strSQL = 'Select * From TblDataSamples Where MachineID = ' + str(pMachine.ID)
        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstValues = RstCursor.fetchall()

        for RstData in RstValues:
            mDataSample = DataSample()
            
            print(Fore.GREEN + "Loading Machine Controller Field Actions.")
            mDataSample.Init(pMachine, RstData.ID)
            
            if pMachine.GetParam(RstData.ControllerFieldName, mControlParam):                    
                mControlParam[0].DataSamples[str(mDataSample.ID)] = mDataSample
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

    RstCursor = None
    return returnVal


