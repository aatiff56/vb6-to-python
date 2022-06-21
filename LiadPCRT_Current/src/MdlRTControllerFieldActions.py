import MdlADOFunctions
import MdlGlobal
import MdlConnection

from ControllerFieldAction import ControllerFieldAction

def fLoadMachineControllerFieldActions(Machine):
    returnVal = False
    ControllerID = 0
    ControllerFieldName = ''
    strSQL = ''
    RstCursor = None
    ControllerField = None
    tAction = None
    ControllerFieldName = ''

    try:    
        ControllerID = Machine.ControllerID
        strSQL = 'SELECT ID,ControllerFieldName,Sequence FROM TblControllerFieldActions'
        strSQL = strSQL + ' Where ControllerID = ' + str(ControllerID)
        strSQL = strSQL + ' ORDER BY ControllerFieldName,Sequence'

        RstCursor = MdlConnection.CN.cursor()
        RstCursor.execute(strSQL)
        RstValues = RstCursor.fetchall()

        for RstData in RstValues:
            if MdlADOFunctions.fGetRstValString(RstData.ControllerFieldName) != ControllerFieldName:
                ControllerFieldName = MdlADOFunctions.fGetRstValString(RstData.ControllerFieldName)
                if Machine.GetParam(ControllerFieldName, ControllerField) == False:
                    MdlGlobal.RecordError('fLoadControllerFieldActions', str(3), 'ControllerField could not be found.', 'ControllerFieldActionID = ' + str(RstData.ID))
                    continue

            tAction = ControllerFieldAction()
            tAction.Parent = ControllerField
            tAction.Init(RstData.ID)
            ControllerField.Actions.Add(tAction, MdlADOFunctions.fGetRstValString(RstData.ID))

        RstCursor.close()
        returnVal = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)

    Rst = None
    return returnVal


def fExecutePreActions(ControllerField):
    returnVal = False
    tAction = ControllerFieldAction()

    try:
        for tAction in ControllerField.Actions:
            if tAction.Timing == ControllerFieldAction.ControllerFieldActionTiming.Pre:
                tAction.Validate()
                tAction.Execute()
        returnVal = True

    except:
        pass

    return returnVal


def fExecutePostActions(ControllerField):
    returnVal = False
    tAction = ControllerFieldAction()

    try:
        for tAction in ControllerField.Actions:
            if tAction.Timing == ControllerFieldAction.ControllerFieldActionTiming.Post:
                tAction.Validate()
                tAction.Execute()
        returnVal = True
    
    except:
        pass

    return returnVal
