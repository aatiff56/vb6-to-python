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

    def StartServerConn(self, pArr):
        try:
            if len(pArr) >= 0:
                self.mSCID = pArr(5)
            else:
                self.mSCID = 0
            gServer = server.Server()
            gServer.StartTime = datetime.now()
            LeaderSVR = gServer
            fn_return_value = gServer.StartServer(pArr())
            return fn_return_value
        except BaseException as error:
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
