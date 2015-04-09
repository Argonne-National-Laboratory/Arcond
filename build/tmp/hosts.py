# ANL hosts
def getAllHosts():
    ascComputers=[]
    ascComputers.append("atlaswww")
    ascComputers.append("atlasnis")
    ascComputers.append("atlasnat")
    ascComputers.append("atlasld1")
    ascComputers.append("atlasld2")
    ascComputers.append("atlascal")
    ascComputers.append("atlasfs1") 
    ascComputers.append("atlasfs2")
    for i in range(1,61):
        host="atlas"+str(i)+".hep.anl.gov"
        ascComputers.append(host) 
    return  ascComputers

# only PC farm
def getHosts():
    ascComputers=[]
    for i in range(1,61):
        host="atlas"+str(i)+".hep.anl.gov"
        ascComputers.append(host)
    return  ascComputers
 
