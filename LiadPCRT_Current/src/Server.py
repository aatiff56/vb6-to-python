from datetime import datetime
from colorama import Fore
from Machine import Machine

import os
import MdlADOFunctions
import mdl_Common
import ShiftCalendar
import MdlConnection
import MdlServer
import MdlGlobal
import SystemVariables

class Server:
    
    mServerID = 0
    mPlantID = 0
    mStatus = 0
    mCNstr = ['']
    mCNStatus = 0
    mMetaCNstr = ['']
    mMetaCNStatus = 0
    mConCount = 0
    mMachines = {}
    mMediaPlayer = None
    mInIO = False
    mReadWaitCount = 0
    mMainXML = ''
    mCurrentShiftID = 0
    mCurrentShift = None
    mShiftCalendar = None
    mProducts = {}
    mMolds = {}
    mDepartments = {}
    mMachineTypes = {}
    mSystemVariables = None
    mStartTime = datetime.now()
    cntShiftTimerInterval = 180000
    cntReadTimerInterval = 3000
    cntReadTimerDelay = 1000
    cntWriteTimerInterval = 600000
    mWriteInterval = 0
    # mOPCServer = OPCServer()
    mOPCServer = None
    # mOPCServerGroups = OPCGroups()
    # mOPCServers = Collection()
    WriteMachine = 0
    ReadMachine = 0
    mSCID = 0
    mActiveInventoryItems = {}

#     def UpdateMachineParamLimits(self, MachineID, FName, dMean, dPUCL, dPLCL, dQUCL, dQLCL, UpdateRecipe):
#         Counter = 0
#         temp = False
#         fn_return_value = False
#         temp = False
#         temp = self.mMachines.Item(str(MachineID)).UpdateParamLimits(FName, dMean, dPUCL, dPLCL, dQUCL, dQLCL, UpdateRecipe)
#         fn_return_value = temp
#         return fn_return_value

#     # def __init__(self):
#     #     if Err.Number != 0:            
#     #         pass

    def StartServer(self, Arr, strSchCN):
        try:
            strSQL = ''
            ServerName = ''
            RstCursor = None
            DepRstCursor = None
            tMachine = None
            CurShift = 0
            MultiTimeZoneLeaderServer = False
            TargetDaylightSavingOn = False
            ThisDBGMT = 0
            DepForSC = ''
            # tOPCServer = OPCServer()
            tSystemVariables = None
            tShiftCalendar = None
            tDepartment = None
            tDuplicateRTFound = False
        
            if len(Arr) >= 0:
                if Arr[5].isnumeric():
                    if MdlADOFunctions.fGetRstValLong(Arr[5]) > 0:
                        self.SCID = MdlADOFunctions.fGetRstValLong(Arr[5])
                    else:
                        self.SCID = 0
                else:
                    self.SCID = 0
            else:
                self.SCID = 0
            self.mServerID = 1
            self.mPlantID = 1
            self.mStatus = 0
            self.mConCount = 1
            print(Fore.GREEN + 'Getting the connection strings.')
            if not mdl_Common.GetConnectionStrings(self.mCNstr, self.mMetaCNstr, strSchCN, Arr):
                raise("Couldn't create connection strings.")

            print(Fore.GREEN + 'Connecting to LiadData Database.')
            MdlConnection.CN = MdlConnection.Open(self.mCNstr)

            print(Fore.GREEN + 'Connecting to LiadMeta Database.')
            MdlConnection.MetaCn = MdlConnection.Open(self.mMetaCNstr)


            if self.SCID != 0:
                print(Fore.GREEN + 'Initializing Shift Calendar.')
                tShiftCalendar = ShiftCalendar.ShiftCalendar()
                tShiftCalendar.Init(self.SCID)
                self.ShiftCalendar = tShiftCalendar
            # tDuplicateRTFound = MdlServer.fCheckForDuplicateRealTimes(self)
            tDuplicateRTFound = False
            if tDuplicateRTFound == True:
                MdlGlobal.RecordError('StartServer', '9999', 'Duplicate Realtimes Found', '')
                print(Fore.GREEN + 'Duplicated RealTimes Found for this ShiftCalendar!!!')
                AllowClose = True
                            
                MdlConnection.Close(MdlConnection.CN)
                MdlConnection.Close(MdlConnection.MetaCn)

                os.kill(os.kill, 0)
                return False
                
            else:
                self.ShiftCalendar.WindowsProcessID = os.getpid()
                self.ShiftCalendar.UpdateWindowsProcessID()
            
            print(Fore.GREEN + 'Cleaning Job Web Params.')
            self.CleanActivateJobWebParams()
            
            # self.mOPCServer = OPCServer()
            # ServerName = MdlADOFunctions.GetSingleValue('OPCServer', 'STblSystemVariables', 'ID = 1', 'CN')
            # self.mOPCServer.Connect(ServerName)
            # self.mOPCServerGroups = self.mOPCServer.OPCGroups
            GeneralGroupRefreshRate = 2000
            
            if self.mSCID > 0:
                CurShift = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CurrentShiftID', 'STblShiftCalendar', 'ID = ' + str(self.SCID), 'CN'))
            else:
                CurShift = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('CurrentShiftID', 'STblSystemVariables', 'ID > 0', 'CN'))
            self.CurrentShiftID = CurShift
            strEncoding = MdlADOFunctions.GetSingleValue('Encoding', 'STblSystemVariables', 'ID > 0', 'CN')
            self.mWriteInterval = MdlADOFunctions.fGetRstValLong(str(MdlADOFunctions.GetSingleValue('WriteInterval', 'STblSystemVariables', 'ID > 0', 'CN')))
            strXMLHeader = '<?xml version=\'1.0\' encoding=\'' + str(strEncoding) + '\' ?>' + '\r\n'
            AlarmOnProgressInterval = MdlADOFunctions.fGetRstValLong(str(MdlADOFunctions.GetSingleValue('SetupProgressInterval', 'STblSystemVariables', 'ID > 0', 'CN')))
            
            MultiTimeZoneLeaderServer = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('MultiTimeZoneLeaderServer', 'STblSystemVariables', 'ID > 0', 'CN'), False)
            TargetDaylightSavingOn = MdlADOFunctions.fGetRstValBool(MdlADOFunctions.GetSingleValue('ThisDBDaylightSavingOn', 'STblSystemVariables', 'ID > 0', 'CN'), False)
            ThisDBGMT = MdlADOFunctions.fGetRstValDouble(MdlADOFunctions.GetSingleValue('ThisDBGMT', 'STblSystemVariables', 'ID > 0', 'CN'))
            if MultiTimeZoneLeaderServer and ThisDBGMT > - 720.1 and ThisDBGMT < 720.1:
                if TargetDaylightSavingOn:
                    GMTAdd = ThisDBGMT + 60
                else:
                    GMTAdd = ThisDBGMT
                GMTAdd = GMTAdd -  ( mdl_Common.GetTimeDifference() / 60 )
            else:
                GMTAdd = 0
            
            if GMTAdd != 0:
                self.StartTime = mdl_Common.DateAdd('n', ( GMTAdd ), self.StartTime)
            
            tSystemVariables = SystemVariables.SystemVariables()
            print(Fore.GREEN + 'Initializing System Variables.')
            tSystemVariables.Init()
            self.SystemVariables = tSystemVariables                    

            print(Fore.GREEN + 'Clearing Alarms on Server Initialization.')
            self.fClearAlarmsOnServerINIT(self.SCID)
            
            if self.mSCID > 0:
                strSQL = 'SELECT ID From STblDepartments Where ShiftCalendarID = ' + str(self.mSCID)
                DepRstCursor = MdlConnection.CN.cursor()
                DepRstCursor.execute(strSQL)
                DepRstData = DepRstCursor.fetchall()

                for DepRstValue in DepRstData:                    
                    self.ShiftCalendar.AddDepartment(MdlServer.GetOrCreateDepartment(self, MdlADOFunctions.fGetRstValLong(DepRstValue.ID)))
                    strSQL = 'Select ID, OPCServerName, OPCServerIP From TblMachines Where IsActive <> 0 AND Department = ' + str(DepRstValue.ID) + ' ORDER BY ID'

                    RstCursor = MdlConnection.CN.cursor()
                    RstCursor.execute(strSQL)
                    RstData = RstCursor.fetchall()

                    for RstValue in RstData:
                        tMachine = Machine()
                        
                        tMachine.Server = self
                        ServerName = RstValue.OPCServerName
                        if ServerName != '':
                            tOPCServer = None
                            # tOPCServer = OPCServer()
                            # self.mOPCServers.Add(tOPCServer, str(RstValue.ID))
                            # tOPCServer.Connect(ServerName, '' + RstValue.OPCServerIP)
                            # self.mOPCServerGroups = self.mOPCServer.OPCGroups
                        else:
                            tOPCServer = self.mOPCServer
                        if tMachine.INITMachine(RstValue.ID, tOPCServer) == False:
                            pass
                        self.mMachines.Add(tMachine, str(RstValue.ID))
                        MdlServer.GetOrCreateDepartment(self, MdlADOFunctions.fGetRstValLong(DepRstValue.ID)).AddMachine(tMachine)

                    RstCursor.close()
                DepRstCursor.close()
            else:
                strSQL = 'Select ID From TblMachines Where IsActive <> 0 ORDER BY ID'

                RstCursor = MdlConnection.CN.cursor()
                RstCursor.execute(strSQL)
                RstData = RstCursor.fetchall()

                for RstValue in RstData:
                    tMachine = Machine()
                    
                    tMachine.Server = self
                    if tMachine.INITMachine(RstValue.ID, self.mOPCServer) == False:
                        
                        pass
                    self.mMachines.Add(tMachine, str(RstValue.ID))

                RstCursor.close()
            self.GetCurrentShift
            self.ClosePreviousShifts
            
            self.CompleteMissingShiftsObject
            
            self.ClosePreviousJoshs
            self.ClosePreviousEvents
            self.ClosePreviousWorkingEvents
            self.ClosePreviousEngineEvents
            
            # self.mMediaPlayer = MediaPlayer.MediaPlayer()
            self.mMediaPlayer.AutoStart = True
            
            self.LoadRefControllerFields
            
            return True

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)

            if RstCursor:
                RstCursor.close() 
                RstCursor = None

            if DepRstCursor:
                DepRstCursor.close() 
                DepRstCursor = None

            return False

#     def GetCurrentShift(self):
#         try:
#             self.fShiftTimer_Tick()
#         except BaseException as error:
#             self.logger.Error(error)

#     def CloseEvents(self, pCurrentShiftID):
#         try:
#             strSQL = ''
#             tEventID = 0
#             tEventGroupID = 0
#             tEndTime = Date()
#             tDuration = 0
#             tEffectiveDuration = 0
#             tIsInActiveTime = False
#             tIsDownTime = False
#             tPConfigPC = 0
#             Rst = None
#             eRst = None
#             self.sqlCntr.OpenConnection()
#             tMachine = Machine()
            
#             strSQL = ''
#             strSQL = strSQL + 'SELECT *' + '\r\n'
#             strSQL = strSQL + 'FROM TblEvent' + '\r\n'
#             strSQL = strSQL + 'WHERE ShiftID = ' + pCurrentShiftID + ' AND EndTime IS NULL'
#             RstData = Rst.SelectAllData(strSQL)
#             while not RstData.EOF:    
#                 tEventID = 0
#                 tEventGroupID = 0
#                 tEndTime = mdl_Common.NowGMT()
#                 tDuration = MdlADOFunctions.fGetRstValDouble(DateDiff('n', RstData.EventTime, mdl_Common.NowGMT()))
#                 RstData.Status = 3
                
#                 if fCheckCalendarForCloseEventsOnStart(MdlADOFunctions.fGetRstValLong(RstData.MachineID), CDate(RstData.EventTime), tDuration, tEventID, tEventGroupID) == True:
#                     RstData.IsCalendarEvent = True
#                     RstData.RootEventID = 0
#                 else:
#                     tEventID = MdlADOFunctions.fGetRstValLong(RstData.event)
#                     tEventGroupID = MdlADOFunctions.fGetRstValLong(RstData.EventGroup)
#                 tPConfigPC = MdlADOFunctions.fGetRstValDouble(RstData.PConfigPC)
#                 if tPConfigPC == 0:
#                     tPConfigPC = 100
#                 tEffectiveDuration = tDuration *  ( tPConfigPC / 100 )
#                 if tEventID == 0:
#                     RstData.DownTime = tDuration
#                     RstData.EffectiveDownTime = tEffectiveDuration
#                 else:
#                     eRst = None
#                     strSQL = 'SELECT IsDownTime,IsInActiveTime FROM STblEventDesr WHERE ID = ' + tEventID
#                     eRstData = eRst.SelectAllData(strSQL)
#                     if eRstData.RecordCount == 1:
#                         tIsInActiveTime = MdlADOFunctions.fGetRstValBool(eRstData["IsInactiveTime"], False)
#                         tIsDownTime = MdlADOFunctions.fGetRstValBool(eRstData["IsDownTime"], False)
#                     eRstData.Close()
#                     eRstData = None
#                     if tIsInActiveTime == True:
#                         RstData.InActiveTime = tDuration
#                         RstData.EffectiveInActiveTime = tEffectiveDuration
#                     else:
#                         RstData.InActiveTime = 0
#                         RstData.EffectiveInActiveTime = 0
#                     if tIsDownTime == True:
#                         RstData.DownTime = tDuration
#                         RstData.EffectiveDownTime = tEffectiveDuration
#                     else:
#                         RstData.DownTime = 0
#                         RstData.EffectiveDownTime = 0
#                 if MdlADOFunctions.fGetRstValLong(RstData.PConfigParentID) != 0:
#                     tDuration = 0
#                 RstData.event = tEventID
#                 RstData.EventGroup = tEventGroupID
#                 RstData.EndTime = tEndTime
#                 RstData.Duration = tDuration
#                 RstData.EffectiveDuration = tEffectiveDuration
#                 RstData.Update()
#                 RstData.MoveNext()
#             RstData.Close()
#             RstData = None
#         except BaseException as error:
#             self.sqlCntr.CloseConnection()
#             self.logger.Error(error)

#     def __del__(self):
#         try:
#             Counter = 0
#             tOPCServer = OPCServer()
#             for Counter in range(1, self.mMachines.Count):            
#                 self.mMachines.Remove(Counter)
#             self.mMachines = None            
#             self.mMediaPlayer = None
            
#             if not ( self.mOPCServer is None ) :
#                 if self.mOPCServer.ServerState == 1:
#                     self.mOPCServer.Disconnect()
#             for tOPCServer in self.mOPCServers:
#                 if not ( tOPCServer is None ) :
#                     if tOPCServer.ServerState == 1:
#                         tOPCServer.Disconnect()
#             self.mOPCServer = None
#             tOPCServer = None
#         except BaseException as error:
#             self.sqlCntr.CloseConnection()
#             self.logger.Error(error)

#     def WMPlayFile(self, strFilePath, pMachineID, pJobID, Repeated=False):
#         try:
#             self.sqlCntr.OpenConnection()
#             Rst = None
            
#             strSQL = ''
#             strSQL = 'INSERT INTO TblNotifications ' + '\r\n'
#             strSQL = strSQL + '(NotificationType, MachineID, JobID, FilePath, Repeated)' + '\r\n'
#             strSQL = strSQL + 'VALUES (1,' + pMachineID + ',' + pJobID + ',\'' + strFilePath + '\',' + IIf(Repeated == True, '1', '0') + ')'
#             Rst.ManipulateData(strSQL)
#             strSQL = ''
#         except BaseException as error:
#             self.sqlCntr.CloseConnection()
#             self.logger.Error(error)

#     def WMPlayStop(self):        
#         self.mMediaPlayer.Stop()

#     def fShiftTimer_Tick(self):
#         fCalcShiftChange(self)
#         fn_return_value = 'Shift ' + mdl_Common.NowGMT + '; Error: ' + Err.Number + ':' + Err.Description
#         return fn_return_value

#     def XMLMain(self, McID):
#         strXML = ''
#         Counter = 0
#         IsOnline = Date()
#         tMachine = Machine()
#         IsOnline = ShortDate(mdl_Common.NowGMT(), False, True)

#         if McID == 0:
#             fn_return_value = self.mMainXML
#         else:
#             tMachine = self.mMachines.Item(McID)
#             strXML = strXML + '<Machines>'
#             strXML = strXML + tMachine.XMLMain
#             strXML = XmlHeader + '\r\n' + strXML + '<IsOnline>' + str(IsOnline) + '</IsOnline>' + '\r\n' + '</Machines>' + '\r\n'
#             fn_return_value = strXML
#         return fn_return_value

#     def XMLMainCalc(self, DepartmentID):
#         try:
#             Counter = 0
#             strXML = ''
#             strDepartmentXML = ''
#             strSQL = ''
#             strTemp = ''
#             tMachine = Machine()
#             IsOnline = Date()
#             Rst = None
#             self.sqlCntr.OpenConnection()
#             IsOnline = ShortDate(mdl_Common.NowGMT(), False, True)
#             strDepartmentXML = strDepartmentXML + '<Machines>'
#             for Counter in range(1, self.mMachines.Count):
#                 tMachine = self.mMachines.Item(Counter)
#                 strTemp = tMachine.XMLMain
                
#                 if DepartmentID > 0:
#                     if self.mMachines.Item(Counter).Department == DepartmentID:
#                         strDepartmentXML = strDepartmentXML + strTemp
            
#             strDepartmentXML = XmlHeader + '\r\n' + strDepartmentXML + '<IsOnline>' + str(IsOnline) + '</IsOnline>' + '\r\n' + '</Machines>' + '\r\n'
            
#             if DepartmentID > 0:
#                 strSQL = 'Select MachinesMainXML From STblDepartments Where ID  = ' + DepartmentID
#                 RstData = Rst.SelectAllData(strSQL)
#                 RstData.MachinesMainXML = strDepartmentXML
#                 RstData.Update()
#                 RstData.Close()
#             strDepartmentXML = ''
#             strXML = ''
                
#             if RstData.State != 0:
#                 RstData.Close()
#             RstData = None
#         except BaseException as error:
#             self.sqlCntr.CloseConnection()
#             self.logger.Error(error)

#     def XMLController(self, McID):
#         try:
#             strXML = ''
#             Counter = 0
#             tMachine = Machine()
#             tMachine = self.mMachines.Item(str(McID))
#             strXML = XmlHeader + '\r\n' + tMachine.XMLController
#             fn_return_value = strXML
#             return fn_return_value
#         except BaseException as error:
#             self.logger.Error(error)
#             return ''

#     def XMLChannel(self, McID):
#         try:
#             strXML = ''
#             Counter = 0
#             tMachine = Machine()
#             tMachine = self.mMachines.Item(str(McID))
#             strXML = XmlHeader + '\r\n' + tMachine.XMLChannel
#             fn_return_value = strXML
#             return fn_return_value
#         except BaseException as error:
#             self.logger.Error(error)
#             return ''

#     def GetMachineFieldValue(self, MachineID, FieldName, ValType='LasValue'):
#         tMachine = Machine()
        
#         tMachine = self.mMachines.Item(str(MachineID))
#         select_variable_0 = FieldName
#         if (select_variable_0 == 'MoldCavities'):
            
#             fn_return_value = tMachine.MoldActiveCavities
#         elif (select_variable_0 == 'ActiveJobID'):
#             fn_return_value = tMachine.ActiveJobID
#         else:
#             fn_return_value = tMachine.GetFieldValue(FieldName, ValType)
#         return fn_return_value

#     def SetMachineFieldLValue(self, MachineID, FieldName, pLValue):
#         try:
#             tMachine = Machine()
#             tChannel = Channel()
#             tChannelNum = 0
            
#             tMachine = self.mMachines.Item(str(MachineID))
#             fn_return_value = tMachine.SetFieldLValue('MoldCavities', pLValue)
#             return fn_return_value
#         except BaseException as error:
#             self.logger.Error(error)
#             return ''

#     def SetMachineFieldHValue(self, MachineID, FieldName, pLValue):
#         try:
#             tMachine = Machine()
#             tChannel = Channel()
#             tChannelNum = 0
#             tMachine = self.mMachines.Item(str(MachineID))
#             fn_return_value = tMachine.SetFieldLValue('MoldCavities', pLValue)
#             return fn_return_value

#         except BaseException as error:
#             self.logger.Error(error)
#             return ''

#     def SetMachineFieldValue(self, MachineID, FieldName, strValue):
#         try:
#             tMachine = Machine()
#             tChannel = Channel()
#             tChannelNum = 0
#             tMachine = self.mMachines.Item(str(MachineID))
#             select_variable_1 = FieldName

#             if (select_variable_1 == 'MoldActiveCavities'):
#                 tMachine.MoldActiveCavities = strValue
#                 if not tMachine.ActiveJob is None:
#                     tMachine.ActiveJob.CavitiesActual = CDbl(strValue)
#                     if not tMachine.ActiveJob.ActiveJosh is None:
#                         tMachine.ActiveJob.ActiveJosh.CavitiesActual = strValue
#                 fn_return_value = tMachine.SetFieldValue('MoldCavities', strValue)
#                 fn_return_value = True
#             elif (select_variable_1 == 'Cnl1IsActive'):
#                 if not tMachine.ActiveJob is None:
#                     fn_return_value = tMachine.SetFieldValue(FieldName, strValue)
                
#             elif (select_variable_1 == 'ProductWeight'):
#                 if not tMachine.ActiveJob is None:
#                     tMachine.ActiveJob.ProductWeightLast = CDbl(strValue)
#                     tMachine.ActiveJob.ProductWeightStandard = CDbl(strValue)
#                     if not tMachine.ActiveJob.ActiveJosh is None:
#                         tMachine.ActiveJob.ActiveJosh.ProductWeightLast = CDbl(strValue)
#                         tMachine.ActiveJob.ActiveJosh.ProductWeightStandard = CDbl(strValue)
#                 fn_return_value = tMachine.SetFieldValue(FieldName, strValue)
#             elif (select_variable_1 == 'DSIsActive'):
#                 if strValue == '0':
#                     tMachine.DSIsActive = False
#                 elif strValue == '1':
#                     tMachine.DSIsActive = True
#             else:
#                 fn_return_value = tMachine.SetFieldValue(FieldName, strValue)
#             return fn_return_value
#         except BaseException as error:
#             self.logger.Error(error)
#             return ''

#     def fUpdateMachineAlarm(self, pAlarmActive, pMachineID):
#         tMachine = Machine()
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
#         tMachine.AlarmsActive = pAlarmActive
#         fn_return_value = True
#         return fn_return_value

#     def AlarmsAcknowledge(self, MachineID):
#         tMachine = Machine()
#         UpdateParam = False
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(MachineID))
#         tMachine.UpdateAlarmsFromDB
#         return fn_return_value

#     def AlarmsXML(self, MachineID):
#         strXML = ''
#         tMachine = Machine()
#         tMachine = self.mMachines.Item(str(MachineID))
#         strXML = XmlHeader + tMachine.AlarmsXML
#         fn_return_value = strXML
#         return fn_return_value

#     def MachineLoadJob(self, MachineID, JobID, ResetTotals, pFromActivateJob):
#         try:
#             tMachine = Machine()
#             tJob = 0
#             TResetTotals = False
#             tMachine = self.mMachines.Item(str(MachineID))
#             tJob = JobID
#             if JobID == 0:
#                 TResetTotals = False
#             else:
#                 TResetTotals = ResetTotals
#             fn_return_value = tMachine.JobLoad(tJob, TResetTotals, VBGetMissingArgument(tMachine.JobLoad, 2), VBGetMissingArgument(tMachine.JobLoad, 3), pFromActivateJob)
#             if tJob != 0:
#                 fCopyJobRecipeToJoshRecipe(tJob, tMachine.ActiveJoshID)
                
#             return fn_return_value
#         except BaseException as error:
#             self.logger.Error(error)
#             return ''

    
#     def ShiftChange(self, EndTimeForOldShift, OldShift=VBMissingArgument, NewShiftDef=VBMissingArgument, ManagerID=0):
#         Counter = 0
#         tMachine = Machine()
#         fn_return_value = fShiftChange(EndTimeForOldShift, self, OldShift, NewShiftDef, ManagerID)
#         return fn_return_value

#     def MachinesCount(self):
#         fn_return_value = self.mMachines.Count
#         return fn_return_value

#     def CalcJobData(self, McID):
#         tMachine = Machine()
#         Status = 0
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(McID))
#         tMachine.fWriteMainData
#         fn_return_value = True
#         return fn_return_value

#     def fReadTimer_Tick(self):
#         Counter = 0
#         WriteCount = 0
#         tMachineName = ''
#         strSQL = ''
#         if DateDiff('n', self.ShiftCalendar.LastSQLReconnect, mdl_Common.NowGMT) >= self.ShiftCalendar.SQLReconnectInterval:
#             self.ShiftCalendar.LastSQLReconnect = mdl_Common.NowGMT
#             if CN.State == 1:
#                 CN.Close()
#             if MetaCn.State == 1:
#                 MetaCn.Close()
#             CN.Open()
#             MetaCn.Open()
#         self.RunWebActions()
#         if CN.State == 0:
#             CN.Open()
#         if MetaCn.State == 0:
#             MetaCn.Open()
#         if self.mWriteInterval == 0:
#             if self.mMachines.Count > 1:
#                 self.ReadMachine = self.GetNextMachineRead(self.ReadMachine)
#             else:
#                 self.ReadMachine = 1
#             if self.ReadMachine > 0:
#                 self.mMachines.Item(self.ReadMachine).fReadMainData(False, True)
#                 tMachineName = self.mMachines.Item(self.ReadMachine).LName
#         else:
#             for Counter in range(1, self.mMachines.Count):
#                 self.mMachines.Item(Counter).fReadMainData(False, False)
            
#             for Counter in range(1, self.mWriteInterval):
#                 if self.mMachines.Count > 1:
#                     self.ReadMachine = self.GetNextMachineRead(self.ReadMachine)
#                 else:
#                     self.ReadMachine = 1
#                 if self.ReadMachine > 0:
#                     self.mMachines.Item(self.ReadMachine).fReadMainData(False, True)
#         self.mReadWaitCount = self.mMachines.Count - self.ReadMachine
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             if CN.Errors.Count < 200 and CN.Errors.Count > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
                
#             if MetaCn.Errors.Count < 200 and CN.Errors.Count > 0:
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
                
#             fn_return_value = 'Read: ' + mdl_Common.NowGMT + '; Machine:' + self.ReadMachine + ' (' + tMachineName + '); Wait: ' + self.mReadWaitCount + '; Error: ' + Err.Number + ':' + Err.Description
#             Err.Clear()
            
#         fn_return_value = 'Read: ' + mdl_Common.NowGMT + '; Machine:' + self.ReadMachine + ' (' + tMachineName + '); Wait: ' + self.mReadWaitCount + '; Error: ' + Err.Number + ':' + Err.Description
#         strSQL = 'UPDATE STblShiftCalendar SET Descr = \'' + strFixBadChars(self.fReadTimer_Tick()) + '\', RTLastUpdate = \'' + ShortDate(mdl_Common.NowGMT, True, True, True) + '\' Where ID = ' + self.SCID
#         CN.Execute(( strSQL ))
#         return fn_return_value

#     def fWriteTimer_Tick(self):
#         return 'Write ' + mdl_Common.NowGMT + '; Error: ' + Err.Number + ':' + Err.Description

#     def WriteAllMachines(self, pCalcMaterial=True):
#         Counter = 0
        
#         fn_return_value = False
#         for Counter in range(1, self.mMachines.Count):
#             self.mMachines.Item(Counter).fWriteMainData
#         fn_return_value = True
#         return fn_return_value

#     def GeneralUpdateRateGet(self, MachineID):
#         tMachine = Machine()
        
#         tMachine = self.mMachines.Item(str(MachineID))
#         return tMachine.GeneralUpdateRate

#     def MachineControllerAdd(self, MachineID, ControllerDefID, ChannelID):
#         temp = ''
#         strChannel = ''
#         strDescr = ''
#         tMachine = Machine()
#         strChannel = fGetStringNumber('Channel', CDbl(ChannelID), 2)
#         temp = QAddMachine(ControllerDefID, MachineID, self.mOPCServer, strChannel, strDescr)
#         fn_return_value = strDescr
#         if temp == 'True':
#             tMachine = Machine()
#             if tMachine.INITMachine(MachineID, self.mOPCServer) == False:
#                 pass
#             self.mMachines.Add(tMachine, str(MachineID))
#             tMachine.Server = self
        
#         return fn_return_value

#     def MachineControllerDel(self, MachineID, ChannelID):
#         temp = ''
#         strChannel = ''
#         tMachine = Machine()
#         CsID = 0
#         Counter = 0
#         fn_return_value = False
#         strChannel = fGetStringNumber('Channel', CDbl(ChannelID), 2)
#         tMachine = self.mMachines.Item(str(MachineID))
#         CsID = tMachine.ControllerID
#         if QMachineDel(CsID, strChannel, self.mOPCServer) == False:
#             raise(1)
#         else:
#             for Counter in range(1, self.mMachines.Count):
#                 if self.mMachines.Item(Counter).ID == MachineID:
#                     self.mMachines.Remove(str(MachineID))
#                     tMachine.__del__()
#                     tMachine = None
#                     break
#         fn_return_value = True
#         return fn_return_value

#     def MachineSetupEnd(self, pMachineID, pRejectReasonID, pTechnicianUserID, pJobID=0):
#         tMachine = Machine()
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not tMachine.ActiveJob is None:
#             if pJobID != 0 and tMachine.ActiveJob.ID != pJobID:
#                 fn_return_value = True
#                 return fn_return_value
#             if tMachine.NewJob == True:
#                 tMachine.ActiveJob.EndSetUp(pRejectReasonID, pTechnicianUserID)
#         fn_return_value = True
#         return fn_return_value

    
    
#     def MachineManualReadSet(self, McID, ManualRead):
#         tMachine = Machine()
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(McID))
#         tMachine.ManualRead = ManualRead
#         fn_return_value = True
#         return fn_return_value

    
#     def GetNextMachineRead(self, lReadMachine):
#         AllCount = 0
        
#         AllCount = self.mMachines.Count
#         while AllCount > 0:
#             if lReadMachine <  ( self.mMachines.Count ) :
#                 lReadMachine = lReadMachine + 1
#             else:
#                 lReadMachine = 1
#             if ( self.mMachines.Item(lReadMachine).ManualRead == False )  and  ( not self.mMachines.Item(lReadMachine).IsDosingSystem ) :
#                 fn_return_value = lReadMachine
#                 break
#             else:
#                 AllCount = AllCount - 1
        
        
#         return fn_return_value

    
#     def ManualEntryCalc(self, pMachineID):
#         tMachine = Machine()
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if tMachine.ManualEntryCalc() == False:
#             raise(1)
#         fn_return_value = True
#         return fn_return_value

    
#     def GetNextMachineWrite(self, lWriteMachine):
#         AllCount = 0
        
#         AllCount = self.mMachines.Count
#         while AllCount > 0:
#             if lWriteMachine <  ( self.mMachines.Count ) :
#                 lWriteMachine = lWriteMachine + 1
#             else:
#                 lWriteMachine = 1
#             if self.mMachines.Item(lWriteMachine).ManualRead == False:
#                 fn_return_value = lWriteMachine
#                 break
#             else:
#                 AllCount = AllCount - 1
        
        
#         return fn_return_value

#     def RunWebActions(self):
#         strSQL = ''

#         FuncName = ''

#         ActionOK = False

#         Rst = None

#         Arg1 = Variant()

#         Arg2 = Variant()

#         Arg3 = Variant()

#         Arg4 = Variant()

#         Arg5 = Variant()

#         Arg6 = Variant()

#         Arg7 = Variant()

#         Arg8 = Variant()

#         MachineID = 0

#         RecalcMachine = False

#         tMachine = Machine()

#         tmpIngnoreCycleTimeFilter = False
        
#         RecalcMachine = False
#         tmpIngnoreCycleTimeFilter = False
        
#         strSQL = 'Select * From STblWebParams ORDER BY ID'
#         RstData = Rst.SelectAllData(strSQL)
#         while not Rst.EOF:
#             FuncName = '' + Rst["FuncName"]
#             select_variable_2 = FuncName
#             if (select_variable_2 == 'ShiftChange'):
                
#                 Arg1 = CDate('' + Rst["Arg1"])
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 Arg4 = MdlADOFunctions.fGetRstValLong(Rst["Arg4"])
#                 ActionOK = self.ShiftChange(Arg1, CLng(Arg2), CLng(Arg3), CLng(Arg4))
#             elif (select_variable_2 == 'ChangeMoldCavities'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = '' + Rst["Arg2"]
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
#                 ActionOK = self.SetMachineFieldValue(CLng(Arg1), 'MoldActiveCavities', str(Arg2))
#             elif (select_variable_2 == 'SetMachineFieldValue'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = '' + Rst["Arg2"]
#                 Arg3 = '' + Rst["Arg3"]
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.SetMachineFieldValue(CLng(Arg1), str(Arg2), str(Arg3))
#                 RecalcMachine = True
#                 MachineID = CLng(Arg1)
#             elif (select_variable_2 == 'DownloadMachineQueue'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
#                 ActionOK = self.DownloadMachineQueue(CLng(Arg1))
#                 MachineID = CLng(Arg1)
#             elif (select_variable_2 == 'MachineSetupEnd'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 Arg4 = MdlADOFunctions.fGetRstValLong(Rst["Arg4"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.MachineSetupEnd(CLng(Arg1), CLng(Arg2), CLng(Arg3), CLng(Arg4))
#                 RecalcMachine = True
#                 MachineID = CLng(Arg1)
#                 tmpIngnoreCycleTimeFilter = True
#             elif (select_variable_2 == 'ManualEntryCalc'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.ManualEntryCalc(CLng(Arg1))
#                 tmpIngnoreCycleTimeFilter = True
#             elif (select_variable_2 == 'MachineLoadJob'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValBool(Rst["Arg3"], False)
#                 Arg4 = MdlADOFunctions.fGetRstValBool(Rst["Arg4"], False)
#                 Debug.Print('WEB: MachineLoadJob: MachineID=' + Arg1 + ' JobID=' + Arg2 + ' ResetTotals=' + Arg3 + ' FromActivateJob=' + Arg4 + ' | ' + mdl_Common.NowGMT)
#                 ActionOK = self.MachineLoadJob(CLng(Arg1), CLng(Arg2), CBool(Arg3), CBool(Arg4))
#                 if CLng(Arg2) > 0:
#                     RecalcMachine = True
#                     MachineID = CLng(Arg1)
#                 if CBool(Arg3) == False:
#                     tmpIngnoreCycleTimeFilter = True
#                 else:
#                     tmpIngnoreCycleTimeFilter = False
#             elif (select_variable_2 == 'AlarmsAcknowledge'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.AlarmsAcknowledge(CLng(Arg1))
#             elif (select_variable_2 == 'fUpdateMachineAlarm'):
                
#                 Arg2 = MdlADOFunctions.fGetRstValBool(Rst["Arg1"], True)
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.fUpdateMachineAlarm(CBool(Arg2), CLng(Arg1))
#             elif (select_variable_2 == 'MachineManualReadSet'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValBool(Rst["Arg2"], False)
#                 ActionOK = self.fUpdateMachineAlarm(CLng(Arg1), CBool(Arg2))
#             elif (select_variable_2 == 'CalcJobData'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.CalcJobData(CLng(Arg1))
#             elif (select_variable_2 == 'UpdateMachineParamLimits'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 Arg2 = '' + Rst["Arg2"]
#                 Arg3 = '' + Rst["Arg3"]
#                 Arg4 = '' + Rst["Arg4"]
#                 Arg5 = '' + Rst["Arg5"]
#                 Arg6 = '' + Rst["Arg6"]
#                 Arg7 = '' + Rst["Arg7"]
#                 Arg8 = '' + Rst["Arg8"]
#                 if Arg8 == 'true' or Arg8 == 'True' or Arg8 == 'TRUE' or Arg8 == '1' or Arg8 == '-1':
#                     Arg8 = True
#                 else:
#                     Arg8 = False
#                 ActionOK = self.UpdateMachineParamLimits(CLng(Arg1), '' + Arg2, '' + Arg3, '' + Arg4, '' + Arg5, '' + Arg6, '' + Arg7, CBool(Arg8))
#                 RecalcMachine = True
#                 MachineID = CLng(Arg1)
#             elif (select_variable_2 == 'MachineControllerDel'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 ActionOK = self.MachineControllerDel(CLng(Arg1), CLng(Arg2))
#             elif (select_variable_2 == 'MachineControllerAdd'):
                
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 self.MachineControllerAdd(CLng(Arg1), CLng(Arg2), CLng(Arg3))
#             elif (select_variable_2 == 'MachineJobDetailsCalc'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
                
#                 Arg4 = MdlADOFunctions.fGetRstValLong(Abs(MdlADOFunctions.fGetRstValBool(Rst["Arg4"], False)))
#                 Arg5 = MdlADOFunctions.fGetRstValLong(Rst["Arg5"])
                
#                 ActionOK = self.MachineJobDetailsCalc(CLng(Arg1), CLng(Arg2), CLng(Arg3), CLng(Arg4), CLng(Arg5))
#             elif (select_variable_2 == 'MachineJoshDetailsCalc'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
                
#                 Arg4 = MdlADOFunctions.fGetRstValLong(Abs(MdlADOFunctions.fGetRstValBool(Rst["Arg4"], False)))
#                 Arg5 = MdlADOFunctions.fGetRstValLong(Rst["Arg5"])
#                 ActionOK = self.MachineJoshDetailsCalc(CLng(Arg1), CLng(Arg2), CLng(Arg3), CLng(Arg4), CLng(Arg5))
#             elif (select_variable_2 == 'UpdateControllerFieldsParam'):
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
                
#                 ActionOK = self.fUpdateControllerFieldsParam(CLng(Arg1), CLng(Arg2))
#             elif (select_variable_2 == 'UpdateJobUnitsReportedOK'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValDouble(Rst["Arg3"])
#                 self.UpdateJobUnitsReportedOK(CLng(Arg1), CLng(Arg2), CDbl(Arg3))
#             elif (select_variable_2 == 'UpdateJoshUnitsReportedOK'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValDouble(Rst["Arg3"])
#                 self.UpdateJoshUnitsReportedOK(CLng(Arg1), CLng(Arg2), CDbl(Arg3))
#             elif (select_variable_2 == 'UpdateMoldEndTime'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 self.UpdateMoldEndTime(CLng(Arg1))
#             elif (select_variable_2 == 'UpdateUnitsTarget'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValDouble(Rst["Arg3"])
#                 self.UpdateMachineUnitsTarget(CLng(Arg1), CLng(Arg2), CDbl(Arg3))
#             elif (select_variable_2 == 'UpdateOpenEvent'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 Arg4 = MdlADOFunctions.fGetRstValLong(Rst["Arg4"])
#                 Arg5 = MdlADOFunctions.fGetRstValLong(Rst["Arg5"])
#                 self.UpdateMachineOpenEvent(CLng(Arg1), CLng(Arg2), CLng(Arg3), CLng(Arg4), CLng(Arg5))
#             elif (select_variable_2 == 'StartMaterialFlow'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 self.StartMachineMaterialFlow(CLng(Arg1), CLng(Arg2))
#             elif (select_variable_2 == 'AddMaterialFlowFromLastJob'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 self.AddMaterialFlowFromLastJob(CLng(Arg1), CLng(Arg2))
#             elif (select_variable_2 == 'ReduceConsumptionByRejects'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 Arg4 = MdlADOFunctions.fGetRstValDouble(Rst["Arg4"])
#                 self.ReduceConsumptionByRejects(CLng(Arg1), CLng(Arg2), CLng(Arg3), CDbl(Arg4))
#             elif (select_variable_2 == 'ActivateLocationOnChannelSplit'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 Arg4 = MdlADOFunctions.fGetRstValLong(Rst["Arg4"])
#                 self.ActivateLocationOnChannelSplit(MdlADOFunctions.fGetRstValLong(Arg1), MdlADOFunctions.fGetRstValLong(Arg2), MdlADOFunctions.fGetRstValLong(Arg3), MdlADOFunctions.fGetRstValLong(Arg4))
#             elif (select_variable_2 == 'LinkLocationToChannelSplit'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
#                     GoTo(line1)
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 Arg4 = MdlADOFunctions.fGetRstValLong(Rst["Arg4"])
#                 self.LinkLocationToChannelSplit(MdlADOFunctions.fGetRstValLong(Arg1), MdlADOFunctions.fGetRstValLong(Arg2), MdlADOFunctions.fGetRstValLong(Arg3), MdlADOFunctions.fGetRstValLong(Arg4))
#             elif (select_variable_2 == 'SetMachineFieldLValue'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = '' + Rst["Arg2"]
#                 Arg3 = '' + Rst["Arg3"]
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.SetMachineFieldLValue(CLng(Arg1), str(Arg2), MdlADOFunctions.fGetRstValDouble(Arg3))
#                 RecalcMachine = False
#                 MachineID = CLng(Arg1)
#             elif (select_variable_2 == 'SetMachineFieldHValue'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = '' + Rst["Arg2"]
#                 Arg3 = '' + Rst["Arg3"]
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.SetMachineFieldHValue(CLng(Arg1), str(Arg2), MdlADOFunctions.fGetRstValDouble(Arg3))
#                 RecalcMachine = False
#                 MachineID = CLng(Arg1)
#             elif (select_variable_2 == 'WareHouseLocationActiveBatchRemove'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.WareHouseLocationActiveBatchRemove(CLng(Arg1), str(Arg2))
#             elif (select_variable_2 == 'CreateActivePallet'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.CreateActivePallet(CLng(Arg1), str(Arg2))
#             elif (select_variable_2 == 'CloseActivePallet'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
                
#                 ActionOK = self.CloseActivePallet(CLng(Arg1))
#             elif (select_variable_2 == 'UpdateInventoryItemParams'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 ActionOK = self.UpdateInventoryItemParams(CLng(Arg1))
#             elif (select_variable_2 == 'RunSPCAnalysisOnQCReport'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 Arg4 = MdlADOFunctions.fGetRstValDouble(Rst["Arg4"])
                
                
                
                
                
                
                
#                 if not ( self.SCID == CLng(Arg1) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
#                 Rst.Delete(adAffectCurrent)
#                 ActionOK = self.RunSPCAnalysisOnQCReport(CLng(Arg2), CLng(Arg3), fGetRstValString(Arg4))
#             elif (select_variable_2 == 'UpdateMachineProductionMode'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
#                 ActionOK = self.UpdateMachineProductionMode(CLng(Arg1), CLng(Arg2))
#             elif (select_variable_2 == 'SplitActiveEvent'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = MdlADOFunctions.fGetRstValLong(Rst["Arg2"])
#                 Arg3 = MdlADOFunctions.fGetRstValLong(Rst["Arg3"])
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
#                 ActionOK = self.SplitActiveEvent(CLng(Arg1), CLng(Arg2), CLng(Arg3))
#             elif (select_variable_2 == 'UpdateMachineActiveCalendarEvent'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
#                 Arg2 = MdlADOFunctions.fGetRstValBool(Rst["Arg2"], False)
#                 if not ( self.SCID == fGetShiftCalendarIDByMachine(CLng(Arg1)) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
#                 ActionOK = self.UpdateMachineActiveCalendarEvent(CLng(Arg1), CBool(Arg2))
#             elif (select_variable_2 == 'CloseRealTime'):
#                 Arg1 = MdlADOFunctions.fGetRstValLong(Rst["Arg1"])
                
#                 if not ( self.SCID == CLng(Arg1) and self.SCID != 0 ) :
                    
#                     GoTo(line1)
#                 Rst.Delete(adAffectCurrent)
                
#                 frmMain.CloseNext = True
                
                
                
                
                
                
                
                
                
                
#             Rst.Delete(adAffectCurrent)
            
#             Rst.MoveNext()
#         Rst.Close()
#         if RecalcMachine == True:
#             tMachine = self.mMachines.Item(str(MachineID))
#             tMachine.fReadMainData(VBGetMissingArgument(tMachine.fReadMainData, 0), True, tmpIngnoreCycleTimeFilter)
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             RecordError('Server:RunWebAction', str(Err.Number), Err.Description, 'FuncName: ' + FuncName)
#             Err.Clear()
            
#         if Rst.State != 0:
#             Rst.Close()
#         Rst = None
#         return fn_return_value

#     def fCloseEvents(self, EventGroup, EventID, NewShiftID):
#         Counter = 0

#         CsID = 0

#         tMachine = Machine()

#         tChildJob = Job()

#         tVariant = Variant()
        
        
#         for Counter in range(1, self.mMachines.Count):
#             tMachine = self.mMachines.Item(Counter)
#             CsID = tMachine.ControllerID
#             if not tMachine.ActiveJob is None:
#                 if tMachine.NewJob == True:
#                     if tMachine.SetupEventIDOnShiftEnd == 1:
#                         if not tMachine.ActiveJob.OpenEvent is None:
#                             tMachine.ActiveJob.OpenEvent.CloseAndCreateForNewShift(NewShiftID, False)
#                             if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
#                                 for tVariant in tMachine.ActiveJob.PConfigJobs:
#                                     tChildJob = tVariant
#                                     tChildJob.OpenEvent.CloseAndCreateForNewShift(NewShiftID, False)
#                     else:
#                         if not tMachine.ActiveJob.OpenEvent is None:
#                             tMachine.ActiveJob.OpenEvent.CloseAndCreateForNewShift(NewShiftID, True)
#                             if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
#                                 for tVariant in tMachine.ActiveJob.PConfigJobs:
#                                     tChildJob = tVariant
#                                     tChildJob.OpenEvent.CloseAndCreateForNewShift(NewShiftID, True)
#                 else:
#                     if not tMachine.ActiveJob.OpenEvent is None:
#                         tMachine.ActiveJob.OpenEvent.CloseAndCreateForNewShift(NewShiftID, True)
#                         if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
#                             for tVariant in tMachine.ActiveJob.PConfigJobs:
#                                 tChildJob = tVariant
#                                 tChildJob.OpenEvent.CloseAndCreateForNewShift(NewShiftID, True)
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def fClearAlarms(self, ShiftCalendarID):
#         strSQL = ''

#         tVariant = Variant()

#         tMachine = Machine()

#         tVarAlarm = Variant()

#         tAlarm = Alarm()

#         tControlParam = ControlParam()
        
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblEvent SET AlarmDismissed = 1' + '\r\n'
#         strSQL = strSQL + 'WHERE ID IN(' + '\r\n'
#         strSQL = strSQL + 'SELECT EventID FROM TblAlarms WHERE EventID <> 0 AND ShiftID IN '
#         strSQL = strSQL + '(SELECT ID From TblShift Where ShiftCalendarID = ' + ShiftCalendarID + ')'
#         strSQL = strSQL + ')'
#         CN.Execute(strSQL)
#         strSQL = 'DELETE From TblAlarms'
#         strSQL = strSQL + ' WHERE ShiftID IN '
#         strSQL = strSQL + '(SELECT ID From TblShift Where ShiftCalendarID = ' + ShiftCalendarID + ')'
#         CN.Execute(strSQL)
        
#         for tVariant in self.mMachines:
#             tMachine = tVariant
#             tMachine.AlarmsOnCount = 0
#             if not tMachine.ActiveJob is None:
#                 if not tMachine.ActiveJob.OpenAlarms.Count == 0:
#                     for tVarAlarm in tMachine.ActiveJob.OpenAlarms:
#                         tAlarm = tVarAlarm
#                         tAlarm.Delete
#                         tMachine.ActiveJob.OpenAlarms.Remove(str(tAlarm.ID))
                    
#                     for tControlParam in tMachine.CParams:
#                         if tControlParam.ErrorAlarmActive:
#                             if not tControlParam.Alarms is None:
#                                 for tVarAlarm in tControlParam.Alarms:
#                                     tAlarm = tVarAlarm
#                                     tControlParam.Alarms.Remove(str(tAlarm.ID))
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             RecordError('SERVER:fClearAlarms', str(Err.Number), Err.Description, 'ShiftCalendarID = ' + ShiftCalendarID)
#             Err.Clear()
#         tVariant = None
#         tMachine = None
#         tAlarm = None
#         tVarAlarm = None
#         return fn_return_value

#     def MachineJobDetailsCalc(self, pMachineID, pJobID, pCalcDuration=0, pCalcMat=0, pLiveCalc=0):
#         tMachine = Machine()

#         tCalcTimes = False

#         tCalcMaterial = False

#         tJob = Job()

#         tVariant = Variant()

#         tChildJob = Job()

#         tJobFound = False
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
        
        
        
        
        
        
#         tCalcTimes = True
        
#         if pCalcMat != 0:
#             tCalcMaterial = True
#         else:
#             tCalcMaterial = False
        
#         if not tMachine.ActiveJob is None:
#             if tMachine.ActiveJob.ID == pJobID:
#                 if tMachine.IsOffline == False:
#                     if tCalcMaterial == True:
#                         tMachine.ActiveJob.ControllerChannels = Collection()
#                         tMachine.ActiveJob.InitControllerChannels(0, False)
#                     tMachine.ActiveJob.DetailsCalc(tCalcTimes, tCalcMaterial)
#             elif not tMachine.ActiveJob.PConfigJobs is None:
#                 for tVariant in tMachine.ActiveJob.PConfigJobs:
#                     tChildJob = tVariant
#                     if tChildJob.ID == pJobID:
#                         if tCalcMaterial == True:
#                             tChildJob.ControllerChannels = Collection()
#                             tChildJob.InitControllerChannels(0, False)
#                         tChildJob.DetailsCalc(tCalcTimes, tCalcMaterial)
#                         tJobFound = True
#                 if tJobFound == False:
#                     GoTo(LoadAndCalc)
#             else:
#                 GoTo(LoadAndCalc)
#         else:
#             tJob = Job()
#             tJob.Init(tMachine, pJobID, False)
#             tJob.InitControllerChannels(0, False)
#             tJob.DetailsCalc(tCalcTimes, tCalcMaterial)
#             tJob.RunValidations(EndOfJob)
#             tJob.Update
#             tJob.Terminate
#             tJob = None
#         fn_return_value = True
#         if Err.Number != 0:
#             Err.Clear()
#         tMachine = None
#         tJob = None
#         tChildJob = None
#         return fn_return_value

#     def MachineJoshDetailsCalc(self, pMachineID, pJoshID, pCalcDuration=0, pCalcMat=0, pLiveCalc=0):
#         tMachine = Machine()

#         tShiftID = 0

#         JobID = 0

#         tCalcDuration = False

#         tCalcMaterial = False

#         tJob = Job()

#         tJosh = Josh()

#         tJobID = 0
        
        
        
        
        
        
#         tCalcDuration = True
        
#         if pCalcMat != 0:
#             tCalcMaterial = True
#         else:
#             tCalcMaterial = False
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
#         tShiftID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ShiftID', 'TblJosh', 'ID = ' + pJoshID, 'CN'))
#         if not tMachine.ActiveJob is None:
#             if not tMachine.ActiveJob.ActiveJosh is None:
#                 if tMachine.ActiveJob.ActiveJosh.ID == pJoshID:
#                     if tMachine.IsOffline == False:
#                         tMachine.ActiveJob.ActiveJosh.DetailsCalc(tCalcDuration, tCalcMaterial)
#                 else:
#                     GoTo(LoadAndCalc)
#             else:
#                 GoTo(LoadAndCalc)
#         else:
#             tJobID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('JobID', 'TblJosh', 'ID = ' + pJoshID))
#             tJob = Job()
#             tJob.Init(tMachine, tJobID, False)
#             tJob.InitControllerChannels(pJoshID, False)
#             tJosh = Josh()
#             tJosh.Init(tJob, pJoshID)
#             tJosh.DetailsCalc(tCalcDuration, tCalcMaterial)
#             tJosh.RunValidations(EndOfJosh)
#             tJosh.Update
#             tJosh.Job = None
#             tJob.Terminate
#         fn_return_value = True
#         if Err.Number != 0:
#             Err.Clear()
#         tMachine = None
#         tJob = None
#         tJosh = None
#         return fn_return_value

#     def fUpdateControllerFieldsParam(self, pCsID, pMachineID):
#         tMachine = Machine()

#         tControlParam = ControlParam()

#         vParam = ControlParam()

#         ParamFound = False

#         rVal = 0
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
#         fn_return_value = tMachine.UpdateControllerFieldsParam(pCsID, pMachineID)
        
#         return fn_return_value

#     def ResetMachineByID(self, pMachineID):
#         tMachine = Machine()
        
#         fn_return_value = False
#         for tMachine in self.mMachines:
#             if tMachine.ID == pMachineID:
#                 if tMachine.ResetMachineTotalFields == False:
#                     raise(1)
#                 fn_return_value = True
#                 break
#         if Err.Number != 0:
#             RecordError('ResetMachineByID', Err.Number, Err.Description, 'MachineID = ' + pMachineID)
#         return fn_return_value

#     def DownloadMachineQueue(self, MachineID):
#         tMachine = Machine()
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(MachineID))
#         tMachine.SaveJobsQueue
#         fn_return_value = True
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def fRefreshSettings(self):
#         tSystemVariables = self.SystemVariables()
        
        
#         self.SystemVariables = None
#         tSystemVariables = self.SystemVariables()
#         tSystemVariables.Init
#         self.SystemVariables = tSystemVariables
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def ReInitMachine(self, MachineID):
#         strSQL = ''

#         Rst = None

#         tMachine = Machine()

#         ServerName = ''

#         tOPCServer = OPCServer()
        
#         fn_return_value = False
        
#         if not ( self.mMachines.Item(str(MachineID)) is None ) :
#             self.mMachines.Remove(( str(MachineID) ))
#         else:
#             raise(1)
        
#         strSQL = 'Select OPCServerName,OPCServerIP,ID From TblMachines Where ID = ' + MachineID
#         RstData = Rst.SelectAllData(strSQL)
#         Rst.ActiveConnection = None
#         if Rst.RecordCount == 1:
#             tMachine = Machine()
            
#             tMachine.Server = self
#             ServerName = '' + Rst["OPCServerName"]
#             if ServerName != '':
#                 tOPCServer = OPCServer()
#                 self.mOPCServers.Add(tOPCServer, str(Rst["ID"]))
#                 tOPCServer.Connect(ServerName, '' + Rst["OPCServerIP"])
#                 self.mOPCServerGroups = self.mOPCServer.OPCGroups
#             else:
#                 tOPCServer = self.mOPCServer
#             if tMachine.INITMachine(Rst["ID"], tOPCServer) == False:
                
#                 pass
#             self.mMachines.Add(tMachine, str(Rst["ID"]))
#         Rst.Close()
#         fn_return_value = True
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#         Rst = None
#         return fn_return_value

#     def UpdateJobUnitsReportedOK(self, pMachineID, pJobID, pUnitsReportedOK):
#         tMachine = Machine()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not tMachine.ActiveJob is None:
#             if tMachine.ActiveJob.ID == pJobID:
#                 tMachine.ActiveJob.UnitsReportedOK = pUnitsReportedOK
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def UpdateJoshUnitsReportedOK(self, pMachineID, pJoshID, pUnitsReportedOK):
#         tMachine = Machine()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not tMachine.ActiveJob is None:
#             if not tMachine.ActiveJob.ActiveJosh is None:
#                 if tMachine.ActiveJob.ActiveJosh.ID == pJoshID:
#                     tMachine.ActiveJob.ActiveJosh.UnitsReportedOK = pUnitsReportedOK
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def CleanUnusedObjects(self):
#         tVariant = Variant()

#         tProduct = Product()

#         tMachine = Machine()

#         tMold = Mold()

#         tFound = False

#         tVariant2 = Variant()

#         strSQL = ''
        
#         fn_return_value = False
#         for tVariant in self.Products:
#             tFound = False
#             tProduct = tVariant
#             for tVariant2 in self.Machines:
#                 tMachine = tVariant2
#                 if not tMachine.ActiveJob is None:
#                     if tMachine.ActiveJob.Product.ID == tProduct.ID:
#                         tFound = True
#                         break
#             if not tFound:
#                 self.Products.Remove(str(tProduct.ID))
#         for tVariant in self.Molds:
#             tFound = False
#             tMold = tVariant
#             for tVariant2 in self.Machines:
#                 tMachine = tVariant2
#                 if not tMachine.ActiveJob is None:
#                     if tMachine.ActiveJob.Mold.ID == tMold.ID:
#                         tFound = True
#                         break
#             if not tFound:
#                 self.Molds.Remove(str(tMold.ID))
        
#         strSQL = 'DELETE STblUtilizationLogs WHERE (LogTime <= mdl_Common.DateAdd(DD, -180, GETDATE()))'
#         CN.Execute(strSQL)
#         fn_return_value = True
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()
#         return fn_return_value

#     def UpdateMoldEndTime(self, pMachineID):
#         tMachine = Machine()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not tMachine.ActiveJob is None:
#             tMachine.ActiveJob.InitMoldChangeDetails
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

    def fClearAlarmsOnServerINIT(self, pShiftCalendarID):        
        strSQL = ''
        try:
            strSQL = strSQL + 'UPDATE TblEvent SET AlarmDismissed = 1' + '\r\n'
            strSQL = strSQL + 'WHERE ID IN(' + '\r\n'
            strSQL = strSQL + 'SELECT EventID FROM TblAlarms WHERE EventID <> 0 AND MachineID IN'
            strSQL = strSQL + '('
            strSQL = strSQL + 'SELECT ID FROM TblMachines WHERE Department IN'
            strSQL = strSQL + '('
            strSQL = strSQL + 'SELECT ID FROM STblDepartments WHERE ShiftCalendarID = ' + str(pShiftCalendarID)
            strSQL = strSQL + ')'
            strSQL = strSQL + ')'
            strSQL = strSQL + ')'
            MdlConnection.CN.execute(strSQL)

            strSQL = 'DELETE TblAlarms WHERE MachineID IN'
            strSQL = strSQL + '('
            strSQL = strSQL + 'SELECT ID FROM TblMachines WHERE Department IN'
            strSQL = strSQL + '('
            strSQL = strSQL + 'SELECT ID FROM STblDepartments WHERE ShiftCalendarID = ' + str(pShiftCalendarID)
            strSQL = strSQL + ')'
            strSQL = strSQL + ')'
            MdlConnection.CN.execute(strSQL)

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)


#     def UpdateMachineUnitsTarget(self, pMachineID, pJobID, pUnitsTarget):
#         tMachine = Machine()

#         tVariant = Variant()

#         tChildJob = Job()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not tMachine.ActiveJob is None:
#             if tMachine.ActiveJob.ID == pJobID:
#                 tMachine.ActiveJob.UnitsTarget = pUnitsTarget
#             else:
#                 if not tMachine.ActiveJob.PConfigJobs is None:
#                     for tVariant in tMachine.ActiveJob.PConfigJobs:
#                         tChildJob = tVariant
#                         if tChildJob.ID == pJobID:
#                             tChildJob.UnitsTarget = pUnitsTarget
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def UpdateMachineOpenEvent(self, pMachineID, pJobID, pEventID, pEventGroupID, pEventReasonID):
#         tMachine = Machine()

#         tVariant = Variant()

#         tChildJob = Job()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not tMachine.ActiveJob is None:
#             if tMachine.ActiveJob.ID == pJobID:
#                 if not tMachine.ActiveJob.OpenEvent is None:
#                     if tMachine.ActiveJob.OpenEvent.ID == pEventID:
#                         tMachine.ActiveJob.OpenEvent.Refresh(pEventGroupID, pEventReasonID)
                        
#                         if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
#                             for tVariant in tMachine.ActiveJob.PConfigJobs:
#                                 tChildJob = tVariant
#                                 tChildJob.OpenEvent.Refresh(pEventGroupID, pEventReasonID)
#             else:
#                 if not tMachine.ActiveJob.PConfigJobs is None:
#                     for tVariant in tMachine.ActiveJob.PConfigJobs:
#                         tChildJob = tVariant
#                         if tChildJob.ID == pJobID:
#                             if not tChildJob.OpenEvent is None:
#                                 if tChildJob.OpenEvent.ID == pEventID:
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def ClosePreviousShifts(self):
#         strSQL = ''

#         Rst = None

#         tStartTime = Date()

#         tEndTime = Date()
        
        
#         if self.CurrentShiftID != 0:
#             strSQL = 'SELECT ID,EndTime FROM TblShift WHERE EndTime IS NULL AND ID < ' + self.CurrentShiftID + ' AND ShiftCalendarID = ' + self.SCID
#             RstData = Rst.SelectAllData(strSQL)
#             while not RstData.EOF:
#                 tStartTime = MdlADOFunctions.GetSingleValue('TOP 1 StartTime', 'TblShift', 'ShiftCalendarID = ' + self.SCID + ' AND ID > ' + RstData.ID + ' ORDER BY ID')
#                 if tStartTime != 0:
#                     RstData.EndTime = tStartTime
#                     RstData.Update()
#                 RstData.MoveNext()
#             RstData.Close()
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()
#         RstData = None
#         return fn_return_value

#     def StartMachineMaterialFlow(self, pMachineID, pJobID):
#         tMachine = Machine()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not ( tMachine is None ) :
#             if tMachine.ActiveJob.ID == pJobID:
#                 tMachine.ActiveJob.NextJobMaterialFlowStart = mdl_Common.NowGMT
#                 tMachine.StartMaterialFlow(tMachine.ActiveJob)
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def AddMaterialFlowFromLastJob(self, pMachineID, pJobID):
#         tMachine = Machine()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not ( tMachine is None ) :
#             if tMachine.ActiveJob.ID == pJobID:
#                 tMachine.ActiveJob.AddMaterialFlowFromLastJob
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def ReduceConsumptionByRejects(self, pMachineID, pJobID, pJoshID, pRejectsAmount):
#         tMachine = Machine()

#         tChannel = Channel()

#         tSplit = ChannelSplit()

#         tVariant = Variant()

#         tVariant2 = Variant()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not ( tMachine is None ) :
#             if tMachine.ActiveJob.ID == pJobID:
#                 for tVariant in tMachine.ActiveJob.ControllerChannels:
#                     tChannel = tVariant
#                     if tChannel.SplitsCounter > 0:
#                         for tVariant2 in tChannel.Splits:
#                             tSplit = tVariant2
#                             ReduceSplitAmountByRejects(tMachine.ActiveJob, tSplit, pRejectsAmount, FromJob)
#                             if pJoshID != 0:
#                                 ReduceSplitAmountByRejects(tMachine.ActiveJob, tSplit, pRejectsAmount, FromJosh)
#                     else:
#                         ReduceChannelAmountByRejects(tMachine.ActiveJob, tChannel, pRejectsAmount, FromJob)
#                         if pJoshID != 0:
#                             ReduceChannelAmountByRejects(tMachine.ActiveJob, tChannel, pRejectsAmount, FromJosh)
#         if Err.Number != 0:
#             Err.Clear()
#         tMachine = None
#         tChannel = None
#         tSplit = None
#         tVariant = None
#         tVariant2 = None
#         return fn_return_value

#     def LoadRefControllerFields(self):
#         strSQL = ''

#         Rst = None

#         tMachine = Machine()

#         tRefMachine = Machine()

#         tRefMachineID = 0

#         tControlParam = ControlParam()

#         tRefControlParam = ControlParam()

#         tRefFieldName = ''

#         tFieldName = ''
        
#         strSQL = ''
#         strSQL = strSQL + 'SELECT TblControllerFields.MachineID AS MachineID,' + '\r\n'
#         strSQL = strSQL + '    TblControllerFields.FieldName AS FieldName,' + '\r\n'
#         strSQL = strSQL + '    TblControllerFields.RefReadControllerField AS RefReadControllerField,' + '\r\n'
#         strSQL = strSQL + '    TblControllerFields.RefWriteControllerField AS RefWriteControllerField' + '\r\n'
#         strSQL = strSQL + 'FROM TblControllerFields' + '\r\n'
#         strSQL = strSQL + '     INNER JOIN TblMachines ON TblControllerFields.MachineID = TblMachines.ID' + '\r\n'
#         strSQL = strSQL + '     INNER JOIN STblDepartments ON TblMachines.Department = STblDepartments.ID' + '\r\n'
#         strSQL = strSQL + '     INNER JOIN STblShiftCalendar ON STblDepartments.ShiftCalendarID = STblShiftCalendar.ID' + '\r\n'
#         strSQL = strSQL + 'WHERE (TblMachines.IsActive <> 0)' + '\r\n'
#         strSQL = strSQL + '    AND (TblControllerFields.ControllerFieldTypeID = 2)' + '\r\n'
#         strSQL = strSQL + '    AND (' + '\r\n'
#         strSQL = strSQL + '        NOT TblControllerFields.RefReadControllerField IS NULL' + '\r\n'
#         strSQL = strSQL + '        OR NOT TblControllerFields.RefWriteControllerField IS NULL' + '\r\n'
#         strSQL = strSQL + '        )' + '\r\n'
#         strSQL = strSQL + '    AND STblShiftCalendar.ID = ' + self.SCID + '\r\n'
#         strSQL = strSQL + 'ORDER BY MachineID' + '\r\n'
#         RstData = Rst.SelectAllData(strSQL)
#         Rst.ActiveConnection = None
#         while not Rst.EOF:
#             tMachine = self.Machines.Item(str(Rst["MachineID"]))
#             tFieldName = fGetRstValString(Rst["FieldName"])
#             if fGetRstValString(Rst["RefReadControllerField"]) != '':
#                 tRefMachineID = GetRefMachineIDForRefControllerField(fGetRstValString(Rst["RefReadControllerField"]))
#                 if tRefMachineID != 0:
#                     tRefMachine = self.Machines.Item(str(tRefMachineID))
#                     if not tRefMachine is None:
#                         tRefFieldName = GetRefFieldNameForRefControllerField(Rst["RefReadControllerField"])
#                         if tRefFieldName != '':
#                             if tRefMachine.GetParam(tRefFieldName, tRefControlParam) == True:
#                                 if tMachine.GetParam(tFieldName, tControlParam) == True:
#                                     tControlParam.RefReadControllerField = tRefControlParam
#                             else:
#                                 RecordError('Server.LoadRefControllerFields', 1, 'ControllerField not found!', 'RefMachineID: ' + tRefMachineID + '. RefFieldName: ' + tRefFieldName)
#                     else:
#                         RecordError('Server.LoadRefControllerFields', 1, 'Machine not found!', 'RefMachineID: ' + tRefMachineID)
#             if fGetRstValString(Rst["RefWriteControllerField"]) != '':
#                 tRefMachineID = GetRefMachineIDForRefControllerField(fGetRstValString(Rst["RefWriteControllerField"]))
#                 if tRefMachineID != 0:
#                     tRefMachine = self.Machines.Item(str(tRefMachineID))
#                     if not tRefMachine is None:
#                         tRefFieldName = GetRefFieldNameForRefControllerField(Rst["RefWriteControllerField"])
#                         if tRefFieldName != '':
#                             if tRefMachine.GetParam(tRefFieldName, tRefControlParam) == True:
#                                 if tMachine.GetParam(tFieldName, tControlParam) == True:
#                                     tControlParam.RefWriteControllerField = tRefControlParam
#                             else:
#                                 RecordError('Server.LoadRefControllerFields', 1, 'ControllerField not found!', 'RefMachineID: ' + tRefMachineID + '. RefFieldName: ' + tRefFieldName)
#                     else:
#                         RecordError('Server.LoadRefControllerFields', 1, 'Machine not found!', 'RefMachineID: ' + tRefMachineID)
#             Rst.MoveNext()
#         Rst.Close()
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             RecordError('Server.LoadRefControllerFields', Err.Number, Err.Description, '')
#             Err.Clear()
            
#         tMachine = None
#         Rst = None

#     def ActivateLocationOnChannelSplit(self, pMachineID, pChannelNum, pSplitNum, pLocationID):
#         tMachine = Machine()

#         tChannel = Channel()

#         tSplit = ChannelSplit()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not ( tMachine.ActiveJob is None ) :
#             tChannel = tMachine.ActiveJob.ControllerChannels.Item(str(pChannelNum))
#             if pSplitNum != 0:
#                 tSplit = tChannel.Splits.Item(str(pSplitNum))
#                 if tSplit.WareHouseLocationID == pLocationID:
#                     tSplit.PerformActivationForLocationBatch
#             else:
#                 if tChannel.WareHouseLocationID == pLocationID:
#                     tChannel.PerformActivationForLocationBatch
#         if Err.Number != 0:
#             Err.Clear()
#         tMachine = None
#         tChannel = None
#         tSplit = None
#         return fn_return_value

#     def LinkLocationToChannelSplit(self, pMachineID, pChannelNum, pSplitNum, pLocationID):
#         tMachine = Machine()

#         tChannel = Channel()

#         tSplit = ChannelSplit()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not ( tMachine.ActiveJob is None ) :
#             tChannel = tMachine.ActiveJob.ControllerChannels.Item(str(pChannelNum))
#             if pSplitNum != 0:
#                 tSplit = tChannel.Splits.Item(str(pSplitNum))
#                 tSplit.SetWareHouseLocationID(pLocationID)
#             else:
#                 tChannel.SetWareHouseLocationID(pLocationID)
#         if Err.Number != 0:
#             Err.Clear()
#         tMachine = None
#         tChannel = None
#         tSplit = None
#         return fn_return_value

#     def ClearUserMessages(self):
#         strSQL = ''

#         Rst = None

#         RID = 0
        
#         strSQL = 'SELECT TOP 1 ID FROM App_UserMessages ORDER BY ID DESC'
#         Rst.Open(strSQL, MetaCn, adOpenStatic, adLockReadOnly)
#         Rst.ActiveConnection = None
#         RID = Rst["ID"]
#         Rst.Close()
#         if RID > 10000:
#             strSQL = 'DELETE App_UserMessages Where ID < ' +  ( RID - 10000 )
#             MetaCn.Execute(strSQL)
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()

#     def WareHouseLocationActiveBatchRemove(self, pMachineID, pWareHouseLocationID):
#         tMachine = Machine()

#         tChannel = Channel()

#         tSplit = ChannelSplit()

#         tVariant = Variant()

#         tVariant2 = Variant()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if not ( tMachine.ActiveJob is None ) :
#             for tVariant in tMachine.ActiveJob.ControllerChannels:
#                 tChannel = tVariant
#                 if tChannel.WareHouseLocationID == pWareHouseLocationID:
#                     tChannel.PerformActivationForLocationBatch
#                 for tVariant2 in tChannel.Splits:
#                     tSplit = tVariant2
#                     if tSplit.WareHouseLocationID == pWareHouseLocationID:
#                         tSplit.PerformActivationForLocationBatch
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def CreateActivePallet(self, pMachineID, pActivePalletInventoryID):
#         tMachine = Machine()

#         tChannel = Channel()

#         tSplit = ChannelSplit()

#         tVariant = Variant()

#         tVariant2 = Variant()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         tMachine.ActivePalletInventoryID = pActivePalletInventoryID
#         tMachine.FireEventTriggeredTasks(5)
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def CloseActivePallet(self, pMachineID):
#         tMachine = Machine()

#         tChannel = Channel()

#         tSplit = ChannelSplit()

#         tVariant = Variant()

#         tVariant2 = Variant()
        
#         tMachine = self.mMachines.Item(str(pMachineID))
#         tMachine.ActivePalletInventoryID = 0
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def UpdateInventoryItemParams(self, pInventoryID):
#         tVar = Variant()

#         tMaterialBatch = MaterialBatch()
        
#         fn_return_value = False
#         for tVar in self.ActiveInventoryItems:
#             tMaterialBatch = tVar
#             if tMaterialBatch.ID == pInventoryID:
#                 tMaterialBatch.Refresh
#         fn_return_value = True
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def RunSPCAnalysisOnQCReport(self, RID, UserID, SessionID):
#         tMachine = Machine()

#         tVariant = Variant()

#         tVariant2 = Variant()

#         tQC = QC()
        
#         tQC.Init(UserID, RID)
        
#         tQC.CollectSPCDatafromTests(RID, UserID, SessionID)
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def UpdateMachineProductionMode(self, pMachineID, pProductionModeID):
#         tMachine = Machine()

#         strSQL = ''

#         PRst = None
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
#         if pProductionModeID == 0:
#             pProductionModeID = 1
#         tMachine.ProductionModeID = pProductionModeID
        
        
        
#         strSQL = 'SELECT * FROM STblProductionModes WHERE ID = ' + tMachine.ProductionModeID
#         PRst.Open(strSQL, CN, adOpenStatic, adLockReadOnly)
#         PRst.ActiveConnection = None
#         if PRst.RecordCount == 1:
#             tMachine.ProductionModeReasonID = MdlADOFunctions.fGetRstValLong(PRst["EventReasonID"])
#             tMachine.ProductionModeGroupReasonID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('EventGroupID', 'STblEventDesr', 'ID = ' + tMachine.ProductionModeReasonID))
#             tMachine.ProductionModeDisableProductionTime = MdlADOFunctions.fGetRstValBool(PRst["DisableProductionTime"], False)
#             tMachine.ProductionModeCalcEfficiencies = MdlADOFunctions.fGetRstValBool(PRst["CalcEfficiencies"], False)
#             tMachine.ProductionModeOverCalendarEvent = MdlADOFunctions.fGetRstValBool(PRst["OverCalendarEvent"], True)
#         PRst.Close()
#         fn_return_value = True
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()
#         if PRst.State != 0:
#             PRst.Close()
#         PRst = None
#         return fn_return_value

#     def SplitActiveEvent(self, pMachineID, pNewShiftID=0, pEventID=0, pRootEventID=0, FromSplit=True):
#         Counter = 0

#         CsID = 0

#         tMachine = Machine()

#         tChildJob = Job()

#         tVariant = Variant()

#         strSQL = ''

#         tOldEventID = 0
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
        
#         if pNewShiftID == 0:
#             pNewShiftID = self.CurrentShiftID
#         if not tMachine.ActiveJob is None:
#             if tMachine.NewJob == True:
#                 if tMachine.SetupEventIDOnShiftEnd == 1:
#                     if not tMachine.ActiveJob.OpenEvent is None:
#                         if pEventID != 0 and tMachine.ActiveJob.OpenEvent.ID != pEventID:
#                             return fn_return_value
#                         tMachine.ActiveJob.OpenEvent.CloseAndCreateForNewShift(pNewShiftID, False, pRootEventID)
                        
#                         if tMachine.ActiveJob.OpenEvent.ID != pEventID and FromSplit:
#                             strSQL = 'UPDATE TblEvent SET OriginalEVID = ' + pEventID + ' WHERE ID = ' + tMachine.ActiveJob.OpenEvent.ID
#                             CN.Execute(( strSQL ))
#                             strSQL = 'UPDATE TblEvent SET IsParent = 1 WHERE ID = ' + pEventID
#                             CN.Execute(( strSQL ))
#                         if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
#                             for tVariant in tMachine.ActiveJob.PConfigJobs:
#                                 tChildJob = tVariant
#                                 if not tChildJob.OpenEvent is None:
#                                     tOldEventID = tChildJob.OpenEvent.ID
#                                     tChildJob.OpenEvent.CloseAndCreateForNewShift(pNewShiftID, False, pRootEventID)
                                    
#                                     if tChildJob.OpenEvent.ID != tOldEventID and FromSplit:
#                                         strSQL = 'UPDATE TblEvent SET OriginalEVID = ' + tOldEventID + ' WHERE ID = ' + tChildJob.OpenEvent.ID
#                                         CN.Execute(( strSQL ))
#                                         strSQL = 'UPDATE TblEvent SET IsParent = 1 WHERE ID = ' + tOldEventID
#                                         CN.Execute(( strSQL ))
#                 else:
#                     if not tMachine.ActiveJob.OpenEvent is None:
#                         if pEventID != 0 and tMachine.ActiveJob.OpenEvent.ID != pEventID:
#                             return fn_return_value
#                         tMachine.ActiveJob.OpenEvent.CloseAndCreateForNewShift(pNewShiftID, True, pRootEventID)
                        
#                         if tMachine.ActiveJob.OpenEvent.ID != pEventID and FromSplit:
#                             strSQL = 'UPDATE TblEvent SET OriginalEVID = ' + pEventID + ' WHERE ID = ' + tMachine.ActiveJob.OpenEvent.ID
#                             CN.Execute(( strSQL ))
#                             strSQL = 'UPDATE TblEvent SET IsParent = 1 WHERE ID = ' + pEventID
#                             CN.Execute(( strSQL ))
#                         if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
#                             for tVariant in tMachine.ActiveJob.PConfigJobs:
#                                 tChildJob = tVariant
#                                 if not tChildJob.OpenEvent is None:
#                                     tOldEventID = tChildJob.OpenEvent.ID
#                                     tChildJob.OpenEvent.CloseAndCreateForNewShift(pNewShiftID, True, pRootEventID)
                                    
#                                     if tChildJob.OpenEvent.ID != tOldEventID and FromSplit:
#                                         strSQL = 'UPDATE TblEvent SET OriginalEVID = ' + tOldEventID + ' WHERE ID = ' + tChildJob.OpenEvent.ID
#                                         CN.Execute(( strSQL ))
#                                         strSQL = 'UPDATE TblEvent SET IsParent = 1 WHERE ID = ' + tOldEventID
#                                         CN.Execute(( strSQL ))
#             else:
#                 if not tMachine.ActiveJob.OpenEvent is None:
#                     if pEventID != 0 and tMachine.ActiveJob.OpenEvent.ID != pEventID:
#                         return fn_return_value
#                     tMachine.ActiveJob.OpenEvent.CloseAndCreateForNewShift(pNewShiftID, True, pRootEventID)
                    
#                     if tMachine.ActiveJob.OpenEvent.ID != pEventID and FromSplit:
#                         strSQL = 'UPDATE TblEvent SET OriginalEVID = ' + pEventID + ' WHERE ID = ' + tMachine.ActiveJob.OpenEvent.ID
#                         CN.Execute(( strSQL ))
#                         strSQL = 'UPDATE TblEvent SET IsParent = 1 WHERE ID = ' + pEventID
#                         CN.Execute(( strSQL ))
#                     if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
#                         for tVariant in tMachine.ActiveJob.PConfigJobs:
#                             tChildJob = tVariant
#                             if not tChildJob.OpenEvent is None:
#                                 tOldEventID = tChildJob.OpenEvent.ID
#                                 tChildJob.OpenEvent.CloseAndCreateForNewShift(pNewShiftID, True, pRootEventID)
                                
#                                 if tChildJob.OpenEvent.ID != tOldEventID and FromSplit:
#                                     strSQL = 'UPDATE TblEvent SET OriginalEVID = ' + tOldEventID + ' WHERE ID = ' + tChildJob.OpenEvent.ID
#                                     CN.Execute(( strSQL ))
#                                     strSQL = 'UPDATE TblEvent SET IsParent = 1 WHERE ID = ' + tOldEventID
#                                     CN.Execute(( strSQL ))
#         fn_return_value = True
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()
#         return fn_return_value

#     def ClosePreviousJoshs(self):
#         strSQL = ''
        
#         fn_return_value = False
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblJosh SET EndTime = (SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblJosh.ShiftID), Status = 20,' + '\r\n'
#         strSQL = strSQL + 'DurationMin = DATEDIFF(n,StartTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblJosh.ShiftID))' + '\r\n'
#         strSQL = strSQL + 'WHERE (EndTime IS NULL OR Status = 10) AND ShiftID IN(SELECT ID FROM TblShift WHERE EndTime IS NOT NULL) AND JobID NOT IN(SELECT ID FROM TblJob WHERE Status > 10)'
#         CN.Execute(strSQL)
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblJosh SET EndTime = (CASE WHEN (SELECT TblJob.EndTime FROM TblJob WHERE TblJob.ID = TblJosh.JobID) <= (SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblJosh.ShiftID)' + '\r\n'
#         strSQL = strSQL + 'THEN (SELECT TblJob.EndTime FROM TblJob WHERE TblJob.ID = TblJosh.JobID) ELSE (SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblJosh.ShiftID) END), Status = 20,' + '\r\n'
#         strSQL = strSQL + 'DurationMin = DATEDIFF(n,StartTime,(CASE WHEN (SELECT TblJob.EndTime FROM TblJob WHERE TblJob.ID = TblJosh.JobID) <= (SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblJosh.ShiftID)' + '\r\n'
#         strSQL = strSQL + 'THEN (SELECT TblJob.EndTime FROM TblJob WHERE TblJob.ID = TblJosh.JobID) ELSE (SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblJosh.ShiftID) END))' + '\r\n'
#         strSQL = strSQL + 'WHERE (EndTime IS NULL OR Status = 10) AND ShiftID IN(SELECT ID FROM TblShift WHERE EndTime IS NOT NULL) AND JobID IN(SELECT ID FROM TblJob WHERE Status > 10)'
#         CN.Execute(strSQL)
#         strSQL = ''
#         strSQL = 'UPDATE TblJosh SET EndTime = DATEADD(n,DurationMin,StartTime) WHERE DurationMin IS NOT NULL AND EndTime IS NULL AND SHiftID NOT IN(SELECT ID FROM TblShift WHERE EndTime IS NULL)'
#         CN.Execute(strSQL)
        
#         strSQL = ''
#         strSQL = 'DELETE FROM TblJoshCurrent WHERE ID IN(SELECT ID FROM TblJosh WHERE EndTime IS NOT NULL)'
#         CN.Execute(strSQL)
#         fn_return_value = True
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()
#         return fn_return_value

#     def ClosePreviousEvents(self):
#         strSQL = ''
        
#         fn_return_value = False
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblEvent SET JoshID = (SELECT TOP 1 ID FROM TblJosh WHERE ShiftID = TblEvent.ShiftID AND JobID = TblEvent.JobID)' + '\r\n'
#         strSQL = strSQL + 'WHERE JoshID = 0 AND JobID <> 0 AND ShiftID <> 0'
#         CN.Execute(strSQL)
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblEvent SET ' + '\r\n'
#         strSQL = strSQL + 'EndTime = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEvent.JoshID)) < 0 THEN EventTime ELSE (SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEvent.JoshID) END,' + '\r\n'
#         strSQL = strSQL + 'Duration = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEvent.JoshID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEvent.JoshID)) END,' + '\r\n'
#         strSQL = strSQL + 'DownTime = CASE WHEN (SELECT IsDownTime FROM STblEventDesr WHERE ID = TblEvent.Event) <> 0 THEN CASE WHEN DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEvent.JoshID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEvent.JoshID)) END ELSE 0 END,' + '\r\n'
#         strSQL = strSQL + 'InactiveTime = CASE WHEN (SELECT IsInactiveTime FROM STblEventDesr WHERE ID = TblEvent.Event) <> 0 THEN CASE WHEN DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEvent.JoshID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEvent.JoshID)) END ELSE 0 END' + '\r\n'
#         strSQL = strSQL + 'WHERE EndTime IS NULL AND JoshID IN(SELECT ID FROM TblJosh WHERE EndTime IS NOT NULL)'
#         CN.Execute(strSQL)
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblEvent SET ' + '\r\n'
#         strSQL = strSQL + 'EndTime = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEvent.ShiftID)) < 0 THEN EventTime ELSE (SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEvent.ShiftID) END,' + '\r\n'
#         strSQL = strSQL + 'Duration = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEvent.ShiftID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEvent.ShiftID)) END,' + '\r\n'
#         strSQL = strSQL + 'DownTime = CASE WHEN (SELECT IsDownTime FROM STblEventDesr WHERE ID = TblEvent.Event) <> 0 THEN CASE WHEN DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEvent.ShiftID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEvent.ShiftID)) END ELSE 0 END,' + '\r\n'
#         strSQL = strSQL + 'InactiveTime = CASE WHEN (SELECT IsInactiveTime FROM STblEventDesr WHERE ID = TblEvent.Event) <> 0 THEN CASE WHEN DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEvent.ShiftID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEvent.ShiftID)) END ELSE 0 END' + '\r\n'
#         strSQL = strSQL + 'WHERE EndTime IS NULL AND JoshID = 0'
#         CN.Execute(strSQL)
#         fn_return_value = True
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()
#         return fn_return_value

#     def ClosePreviousWorkingEvents(self):
#         strSQL = ''
        
#         fn_return_value = False
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblWorkingEvents SET JoshID = (SELECT TOP 1 ID FROM TblJosh WHERE ShiftID = TblWorkingEvents.ShiftID AND JobID = TblWorkingEvents.JobID)' + '\r\n'
#         strSQL = strSQL + 'WHERE JoshID = 0 AND JobID <> 0 AND ShiftID <> 0'
#         CN.Execute(strSQL)
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblWorkingEvents SET ' + '\r\n'
#         strSQL = strSQL + 'EndTime = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblWorkingEvents.JoshID)) < 0 THEN EventTime ELSE (SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblWorkingEvents.JoshID) END,' + '\r\n'
#         strSQL = strSQL + 'Duration = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblWorkingEvents.JoshID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblWorkingEvents.JoshID)) END' + '\r\n'
#         strSQL = strSQL + 'WHERE EndTime IS NULL AND JoshID IN(SELECT ID FROM TblJosh WHERE EndTime IS NOT NULL)'
#         CN.Execute(strSQL)
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblWorkingEvents SET ' + '\r\n'
#         strSQL = strSQL + 'EndTime = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblWorkingEvents.ShiftID)) < 0 THEN EventTime ELSE (SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblWorkingEvents.ShiftID) END,' + '\r\n'
#         strSQL = strSQL + 'Duration = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblWorkingEvents.ShiftID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblWorkingEvents.ShiftID)) END' + '\r\n'
#         strSQL = strSQL + 'WHERE EndTime IS NULL AND JoshID = 0'
#         CN.Execute(strSQL)
#         fn_return_value = True
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()
#         return fn_return_value


    def CleanActivateJobWebParams(self):
        strSQL = ''
        try:
            strSQL = 'DELETE FROM STblWebParams WHERE FuncName = \'MachineLoadJob\''
            MdlConnection.CN.execute(strSQL)
            strSQL = 'DELETE FROM STblWebParams WHERE FuncName = \'CloseRealTime\' AND Arg1 = \'' + str(self.SCID) + '\''
            MdlConnection.CN.execute(strSQL)

        except BaseException as error:
            if 'nnection' in error.args[0]:
                if MdlConnection.CN:
                    MdlConnection.Close(MdlConnection.CN)
                MdlConnection.CN = MdlConnection.Open(MdlConnection.strCon)

                if MdlConnection.MetaCn:
                    MdlConnection.Close(MdlConnection.MetaCn)
                MdlConnection.MetaCn = MdlConnection.Open(MdlConnection.strMetaCon)


#     def CompleteMissingShiftsObject(self):
#         strSQL = ''

#         situation = 0

#         NewShiftID = 0

#         OldJoshID = 0

#         JoshID = 0

#         SetupDuration = 0

#         NewJoshID = 0

#         JobID = 0

#         ShiftDefID = 0

#         Counter = 0

#         tMachine = Machine()

#         DepForSC = ''

#         tVariant = Variant()

#         tVariant2 = Variant()

#         tChildJob = Job()

#         tJosh = Josh()
        
#         fn_return_value = False
#         for tVariant in self.Machines:
#             tMachine = tVariant
#             if not tMachine.ActiveJob is None:
                
                
#                 if tMachine.ActiveJob.ActiveJosh.ID == 0:
#                     tMachine.ActiveJoshID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblJoshCurrent', 'JobID = ' + tMachine.ActiveJob.ID + ' AND ShiftID <> ' + self.CurrentShiftID + ' ORDER BY StartTime DESC', 'CN'))
#                     tJosh = Josh()
#                     tJosh.Init(tMachine.ActiveJob, tMachine.ActiveJoshID)
#                     tMachine.ActiveJob.ActiveJosh = tJosh
#                     tMachine.ActiveJobID = tMachine.ActiveJob.ID
#                     tMachine.ActiveJosh = tJosh
#                     tMachine.ActiveJoshID = tMachine.ActiveJosh.ID
#                     if tMachine.ActiveJob.OpenEvent is None:
#                         tMachine.ActiveJob.GetOpenEvent
#                     if not tMachine.ActiveJob.OpenEvent is None:
#                         tMachine.ActiveJob.OpenEvent.Josh = tJosh
#                         tMachine.ActiveJob.OpenEvent.Update
                    
#                     if tMachine.ActiveJob.OpenWorkingEvent is None:
#                         tMachine.ActiveJob.GetOpenWorkingEvent
#                     if not tMachine.ActiveJob.OpenWorkingEvent is None:
#                         tMachine.ActiveJob.OpenWorkingEvent.Josh = tJosh
#                         tMachine.ActiveJob.OpenWorkingEvent.Update
                    
#                     if tMachine.ActiveJob.OpenEngineEvent is None:
#                         tMachine.ActiveJob.GetOpenEngineEvent
#                     if not tMachine.ActiveJob.OpenEngineEvent is None:
#                         tMachine.ActiveJob.OpenEngineEvent.Josh = tJosh
#                         tMachine.ActiveJob.OpenEngineEvent.Update
#                     tMachine.ActiveJob.CreateJoshForNewShift
#                 if tMachine.ActiveJob.PConfigID != 0 and tMachine.ActiveJob.IsPConfigMain == True:
#                     for tVariant2 in tMachine.ActiveJob.PConfigJobs:
#                         tChildJob = tVariant2
#                         if tChildJob.ActiveJosh is None:
#                             JoshID = MdlADOFunctions.fGetRstValLong(MdlADOFunctions.GetSingleValue('ID', 'TblJoshCurrent', 'JobID = ' + tChildJob.ID + ' AND ShiftID <> ' + self.CurrentShiftID + ' ORDER BY StartTime DESC', 'CN'))
#                             if JoshID != 0:
#                                 tJosh = Josh()
#                                 tJosh.Init(tChildJob, JoshID)
#                                 tChildJob.ActiveJosh = tJosh
                                
                                
                                
#                                 if tChildJob.OpenEvent is None:
#                                     tChildJob.GetOpenEvent
#                                 if not tChildJob.OpenEvent is None:
#                                     tChildJob.OpenEvent.Josh = tJosh
#                                     tChildJob.OpenEvent.Update
                                
#                                 if tChildJob.OpenWorkingEvent is None:
#                                     tChildJob.GetOpenWorkingEvent
#                                 if not tChildJob.OpenWorkingEvent is None:
#                                     tChildJob.OpenWorkingEvent.Josh = tJosh
#                                     tChildJob.OpenWorkingEvent.Update
                                
#                                 if tChildJob.OpenEngineEvent is None:
#                                     tChildJob.GetOpenEngineEvent
#                                 if not tChildJob.OpenEngineEvent is None:
#                                     tChildJob.OpenEngineEvent.Josh = tJosh
#                                     tChildJob.OpenEngineEvent.Update
#                             tChildJob.CreateJoshForNewShift
#         fn_return_value = True
#         if Err.Number != 0:
#             RecordError('LeaderRT:CompleteMissingShiftsObject', str(Err.Number), Err.Description, strSQL)
#             Err.Clear()
            
            
#         return fn_return_value

#     def UpdateMachineActiveCalendarEvent(self, pMachineID, pActiveCalendarEvent):
#         tMachine = Machine()
        
#         fn_return_value = False
#         tMachine = self.mMachines.Item(str(pMachineID))
#         tMachine.ActiveCalendarEvent = pActiveCalendarEvent
#         if not pActiveCalendarEvent:
#             tMachine.ActiveCalendarEventProductionModeID = 0
#         fn_return_value = True
#         if Err.Number != 0:
#             Err.Clear()
#         return fn_return_value

#     def ClosePreviousEngineEvents(self):
#         strSQL = ''
        
#         fn_return_value = False
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblEngineEvents SET JoshID = (SELECT TOP 1 ID FROM TblJosh WHERE ShiftID = TblEngineEvents.ShiftID AND JobID = TblEngineEvents.JobID)' + '\r\n'
#         strSQL = strSQL + 'WHERE JoshID = 0 AND JobID <> 0 AND ShiftID <> 0'
#         CN.Execute(strSQL)
        
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblEngineEvents SET ' + '\r\n'
#         strSQL = strSQL + 'EndTime = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEngineEvents.JoshID)) < 0 THEN EventTime ELSE (SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEngineEvents.JoshID) END,' + '\r\n'
#         strSQL = strSQL + 'Duration = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEngineEvents.JoshID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblJosh.EndTime FROM TblJosh WHERE TblJosh.ID = TblEngineEvents.JoshID)) END' + '\r\n'
#         strSQL = strSQL + 'WHERE EndTime IS NULL AND JoshID IN(SELECT ID FROM TblJosh WHERE EndTime IS NOT NULL)'
#         CN.Execute(strSQL)
#         strSQL = ''
#         strSQL = strSQL + 'UPDATE TblEngineEvents SET ' + '\r\n'
#         strSQL = strSQL + 'EndTime = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEngineEvents.ShiftID)) < 0 THEN EventTime ELSE (SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEngineEvents.ShiftID) END,' + '\r\n'
#         strSQL = strSQL + 'Duration = CASE WHEN DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEngineEvents.ShiftID)) < 0 THEN 0 ELSE DATEDIFF(n,EventTime,(SELECT TblShift.EndTime FROM TblShift WHERE TblShift.ID = TblEngineEvents.ShiftID)) END' + '\r\n'
#         strSQL = strSQL + 'WHERE EndTime IS NULL AND JoshID = 0'
#         CN.Execute(strSQL)
#         fn_return_value = True
#         if Err.Number != 0:
#             if InStr(Err.Description, 'nnection') > 0:
#                 if CN.State == 1:
#                     CN.Close()
#                 CN.Open()
#                 if MetaCn.State == 1:
#                     MetaCn.Close()
#                 MetaCn.Open()
#                 Err.Clear()
                
#             Err.Clear()
#         return fn_return_value


    def setStartTime(self, value):
        self.mStartTime = value

    def getStartTime(self):
        fn_return_value = self.mStartTime
        return fn_return_value
    StartTime = property(fset=setStartTime, fget=getStartTime)


    
    def setServerID(self, the_mServerID):
        self.mServerID = the_mServerID

    def getServerID(self):
        fn_return_value = self.mServerID
        return fn_return_value
    ServerID = property(fset=setServerID, fget=getServerID)


    
    def setCurrentShiftID(self, the_mCurrentShiftID):
        self.mCurrentShiftID = the_mCurrentShiftID

    def getCurrentShiftID(self):
        fn_return_value = self.mCurrentShiftID
        return fn_return_value
    CurrentShiftID = property(fset=setCurrentShiftID, fget=getCurrentShiftID)


    
    def setCurrentShift(self, value):
        self.mCurrentShift = value

    def getCurrentShift(self):
        if self.mCurrentShift:
            fn_return_value = self.mCurrentShift
        else:
            fn_return_value = None
        return fn_return_value
    CurrentShift = property(fset=setCurrentShift, fget=getCurrentShift)


    
    def setShiftCalendar(self, value):
        self.mShiftCalendar = value

    def getShiftCalendar(self):
        fn_return_value = self.mShiftCalendar
        return fn_return_value
    ShiftCalendar = property(fset=setShiftCalendar, fget=getShiftCalendar)

    
    def setConCount(self, the_mConCount):
        self.mConCount = the_mConCount

    def getConCount(self):
        fn_return_value = self.mConCount
        return fn_return_value
    ConCount = property(fset=setConCount, fget=getConCount)

    
    def setPlantID(self, the_mPlantID):
        self.mPlantID = the_mPlantID

    def getPlantID(self):
        fn_return_value = self.mPlantID
        return fn_return_value
    PlantID = property(fset=setPlantID, fget=getPlantID)


    
    def setStatus(self, the_mStatus):
        self.mStatus = the_mStatus

    def getStatus(self):
        fn_return_value = self.mStatus
        return fn_return_value
    Status = property(fset=setStatus, fget=getStatus)


    
    def setCNstr(self, the_mCNstr):
        self.mCNstr = the_mCNstr

    def getCNstr(self):
        fn_return_value = self.mCNstr
        return fn_return_value
    CNstr = property(fset=setCNstr, fget=getCNstr)


    
    def setSCID(self, the_mSCID):
        self.mSCID = the_mSCID

    def getSCID(self):
        fn_return_value = self.mSCID
        return fn_return_value
    SCID = property(fset=setSCID, fget=getSCID)


    
    def setCNStatus(self, the_mCNStatus):
        self.mCNStatus = the_mCNStatus

    def getCNStatus(self):
        fn_return_value = self.mCNStatus
        return fn_return_value
    CNStatus = property(fset=setCNStatus, fget=getCNStatus)


    
    def setMetaCNstr(self, the_mMetaCNstr):
        self.mMetaCNstr = the_mMetaCNstr

    def getMetaCNstr(self):
        fn_return_value = self.mMetaCNstr
        return fn_return_value
    MetaCNstr = property(fset=setMetaCNstr, fget=getMetaCNstr)


    
    def setMetaCNStatus(self, the_mMetaCNStatus):
        self.mMetaCNStatus = the_mMetaCNStatus

    def getMetaCNStatus(self):
        fn_return_value = self.mMetaCNStatus
        return fn_return_value
    MetaCNStatus = property(fset=setMetaCNStatus, fget=getMetaCNStatus)


    def setProducts(self, value):
        self.mProducts = value

    def getProducts(self):
        fn_return_value = self.mProducts
        return fn_return_value
    Products = property(fset=setProducts, fget=getProducts)


    def setMolds(self, value):
        self.mMolds = value

    def getMolds(self):
        fn_return_value = self.mMolds
        return fn_return_value
    Molds = property(fset=setMolds, fget=getMolds)


    def setDepartments(self, value):
        self.mDepartments = value

    def getDepartments(self):
        fn_return_value = self.mDepartments
        return fn_return_value
    Departments = property(fset=setDepartments, fget=getDepartments)


    def setMachineTypes(self, value):
        self.mMachineTypes = value

    def getMachineTypes(self):
        fn_return_value = self.mMachineTypes
        return fn_return_value
    MachineTypes = property(fset=setMachineTypes, fget=getMachineTypes)

    
    def setMachines(self, value):
        self.mMachines = value

    def getMachines(self):
        fn_return_value = self.mMachines
        return fn_return_value
    Machines = property(fset=setMachines, fget=getMachines)


    def setSystemVariables(self, value):
        self.mSystemVariables = value

    def getSystemVariables(self):
        fn_return_value = self.mSystemVariables
        return fn_return_value
    SystemVariables = property(fset=setSystemVariables, fget=getSystemVariables)


    def setActiveInventoryItems(self, value):
        self.mActiveInventoryItems = value

    def getActiveInventoryItems(self):
        fn_return_value = self.mActiveInventoryItems
        return fn_return_value
    ActiveInventoryItems = property(fset=setActiveInventoryItems, fget=getActiveInventoryItems)


    def setGeneralUpdateRateSet(self, MachineID, vUpdateRate):
        tMachine = Machine()
        Counter = 0
        
        if MachineID > 0:
            tMachine = self.mMachines.Item(str(MachineID))
            tMachine.GeneralUpdateRate = vUpdateRate *  ( self.mMachines.Count + 1 )
        else:
            for Counter in range(1, self.mMachines.Count):
                tMachine = self.mMachines.Item(Counter)
                tMachine.GeneralUpdateRate = vUpdateRate *  ( self.mMachines.Count + 1 )
    GeneralUpdateRateSet = property(fset=setGeneralUpdateRateSet)

    
