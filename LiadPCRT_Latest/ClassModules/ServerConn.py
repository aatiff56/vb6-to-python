from LiadPCUnite.Global import Logs
from datetime import datetime

class ServerConn:
    logger = Logs.Logger()
    mSCID = 0

    def __init__(self):
        if gServer is None:
            pass
        else:
            gServer.ConCount = gServer.ConCount + 1        

    def StartServerConn(self, pArr):
        try:
            if len(pArr) >= 0:
                self.mSCID = pArr(5)
            else:
                self.mSCID = 0
            gServer = self.Server()
            gServer.StartTime = datetime.now()
            LeaderSVR = gServer
            fn_return_value = gServer.StartServer(pArr())
            return fn_return_value
        except BaseException as error:
            self.sqlCntr.CloseConnection()
            self.logger.Error(error)
            return fn_return_value

    def __del__(self):        
        if not ( gServer is None ) :
            gServer.ConCount = gServer.ConCount - 1
            if gServer.ConCount < 1:                
                gServer = None

    def getServer(self):
        fn_return_value = gServer
        return fn_return_value
    Server = property(fget=getServer)
    
    def setSCID(self, the_mSCID):
        self.mSCID = the_mSCID

    def getSCID(self):
        fn_return_value = self.mSCID
        return fn_return_value
    SCID = property(fset=setSCID, fget=getSCID)
