import subprocess
def DviCL(filename):
    p = subprocess.Popen(['./DviCL/bliss',filename])
    p.wait()

'''readfile_at
Size:           1
4
Vertex list:    2
2 0 1 3 
Label:          3
0 1 2 3 
Children Size:  4
3
Children:       5
2 1 3 
Parent:         6
-1
sig:            7
0
depth:          8
0
total: 8 lines
'''
def readfile_at():
    full_tree = []
    corr_name = ['size', 'vertex_list', 'label', 'children_size', 'children', 'parent', 'sig', 'depth']
    canonical_order = 0
    with open('at.txt','r') as f:
        i = 1 # start from the first line
        tmp_tree = {} #tree to be read
        for line in f:
            if i in (2, 3, 5):
                tmp_tree[corr_name[i - 1]] = line.split()   ####!!!!!!!!!important: they are all string, not int
                tmp_tree[corr_name[i - 1]] = [str(n) for n in sorted(int(n) for n in tmp_tree[corr_name[i - 1]])]
            else:
                tmp_tree[corr_name[i - 1]] = line.rstrip()
                if i == 8:
                    tmp_tree['order'] = str(canonical_order)
                    canonical_order += 1
                    full_tree.append(tmp_tree)
                    tmp_tree = {}
                    i = 1
                    continue
            i += 1
    return full_tree

# return all autotrees
def find_autotrees(full_tree, id):
    candidate_trees = []
    for tree in full_tree:
        if id in tree['vertex_list']:
            candidate_trees.append(tree)
    return candidate_trees

if __name__ == "__main__":
    a = readfile_at()
    print(a[1])