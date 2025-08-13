import numpy as np
import cube
from cube import CubeErr, calHash1
import os
import sys
import copy
from collections import deque
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='./cube.log',  
    filemode='w'  
)

class bfsDequeElement:
    def __init__(self, cube, move, lastMove, moveNum, points):
        self.cube = cube
        self.move = move
        self.lastMove = lastMove
        self.moveNum = moveNum
        self.points = points
        
class bfsHashElement:
    def __init__(self, move, points):
        self.move = move
        self.points = points

    

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
    tmpDirectory = "case/"            
    if(not os.path.exists(tmpDirectory)):
        os.makedirs(tmpDirectory)
        
    tmpDirectory = "case/"+str(method1)+"/"
    if(not os.path.exists(tmpDirectory)):
        os.makedirs(tmpDirectory)
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
    allEdgeO = []
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
        allEdgeO.append(False)
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
            allEdgeO.append(True)
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
                        #edgeP[-1].append(tmp1)
                        edgeOp[-1].append(tmp1)
                        tmpEdgeMem.append(tmp2)
                    else:
                        edgeP[-1].append(tmp1)
                elif(tmp2 < 20):
                    if((tmp2+38) in tmpCubePosition or (tmp2+46) in tmpCubePosition or (tmp2+54) in tmpCubePosition):
                        #cornerP[-1].append(tmp1)
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
            for i in range(26,38):
                if(not str(i) in tmpSplit):
                    allEdgeO[-1]=False
                    break
                
                        
    for i in range(len(transfers)):
        #edge p
        before, after = transfers[i][0], transfers[i][1]
        print(before, after)
        travelEdgeOWild = False
        travelCornerOWild = False        
        if(edgeOWild[after] and len(edgeO[before]) < 12):
            travelEdgeOWild = True
        if(cornerOWild[after] and len(cornerO[before]) < 8):
            travelCornerOWild = True
        travelEdgeP = [j  for j in range(12) if ((not j in edgeP[before]) and (not j in edgeOp[before]) and j in edgeP[after])]
        travelEdgeOp = [j  for j in range(12) if ((not j in edgeP[before]) and (not j in edgeOp[before]) and j in edgeOp[after])]
        travelEdgeO = [j  for j in range(12) if ((not j in edgeOp[before])) and j in edgeP[before] and j in edgeOp[after]]
        travelCornerP = [j  for j in range(8) if ((not j in cornerP[before]) and (not j in cornerOp[before]) and j in cornerP[after])]
        travelCornerOp = [j  for j in range(8) if ((not j in cornerOp[before]) and (not j in cornerP[before]) and j in cornerOp[after])]
        travelCornerO = [j  for j in range(8) if ((not j in cornerOp[before]) and j in cornerP[before] and j in cornerOp[after])]
        travelCenter = [j  for j in range(6) if ((not j in center[before]) and j in center[after])]
        edgePAvailable = [j  for j in range(12) if ((not j in edgeP[before]) and (not j in edgeOp[before]))]
        cornerPAvailable = [j  for j in range(8) if ((not j in cornerP[before]) and (not j in cornerOp[before]))]
        centerAvailable = [j  for j in range(6) if (not j in center[before])]
        
        
        listEdge = []
        listCorner = []
        #Start generating
        if(travelEdgeP):
            listEdge = GenerateCaseEdgeP(travelEdgeP, edgePAvailable)
        elif(travelEdgeOp and allEdgeO[before]):
            listEdge = GenerateCaseEdgeP(travelEdgeOp, edgePAvailable)
        elif(travelEdgeOp):
            listEdge = GenerateCaseEdgeOp(travelEdgeOp, edgePAvailable)
        elif(travelEdgeOWild):
            listEdge = GenerateCaseEdgeOWild(edgePAvailable)
        elif(travelEdgeO):
            listEdge = GenerateCaseEdgeO(travelEdgeO)
        else:
            listEdge = [" "]
        if(travelCornerP):
            listCorner = GenerateCaseCornerP(travelCornerP, cornerPAvailable)
        elif(travelCornerOp):
            listCorner = GenerateCaseCornerOp(travelCornerOp, cornerPAvailable)
        else:
            listCorner = [" "]
        if(travelCenter):
            listCenter = GenerateCaseCenter(travelCenter, centerAvailable)
        else:
            listCenter = [" "]
        
        tmpStr = strings[before]
        tmpCase = []
        for item1 in listEdge:
            for item2 in listCorner:
                for item3 in listCenter:
                    tmpCase.append(GenerateCaseShuffle(tmpStr +" "+ item1 +" "+ item2 +" "+ item3))
        
        with open(tmpDirectory + "case_"+str(before)+"_"+str(after)+".txt","w") as f:
            tmpCaseNum = 0
            for item in tmpCase:
                if(cube.IsLegalString(item)):
                    f.write("Case "+str(tmpCaseNum)+"\n")
                    f.write(item+"\n")
                    tmpCaseNum += 1
 

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
    return result



def GenerateCaseEdgeOp(travel,avail):
    # list travel
    tmpDeque = deque()
    tmpDeque.append("")
    result = []
    if(len(travel) > len(avail)):
        sys.exit("Error: travel is greater than avail")
    while(True):
        if(len(tmpDeque) == 0):
            break
        else:
            tmpStr = tmpDeque[0].rstrip()
            tmpSplit = tmpStr.split()
        if(len(tmpSplit) == len(travel) * 4):
            tmpCount = 0
            for i in range(1,len(tmpSplit),2):
                if(int(tmpSplit[i]) >= 38):
                    tmpCount += 1
            result.append(tmpStr)
            tmpDeque.popleft()
        else:
            tmpEdge = travel[len(tmpSplit)//4]
            tmpList = [False] * 12
            for i in avail:
                tmpList[i] = True
            for i in range(1,len(tmpSplit),4):
                tmpList[int(tmpSplit[i])] = False
            for i in range(12):
                if(tmpList[i] and tmpStr):
                    tmpDeque.append(tmpStr + " " + str(tmpEdge) + " " + str(i) + " 0 " + str(i+26))
                    tmpDeque.append(tmpStr + " " + str(tmpEdge) + " " + str(i) + " 0 " + str(i+38))
                elif(tmpList[i] and not tmpStr):
                    tmpDeque.append(str(tmpEdge) + " " + str(i) + " 0 " + str(i+26))
                    tmpDeque.append(str(tmpEdge) + " " + str(i) + " 0 " + str(i+38))
            tmpDeque.popleft()
    return result

def GenerateCaseEdgeO(travel):
    result = []
    tmpDeque = deque()
    tmpDeque.append("")
    while(len(tmpDeque) > 0):
        tmpStr = tmpDeque.popleft()
        tmpStr = tmpStr.strip()
        tmpSplit = tmpStr.split(" ")
        if(len(tmpSplit) == len(travel)*2):
            tmpCnt = 0
            for i in range(1,len(tmpSplit),2):
                if(int(tmpSplit[i]) >= 38):
                    tmpCnt += 1
            result.append(tmpStr)
            continue
        tmpTravel = len(tmpSplit) // 2
        if(tmpStr):
            tmpDeque.append(tmpStr + " 0 " + str(tmpTravel+26))
            tmpDeque.append(tmpStr + " 0 " + str(tmpTravel+38))
        else:
            tmpDeque.append("0 " + str(tmpTravel+26))
            tmpDeque.append("0 " + str(tmpTravel+38))
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
    return result

def GenerateCaseCornerOp(travel,avail):
    result = []
    tmpDeque = deque()
    tmpDeque.append("")
    if(len(travel) > len(avail)):
        sys.exit("Error: travel is greater than avail")
    while(tmpDeque):
        tmpStr = tmpDeque[0].rstrip()
        tmpSplit = tmpStr.split()
        if(len(tmpSplit) == len(travel) * 4):
            tmpCount = 0
            for i in range(1,len(tmpSplit),2):
                if(58 <= int(tmpSplit[i]) <= 65):
                    tmpCount += 1
                elif(66 <= int(tmpSplit[i]) <= 73):
                    tmpCount += 2
            result.append(tmpStr)
            tmpDeque.popleft()
        else:
            tmpCorner = travel[len(tmpSplit)//4]
            tmpList = [False] * 8
            for i in avail:
                tmpList[i] = True
            for i in range(1,len(tmpSplit),4):
                tmpList[int(tmpSplit[i])-12] = False
            for i in range(8):
                if(tmpList[i] and tmpStr):
                    tmpDeque.append(tmpStr + " " + str(tmpCorner) + " " + str(i+12) + " 0 " + str(i + 50))
                    tmpDeque.append(tmpStr + " " + str(tmpCorner) + " " + str(i+12) + " 0 " + str(i + 58))
                    tmpDeque.append(tmpStr + " " + str(tmpCorner) + " " + str(i+12) + " 0 " + str(i + 66))
                elif(tmpList[i] and not tmpStr):
                    tmpDeque.append(str(tmpCorner) + " " + str(i+12) + " 0 " + str(i + 50))
                    tmpDeque.append(str(tmpCorner) + " " + str(i+12) + " 0 " + str(i + 58))
                    tmpDeque.append(str(tmpCorner) + " " + str(i+12) + " 0 " + str(i + 66))
            tmpDeque.popleft()
    return result

def GenerateCaseEdgeOWild(travel):
    result = []
    tmpDeque = deque()
    tmpDeque.append("")
    while(len(tmpDeque) > 0):
        tmpStr = tmpDeque[0].rstrip()
        tmpSplit = tmpStr.split()
        if(len(tmpSplit) == len(travel) * 2):
            tmpCount = 0
            for i in range(1,len(tmpSplit),2):
                if(int(tmpSplit[i]) >= 38):
                    tmpCount += 1
            result.append(tmpStr)
            tmpDeque.popleft()
            continue
        currEdgeIndex = len(tmpSplit) // 2
        if(currEdgeIndex):
            tmpDeque.append(tmpStr + " 0 " + str(travel[currEdgeIndex]+26))
            tmpDeque.append(tmpStr + " 0 " + str(travel[currEdgeIndex]+38))
        else:
            tmpDeque.append("0 " + str(travel[currEdgeIndex]+26))
            tmpDeque.append("0 " + str(travel[currEdgeIndex]+38))
        tmpDeque.popleft()
    return result

def GenerateCaseCornerO(travel):
    return

def GenerateCaseCenter(travel,avail):
    #corner case not considered
    result = []
    if(len(travel) == 2):
        travel0 = travel[0]
        travel1 = travel[1]
        if(0 in avail):
            result.append(str(travel0) + " " + "20" + " " + str(travel1) + " " + "21")
            result.append(str(travel0) + " " + "21" + " " + str(travel1) + " " + "20")
        if(2 in avail):
            result.append(str(travel0) + " " + "22" + " " + str(travel1) + " " + "23")
            result.append(str(travel0) + " " + "23" + " " + str(travel1) + " " + "22")
        if(4 in avail):
            result.append(str(travel0) + " " + "24" + " " + str(travel1) + " " + "25")
            result.append(str(travel0) + " " + "25" + " " + str(travel1) + " " + "24")
        return result
    if(len(travel) == 4):
        if(not(4 in avail) and not(4 in travel)):
            result.append("0 20 1 21 2 22 3 23")
            result.append("0 21 1 20 2 23 3 22")
            result.append("0 22 1 23 2 21 3 20")
            result.append("0 23 1 22 2 20 3 21")
            return result
        else:
            sys.exit("not supported")
    sys.exit("not supported")
    
def GenerateCaseShuffle(str1):
    tmpSplit = str1.rstrip().split()
    tmpList1 = []
    tmpList2 = []
    for i in range(0,len(tmpSplit),2):
        tmpList1.append(int(tmpSplit[i]))
        tmpList2.append(int(tmpSplit[i+1]))
    tmpDict = dict(zip(tmpList2,tmpList1))
    #sort by value, low to high
    tmpDict = dict(sorted(tmpDict.items(), key=lambda item: item[0]))
    result = ""
    for key in tmpDict:
        result += str(tmpDict[key]) + " " + str(key) + " "
    return result.rstrip() + " "
            
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
                else:
                    table = copy.deepcopy(cube.tableBig)
    logging.info(str(listAllowStr))
    listAllowIndex = []
    for item in listAllowStr:
        if(item not in cube.dictIndex):
            raise CubeErr("invalid move "+item)
        else:
            listAllowIndex.append(cube.dictIndex[item])
    logging.info(str(listAllowIndex))
    '''
    tempSum = 0
    for i in range(len(cube.listMoveStr)):
        for j in range(len(cube.listMoveStr)):
            if(table[i][j] == 1):
                tempSum += 1
    print(tempSum)'''
    for i in range(len(cube.listMoveStr)):
        for j in range(len(cube.listMoveStr)):
            if(i not in listAllowIndex or j not in listAllowIndex):
                table[i][j] = 0
    tempSum = 0
    '''for i in range(len(cube.listMoveStr)):
        for j in range(len(cube.listMoveStr)):
            if(table[i][j] == 1):
                tempSum += 1
    print(tempSum)'''
    forwardDeque = deque()
    backwarDeque = deque()
    # first imagine an nop is appended, then popped
    
    forwardHash = dict()
    backwardHash = dict()
    
    tempPath = strMethod+"_state.txt"
    if(not os.path.exists(tempPath)):
        raise CubeErr("no such file "+tempPath)
    with open(tempPath, "r") as f:
        tempLines = f.readlines()
    for i in range(len(tempLines)):
        if(tempLines[i].strip() == "state "+str(idStart)):
            if(i+1>=len(tempLines)):
                raise CubeErr("no next line")
            tempList = tempLines[i+1].rstrip().split()
    tempCube = np.zeros((12, 74),dtype=np.int8)
    if(len(tempList) % 2 != 0):
        raise CubeErr("len(tempList) not an even number")
    for i in range(0,len(tempList),2):
        tempCube[int(tempList[i]),int(tempList[i+1])] = 1
    tempHash = calHash1(tempCube)
    
    forwardHash[tempHash] = []
    forwardHash[tempHash].append(bfsHashElement(" ",0.0))
    # then moves with length 1 are appended
    totalTryForward = 0
    startCube = copy.deepcopy(tempCube)
    for item in listAllowStr:
        forwardDeque.append(bfsDequeElement(startCube@cube.dictMove[item], item,item,1,cube.dictScore[item]))
        totalTryForward += 1
    logging.info(str(totalTryForward)+" moves with length 1 are appended")
    
    tempEnd = len(forwardDeque)
    while(len(forwardDeque) > 0):
        tempBfsElement = forwardDeque.popleft()
        tempLastMove = tempBfsElement.lastMove
        tempHashTuple = cube.calHash1(tempBfsElement.cube)
        
        if(np.array_equal(tempBfsElement.cube,startCube)):
            totalTryForward -= 1
            continue
        
        if(tempHashTuple not in forwardHash):
            forwardHash[tempHashTuple] = []
        forwardHash[tempHashTuple].append(bfsHashElement(tempBfsElement.move,tempBfsElement.points))
        # check if the new cube is equal to the startCube
        
        if(tempBfsElement.moveNum >= 4):
            continue
        # then append some bfs elements to the deque
        for j in range(len(cube.listMoveStr)):
            if(table[cube.dictIndex[tempLastMove]][j] != 0):
                forwardDeque.append(bfsDequeElement(tempBfsElement.cube @ cube.listMoveMatrix[j], tempBfsElement.move +cube.listMoveStr[j],cube.listMoveStr[j],tempBfsElement.moveNum+1,tempBfsElement.points+cube.listScore[j]))
                totalTryForward += 1
        
    logging.info(str(totalTryForward)+" moves with length 1 are appended")
    return 0            
    
if __name__ == "__main__":
    Bfs("Roux_v1",13,14)
    