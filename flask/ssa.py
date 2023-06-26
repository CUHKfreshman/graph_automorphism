import pandas as pd
import subprocess
def convert_to_bin(isDSSA):
    realDir = "./flask/methods/SSA/SSA"
    if isDSSA:
        realDir = "./flask/methods/SSA/DSSA"
    command = [f"{realDir}/el2bin","./flask/usrfile.txt","./flask/usrfile.bin"]
    subprocess.run(command)
    
def run_ssa(seedsize, epsilon, delta, model, isDSSA):
    realPath = "./flask/methods/SSA/SSA/SSA"
    if isDSSA:
        realPath = "./flask/methods/SSA/DSSA/DSSA"
    command = [realPath, 
               "-i", "./flask/usrfile.bin", 
               "-k", str(seedsize), 
               "-epsilon", str(epsilon), 
               "-delta", str(delta), 
               "-o", "./flask/ssaOutput.txt",
               "-m",model]
    result = subprocess.run(command,  text=True, capture_output=True)
    
    return result

def read_output():
    with open("./flask/ssaOutput.txt") as f:
        lines = f.readlines()
        output = [line.split()[0] for line in lines]
        return output
def get_ssa_result(seedsize, epsilon, delta, model, isDSSA):
    #print(seedsize, epsilon, delta, model, isDSSA)
    convert_to_bin(isDSSA)
    detail = run_ssa(seedsize, epsilon, delta, model, isDSSA)
    output = read_output()
    if isDSSA:
        print("DSSA:",output)
    else:
        print("SSA:",output)
    return output

#get_ssa_result(10, 0.1,0.01, "LT", True)