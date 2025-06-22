import numpy as np
import cube
import os
import sys
from collections import deque
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
    
def GenerateCase(method1):
    CheckExistStrict(method1+"_state.txt")
    with open(method1+"_state.txt", 'r') as f:
        lines = f.readlines()
    transfers = []
    strings = []
    edgeP = []
    cornerP = []
    edgeOp = []
    cornerOp = []
    center = []
    edgeOWild = []
    cornerOWild = []
    edgeO = []
    cornerO = []
    for i in range(2):
        strings.append('')
        edgeP.append([])
        cornerP.append([])
        edgeOp.append([])
        cornerOp.append([])
        center.append([])
        edgeOWild.append([])
        cornerOWild.append([])
        edgeO.append([])
        cornerO.append([])
    
    tmpCurrState = 0
    tmpNextState = 0
    for line in lines:
        tmpSplit = line.rstrip().split()
        if(tmpSplit[0] == "state"):
            tmpCurrState = int(tmpSplit[1])
            
        elif(tmpSplit[0] == "next"):
            tmpNextState = int(tmpSplit[1])
            transfers.append([tmpCurrState, tmpNextState])
        else:
            strings.append(line.rstrip())
            edgeP.append([])
            cornerP.append([])
            edgeOp.append([])
            cornerOp.append([])
            center.append([])
            edgeOWild.append([])
            cornerOWild.append([])
            edgeO.append([])
            cornerO.append([])
            tmpCubePosition = []
            tmpEdgeMem = []
            tmpCornerMem = []
            for i in range(1,len(tmpSplit),2):
                tmpCubePosition.append(int(tmpSplit[i]))
            for i in range(0,len(tmpSplit),2):
                tmp1 = int(tmpSplit[i])
                tmp2 = int(tmpSplit[i+1])
                if(tmp2 < 12):
                    if((tmp2+26)in tmpCubePosition or (tmp2+38) in tmpCubePosition):
                        edgeP[-1].append(tmp1)
                        edgeOp[-1].append(tmp1)
                        tmpEdgeMem.append(tmp2)
                    else:
                        edgeP[-1].append(tmp1)
                elif(tmp2 < 20):
                    if((tmp2+38) in tmpCubePosition or (tmp2+46) in tmpCubePosition or (tmp2+54) in tmpCubePosition):
                        cornerP[-1].append(tmp1)
                        cornerOp[-1].append(tmp1)
                        tmpCornerMem.append(tmp2-12)
                    else:
                        cornerP[-1].append(tmp1)
                elif(tmp2 < 26):
                    center[-1].append(tmp1)
                elif(tmp2 < 50):
                    edgeO[-1].append((tmp2-26)%12)
                    if((tmp2-26)%12 in tmpEdgeMem):
                        pass
                    else:
                        edgeOWild[-1].append((tmp2-26)%12)
                else:
                    cornerO[-1].append((tmp2-50)%8)
                    if((tmp2-50)%8 in tmpCornerMem):
                        pass
                    else:
                        cornerOWild[-1].append((tmp2-50)%8)
                        
    for i in range(len(transfers)):
        #edge p
        before, after = transfers[i][0], transfers[i][1]
        print(before, after)
        travelEdgeOWild = False
        travelCornerOWild = False        
        for j in range(12):
            if(j in edgeOWild[after]):
                travelEdgeOWild = True
            if(j in cornerOWild[after]):
                travelCornerOWild = True
        if(travelEdgeOWild):
            print(str(edgeOWild[after])+"travel edgeOWild")
        if(travelCornerOWild):
            print("travel cornerOWild")
        travelEdgeP = [j  for j in range(12) if ((not j in edgeP[before]) and j in edgeP[after])]
        travelEdgeOp = [j  for j in range(12) if ((not j in edgeOp[before]) and j in edgeOp[after])]
        travelCornerP = [j  for j in range(8) if ((not j in cornerP[before]) and j in cornerP[after])]
        travelCornerOp = [j  for j in range(8) if ((not j in cornerOp[before]) and j in cornerOp[after])]
        travelCenter = [j  for j in range(6) if ((not j in center[before]) and j in center[after])]
        edgePAvailable = [j  for j in range(12) if (not j in edgeP[before])]
        cornerPAvailable = [j  for j in range(8) if (not j in cornerP[before])]
        edgeOAvailable = [j  for j in range(12) if (not j in edgeO[before])]
        cornerOAvailable = [j  for j in range(8) if (not j in cornerO[before])]
        centerAvailable = [j  for j in range(6) if (not j in center[before])]
        print(str(travelEdgeP) + "travelEdgeP")
        print(str(travelEdgeOp) + "travelEdgeOp")
        print(str(travelCornerP) + "travelCornerP")
        print(str(travelCornerOp) + "travelCornerOp")
        print(str(travelCenter) + "travelCenter")
        print(edgePAvailable)
        print(cornerPAvailable)
        print(edgeOAvailable)
        print(cornerOAvailable)
        print(centerAvailable)
        print(strings[before])

def GenerateCaseEdgeP(travel,avail):
    result = []
    tmpDeque = deque()
    tmpDeque.append("")
    if(len(travel) > len(avail)):
        sys.exit("Error: travel is greater than avail")
    while(True):
        if(len(tmpDeque) == 0):
            break
        else:
            tmpStr = tmpDeque[0].rstrip()
        if(len(tmpStr.split()) == len(travel) * 2):
            result.append(tmpStr)
            tmpDeque.popleft()
        else:
            tmpList = [False] * 12
            for i in avail:
                tmpList [i] = True
            tmpSplit = tmpStr.split()
            for i in range(1,len(tmpSplit),2):
                tmpList[int(tmpSplit[i])] = False
            for i in range(12):
                if(tmpList[i] and tmpStr):
                    tmpDeque.append(tmpStr + " " + str(travel[len(tmpStr.split())//2]) + " " + str(i))
                elif(tmpList[i] and not(tmpStr)):
                    tmpDeque.append(str(travel[len(tmpStr.split())//2]) + " " + str(i))
            tmpDeque.popleft()
    print(result)
    return result

def GenerateCaseCornerP(travel,avail):
    result = []
    tmpDeque = deque()
    tmpDeque.append("")
    if(len(travel) > len(avail)):
        sys.exit("Error: travel is greater than avail")
    while(True):
        if(len(tmpDeque) == 0):
            break
        else:
            tmpStr = tmpDeque[0].rstrip()
        if(len(tmpStr.split()) == len(travel) * 2):
            result.append(tmpStr)
            tmpDeque.popleft()
        else:
            tmpList = [False] * 8
            for i in avail:
                tmpList [i] = True
            tmpSplit = tmpStr.split()
            for i in range(1,len(tmpSplit),2):
                tmpList[int(tmpSplit[i])] = False
            for i in range(8):
                if(tmpList[i] and tmpStr):
                    tmpDeque.append(tmpStr + " " + str(travel[len(tmpStr.split())//2]) + " " + str(i))
                elif(tmpList[i] and not(tmpStr)):
                    tmpDeque.append(str(travel[len(tmpStr.split())//2]) + " " + str(i))
            tmpDeque.popleft()
    print(result)
    return result

def GenerateCaseCornerOp(travel):
    # list travel
    tmpDeque = deque()
    tmpDeque.append("")
    result = []
    result.append([])
    result.append([])
    while(True):
        if(len(tmpDeque) == 0):
            break
        else:
            tmpStr = tmpDeque[0].rstrip()
            tmpSplit = tmpStr.split()
        if(len(tmpSplit) == len(travel) * 2):
            tmpCount = 0
            for i in range(1,len(tmpSplit),2):
                if(int(tmpSplit[i]) >= 38):
                    tmpCount += 1
            if(tmpCount % 2 == 0):
                result[0].append(tmpStr)
            else:
                result[1].append(tmpStr)
            tmpDeque.popleft()
        else:
            tmpEdge = travel[len(tmpSplit)//2]
            if(tmpStr):
                tmpCase1 = tmpStr + " " + "0" + " " + str(tmpEdge+26)
                tmpCase2 = tmpStr + " " + "0" + " " + str(tmpEdge+38)
                tmpDeque.append(tmpCase1)
                tmpDeque.append(tmpCase2)
                tmpDeque.popleft()
            else:
                tmpCase1 = "0" + " " + str(tmpEdge+26)
                tmpCase2 = "0" + " " + str(tmpEdge+38)
                tmpDeque.append(tmpCase1)
                tmpDeque.append(tmpCase2)
                tmpDeque.popleft()
    return result

def GenerateCaseCornerOp(travel):
    result = []
    tmpDeque = deque()
    tmpDeque.append("")
    result=[]
    result.append([])
    result.append([])
    result.append([])
    while(tmpDeque):
        tmpStr = tmpDeque[0].rstrip()
        tmpSplit = tmpStr.split(" ")
        if(len(tmpSplit) == len(travel) * 2):
            tmpCount = 0
            for i in range(1,len(tmpSplit),2):
                if(58 <= int(tmpSplit[i]) <= 65):
                    tmpCount += 1
                elif(66 <= int(tmpSplit[i]) <= 73):
                    tmpCount += 2
            if(tmpCount % 3 == 0):
                result[0].append(tmpStr)
            elif(tmpCount % 3 == 1):
                result[1].append(tmpStr)
            else:
                result[2].append(tmpStr)
            tmpDeque.popleft()
        else:
            tmpCorner = travel[len(tmpSplit)//2]
            if(tmpStr):
                tmpDeque.append(tmpStr + " " + "0" + " " + str(tmpCorner + 50))
                tmpDeque.append(tmpStr + " " + "0" + " " + str(tmpCorner + 58))
                tmpDeque.append(tmpStr + " " + "0" + " " + str(tmpCorner + 66))
                tmpDeque.popleft()
            else:
                tmpDeque.append("0 " + str(tmpCorner + 50))
                tmpDeque.append("0 " + str(tmpCorner + 58))
                tmpDeque.append("0 " + str(tmpCorner + 66))
                tmpDeque.popleft()
    print(result)
    print(len(result[0]), len(result[1]), len(result[2]))
    return result
            
            
            
            
    
    
    
if __name__ == "__main__":
    GenerateCaseCornerOp([0,1,2,3])