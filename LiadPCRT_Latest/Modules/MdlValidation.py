from Common import MdlADOFunctions as adoFunc
from LiadPCUnite.DataAccess import QueryExecutor as qe
from LiadPCUnite.BusinessLogic import SqlConnector as sc
from LiadPCUnite.Global import Logs

sqlCntr = sc.SqlConnector()
logger = Logs.Logger()

def LoadMachineValidations(pMachine):
    try:
        strSQL = ''
        Rst = qe.QueryExecutor(sqlCntr.GetConnection())
        sqlCntr.OpenConnection()
        tValidation = Validation()
        
        strSQL = 'SELECT ID FROM TblValidations WHERE '
        strSQL = strSQL + ' MachineID = ' + pMachine.ID + ''
        strSQL = strSQL + ' OR DepartmentID = ' + pMachine.Department
        strSQL = strSQL + ' OR MachineType = ' + pMachine.MachineType
        strSQL = strSQL + ' OR ShiftCalendarID = ' + pMachine.Server.SCID
        strSQL = strSQL + ' ORDER BY Sequence'
        sqlCntr.OpenConnection()
        RstData = Rst.SelectAllData(strSQL)

        RstData.ActiveConnection = None
        while not RstData.EOF:
            tValidation = Validation()
            tValidation.Init(pMachine, adoFunc.fGetRstValLong(RstData["ID"]))
            pMachine.Validations.Add(tValidation, str(tValidation.ID))
            RstData.MoveNext()
        Rst.CloseConnection()
        Rst = None
        return fn_return_value
    except BaseException as error:
        sqlCntr.CloseConnection()
        logger.Error(error)
        return False


