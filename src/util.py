from os.path import splitext
from os.path import basename

def convert2geometry(w=0, h=0):
    return str(w) + "x" + str(h)
    
def convert2extensions(content):
    res = []
    for data in content:
        localData = []
        localData.append(data["name"])
        localData.append(data["type"])
        localData = tuple(localData)
        res.append(localData)
    return res

def getBasename(path):
    bsname = basename(path)
    return splitext(bsname)
