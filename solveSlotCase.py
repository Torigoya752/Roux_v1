import numpy as np
import cube
from cube import CubeErr, calHash1
import os
import sys
import copy
from collections import deque
import logging
import block2bfs
import solve


def Slot(strCube, strMethod, stateStart, stateEnd):
    # check file
    tempPath = strMethod+"_state.txt"
    if not os.path.exists(tempPath):
        raise CubeErr("File not exist: "+str(tempPath))
    
    # read file
    with open(tempPath, "r") as f:
        lines = f.readlines()
    listStrip = []
    for line in lines:
        listStrip.append(line.rstrip())
        
    tempStrStart = "XXX"
    tempStrEnd = "XXX"
            
    for i in range(len(listStrip)):
        if(listStrip[i] == "state "+str(stateStart)):
            tempStrStart = listStrip[i+1]
        elif(listStrip[i] == "state "+str(stateEnd)):
            tempStrEnd = listStrip[i+1]
    if(tempStrStart == "XXX" or tempStrEnd == "XXX"):
        raise CubeErr("state not exist")
    
    # get the travel items through block2bfs
    traversalEdgeOp,traversalEdgeO,traversalEdgeP,traversalEdgeWild,traversalCornerOp,traversalCornerO,traversalCornerP,traversalCornerWild,traversalCentre = block2bfs.BlockToBfs(tempStrStart, tempStrEnd, stateStart, stateEnd, strMethod)
    
    # split the strCube
    tempSplit = strCube.rstrip().split()
    if(len(tempSplit)%2!=0):
        raise CubeErr("strCube not even")
    tempPairs = []
    for i in range(0,len(tempSplit),2):
        tempPairs.append((int(tempSplit[i]),int(tempSplit[i+1])))
        
    # prepare an empty list that stores all valid information in strCube
    listValid = []
    
    # previous state
    tempStart = tempStrStart.rstrip().split()
    if(len(tempStart)%2!=0):
        raise CubeErr("stateStart not even")
    for i in range(0,len(tempStart),2):
        listValid.append((int(tempStart[i]),int(tempStart[i+1])))
        
    # traversalEdgeOp
    for item in traversalEdgeOp:
        # traversal tempPairs, get the one with first that is item and second in range 0-12
        for i in range(len(tempPairs)):
            if(tempPairs[i][0] == item and tempPairs[i][1] in range(0,12)):
                tempPosition = tempPairs[i][1]
                listValid.append((item,tempPosition))
                if((0,tempPosition+26) in tempPairs):
                    listValid.append((0,tempPosition+26))
                elif((0,tempPosition+38) in tempPairs):
                    listValid.append((0,tempPosition+38))
                else:
                    raise CubeErr("traversalEdgeOp error, no orentation")
                
    
    # traversalEdgeO
    for item in traversalEdgeO:
        # only check an orientation block
        for i in range(len(tempPairs)):
            if(tempPairs[i] == (0,item+26) or tempPairs[i] == (0,item+38)):
                listValid.append((0,tempPairs[i][1]))
                
    # traversalEdgeP
    for item in traversalEdgeP:
        # only check the permutation
        for i in range(len(tempPairs)):
            if(tempPairs[i][0]==item and tempPairs[i][1] in range(0,12)):
                listValid.append((item,tempPairs[i][1]))
                
    # traversalEdgeWild
    if(traversalEdgeWild > 0):
        for i in range(len(tempPairs)):
            if(tempPairs[i][0]==0 and tempPairs[i][1] in range(26,50)):
                listValid.append((0,tempPairs[i][1]))
    
    # traversalCornerOp
    for item in traversalCornerOp:
        for i in range(len(tempPairs)):
            if(tempPairs[i][0] == item and tempPairs[i][1] in range(12,20)):
                tempPosition = tempPairs[i][1]
                listValid.append((item,tempPosition))
                if((0,tempPosition+38) in tempPairs):
                    listValid.append((0,tempPosition+38))
                elif((0,tempPosition+46) in tempPairs):
                    listValid.append((0,tempPosition+46))
                elif((0,tempPosition+54) in tempPairs):
                    listValid.append((0,tempPosition+54))
                else:
                    raise CubeErr("traversalCornerOp error, no orientation")
                
    # traversalCornerO
    for item in traversalCornerO:
        for i in range(len(tempPairs)):
            if(tempPairs[i]==(0,item+50) or tempPairs[i]==(0,item+58) or tempPairs[i]==(0,item+66)):
                listValid.append((0,tempPairs[i][1]))
                
    # traversalCornerP
    for item in traversalCornerP:
        for i in range(len(tempPairs)):
            if(tempPairs[i][0]==item and tempPairs[i][1] in range(12,20)):
                listValid.append((item,tempPairs[i][1]))
                
    # traversalCornerWild
    if(traversalCornerWild > 0):
        for i in range(len(tempPairs)):
            if(tempPairs[i][0] == 0 and tempPairs[i][1] in range(50,74)):
                listValid.append((0,tempPairs[i][1]))
                
    # traversalCentre
    for item in traversalCentre:
        for i in range(len(tempPairs)):
            if(tempPairs[i][0] == item and tempPairs[i][1] in range(20,26)):
                listValid.append((item,tempPairs[i][1]))
                
    # sort listValid according to the index 1 of the pair
    listValid = list(set(listValid))
    listValid.sort(key=lambda x: x[1])
    
    # logging.info(str(listValid))
    
    # return all algorithms that can be used
    
    # first turn the listValid into a string
    strValid = ""
    for item in listValid:
        strValid += str(item[0]) + " " + str(item[1]) + " "
    strValid.rstrip()
    
    # then check the case/strMethod/case_x_x.txt file
    tempPath = "case/"+strMethod+"/case_"+str(stateStart)+"_"+str(stateEnd)+".txt"
    if(not os.path.exists(tempPath)):
        raise CubeErr("Case file not found")
    
    with open(tempPath, "r") as f:
        lines = f.readlines()
    tempListStrip = []
    for item in lines:
        tempListStrip.append(item.rstrip())
        
    tempCaseNum = -9
    for i in range(len(tempListStrip)):
        if(tempListStrip[i].rstrip() == strValid.rstrip()):
            tempCaseNum = i // 2
            
    if(tempCaseNum == -9):
        raise CubeErr("Case not found")
    
    # logging.info("This is case "+str(tempCaseNum))
    
    # go to the case_x_x.txt file and find the corresponding algorithm
    tempPath = "alg/"+strMethod+"/case_"+str(stateStart)+"_"+str(stateEnd)+".txt"
    if(not os.path.exists(tempPath)):
        raise CubeErr("Alg file not found")
    with open(tempPath, "r") as f:
        lines = f.readlines()
    tempListStrip = []
    for item in lines:
        tempListStrip.append(item.rstrip())
        
    result = []
    for item in tempListStrip:
        tempSplit = item.split()
        if(len(tempSplit) >0 and tempSplit[0] == "case"+str(tempCaseNum)):
            tempList = []
            tempList.append(tempSplit[1][5:])
            for i in range(2, len(tempSplit) -1):
                tempList.append(tempSplit[i])
            # logging.info(str(tempList))
            # logging.info(str(tempSplit[-1][7:]))
            result.append(solve.SolveAlg(tempList[:],float(tempSplit[-1][7:])))
    
    return result

if __name__ == '__main__':
    Slot("4 4 5 5 6 6 7 7 9 9 11 11 0 12 1 13 2 15 3 14 4 16 5 17 6 18 7 19 4 24 5 25 0 30 0 31 0 32 0 33 0 35 0 37 0 50 0 59 0 60 0 61 0 54 0 55 0 56 0 57", "Roux_v1", 13, 14)        
    