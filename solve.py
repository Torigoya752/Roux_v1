import numpy as np
import cube
from cube import CubeErr, calHash1
import os
import sys
import copy
from collections import deque
import logging
import block2bfs
import solveSlotCase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='./cube.log',  
    filemode='w'  
)

class bfsDequeElement:
    def __init__(self, cube, move, lastMove, dualMove, intFirst2, moveNum, points):
        self.cube = cube
        self.move = move
        self.lastMove = lastMove
        self.dualMove = dualMove
        self.intFirst2 = intFirst2
        self.moveNum = moveNum
        self.points = points
        
class bfsHashElement:
    def __init__(self, move, lastMove, dualMove, intFirst2, moveNum, points):
        self.move = move
        self.lastMove = lastMove
        self.dualMove = dualMove
        self.intFirst2 = intFirst2
        self.moveNum = moveNum
        self.points = points
        
class Alg:
    def __init__(self, transferReverse, move, points):
        self.transferReverse = transferReverse
        self.move = move
        self.points = points
    def ModifyTransfer(self,newTransfer):
        self.transferReverse = newTransfer
        
class WinnerAlgs:
    def __init__(self, maxLength):
        self.winnerAlgs = []
        self.minPoint = -1.0
        self.lengthOneAlgs = []
        self.maxLength = maxLength
    def clean(self):
        if(self.minPoint < 0):
            return
        # sort the self.winnerAlgs
        self.winnerAlgs.sort(key=lambda x: x.points)
        # delete the elements with index >= maxLength
        while len(self.winnerAlgs) > self.maxLength:
            del self.winnerAlgs[self.maxLength]
        while(self.winnerAlgs[-1].points > self.minPoint * 1.2 or self.winnerAlgs[-1].points > self.minPoint + 2.5):
            del self.winnerAlgs[-1]
    def judge(self, alg):
        # alg should be class Alg
        tempSplit=alg.move.rstrip().split()
        if(-0.03125 < self.minPoint < 0.03125 and len(tempSplit) == 1):
            self.lengthOneAlgs.append(alg)
            return
        if(self.minPoint>=-0.001 and (alg.points > self.minPoint * 1.2 or alg.points > self.minPoint + 2.5)):
            # do nothing
            pass
       
        tempBool = True
        
        for i in range(self.maxLength):
            if(len(self.winnerAlgs)>=(i+1) and np.all(np.equal(alg.transferReverse,self.winnerAlgs[i].transferReverse))):
                tempBool = False
                if(alg.points>=self.winnerAlgs[i].points):
                    pass
                else:
                    self.winnerAlgs[i] = copy.deepcopy(alg)
                    if(alg.points < self.minPoint):
                        self.minPoint = alg.points
                break
                    
        if(not tempBool):
            # do nothing 
            pass
        elif(alg.points < self.minPoint and self.minPoint >= -0.001):
            self.minPoint = alg.points
            self.winnerAlgs.append(copy.deepcopy(alg))
            self.clean()
        else:
            self.winnerAlgs.append(copy.deepcopy(alg))
            if(self.minPoint < 0):
                self.minPoint = alg.points
            self.clean()

class SolveAlg:
    def __init__(self, listAlg, points):
        self.move = listAlg[:]
        self.points = points
        self.moveMatrix = np.eye(74,dtype=np.int8)
        for item in self.move:
            self.moveMatrix = self.moveMatrix @ cube.dictMove[item]
            
class SolveMove:
    def __init__(self, currMatrix, listAlg, points, currState):
        self.currMatrix = copy.deepcopy(currMatrix)
        self.move = listAlg[:]
        self.points = points
        self.currState = currState
    

def CheckExistStrict(str1):
    if(os.path.isfile(str1)):
        pass
    else:
        raise FileNotFoundError("Cannot find "+ str1)

def CheckExistGenerate(str1):
    if(os.path.isfile(str1)):
        pass
    else:
        with open(str1, 'w') as f:
            pass
        
def CheckExistFolderGenerate(str1):
    if(os.path.exists(str1)):
        pass
    else:
        os.mkdir(str1)
    

def GenerateCase2(str1,str2,intState1, intState2, methodName):
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
        
    # check if all the edges in tempPairs1 are oriented
    tempOriented = [False] * 12
    for item in tempPairs1:
        if(26<=item[1]<=37):
            tempOriented[item[1]-26] = True
    edgeAllOriented = True
    for item in tempOriented:
        if(item==False):
            edgeAllOriented = False
            break
        
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
        logging.info(str((tempHasOrientation1,tempHasOrientation2)))    
        if(tempHasOrientation1 and not(tempHasOrientation2)):
            raise CubeErr("has orientation 1 but not 2")
        
        if(not (tempHasOrientation1) and tempHasOrientation2):
            traversalEdgeO.append(tempPairs1[i][1]) #mark the position of the edge
            logging.info("traversalEdgeO: "+str(tempPairs1[i][1]))

        # remove the grabbed info
        del tempPairs1[i]
        if(tempHasOrientation1):
            del tempPairs1[j-1]
        del tempPairs2[m]
        if(tempHasOrientation2):
            del tempPairs2[n-1]
            
        logging.info("tempPairs1: "+str(tempPairs1))
        logging.info("tempPairs2: "+str(tempPairs2))
            
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
            if(not edgeAllOriented):
                traversalEdgeOp.append(tempPairs2[i][0])
                logging.info("traversalEdgeOp: "+str(tempPairs2[i][0]))
            else:
                traversalEdgeP.append(tempPairs2[i][0])
                logging.info("traversalEdgeP: "+str(tempPairs2[i][0]))
            del tempPairs2[i]
            del tempPairs2[j-1]
        else:
            traversalEdgeP.append(tempPairs2[i][0])
            logging.info("traversalEdgeP: "+str(tempPairs2[i][0]))
            del tempPairs2[i]
        logging.info("tempPairs1: "+str(tempPairs1))
        logging.info("tempPairs2: "+str(tempPairs2))    
        
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
        logging.info("corner...")
        logging.info(str((tempHasOrientation1,tempHasOrientation2)))
        if(tempHasOrientation1 and not (tempHasOrientation2)):
            raise CubeErr("corner has orientation 1 but not 2")
        
        if(not(tempHasOrientation1) and tempHasOrientation2):
            traversalCornerO.append(tempPairs1[i][1])
            # mark the position of the corner
            logging.info("traversalCornerO: "+str(tempPairs1[i][1]))
            
        # remove the grabbed info
        del tempPairs1[i]
        if(tempHasOrientation1):
            del tempPairs1[j-1]
        del tempPairs2[m]
        if(tempHasOrientation2):
            del tempPairs2[n-1]
            
        logging.info("tempPairs1: "+str(tempPairs1))
        logging.info("tempPairs2: "+str(tempPairs2))  
            
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
            logging.info("traversalCornerOp: "+str(tempPairs2[i][0]))
            del tempPairs2[i]
            del tempPairs2[j-1]
        else:
            traversalCornerP.append(tempPairs2[i][0])
            logging.info("traversalCornerP: "+str(tempPairs2[i][0]))
            del tempPairs2[i]
            
        logging.info("tempPairs1: "+str(tempPairs1))
        logging.info("tempPairs2: "+str(tempPairs2))
        
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
        
        logging.info("tempPairs1: "+str(tempPairs1))
        logging.info("tempPairs2: "+str(tempPairs2))
        
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
        logging.info("traversalCentre: "+str(tempPairs2[i][0]))
        del tempPairs2[i]
        logging.info("tempPairs1: "+str(tempPairs1))
        logging.info("tempPairs2: "+str(tempPairs2))
    
    # What remains are edge wild and corner wild. We can count how many wild orientions are there in edge/corner
    for i in range(0,len(tempPairs2)):
        if(tempPairs2[i][1] in range(26,50)):
            traversalEdgeWild+=1
        elif(tempPairs2[i][1] in range(50,74)):
            traversalCornerWild+=1
            
    # if edgeAllOriented, clear the edgeWild
    if(edgeAllOriented):
        traversalEdgeWild = 0
            
    logging.info("edgeWildCount: "+str(traversalEdgeWild))
    logging.info("cornerWildCount: "+str(traversalCornerWild))
    
    class caseProgress:
        def __init__(self,pairsCube,traversalEdgeP,traversalEdgeO,traversalEdgeOp,traversalEdgeWild,traversalCornerP,traversalCornerO,traversalCornerOp,traversalCornerWild,traversalCentre):
            self.pairsCube = pairsCube[:]
            self.traversalEdgeP = traversalEdgeP[:]
            self.traversalEdgeO = traversalEdgeO[:]
            self.traversalEdgeOp = traversalEdgeOp[:]
            self.traversalEdgeWild = traversalEdgeWild
            self.traversalCornerP = traversalCornerP[:]
            self.traversalCornerO = traversalCornerO[:]
            self.traversalCornerOp = traversalCornerOp[:]
            self.traversalCornerWild = traversalCornerWild
            self.traversalCentre = traversalCentre[:]
    
    # remember str1 is the start cube
    tempPairs1 = []
    results = []
    for i in range(0,len(tempSplit1),2):
        tempPairs1.append((int(tempSplit1[i]),int(tempSplit1[i+1])))
    
    tempBfsDeque = deque()
    tempBfsDeque.append(caseProgress(tempPairs1,traversalEdgeP,traversalEdgeO,traversalEdgeOp,traversalEdgeWild,traversalCornerP,traversalCornerO,traversalCornerOp,traversalCornerWild,traversalCentre))
    
    while(9):
        if(len(tempBfsDeque) == 0):
            break
        tempProgress = tempBfsDeque.popleft()
        if(len(tempProgress.traversalEdgeP) > 0):
            tempEdge = tempProgress.traversalEdgeP[0]
            tempTraversalEdgeP = tempProgress.traversalEdgeP[:]
            del tempTraversalEdgeP[0]
            # check which edges are vacant
            tempVacantEdge = [1] * 12
            for item in tempProgress.pairsCube:
                if(item[0] in range(12) and item[1] in range(12)):
                    tempVacantEdge[item[1]] = 0
            for i in range(0,12):
                if(tempVacantEdge[i] == 1):
                    tempPairsCube = tempProgress.pairsCube[:] + [(tempEdge,i)]
                    tempBfsDeque.append(caseProgress(tempPairsCube[:],tempTraversalEdgeP[:],tempProgress.traversalEdgeO,tempProgress.traversalEdgeOp,tempProgress.traversalEdgeWild,tempProgress.traversalCornerP,tempProgress.traversalCornerO,tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            continue
        elif(len(tempProgress.traversalEdgeO) > 0):
            tempEdge = tempProgress.traversalEdgeO[0]
            tempTraversalEdgeO = tempProgress.traversalEdgeO[:]
            del tempTraversalEdgeO[0]
            # check whether tempProgress.pairsCube has a pair with (0,tempEdge+26/38)
            for item in tempProgress.pairsCube:
                if(item[0] == 0 and item[1] in [tempEdge+26,tempEdge+38]):
                    raise CubeErr("Error in traversalEdgeO")
            # only two cases
            tempPairsCube1 = tempProgress.pairsCube[:] + [(0,tempEdge+26)]
            tempBfsDeque.append(caseProgress(tempPairsCube1[:],tempProgress.traversalEdgeP,tempTraversalEdgeO[:],tempProgress.traversalEdgeOp,tempProgress.traversalEdgeWild,tempProgress.traversalCornerP,tempProgress.traversalCornerO,tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            tempPairsCube2 = tempProgress.pairsCube[:] + [(0,tempEdge+38)]
            tempBfsDeque.append(caseProgress(tempPairsCube2[:],tempProgress.traversalEdgeP,tempTraversalEdgeO[:],tempProgress.traversalEdgeOp,tempProgress.traversalEdgeWild,tempProgress.traversalCornerP,tempProgress.traversalCornerO,tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            continue
        
        elif(len(tempProgress.traversalEdgeOp) > 0):
            tempEdge = tempProgress.traversalEdgeOp[0]
            tempTraversalEdgeOp = tempProgress.traversalEdgeOp[:]
            del tempTraversalEdgeOp[0]
            # check which positions are vacant
            tempVacantEdge = [1] * 12
            for item in tempProgress.pairsCube:
                if(item[0] in range(12) and item[1] in range(12)):
                    tempVacantEdge[item[1]] = 0
            for i in range(0,12):
                if(tempVacantEdge[i] == 1):
                    # check if pairsCube has relative orientation info
                    for item in tempProgress.pairsCube:
                        if(item[1] in [i+26,i+38]):
                            raise CubeErr("traversalEdgeOp already has orientation")
                    # two cases
                    tempPairsCube1 = tempProgress.pairsCube[:] + [(tempEdge,i),(0,i+26)]
                    tempBfsDeque.append(caseProgress(tempPairsCube1[:],tempProgress.traversalEdgeP,tempProgress.traversalEdgeO,tempTraversalEdgeOp[:],tempProgress.traversalEdgeWild,tempProgress.traversalCornerP,tempProgress.traversalCornerO,tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
                    tempPairsCube2 = tempProgress.pairsCube[:] + [(tempEdge,i),(0,i+38)]
                    tempBfsDeque.append(caseProgress(tempPairsCube2[:],tempProgress.traversalEdgeP,tempProgress.traversalEdgeO,tempTraversalEdgeOp[:],tempProgress.traversalEdgeWild,tempProgress.traversalCornerP,tempProgress.traversalCornerO,tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            continue
        
        elif(tempProgress.traversalEdgeWild>0):
            # assume that all remaining edges are wild
            # make an assertion
            edgeHasOriented = 0
            for item in tempProgress.pairsCube:
                if(item[1] in range(26,50)):
                    edgeHasOriented += 1
            if(edgeHasOriented != 12 - tempProgress.traversalEdgeWild):
                logging.info("assertion failed: edgeHasOriented != 12 - tempProgress.traversalEdgeWild")
                raise CubeErr("assertion failed: edgeHasOriented != 12 - tempProgress.traversalEdgeWild")
            # traversal all edges with no orientation
            tempOriented = [0] * 12
            for item in tempProgress.pairsCube:
                if(item[1] in range(26,50)):
                    if(tempOriented[(item[1] -2) % 12] == 1):
                        logging.info("assertion failed: tempOriented[(item[1] -2) % 12] == 1")
                        raise CubeErr("assertion failed: tempOriented[(item[1] -2) % 12] == 1")
                    tempOriented[(item[1] -2) % 12] = 1
            tempNotOriented = []
            listBfsEdgeO = []
            for i in range(12):
                if(tempOriented[i] == 0):
                    tempNotOriented.append(i)
            for i in range(2**tempProgress.traversalEdgeWild):
                tempElementBfsEdgeO = []
                for j in range(tempProgress.traversalEdgeWild):
                    if(i & (1 << j)):
                        tempElementBfsEdgeO.append((0, tempNotOriented[j]+26))
                    else:
                        tempElementBfsEdgeO.append((0, tempNotOriented[j]+38))
                listBfsEdgeO.append(tempElementBfsEdgeO)
            for item in listBfsEdgeO:
                tempBfsDeque.append(caseProgress(tempProgress.pairsCube[:]+item[:],[],[],[],0,tempProgress.traversalCornerP,tempProgress.traversalCornerO,tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
                
        elif(len(tempProgress.traversalCornerP) > 0):
            tempCorner = tempProgress.traversalCornerP[0]
            tempTraversalCornerP = tempProgress.traversalCornerP[1:]
            # check which positions are vacant
            tempVacantCorner = [1] * 8
            for item in tempProgress.pairsCube:
                if(item[0] in range(8) and item[1] in range(12,20)):
                    tempVacantCorner[item[1]-12] = 0
            for i in range(8):
                if(tempVacantCorner[i] == 1):
                    tempPairsCube = tempProgress.pairsCube[:] + [(tempCorner, i+12)]
                    tempBfsDeque.append(caseProgress(tempPairsCube[:],[],[],[],0,tempTraversalCornerP[:],tempProgress.traversalCornerO,tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            continue

        elif(len(tempProgress.traversalCornerO) > 0):
            tempCorner = tempProgress.traversalCornerO[0]
            tempTraversalCornerO = tempProgress.traversalCornerO[1:]
            # check whether tempProgress.pairsCube has a pair with (0,tempCorner+38/46/54)
            for item in tempProgress.pairsCube:
                if(item[0] == 0 and (item[1] == tempCorner+50 or item[1] == tempCorner+58 or item[1] == tempCorner+66)):
                    raise CubeErr("Error: pairsCube has a pair with (0,tempCorner+38/46/54)")
            # only three cases
            tempPairsCube1 = tempProgress.pairsCube[:] + [(0,tempCorner+50)]
            tempPairsCube2 = tempProgress.pairsCube[:] + [(0,tempCorner+58)]
            tempPairsCube3 = tempProgress.pairsCube[:] + [(0,tempCorner+66)]
            tempBfsDeque.append(caseProgress(tempPairsCube1[:],[],[],[],0,[],tempTraversalCornerO[:],tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            tempBfsDeque.append(caseProgress(tempPairsCube2[:],[],[],[],0,[],tempTraversalCornerO[:],tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            tempBfsDeque.append(caseProgress(tempPairsCube3[:],[],[],[],0,[],tempTraversalCornerO[:],tempProgress.traversalCornerOp,tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            continue
        
        elif(len(tempProgress.traversalCornerOp) > 0):
            tempCorner = tempProgress.traversalCornerOp[0]
            tempTraversalCornerOp = tempProgress.traversalCornerOp[1:]
            # check which positions are vacant
            tempVacantCorner = [1] * 8
            for item in tempProgress.pairsCube:
                if(item[0] in range(8) and item[1] in range(12,20)):
                    tempVacantCorner[item[1]-12] = 0
            for i in range(8):
                if(tempVacantCorner[i] == 1):
                    # check if pairsCube has relative oriention info
                    for item in tempProgress.pairsCube:
                        if(item[1] in [i+50,i+58,i+66]):
                            raise CubeErr("traversalCornerOp has relative orientation info")
                    
                    # three cases
                    tempPairsCube1 = tempProgress.pairsCube[:] + [(tempCorner, i+12),(0,i+50)]
                    tempPairsCube2 = tempProgress.pairsCube[:] + [(tempCorner, i+12),(0,i+58)]
                    tempPairsCube3 = tempProgress.pairsCube[:] + [(tempCorner, i+12),(0,i+66)]
                    tempBfsDeque.append(caseProgress(tempPairsCube1[:], [],[],[],0,[],[],tempTraversalCornerOp[:],tempProgress.traversalCornerWild,tempProgress.traversalCentre))
                    tempBfsDeque.append(caseProgress(tempPairsCube2[:], [],[],[],0,[],[],tempTraversalCornerOp[:],tempProgress.traversalCornerWild,tempProgress.traversalCentre))
                    tempBfsDeque.append(caseProgress(tempPairsCube3[:], [],[],[],0,[],[],tempTraversalCornerOp[:],tempProgress.traversalCornerWild,tempProgress.traversalCentre))
            continue

        elif(tempProgress.traversalCornerWild>0):
            raise CubeErr("not supported")
        
        elif(len(tempProgress.traversalCentre) > 0):
            tempCentre = tempProgress.traversalCentre[0]
            if(tempCentre % 2 == 0):
                tempCenterPaired = tempCentre + 1
            else:
                tempCenterPaired = tempCentre - 1
            if(len(tempProgress.traversalCentre) == 1 or tempProgress.traversalCentre[1] != tempCenterPaired):
                raise CubeErr("Unpaired traverselCentre")
            
            tempTraversalCentre = tempProgress.traversalCentre[2:]
            # check which positions are vacant
            tempVacantCentre = [1]* 6
            for item in tempProgress.pairsCube:
                if(item[0] in range(6) and item[1] in range(20,26)):
                    tempVacantCentre[item[1]-20] = 0
            for i in range(0,6):
                if(tempVacantCentre[i] == 1):
                    if(i % 2 ==0):
                        j = i + 1
                    else:
                        j = i - 1
                    tempPairsCube = tempProgress.pairsCube[:] + [(tempCentre, i+20),(tempCenterPaired, j+20)]
                    tempBfsDeque.append(caseProgress(tempPairsCube[:],[],[],[],0,[],[],[],0,tempTraversalCentre[:]))
            continue

        else:
            # all set, check if it is legal
            tempPairsCube = tempProgress.pairsCube[:]
            tempPairsCube = sorted(tempPairsCube, key=lambda item:item[1])
            # and then convert to string
            tempStr = ""
            for item in tempPairsCube:
                tempStr += str(item[0]) + " " + str(item[1]) + " "
            tempStr = tempStr.rstrip()
            logging.info(tempStr)
            if(cube.IsLegalString(tempStr)):
                results.append(tempStr)
    
    with open("case/"+str(methodName)+"/case_"+str(intState1)+"_"+str(intState2)+".txt","w") as f:
        for i in range(len(results)):
            f.write("Case "+str(i)+"\n")
            f.write(results[i]+"\n")
            
    
        

def GenerateBfsStartEnd(str1,str2):
    result1 = np.zeros((12, 74),dtype=np.int8)
    result2 = np.zeros((12, 74),dtype=np.int8)
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
        # check if any pair with second tempPosition+26
        j = i
        while(j<len(tempPairs1)):
            if(tempPairs1[j][1] in [tempPosition+26,tempPosition+38]):
                break
            j+=1
        if(j>=len(tempPairs1)):
            # no orientation
            tempHasOrientation = False
        else:
            tempHasOrientation = True
        
        # find the pair with first tempPairs1[i][0]
        m = 0
        while(m<len(tempPairs2)):
            if(tempPairs2[m][0] == tempPairs1[i][0] and tempPairs2[m][1] in range(0,12)):
                break
            m+=1
        if(m>=len(tempPairs2)):
            raise CubeErr("can not find pair 1")
        result1[tempPairs1[i][0]][tempPairs1[i][1]] = 1
        result2[tempPairs2[m][0]][tempPairs2[m][1]] = 1
        logging.info("result1["+str(tempPairs1[i][0])+"]["+str(tempPairs1[i][1])+"] = 1")
        logging.info("result2["+str(tempPairs2[m][0])+"]["+str(tempPairs2[m][1])+"] = 1")
        if(tempHasOrientation):
            n = m
            while(n<len(tempPairs2)):
                if(tempPairs2[n][1] in [tempPairs2[m][1]+26,tempPairs2[m][1]+38]):
                    break
                n+=1
            if(n>=len(tempPairs2)):
                raise CubeErr("can not find pair 2")
            result1[0][tempPairs1[j][1]] = 1
            result2[0][tempPairs2[n][1]] = 1
            logging.info("result1[0]["+str(tempPairs1[j][1])+"] = 1")
            logging.info("result2[0]["+str(tempPairs2[n][1])+"] = 1")
            del tempPairs1[i]
            del tempPairs1[j-1]
            del tempPairs2[m]
            del tempPairs2[n-1]
        else:
            del tempPairs1[i]
            del tempPairs2[m]
    logging.info(str(tempPairs1))
    logging.info(str(tempPairs2))
    
    #for corner
    while(9):
        i = 0
        while(i<len(tempPairs1)):
            if(tempPairs1[i][0] in range(0,8) and tempPairs1[i][1] in range(12,20)):
                break
            i+=1
        if(i==len(tempPairs1)):
            break
        tempPosition = tempPairs1[i][1]
        # check if any pair with second tempPosition+26
        j = i
        while(j<len(tempPairs1)):
            if(tempPairs1[j][1] in [tempPosition+38,tempPosition+46,tempPosition+54]):
                break
            j+=1
        if(j>=len(tempPairs1)):
            # no orientation
            tempHasOrientation = False
        else:
            tempHasOrientation = True
        
        # find the pair with first tempPairs1[i][0]
        m = 0
        while(m<len(tempPairs2)):
            if(tempPairs2[m][0] == tempPairs1[i][0] and tempPairs2[m][1] in range(12,20)):
                break
            m+=1
        if(m>=len(tempPairs2)):
            raise CubeErr("can not find pair 3")
        result1[tempPairs1[i][0]][tempPairs1[i][1]] = 1
        result2[tempPairs2[m][0]][tempPairs2[m][1]] = 1
        logging.info("result1["+str(tempPairs1[i][0])+"]["+str(tempPairs1[i][1])+"] = 1")
        logging.info("result2["+str(tempPairs2[m][0])+"]["+str(tempPairs2[m][1])+"] = 1")
        if(tempHasOrientation):
            n = m
            while(n<len(tempPairs2)):
                if(tempPairs2[n][1] in [tempPairs2[m][1]+38,tempPairs2[m][1]+46,tempPairs2[m][1]+54]):
                    break
                n+=1
            if(n>=len(tempPairs2)):
                raise CubeErr("can not find pair 2")
            result1[0][tempPairs1[j][1]] = 1
            result2[0][tempPairs2[n][1]] = 1
            logging.info("result1[0]["+str(tempPairs1[j][1])+"] = 1")
            logging.info("result2[0]["+str(tempPairs2[n][1])+"] = 1")
            del tempPairs1[i]
            del tempPairs1[j-1]
            del tempPairs2[m]
            del tempPairs2[n-1]
        else:
            del tempPairs1[i]
            del tempPairs2[m]
    logging.info(str(tempPairs1))
    logging.info(str(tempPairs2))
    
    #for centre
    while(9):
        i = 0
        while(i<len(tempPairs1)):
            if(tempPairs1[i][0] in range(0,6) and tempPairs1[i][1] in range(20,26)):
                break
            i+=1
        if(i==len(tempPairs1)):
            break
        tempPosition = tempPairs1[i][1]
        
        
        # find the pair with first tempPairs1[i][0]
        m = 0
        while(m<len(tempPairs2)):
            if(tempPairs2[m][0] == tempPairs1[i][0] and tempPairs2[m][1] in range(20,26)):
                break
            m+=1
        if(m>=len(tempPairs2)):
            raise CubeErr("can not find pair 3")
        result1[tempPairs1[i][0]][tempPairs1[i][1]] = 1
        result2[tempPairs2[m][0]][tempPairs2[m][1]] = 1
        logging.info("result1["+str(tempPairs1[i][0])+"]["+str(tempPairs1[i][1])+"] = 1")
        logging.info("result2["+str(tempPairs2[m][0])+"]["+str(tempPairs2[m][1])+"] = 1")
        del tempPairs1[i]
        del tempPairs2[m]
    logging.info(str(tempPairs1))
    logging.info(str(tempPairs2))
    # TODO if the rest of tempPairs1 and tempPairs2 have same number of edges with only orientation, please add them. Same for corners
    # count edges
    tempCount1 = 0
    tempCount2 = 0
    for item in tempPairs1:
        if(item[1] in range(26,50)):
            tempCount1+=1
    for item in tempPairs2:
        if(item[1] in range(26,50)):
            tempCount2+=1
    if(tempCount1 == tempCount2):
        for item in tempPairs1:
            if(item[1] in range(26,50)):
                result1[0][item[1]] = 1
                logging.info("result1[0]["+str(item[1])+"] = 1")
        for item in tempPairs2:
            if(item[1] in range(26,50)):
                result2[0][item[1]] = 1
                logging.info("result2[0]["+str(item[1])+"] = 1")
    
    # count corners
    tempCount1 = 0
    tempCount2 = 0
    for item in tempPairs1:
        if(item[1] in range(50,74)):
            tempCount1+=1
    for item in tempPairs2:
        if(item[1] in range(50,74)):
            tempCount2+=1
    if(tempCount1 == tempCount2):
        for item in tempPairs1:
            if(item[1] in range(50,74)):
                result1[0][item[1]] = 1
                logging.info("result1[0]["+str(item[1])+"] = 1")
        for item in tempPairs2:
            if(item[1] in range(50,74)):
                result2[0][item[1]] = 1
                logging.info("result2[0]["+str(item[1])+"] = 1")
    return result1,result2
    
def Bfs(strMethod,idStart,idEnd):
    tempPath = strMethod+"_allowMove.txt"
    if(not os.path.exists(tempPath)):
        raise CubeErr(tempPath + "not found ")
    
    listAllowStr = []
    with open(tempPath,"r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if(lines[i].rstrip()==str(idStart)+" "+str(idEnd)):
                tempSplit = lines[i+1].rstrip().split()
                for item in tempSplit:
                    listAllowStr.append(item)
                if(lines[i+2].rstrip() == "small"):
                    table = copy.deepcopy(cube.tableSmall)
                    bfsSmall = True
                else:
                    table = copy.deepcopy(cube.tableBig)
                    bfsSmall = False
    logging.info(str(listAllowStr))
    listAllowIndex = []
    for item in listAllowStr:
        if(item not in cube.dictIndex):
            raise CubeErr("invalid move "+item)
        else:
            listAllowIndex.append(cube.dictIndex[item])
    logging.info(str(listAllowIndex))
    
    for i in range(len(cube.listMoveStr)):
        for j in range(len(cube.listMoveStr)):
            if(i not in listAllowIndex or j not in listAllowIndex):
                table[i][j] = 0
    tempSum = 0
    
    if(cube.dictIndex['M'] not in listAllowIndex and cube.dictIndex['M1'] not in listAllowIndex):
        if(cube.dictIndex['M2'] not in listAllowIndex):
            for i in range(len(cube.listMoveStr)):
                for j in range(len(cube.listMoveStr)):
                    if((cube.listMoveStr[i][-1] == 'R' or (len(cube.listMoveStr[i])>=2 and cube.listMoveStr[i][-2]=='R')) and cube.listMoveStr[j][0] == 'r'):
                        table[i][j] = 0
                    elif(cube.listMoveStr[i] in ['r','r1'] and cube.listMoveStr[j][0] == 'R'):
                        table[i][j] = 0
    
    forwardDeque = deque()
    backwardDeque = deque()
    # first imagine an nop is appended, then popped
    
    # 8 hashes for forward, and 8 for backward
    
    forwardHashList = []
    backwardHashList = []
    for i in range(8):
        forwardHashList.append(dict())
        backwardHashList.append(dict())
    
    tempPath = strMethod+"_state.txt"
    if(not os.path.exists(tempPath)):
        raise CubeErr("no such file "+tempPath)
    with open(tempPath, "r") as f:
        tempLines = f.readlines()
    for i in range(len(tempLines)):
        if(tempLines[i].strip() == "state "+str(idStart)):
            if(i+1>=len(tempLines)):
                raise CubeErr("no next line")
            tempStrStart = tempLines[i+1].rstrip()
            tempList = tempLines[i+1].rstrip().split()
        if(tempLines[i].strip() == "state "+str(idEnd)):
            if(i+1>=len(tempLines)):
                raise CubeErr("no next line")
            tempStrEnd = tempLines[i+1].rstrip()
    tempCubeStart, tempCubeEnd = GenerateBfsStartEnd(tempStrStart, tempStrEnd)
    
    if(np.equal(tempCubeStart,tempCubeEnd).all()):
        shifting = False
    else:
        shifting = True
        listBfsToItself1 = []
        listBfsToItself2 = []
    tempCube = np.zeros((12, 74),dtype=np.int8)
    if(len(tempList) % 2 != 0):
        raise CubeErr("len(tempList) not an even number")
    for i in range(0,len(tempList),2):
        tempCube[int(tempList[i]),int(tempList[i+1])] = 1
    tempHashStart = calHash1(tempCubeStart)
    
    forwardHashList[0][tempHashStart] = []
    temp = cube.dictIndex['N'] * len(cube.listMoveStr) + cube.dictIndex['N']
    forwardHashList[0][tempHashStart].append(bfsHashElement("N","N",'N',temp,0, 0.0))
    # then moves with length 1 are appended
    startCube = copy.deepcopy(tempCubeStart)
    endCube = copy.deepcopy(tempCubeEnd)
    for item in listAllowStr:
        temp = cube.dictIndex['N'] * len(cube.listMoveStr) + cube.dictIndex[item]
        forwardDeque.append(bfsDequeElement(startCube@cube.dictMove[item], item,item,'N',temp,1,cube.dictScore[item]))
    
    while(len(forwardDeque) > 0):
        tempBfsElement = forwardDeque.popleft()
        tempLastMove = tempBfsElement.lastMove
        tempHashTuple = cube.calHash1(tempBfsElement.cube)
        
        if(np.array_equal(tempBfsElement.cube,endCube) and tempBfsElement.moveNum >= 3):
            continue
        
        if(shifting and np.array_equal(tempBfsElement.cube,startCube)):
            listBfsToItself1.append(copy.deepcopy(tempBfsElement))
            continue
        
        if(tempHashTuple not in forwardHashList[tempBfsElement.moveNum]):
            forwardHashList[tempBfsElement.moveNum][tempHashTuple] = []
        forwardHashList[tempBfsElement.moveNum][tempHashTuple].append(bfsHashElement(tempBfsElement.move,tempBfsElement.lastMove, tempBfsElement.dualMove, tempBfsElement.intFirst2,tempBfsElement.moveNum, tempBfsElement.points))
        
        if(np.array_equal(tempBfsElement.cube,endCube)):
            continue
        
        if(tempBfsElement.moveNum >= 4):
            continue
        # then append some bfs elements to the deque
        for j in range(len(cube.listMoveStr)):
            if(table[cube.dictIndex[tempLastMove]][j] == 0):
                continue
            if(tempBfsElement.dualMove == cube.listMoveParallel[j]):
                continue
            #  if dualMove --- nextMove, continue
            if(tempBfsElement.intFirst2 in cube.dict3Forward and j in cube.dict3Forward[tempBfsElement.intFirst2]):
                continue
            
            if(cube.dictParallelMove[tempBfsElement.lastMove] == cube.listMoveParallel[j]):
                tempDualMove = cube.listMoveParallel[j]
            else:
                tempDualMove = 'N'
                
            temp = tempBfsElement.intFirst2 % len(cube.listMoveStr) * len(cube.listMoveStr) + j
            forwardDeque.append(bfsDequeElement(tempBfsElement.cube @ cube.listMoveMatrix[j], tempBfsElement.move +" "+cube.listMoveStr[j],cube.listMoveStr[j],tempDualMove,temp,tempBfsElement.moveNum+1,tempBfsElement.points+cube.listScore[j]))
    
    #bfs reverse
    
    tempHashEnd = calHash1(tempCubeEnd)
    
    backwardHashList[0][tempHashEnd] = []
    temp = cube.dictIndex['N'] * len(cube.listMoveStr) + cube.dictIndex['N']
    backwardHashList[0][tempHashEnd].append(bfsHashElement("N","N",'N',temp,0,0.0))
    #pay attention 'last move' is actually the move done first, in real solve
    #then moves with length 1 are appended
    startCube = copy.deepcopy(tempCubeEnd)
    endCube = copy.deepcopy(tempCubeStart)
    for item in listAllowStr:
        temp = cube.dictIndex['N'] * len(cube.listMoveStr) + cube.dictIndex[item]
        backwardDeque.append(bfsDequeElement(startCube@cube.dictReverseMove[item],item,item,'N',temp,1,cube.dictScore[item]))
    
    while(len(backwardDeque)>0):
        tempBfsElement = backwardDeque.popleft()
        tempHashTuple = cube.calHash1(tempBfsElement.cube)
        
        if(np.array_equal(tempBfsElement.cube,endCube) and tempBfsElement.moveNum >= 3):
            continue
        
        if(shifting and np.array_equal(tempBfsElement.cube,startCube)):
            listBfsToItself2.append(copy.deepcopy(tempBfsElement))
            continue
        
        if(tempHashTuple not in backwardHashList[tempBfsElement.moveNum]):
            backwardHashList[tempBfsElement.moveNum][tempHashTuple] = []
        backwardHashList[tempBfsElement.moveNum][tempHashTuple].append(bfsHashElement(tempBfsElement.move,tempBfsElement.lastMove,tempBfsElement.dualMove,tempBfsElement.intFirst2,tempBfsElement.moveNum,tempBfsElement.points))
        
        if(np.array_equal(tempBfsElement.cube,startCube)):
            continue
        
        if(tempBfsElement.moveNum >= 4):
            continue
        
        # then append some bfs elements to the queue
        for j in range(len(cube.listMoveStr)):
            if(table[j][cube.dictIndex[tempBfsElement.lastMove]] == 0):
                continue
            if(tempBfsElement.dualMove == cube.listMoveParallel[j]):
                continue
            if(tempBfsElement.intFirst2 in cube.dict3Backward and j in cube.dict3Backward[tempBfsElement.intFirst2]):
                continue
            
            if(cube.dictParallelMove[tempBfsElement.lastMove] == cube.listMoveParallel[j]):
                tempDualMove = cube.listMoveParallel[j]
            else:
                tempDualMove = 'N'
                
            temp = tempBfsElement.intFirst2 % len(cube.listMoveStr) * len(cube.listMoveStr) + j
            
            backwardDeque.append(bfsDequeElement(tempBfsElement.cube @ cube.dictReverseMove[cube.listMoveStr[j]],cube.listMoveStr[j]+" "+tempBfsElement.move,cube.listMoveStr[j],tempDualMove,temp,tempBfsElement.moveNum+1,tempBfsElement.points+cube.listScore[j]))
    
    # stat the number of elements 
    for i in range(8):
        totalSum = 0
        for key in forwardHashList[i]:
            totalSum += len(forwardHashList[i][key])
        logging.info ("forwardHashList %d: %d",i,totalSum)
        totalSum = 0
        for key in backwardHashList[i]:
            totalSum += len(backwardHashList[i][key])
        logging.info ("backwardHashList %d: %d",i,totalSum)

    # sort the 16 hashes
    for i in range(8):
        # sorted_dict = {k: my_dict[k] for k in sorted(my_dict)}
        forwardHashList[i] = {k: forwardHashList[i][k] for k in sorted(forwardHashList[i])}
        backwardHashList[i] = {k: backwardHashList[i][k] for k in sorted(backwardHashList[i])}

    #logging.info("key1 "+str(list(forwardHashList[2].keys())[0:3]))
    # pair the elements in forward hash and backward hash
    algFound = 0
    listStrAlg = []
    for i in range(0,8):
        for j in range(max(i-1,0),min(i+1,8)):
            # use the ladder to compare alg
            footForward = 0
            footBackward = 0
            footForwardMax = len(forwardHashList[i])-1
            footBackwardMax = len(backwardHashList[j])-1
            listKeyForward = list(forwardHashList[i].keys())
            listKeyBackward = list(backwardHashList[j].keys())
            
            #compare the two feet
            while(footForward <= footForwardMax and footBackward <= footBackwardMax):
                if listKeyForward[footForward] == listKeyBackward[footBackward]:
                    for item1 in forwardHashList[i][listKeyForward[footForward]]:
                        for item2 in backwardHashList[j][listKeyBackward[footBackward]]:
                            lastMoveIndex1 = cube.dictIndex[item1.lastMove]
                            lastMoveIndex2 = cube.dictIndex[item2.lastMove]
                            if(table[lastMoveIndex1][lastMoveIndex2] == 0 and item1.lastMove != 'N' and item2.lastMove != 'N'):
                                continue
                            if((item1.dualMove == cube.dictParallelMove[item2.lastMove] or item2.dualMove == cube.dictParallelMove[item1.lastMove]) and item1.lastMove != 'N' and item2.lastMove != 'N'):
                                continue
                            if(item1.intFirst2 in cube.dict3Forward and cube.dictIndex[item2.lastMove] in cube.dict3Forward[item1.intFirst2]):
                                continue
                            if(item2.intFirst2 in cube.dict3Backward and cube.dictIndex[item1.lastMove] in cube.dict3Backward[item2.intFirst2]):
                                continue
                            if(item1.points + item2.points > 18.28):
                                continue
                            if(item1.move=="N" and item2.move=="N"):
                                tempMove = "N"
                            elif(item2.move=="N"):
                                tempMove = item1.move
                            else:
                                tempMove = item1.move + " " + item2.move
                                
                            logging.info("Found alg: "+str(tempMove))
                            
                            
                            # generate the transferReverse and add to it
                            tempSplit = tempMove.rstrip().split()
                            tempSplit.reverse()
                            tempTransferReverse = np.eye(74,dtype=np.int8)
                            for item in tempSplit:
                                tempTransferReverse = tempTransferReverse @ cube.dictReverseMove[item]
                            # initialize the item to append
                            listStrAlg.append(Alg(tempTransferReverse, tempMove, item1.points + item2.points))
                            algFound += 1
                    footForward += 1
                    footBackward += 1
                    continue
                elif listKeyForward[footForward] < listKeyBackward[footBackward]:
                    footForward += 1
                    continue
                else:
                    footBackward += 1
                    continue
    logging.info("algFound: %d",algFound)
    
    # Then check if no cases share the same hash 
    tempPath = "case/"+strMethod+"/case_"+str(idStart)+"_"+str(idEnd)+".txt"
    if (not os.path.exists(tempPath)):
        raise CubeErr(str(tempPath)+" does not exist")

    with open(tempPath, "r") as f:
        tempLines = f.readlines()
    
    BFSCaseNum = len(tempLines)//2
    
    dictCase = {}
    for i in range(0,len(tempLines),2):
        tempLine0 = tempLines[i].rstrip()
        tempLine1 = tempLines[i+1].rstrip()
        tempIndex = int(tempLine0.split()[1])
        tempCube = np.zeros((12, 74),dtype=np.int8)
        tempSplit1 = tempLine1.split()
        for j in range(0, len(tempSplit1),2):
            tempCube[int(tempSplit1[j]),int(tempSplit1[j+1])] = 1
        tempHash = cube.calHash1(tempCube)
        if (tempHash not in dictCase):
            dictCase[tempHash] = []
        dictCase[tempHash].append(tempIndex)
        
    NoSame =  True    
    for key in dictCase:
        if (len(dictCase[key]) > 1):
            logging.info("Hash %s is shared by %d cases",str(key),len(dictCase[key]))
            NoSame = False
            raise CubeErr("Hash is shared by multiple cases")
    logging.info("No same hash: "+str(NoSame))
    
    # Traversel each alg, calculate the hash and then slot
    tempPath = strMethod+"_state.txt"
    if (not os.path.exists(tempPath)):
        raise CubeErr(str(tempPath)+" does not exist")

    with open(tempPath, "r") as f:
        tempLines = f.readlines()
    tempLines = [x.rstrip() for x in tempLines]
    for i in range(0, len(tempLines)):
        if(tempLines[i] == "state "+str(idEnd)):
            tempLine1 = tempLines[i+1]
            break
    
    fineCube = np.zeros((12,74), dtype=np.int8)
    tempSplit1 = tempLine1.split()
    for i in range(0, len(tempSplit1), 2):
        fineCube[int(tempSplit1[i])][int(tempSplit1[i+1])] = 1
        
    
    tempPath = "case/"+strMethod+"/case_"+str(idStart)+"_"+str(idEnd)+".txt"
    if (not os.path.exists(tempPath)):
        raise CubeErr(str(tempPath)+" does not exist")

    with open(tempPath, "r") as f:
        tempLines = f.readlines()
        
    tempCaseNum = len(tempLines) // 2
    
    listAlgForAllCases = []
    
    # Set the maxLength of WinnerAlgs according to the tempCaseNum.
    tempMaxLength = 0
    tempMaxLength = 3000 // tempCaseNum
    if(tempMaxLength < 2):
        tempMaxLength = 2
    if(tempMaxLength > 7):
        tempMaxLength = 7
    
    for i in range(tempCaseNum):
        listAlgForAllCases.append(WinnerAlgs(tempMaxLength))
          
    for item in listStrAlg:
        tempCube = copy.deepcopy(fineCube)
        tempCube = tempCube @ item.transferReverse
        
        tempHash = cube.calHash1(tempCube)
        
        if(tempHash in dictCase):
            tempIndex = dictCase[tempHash][0]
            
        else:
            logging.info("hash error")
            raise CubeErr("hash error")
        
        # judge if it is the winner using tempIndex
        listAlgForAllCases[tempIndex].judge(copy.deepcopy(item))
        
    logging.info("All alg hash calculation done")
    
    # Stat how many cases already have algs
    tempHasAlg = 0
    for i in range(len(listAlgForAllCases)):
        for item in listAlgForAllCases[i].winnerAlgs:
            tempMove = item.move
            tempPoints  = item.points
            # logging.info("case"+str(i)+" move="+str(tempMove)+" points="+str(tempPoints))
        if(len(listAlgForAllCases[i].winnerAlgs)!=0):
            tempHasAlg+=1
    logging.info("has alg cases:"+str(tempHasAlg))
    
    # For shifting==True cases, transfer bfs elements into algs, and then sort. 
    if(shifting):
        listAlgItself1 = []
        listAlgItself2 = []
        for item in listBfsToItself1:
            tempMove = item.move
            tempSplit = tempMove.rstrip().split()
            tempSplit.reverse()
            tempPoints = item.points
            tempTransferReverse = np.eye(74,dtype=np.int8)
            for item2 in tempSplit:
                tempTransferReverse = tempTransferReverse @ cube.dictReverseMove[item2]
            listAlgItself1.append(Alg(tempTransferReverse, tempMove, tempPoints))
        for item in listBfsToItself2:
            tempMove = item.move
            tempSplit = tempMove.rstrip().split()
            tempSplit.reverse()
            tempPoints = item.points
            tempTransferReverse = np.eye(74,dtype=np.int8)
            for item2 in tempSplit:
                tempTransferReverse = tempTransferReverse @ cube.dictReverseMove[item2]
            listAlgItself2.append(Alg(tempTransferReverse, tempMove, tempPoints))
        listAlgItself1.sort(key=lambda x: x.points)
        listAlgItself2.sort(key=lambda x: x.points)
        listAlgItself1 = listAlgItself1[:50]
        listAlgItself2 = listAlgItself2[:50]
        for i in range(len(listAlgItself1)):
            logging.info("move "+str(listAlgItself1[i].move)+" points "+str(listAlgItself1[i].points))
        for i in range(len(listAlgItself2)):
            logging.info("move "+str(listAlgItself2[i].move)+" points "+str(listAlgItself2[i].points))
    
    
    
    # The last section is to combine algs with small points
    # capture some algs with smallest points
    listGoodAlg = []
    GOOD_ALG_NUM = 50
    for i in range(GOOD_ALG_NUM):
        listGoodAlg.append(Alg(np.eye(74,dtype=np.int8), "fool", 8191))
    for tempWinnerAlgs in listAlgForAllCases:
        for tempAlg  in tempWinnerAlgs.winnerAlgs:
            if(tempAlg.points<listGoodAlg[GOOD_ALG_NUM-1].points and tempAlg.move[0] not in ["N","x","y","z"]):
                listGoodAlg[GOOD_ALG_NUM-1] = tempAlg
                listGoodAlg.sort(key=lambda x: x.points)
        for tempAlg in tempWinnerAlgs.lengthOneAlgs:
            if(tempAlg.points<listGoodAlg[GOOD_ALG_NUM-1].points and tempAlg.move[0] not in ["N","x","y","z"]):
                listGoodAlg[GOOD_ALG_NUM-1] = tempAlg
                listGoodAlg.sort(key=lambda x: x.points)
                
    # Add a lock that blocks all algs with points >= min(bestx3.6,best+7.5)
    for goodNumber in range(GOOD_ALG_NUM):
        if(listGoodAlg[goodNumber].points>=min(listGoodAlg[0].points*3.6,listGoodAlg[0].points+7.5)):
            break
    
    for i in range(goodNumber):
        logging.info("good alg "+str(i)+" move="+str(listGoodAlg[i].move)+" points="+str(listGoodAlg[i].points))
        
    
    
    # TODO just cat good algs and generated algs together, calculate the hash and then put into the alg table, and then clean the table
    if(not shifting):
        tempAddAlg = []
        remainIterations = 3
        tempPreviousHasAlg = 0
        while(remainIterations>0):
            tempAddAlg.clear()
            for i in range(BFSCaseNum):
                tempAddAlg.append([])
            for tempWinnerAlgs in listAlgForAllCases:
                for tempAlg in tempWinnerAlgs.winnerAlgs:
                    if(tempAlg.move == "N"):
                        continue
                    # for tempGoodAlgIndex in listGoodAlg:
                    for tempGoodAlgIndex in range(goodNumber):
                        tempGoodAlg = listGoodAlg[tempGoodAlgIndex]
                        # we know that N is not included in tempGoodAlg
                        # we need to check if xyz are stuck in the middle
                        if(tempAlg.move[0] not in ["x","y","z"]):
                            tempAlg0 = Alg(tempAlg.transferReverse @ tempGoodAlg.transferReverse, tempGoodAlg.move + " " + tempAlg.move, tempGoodAlg.points + tempAlg.points)
                            tempCube = copy.deepcopy(fineCube)
                            tempHash = cube.calHash1(tempCube @ tempAlg0.transferReverse)
                            if(tempHash not in dictCase):
                                raise CubeErr ("Hash not found 0")
                            tempIndex = dictCase[tempHash][0]
                            tempAddAlg[tempIndex].append(copy.deepcopy(tempAlg0))
                        # tempAlg1
                        if(tempGoodAlg.move[0] not in ["x","y","z"]):
                            tempAlg1 = Alg(tempGoodAlg.transferReverse @ tempAlg.transferReverse, tempAlg.move + " " + tempGoodAlg.move, tempGoodAlg.points + tempAlg.points)
                            tempCube = copy.deepcopy(fineCube)
                            tempHash = cube.calHash1(tempCube @ tempAlg1.transferReverse)
                            if(tempHash not in dictCase):
                                raise CubeErr ("Hash not found 1")
                            tempIndex = dictCase[tempHash][0]
                            tempAddAlg[tempIndex].append(copy.deepcopy(tempAlg1))
            for i in range(BFSCaseNum):
                for item in tempAddAlg[i]:
                    listAlgForAllCases[i].judge(item)
            
            tempHasAlg = 0
            for i in range(BFSCaseNum):
                if(len(listAlgForAllCases[i].winnerAlgs) > 0):
                    tempHasAlg += 1
            logging.info("has alg cases:"+str(tempHasAlg))
            if(tempPreviousHasAlg == tempHasAlg):
                remainIterations -= 0
            else:
                tempPreviousHasAlg = tempHasAlg
            remainIterations -= 1
                
    else: # if shifting
        tempAddAlg = []
        remainIterations = 4
        tempPreviousHasAlg = 0
        while(remainIterations>0):
            tempAddAlg.clear()
            for i in range(BFSCaseNum):
                tempAddAlg.append([])
            for tempWinnerAlgs in listAlgForAllCases:
                for tempAlg in tempWinnerAlgs.winnerAlgs:
                    if(tempAlg.move == "N"):
                        continue
                    for tempItself1 in listAlgItself1:
                        tempAlg1 = Alg(tempAlg.transferReverse @ tempItself1.transferReverse, 
                                    tempItself1.move + " " + tempAlg.move,
                                    tempItself1.points + tempAlg.points)
                        tempCube = copy.deepcopy(fineCube)
                        tempHash = cube.calHash1(tempCube @ tempAlg1.transferReverse)
                        if(tempHash not in dictCase):
                            tempCube2 = tempCube @ tempAlg1.transferReverse
                            for ro in range(12):
                                for col in range(74):
                                    if(tempCube2[ro][col]==1):
                                        logging.info("At: " + str(ro) + " " + str(col))
                            logging.info("At move: "+str(tempItself1.move))
                            logging.info("At move: "+str(tempAlg.move))
                            raise CubeErr ("Hash not found 1")
                        tempIndex = dictCase[tempHash][0]
                        tempAddAlg[tempIndex].append(copy.deepcopy(tempAlg1))
                        
                    for tempItself2 in listAlgItself2:
                        tempAlg2 = Alg(tempItself2.transferReverse @ tempAlg.transferReverse, 
                                    tempAlg.move + " " + tempItself2.move,
                                    tempItself2.points + tempAlg.points)
                        tempCube = copy.deepcopy(fineCube)
                        tempHash = cube.calHash1(tempCube @ tempAlg2.transferReverse)
                        if(tempHash not in dictCase):
                            raise CubeErr ("Hash not found 2")
                        tempIndex = dictCase[tempHash][0]
                        tempAddAlg[tempIndex].append(copy.deepcopy(tempAlg2))
            for i in range(BFSCaseNum):
                for item in tempAddAlg[i]:
                    listAlgForAllCases[i].judge(item)
                    
            tempHasAlg = 0
            for i in range(BFSCaseNum):
                if(len(listAlgForAllCases[i].winnerAlgs) > 0):
                    tempHasAlg += 1
            logging.info("has alg cases:"+str(tempHasAlg))
            tempPreviousHasAlg = tempHasAlg
            
            remainIterations -= 1           
    
    tempFolder = "alg/"+strMethod
    if(not os.path.exists(tempFolder)):
        raise CubeErr("Folder not found")
    tempPath = tempFolder+"/case_"+str(idStart)+"_"+str(idEnd)+".txt"
    with open(tempPath,"w") as f:
        for i in range(BFSCaseNum):
            for tempAlg in listAlgForAllCases[i].winnerAlgs:
                tempMove = tempAlg.move
                tempPoints = tempAlg.points
                f.write("case"+str(i)+" move="+str(tempMove)+" points="+str(tempPoints)+"\012")
                    
def Solve(listScramble):
    # construct a fine cube
    fine = np.zeros((12, 74),dtype=np.int8)
    fine[:12, :12] = np.eye(12,dtype=np.int8)
    fine[:8,12:20] = np.eye(8,dtype=np.int8)
    fine[:6,20:26] = np.eye(6,dtype=np.int8)
    for i in range(26,38):
        fine[0,i] = 1
    for i in range(50,58):
        fine[0,i] = 1
    
    matrixScramble = SolveAlg(listScramble,1).moveMatrix
    scrambledCube = fine @ matrixScramble
    tempStr = ""
    tempCube = copy.deepcopy(scrambledCube)
    listSolution = []
    tempPoints = 0
    
    listBefore = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    listAfter = [[2],[3,4],[5],[6],[7],[8],[9],[9],[10],[11,12],[13],[13],[14],[15],[16],[17]]
    dictBeforeAfter = dict(zip(listBefore,listAfter))
    
    tempPairs = [(1,2),(2,3),(3,5),(5,7),(7,9),(9,10),(10,11),(11,13),(13,14),(14,15),(15,16),(16,17)]
    dequeBfs = deque()
    dequeBfs.append(SolveMove(scrambledCube, [], 0, 1))
    listResult = []
    
    while(len(dequeBfs) > 0):
        tempSolveMove  = dequeBfs.popleft()
        # pop out if currState == 17
        if(tempSolveMove.currState == 17):
            listResult.append(copy.deepcopy(tempSolveMove))
            continue
        
        # throw if currState not in dictBeforeAfter
        if(tempSolveMove.currState not in dictBeforeAfter):
            raise CubeErr("currState not in dictBeforeAfter")
        
        # traversal dictBeforeAfter[currState] and acquire the algs
        tempStrBefore = ""
        for i in range(74):
            for j in range(12):
                if(tempSolveMove.currMatrix[j,i]==1):
                    tempStrBefore = tempStrBefore + str(j) + " " + str(i) + " "
                    
        # logging.info(tempStrBefore)
        
        for item in dictBeforeAfter[tempSolveMove.currState]:
            tempAlgList = solveSlotCase.Slot(tempStrBefore, "Roux_v1", tempSolveMove.currState, item)
            for i in range(0,min(len(tempAlgList),2)):
                tempAlg = tempAlgList[i]
                tempCube = copy.deepcopy(tempSolveMove.currMatrix) @ tempAlg.moveMatrix
                tempPoints = tempSolveMove.points + tempAlg.points
                tempMove = tempSolveMove.move[:] + tempAlg.move[:]
                dequeBfs.append(SolveMove(copy.deepcopy(tempCube), tempMove, tempPoints, item))
            
    print(len(listResult))
    # sort the listResult according to *.points
    listResult.sort(key=lambda x: x.points, reverse=False)
    for i in range(0,min(1000,len(listResult))):
        item = listResult[i]
        logging.info(item.move)
        logging.info(item.points)
        
def Solve_v2(listScramble):
    # construct a fine cube
    fine = np.zeros((12, 74),dtype=np.int8)
    fine[:12, :12] = np.eye(12,dtype=np.int8)
    fine[:8,12:20] = np.eye(8,dtype=np.int8)
    fine[:6,20:26] = np.eye(6,dtype=np.int8)
    for i in range(26,38):
        fine[0,i] = 1
    for i in range(50,58):
        fine[0,i] = 1
    
    matrixScramble = SolveAlg(listScramble,1).moveMatrix
    scrambledCube = fine @ matrixScramble
    tempStr = ""
    tempCube = copy.deepcopy(scrambledCube)
    listSolution = []
    tempPoints = 0
    
    listBefore = [1,2,3,4,5,6,7,8,9,10,11]
    listAfter = [[2,3],[4],[4],[5],[6],[7],[8,9],[10,11],[10,11],[12],[12]]
    dictBeforeAfter = dict(zip(listBefore,listAfter))
    
    tempPairs = [(1,2),(2,4),(4,5),(5,6),(6,7),(7,8),(8,10),(10,12)]
    dequeBfs = deque()
    dequeBfs.append(SolveMove(scrambledCube, [], 0, 1))
    listResult = []
    
    while(len(dequeBfs) > 0):
        tempSolveMove  = dequeBfs.popleft()
        # pop out if currState == 17
        if(tempSolveMove.currState == 12):
            listResult.append(copy.deepcopy(tempSolveMove))
            continue
        
        # throw if currState not in dictBeforeAfter
        if(tempSolveMove.currState not in dictBeforeAfter):
            raise CubeErr("currState not in dictBeforeAfter")
        
        # traversal dictBeforeAfter[currState] and acquire the algs
        tempStrBefore = ""
        for i in range(74):
            for j in range(12):
                if(tempSolveMove.currMatrix[j,i]==1):
                    tempStrBefore = tempStrBefore + str(j) + " " + str(i) + " "
                    
        # logging.info(tempStrBefore)
        
        for item in dictBeforeAfter[tempSolveMove.currState]:
            tempAlgList = solveSlotCase.Slot(tempStrBefore, "Roux_v2", tempSolveMove.currState, item)
            for i in range(0,min(len(tempAlgList),3)):
                tempAlg = tempAlgList[i]
                tempCube = copy.deepcopy(tempSolveMove.currMatrix) @ tempAlg.moveMatrix
                tempPoints = tempSolveMove.points + tempAlg.points
                tempMove = tempSolveMove.move[:] + tempAlg.move[:]
                dequeBfs.append(SolveMove(copy.deepcopy(tempCube), tempMove, tempPoints, item))
                
    print(len(listResult))
    # sort the listResult according to *.points
    listResult.sort(key=lambda x: x.points, reverse=False)
    for i in range(0,min(1000,len(listResult))):
        item = listResult[i]
        logging.info(item.move)
        logging.info(item.points)
    
if __name__ == "__main__":
    tempStr = "x2 z B F U F D R1 F D L B2 U1 B2 D B1 R1 F2 L2 R2 U1"
    tempScramble = tempStr.split()
    Solve(tempScramble)