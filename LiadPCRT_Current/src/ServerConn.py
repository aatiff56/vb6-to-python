from datetime import datetime
import Server as server

class ServerConn:
    mSCID = 0
    gServer = None

    def __init__(self):
        try:
            if self.gServer is None:
                pass
            else:
                self.gServer.ConCount = self.gServer.ConCount + 1
        except:
            pass

    def StartServerConn(self, pArr, strSchCN):
        try:
            if len(pArr) >= 0:
                self.mSCID = pArr[5]
            else:
                self.mSCID = 0
            self.gServer = server.Server()
            self.gServer.StartTime = datetime.now()
            LeaderSVR = self.gServer
            fn_return_value = self.gServer.StartServer(pArr, strSchCN)
            return fn_return_value
        
        except BaseException as error:
            return fn_return_value

    def __del__(self):        
        if self.gServer :
            self.gServer.ConCount = self.gServer.ConCount - 1
            if self.gServer.ConCount < 1:                
                self.gServer = None

    def getServer(self):
        fn_return_value = self.gServer
        return fn_return_value
    Server = property(fget=getServer)
    
    def setSCID(self, the_mSCID):
        self.mSCID = the_mSCID

    def getSCID(self):
        fn_return_value = self.mSCID
        return fn_return_value
    SCID = property(fset=setSCID, fget=getSCID)
