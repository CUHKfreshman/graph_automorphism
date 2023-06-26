import pandas as pd
import subprocess
def convert_to_pmc(file_name, prob):
    #file_name = './facebook1.txt'  
    with open(file_name, 'r') as g_file:
        _nodenum = int(g_file.readline())
        _edgenum = int(g_file.readline())
        df = pd.read_csv(file_name, sep = "\s+|\t+|\s+\t+|\t+\s+", skiprows=2,header=None, names=['src','tar'], engine='python')
    df['prob'] = prob
    df.to_csv('./flask/test.tsv',index=False,header=False,sep='\t')

def run_benchmark(seedsize, decay):
    #seedsize = 10
    #path = 100

    command = ["./flask/methods/pmc/benchmark","./flask/test.tsv", f"{seedsize}", f"{decay}"]
    result = subprocess.run(command,  text=True, capture_output=True)

    output = result.stdout.split(',')[:-1]
    
    return output

def get_pmc_result(seedsize, decay, prob):
    convert_to_pmc('./flask/usrfile.txt', prob)
    output = run_benchmark(seedsize, decay)
    print("pmc:",output)
    return output

#get_pmc_result(10, 100,0.2)