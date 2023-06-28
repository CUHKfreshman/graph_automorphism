import pandas as pd
import subprocess
def format_to_subsim(file_name, pdist, wcvariant, pedge, skew):
    #file_name = './facebook1.txt'  
    command = ["./flask/methods/subsim/subsim", "-func=format", "-dir=./flask","-outpath=./flask", f"-gname={file_name}", f"-pdist={pdist}"]
    if pdist == 'wc':
        command.append(f"-wcvariant={wcvariant}")
    elif pdist == 'uniform':
        command.append(f"-pedge={pedge}")
    else:
        command.append(f"-skew={skew}")
    cmdstr = " ".join(command)
    print("Formatting Subsim..., CMD:", cmdstr)
    subprocess.run(cmdstr, shell=True)
    print("Formatted Subsim")

def run_subsim(filename,seedsize, eps, delta, vanilla, hist):
    #seednum = 10
    #path = 100

    command = ["./flask/methods/subsim/subsim", 
               "-func=im",  
               "-dir=./flask", 
               "-outpath=./flask",
               f"-gname={filename}", 
               f"-seedsize={seedsize}", 
               f"-eps={eps}",
               f"-delta={delta}",
               f"vanilla={vanilla}",
               f"hist={hist}"]
    cmdstr = " ".join(command)
    print("Running Subsim..., CMD:", cmdstr)
    subprocess.run(cmdstr, shell=True)
    
def run_subsim_raw(params):
    command = "./flask/methods/subsim/subsim -dir=./flask -outpath=./flask -gname=usrfile.txt " +  params
    subprocess.run(command,  text=True, capture_output=True, shell=True)
    #output = read_subsim_seed("usrfile.txt", )
    #print("pmc:", output)
    #return output
    
def read_subsim_seed(filename, seedsize, pdist):
    with open(f"./flask/seed/seed_{filename}_subsim_k{seedsize}_{pdist}", "r") as f:
        lines = f.readlines()
        return [line.strip() for line in lines]
def get_subsim_result(seedsize, pdist, wcvariant, pedge, skew, eps, delta, vanilla, hist):
    filename='usrfile.txt'
    format_to_subsim(filename, pdist, wcvariant, pedge, skew)
    run_subsim(filename, seedsize, eps, delta, vanilla, hist)
    output = read_subsim_seed(filename, seedsize, pdist)
    print("subsim:",output)
    return output

#get_subsim_result(10,'wc')