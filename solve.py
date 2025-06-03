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
    CheckExistFolderGenerate("case")
    CheckExistGenerate("case/"+method1+".txt")
    
    
    
if __name__ == "__main__":
    GenerateCase("Roux_v1")