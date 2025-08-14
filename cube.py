import numpy as np
import copy
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='cube.log',  
    filemode='w'  
)

class CubeErr(Exception):
    pass

fine = np.zeros((12, 74),dtype=np.int8)
fine[:12, :12] = np.eye(12,dtype=np.int8)
fine[:8,12:20] = np.eye(8,dtype=np.int8)
fine[:6,20:26] = np.eye(6,dtype=np.int8)
for i in range(26,38):
    fine[0,i] = 1
for i in range(50,58):
    fine[0,i] = 1

U = np.eye(74,dtype=np.int8)
tmp = np.array([[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]],dtype=np.int8)
U[0:4, 0:4] = tmp
U[12:16,12:16] = tmp
U[26:30,26:30] = tmp
U[38:42,38:42] = tmp
U[50:54,50:54] = tmp
U[58:62,58:62] = tmp
U[66:70,66:70] = tmp
U2 = U@U
U1 = U2@U

D = np.eye(74,dtype=np.int8)
tmp = np.array([[0,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,1,0]],dtype=np.int8)
D[8:12,8:12] = tmp
D[16:20,16:20] = tmp
D[34:38,34:38] = tmp
D[46:50,46:50] = tmp
D[54:58,54:58] = tmp
D[62:66,62:66] = tmp
D[70:74,70:74] = tmp
D2 = D@D
D1 = D2@D

R = np.eye(74,dtype=np.int8)
#offset50
tmpList1 = [3,6,11,7]
for i in range(4):
    R[tmpList1[i],tmpList1[(i+1)%4]] = 1
    R[tmpList1[i],tmpList1[i]] = 0
    
tmpList1 = [14,18,19,15]
for i in range(4):
    R[tmpList1[i],tmpList1[(i+1)%4]] = 1
    R[tmpList1[i],tmpList1[i]] = 0
    
tmpList1 = [29,32,37,33]
tmpList2 = [41,44,49,45]
for i in range(4):
    R[tmpList1[i],tmpList1[(i+1)%4]] = 1
    R[tmpList1[i],tmpList1[i]] = 0
    R[tmpList2[i],tmpList2[(i+1)%4]] = 1
    R[tmpList2[i],tmpList2[i]] = 0
    
tmpList1 = [52,72,57,69]
tmpList2 = [60,56,65,53]
tmpList3 = [68,64,73,61]
for i in range(4):
    R[tmpList1[i],tmpList1[(i+1)%4]] = 1
    R[tmpList1[i],tmpList1[i]] = 0
    R[tmpList2[i],tmpList2[(i+1)%4]] = 1
    R[tmpList2[i],tmpList2[i]] = 0
    R[tmpList3[i],tmpList3[(i+1)%4]] = 1
    R[tmpList3[i],tmpList3[i]] = 0
R2 = R@R
R1 = R2@R
tmp = R@R@R@R

L = np.eye(74,dtype=np.int8)
tmpList1 = [1,4,9,5]
for i in range(4):
    L[tmpList1[i],tmpList1[(i+1)%4]] = 1
    L[tmpList1[i],tmpList1[i]] = 0

tmpList1 = [13,12,16,17]
for i in range(4):
    L[tmpList1[i],tmpList1[(i+1)%4]] = 1
    L[tmpList1[i],tmpList1[i]] = 0
    
tmpList1 = [27,30,35,31]
tmpList2 = [39,42,47,43]
for i in range(4):
    L[tmpList1[i],tmpList1[(i+1)%4]] = 1
    L[tmpList1[i],tmpList1[i]] = 0
    L[tmpList2[i],tmpList2[(i+1)%4]] = 1
    L[tmpList2[i],tmpList2[i]] = 0
    
tmpList1 = [50,70,55,67]
tmpList2 = [58,54,63,51]
tmpList3 = [66,62,71,59]
for i in range(4):
    L[tmpList1[i],tmpList1[(i+1)%4]] = 1
    L[tmpList1[i],tmpList1[i]] = 0
    L[tmpList2[i],tmpList2[(i+1)%4]] = 1
    L[tmpList2[i],tmpList2[i]] = 0
    L[tmpList3[i],tmpList3[(i+1)%4]] = 1
    L[tmpList3[i],tmpList3[i]] = 0

L2 = L@L
L1 = L2@L

F = np.eye(74,dtype=np.int8)
tmpList1 = [0,7,8,4]
for i in range(4):
    F[tmpList1[i],tmpList1[(i+1)%4]] = 1
    F[tmpList1[i],tmpList1[i]] = 0
    
tmpList1 = [12,15,19,16]
for i in range(4):
    F[tmpList1[i],tmpList1[(i+1)%4]] = 1
    F[tmpList1[i],tmpList1[i]] = 0
    
tmpList1 = [26,45,34,42]
tmpList2 = [38,33,46,30]
for i in range(4):
    F[tmpList1[i],tmpList1[(i+1)%4]] = 1
    F[tmpList1[i],tmpList1[i]] = 0
    F[tmpList2[i],tmpList2[(i+1)%4]] = 1
    F[tmpList2[i],tmpList2[i]] = 0
    
tmpList1 = [50,61,57,62]
tmpList2 = [58,69,65,70]
tmpList3 = [66,53,73,54]
for i in range(4):
    F[tmpList1[i],tmpList1[(i+1)%4]] = 1
    F[tmpList1[i],tmpList1[i]] = 0
    F[tmpList2[i],tmpList2[(i+1)%4]] = 1
    F[tmpList2[i],tmpList2[i]] = 0
    F[tmpList3[i],tmpList3[(i+1)%4]] = 1
    F[tmpList3[i],tmpList3[i]] = 0
    
F2 = F@F
F1 = F2@F

B = np.eye(74,dtype=np.int8)
tmpList1 = [2,5,10,6]
for i in range(4):
    B[tmpList1[i],tmpList1[(i+1)%4]] = 1
    B[tmpList1[i],tmpList1[i]] = 0
    
tmpList1 = [13,17,18,14]
for i in range(4):
    B[tmpList1[i],tmpList1[(i+1)%4]] = 1
    B[tmpList1[i],tmpList1[i]] = 0
    
tmpList1 = [28,43,36,44]
tmpList2 = [40,31,48,32]
for i in range(4):
    B[tmpList1[i],tmpList1[(i+1)%4]] = 1
    B[tmpList1[i],tmpList1[i]] = 0
    B[tmpList2[i],tmpList2[(i+1)%4]] = 1
    B[tmpList2[i],tmpList2[i]] = 0
    
tmpList1 = [51,71,56,68]
tmpList2 = [59,55,64,52]
tmpList3 = [67,63,72,60]
for i in range(4):
    B[tmpList1[i],tmpList1[(i+1)%4]] = 1
    B[tmpList1[i],tmpList1[i]] = 0
    B[tmpList2[i],tmpList2[(i+1)%4]] = 1
    B[tmpList2[i],tmpList2[i]] = 0
    B[tmpList3[i],tmpList3[(i+1)%4]] = 1
    B[tmpList3[i],tmpList3[i]] = 0

B2 = B@B
B1 = B2@B

M = np.eye(74,dtype=np.int8)
tmpList1 = [0,8,10,2]
for i in range(4):
    M[tmpList1[i],tmpList1[(i+1)%4]] = 1
    M[tmpList1[i],tmpList1[i]] = 0
    
tmpList1 = [20,22,21,23]
for i in range(4):
    M[tmpList1[i],tmpList1[(i+1)%4]] = 1
    M[tmpList1[i],tmpList1[i]] = 0

tmpList1 = [26,46,36,40]
tmpList2 = [38,34,48,28]
for i in range(4):
    M[tmpList1[i],tmpList1[(i+1)%4]] = 1
    M[tmpList1[i],tmpList1[i]] = 0
    M[tmpList2[i],tmpList2[(i+1)%4]] = 1
    M[tmpList2[i],tmpList2[i]] = 0
    
M2 = M@M
M1 = M2@M

E = np.eye(74,dtype=np.int8)
tempList1 = [4,7,6,5]
for i in range(4):
    E[tempList1[i],tempList1[(i+1)%4]] = 1
    E[tempList1[i],tempList1[i]] = 0
    
tempList1 = [22,25,23,24]
for i in range(4):
    E[tempList1[i],tempList1[(i+1)%4]] = 1
    E[tempList1[i],tempList1[i]] = 0
    
tempList1 = [30,45,32,43]
tempList2 = [42,33,44,31]
for i in range(4):
    E[tempList1[i],tempList1[(i+1)%4]] = 1
    E[tempList1[i],tempList1[i]] = 0
    E[tempList2[i],tempList2[(i+1)%4]] = 1
    E[tempList2[i],tempList2[i]] = 0
    
E2 = E@E
E1 = E2@E

S = np.eye(74,dtype=np.int8)
tempList1 = [1,3,11,9]
for i in range(4):
    S[tempList1[i],tempList1[(i+1)%4]] = 1
    S[tempList1[i],tempList1[i]] = 0
    
tempList1 = [20,25,21,24]
for i in range(4):
    S[tempList1[i],tempList1[(i+1)%4]] = 1
    S[tempList1[i],tempList1[i]] = 0
    
tempList1 = [27,41,37,47]
tempList2 = [39,29,49,35]
for i in range(4):
    S[tempList1[i],tempList1[(i+1)%4]] = 1
    S[tempList1[i],tempList1[i]] = 0
    S[tempList2[i],tempList2[(i+1)%4]] = 1
    S[tempList2[i],tempList2[i]] = 0

S2 = S@S
S1 = S2@S

u = U@E1
u2 = u@u
u1 = u2@u
d = D@E
d2 = d@d
d1 = d2@d
r = R@M1
r2 = r@r
r1 = r2@r
l = L@M
l2 = l@l
l1 = l2@l
f = F@S
f2 = f@f
f1 = f2@f
b = B@S1
b2 = b@b
b1 = b2@b

x = L1@r
x2 = x@x
x1 = x2@x
y = U@d1
y2 = y@y
y1 = y2@y
z = f@B1
z2 = z@z
z1 = z2@z

RUR1 = R@U@R1
RU1R1 = R@U1@R1
R1UR = R1@U@R
R1U1R = R1@U1@R

RUR1U1R = R@U@R1@U1@R
RU1R1UR = R@U1@R1@U@R
R1URU1R1 = R1@U@R@U1@R1
R1U1RU1R1 = R1@U1@R@U@R1

R1DR = R1@D@R
R1D1R = R1@D1@R
R1FR = R1@F@R

listMoveStr = ['U','U1','U2','D','D1','D2','R','R1','R2','L','L1','L2','F','F1','F2','B','B1','B2']
listMoveStr = listMoveStr + ['u','u1','u2','d','d1','d2','r','r1','r2','l','l1','l2','f','f1','f2','b','b1','b2']
listMoveStr = listMoveStr + ['M','M1','M2','E','E1','E2','S','S1','S2']
listMoveStr = listMoveStr + ['x','x1','x2','y','y1','y2','z','z1','z2']
listMoveStr = listMoveStr + ['RUR1','RU1R1','R1UR','R1U1R','R1FR','N']
    
listMoveMatrix = [U,U1,U2,D,D1,D2,R,R1,R2,L,L1,L2,F,F1,F2,B,B1,B2]
listMoveMatrix = listMoveMatrix + [u,u1,u2,d,d1,d2,r,r1,r2,l,l1,l2,f,f1,f2,b,b1,b2]
listMoveMatrix = listMoveMatrix + [M,M1,M2,E,E1,E2,S,S1,S2]
listMoveMatrix = listMoveMatrix + [x,x1,x2,y,y1,y2,z,z1,z2]
listMoveMatrix = listMoveMatrix + [RUR1,RU1R1,R1UR,R1U1R,R1FR,np.eye(74,dtype=np.int8)]

dictMove = dict(zip(listMoveStr,listMoveMatrix))

listScore = [1.0,1.0,1.4,1.5,1.5,3,1.0,1.0,1.4,1.5,1.5,3,1.5,1.5,2.5,2.5,2.5,5]
listScore = listScore + [1.9,1.9,3.8,2.9,2.9,5.8,1.9,1.9,3.8,2.4,2.4,4.8,2.4,2.4,4.8,3.9,3.9,7.8]
listScore = listScore + [1.9,1.1,2.2,2.4,1.9,3.8,2.9,2.9,5.8]
listScore = listScore + [0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011,0.011]
listScore = listScore + [2.1,2.1,2.1,2.1,2.5,0]

dictScore = dict(zip(listMoveStr,listScore))

#create a list with len(listMoveMatrix) that is [0,1,2,3...]
listIndex = list(range(len(listMoveMatrix)))
dictIndex = dict(zip(listMoveStr,listIndex))

#create a dict for reverse moves
listReverseMoveMatrix = [U1,U,U2,D1,D,D2,R1,R,R2,L1,L,L2,F1,F,F2,B1,B,B2]
listReverseMoveMatrix = listReverseMoveMatrix + [u1,u,u2,d1,d,d2,r1,r,r2,l1,l,l2,f1,f,f2,b1,b,b2]
listReverseMoveMatrix = listReverseMoveMatrix + [M1,M,M2,E1,E,E2,S1,S,S2]
listReverseMoveMatrix = listReverseMoveMatrix + [x1,x,x2,y1,y,y2,z1,z,z2]
listReverseMoveMatrix = listReverseMoveMatrix + [RU1R1,RUR1,R1U1R,R1UR,R1@F1@R,np.eye(74,dtype=np.int8)]
dictReverseMove = dict(zip(listMoveStr,listReverseMoveMatrix))

# Create two tables to ban/pick the next move
#create a 2d array [len(listMoveMatrix)][len(listMoveMatrix)] with all 1
tableBig = [[1 for i in range(len(listMoveMatrix))] for j in range(len(listMoveMatrix))]
tableSmall = [[1 for i in range(len(listMoveMatrix))] for j in range(len(listMoveMatrix))]
# big table to enable awkward moves 
# small table for faster moves 
# two tables: ban cases with 1st tail == 2nd head eg: U U1 banned, D D1 banned 
def OmitTailHead(str1,str2):
    #find the last alphabet in str1.
    indexStr1 = -1
    moveAngle1 = 1
    if(str1[-1] == '1'):
        indexStr1 = -2
        moveAngle1 = 3
    elif(str1[-1] == '2'):
        indexStr1 = -2
        moveAngle1 = 2
    motion1 = str1[indexStr1]
    motion2 = str2[0]
    moveAngle2 = 1
    if(len(str2)>=2 and str2[1] == '1'):
        moveAngle2 = 3
    elif(len(str2)>=2 and str2[1] == '2'):
        moveAngle2 = 2
    if(motion1 == motion2 and moveAngle1+moveAngle2 in [3,4,5]):
        return True
    #if neither of the strings has length>=3, also return True
    if(motion1 == motion2 and len(str1)<3 and len(str2)<3):
        return True
    return False

lenList = len(listMoveMatrix)
for i in range(lenList):
    for j in range(lenList):
        if(OmitTailHead(listMoveStr[i],listMoveStr[j])):
            tableBig[i][j] = 0
            tableSmall[i][j] = 0

# two tables: ban S, b and d 
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i][0] in ['S','b','d'] or listMoveStr[j][0] in ['S','b','d']):
            tableBig[i][j] = 0
            tableSmall[i][j] = 0
           
# two tables: ban rotation
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] in ['x','x1','y','y1','z','z1'] or listMoveStr[j] in ['x','x1','y','y1','z','z1']):
            tableBig[i][j] = 0
            tableSmall[i][j] = 0
# small table configuration
for i in range(lenList):
    for j in range(lenList):
        if(listScore[i] >= 2.598 or listScore[j] >= 2.598):
            tableSmall[i][j] = 0
            
# U cannot be followed by D
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] == 'U' and listMoveStr[j][0] == 'D'):
            tableSmall[i][j] = 0
        if(listMoveStr[i] == 'U1' and listMoveStr[j][0] == 'D'):
            tableSmall[i][j] = 0
        if(listMoveStr[i] == 'U2' and listMoveStr[j][0] == 'D'):
            tableSmall[i][j] = 0
            
# D cannot be followed by F, B, u,f, l, U
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] == 'D' and listMoveStr[j][0] in ['F','B','f','l','u','U']):
            tableSmall[i][j] = 0
        if(listMoveStr[i] == 'D1' and listMoveStr[j][0] in ['F','B','f','l','u','U']):
            tableSmall[i][j] = 0

# F cannot be followed by D, B, L, u,f,l
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] == 'F' and listMoveStr[j][0] in ['D','B','L','u','f','l']):
            tableSmall[i][j] = 0
        if(listMoveStr[i] == 'F1' and listMoveStr[j][0] in ['D','B','L','u','f','l']):
            tableSmall[i][j] = 0
# B cannot be followed by D, F, L, u,f,l
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] == 'B' and listMoveStr[j][0] in ['D','F','L','u','f','l']):
            tableSmall[i][j] = 0
        if(listMoveStr[i] == 'B1' and listMoveStr[j][0] in ['D','F','L','u','f','l']):
            tableSmall[i][j] = 0
            
# L can only be followed by U,R,D
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] == 'L' and listMoveStr[j][0] not in ['U','R','D']):            
            tableSmall[i][j] = 0
        if(listMoveStr[i] == 'L1' and listMoveStr[j][0] not in ['U','R','D']):
            tableSmall[i][j] = 0
            
# f can only be followed by U,R
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] == 'f' and listMoveStr[j][0] not in ['U','R']):
            tableSmall[i][j] = 0
        if(listMoveStr[i] == 'f1' and listMoveStr[j][0] not in ['U','R']):            
            tableSmall[i][j] = 0


# M1 can only be followed by U, and can only follow U
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] == 'M1' and listMoveStr[j][0] not in ['U']):
            tableSmall[i][j] = 0
        if(listMoveStr[i][0] not in ['U'] and listMoveStr[j] == 'M1'):
            tableSmall[i][j] = 0

# R2 cannot be followed by L, L1, f, f1
for i in range(lenList):
    for j in range(lenList):
        if(listMoveStr[i] == 'R2' and listMoveStr[j] in ['L','L1','f','f1']):
            tableSmall[i][j] = 0
        if(listMoveStr[i] in ['L','L1','f','f1'] and listMoveStr[j] == 'R2'):
            tableSmall[i][j] = 0




# form a list with 888 elements, containing the smallest 888 primes
primeList = []
temp = 2
while(len(primeList) < 888):
    isPrime = True
    for j in range(2,int(np.sqrt(temp))+1):
        if(temp%j == 0):
            isPrime = False
            break
    if(isPrime):
        primeList.append(temp)
    temp += 1
primeTable = np.zeros((12,74),dtype=int)
primeIndex = 0
for i in range(12):
    for j in range(12):
        primeTable[j][i] = primeList[primeIndex]
        primeIndex += 1
for i in range(12,20):
    for j in range(8):
        primeTable[j][i] = primeList[primeIndex]
        primeIndex += 1
for i in range(20,26):
    for j in range(6):
        primeTable[j][i] = primeList[primeIndex]
        primeIndex += 1
for i in range(26,74):
    primeTable[0][i] = primeList[primeIndex]
    primeIndex += 1
        

SIZEHASH1 = 524287
SIZEHASH2 = 524269
SIZEHASH3 = 524261
SIZEHASH4 = 524257
SIZEHASH5 = 524243
SIZEHASH6 = 524231
def calHash1(cube1):
    tempProduct1 = 1
    tempProduct2 = 1
    tempProduct3 = 1
    tempProduct4 = 1
    tempProduct5 = 1
    tempProduct6 = 1
    for i in range(12):
        for j in range(74):
            if(cube1[i,j] == 1):
                tempProduct1 *= primeTable[i][j]
                tempProduct2 *= primeTable[i][j]
                tempProduct3 *= primeTable[i][j]
                tempProduct4 *= primeTable[i][j]
                tempProduct5 *= primeTable[i][j]
                tempProduct6 *= primeTable[i][j]
                tempProduct1 %= SIZEHASH1
                tempProduct2 %= SIZEHASH2
                tempProduct3 %= SIZEHASH3
                tempProduct4 %= SIZEHASH4
                tempProduct5 %= SIZEHASH5
                tempProduct6 %= SIZEHASH6
    return (int(tempProduct1),int(tempProduct2),int(tempProduct3),int(tempProduct4),int(tempProduct5),int(tempProduct6))

# A function to check if the cube is legal
def IsLegalMatrix(cube):
    for i in range(12):
        if(np.sum(cube[i,:12]) >= 2 or np.sum(cube[:12,i]) >= 2):
            return False
    for i in range(8):
        if(np.sum(cube[i,12:20]) >= 2 or np.sum(cube[0:8,i+12]) >= 2):
            return False
    for i in range(6):
        if(np.sum(cube[i,20:26]) >= 2 or np.sum(cube[0:6,i+20]) >= 2):
            return False
    for i in range(12):
        if(cube[0,26+i] + cube[0,38+i] >= 2):
            return False
    for i in range(8):
        if(cube[0,50+i] + cube[0,58+i] + cube[0,66+i] >= 2):
            return False
    # edge oriention
    if(np.sum(cube[0,26:50]) == 11):
        return False
    elif(np.sum(cube[0,26:50]) <= 10):
        pass
    elif(np.sum(cube[0,26:38]) % 2 != 0):
        return False
    # corner oriention
    if(np.sum(cube[50:74]) == 11):
        return False
    elif(np.sum(cube[50:74]) <= 10):
        pass
    else:
        cornerOriention = 0
        cornerOriention += np.sum(cube[58:66]) * 1 + np.sum(cube[66:74]) * 2
        if(cornerOriention % 3 != 0):
            return False
    # edge permutation
    edgePermutation = 0
    if(np.sum(cube[:12,:12]) == 11):
        return False
    elif(np.sum(cube[:12,:12]) <= 10):
        edgePermutation = 0
    else:
        tmpList = []
        for i in range(12):
            for j in range(12):
                if(cube[i,j] == 1):
                    tmpList.append(j)
        for i in range(11):
            for j in range(i+1,12):
                if(tmpList[j] < tmpList[i]):
                    edgePermutation += 1
        if(edgePermutation % 2 != 0):
            edgePermutation = 1
        else:
            edgePermutation = 2
    # corner permutation
    cornerPermutation = 0
    if(np.sum(cube[:8,12:20]) == 7):
        return False
    elif(np.sum(cube[:8,12:20]) <= 10):
        cornerPermutation = 0
    else:
        tmpList = []
        for i in range(8):
            for j in range(12,20):
                if(cube[i,j] == 1):
                    tmpList.append(j)
        for i in range(7):
            for j in range(i+1,8):
                if(tmpList[j] < tmpList[i]):
                    cornerPermutation += 1
        if(cornerPermutation % 2 == 0):
            cornerPermutation = 2
        else:
            cornerPermutation %= 1
    
    #center permutation
    centerPermutation = 0
    if(np.sum(cube[:6,20:26]) % 2 != 0):
        return False
    elif(np.sum(cube[:6,20:26]) <= 4):
        centerPermutation = 0
    else:
        tmpList = []
        for i in range(6):
            for j in range(20,26):
                if(cube[i,j] == 1):
                    tmpList.append(j)
        for i in range(5):
            for j in range(i+1,6):
                if(tmpList[j] < tmpList[i]):
                    centerPermutation += 1
        if(centerPermutation % 2 == 0):
            centerPermutation = 2
        else:
            centerPermutation %= 1

    if(centerPermutation*cornerPermutation*edgePermutation == 0):
        return True
    elif(centerPermutation+cornerPermutation+edgePermutation % 2 != 0):
        return False
    else:
        return True
    
def IsLegalString(str1):
    tmpSplit = str1.rstrip().split()
    tmpList1 = []
    tmpList1.clear()
    tmpList2 = []
    tmpList2.clear()
    if(len(tmpSplit) % 2):
        print("A")
        return False
    for i in range(0,len(tmpSplit),2):
        tmpList1.append(int(tmpSplit[i]))
        tmpList2.append(int(tmpSplit[i+1]))
        
    # tmpList2 should be in ascending order
    for i in range(1,len(tmpList2)):
        if(tmpList2[i] <= tmpList2[i-1]):
            print("B")
            return False
    
    # edge
    tmpListEdgeP1 = []
    tmpListEdgeP2 = []
    i = 0
    for i in range(0,len(tmpList2)):
        if(tmpList2[i] >= 12):
            break
    for j in range(0,i):
        tmpListEdgeP1.append(tmpList1[j])
        tmpListEdgeP2.append(tmpList2[j])
        
    # false if redundent numbers in tmpListEdgeP1
    tmp = [False] * 12
    for i in range(0,len(tmpListEdgeP1)):
        if(not(0<=tmpListEdgeP1[i]<=11) or tmp[tmpListEdgeP1[i]] == True):
            print("C")
            return False
        else:
            tmp[tmpListEdgeP1[i]] = True
    
    #check the permutation of edge
    edgeP = 0
    if(len(tmpListEdgeP1) == 11):
        print("D")
        return False
    elif(len(tmpListEdgeP1) <= 10):
        edgeP = 0
    else:
        tmpReverse = 0
        for i in range(len(tmpListEdgeP1)):
            for j in range(i+1,len(tmpListEdgeP1)):
                if(tmpListEdgeP1[i] > tmpListEdgeP1[j]):
                    tmpReverse += 1
        if(tmpReverse % 2 == 0):
            edgeP = 2
        else:
            edgeP = 3
    
    #corner
    tmpListCornerP1 = []
    tmpListCornerP2 = []
    for i in range(len(tmpListEdgeP1),len(tmpList2)):
        if(tmpList2[i] >= 20):
            break
        tmpListCornerP1.append(tmpList1[i])
        tmpListCornerP2.append(tmpList2[i])
    
    #false if redundent number in tmpListCornerP1
    tmp = [False for i in range(8)]
    for i in range(len(tmpListCornerP1)):
        if(not(0<=tmpListCornerP1[i]<=7) or tmp[tmpListCornerP1[i]] == True):
            print("E")
            return False
        else:
            tmp[tmpListCornerP1[i]] = True
    

    #check the permuation of corner
    cornerP = 0
    if(len(tmpListCornerP1) == 7):
        print("F")
        return False
    elif(len(tmpListCornerP1) <=6):
        cornerP = 0
    else:
        tmpReverse = 0
        for i in range(len(tmpListCornerP1)):
            for j in range(i+1,len(tmpListCornerP1)):
                if(tmpListCornerP1[i] > tmpListCornerP1[j]):
                    tmpReverse += 1
        if(tmpReverse % 2 == 0):
            cornerP = 2
        else:
            cornerP = 3

    #center
    tmpListCenter1 = []
    tmpListCenter2 = []
    for i in range(0,len(tmpList1)):
        if(tmpList2[i] < 20):
            continue
        elif(tmpList2[i] >=26):
            break
        tmpListCenter1.append(tmpList1[i])
        tmpListCenter2.append(tmpList2[i])
    
    #False if redundent number in tmpListCenter1
    tmp = [False for i in range(0,6)]
    for i in range(0,len(tmpListCenter1)):
        if(not(0<=tmpListCenter1[i]<=5) or tmp[tmpListCenter1[i]] == True):
            print("G")
            return False
        else:
            tmp[tmpListCenter1[i]] = True
            
    #check the permutation of center
    centerP = 0
    if(not(len(tmpListCenter2) in [0,2,6])):
        print("H")
        return False
    elif(len(tmpListCenter2) == 0):
        centerP = 0
    elif(len(tmpListCenter2) == 2):
        if(not(tmpListCenter1[0] - tmpListCenter1[1] in [1,-1])):
            return False
        if(not(tmpListCenter1[0] + tmpListCenter1[1] in [1,5,9])):
            return False
        if(not(tmpListCenter2[0] - tmpListCenter2[1] in [1,-1])):
            return False
        if(not(tmpListCenter2[0] + tmpListCenter2[1] in [41,45,49])):
            return False
        centerP = 0
    else:
        #tmpListCenter1 must be [0,1,2,3,4,5] no need to check
        if(not(tmpListCenter1[0] - tmpListCenter1[1] in [1,-1])):
            return False
        if(not(tmpListCenter1[2] - tmpListCenter1[3] in [1,-1])):
            return False
        if(not(tmpListCenter1[4] - tmpListCenter1[5] in [1,-1])):
            return False
        centerP = centerPCal(tmpListCenter1)
        if(centerP == -1):
            return False
    
    #3P should be 0 or 8 or 18
    if(not (edgeP*cornerP*centerP in [0,8,18])):
        return False
    
    #edge orientation
    tmpListEdgeO1 = []
    tmpListEdgeO2 = []
    for i in range(len(tmpList1)):
        if(tmpList2[i] < 26):
            continue
        elif(tmpList2[i] >= 50):
            break
        tmpListEdgeO1.append(tmpList1[i])
        tmpListEdgeO2.append(tmpList2[i])
        
    #False if tmpListEdgeO1 has element != 0
    for i in range(len(tmpListEdgeO1)):
        if(tmpListEdgeO1[i] != 0):
            return False
    
    #False if tmpListEdgeO2 has same remaining at 12
    tmp = [False for i in range(12)]
    for i in range(len(tmpListEdgeO2)):
        if(tmp[tmpListEdgeO2[i]%12] == True):
            return False
        else:
            tmp[tmpListEdgeO2[i]%12] = True
            
    #False if oriention incorrect
    if(len(tmpListEdgeO2) == 11):
        return False
    elif(len(tmpListEdgeO2) <= 10):
        pass
    else:
        edgeFlipCount = 0
        for i in tmpListEdgeO2:
            if(i >= 38):
                edgeFlipCount += 1
        if(edgeFlipCount % 2 != 0):
            return False
        
    #corner oriention
    tmpListCornerO1 = []
    tmpListCornerO2 = []
    for i in range(len(tmpList1)):
        if(tmpList2[i] < 50):
            continue
        tmpListCornerO1.append(tmpList1[i])
        tmpListCornerO2.append(tmpList2[i])
    
    #False if tmpListCornerO1 has element != 0
    for i in range(len(tmpListCornerO1)):
        if(tmpListCornerO1[i] != 0):
            return False

    #False if tmpListCornerO2 has same remaining at 8
    tmp = [False for i in range(8)]
    for i in range(len(tmpListCornerO2)):
        if(tmp[tmpListCornerO2[i]%8] == True):
            return False
        else:
            tmp[tmpListCornerO2[i]%8] = True
            
    #False if oriention incorrect
    if(len(tmpListCornerO2) == 7):
        return False
    elif(len(tmpListCornerO2) <= 6):
        pass
    else:
        cornerFlipCount = 0
        for i in tmpListCornerO2:
            if(i < 58):
                pass
            elif(i < 66):
                cornerFlipCount += 1
            else:
                cornerFlipCount += 2

        if(cornerFlipCount % 3 != 0):
            return False
    
    return True

def centerPCal(list1):
    #assume that list1 only contain 0,1,2,3,4,5
    rotation = 0
    if(list1[4] == 0 or list1[5] ==0):
        #z
        while(list1[0] != 0):
            tmp = list1[0]
            list1[0] = list1[4]
            list1[4] = list1[1]
            list1[1] = list1[5]
            list1[5] = tmp
            rotation += 1
    elif(list1[2] == 0 or list1[3] ==0 or list1[1] ==0):
        #x
        while(list1[0] != 0):
            tmp = list1[0]
            list1[0] = list1[2]
            list1[2] = list1[1]
            list1[1] = list1[3]
            list1[3] = tmp
            rotation += 1
    while(list1[2] != 2):
        #y
        tmp = list1[2]
        list1[2] = list1[5]
        list1[5] = list1[3]
        list1[3] = list1[4]
        list1[4] = tmp
        rotation += 1
    
    if(list1[4] != 4 or list1[2] != 2 or list1[0] != 0):
        return -1
    elif(rotation % 2 == 0):
        return 2
    else:
        return 3
if __name__ == "__main__":
    str13 = "4 4 5 5 6 6 7 7 9 9 11 11 4 16 5 17 6 18 7 19 4 24 5 25 0 30 0 31 0 32 0 33 0 35 0 37 0 54 0 55 0 56 0 57"
    listStr13 = str13.rstrip().split()
    cube13 = np.zeros((12, 74),dtype=np.int8)
    for i in range(0,len(listStr13),2):
        cube13[int(listStr13[i])][int(listStr13[i+1])] = 1
    logging.info(str(calHash1(cube13)))
    logging.info(str(calHash1(cube13 @ U)))
    logging.info(str(calHash1(cube13 @ R)))
    logging.info(str(calHash1(cube13 @ F)))