import numpy as np
import cube
import os
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
    
    edgeP = []
    cornerP = []
    edgeOp = []
    cornerOp = []
    center = []
    edgeOWild = []
    cornerOWild = []
    for i in range(2):
        edgeP.append([])
        cornerP.append([])
        edgeOp.append([])
        cornerOp.append([])
        center.append([])
        edgeOWild.append([])
        cornerOWild.append([])
    
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

            edgeP.append([])
            cornerP.append([])
            edgeOp.append([])
            cornerOp.append([])
            center.append([])
            edgeOWild.append([])
            cornerOWild.append([])
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
                    if((tmp2-26)%12 in tmpEdgeMem):
                        pass
                    else:
                        edgeOWild[-1].append((tmp2-26)%12)
                else:
                    if((tmp2-50)%8 in tmpCornerMem):
                        pass
                    else:
                        cornerOWild[-1].append((tmp2-50)%8)
                        
                #
    print(transfers)
    '''
    print("edgeP")
    print(edgeP)
    print("edgeOp")
    print(edgeOp)
    print("edgeOWild")
    print(edgeOWild)
    print("cornerP")
    print(cornerP)
    print("cornerOp")
    print(cornerOp)
    print("cornerOWild")
    print(cornerOWild)
    print("center")
    print(center)
    '''
    for i in range(len(transfers)):
        #edge p
        before, after = transfers[i][0], transfers[i][1]
        if(before==16 and after==17):
            travelEdgeOWild = False
            travelCornerOWild = False        
            for j in range(12):
                if((not j in edgeP[before]) and j in edgeP[after]):
                    print("travel edgeP "+str(j))
                if((not j in edgeOp[before]) and j in edgeOp[after]):
                    print("travel edgeOp "+str(j))
                if((not j in cornerOp[before]) and j in cornerOp[after]):
                    print("travel cornerOp "+str(j))
                if((not j in cornerP[before]) and j in cornerP[after]):
                    print("travel cornerP "+str(j))
                if((not j in center[before]) and j in center[after]):
                    print("travel center "+str(j))
                if(j in edgeOWild[after]):
                    travelEdgeOWild = True
                if(j in cornerOWild[after]):
                    travelCornerOWild = True
            if(travelEdgeOWild):
                print("travel edgeOWild")
            if(travelCornerOWild):
                print("travel cornerOWild")
            
            
            
    
    
    
if __name__ == "__main__":
    GenerateCase("Roux_v1")