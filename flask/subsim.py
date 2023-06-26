import pandas as pd
import subprocess
def format_to_subsim(file_name, pdist):
    #file_name = './facebook1.txt'  
    command = ["./flask/methods/subsim/subsim", "-func=format", f"-gname={file_name}", f"-pdist={pdist}", "-dir=./flask"]
    subprocess.run(command)
    print("Formatted Subsim")

def run_subsim(filename,seedsize):
    #seednum = 10
    #path = 100

    command = ["./flask/methods/subsim/subsim", 
               "-func=im", 
               f"-gname={filename}", 
               f"-seedsize={seedsize}", 
               "-eps=0.01", 
               "-dir=./flask", 
               "-outpath=./flask"]
    result = subprocess.run(command,  text=True, capture_output=True)
    
    return result

def read_subsim_seed(filename, seedsize, pdist):
    with open(f"./flask/seed/seed_{filename}_subsim_k{seedsize}_{pdist}", "r") as f:
        lines = f.readlines()
        return [line.strip() for line in lines]
def get_subsim_result(seedsize, pdist):
    filename='usrfile.txt'
    format_to_subsim(filename, pdist)
    run_subsim(filename, seedsize)
    output = read_subsim_seed(filename, seedsize, pdist)
    print("subsim:",output)
    return output

#get_subsim_result(10,'wc')