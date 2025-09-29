import cube
import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='cube.log',  
    filemode='w'  
)

class CubeErr(Exception):
    pass

def BlockToBfs(str1,str2,intState1,intState2,methodName):
    traversalEdgeOp = []
    traversalEdgeO = []
    traversalEdgeP = []
    traversalCornerOp = []
    traversalCornerO = []
    traversalCornerP = []
    traversalEdgeWild = 0
    traversalCornerWild = 0
    traversalCentre = []
    tempSplit1 = str1.rstrip().split()
    tempSplit2 = str2.rstrip().split()
    tempPairs1 = []
    tempPairs2 = []
    if(len(tempSplit1)%2!=0):
        raise CubeErr("str1 is not even")
    if(len(tempSplit2)%2!=0):
        raise CubeErr("str2 is not even")
    for i in range(0,len(tempSplit1),2):
        tempPairs1.append((int(tempSplit1[i]),int(tempSplit1[i+1])))
    for i in range(0,len(tempSplit2),2):
        tempPairs2.append((int(tempSplit2[i]),int(tempSplit2[i+1])))
        
    # find a pair in tempPairs1 with first in range 0-11
    while(9):
        i = 0
        while(i<len(tempPairs1)):
            if(tempPairs1[i][0] in range(0,12) and tempPairs1[i][1] in range(0,12)):
                break
            i+=1
        if(i==len(tempPairs1)):
            break
        tempPosition = tempPairs1[i][1]
        #check if any pair with second tempPosition+26
        j = i
        while(j<len(tempPairs1)):
            if(tempPairs1[j][1] in [tempPosition+26,tempPosition+38]):
                break
            j+=1
        if(j>=len(tempPairs1)):
            # no orientation
            tempHasOrientation1 = False
        else:
            tempHasOrientation1 = True
            
        # find the pair with first tempPairs1[i][0]
        m = 0
        while(m<len(tempPairs2)):
            if(tempPairs2[m][0] == tempPairs1[i][0] and tempPairs2[m][1] in range(0,12)):
                break
            m+=1
        if(m>=len(tempPairs2)):
            raise CubeErr("can not find pair 1")
        tempPosition = tempPairs2[m][1]
        #check if any pair with second tempPosition+26
        n = m
        while(n<len(tempPairs2)):
            if(tempPairs2[n][1] in [tempPosition+26,tempPosition+38]):
                break
            n+=1
        if(n>=len(tempPairs2)):
            # no orientation
            tempHasOrientation2 = False
        else:
            tempHasOrientation2 = True
        # logging.info(str((tempHasOrientation1,tempHasOrientation2)))    
        if(tempHasOrientation1 and not(tempHasOrientation2)):
            raise CubeErr("has orientation 1 but not 2")
        
        if(not (tempHasOrientation1) and tempHasOrientation2):
            traversalEdgeO.append(tempPairs1[i][1]) #mark the position of the edge
            # logging.info("traversalEdgeO: "+str(tempPairs1[i][1]))

        # remove the grabbed info
        del tempPairs1[i]
        if(tempHasOrientation1):
            del tempPairs1[j-1]
        del tempPairs2[m]
        if(tempHasOrientation2):
            del tempPairs2[n-1]
            
        # logging.info("tempPairs1: "+str(tempPairs1))
        # logging.info("tempPairs2: "+str(tempPairs2))
        
    # find a pair in tempPairs2 with first in range 0-11
    while(9):
        i = 0
        while(i<len(tempPairs2)):
            if(tempPairs2[i][0] in range(0,12) and tempPairs2[i][1] in range(0,12)):
                break
            i+=1
        if(i==len(tempPairs2)):
            break
        tempPosition = tempPairs2[i][1]
        #check if any pair with second tempPosition+26
        j = i
        while(j<len(tempPairs2)):
            if(tempPairs2[j][1] in [tempPosition+26,tempPosition+38]):
                break
            j+=1
        if(j>=len(tempPairs2)):
            # no orientation
            tempHasOrientation2 = False
        else:
            tempHasOrientation2 = True
            
        #There should not be any position info in tempPairs1 because it has been deleted by the previous loop
        if(tempHasOrientation2):
            traversalEdgeOp.append(tempPairs2[i][0])
            # logging.info("traversalEdgeOp: "+str(tempPairs2[i][0]))
            del tempPairs2[i]
            del tempPairs2[j-1]
        else:
            traversalEdgeP.append(tempPairs2[i][0])
            # logging.info("traversalEdgeP: "+str(tempPairs2[i][0]))
            del tempPairs2[i]
        # logging.info("tempPairs1: "+str(tempPairs1))
        # logging.info("tempPairs2: "+str(tempPairs2))    
        
    # corner        
    while(9):
        i = 0
        while(i<len(tempPairs1)):
            if(tempPairs1[i][0] in range(0,8) and tempPairs1[i][1] in range(12,20)):
                break
            i+=1
        if(i==len(tempPairs1)):
            break
        tempPosition = tempPairs1[i][1]
        #check if any pair with second tempPosition+38 or +46 or +54
        j = i
        while(j<len(tempPairs1)):
            if(tempPairs1[j][1] in [tempPosition+38,tempPosition+46,tempPosition+54]):
                break
            j+=1
        if(j>=len(tempPairs1)):
            # no orientation
            tempHasOrientation1 = False
        else:
            tempHasOrientation1 = True
            
        m = 0
        while(m<len(tempPairs2)):
            if(tempPairs2[m][0] == tempPairs1[i][0] and tempPairs2[m][1] in range(12,20)):
                break
            m+=1
        if(m>=len(tempPairs2)):
            raise CubeErr("cannot find pair 2")
        tempPosition = tempPairs2[m][1]
        # check if any pair with second tempPosition +38/+46/+54
        n = m
        while(n<len(tempPairs2)):
            if(tempPairs2[n][1] in [tempPosition+38,tempPosition+46,tempPosition+54]):
                break
            n+=1
        if(n>=len(tempPairs2)):
            # no orientation
            tempHasOrientation2 = False
        else:
            tempHasOrientation2 = True
        # logging.info("corner...")
        # logging.info(str((tempHasOrientation1,tempHasOrientation2)))
        if(tempHasOrientation1 and not (tempHasOrientation2)):
            raise CubeErr("corner has orientation 1 but not 2")
        
        if(not(tempHasOrientation1) and tempHasOrientation2):
            traversalCornerO.append(tempPairs1[i][1])
            # mark the position of the corner
            # logging.info("traversalCornerO: "+str(tempPairs1[i][1]))
            
        # remove the grabbed info
        del tempPairs1[i]
        if(tempHasOrientation1):
            del tempPairs1[j-1]
        del tempPairs2[m]
        if(tempHasOrientation2):
            del tempPairs2[n-1]
            
        # logging.info("tempPairs1: "+str(tempPairs1))
        # logging.info("tempPairs2: "+str(tempPairs2))  
            
    # find a pair in tempPairs2 with first in range 0-7
    while(9):
        i = 0
        while(i<len(tempPairs2)):
            if(tempPairs2[i][0] in range(0,8) and tempPairs2[i][1] in range(12,20)):
                break
            i+=1
        if(i>=len(tempPairs2)):
            break
        tempPosition = tempPairs2[i][1]
        # check if any pair with second tempPosition+38/+46/+54
        j = i
        while(j<len(tempPairs2)):
            if(tempPairs2[j][1] in [tempPosition+38,tempPosition+46,tempPosition+54]):
                break
            j+=1
        if(j>=len(tempPairs2)):
            tempHasOrientation2 = False
        else:
            tempHasOrientation2 = True
            
        #There should not be any position info in tempPairs1 because it has been deleted by the previous loop
        if(tempHasOrientation2):
            traversalCornerOp.append(tempPairs2[i][0])
            # logging.info("traversalCornerOp: "+str(tempPairs2[i][0]))
            del tempPairs2[i]
            del tempPairs2[j-1]
        else:
            traversalCornerP.append(tempPairs2[i][0])
            # logging.info("traversalCornerP: "+str(tempPairs2[i][0]))
            del tempPairs2[i]
            
        # logging.info("tempPairs1: "+str(tempPairs1))
        # logging.info("tempPairs2: "+str(tempPairs2))
        
    #centre
    #find a pair in tempPairs1 with first in range 0-6 and second in range 20-26
    while(9):
        i = 0
        while(i<len(tempPairs1)):
            if(tempPairs1[i][0] in range(0,6) and tempPairs1[i][1] in range(20,26)):
                break
            i+=1
        if(i>=len(tempPairs1)):
            break
        tempPosition = tempPairs1[i][1]
        
        # find the pair with first tempPairs[i][0] in tempPairs2
        m = 0
        while(m<len(tempPairs2)):
            if(tempPairs2[m][0] == tempPairs1[i][0] and tempPairs2[m][1] in range(20,26)):
                break
            m+=1
        if(m>=len(tempPairs2)):
            raise CubeErr("cannot find pair 1 in centre")
        
        # remove the grabbed info
        del tempPairs1[i]
        del tempPairs2[m]
        
        # logging.info("tempPairs1: "+str(tempPairs1))
        # logging.info("tempPairs2: "+str(tempPairs2))
        
    while(9):
        i = 0
        while(i<len(tempPairs2)):
            if(tempPairs2[i][0] in range(0,6) and tempPairs2[i][1] in range(20,26)):
                break
            i+=1
        if(i>=len(tempPairs2)):
            break

        # There should not be any position info in tempPairs1 because it has been deleted by the previous loop
        traversalCentre.append(tempPairs2[i][0])
        # logging.info("traversalCentre: "+str(tempPairs2[i][0]))
        del tempPairs2[i]
        # logging.info("tempPairs1: "+str(tempPairs1))
        # logging.info("tempPairs2: "+str(tempPairs2))
    
    # What remains are edge wild and corner wild. We can count how many wild orientions are there in edge/corner
    for i in range(0,len(tempPairs2)):
        if(tempPairs2[i][1] in range(26,50)):
            traversalEdgeWild+=1
        elif(tempPairs2[i][1] in range(50,74)):
            traversalCornerWild+=1
            
    # logging.info("edgeWildCount: "+str(traversalEdgeWild))
    # logging.info("cornerWildCount: "+str(traversalCornerWild))
    return traversalEdgeOp,traversalEdgeO,traversalEdgeP,traversalEdgeWild,traversalCornerOp,traversalCornerO,traversalCornerP,traversalCornerWild,traversalCentre

if __name__ == "__main__":
    BlockToBfs("9 9 0 35", "4 8 9 9 4 24 5 25 0 35", 2, 3, "Roux_v1")  