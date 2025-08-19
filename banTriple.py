import cube
import os
import logging


def GenDict3Forward(strMethod):
    dict3Forward = dict()
    dict3Backward = dict()
    fileName = strMethod+"_banTriple.txt"
    if (not os.path.exists(fileName)):
        raise cube.CubeError("File "+fileName+" does not exist")
    with open(fileName, "r") as file:
        lines = file.readlines()
    for line in lines:
        tempSplit = line.rstrip().split()
        if(len(tempSplit) != 3):
            raise cube.CubeError("File "+fileName+" is not formatted correctly")
        tempStr0 = tempSplit[0]
        tempStr1 = tempSplit[1]
        tempStr2 = tempSplit[2]
        tempIntFirstTwo = cube.dictIndex[tempStr0] * len(cube.dictIndex) + cube.dictIndex[tempStr1]
        tempIntThird = cube.dictIndex[tempStr2]
        tempIntFirst = cube.dictIndex[tempStr0]
        tempIntLastTwo = cube.dictIndex[tempStr2] * len(cube.dictIndex) + cube.dictIndex[tempStr1]
        if(tempIntFirstTwo not in dict3Forward):
            dict3Forward[tempIntFirstTwo] = []
        if(tempIntThird not in dict3Forward[tempIntFirstTwo]):
            dict3Forward[tempIntFirstTwo].append(tempIntThird)
        if(tempIntLastTwo not in dict3Backward):
            dict3Backward[tempIntLastTwo] = []
        if(tempIntFirst not in dict3Backward[tempIntLastTwo]):
            dict3Backward[tempIntLastTwo].append(tempIntFirst)
    return dict3Forward, dict3Backward

if __name__ == "__main__":
    tempDict3Forward, tempDict3Backward = GenDict3Forward("Roux_v1")
    for key in tempDict3Forward:
        logging.info(key)
        logging.info(tempDict3Forward[key])
    logging.info("------------------------")
    for key in tempDict3Backward:
        logging.info(key)
        logging.info(tempDict3Backward[key])
        