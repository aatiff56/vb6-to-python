from datetime import datetime
import MdlADOFunctions
import mdl_Common
import MdlConnection
import MdlGlobal


def fJobPConfigSubDetailsUpdate(JobID):
    try:
        PConfigID = 0
        JobAmount = 0
        Counter = 0
        LastJobID = 0
        strSQL = ''
        SRstCursor = MdlConnection.CN.cursor()
        DrstCursor = MdlConnection.CN.cursor()
        PCRstCursor = MdlConnection.CN.cursor()
        rstFormCursor = MdlConnection.CN.cursor()
        CurrentNewAdded = False
        NewJobAdded = False
        
        strSQL = 'Select * From Meta_Tbl_FormFields where FormID = 68 AND IsActive <> 0'
        rstFormCursor.execute(strSQL)

        strSQL = 'Select * From TblJob Where ID = ' + JobID
        SRstCursor.execute(strSQL)
        SRstData = SRstCursor.fetchone()
        if SRstData["IsPConfigMain"] == True and SRstData["PConfigID"] > 0:
            PConfigID = SRstData["PConfigID"]
            JobAmount = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('Amount', 'TblPConfigJobs', 'PConfigID = ' + PConfigID + ' AND ProductID = ' + SRstData["ProductID"], 'CN'))
            
            strSQL = 'Select * From TblPConfigJobs Where PConfigID = ' + PConfigID + ' AND ProductID <> ' + SRstData["ProductID"] + ' ORDER BY ID'
            PCRstCursor.execute(strSQL)

            while not PCRstCursor.next():
                PCRstData = PCRst.fetchone(strSQL)
                NewJobAdded = False
                Counter = Counter + 1
                CurrentNewAdded = False
                LastJobID = 0
                strSQL = 'Select * From TblJob Where PConfigParentID = ' + JobID + ' AND PConfigJobID = ' + PCRstData["ID"] + ' ORDER BY ID'
                DrstData = DrstCursor.fetchone(strSQL)

                if not ( DrstCursor.RecordCount > 0 ):
                    DrstCursor.AddNew()
                    NewJobAdded = True
                DrstData["PConfigJobID"] = MdlADOFunctions.fGetRstValLong(PCRstData["ID"])
                DrstData["PConfigParentID"] = JobID
                DrstData["PConfigID"] = SRstData["PConfigID"]
                DrstData["PConfigRelation"] = MdlADOFunctions.fGetRstValLong(SRstData["PConfigRelation"])
                DrstData["PConfigPC"] = PCRstData["Weight"]
                DrstData["PConfigLabel"] = PCRstData["LabelPrintDeafult"]
                DrstData["PConfigUnits"] = PCRstData["UnitsToInjection"]
                DrstData["PConfigJobCycles"] = PCRstData["PConfigJobCycles"]
                DrstData["PConfigProductionOrder"] = PCRstData["ProductionOrder"]
                DrstData["PConfigIsMaterialCount"] = MdlADOFunctions.fGetRstValBool(PCRstData["IsMaterialCount"], True)
                DrstData["PConfigIsChannel100Count"] = MdlADOFunctions.fGetRstValBool(PCRstData["IsChannel100Count"], True)
                DrstData["PConfigIsSpecialMaterialCount"] = MdlADOFunctions.fGetRstValBool(PCRstData["IsSpecialMaterialCount"], True)
                if DrstData["LocalID"] == None and SRstData["LocalID"] != None:
                    DrstData["LocalID"] = SRstData["LocalID"] + '-' + Counter
                DrstData["Status"] = SRstData["Status"]
                DrstData["CavitiesStandard"] = PCRstData["Amount"]
                DrstData["CavitiesActual"] = PCRstData["Amount"]
                
                if MdlADOFunctions.fCopyRecordByForm(SRstCursor, DrstCursor, rstFormCursor) == False:
                    raise Exception('Invalid Operation')
                DrstData["ProductID"] = PCRstData["ProductID"]
                if SRstData["PConfigUnits"] > 0:
                    DrstData["UnitsTarget"] = PCRstData["UnitsToInjection"] * SRstData["UnitsTarget"] / SRstData["PConfigUnits"]
                else:
                    DrstData["UnitsTarget"] = PCRstData["UnitsToInjection"] * SRstData["UnitsTarget"]
                DrstData["MoldID"] = SRstData["MoldID"]
                DrstData["MachineID"] = SRstData["MachineID"]
                DrstData["ControllerID"] = SRstData["ControllerID"]
                DrstData["Status"] = SRstData["Status"]
                DrstCursor.Update()
                LastJobID = DrstData["ID"]
                DrstCursor.Close()
                
                select_variable_0 = SRstData["Status"]
                if (select_variable_0 == 10):
                    strSQL = 'Select * From TblJobCurrent Where ID = ' + LastJobID
                    
                    if not ( DrstCursor.RecordCount > 0 ) :
                        DrstCursor.AddNew()
                        CurrentNewAdded = True
                    
                    if MdlADOFunctions.fCopyRecordByForm(SRstCursor, DrstCursor, rstFormCursor) == False:
                        raise Exception('Invalid Operation')
                    DrstData["PConfigJobID"] = MdlADOFunctions.fGetRstValLong(PCRstData["ID"])
                    DrstData["ProductID"] = PCRstData["ProductID"]
                    DrstData["PConfigParentID"] = JobID
                    DrstData["PConfigID"] = SRstData["PConfigID"]
                    DrstData["PConfigRelation"] = MdlADOFunctions.fGetRstValLong(SRstData["PConfigRelation"])
                    DrstData["PConfigPC"] = PCRstData["Weight"]
                    DrstData["PConfigLabel"] = PCRstData["LabelPrintDeafult"]
                    DrstData["PConfigUnits"] = PCRstData["UnitsToInjection"]
                    DrstData["PConfigJobCycles"] = PCRstData["PConfigJobCycles"]
                    DrstData["PConfigProductionOrder"] = PCRstData["ProductionOrder"]
                    DrstData["PConfigIsMaterialCount"] = MdlADOFunctions.fGetRstValBool(PCRstData["IsMaterialCount"], True)
                    DrstData["PConfigIsChannel100Count"] = MdlADOFunctions.fGetRstValBool(PCRstData["IsChannel100Count"], True)
                    DrstData["PConfigIsSpecialMaterialCount"] = MdlADOFunctions.fGetRstValBool(PCRstData["IsSpecialMaterialCount"], True)
                    DrstData["Status"] = SRstData["Status"]
                    DrstData["ID"] = LastJobID
                    DrstCursor.Update()
                    DrstCursor.Close()
                    if CurrentNewAdded == True and LastJobID > 0:
                        fJobCurrentTablesAdd(LastJobID, False)
                elif (select_variable_0 == 11) or (select_variable_0 == 12) or (select_variable_0 == 20) or (select_variable_0 == 0):
                    
                    strSQL = 'Delete TblJobCurrent Where PConfigParentID = ' + JobID
                    DrstCursor.execute(strSQL)
                    strSQL = 'Delete TblJobMaterialForecast Where Job=' + LastJobID
                    DrstCursor.execute(strSQL)
                    fRemoveCurrentTables(LastJobID)

        return True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('LeaderRT:fJobPConfigSubDetailsUpdate', 0, error.args[0], str(JobID))
    
        if SRstCursor:
            SRstCursor.Close()
        SRstCursor = None

        if DrstCursor:
            DrstCursor.Close()
        DrstCursor = None

        if PCRst:
            PCRst.Close()
        PCRst = None

        if rstFormCursor:
            rstFormCursor.Close()
        rstFormCursor = None

    return False


def fJobCurrentTablesAdd(RID, RemoveCurrent=True, tMachine=None):
    try:
        RstSourceCursor = MdlConnection.CN.cursor()
        RstTargetCursor = MdlConnection.CN.cursor()
        RstCursor = MdlConnection.CN.cursor()
        rstFormCursor = MdlConnection.CN.cursor()

        strSQL = ''
        JoshID = 0
        ShiftID = 0
        ShiftManagerID = 0
        LastSVID = 0
        ShiftDefID = 0
        JobOrderNum = 0
        InjectionsCountStart = 0
        JoshStartUnits = 0
        MachineID = ''
        WorkerID = ''
        tMachineID = 0
    
        fn_return_value = False
        if RemoveCurrent == True:
            fRemoveCurrentTables(RID, MdlADOFunctions.VBGetMissingArgument(fRemoveCurrentTables, 1), False, False)
        if tMachine is None:
            tMachineID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('MachineID', 'TblJob', 'ID = ' + RID, 'CN'))
        else:
            tMachineID = tMachine.ID
        
        ShiftID = MdlADOFunctions.fGetCurrentShiftIDByShiftCalendar(MdlADOFunctions.fGetShiftCalendarIDByMachine(tMachineID))
        ShiftDefID = MdlADOFunctions.GetSingleValue('ShiftDefID', 'TblShift', 'ID = ' + ShiftID, 'CN')
        ShiftManagerID = MdlADOFunctions.GetSingleValue('ManagerID', 'TblShift', 'ID=' + ShiftID, 'CN')
        strSQL = 'Select * From TblJob Where ID=' + RID

        RstSourceCursor.execute(strSQL)
        RstSourceData = RstSourceCursor.fetchone()
        
        strSQL = 'Select * From TblJobCurrent Where ID = ' + RID
        RstTargetCursor.execute(strSQL)
        RstTargetData = RstTargetCursor.fetchone()
        if RstTargetCursor:
            RstTargetCursor.AddNew()
            RstTargetData["ID"] = RID
        strSQL = 'Select * From Meta_Tbl_FormFields where FormID = 50 AND IsActive <> 0'
        rstFormCursor.execute(strSQL)
        if MdlADOFunctions.fCopyRecordByForm(RstSourceCursor, RstTargetCursor, rstFormCursor) == False:
            raise Exception('Invalid Operation')
        RstTargetData["StartTime"] = datetime.now()
        RstTargetData["SetUpStart"] = datetime.now()
        RstTargetData["Notes"] = RstSourceData["Notes"]
        RstTargetData["EntryTime"] = RstSourceData["EntryTime"]
        RstTargetData["EntryUser"] = RstSourceData["EntryUser"]
        RstTargetCursor.Update()
        RstTargetCursor.Close()
        rstFormCursor.Close()
        strSQL = 'Select JobOrderNum, InjectionsCount From TblJosh  Where JobID = ' + RID + ' Order By ShiftID Desc'
        RstCursor.execute(strSQL)
        RstData = RstCursor.fetchone()
        if not RstCursor:
            if RstData["JobOrderNum"] != None:
                JobOrderNum = RstData["JobOrderNum"]
        RstCursor.Close()
        JobOrderNum = JobOrderNum + 1
        strSQL = 'Select InjectionsCount From TblJob Where ID = ' + RID
        RstCursor.execute(strSQL)
        if not RstCursor:
            if RstData["InjectionsCount"] != None:
                InjectionsCountStart = RstData["InjectionsCount"]
        
        if tMachineID > 0:
            WorkerID = '' + MdlADOFunctions.GetSingleValue('WorkerID', 'TblMachines', 'ID=' + tMachineID, 'CN')
        
        strSQL = 'Select * From TblJosh Where JobID = ' + RID + ' AND ShiftID = ' + ShiftID
        
        RstTargetCursor.AddNew()
        RstTargetData["JobID"] = RID
        RstTargetData["ShiftID"] = ShiftID
        RstTargetData["UnitsProducedPCJob"] = RstSourceData["UnitsProducedPC"]
        RstTargetData["InjectionsCountStart"] = InjectionsCountStart
        RstTargetData["UnitsTargetJob"] = RstSourceData["UnitsTarget"]
        
        strSQL = 'Select * From Meta_Tbl_FormFields where FormID = 51 AND IsActive <> 0'
        if MdlADOFunctions.fCopyRecordByForm(RstSourceCursor, RstTargetCursor, rstFormCursor) == False:
            raise Exception('Invalid Operation')
        if RstSourceData["InjectionsCount"] != None and RstSourceData["CavitiesActual"] != None:
            JoshStartUnits = RstSourceData["InjectionsCount"] * RstSourceData["CavitiesActual"]
            RstTargetData["JoshStartUnits"] = JoshStartUnits
        RstTargetData["StartTime"] = datetime.now()
        RstTargetData["ShiftManagerID"] = ShiftManagerID
        RstTargetData["JobOrderNum"] = JobOrderNum
        RstTargetData["ShiftDefID"] = ShiftDefID
        
        RstTargetData["WorkerID"] = MdlADOFunctions.fGetRstValString(WorkerID)
        
        RstTargetCursor.Update()
        JoshID = RstTargetData["ID"]
        RstTargetCursor.Close()
        
        strSQL = 'Select * From TblJoshCurrent Where ID = ' + JoshID
        if RstTargetCursor:
            RstTargetCursor.AddNew()
            RstTargetData["JobID"] = RID
            RstTargetData["ID"] = JoshID
            RstTargetData["ShiftID"] = ShiftID
            RstTargetData["StartTime"] = datetime.now()
            RstTargetData["ShiftManagerID"] = ShiftManagerID
            RstTargetData["JobOrderNum"] = JobOrderNum
        if MdlADOFunctions.fCopyRecordByForm(RstSourceCursor, RstTargetCursor, rstFormCursor) == False:
            raise Exception('Invalid Operation')
        if RstSourceData["InjectionsCount"] != None and RstSourceData["CavitiesActual"] != None:
            JoshStartUnits = RstSourceData["InjectionsCount"] * RstSourceData["CavitiesActual"]
            RstTargetData["JoshStartUnits"] = JoshStartUnits
        RstTargetData["UnitsProducedJob"] = RstSourceData["UnitsProduced"]
        RstTargetData["UnitsProducedPCJob"] = RstSourceData["UnitsProducedPC"]
        RstTargetData["InjectionsCountStart"] = InjectionsCountStart
        RstTargetData["UnitsTargetJob"] = RstSourceData["UnitsTarget"]
        RstTargetData["ShiftDefID"] = ShiftDefID
        
        RstTargetData["WorkerID"] = MdlADOFunctions.fGetRstValString(WorkerID)
        
        RstTargetCursor.Update()
        fn_return_value = True

    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
        MdlGlobal.RecordError('fJobCurrentTablesAdd', 0, error.args[0], "JobID: " + RID)

    if rstFormCursor:
        rstFormCursor.Close()
    rstFormCursor = None

    if RstSourceCursor:
        RstSourceCursor.Close()
    RstSourceCursor = None

    if RstTargetCursor:
        RstTargetCursor.Close()
    RstTargetCursor = None

    if RstCursor:
        RstCursor.Close()
    RstCursor = None

    return fn_return_value


def fRemoveCurrentTables(RID, AllData=False, DJobCurrent=True, DJobCurrentMaterial=True, DJoshCurrent=True, DJoshCurrentMaterial=True):
    try:
        RstCursor = MdlConnection.CN.cursor()
        strSQL = ''
        MachineID = ''
        strCriteria = ''
        fn_return_value = False
        MachineID = '' + MdlADOFunctions.GetSingleValue('MachineID', 'TblJob', 'ID = ' + RID, 'CN')
        if MachineID != '':
            strCriteria = ' Where MachineID = ' + MachineID
        else:
            strCriteria = ' Where ID = ' + RID
        
        if DJobCurrent == True:
            strSQL = 'Delete TblJobCurrent '
            if AllData == False:
                strSQL = strSQL + strCriteria
            RstCursor.execute(strSQL)        

        if DJoshCurrent == True:
            strSQL = 'Delete TblJoshCurrent '
            if AllData == False:
                strSQL = strSQL + strCriteria
            RstCursor.execute(strSQL)        
        
        if DJobCurrentMaterial == True:
            strSQL = 'Delete TblJobCurrentMaterial  '
            if AllData == False:
                
                strSQL = strSQL + ' WHere Job = ' + RID
            RstCursor.execute(strSQL)        
        
        if DJoshCurrentMaterial == True:
            strSQL = 'Delete TblJoshCurrentMaterial'
            if AllData == False:
                
                strSQL = strSQL + ' WHere JobID = ' + RID
            RstCursor.execute(strSQL)        
        fn_return_value = True                
        cmd = None
    except BaseException as error:
        if 'nnection' in error.args[0]:
            if MdlConnection.CN:
                MdlConnection.Close(MdlConnection.CN)
            MdlConnection.Open(MdlConnection.CN, MdlConnection.strCon)

            if MdlConnection.MetaCn:
                MdlConnection.Close(MdlConnection.MetaCn)
            MdlConnection.Open(MdlConnection.MetaCn, MdlConnection.strMetaCon)
    return fn_return_value

