import numpy as np
import copy
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

tmpCube = np.eye(74,dtype=np.int8)
for i in range(8):
    tmpCube = tmpCube@U@E1@U1@E
    
# A function to check if the cube is legal
def IsLegal(cube):
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

if __name__ == "__main__":
    fine = fine@RUR1@U@RUR1@F1@RUR1@U1@R1FR@RU1R1@U2@RU1R1
    print(fine[:12,:12])
    print(fine[:8,12:20])
    print(fine[:6,20:26])
    print(fine[0,26:50])
    print(fine[0,50:74])
    print(IsLegal(fine))