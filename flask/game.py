import pandas as pd
import subprocess
def run_greedy(seedsize, ):
    #seedsize = 10
    #path = 100

    command = ["./flask/methods/game/Greedy++", "./flask/usrfile.txt", "./flask/gameOutput.txt", str(seedsize)]
    subprocess.run(command)

def read_output():
    with open("./flask/gameOutput.txt") as f:
        lines = f.readlines()
        output = [line.split()[0] for line in lines]
        return output
def get_game_result(seedsize, ):
    run_greedy(seedsize)
    output = read_output()
    print("Game:",output)
    return output

#get_game_result(10)