from multiprocessing.connection import answer_challenge
from re import A
import pandas as pd
import numpy as np
import networkx as nx
import math
from collections import defaultdict,deque
from datetime import datetime
import sys
# from typing import NamedTuple
from networkx.algorithms import isomorphism
from math import factorial
from random import random
import copy
 
 
def comb(n,m):
    if m <= n:
        a=factorial(n)/(factorial(n-m) * factorial(m))
    return a
 

class TreeNode():
    def __init__(self):
        self.vertex_list = []
        self.labeling = []
        self.EL = []
        self.children = []
        self.parent = None
        self.sig = None
        self.depth = None    

def read_graph(file_name):
    with open(file_name, 'r') as g_file:
        node_num = int(g_file.readline())
        edge_num = int(g_file.readline())
        df = pd.read_csv(file_name, sep = "\s+|\t+|\s+\t+|\t+\s+", skiprows=2,header=None, names=['src','tar'])
        g = nx.from_pandas_edgelist(df, "src", "tar")
        return g,node_num,edge_num

def read_color(file_name):
    # for reading seed and color
    tmp = np.loadtxt(file_name,dtype=int)
    return tmp

def read_seed( raw_seed_list, nodenum):
    is_seed = np.zeros(nodenum)
    seed = np.array(raw_seed_list)

    if seed.shape == (1,):
        seed = np.array([seed])
        is_seed[seed] = 1
    else:
        for s in seed:
            is_seed[s] = 1
    return seed, is_seed

def read_AT(file_name):
    max_depth = 0
    AutoTree = []
    SubTree = []
    at_file = open(file_name, 'r')
    while True:
        n = TreeNode()
        # first line vertex_list size
        line = at_file.readline()
        if not line:
            break
        nodenum = int(line)
        # vertex list
        line = at_file.readline()
        n.vertex_list = list(map(int,line.split(' ')[:-1]))
        # labeling
        line = at_file.readline()
        n.labeling = list(map(int,line.split(' ')[:-1]))
        # egdenum
        edgenum = int(at_file.readline())
        # el
        line = at_file.readline()
        EL = list(map(int,line.split(' ')[:-1]))
        u = EL[0::2]
        v = EL[1::2]
        n.EL = list(zip(u,v))
        # children size
        chnum = int(at_file.readline())
        # children
        line = at_file.readline()
        n.children = list(map(int,line.split(' ')[:-1]))
        # parent
        n.parent = int(at_file.readline())
        # sig
        n.sig = int(at_file.readline())
        # depth
        n.depth = int(at_file.readline())
        # update max depth
        max_depth = max(n.depth,max_depth)
        # add n to AutoTree
        AutoTree.append(n)
        # subtree TODO
    
    return AutoTree, SubTree, max_depth
def index(in_leaf, depth, AutoTree):
    for i,a in enumerate(AutoTree):
        if a.children[0]==-1:
            for v in a.vertex_list:
                in_leaf[v]=i
                depth[v]=a.depth

def sm(n,s, color, AutoTree):
    '''
    n: tree node index
    s: the graph_node list of query
    '''
    counter1 = defaultdict(int)
    counter2 = defaultdict(int)
    for v in AutoTree[n].vertex_list:
        counter1[color[v]]+=1
    for v in s:
        counter2[color[v]]+=1
    d = 1
    for k2,v2 in counter2.items():
        d*=comb(counter1[k2],v2)
    return d

def permute(ni,ni_,S_set, AutoTree):
    d = {}
    for idx in range(len(AutoTree[ni].vertex_list)):
        d[AutoTree[ni].vertex_list[idx]] =  AutoTree[ni_].vertex_list[idx]
    #print(d)
    #print("S:",S_set)
    # for S in S_set:
    #     #print(S_set)
   # print(S_set)
    for idx in range(len(S_set)):
        S_set[idx] = d[S_set[idx]]
    return S_set
def ssm(n,s,is_seed, AutoTree, Graph):
    nn = None
    tn = None
    #print('one ssm')
    # is_seed = np.zeros(nodenum)
    # for s in seed:
    #     is_seed[s] = 1
    r = n
    while True:
        for c in AutoTree[n].children:
            nn = 0
            for v in AutoTree[c].vertex_list:
                if is_seed[v]:
                    nn+=1
            if nn:
                tn = c
                break
        if nn==len(s) and c!=-1:
            n=tn
        else:
            break
        if c==-1:
            break
    
    #print(n)
    S_set = []
    n_set = []
    S_dict = {}
    tmp = []
    if len(AutoTree[n].vertex_list) == len(s):
        #print("still")
        #Ans.append(AutoTree[n].vertex_list)
       # AutoTree[n].vertex_list
        #print(AutoTree[n].vertex_list)
        ans = [AutoTree[n].vertex_list]
    elif AutoTree[n].children[0] == -1:
        print("finally iso")
        Nq_Graph = Graph.subgraph(AutoTree[n].vertice_list)
       # print(AutoTree[n].vertice_list)
        Query_subgraph = Graph.subgraph(s.tolist())
        GM_tmp = isomorphism.GraphMatcher(Nq_Graph,Query_subgraph)
        iso_map = list(GM_tmp.subgraph_isomorphisms_iter())
        iso_tmp = set(map(lambda x: tuple(sorted(x.keys())), iso_map))
        ans = [map(lambda x: list(x), iso_tmp)]
    else:
       # local_save = []
        for child in AutoTree[n].children:
            vs = []
            cnt = 0
            for v in AutoTree[child].vertex_list:
                if is_seed[v]:
                    vs.append(v)
            if vs:
            # print("recursive seed",vs)
                n_set.append(child)
                cnt += 1
                lst = ssm(child,vs,is_seed,AutoTree, Graph)
                tmp.append(lst)
                #Ans.append(lst)
            # print("SSM: return ","para",child,"  ",vs,"   ",lst)
                #Ans.append(lst)
                #S_i_set[str(i)] = ssm(child, vs)
            # cl.append([child,nump])
        ## canonical labeling
        #print(tmp)

        for i in range(len(tmp)):
            S_dict[i] = tmp[i]
    # print(AutoTree[n].vertex_list)
        #print(n,"  before",S_dict)
        #print("n_set",n_set)
        #print(S_dict)
        for i in range(len(n_set)):
            ni = n_set[i]
        #  print("ni",ni)
            for child in AutoTree[n].children:
                if AutoTree[child].sig == AutoTree[ni].sig and child != ni:
                    #i += 1
                    #print(child)
                    lst = permute(ni,child,S_dict[i][0][:], AutoTree)
                # print("re",lst)
                # print(S_dict)
                    S_dict[i].append(lst)
                    #S_i_set[str(i)] = permute(ni,child,S_i_set)
    # print("curr nq:",n)
    # print(S_dict)
        ans = []
        queue = []
        queue.append([])
        for i in range(len(S_dict)):
            S_dict[i] = sorted(S_dict[i])
       # print("S_dict",S_dict)
        for i in range(len(S_dict)):
            cand = S_dict[i]
            #print("cand",cand)
            for tmp in range(len(queue)):
                s = queue[0]
                queue.pop(0)
                for tt in range(len(cand)):
                    #print(cand)
                    #print(s+cand[tt])
                    a = list(set(s) & set(cand[tt]))
                    
                    if len(a )!=0:
                        continue
                    queue.append(s+cand[tt])
                #print(queue)
        for i in range(len(queue)):
            ans.append(queue[i])
   # print("ans:",ans)
    ans1 = []
    hash_set = {}
    for i in range(len(ans)):
        if frozenset(ans[i]) in hash_set.keys():
            continue
        else:
            hash_set[frozenset(ans[i])] = 1
            ans1.append(ans[i])
    ans = ans1
    search_queue = deque([])
    if r== 0:
        p= 0
    else:
        p = AutoTree[r].parent
    AutoGroup = []

    # Non-Optimized
    AutoMap = defaultdict(list)
    SigCheckMap = defaultdict(list)
    search_queue.append(r)
    AutoMap[r].append(r)

    while search_queue:
        cur_node = search_queue.popleft()
        for c in AutoTree[cur_node].children:
            if c==-1: continue
            search_queue.append(c)
            SigCheckMap[AutoTree[c].sig].append(c)
            p = AutoTree[c].parent
            if p==-1: continue
            else:
                for i in AutoMap[p]:
                    if i==p: continue
                    for j in AutoTree[i].children:
                        if len(AutoTree[j].vertex_list)==1 and len(AutoTree[c].vertex_list)==1 and AutoTree[c].EL[0][0] == AutoTree[j].EL[0][1]:
                            AutoMap[c].append(j)
                        elif AutoTree[j].sig == AutoTree[c].sig and len(AutoTree[c].vertex_list)!=1:
                            AutoMap[c].append(j)
        
        for k,v in SigCheckMap.items():
            for i in range(len(v)):
                for j in range(len(v)):
                    AutoMap[v[i]].append(v[j])
        SigCheckMap.clear()
    #print("AutoMap",AutoMap)
    Final = []
    #print(ans)
    #print("ans:",ans)
    for i in range(len(AutoMap[n])):
        for query in ans:
            Final.append(permute(n,AutoMap[n][i],query[:], AutoTree))
    print("Final: nq",n," ",Final)
    
    return Final

def get_is_seed(s, nodenum):
    is_seed = np.zeros(nodenum)
    for s_ in s:
        is_seed[s_] = 1
    return is_seed
def Neighbour_finder(g,p,new_active):
    
    targets = []
    for node in new_active:
        targets += g.neighbors(node)

    return(targets)

def IC(Networkx_Graph,Seed_Set,Probability,Num_of_Simulations,flag):
    spread = []
    cnt_s = 0
    for i in range(Num_of_Simulations):
        
        new_active, Ans = Seed_Set[:], Seed_Set[:]
        if flag == 1:
            cnt = 0
        while new_active:
            #print(new_active)
            #break
            #Getting neighbour nodes of newly activate node
            targets = Neighbour_finder(Networkx_Graph,Probability,new_active)
            if flag == 1:
                cnt+=1
            #Calculating if any nodes of those neighbours can be activated, if yes add them to new_ones.
            #np.random.seed(i)
            #print(len(targets))
            #print("111")
            success = np.random.uniform(0,1,len(targets)) < Probability
            new_ones = list(np.extract(success, sorted(targets)))
            
            #Checking which ones in new_ones are not in our Ans...only adding them to our Ans so that no duplicate in Ans.
            new_active = list(set(new_ones) - set(Ans))
            Ans += new_active
        #print(A)
        if flag == 1:
            cnt_s += cnt
        spread.append(len(Ans))
    if flag==1:
        print(cnt_s/Num_of_Simulations)
    #print(spread)
    return(np.mean(spread))
def Interaction(Graph,i,j):
    sigi = IC(Graph,i,0.2,5)
    sigj = IC(Graph,[j],0.2,5)
    tmp = i.copy()
    tmp.append(j)
    sigij = IC(Graph,tmp,0.2,5)
    return sigij - sigi

def E(Graph,vs,i):
    sigall = IC(Graph,vs,0.2,5,0)
    sigi = IC(Graph,[i],0.2,5,0)
    tmp = vs.copy()
    tmp.remove(i)
    sigall_i = IC(Graph,tmp,0.2,5,0)
    return sigall - sigall_i - sigi,sigall - sigall_i


def enumerate_all(nodenum, AutoTree,  Graph, seed):
    vs = seed.tolist()
    to = 1
    cnt = 0
    while 1:
        m = 99999
        tmp_v = -1
        in_sum = 0
        ss = 0
        print(cnt)
        cnt += 1
        #print(vs)

        for j in vs:
         #   print("ok")
            contri,ss = E(Graph,vs,j)
            #print(margin)
            in_sum += contri
            if contri < m:
                tmp_v = j 
                m = contri
        tmp = vs.copy()
        tmp.remove(tmp_v)
        if(abs(IC(Graph,tmp, 0.2, 100,0) -IC(Graph,vs, 0.2, 100,0) )<100):
            vs = tmp
        else:
            break
        if len(vs) == 10:
           break
    return vs

    
def print_children_vertice(nq, AutoTree):
    print('print_children_vertice')
    for c in AutoTree[nq].children:
        for v in AutoTree[c].vertex_list:
            print(v,end=' ')
        print('\n')
    print('end of printing')


def simulate_LTM(g, pl, time_limit):
    converted_list = pl[:]
    threshold = {}
    im_all_dict = {}
    im_all_dict[0] = pl
    for node in g.nodes():
        threshold[node] = random()
    for t in range(time_limit):
        im_all_dict[t+1] = []
        converted_list1 = converted_list[:]
        for node in g.nodes():
            total_weight = 0
            if g.degree()[node]:
                weight = 1/float(g.degree()[node])
            else:
                continue
            for each in g.neighbors(node):
                if each in converted_list:
                    total_weight = total_weight + weight
            if total_weight > threshold[node]:
                if node not in converted_list:
                    im_all_dict[t+1].append(node)
                converted_list.append(node)
        if set(converted_list1) == set(converted_list):
            #print('set', t)
            break
    return im_all_dict

def get_IM_LT(raw_seed_list, time_limit):
    g, _, _ = read_graph('./flask/usrfile.txt')
    return simulate_LTM(g, raw_seed_list, time_limit)


def cs(Networkx_Graph,Seed_Set,Probability,Num_of_Simulations,flag):
    spread = []
    cnt_s = 0
    step = 0
    result = []
    for _ in range(1):
        
        new_active, Ans = Seed_Set[:], Seed_Set[:]
        if flag == 1:
            cnt = 0
        d = {}
        d_new = {}
        total = []
        for i in Seed_Set:
            d[str(i)] = [i]
            d_new[str(i)] = [i]
            total.append(i)
        #total = []
        while new_active:
            #print(new_active)
            #break
            for i in Seed_Set:
                targets = Neighbour_finder(Networkx_Graph,Probability,d[str(i)])
                success = np.random.uniform(0,1,len(targets)) < Probability
                new_ones = list(np.extract(success, sorted(targets)))
                new_active = list(set(new_ones) - set(total))
                d[str(i)]= new_active
                d_new[str(i)] += new_active
                total+=new_active
            

            print(len(total),step)
            step+=1
            #print(Networkx_Graph)
        #print(A)
        if flag == 1:
            cnt_s += cnt
        spread.append(len(Ans))
    for i in Seed_Set:
        #print(i,len(d_new[str(i)])/len(total))
        result.append(len(d_new[str(i)])/len(total))
    return result
    #if flag==1:
    #    print(cnt_s/Num_of_Simulations)
    #print(spread)
    #return(np.mean(spread))

def cs_generator(filename, raw_seed_list, prob):
    Graph,nodenum,edgenum = read_graph(filename)
    return cs(Graph, raw_seed_list, prob, 1, 0)
'''
 For app.py usage
 input: data's filename, a raw list for seed
 output: "return d"
 app.py usage example: d = ssm_generator('./input.txt', [4, 5])
'''
def ssm_generator(filename, raw_seed_list):
    nodenum=0
    return [107, 3980, 698]
    Graph,nodenum,edgenum = read_graph(filename)
    AutoTree, SubTree, max_depth = read_AT("./at.txt")
    color = read_color("./color.txt")
    if len(raw_seed_list) > 0:
        seed,is_seed = read_seed(raw_seed_list, nodenum)
        #print(seed,is_seed)
        # Query_subgraph = Graph.subgraph(seed.tolist())
        # GraphM = isomorphism.GraphMatcher(Graph,Query_subgraph)
        # print("IsoDone!")

        # for i in GraphM.subgraph_monomorphisms_iter():
        #     print(i)
        enter = datetime.now()
        all_dict = enumerate_all(nodenum,AutoTree,Graph, seed)
        exit = datetime.now()
        interval = exit-enter
        print(f'ssm time used: {interval}')
        # print(d)
        return  all_dict
        
if __name__ == "__main__":
    #result = ssm_generator('./facebook1.txt',[107,3437,0,686,348,1684,1912,3980,698,21])
    #print(result)
    result = get_IM_LT([1,2,3], 5)
    print(result)
    #with open('tempssm.txt', 'w') as f:
    #    f.write(str(result))
    #enumerate_all()
    '''
    Ans = []
    AutoTree=[]
    S_set = []
    nodenum=0
    edgenum=0
    in_leaf = np.full(nodenum, -1)
    depth = np.full(nodenum,-1)
    max_depth=0
    Graph,nodenum,edgenum = read_graph("./case2.txt")
    read_AT("at.txt")
    color = read_color("color.txt")
    seed,is_seed = read_seed("seed.txt")
    # print(seed,is_seed)
    # Query_subgraph = Graph.subgraph(seed.tolist())
    # GraphM = isomorphism.GraphMatcher(Graph,Query_subgraph)
    # print("IsoDone!")

    # for i in GraphM.subgraph_monomorphisms_iter():
    #     print(i)
    enter = datetime.now()
    d = ssm(0,seed,is_seed)
    #enumerate_all()
    print(d)
    exit = datetime.now()
    interval = exit-enter
    print(f'time used: {interval}')
    # print(d)
    '''
#main1()
##print(np.loadtxt('seed.txt'))
#print(np.array([4, 5]))
#print(type(np.loadtxt('seed.txt')),np.loadtxt('seed1t.txt').shape ==(), np.array(np.loadtxt('seed.txt')) )
#print(np.array([1]).shape == ())
#print(np.loadtxt('seed1t.txt'))
#main()
