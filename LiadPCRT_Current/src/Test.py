obj = {}
n = 'Name'
a = 'age'

obj[n] = 'Ahmed'
obj[a] = 27

print(obj)





def GetInventoryItemFromGlobalCollection(pCollection, pInventoryID):
    returnVal = None
    tMaterialBatch = None

    try:
        if pCollection.Count > 0:
            if not ( pCollection[str(pInventoryID)] is None ) :
                tMaterialBatch = pCollection[str(pInventoryID)]
                returnVal = tMaterialBatch
            else:
                returnVal = None
        else:
            returnVal = None

    except BaseException as error:
        MdlGlobal.RecordError('GetInventoryItemFromGlobalCollection', str(0), error.args[0], 'InventoryID: ' + str(pInventoryID))
        returnVal = None
    return returnVal

def AddInventoryItemToGlobalCollection(pMaterialBatch):
    returnVal = False
    try:
        if MdlGlobal.gServer.ActiveInventoryItems[str(pMaterialBatch.ID)] is None:
            MdlGlobal.gServer.ActiveInventoryItems[str(pMaterialBatch.ID)] = pMaterialBatch
        returnVal = True

    except BaseException as error:
        MdlGlobal.RecordError('AddInventoryItemToGlobalCollection', str(0), error.args[0], 'InventoryID: ' + str(pMaterialBatch.ID))
    return returnVal
