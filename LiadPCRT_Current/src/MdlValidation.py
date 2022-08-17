from Validation import Validation

import MdlADOFunctions
import MdlConnection

def LoadMachineValidations(pMachine):
    strSQL = ''
    RstCursor = None
    tValidation = None

    try:
        strSQL = 'SELECT ID FROM TblValidations WHERE '
        strSQL = strSQL + ' MachineID = ' + str(pMachine.ID) + ''
        strSQL = strSQL + ' OR DepartmentID = ' + str(pMachine.Department)
        strSQL = strSQL + ' OR MachineType = ' + str(pMachine.MachineType)
        strSQL = strSQL + ' OR ShiftCalendarID = ' + str(pMachine.Server.SCID)
        strSQL = strSQL + ' ORDER BY Sequence'

        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstValues = RstCursor.fetchall()

        for RstData in RstValues:
            tValidation = Validation()
            tValidation.Init(pMachine, MdlADOFunctions.fGetRstValLong(RstData.ID))
            pMachine.Validations[str(tValidation.ID)] = tValidation

        RstCursor.close()

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)

    RstCursor = None


