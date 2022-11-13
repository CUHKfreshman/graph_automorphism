from random import randint, choices

def edge_str_generator(a,b):
    return f'{a} {b}\n'

def edge_target_generator(node_id, max_id):
    if max_id - node_id < 4:
        if node_id in nodemap:
            edge_num = choices(list(range(node_id - node_id, max_id - node_id)), k  = 1)[0]
        elif node_id + 1 == max_id:
            edge_num = 1
        else:
            edge_num = choices(list(range(node_id - node_id + 1, max_id - node_id)), k  = 1)[0]
    elif node_id in nodemap:
        edge_num = choices([0,1,2,3], weights=[30, 7, 3, 1], k=1)[0]
    else:
        edge_num = choices([1,2,3,4], weights=[30, 3, 3, 1], k=1)[0]
    target_list = []
    i = 0
    while i != edge_num:
        target_node_id = randint(node_id + 1, max_id)
        if target_node_id not in target_list:
            target_list.append(target_node_id)
            i += 1
    return target_list

def graph_generator(node_num): # actually is total num - 1
    edge_num = 0
    edge_string = ''
    for node in range(0, node_num):
        target_list = edge_target_generator(node, node_num)
        nodemap.append(node)
        edge_num += len(target_list)
        for target in target_list:
            edge_string += edge_str_generator(node, target)
    return str(node_num + 1) + '\n' + str(edge_num) + '\n' + edge_string
        
nodemap = []      
with open('test.txt', 'w') as f:
    f.write(graph_generator(400))