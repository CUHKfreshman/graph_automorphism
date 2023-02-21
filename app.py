#import dash_cytoscape as cyto
#from dash import html, Dash, ctx, Dash
#import networkx as nx
#import pandas as pd
#from dash.dependencies import Input, Output, State
#import dash_bootstrap_components as dbc
#import dash_defer_js_import as dji
#import autotree
from math import ceil
from flask import Flask, render_template, request
import json
import ssm
import autotree
app = Flask(__name__, template_folder='templates', static_folder="static", static_url_path='/static')
'''
cyto_stylesheet = [
    # {'selector': '.TP', 'style': {'color':'red',"background-color": "red", }},
    # {'selector': '.FP', 'style': {'color':'lightblue', "background-color": "blue" }},
    # {'selector': '.center', 'style': {'color':'green', "background-color": "green" }},
    # {'selector': '.Real-Node', 'style': {'shape': 'circle'} },
    # {'selector': '.Fake-Node', 'style': {'shape': 'triangle'} },
    {'selector': 'node', 'style': {'width':'data(width)', 'height':'data(height)','font-size': '8px','label':'data(label)' } },#'data(label)'
    {'selector': 'edge', 'style': {'width':'0.5px' } },
    
    # set styles for mouse hover on a node
    {
        'selector': 'node.highlight',
        'style': {
            'border-color': '#FFF',
            'border-width': '1px'
        }
    },
    {
        'selector': 'node.semitransp',
        'style':{ 'opacity': '0.25' }
    },
    {
        'selector': 'edge.highlight',
        'style': { 
            'mid-target-arrow-color': '#FFF',
            'label': 'data(label)', # 🚩
            'color': 'white', # 🚩
            'font-size':'8px', # 🚩
            'width':'2.5px', # 🚩  
        }
    },
    
    {
        'selector': 'edge.semitransp',
        'style':{ 'opacity': '0.125' }
    },

]

def get_elements(file_name):
    # with open(file_name,'r') as f:
    #     first_line = f.readline()
    #     num_node = int(first_line)
    df = pd.read_csv(file_name, delimiter = " ", skiprows=2,header=None, names=['src','tar'])
    G = nx.from_pandas_edgelist(df, "src", "tar") # do we need to consider isolated nodes?
    element_nodes = [
        {
            'data': {
                'id':str(n), 
                'label': str(n),
                'width': str(4) + 'px',
                'height': str(4) + 'px',
            },
            'classes': 'node',
        }
        for n in G.nodes
    ]
    
    
    element_edges = [
        {
        'data': 
            {'source': str(s), 
            'target': str(t),
            },
        'classes':'edge',
        }
        for s,t in G.edges  
    ]

    return element_nodes,element_edges, G

def get_autotree_subgraph_elements(vertex_list):
    vertex_list = [int(n) for n in vertex_list]
    tree_edges = FULL_GRAPH.edges(vertex_list)
    element_nodes = [
        {
            'data': {
                'id':str(n), 
                'label': str(n),
                'width': str(4) + 'px',
                'height': str(4) + 'px',
            },
            'classes': 'node',
        }
        for n in vertex_list
    ]
    
    
    element_edges = [
        {
        'data': 
            {'source': str(s), 
            'target': str(t),
            },
        'classes':'edge',
        }
        for s,t in tree_edges if s in vertex_list and t in vertex_list
    ]
    return element_nodes,element_edges

def get_autotree_subgraph_elements_by_id(id):
    if id == "-1":
        return [{'data': {'id': '0', 'label': '0', 'width': '0px', 'height': '0px'}, 'classes': 'node'}], []
    vertex_list = [int(n) for n in full_autotree[int(id)]['vertex_list']]
    tree_edges = FULL_GRAPH.edges(vertex_list)
    element_nodes = [
        {
            'data': {
                'id':str(n), 
                'label': str(n),
                'width': str(4) + 'px',
                'height': str(4) + 'px',
            },
            'classes': 'node',
        }
        for n in vertex_list
    ]
    
    
    element_edges = [
        {
        'data': 
            {'source': str(s), 
            'target': str(t),
            },
        'classes':'edge',
        }
        for s,t in tree_edges if s in vertex_list and t in vertex_list
    ]
    return element_nodes,element_edges

def get_autotree_fullgraph_edges():
    edge = []
    for tree in full_autotree:
        if tree['children'][0] != '-1':
            for child in tree['children']:
                edge.append([tree['order'], child])
    return edge

def get_autotree_fullgraph():
    element_nodes = [
        {
            'data': {
                'id':tree['order'], 
                'label': tree['order'],
                'width': str(min(48, 4 * int(tree['size']))) + 'px',
                'height': str(min(48, 4 * int(tree['size']))) + 'px',
            },
            'classes': 'node',
        }
        for tree in full_autotree
    ]
    
    
    element_edges = [
        {
        'data': 
            {'source': str(s), 
            'target': str(t),
            },
        'classes':'edge',
        }
        for s,t in get_autotree_fullgraph_edges()
    ]
    return element_nodes, element_edges

def get_cyto_graph(file_name):
    element_nodes, element_edges, G = get_elements(file_name)
    #print(element_nodes+ element_edges)
    new_cyg = cyto.Cytoscape(
        id='cy-component',
        layout={'name': 'cose'}, # spread cose
        style={'width': '100%', 'height': '100%', 'background':'#FFF'},
        stylesheet=cyto_stylesheet,
        elements=element_nodes + element_edges,
        minZoom=1e-2,
        maxZoom=1e3,
    )
    return new_cyg, G


def init_autotree_subgraph():
    #element_nodes, element_edges = get_autotree_subgraph_elements(vertex_list)
    new_cyg = cyto.Cytoscape(
        id='cy-component-autotree-subgraph',
        layout={'name': 'cose'}, # spread cose
        style={'width': '100%', 'height': '100%', 'background':'#FFF'},
        stylesheet=cyto_stylesheet,
        elements=[{'data': {'id': '0', 'label': '0', 'width': '0px', 'height': '0px'}, 'classes': 'node'}],#init a false node in order to avoid error
        minZoom=1e-2,
        maxZoom=1e3,
    )
    return new_cyg

def init_autotree_fullgraph():
    element_nodes, element_edges = get_autotree_fullgraph()
    new_cyg = cyto.Cytoscape(
        id='cy-component-autotree-fullgraph',
        layout={'name': 'cose'}, # spread cose
        style={'width': '100%', 'height': '100%', 'background':'#FFF'},
        stylesheet=cyto_stylesheet,
        elements= element_nodes + element_edges,#init a false node in order to avoid error
        minZoom=1e-2,
        maxZoom=1e3,
    )
    return new_cyg

def init_autotree_subgraph_parent():
    new_cyg = cyto.Cytoscape(
        id='cy-component-autotree-subgraph-parent',
        layout={'name': 'cose'}, # spread cose
        style={'width': '100%', 'height': '100%', 'background':'#FFF'},
        stylesheet=cyto_stylesheet,
        elements=[{'data': {'id': '0', 'label': '0', 'width': '0px', 'height': '0px'}, 'classes': 'node'}],#init a false node in order to avoid error
        minZoom=1e-2,
        maxZoom=1e3,
    )
    return new_cyg

def init_autotree_subgraph_child():
    new_cyg = cyto.Cytoscape(
        id='cy-component-autotree-subgraph-child',
        layout={'name': 'cose'}, # spread cose
        style={'width': '100%', 'height': '100%', 'background':'#FFF'},
        stylesheet=cyto_stylesheet,
        elements=[{'data': {'id': '0', 'label': '0', 'width': '0px', 'height': '0px'}, 'classes': 'node'}],#init a false node in order to avoid error
        minZoom=1e-2,
        maxZoom=1e3,
    )
    return new_cyg

inputfile = 'input.txt'
autotree.DviCL(inputfile)# generate autotree
full_autotree = autotree.readfile_at()#read at.txt
external_scripts = None#['assets/sigma.js', 'assets/graphology.js', 'assets/sigma.min.js', 'assets/graphology-library.js', 'assets/graphology-library.min.js', ]
app = Dash(__name__, assets_ignore='biggraph.js',external_stylesheets=[dbc.themes.PULSE], external_scripts=external_scripts)
server = app.server
cyto_graph, FULL_GRAPH = get_cyto_graph(inputfile)
autotree_subgraph = init_autotree_subgraph()
autotree_fullgraph = init_autotree_fullgraph()
autotree_subgraph_parent = init_autotree_subgraph_parent()
autotree_subgraph_child = init_autotree_subgraph_child()
autotree_offcanvas = html.Div(
    [
        dbc.Offcanvas(
            [
                html.Div(
                    dbc.Row
                    ([
                        dbc.Col([
                            #html.Div([html.P('>>>', className='text-start'),html.P('Parent #id', className='text-center'),html.P('>>>', className='text-end')],className="my-auto w-100 d-flex justify-content-between"),
                            dbc.Card
                            ([
                                dbc.CardHeader('Corresponding AutoTree Subgraph', id='subgraph-header'),
                                dbc.CardBody
                                ([
                                    autotree_subgraph,
                                ])
                            ], class_name='h-75 align-self-center w-100'),
                            #html.Div([html.P('>>>', className='text-start'),html.P('Child #id', className='text-center'),html.P('>>>', className='text-end')],className="my-auto w-100 d-flex justify-content-between"),
                        ], class_name='h-100 d-flex flex-wrap justify-content-between', width=6),
                        dbc.Col
                        ([
                            dbc.Card([dbc.CardHeader('Parent', id='parent-header'), dbc.CardBody(autotree_subgraph_parent)], class_name='w-100', style={'height':'42vh'}),
                            dbc.Card([dbc.CardHeader('Child', id='child-header'), dbc.CardBody(autotree_subgraph_child)], class_name='w-100 align-self-end', style={'height':'42vh'})
                        ],width=6, class_name='h-100 d-flex flex-wrap justify-content-between')
                    ], class_name='mt-2 mb-2 ms-0 mb-0 w-100')
                ,className='border border-2 h-100 d-flex')
            ],
            id="offcanvas",
            title="AutoTree Analyzer",
            is_open=False,
            backdrop=False,
            style={'width':'66.5%'}
        ),
    ]
)
app.layout = dbc.Container(children=
                        [
                            #dbc.Navbar([
                            #            dbc.Container([
                            #                dbc.Row([
                            #                    dbc.Col(dbc.NavbarBrand('This is a navbar, or headline, or other functions integrated.'))
                            #                    ])
                            #                ])
                            #            ]),
                            dbc.Container([autotree_offcanvas,
                                            dbc.Row
                                            ([
                                                dbc.Col([
                                                    dbc.Card
                                                    (
                                                        [
                                                            #cyto_graph,
                                                            #dji.Import(src='./graphology.js'),
                                                            #dji.Import(src='./sigma.js'),
                                                            #dji.Import(src='./sigma.min.js'),
                                                            dji.Import(src='assets/biggraph.js'),
                                                            html.Div(id='orig-fullgraph-container', className='h-100 w-100'),
                                                            #dji.Import(src="./custom-script.js")
                                                        ],
                                                        id='cyto_div', class_name='border-3 p-0', style={"height":"95.5vh"},
                                                    ),
                                                ],width=8, class_name='p-2'),
                                                dbc.Col([
                                                    dbc.Row([
                                                        dbc.Row([
                                                            dbc.Card
                                                            (
                                                                [
                                                                    html.Div([html.P('Full AutoTree',className='m-0 d-inline align-bottom'),
                                                                              html.P('>>>', className='m-0 d-inline float-end text-secondary', id='autotree-entry',n_clicks=0)], className='card-header'),
                                                                    autotree_fullgraph,
                                                                ],
                                                                id='auto_tree',class_name='p-0 border-2', style={'height':'40vh','overflow':'hidden'}
                                                            )
                                                        ]),
                                                        dbc.Row([
                                                            dbc.Tabs([
                                                                dbc.Tab([
                                                                    dbc.Card([
                                                                        dbc.Input(type='file',name='readfile',id='readfile'),
                                                                        #dbc.CardBody([
                                                                        #    dbc.Row([
                                                                        #            dbc.Col(dbc.Label("Current Node ID", html_for="current-node"),width=4),
                                                                        #            dbc.Col(
                                                                        #                id='cytoscape-tapNodeData-output',
                                                                        #                width=8,align='text-center'
                                                                        #            ),
                                                                        #        ])
                                                                        #])
                                                                        
                                                                            dbc.Table(
                                                                            html.Tbody([
                                                                                html.Tr([html.Td("Node ID",className='w-25'),html.Td(id='cytoscape-tapNodeData-output')]),
                                                                                
                                                                                html.Tr([html.Td("Graph Size",className='w-25'),html.Td(id='size-output')]),
                                                                                
                                                                                html.Tr([html.Td("Vertices",className='w-25'),html.Td(id='vertex-output')]),
                                                                                
                                                                                #html.Tr([html.Td("Labels",className='w-25'),html.Td(id='label-output')]),
                                                                                
                                                                                html.Tr([html.Td("Children Size",className='w-25'),html.Td(id='childrensize-output')]),
                                                                                
                                                                                html.Tr([html.Td("Children",className='w-25'),html.Td(dbc.Pagination(max_value=0,id='children-output-pagination', active_page=None, class_name='mb-0 p-0 d-none',style={'margin-top':'0.35%'}), className='m-0 p-0')]),
                                                                                
                                                                                html.Tr([html.Td("Parent",className='w-25'),html.Td(id='parent-output')]),
                                                                                
                                                                                #html.Tr([html.Td("Signature",className='w-25'),html.Td(id='sig-output')]),
                                                                                
                                                                                html.Tr([html.Td("Depth",className='w-25'),html.Td(id='depth-output')]),
                                                                            ]),
                                                                            hover=True,bordered=True,striped=True,style={'width':'100%', 'margin-left':'-0.25%','margin-top':'-0.25%'}
                                                                        )
                                                                    ], class_name='mt-0 border-2 me-0 ms-0 be-0 bs-0', style={'height':'49vh'})
                                                                ], class_name='p-0',label='Single Selection'),
                                                            dbc.Tab([
                                                                    dbc.Card([
                                                                        #dbc.CardBody([
                                                                        #    dbc.Row([
                                                                        #            dbc.Col(dbc.Label("Current Node ID", html_for="current-node"),width=4),
                                                                        #            dbc.Col(
                                                                        #                id='cytoscape-tapNodeData-output',
                                                                        #                width=8,align='text-center'
                                                                        #            ),
                                                                        #        ])
                                                                        #])
                                                                        
                                                                            dbc.Table(
                                                                            html.Tbody([
                                                                                html.Tr([html.Td("Node IDs",className='w-25'),html.Td(id='other3-output')]),
                                                                                
                                                                                html.Tr([html.Td("Other4",className='w-25'),html.Td(id='other4-output')]),
                                                                                
                                                                                html.Tr([html.Td("Other5",className='w-25'),html.Td(id='other5-output')])
                                                                            ]),
                                                                            hover=True,bordered=True,striped=True,style={'width':'100.5%', 'margin-left':'-0.25%','margin-top':'-0.25%'}
                                                                        )
                                                                    ], class_name='mt-0 border-2 me-0 ms-0 be-0 bs-0')
                                                                ],label='Multiple Selection'),
                                                            dbc.Tab(label='SSM Analysis')
                                                            ])

                                                        ],class_name='mt-2 d-flex')
                                                    ])
                                                ],width=4,class_name='p-2 me-1 ms-1')
                                            ],class_name='w-100 flex-sm-nowrap'),
                                        ],fluid=True, class_name='p-0 mt-3 ms-3 me-3 h-100 d-flex flex-sm-nowrap  align-items-center justify-content-center justify-content-lg-start ')
                        ],fluid=True,class_name='p-0 m-0', style={'min-height':'100vh','overflow':'hidden'}
    )
'''
'''
@app.callback(Output('cy-component', 'stylesheet'),
              Input('cy-component', 'tapNodeData'))
def update_stylesheet(NodeData):
    new_styles=[]
    if NodeData is not None:
        #print(NodeData)
        new_styles =    [
            {
                'selector': f'#{NodeData["id"]}',
                'style': {
                    'background-color': 'red'
                }
            }]

    return cyto_stylesheet + new_styles
'''
'''

#autotree offcanvas
@app.callback(
    Output("offcanvas", "is_open"),
    Input("autotree-entry", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(Output('readfile',"value"),Input('readfile','value'))
def print_it(data):
    print(data)
    return data

@app.callback([ Output('cy-component-autotree-subgraph', 'elements'),
                Output('cy-component-autotree-subgraph-parent', 'elements'),
                Output('cy-component-autotree-subgraph-child', 'elements'),
                Output('cytoscape-tapNodeData-output', 'children'),
                Output('size-output','children'),
                Output('vertex-output','children'),
                #Output('label-output','children'),
                Output('childrensize-output','children'),
                Output('children-output-pagination','min_value'),
                Output('children-output-pagination','max_value'),
                Output('children-output-pagination','class_name'),
                Output('parent-output','children'),
                #Output('sig-output','children'),
                Output('depth-output','children'),
                Output('cy-component-autotree-fullgraph', 'stylesheet'),
                Output('cy-component-autotree-subgraph', 'stylesheet'),
                Output('cy-component-autotree-subgraph-parent', 'stylesheet'),
                Output('cy-component-autotree-subgraph-child', 'stylesheet'),
                Output('subgraph-header','children'),
                Output('parent-header','children'),
                Output('child-header','children'),],
                [#Input('cy-component', 'tapNodeData'),
                Input('cy-component-autotree-fullgraph', 'tapNodeData'),
                Input('children-output-pagination', 'active_page'),
                State('cy-component-autotree-subgraph', 'elements'),
                State('cy-component-autotree-subgraph-parent', 'elements'),
                State('cy-component-autotree-subgraph-child', 'elements'),
                State('cytoscape-tapNodeData-output', 'children'),
                State('size-output','children'),
                State('vertex-output','children'),
                #State('label-output','children'),
                State('childrensize-output','children'),
                State('children-output-pagination','min_value'),
                State('children-output-pagination','max_value'),
                State('children-output-pagination','class_name'),
                State('parent-output','children'),
                #State('sig-output','children'),
                State('depth-output','children'),
                State('cy-component-autotree-fullgraph','stylesheet'),
                State('cy-component-autotree-subgraph','stylesheet'),
                State('cy-component-autotree-subgraph-parent','stylesheet'),
                State('cy-component-autotree-subgraph-child','stylesheet'),
                State('subgraph-header','children'),
                State('parent-header','children'),
                State('child-header','children'),
                ])
#data_origraph, data_fullgraph, data_pagination, elements, elements_parent, elements_child, node_id, size, vertex, label, children_size, min_val,max_val, child_class_name, parent, sig, depth, stylesheet_fullgraph, stylesheet_subgraph, stylesheet_subgraph_parent, stylesheet_subgraph_child, subgraph_header, parent_header, child_header
def update_graphs_switcher(data_fullgraph, data_pagination, elements, elements_parent, elements_child, node_id, size, vertex,  children_size, min_val,max_val, child_class_name, parent, depth, stylesheet_fullgraph, stylesheet_subgraph, stylesheet_subgraph_parent, stylesheet_subgraph_child, subgraph_header, parent_header, child_header ):
    triggered_func = ctx.triggered_id
    print('triggered',triggered_func)
    #if triggered_func == 'cy-component':
    #    return update_graphs_by_origraph_single(data_origraph, elements_child, child_class_name, subgraph_header, parent_header, child_header)
    if triggered_func == 'cy-component-autotree-fullgraph':
        return update_graphs_by_autotree_fullgraph(data_fullgraph, elements_child, node_id, child_class_name, subgraph_header, parent_header, child_header)
    if triggered_func == 'children-output-pagination':
        return update_child_graph_by_pagination(data_pagination, elements, elements_parent,  node_id, size, vertex,  children_size, min_val,max_val, child_class_name,  parent,  depth, stylesheet_fullgraph, stylesheet_subgraph,stylesheet_subgraph_parent,  stylesheet_subgraph_child , subgraph_header, parent_header, child_header)
    return elements, elements_parent, elements_child, node_id, size, vertex,  children_size, min_val,max_val, child_class_name,  parent,  depth, stylesheet_fullgraph, stylesheet_subgraph, stylesheet_subgraph_parent, stylesheet_subgraph_child, subgraph_header, parent_header, child_header

# update when click the original graph node #tmp: (data, elements, elements_parent, elements_child, id, size, vertex, label, children_size, min_val,max_val,  child_class_name, parent, sig, depth)
def update_graphs_by_origraph_single(data, elements_child, child_class_name, subgraph_header, parent_header, child_header):
    if data:
        selected_id = str(data['id'])
        corr_trees = autotree.find_autotrees(full_autotree, selected_id) # all autotrees which have the selected node
        if len(corr_trees) != 0:#if has autotree
            # default the second largest node (the largest node is the FULL_GRAPH itself)
            largest_tree = corr_trees[1]#TODO: More functionalities in autotree analyzer
            element_nodes, element_edges = get_autotree_subgraph_elements(largest_tree['vertex_list'])
            element_nodes_parent, element_edges_parent = get_autotree_subgraph_elements_by_id(largest_tree['parent'])
            #element_nodes_child, element_edges_child = get_autotree_subgraph_elements_by_id(largest_tree['children'][0])
            #print(element_nodes + element_edges)
            #print(largest_tree)
            
            new_styles_subgraph =    [
                {
                    'selector': f'#{data["id"]}',
                    'style': {
                        'background-color': 'red'
                    }
                }]
            new_styles_fullgraph =    [
                {
                    'selector': f'#{tree["order"]}',
                    'style': {
                        'background-color': 'green'
                    }
                } for tree in corr_trees if tree['order'] != largest_tree['order']]
            new_styles_fullgraph.append({'selector': f'#{largest_tree["order"]}', 'style': {'background-color': 'red'}})
            if int(largest_tree['children'][0]) == -1:
                largest_tree['children_size'] = '0'
                child_class_name = 'mb-0 p-0 d-none'
            else:
                child_class_name = 'mb-0 p-0'
            subgraph_header, parent_header = f'Corresponding AutoTree Subgraph #{largest_tree["order"]}', f'Parent #{largest_tree["parent"]}'
            return  element_nodes + element_edges,element_nodes_parent + element_edges_parent, elements_child , str(data['id']), largest_tree['size'], str(largest_tree['vertex_list']), str(largest_tree['label']), largest_tree['children_size'], int(largest_tree['children'][0]), int(largest_tree['children'][-1]),  child_class_name, largest_tree['parent'],  largest_tree['depth'],  cyto_stylesheet + new_styles_fullgraph, cyto_stylesheet + new_styles_subgraph, cyto_stylesheet + new_styles_subgraph, cyto_stylesheet + new_styles_subgraph, subgraph_header, parent_header, child_header
    #return elements, elements_parent, elements_child, id, size, vertex, label, children_size, min_val,max_val,  child_class_name, parent, sig, depth, cyto_stylesheet, cyto_stylesheet, cyto_stylesheet, cyto_stylesheet

def update_graphs_by_autotree_fullgraph(data, elements_child, node_id, child_class_name, subgraph_header, parent_header, child_header):
    if data:
        selected_id = str(data['id'])
        corr_trees = autotree.find_autotrees(full_autotree, node_id) # all autotrees which have the selected node
        new_tree = full_autotree[int(selected_id)]#TODO: More functionalities in autotree analyzer
        
        element_nodes, element_edges = get_autotree_subgraph_elements_by_id(selected_id)
        element_nodes_parent, element_edges_parent = get_autotree_subgraph_elements_by_id(new_tree['parent'])
        #element_nodes_child, element_edges_child = get_autotree_subgraph_elements_by_id(new_tree['children'][0])
        new_styles_subgraph =    [
            {
                'selector': f'#{node_id}',
                'style': {
                    'background-color': 'red'
                }
            }]
        new_styles_fullgraph =    [
            {
                'selector': f'#{tree["order"]}',
                'style': {
                    'background-color': 'green'
                }
            } for tree in corr_trees if selected_id != tree['order']]
        new_styles_fullgraph.append({'selector': f'#{selected_id}', 'style': {'background-color': 'red'}})
        if int(new_tree['children'][0]) == -1:
            new_tree['children_size'] = '0'
            child_class_name = 'mb-0 p-0 d-none'
        else:
            child_class_name = 'mb-0 p-0'
        if new_tree['parent'] == '-1':
            new_tree['parent'] = 'None'
        subgraph_header, parent_header,child_header = f'Corresponding AutoTree Subgraph #{new_tree["order"]}', f'Parent #{new_tree["parent"]}', 'Child'
        return  element_nodes + element_edges,element_nodes_parent + element_edges_parent,init_autotree_subgraph_child(), node_id, new_tree['size'], str(new_tree['vertex_list']), str(new_tree['label']), new_tree['children_size'], int(new_tree['children'][0]), int(new_tree['children'][-1]), child_class_name, new_tree['parent'],  new_tree['depth'],  cyto_stylesheet + new_styles_fullgraph, cyto_stylesheet + new_styles_subgraph,  cyto_stylesheet + new_styles_subgraph, cyto_stylesheet + new_styles_subgraph, subgraph_header, parent_header, child_header

def update_child_graph_by_pagination(data, elements, elements_parent, node_id, size, vertex, children_size, min_val,max_val, child_class_name,  parent,  depth, stylesheet_fullgraph, stylesheet_subgraph, stylesheet_subgraph_parent, stylesheet_subgraph_child, subgraph_header, parent_header, child_header ):
    if data:
        selected_id = str(data)
        element_nodes_child, element_edges_child = get_autotree_subgraph_elements_by_id(selected_id)
        corr_trees = autotree.find_autotrees(full_autotree, node_id) # all autotrees which have the selected node
        for element in stylesheet_fullgraph:
            if '#' in element['selector']:
                if element['style']['background-color'] == 'red':
                    red_chosen_node = element['selector'][1:]
                    break
        new_styles_fullgraph =    [
            {
                'selector': f'#{tree["order"]}',
                'style': {
                    'background-color': 'green'
                }
            } for tree in corr_trees if selected_id != tree['order'] and selected_id != red_chosen_node]
        new_styles_fullgraph.append({'selector':f'#{red_chosen_node}', 'style':{'background-color': 'red'}})
        new_styles_fullgraph.append({'selector': f'#{selected_id}', 'style': {'background-color': 'purple'}})
        child_header = f'Child #{selected_id}'
 
    return elements, elements_parent, element_nodes_child + element_edges_child, node_id, size, vertex,  children_size, min_val,max_val, child_class_name,  parent, depth,  cyto_stylesheet + new_styles_fullgraph, stylesheet_subgraph, stylesheet_subgraph_parent, stylesheet_subgraph_child, subgraph_header, parent_header, child_header
if __name__ == '__main__':
    app.run_server(debug=True)
'''
ssm_all_dict= {}
@app.route('/',methods=['GET','POST'])
def mainpage():
    return render_template('index.html')
@app.route('/upload', methods = ['POST'])
def get_post_javascript_data():
    tempssm_Facebook= {0: [[0]], 3437: [[3437]], 107: [[107]], 414: [[414]], 3980: [[3980]], 1912: [[1912]], 1684: [[1684]], 698: [[698]], 348: [[348]], 686: [[686]], 171: [[171]], 3918: [[3918]], 192: [[192]], 49: [[49]], 453: [[453]], 4027: [[4027]], 2456: [[2456]], 757: [[757]], 179: [[179]], 23: [[23]], 230: [[230]], 532: [[532]], 19: [[19]], 1202: [[1202]], 1240: [[1240]], 2863: [[2863]], 143: [[143]], 833: [[833]], 4017: [[4017]], 3999: [[3999]], 58: [[58]], 312: [[312]], 1909: [[1909]], 885: [[885]], 3789: [[3789]], 596: [[596]], 3610: [[3610]], 1860: [[1860]], 260: [[260]], 3887: [[3887]], 563: [[563]], 848: [[848]], 3536: [[3536]], 4023: [[4023]], 770: [[770]], 5: [[5]], 2668: [[2668]], 1660: [[1660]], 3077: [[3077]], 219: [[219]], 111: [[111]], 3271: [[3271]], 1591: [[1591]], 280: [[280]], 81: [[81]], 3200: [[3200]], 3592: [[3592]], 239: [[239]], 243: [[243]], 3996: [[3996]], 3891: [[3891]], 3544: [[3544]], 1536: [[1536]], 3556: [[3556]], 133: [[133]], 3187: [[3187]], 3136: [[3136]], 386: [[386]], 617: [[617]], 3561: [[3561]], 740: [[740]], 1835: [[1835]], 3503: [[3503]], 1739: [[1739]], 904: [[904]], 301: [[301]], 3801: [[3801]], 1347: [[1347]], 383: [[383]], 1791: [[1791]], 1711: [[1711]], 1797: [[1797]], 3987: [[4001], [4029], [3987], [4012]], 4012: [[4001], [4029], [3987], [4012]], 4001: [[3987], [4012], [4001], [4029]], 4029: [[3987], [4012], [4001], [4029]], 581: [[581], [642]], 642: [[581], [642]], 33: [[233], [256], [244], [282], [33], [42]], 42: [[233], [256], [244], [282], [33], [42]], 233: [[33], [42], [244], [282], [233], [256]], 256: [[33], [42], [244], [282], [233], [256]], 244: [[33], [42], [233], [256], [244], [282]], 282: [[33], [42], [233], [256], [244], [282]], 3746: [[3746], [3846]], 3846: [[3746], [3846]], 3268: [[3268], [3407]], 3407: [[3268], [3407]], 3830: [[3830]], 25: [[25]], 1890: [[1890]], 88: [[88]], 3672: [[3672]], 4000: [[4000]], 1194: [[1194]], 174: [[174]], 2527: [[2527]], 182: [[182]], 2691: [[2691], [2792], [3037]], 2792: [[2691], [2792], [3037]], 3037: [[2691], [2792], [3037]], 437: [[437]], 3690: [[3690]], 2421: [[2421]], 2313: [[2313]], 3861: [[3861]], 3442: [[3442]], 3546: [[3546]], 4031: [[4031]], 3989: [[3989]], 594: [[594]], 1002: [[1002], [1105]], 1105: [[1002], [1105]], 3998: [[3998]], 2734: [[2734]], 277: [[277]], 3680: [[3680]], 2805: [[2805]], 2677: [[2677]], 387: [[387]], 157: [[157]], 2483: [[2483], [2595]], 2595: [[2483], [2595]], 1046: [[1046], [1586]], 1586: [[1046], [1586]], 428: [[428]], 175: [[175]], 3616: [[3616]], 324: [[324]], 1469: [[1469]], 2535: [[2535]], 322: [[322]], 564: [[564]], 1956: [[1956]], 2106: [[2106]], 504: [[504]], 3045: [[3045]], 498: [[498]], 460: [[460]], 3533: [[3533]], 3: [[3]], 3954: [[3954]], 1133: [[1133]], 356: [[356]], 3949: [[3949]], 285: [[285]], 3439: [[3439]], 1283: [[1283]], 56: [[56]], 3105: [[3105]], 3521: [[3521]], 782: [[782]], 1030: [[1030]], 734: [[734]], 727: [[727]], 3443: [[3443]], 77: [[77]], 472: [[472]], 1442: [[1442]], 411: [[411]], 1027: [[1027], [1627]], 1627: [[1027], [1627]], 616: [[616]], 53: [[53]], 2321: [[2321]], 29: [[29]], 1499: [[1499]], 784: [[784]], 130: [[130]], 584: [[584]], 3168: [[3168]], 991: [[991]], 1693: [[1693]], 193: [[193]], 363: [[363]], 3028: [[3028]], 1357: [[1357]], 3121: [[3121]], 3986: [[3986]], 1889: [[1889]], 351: [[351]], 3872: [[3872]], 3274: [[3274]], 269: [[269]], 3921: [[3921]], 307: [[307]], 97: [[97], [253]], 253: [[97], [253]], 1071: [[1071], [1253]], 1253: [[1071], [1253]], 1254: [[1254]], 3019: [[3019]], 3648: [[3648]], 2711: [[2711]], 2791: [[2791]], 432: [[432]], 2979: [[2979]], 2936: [[2936]], 3303: [[3303]], 3721: [[3721]], 3633: [[3633]], 2448: [[2448]], 2738: [[2738]], 2946: [[2946]], 2316: [[2316]], 3621: [[3621]], 580: [[580]], 413: [[413]], 3157: [[3157]], 2499: [[2499]], 2821: [[2821]], 2766: [[2766]], 3752: [[3752]], 1259: [[1259]], 1070: [[1070]], 3265: [[3265]], 283: [[283]], 124: [[124]], 155: [[155]], 3694: [[3694]], 2037: [[2037]], 846: [[846]], 222: [[222]], 270: [[270]], 120: [[120]], 1760: [[1760]], 3560: [[3717], [3744], [3560], [3691]], 3691: [[3717], [3744], [3560], [3691]], 3717: [[3560], [3691], [3717], [3744]], 3744: [[3560], [3691], [3717], [3744]], 401: [[401]], 377: [[377]], 90: [[90], [145]], 145: [[90], [145]], 286: [[286]], 47: [[47]], 3885: [[3885]], 1224: [[1224]], 798: [[798]], 3990: [[3990], [4007], [4016], [4025]], 4007: [[3990], [4007], [4016], [4025]], 4016: [[3990], [4007], [4016], [4025]], 4025: [[3990], [4007], [4016], [4025]], 173: [[173]], 376: [[376]], 115: [[115]], 556: [[556]], 864: [[864]], 2017: [[2017]], 857: [[857]], 2581: [[2581]], 717: [[717], [852], [855]], 852: [[717], [852], [855]], 855: [[717], [852], [855]], 436: [[436]], 2437: [[2437]], 3823: [[3823]], 464: [[464]], 720: [[720]], 136: [[136]], 350: [[350]], 862: [[862]], 1650: [[1650]], 3701: [[3701]], 1208: [[1208]], 8: [[8], [91], [259]], 91: [[8], [91], [259]], 259: [[8], [91], [259]], 110: [[110], [264]], 264: [[110], [264]], 2558: [[2558]], 856: [[856]], 3742: [[3742]], 119: [[119]], 3720: [[3720]], 870: [[870]], 3799: [[3799]], 198: [[198]], 3638: [[3638]], 329: [[329]], 3756: [[3756]], 1537: [[1537]], 3775: [[3775]], 884: [[884]], 1505: [[1505]], 879: [[879]], 806: [[806]], 732: [[732]], 2034: [[2034]], 3982: [[3982]], 1545: [[1545]], 1473: [[1473]], 3530: [[3530]], 800: [[800]], 3586: [[3586]], 170: [[170]], 713: [[713]], 736: [[736]], 1029: [[1029]], 1098: [[1098]], 982: [[982]], 359: [[359]], 361: [[361]], 3477: [[3477]], 825: [[825]], 2357: [[2357]], 1013: [[1013]], 384: [[384], [552]], 552: [[384], [552]], 1594: [[1594]], 1654: [[1654]], 893: [[893]], 89: [[89], [319]], 319: [[89], [319]], 6: [[6], [147]], 147: [[6], [147]], 3679: [[3679]], 776: [[776]], 867: [[867]], 3847: [[3847]], 866: [[866]], 95: [[95]], 3612: [[3612]], 137: [[137]], 1000: [[1000]], 1840: [[1840]], 40: [[40]], 3548: [[3548]], 3836: [[3836]], 3880: [[3880]], 828: [[828]], 3908: [[3908]], 1165: [[1165]], 4014: [[4014]], 1666: [[1666]], 3963: [[3963]], 3637: [[3637]], 1087: [[1087]], 3740: [[3740]], 4020: [[4020]], 3495: [[3495]], 3994: [[3994]], 3930: [[3930]], 3280: [[3280]], 4002: [[4002]], 3661: [[3661]], 745: [[745]], 2904: [[2904]], 3272: [[3272]], 3625: [[3625]], 3583: [[3583]], 203: [[203]], 2412: [[2412]], 3774: [[3774]], 3571: [[3571]], 1996: [[1996], [2565]], 2565: [[1996], [2565]], 803: [[803]], 214: [[214]], 3513: [[3513]], 3455: [[3455]], 1730: [[1730]], 995: [[995]], 169: [[169]], 1134: [[1134]], 3705: [[3705]], 3084: [[3084]], 3153: [[3153]], 3664: [[3664]], 3042: [[3042]], 739: [[739]], 2168: [[2168]], 3596: [[3596]], 3454: [[3454]], 2813: [[2813]], 1676: [[1676]], 3671: [[3671]], 1268: [[1268]], 178: [[178]], 71: [[71]], 3526: [[3526]], 467: [[467], [572]], 572: [[467], [572]], 121: [[121]], 372: [[372]], 3901: [[3901]], 1086: [[1086]], 3792: [[3792]], 3670: [[3670]], 3970: [[3970]], 199: [[199]], 3095: [[3095]], 2745: [[2745]], 166: [[166]], 315: [[315]], 1574: [[1574]], 1770: [[1770]], 3635: [[3635]], 3290: [[3290]], 2838: [[2838], [3003]], 3003: [[2838], [3003]], 865: [[865], [868]], 868: [[865], [868]], 202: [[202]], 96: [[96]], 3760: [[3760]], 1419: [[1419]], 2015: [[2015]], 2422: [[2422]], 3827: [[3827]], 247: [[247]], 3759: [[3759]], 2087: [[2087]], 3862: [[3862]], 3781: [[3781], [3946]], 3946: [[3781], [3946]], 4005: [[4005]], 2443: [[2443]], 1768: [[1768]], 1778: [[1778]], 1157: [[1157]], 2385: [[2385]], 3914: [[3914]], 112: [[112], [293]], 293: [[112], [293]], 3733: [[3733]], 832: [[832]], 790: [[790]], 3036: [[3036]], 229: [[229]], 220: [[220], [262]], 262: [[220], [262]], 2302: [[2302]], 941: [[941]], 1704: [[1704]], 1444: [[1444]], 1406: [[1406]], 2808: [[2808]], 1492: [[1492]], 4036: [[4036]], 4028: [[4028]], 76: [[76]], 749: [[749], [775]], 775: [[749], [775]], 241: [[241], [255]], 255: [[241], [255]], 1808: [[1808]], 912: [[912]], 2774: [[2774], [3055], [3074], [3127]], 3055: [[2774], [3055], [3074], [3127]], 3074: [[2774], [3055], [3074], [3127]], 3127: [[2774], [3055], [3074], [3127]], 3825: [[3825]], 881: [[881]], 1171: [[1171]], 1964: [[1964]], 3539: [[3539]], 3652: [[3652]], 895: [[895]], 483: [[483]], 567: [[567]], 3444: [[3444], [3849]], 3849: [[3444], [3849]], 3665: [[3665]], 910: [[910], [1657], [1776]], 1657: [[910], [1657], [1776]], 1776: [[910], [1657], [1776]], 3904: [[3904]], 1664: [[1664]], 871: [[871]], 3662: [[3662]], 2217: [[2217]], 3923: [[3923]], 4030: [[4030]], 339: [[339]], 1317: [[1317]], 2263: [[2263]], 364: [[364]], 771: [[771]], 2861: [[2861]], 3751: [[3751]], 2152: [[2152]], 961: [[961]], 3141: [[3141]], 177: [[177]], 422: [[422]], 412: [[412]], 278: [[278]], 2528: [[2528]], 3267: [[3267]], 3727: [[3727]], 3745: [[3745]], 3489: [[3489], [3676]], 3676: [[3489], [3676]], 894: [[894]], 2156: [[2156]], 1607: [[1607]], 3791: [[3791]], 1387: [[1387]], 3233: [[3233]], 1540: [[1540]], 3931: [[3931]], 513: [[513]], 3279: [[3279]], 1672: [[1672]], 1089: [[1089]], 1057: [[1057]], 2869: [[2869]], 2283: [[2283]], 1024: [[1024]], 1518: [[1518]], 1701: [[1701]], 1471: [[1471]], 2099: [[2099]], 2884: [[2884]], 1501: [[1501]], 3565: [[3565]], 899: [[899]], 1642: [[1642]], 2281: [[2281], [2487]], 2487: [[2281], [2487]], 769: [[769]], 3327: [[3327]], 2041: [[2041]], 3248: [[3248]], 818: [[818]], 2771: [[2771]], 2214: [[2214]], 1838: [[1838]], 2453: [[2453]], 3487: [[3487]], 3551: [[3551]], 2836: [[2836]], 2949: [[2949]], 2886: [[2886]], 1725: [[1725]], 3950: [[3950]], 1785: [[1785]], 3626: [[3626]], 1749: [[1749]], 1106: [[1106]], 3440: [[3440]], 2094: [[2094]], 3162: [[3162]], 645: [[645]], 2776: [[2776]], 252: [[252]], 427: [[427]], 697: [[697]], 2951: [[2951]], 1264: [[1264]], 1974: [[1974]], 2651: [[2651]], 3504: [[3504]], 3256: [[3256]], 2926: [[2926]], 3677: [[3677]], 3927: [[3927]], 508: [[508]], 4009: [[4009]], 2789: [[2789]], 434: [[434]], 2204: [[2204]], 1138: [[1138]], 3961: [[3961]], 2999: [[2999]], 2693: [[2693]], 1896: [[1896]], 1555: [[1555]], 3659: [[3659]], 1360: [[1360]], 3809: [[3809]], 480: [[480]], 3537: [[3537]], 478: [[478]], 3300: [[3300]], 2978: [[2978]], 3916: [[3916]], 3374: [[3374]], 819: [[819]], 937: [[937]], 3269: [[3269]], 534: [[534]], 1150: [[1150]], 1277: [[1277]], 4: [[4], [181], [275]], 181: [[4], [181], [275]], 275: [[4], [181], [275]], 78: [[78], [195], [218], [273], [306], [328]], 195: [[78], [195], [218], [273], [306], [328]], 218: [[78], [195], [218], [273], [306], [328]], 273: [[78], [195], [218], [273], [306], [328]], 306: [[78], [195], [218], [273], [306], [328]], 328: [[78], [195], [218], [273], [306], [328]], 939: [[939]], 1861: [[1861]], 1023: [[1023]], 3072: [[3072]], 118: [[118]], 2406: [[2406]], 2682: [[2682]], 122: [[122]], 1053: [[1053]], 3826: [[3826]], 1722: [[1722]], 1295: [[1295]], 1297: [[1297]], 454: [[454]], 518: [[518]], 3803: [[3803]], 397: [[397]], 3365: [[3365]], 3324: [[3324]], 3674: [[3674]], 968: [[968]], 3888: [[3888]], 799: [[799]], 3564: [[3564]], 1670: [[1670]], 156: [[156]], 1553: [[1553]], 533: [[533]], 3632: [[3632]], 21: [[21]], 3848: [[3848]], 3449: [[3449]], 1154: [[1154]], 1527: [[1527]], 59: [[59]], 1899: [[1899]], 2540: [[2540]], 1435: [[1435]], 362: [[362]], 470: [[470]], 2885: [[2885]], 3929: [[3929]], 3750: [[3750]], 1937: [[1937]], 917: [[917]], 3535: [[3535]], 3867: [[3867]], 431: [[431]], 2345: [[2345]], 1161: [[1161]], 1332: [[1332]], 1694: [[1694]], 506: [[506]], 368: [[368]], 1110: [[1110]], 542: [[542]], 3608: [[3608]], 896: [[896]], 2358: [[2358]], 1383: [[1383]], 777: [[777]], 54: [[54]], 61: [[61]], 228: [[228]], 477: [[477]], 604: [[604]], 566: [[566]], 998: [[998]], 1894: [[1894]], 1598: [[1598]], 1621: [[1621]], 3816: [[3816]], 2961: [[2961]], 2441: [[2441]], 1214: [[1214]], 669: [[669]], 3270: [[3270]], 443: [[443], [468]], 468: [[443], [468]], 52: [[52], [205]], 205: [[52], [205]], 3875: [[3875]], 3808: [[3808]], 2788: [[2788]], 1270: [[1270]], 1854: [[1854]], 2962: [[2962]], 2817: [[2817], [3147]], 3147: [[2817], [3147]], 4004: [[4004]], 3894: [[3894]], 2671: [[2671], [2721], [2824], [3091]], 2721: [[2671], [2721], [2824], [3091]], 2824: [[2671], [2721], [2824], [3091]], 3091: [[2671], [2721], [2824], [3091]], 227: [[227]], 100: [[100]], 872: [[872], [874]], 874: [[872], [874]], 4038: [[4038]], 2439: [[2439]], 3995: [[3995]], 3787: [[3787]], 3624: [[3624]], 1758: [[1758]], 231: [[231]], 3988: [[3988]], 373: [[373]], 2411: [[2411]], 3606: [[3606]], 3870: [[3870]], 99: [[99]], 858: [[858]], 310: [[310]], 822: [[822]], 150: [[150]], 7: [[7]], 2893: [[2893]], 41: [[41]], 399: [[399], [441], [501]], 441: [[399], [441], [501]], 501: [[399], [441], [501]], 337: [[337]], 3511: [[3511]], 332: [[332]], 2133: [[2133]], 2450: [[2450]], 630: [[630]], 3932: [[3932]], 3584: [[3584]], 3617: [[3617]], 1127: [[1127]], 3749: [[3749]], 3538: [[3538]], 3682: [[3682]], 2317: [[2317]], 592: [[592]], 3897: [[3897]], 225: [[225]], 3985: [[3985]], 3993: [[3993]], 93: [[93]], 263: [[263], [296]], 296: [[263], [296]], 1304: [[1304]], 929: [[929]], 889: [[889]], 3580: [[3580]], 167: [[167]], 1702: [[1702]], 313: [[313]], 343: [[343]], 20: [[20]], 3505: [[3505]], 1911: [[1911]], 1369: [[1369]], 327: [[327]], 2724: [[2724]], 3302: [[3302]], 2047: [[2047]], 2113: [[2113]], 2236: [[2236]], 3806: [[3806]], 1193: [[1193]], 3216: [[3216]], 3483: [[3483]], 3553: [[3553]], 3508: [[3508]], 3139: [[3139]], 3738: [[3738]], 3392: [[3392]], 4011: [[4011]], 3938: [[3938]], 3831: [[3831]], 3948: [[3948]], 1794: [[1794]], 3703: [[3703]], 2663: [[2663]], 3737: [[3737]], 2726: [[2726]], 1114: [[1114]], 1626: [[1626]], 1321: [[1321]], 353: [[353]], 1177: [[1177]], 539: [[539]], 3629: [[3629]], 2031: [[2031]], 2760: [[2760]], 955: [[955], [1368]], 1368: [[955], [1368]], 3057: [[3057]], 3154: [[3154]], 3366: [[3366]], 4013: [[4013]], 3027: [[3027]], 746: [[746]], 1450: [[1450]], 1667: [[1667]], 261: [[261]], 3318: [[3318]], 2670: [[2670]], 1783: [[1783]], 3812: [[3812]], 1529: [[1529]], 3227: [[3227]], 3771: [[3771]], 1549: [[1549]], 213: [[213]], 1088: [[1088]], 3905: [[3905]], 3525: [[3525]], 1827: [[1827]], 3780: [[3780]], 1571: [[1571]], 3176: [[3176]], 920: [[920]], 190: [[190]], 117: [[117]], 1486: [[1486]], 2514: [[2514]], 1483: [[1483]], 2066: [[2066]], 3464: [[3464]], 2548: [[2548]], 2207: [[2207]], 109: [[109]], 148: [[148]], 407: [[407]], 510: [[510]], 1447: [[1447]], 1923: [[1923]], 2968: [[2968]], 2474: [[2474]], 1970: [[1970]], 3619: [[3619]], 271: [[271]], 334: [[334]], 475: [[475]], 830: [[830]], 3844: [[3844]], 2889: [[2889]], 1308: [[1308]], 342: [[342]], 1988: [[1988]], 2401: [[2401]], 1876: [[1876]], 3952: [[3952]], 3229: [[3229]], 3232: [[3232]], 3543: [[3543]], 2895: [[2895]], 3991: [[3991]], 1252: [[1252]], 1936: [[1936]], 3225: [[3225]], 1472: [[1472]], 943: [[943]], 1934: [[1934]], 360: [[360]], 3693: [[3693]], 3119: [[3119]], 3188: [[3188]], 657: [[657]], 1477: [[1477]], 2622: [[2622]], 3598: [[3598]], 2959: [[2959]], 249: [[249]], 2846: [[2846]], 433: [[433]], 3140: [[3140]], 3769: [[3769]], 3939: [[3939]], 3034: [[3034]], 3013: [[3013]], 38: [[38]], 246: [[246]], 1213: [[1213]], 964: [[964]], 2934: [[2934]], 408: [[408]], 905: [[905]], 3245: [[3245]], 3314: [[3314]], 2748: [[2748]], 3016: [[3016]], 3651: [[3651]], 1590: [[1590]], 2259: [[2259]], 2641: [[2641]], 520: [[520]], 3663: [[3663]], 2230: [[2230]], 2226: [[2226]], 1371: [[1371]], 3944: [[3944]], 3941: [[3941]], 2686: [[2686]], 1093: [[1093]], 2419: [[2419]], 1220: [[1220]], 2909: [[2909]], 450: [[450]], 1037: [[1037]], 2927: [[2927]], 3194: [[3194]], 1117: [[1117]], 785: [[785]], 2777: [[2777]], 3390: [[3390]], 2800: [[2800]], 926: [[926]], 1091: [[1091]], 294: [[294]], 3044: [[3044]], 2980: [[2980]], 154: [[154]], 31: [[31]], 3502: [[3502]], 3669: [[3669], [3700], [3813], [3864], [3911]], 3700: [[3669], [3700], [3813], [3864], [3911]], 3813: [[3669], [3700], [3813], [3864], [3911]], 3864: [[3669], [3700], [3813], [3864], [3911]], 3911: [[3669], [3700], [3813], [3864], [3911]], 2301: [[2301]], 84: [[84]], 3251: [[3251]], 2732: [[2732], [2930], [3131], [3180], [3181]], 2930: [[2732], [2930], [3131], [3180], [3181]], 3131: [[2732], [2930], [3131], [3180], [3181]], 3180: [[2732], [2930], [3131], [3180], [3181]], 3181: [[2732], [2930], [3131], [3180], [3181]], 873: [[873], [887]], 887: [[873], [887]], 3010: [[3010]], 2809: [[2809]], 3080: [[3080]], 291: [[291]], 3394: [[3394]], 2841: [[2841]], 217: [[217]], 708: [[708]], 68: [[68]], 2621: [[2621]], 682: [[682]], 168: [[168]], 132: [[132]], 102: [[102]], 51: [[51], [83], [237]], 83: [[51], [83], [237]], 237: [[51], [83], [237]], 2505: [[2505]], 811: [[811]], 2431: [[2431]], 3490: [[3490]], 3549: [[3549]], 3568: [[3568]], 694: [[694]], 3723: [[3723]], 2342: [[2342]], 3405: [[3405]], 3066: [[3066]], 3128: [[3128]], 3997: [[3997]], 3053: [[3053]], 2245: [[2245]], 3555: [[3555]], 2126: [[2126]], 1831: [[1831]], 3779: [[3779]], 3925: [[3925]], 3647: [[3647]], 64: [[64], [189]], 189: [[64], [189]], 829: [[829]], 1674: [[1674]], 3499: [[3499]], 32: [[32]], 3231: [[3231]], 2837: [[2837]], 3126: [[3126], [3322]], 3322: [[3126], [3322]], 3981: [[3981]], 3566: [[3566]], 795: [[795]], 2818: [[2818]], 423: [[423]], 3397: [[3397]], 48: [[48]], 1: [[1]], 678: [[678]], 2341: [[2341]], 158: [[158]], 3628: [[3628]], 3725: [[3725], [3743]], 3743: [[3725], [3743]], 815: [[815]], 796: [[796]], 3645: [[3645]], 4021: [[4021]], 1064: [[1064]], 2614: [[2614]], 1531: [[1531]], 1356: [[1356]], 2167: [[2167]], 320: [[320]], 1656: [[1656]], 1910: [[1910]], 3821: [[3821]], 1212: [[1212]], 1858: [[1858]], 579: [[579]], 2107: [[2107]], 3331: [[3331]], 2291: [[2291]], 574: [[574]], 622: [[622]], 774: [[774]], 890: [[890]], 1534: [[1534]], 3295: [[3295]], 2371: [[2371]], 869: [[869]], 2265: [[2265]], 248: [[248]], 1077: [[1077]], 3459: [[3459]], 304: [[304]], 3466: [[3466]], 3221: [[3221]], 2051: [[2051]], 753: [[753]], 767: [[767]], 3764: [[3764]], 543: [[543]], 634: [[634]], 3107: [[3107]], 2781: [[2781]], 3550: [[3550]], 299: [[299]], 1478: [[1478]], 646: [[646]], 2178: [[2178]], 637: [[637]], 3531: [[3531]], 2455: [[2455]], 631: [[631]], 325: [[325]], 347: [[347]], 188: [[188]], 3868: [[3868]], 144: [[144]], 28: [[28]], 618: [[618]], 308: [[308]], 1634: [[1634]], 663: [[663]], 265: [[265]], 22: [[22]], 3956: [[3956]], 3294: [[3294]], 3855: [[3855]], 2114: [[2114]], 2222: [[2222]], 1977: [[1977]], 129: [[129]], 146: [[146]], 2700: [[2700]], 3005: [[3005]], 2812: [[2812]], 3842: [[3842]], 3343: [[3343]], 1090: [[1090]], 1248: [[1248]], 695: [[695]], 80: [[80]], 1781: [[1781]], 1807: [[1807]], 1552: [[1552]], 14: [[14]], 3819: [[3819]], 346: [[346]], 587: [[587]], 2702: [[2702]], 3001: [[3001]], 3957: [[3957]], 3757: [[3757]], 791: [[791]], 2232: [[2232]], 2826: [[2826]], 3002: [[3002]], 2948: [[2948]], 449: [[449]], 3675: [[3675]], 2534: [[2534]], 1405: [[1405]], 3075: [[3075]], 2318: [[2318]], 897: [[897]], 3145: [[3145]], 3614: [[3614]], 1058: [[1058]], 987: [[987]], 1470: [[1470]], 94: [[94]], 101: [[101]], 73: [[73]], 3204: [[3204]], 3573: [[3573]], 1393: [[1393]], 3805: [[3805]], 2296: [[2296]], 3886: [[3886]], 626: [[626]], 2128: [[2128]], 2939: [[2939]], 2898: [[2898]], 2368: [[2368]], 996: [[996]], 344: [[344]], 794: [[794]], 3301: [[3301]], 2673: [[2673]], 3129: [[3129]], 2227: [[2227]], 3195: [[3195]], 3881: [[3881]], 3893: [[3893]], 3388: [[3388]], 1680: [[1680]], 540: [[540]], 1767: [[1767]], 1007: [[1007]], 1203: [[1203]], 2896: [[2896]], 2765: [[2765]], 3113: [[3113]], 1353: [[1353]], 655: [[655]], 1455: [[1455]], 1762: [[1762]], 3197: [[3197]], 4006: [[4006], [4032]], 4032: [[4006], [4032]], 593: [[593]], 1394: [[1394]], 2902: [[2902], [3372]], 3372: [[2902], [3372]], 839: [[839]], 714: [[714]], 393: [[393]], 476: [[476]], 805: [[805]], 1337: [[1337]], 245: [[245]], 2634: [[2634]], 201: [[201]], 3402: [[3402]], 3263: [[3263]], 768: [[768]], 3425: [[3425]], 3446: [[3446]], 804: [[804]], 729: [[729]], 863: [[863], [876]], 876: [[863], [876]], 3338: [[3338], [3427]], 3427: [[3338], [3427]], 3376: [[3376], [3401]], 3401: [[3376], [3401]], 712: [[712]], 3716: [[3716]], 3081: [[3081]], 3061: [[3061]], 2642: [[2642]], 3933: [[3933]], 3083: [[3083]], 3336: [[3336]], 1761: [[1761]], 1696: [[1696]], 1599: [[1599]], 149: [[149]], 1814: [[1814]], 789: [[789]], 3968: [[3968]], 702: [[702]], 3308: [[3308]], 1178: [[1178]], 2688: [[2688]], 3794: [[3794]], 349: [[349]], 3839: [[3839]], 4026: [[4026]], 1806: [[1806]], 3122: [[3122], [3218], [3354]], 3218: [[3122], [3218], [3354]], 3354: [[3122], [3218], [3354]], 3506: [[3506]], 3863: [[3863]], 707: [[707]], 1155: [[1155]], 1616: [[1616]], 877: [[877]], 2983: [[2983]], 705: [[705]], 3979: [[3979]], 878: [[878]], 4019: [[4019]], 3838: [[3838]], 688: [[688]], 3768: [[3768]], 1073: [[1073]], 2997: [[2997]], 3793: [[3793]], 2277: [[2277]], 726: [[726]], 853: [[853]], 1062: [[1062]], 425: [[425]], 980: [[980]], 3722: [[3722]], 3778: [[3778]], 3398: [[3398]], 3266: [[3266]], 2173: [[2173]], 1845: [[1845]], 3547: [[3547]], 496: [[496]], 2289: [[2289]], 831: [[831]], 3829: [[3829]], 719: [[719]], 1307: [[1307]], 827: [[827]], 3559: [[3559]], 1703: [[1703]], 886: [[886]], 2570: [[2570]], 842: [[842]], 1162: [[1162]], 1731: [[1731]], 326: [[326]], 116: [[116]], 1566: [[1566]], 1497: [[1497]], 3545: [[3545]], 1975: [[1975]], 3604: [[3604]], 786: [[786]], 3971: [[3971]], 3833: [[3833]], 3747: [[3747]], 226: [[226]], 703: [[703]], 908: [[908]], 3478: [[3478]], 2375: [[2375]], 333: [[333]], 3967: [[3967]], 1944: [[1944]], 1033: [[1033]], 3926: [[3926]], 507: [[507]], 2242: [[2242]], 2029: [[2029]], 3869: [[3869]], 126: [[126]], 817: [[817]], 847: [[847]], 3035: [[3035]], 3653: [[3653]], 882: [[882]], 2764: [[2764]], 2146: [[2146]], 4018: [[4018]], 2120: [[2120]], 1010: [[1010]], 186: [[186]], 3473: [[3473]], 824: [[824]], 3698: [[3698]], 3482: [[3482]], 3144: [[3144]], 3917: [[3917]], 3214: [[3214]], 3152: [[3152]], 2725: [[2725]], 974: [[974]], 3432: [[3432]], 2806: [[2806]], 2903: [[2903]], 238: [[238]], 3706: [[3706]], 1850: [[1850]], 1901: [[1901]], 2481: [[2481]], 3898: [[3898]], 3011: [[3011]], 3012: [[3012]], 3456: [[3456]], 747: [[747]], 2807: [[2807]], 573: [[573]], 419: [[419]], 2181: [[2181]], 3644: [[3644]], 3345: [[3345]], 303: [[303]], 469: [[469]], 523: [[523]], 206: [[206]], 654: [[654]], 3906: [[3906]], 4037: [[4037]], 3734: [[3734]], 2923: [[2923]], 3947: [[3947]], 3491: [[3491]], 405: [[405]], 2922: [[2922]], 3739: [[3739]], 689: [[689]], 823: [[823]], 973: [[973]], 2286: [[2286]], 3258: [[3258]], 370: [[370]], 810: [[810]], 1685: [[1685]], 1734: [[1734]], 3159: [[3159]], 725: [[725]], 2: [[2]], 2176: [[2176]], 484: [[484]], 778: [[778]], 653: [[653]], 162: [[162]], 2858: [[2858]], 1001: [[1001]], 3714: [[3714]], 837: [[837]], 461: [[461]], 524: [[524]], 711: [[711]], 3673: [[3673]], 3321: [[3321]], 3507: [[3507]], 1706: [[1706]], 1215: [[1215]], 3389: [[3389]], 3424: [[3424]], 3822: [[3822]], 3342: [[3342]], 1718: [[1718]], 3486: [[3486]], 1440: [[1440]], 3299: [[3299]], 2610: [[2610]], 1847: [[1847]], 748: [[748]], 3654: [[3654]], 45: [[45]], 1588: [[1588]], 3038: [[3038]], 3288: [[3288]], 1573: [[1573]], 1235: [[1235]], 932: [[932]], 3692: [[3692]], 3934: [[3934]], 2480: [[2480]], 3915: [[3915]], 3059: [[3059]], 620: [[620]], 1026: [[1026]], 1708: [[1708]], 559: [[559]], 560: [[560]], 3588: [[3588]], 3224: [[3224]], 933: [[933]], 1183: [[1183]], 3784: [[3784]], 1663: [[1663]], 1512: [[1512]], 936: [[936]], 1322: [[1322]], 772: [[772]], 1872: [[1872]], 27: [[27]], 2452: [[2452]], 1862: [[1862]], 1716: [[1716]], 3978: [[3978]], 2952: [[2952]], 1401: [[1401]], 667: [[667]], 841: [[841]], 160: [[160]], 216: [[216]], 3807: [[3807]], 2382: [[2382], [2541]], 2541: [[2382], [2541]], 3496: [[3496]], 2799: [[2799]], 3447: [[3447]], 1043: [[1043]], 455: [[455]], 1687: [[1687]], 1218: [[1218]], 979: [[979]], 742: [[742]], 531: [[531]], 956: [[956]], 1961: [[1961]], 323: [[323]], 522: [[522]], 1726: [[1726]], 1358: [[1358]], 1585: [[1585]], 3087: [[3087]], 724: [[724]], 429: [[429]], 773: [[773]], 1173: [[1173]], 2211: [[2211]], 3515: [[3515]], 1673: [[1673]], 366: [[366]], 2517: [[2517]], 3992: [[3992]], 4033: [[4033]], 1197: [[1197]], 909: [[909]], 1045: [[1045]], 1788: [[1788]], 1016: [[1016], [1403]], 1403: [[1016], [1403]], 3470: [[3470]], 184: [[184]], 127: [[127]], 197: [[197]], 284: [[284]], 281: [[281]], 251: [[251]], 67: [[67]], 816: [[816]], 1494: [[1494]], 2803: [[2803]], 1274: [[1274]], 3020: [[3020]], 861: [[861]], 990: [[990]], 3684: [[3684]], 1562: [[1562]], 104: [[104]], 1328: [[1328]], 331: [[331]], 481: [[481]], 466: [[466]], 529: [[529]], 212: [[212]], 3958: [[3958]], 1144: [[1144]], 1174: [[1174]], 2193: [[2193]], 3790: [[3790]], 793: [[793]], 2335: [[2335]], 2848: [[2848]], 1615: [[1615]], 3895: [[3895]], 257: [[257]], 3069: [[3069]], 1445: [[1445]], 82: [[82]], 2933: [[2933]], 2160: [[2160]], 3585: [[3585]], 3155: [[3155]], 172: [[172]], 1960: [[1960]], 185: [[185]], 3814: [[3814]], 2238: [[2238]], 3017: [[3017]], 62: [[62]], 3377: [[3377]], 163: [[163]], 314: [[314]], 2618: [[2618]], 3325: [[3325]], 2703: [[2703]], 1366: [[1366]], 2644: [[2644]], 2972: [[2972]], 621: [[621]], 3222: [[3222]], 2036: [[2036]], 2566: [[2566]], 2256: [[2256]], 1678: [[1678]], 1543: [[1543]], 1349: [[1349]], 1200: [[1200]], 3063: [[3063]], 2361: [[2361]], 2772: [[2772]], 2957: [[2957]], 549: [[549]], 1825: [[1825]], 3640: [[3640]], 813: [[813]], 2145: [[2145]], 1569: [[1569]], 820: [[820]], 2656: [[2656]], 274: [[274]], 797: [[797]], 787: [[787]], 1168: [[1168]], 3841: [[3841]], 3438: [[3438]], 1705: [[1705]], 2632: [[2632]], 755: [[755]], 758: [[758]], 960: [[960]], 3697: [[3697]], 1330: [[1330]], 649: [[649]], 3699: [[3699]], 1085: [[1085]], 923: [[923]], 3599: [[3599]], 3590: [[3590]], 3710: [[3710]], 1641: [[1641]], 3728: [[3728]], 733: [[733]], 3753: [[3753]], 3164: [[3164]], 691: [[691]], 3283: [[3283]], 3636: [[3636]], 3660: [[3660]], 3953: [[3953]], 159: [[159]], 224: [[224]], 1792: [[1792]], 3754: [[3754]], 1047: [[1047]], 850: [[850]], 3554: [[3554]], 3203: [[3203]], 2391: [[2391]], 2056: [[2056]], 701: [[701]], 951: [[951]], 836: [[836]], 1422: [[1422]], 2661: [[2661]], 2147: [[2147]], 2300: [[2300]], 2350: [[2350]], 1453: [[1453]], 3558: [[3558]], 1915: [[1915]], 141: [[141]], 1424: [[1424]], 3423: [[3423]], 2515: [[2515]], 3770: [[3770]], 3767: [[3767]], 3828: [[3828]], 1976: [[1976]], 1965: [[1965]], 2405: [[2405]], 3951: [[3951]], 2018: [[2018]], 1972: [[1972]], 3882: [[3882]], 2829: [[2829]], 1061: [[1061]], 913: [[913]], 2992: [[2992]], 1234: [[1234]], 3452: [[3452]], 2984: [[2984]], 2662: [[2662]], 311: [[311]], 754: [[754]], 2459: [[2459]], 606: [[606]], 1644: [[1644]], 809: [[809]], 1399: [[1399]], 731: [[731]], 950: [[950]], 2262: [[2262]], 1498: [[1498]], 1346: [[1346]], 1094: [[1094]], 1179: [[1179]], 1122: [[1122]], 3400: [[3400]], 1646: [[1646]], 1331: [[1331]], 3358: [[3358]], 2009: [[2009]], 2297: [[2297]], 1367: [[1367]], 3316: [[3316]], 3217: [[3217]], 2454: [[2454]], 2588: [[2588]], 3416: [[3416]], 1921: [[1921]], 1928: [[1928]], 1631: [[1631]], 1490: [[1490]], 1721: [[1721]], 3983: [[3983]], 859: [[859]], 70: [[70]], 1326: [[1326]], 1111: [[1111]], 3500: [[3500]], 3758: [[3758]], 1325: [[1325]], 152: [[152]], 888: [[888]], 369: [[369]], 389: [[389]], 131: [[131]], 738: [[738]], 26: [[26]], 3529: [[3529]], 86: [[86]], 9: [[9]], 2690: [[2690]], 551: [[551]], 1136: [[1136]], 3468: [[3468]], 3116: [[3116]], 2881: [[2881]], 3329: [[3329]], 3532: [[3532]], 36: [[36]], 3776: [[3776]], 3587: [[3587]], 3960: [[3960]], 3696: [[3696]], 3534: [[3534]], 3605: [[3605]], 2228: [[2228]], 2231: [[2231]], 3124: [[3124]], 3903: [[3903]], 462: [[462]], 1008: [[1008]], 406: [[406]], 499: [[499]], 3369: [[3369]], 2360: [[2360]], 2730: [[2730]], 3902: [[3902]], 568: [[568]], 1640: [[1640]], 457: [[457]], 516: [[516]], 200: [[200]], 2865: [[2865]], 236: [[236]], 2488: [[2488]], 424: [[424]], 486: [[486]], 39: [[39]], 766: [[766]], 3542: [[3542]], 1593: [[1593]], 46: [[46]], 3945: [[3945]], 2650: [[2650]], 2076: [[2076]], 3593: [[3593]], 2325: [[2325]], 2822: [[2822]], 135: [[135], [309]], 309: [[135], [309]], 3361: [[3361]], 3052: [[3052]], 2170: [[2170]], 1992: [[1992]], 2678: [[2678]], 3304: [[3304]], 3475: [[3475]], 3471: [[3471]], 3497: [[3497]], 1474: [[1474]], 2758: [[2758]], 1908: [[1908]], 2577: [[2577]], 2333: [[2333]], 2328: [[2328]], 2694: [[2694]], 2509: [[2509]], 2081: [[2081]], 2304: [[2304]], 2282: [[2282]], 2294: [[2294]], 1384: [[1384]], 3173: [[3173]], 2856: [[2856]], 1548: [[1548]], 3255: [[3255]], 728: [[728]], 3782: [[3782]], 781: [[781]], 357: [[357]], 2901: [[2901]], 3719: [[3719]], 3804: [[3804]], 814: [[814]], 1888: [[1888]], 2100: [[2100]], 2665: [[2665]], 258: [[258]], 2735: [[2735]], 3711: [[3711]], 142: [[142]], 2784: [[2784]], 2667: [[2667]], 555: [[555]], 2868: [[2868]], 463: [[463]], 1980: [[1980]], 1410: [[1410]], 3211: [[3211]], 3291: [[3291]], 3667: [[3667]], 3298: [[3298]], 3528: [[3528]], 3485: [[3485]], 2523: [[2523]], 826: [[826]], 2626: [[2626]], 2061: [[2061]], 2648: [[2648]], 1833: [[1833]], 2716: [[2716]], 2825: [[2825]], 2049: [[2049]], 591: [[591]], 792: [[792]], 3920: [[3920]], 2486: [[2486]], 3655: [[3655]], 2320: [[2320]], 3576: [[3576]], 2832: [[2832]], 3772: [[3772]], 651: [[651]], 3602: [[3602]], 985: [[985]], 586: [[586]], 3524: [[3524]], 3024: [[3024]], 50: [[50]], 30: [[30]], 3724: [[3724]], 834: [[834]], 3964: [[3964]], 3907: [[3907]], 3642: [[3642]], 3150: [[3150]], 687: [[687]], 3196: [[3196]], 2921: [[2921]], 4003: [[4003]], 2707: [[2707]], 3167: [[3167]], 2023: [[2023]], 2989: [[2989]], 3802: [[3802]], 3165: [[3165]], 947: [[947]], 3067: [[3067]], 2718: [[2718]], 3900: [[3900]], 3373: [[3373]], 3273: [[3273]], 2466: [[2466]], 1433: [[1433]], 3242: [[3242]], 3622: [[3622]], 3615: [[3615]], 752: [[752]], 3340: [[3340]], 105: [[105]], 2364: [[2364]], 2709: [[2709]], 3208: [[3208]], 2958: [[2958]], 3762: [[3762]], 528: [[528]], 430: [[430]], 514: [[514]], 3940: [[3940]], 1528: [[1528]], 459: [[459]], 3462: [[3462]], 3786: [[3786]], 928: [[928]], 1675: [[1675]], 3600: [[3600]], 317: [[317]], 2199: [[2199]], 1759: [[1759]], 3859: [[3859]], 1741: [[1741]], 440: [[440]], 1425: [[1425]], 435: [[435]], 2402: [[2402]], 3404: [[3404]], 3032: [[3032]], 3678: [[3678]], 970: [[970]], 444: [[444]], 2637: [[2637]], 2498: [[2498]], 1520: [[1520]], 3707: [[3707]], 3349: [[3349]], 3310: [[3310]], 1126: [[1126]], 2284: [[2284]], 2928: [[2928]], 2225: [[2225]], 1618: [[1618]], 3333: [[3333]], 3627: [[3627]], 497: [[497]], 1523: [[1523]], 1804: [[1804]], 3890: [[3890]], 1589: [[1589]], 3287: [[3287]], 3347: [[3347]], 1637: [[1637]], 1554: [[1554]], 3461: [[3461]], 1886: [[1886]], 1789: [[1789]], 3106: [[3106]], 3494: [[3494]], 2182: [[2182]], 3419: [[3419]], 2597: [[2597]], 1891: [[1891]], 2006: [[2006]], 1950: [[1950]], 1700: [[1700]], 3429: [[3429]], 2177: [[2177]], 379: [[379]], 2587: [[2587]], 2839: [[2839]], 2967: [[2967]], 2754: [[2754]], 1236: [[1236]], 1441: [[1441]], 1779: [[1779]], 1564: [[1564]], 1055: [[1055]], 1343: [[1343]], 2091: [[2091]], 2659: [[2659]], 1266: [[1266]], 1544: [[1544]], 3797: [[3797]], 113: [[113]], 2943: [[2943]], 1822: [[1822]], 3264: [[3264]], 548: [[548]], 211: [[211]], 391: [[391]], 367: [[367]], 2935: [[2935]], 2759: [[2759]], 490: [[490]], 2920: [[2920]], 72: [[72]], 1922: [[1922]], 3213: [[3213]], 3226: [[3226]], 554: [[554]], 2840: [[2840]], 3368: [[3368]], 2129: [[2129]], 3657: [[3657]], 3850: [[3850]], 3472: [[3472]], 3685: [[3685]], 3595: [[3595]], 1050: [[1050]], 1905: [[1905]], 3851: [[3851]], 1225: [[1225]], 509: [[509]], 1476: [[1476]], 3320: [[3320]], 2719: [[2719]], 3441: [[3441]], 1237: [[1237]], 2844: [[2844]], 3060: [[3060]], 3396: [[3396]], 3076: [[3076]], 3484: [[3484]], 418: [[418]], 2260: [[2260]], 2397: [[2397]], 3385: [[3385]], 639: [[639]], 2843: [[2843]], 1709: [[1709]], 3567: [[3567]], 3205: [[3205]], 1431: [[1431]], 3469: [[3469]], 17: [[17]], 3460: [[3460]], 87: [[87]], 2349: [[2349]], 3309: [[3309]], 3382: [[3382]], 3412: [[3412]], 3207: [[3207]], 977: [[977]], 2955: [[2955]], 679: [[679]], 1228: [[1228]], 3510: [[3510]], 3104: [[3104]], 491: [[491]], 2501: [[2501]], 502: [[502]], 446: [[446]], 2251: [[2251]], 3346: [[3346]], 1415: [[1415]], 3328: [[3328]], 108: [[108]], 2497: [[2497]], 2255: [[2255]], 3054: [[3054]], 3362: [[3362]], 3237: [[3237]], 128: [[128]], 2101: [[2101]], 2451: [[2451]], 3501: [[3501]], 2879: [[2879]], 2699: [[2699]], 3086: [[3086]], 505: [[505]], 2751: [[2751]], 1299: [[1299]], 3253: [[3253]], 2877: [[2877]], 1223: [[1223]], 2925: [[2925]], 3143: [[3143]], 3966: [[3966]], 924: [[924]], 2197: [[2197]], 3068: [[3068]], 641: [[641]], 1744: [[1744]], 2085: [[2085]], 3761: [[3761]], 517: [[517]], 3428: [[3428]], 395: [[395]], 2221: [[2221]], 2438: [[2438]], 123: [[123]], 3146: [[3146]], 240: [[240]], 232: [[232]], 1765: [[1765]], 378: [[378]], 2932: [[2932]], 2944: [[2944]], 546: [[546]], 1355: [[1355]], 2706: [[2706]], 3023: [[3023]], 3330: [[3330]], 3286: [[3286]], 1639: [[1639]], 2827: [[2827]], 2399: [[2399]], 2867: [[2867]], 2916: [[2916]], 2960: [[2960]], 2235: [[2235]], 2054: [[2054]], 3356: [[3356]], 2915: [[2915]], 3249: [[3249]], 2790: [[2790]], 2603: [[2603]], 1280: [[1280]], 2072: [[2072]], 3049: [[3049]], 1459: [[1459]], 1893: [[1893]], 1210: [[1210]], 1374: [[1374]], 3199: [[3199]], 1204: [[1204]], 1679: [[1679]], 1628: [[1628]], 723: [[723]], 756: [[756]], 3096: [[3096]], 2940: [[2940]], 1611: [[1611]], 601: [[601]], 3936: [[3936]], 2096: [[2096]], 1475: [[1475]], 3220: [[3220]], 2911: [[2911]], 2750: [[2750]], 3281: [[3281]], 965: [[965]], 3689: [[3689]], 1400: [[1400]], 1292: [[1292]], 3098: [[3098]], 953: [[953]], 2274: [[2274]], 1772: [[1772]], 1286: [[1286]], 2252: [[2252]], 3922: [[3922]], 2857: [[2857]], 3479: [[3479], [3562], [3613], [3649], [3695], [3883]], 3562: [[3479], [3562], [3613], [3649], [3695], [3883]], 3613: [[3479], [3562], [3613], [3649], [3695], [3883]], 3649: [[3479], [3562], [3613], [3649], [3695], [3883]], 3695: [[3479], [3562], [3613], [3649], [3695], [3883]], 3883: [[3479], [3562], [3613], [3649], [3695], [3883]], 3481: [[3481], [3523]], 3523: [[3481], [3523]], 3516: [[3516]], 3341: [[3341]], 272: [[272]], 3383: [[3383]], 2795: [[2795]], 2820: [[2820]], 3275: [[3275]], 849: [[849]], 741: [[741]], 1025: [[1025]], 763: [[763]], 3307: [[3307]], 1844: [[1844]], 1097: [[1097]], 410: [[410]], 3378: [[3378]], 439: [[439]], 1189: [[1189]], 1468: [[1468]], 1526: [[1526]], 2975: [[2975]], 3912: [[3912]], 3874: [[3874]], 2780: [[2780]], 1327: [[1327]], 3892: [[3892]], 1434: [[1434]], 3090: [[3090]], 3522: [[3522]], 835: [[835]], 345: [[345]], 3178: [[3178]], 3360: [[3360]], 3138: [[3138]], 3731: [[3731]], 2715: [[2715]], 3611: [[3611]], 355: [[355]], 3873: [[3873]], 718: [[718]], 3130: [[3130]], 2710: [[2710]], 2739: [[2739]], 589: [[589]], 1217: [[1217]], 3785: [[3785]], 3878: [[3878]], 2787: [[2787]], 1852: [[1852]], 3215: [[3215]], 2105: [[2105]], 1244: [[1244]], 1464: [[1464]], 235: [[235]], 3581: [[3581]], 85: [[85]], 3594: [[3594]], 680: [[680]], 3411: [[3411]], 2697: [[2697]], 664: [[664]], 2950: [[2950]], 3896: [[3896]], 69: [[69]], 2373: [[2373]], 1487: [[1487]], 612: [[612]], 716: [[716]], 685: [[685]], 2954: [[2954]], 583: [[583]], 615: [[615]], 1421: [[1421]], 600: [[600], [643], [661]], 643: [[600], [643], [661]], 661: [[600], [643], [661]], 578: [[578], [627], [658], [659]], 627: [[578], [627], [658], [659]], 658: [[578], [627], [658], [659]], 659: [[578], [627], [658], [659]], 3409: [[3409]], 681: [[681]], 1774: [[1774]], 3185: [[3185]], 3924: [[3924]], 500: [[500]], 374: [[374]], 3810: [[3810]], 547: [[547]], 544: [[544]], 1428: [[1428]], 396: [[396]], 452: [[452]], 3088: [[3088]], 3101: [[3101]], 1051: [[1051]], 465: [[465]], 1167: [[1167]], 3148: [[3148]], 295: [[295]], 3099: [[3099]], 2778: [[2778]], 2965: [[2965]], 1465: [[1465]], 1995: [[1995]], 1436: [[1436]], 474: [[474]], 165: [[165]], 1519: [[1519]], 3755: [[3755]], 1546: [[1546]], 3353: [[3353]], 1882: [[1882]], 3824: [[3824]], 1408: [[1408]], 2783: [[2783]], 647: [[647]], 1818: [[1818]], 3646: [[3646]], 1897: [[1897]], 354: [[354]], 2876: [[2876]], 1409: [[1409]], 3422: [[3422]], 915: [[915]], 403: [[403]], 1713: [[1713]], 541: [[541]], 3811: [[3811]], 1837: [[1837]], 1733: [[1733]], 1895: [[1895]], 1798: [[1798]], 1137: [[1137]], 3514: [[3514]], 1035: [[1035]], 2440: [[2440]], 3260: [[3260]], 415: [[415]], 1787: [[1787]], 1630: [[1630]], 473: [[473]], 1314: [[1314]], 445: [[445]], 1747: [[1747]], 3015: [[3015]], 1118: [[1118]], 1533: [[1533]], 903: [[903]], 901: [[901]], 1629: [[1629]], 1452: [[1452]], 1109: [[1109]], 321: [[321]], 2996: [[2996]], 3730: [[3730]], 662: [[662]], 599: [[599]], 632: [[632]], 845: [[845]], 1017: [[1017]], 704: [[704]], 2894: [[2894]], 3009: [[3009]], 2388: [[2388]], 2004: [[2004]], 3702: [[3702]], 1933: [[1933]], 13: [[13]], 1880: [[1880]], 665: [[665]], 3518: [[3518]], 1823: [[1823]], 485: [[485]], 489: [[489]], 1839: [[1839]], 963: [[963]], 1378: [[1378]], 1056: [[1056]], 2859: [[2859]], 821: [[821]], 221: [[221]], 1080: [[1080]], 1427: [[1427]], 3172: [[3172]], 1385: [[1385]], 1565: [[1565]], 1113: [[1113]], 1142: [[1142]], 1695: [[1695]], 1318: [[1318]], 1294: [[1294]], 1514: [[1514]], 1156: [[1156]], 297: [[297]], 762: [[762]], 1957: [[1957]], 1603: [[1603]], 1042: [[1042]], 759: [[759]], 2159: [[2159]], 3367: [[3367]], 3973: [[3973]], 1790: [[1790]], 1991: [[1991]], 2014: [[2014]], 1291: [[1291]], 1516: [[1516]], 1777: [[1777]], 34: [[34]], 35: [[35]], 2814: [[2814]], 3800: [[3800]], 3541: [[3541]], 2851: [[2851]], 2785: [[2785]], 737: [[737]], 3577: [[3577]], 161: [[161]], 151: [[151]], 204: [[204]], 140: [[140]], 1131: [[1131]], 180: [[180]], 2562: [[2562]], 2769: [[2769]], 2810: [[2810]], 2729: [[2729]], 1334: [[1334]], 1484: [[1484]], 2794: [[2794]], 3413: [[3413]], 1866: [[1866]], 2870: [[2870]], 3857: [[3857]], 1803: [[1803]], 2685: [[2685]], 1301: [[1301]], 1041: [[1041]], 677: [[677]], 2831: [[2831]], 3474: [[3474]], 3312: [[3312]], 2117: [[2117]], 693: [[693]], 2545: [[2545]], 3634: [[3634]], 807: [[807]], 623: [[623]], 1038: [[1038]], 3025: [[3025]], 2741: [[2741]], 3161: [[3161]], 3977: [[3977]], 1420: [[1420]], 2444: [[2444]], 3643: [[3643]], 3840: [[3840]], 1688: [[1688]], 3008: [[3008]], 92: [[92]], 625: [[625]], 2490: [[2490]], 944: [[944]], 3097: [[3097]], 380: [[380]], 3041: [[3041]], 2728: [[2728]], 553: [[553]], 3046: [[3046]], 3048: [[3048]], 2713: [[2713]], 1011: [[1011]], 1306: [[1306]], 458: [[458]], 3241: [[3241]], 2611: [[2611]], 3426: [[3426]], 2035: [[2035]], 1258: [[1258]], 3114: [[3114]], 2742: [[2742]], 3517: [[3517]], 588: [[588]], 3190: [[3190]], 764: [[764]], 3448: [[3448]], 3817: [[3817]], 3007: [[3007]], 1780: [[1780]], 3457: [[3457]], 1169: [[1169]], 1756: [[1756]], 743: [[743]], 2982: [[2982]], 266: [[266]], 194: [[194]], 684: [[684]], 254: [[254]], 3773: [[3773]], 3311: [[3311]], 3540: [[3540]], 187: [[187]], 3100: [[3100]], 2882: [[2882]], 3191: [[3191]], 57: [[57]], 1249: [[1249]], 3261: [[3261]], 3876: [[3876]], 812: [[812]], 1373: [[1373]], 3962: [[3962]], 330: [[330]], 3050: [[3050]], 3089: [[3089]], 840: [[840]], 1246: [[1246]], 3607: [[3607]], 1584: [[1584]], 1698: [[1698]], 2309: [[2309]], 3683: [[3683]], 1449: [[1449]], 3445: [[3445]], 2888: [[2888]], 2526: [[2526]], 765: [[765]], 709: [[709]], 3156: [[3156]], 1480: [[1480]], 276: [[276]], 1461: [[1461]], 3937: [[3937]], 2762: [[2762]], 978: [[978]], 3492: [[3492]], 2966: [[2966]], 3158: [[3158]], 994: [[994]], 3135: [[3135]], 2907: [[2907]], 1006: [[1006]], 2744: [[2744]], 106: [[106]], 1014: [[1014]], 1141: [[1141]], 1481: [[1481]], 2162: [[2162]], 1538: [[1538]], 65: [[65]], 1456: [[1456]], 2981: [[2981]], 16: [[16]], 1101: [[1101]], 1610: [[1610]], 1782: [[1782]], 948: [[948]], 2229: [[2229]], 1985: [[1985]], 1677: [[1677]], 338: [[338]], 2731: [[2731]], 2786: [[2786]], 3166: [[3166]], 1948: [[1948]], 2069: [[2069]], 3079: [[3079]], 3189: [[3189]], 1182: [[1182]], 3058: [[3058]], 2830: [[2830]], 1261: [[1261]], 1284: [[1284]], 1132: [[1132]], 3832: [[3832]], 2924: [[2924]], 2749: [[2749]], 1172: [[1172]], 921: [[921]], 1148: [[1148]], 2103: [[2103]], 1376: [[1376]], 2929: [[2929]], 919: [[919]], 2165: [[2165]], 2073: [[2073]], 316: [[316]], 3589: [[3589]], 3688: [[3688]], 3959: [[3959]], 3639: [[3639], [3919]], 3919: [[3639], [3919]], 3278: [[3278]], 644: [[644]], 609: [[609]], 2696: [[2696]], 1982: [[1982]], 75: [[75]], 788: [[788]], 139: [[139]], 3713: [[3713]], 3601: [[3601]], 1624: [[1624]], 3254: [[3254]], 2941: [[2941]], 1692: [[1692]], 633: [[633]], 1507: [[1507]], 176: [[176]], 3837: [[3837]], 3519: [[3519]], 3465: [[3465], [3579]], 3579: [[3465], [3579]], 3431: [[3431]], 3476: [[3476]], 3708: [[3708]], 2964: [[2964]], 3276: [[3276]], 619: [[619]], 3062: [[3062]], 3223: [[3223]], 2727: [[2727]], 802: [[802]], 3137: [[3137]], 1743: [[1743]], 3835: [[3835]], 3244: [[3244]], 3246: [[3246]], 2387: [[2387]], 2322: [[2322]], 2768: [[2768]], 3051: [[3051]], 1567: [[1567]], 2938: [[2938]], 1904: [[1904]], 2416: [[2416]], 3763: [[3763]], 3363: [[3363]], 1620: [[1620]], 44: [[44]], 2092: [[2092]], 2209: [[2209]], 2067: [[2067]], 3133: [[3133]], 2141: [[2141]], 2080: [[2080]], 2914: [[2914]], 843: [[843]], 1418: [[1418]], 1095: [[1095]], 3866: [[3866]], 3623: [[3623]], 3415: [[3415]], 605: [[605]], 2510: [[2510]], 3406: [[3406]], 3186: [[3186]], 1273: [[1273]], 722: [[722]], 2266: [[2266]], 844: [[844]], 1661: [[1661]], 2878: [[2878]], 2555: [[2555]], 3899: [[3899]], 2543: [[2543]], 3313: [[3313]], 2899: [[2899]], 1926: [[1926]], 525: [[525]], 456: [[456]], 493: [[493]], 538: [[538]], 404: [[404]], 479: [[479]], 2890: [[2890]], 1504: [[1504]], 3403: [[3403]], 1906: [[1906]], 3421: [[3421]], 1683: [[1683]], 2003: [[2003]], 3326: [[3326]], 780: [[780]], 730: [[730]], 1513: [[1513]], 675: [[675]], 650: [[650]], 779: [[779]], 2763: [[2763]], 1719: [[1719]], 3184: [[3184]], 3193: [[3193]], 2761: [[2761]], 2366: [[2366]], 2473: [[2473]], 700: [[700]], 640: [[640]], 2683: [[2683]], 3498: [[3498]], 2629: [[2629]], 3735: [[3735]], 3030: [[3030]], 3317: [[3317]], 1959: [[1959]], 1727: [[1727]], 1128: [[1128]], 2032: [[2032]], 3257: [[3257]], 2148: [[2148]], 3815: [[3815]], 1005: [[1005]], 340: [[340]], 1817: [[1817]], 3234: [[3234]], 760: [[760]], 3160: [[3160]], 3306: [[3306]], 1509: [[1509]], 2919: [[2919]], 2144: [[2144]], 721: [[721]], 1003: [[1003]], 2347: [[2347]], 2567: [[2567]], 2608: [[2608]], 2153: [[2153]], 3480: [[3480]], 1231: [[1231]], 1354: [[1354]], 2995: [[2995]], 1720: [[1720]], 1865: [[1865]], 2071: [[2071]], 223: [[223]], 290: [[290]], 341: [[341]], 1324: [[1324]], 2576: [[2576]], 2506: [[2506]], 2472: [[2472]], 2042: [[2042]], 2736: [[2736]], 2161: [[2161]], 1955: [[1955]], 3575: [[3575]], 2241: [[2241]], 2653: [[2653]], 2465: [[2465]], 2151: [[2151]], 1556: [[1556]], 279: [[279]], 3942: [[3942]], 1065: [[1065]], 3975: [[3975]], 3877: [[3877]], 2426: [[2426]], 1338: [[1338]], 3783: [[3783]], 636: [[636]], 3641: [[3641]], 2513: [[2513]], 1671: [[1671]], 3043: [[3043]], 1990: [[1990]], 3103: [[3103]], 3420: [[3420]], 1829: [[1829]], 3512: [[3512]], 3871: [[3871]], 590: [[590]], 1863: [[1863]], 1846: [[1846]], 3909: [[3909]], 1458: [[1458]], 3795: [[3795]], 242: [[242]], 302: [[302]], 3171: [[3171]], 3285: [[3285]], 1052: [[1052]], 3292: [[3292]], 381: [[381]], 3766: [[3766]], 1511: [[1511]], 2314: [[2314]], 3969: [[3969]], 2116: [[2116]], 603: [[603]], 597: [[597]], 2775: [[2775]], 1275: [[1275]], 2248: [[2248]], 98: [[98]], 438: [[438]], 24: [[24]], 2403: [[2403]], 3335: [[3335]], 3718: [[3718]], 1851: [[1851]], 2008: [[2008]], 3082: [[3082]], 2478: [[2478]], 2424: [[2424]], 1748: [[1748]], 382: [[382]], 1686: [[1686]], 134: [[134]], 3350: [[3350]], 2425: [[2425]], 1577: [[1577]], 575: [[575]], 3656: [[3656]], 2503: [[2503]], 3212: [[3212]], 3493: [[3493]], 2089: [[2089]], 3972: [[3972]], 3093: [[3093]], 409: [[409]], 2155: [[2155]], 3965: [[3965]], 1139: [[1139]], 666: [[666]], 3209: [[3209]], 3620: [[3620]], 526: [[526]], 783: [[783]], 3458: [[3458]], 1312: [[1312]], 3631: [[3631]], 2866: [[2866]], 2854: [[2854]], 2082: [[2082]], 3910: [[3910]], 2494: [[2494]], 471: [[471]], 3715: [[3715]], 1460: [[1460]], 922: [[922]], 2557: [[2557]], 3410: [[3410]], 1496: [[1496]], 1482: [[1482]], 1296: [[1296]], 3557: [[3557]], 3111: [[3111]], 2393: [[2393]], 2525: [[2525]], 1942: [[1942]], 2476: [[2476]], 2234: [[2234]], 660: [[660]], 557: [[557]], 2892: [[2892]], 3777: [[3777]], 1443: [[1443]], 3182: [[3182]], 925: [[925]], 3591: [[3591]], 1344: [[1344]], 2712: [[2712]], 2931: [[2931]], 1112: [[1112]], 3509: [[3509]], 1900: [[1900]], 2119: [[2119]], 3976: [[3976]], 2398: [[2398]], 3179: [[3179]], 537: [[537]], 2937: [[2937]], 2189: [[2189]], 426: [[426]], 1605: [[1605]], 1645: [[1645]], 3351: [[3351]], 1196: [[1196]], 962: [[962]], 1815: [[1815]], 2664: [[2664]], 2171: [[2171]], 2157: [[2157]], 2378: [[2378]], 3056: [[3056]], 2019: [[2019]], 2365: [[2365]], 416: [[416]], 2756: [[2756]], 2797: [[2797]], 420: [[420]], 2708: [[2708]], 3352: [[3352]], 2971: [[2971]], 1074: [[1074]], 3170: [[3170]], 690: [[690]], 2864: [[2864]], 2001: [[2001]], 1570: [[1570]], 2986: [[2986]], 1557: [[1557]], 3943: [[3943]], 451: [[451]], 2910: [[2910]], 1999: [[1999]], 1209: [[1209]], 1059: [[1059]], 2811: [[2811]], 1771: [[1771]], 735: [[735]], 2998: [[2998]], 3375: [[3375]], 3467: [[3467]], 699: [[699]], 3732: [[3732]], 2834: [[2834]], 3151: [[3151]], 289: [[289]], 3488: [[3488]], 3219: [[3219]], 2779: [[2779]], 3296: [[3296]], 1575: [[1575]], 3334: [[3334]], 3796: [[3796]], 3177: [[3177]], 2384: [[2384]], 1978: [[1978]], 2847: [[2847]], 2747: [[2747]], 196: [[196]], 2038: [[2038]], 1949: [[1949]], 3393: [[3393]], 2250: [[2250]], 2355: [[2355]], 2767: [[2767]], 2111: [[2111]], 2529: [[2529]], 2203: [[2203]], 2616: [[2616]], 2389: [[2389]], 2531: [[2531]], 402: [[402]], 3110: [[3110]], 1221: [[1221]], 2247: [[2247]], 1913: [[1913]], 2400: [[2400]], 2102: [[2102]], 931: [[931]], 2084: [[2084]], 3741: [[3741]], 3357: [[3357]], 2819: [[2819]], 3726: [[3726]], 696: [[696]], 1188: [[1188]], 1885: [[1885]], 3198: [[3198]], 2319: [[2319]], 2413: [[2413]], 3520: [[3520]], 2127: [[2127]], 2068: [[2068]], 2336: [[2336]], 2372: [[2372]], 3463: [[3463]], 1170: [[1170]], 3371: [[3371]], 3018: [[3018]], 2057: [[2057]], 1412: [[1412]], 1072: [[1072]], 3658: [[3658]], 2142: [[2142]], 3395: [[3395]], 2058: [[2058]], 2449: [[2449]], 2752: [[2752]], 519: [[519]], 300: [[300]], 1437: [[1437]], 1104: [[1104]], 986: [[986]], 1247: [[1247]], 2900: [[2900]], 1559: [[1559]], 3380: [[3380]], 417: [[417]], 1983: [[1983]], 2044: [[2044]], 1429: [[1429]], 1500: [[1500]], 1745: [[1745]], 1941: [[1941]], 935: [[935]], 967: [[967]], 2138: [[2138]], 1348: [[1348]], 562: [[562]], 2542: [[2542]], 2461: [[2461]], 1966: [[1966]], 1987: [[1987]], 1067: [[1067]], 1303: [[1303]], 3305: [[3305]], 2427: [[2427]], 2631: [[2631]], 2737: [[2737]], 2186: [[2186]], 954: [[954]], 1120: [[1120]], 1391: [[1391]], 1479: [[1479]], 1426: [[1426]], 1021: [[1021]], 3603: [[3603]], 2674: [[2674]], 1195: [[1195]], 191: [[191]], 2191: [[2191]], 1335: [[1335]], 2572: [[2572]], 3235: [[3235]], 2285: [[2285]], 2692: [[2692]], 2052: [[2052]], 138: [[138]], 1342: [[1342]], 1216: [[1216]], 2502: [[2502]], 1159: [[1159]], 2132: [[2132]], 1333: [[1333]], 2516: [[2516]], 2028: [[2028]], 2125: [[2125]], 1916: [[1916]], 838: [[838]], 611: [[611]], 3630: [[3630]], 3236: [[3236]], 3430: [[3430]], 2918: [[2918]], 3563: [[3563]], 3852: [[3852]], 3210: [[3210]], 570: [[570]], 2312: [[2312]], 992: [[992]], 494: [[494]], 558: [[558]], 2434: [[2434]], 1525: [[1525]], 946: [[946]], 398: [[398]], 352: [[352]], 1601: [[1601]], 2292: [[2292]], 2883: [[2883]], 2582: [[2582]], 2871: [[2871]], 535: [[535]], 2723: [[2723]], 2246: [[2246]], 2149: [[2149]], 421: [[421]], 545: [[545]], 1352: [[1352]], 1503: [[1503]], 2223: [[2223]], 2224: [[2224]], 1372: [[1372]], 503: [[503]], 3884: [[3884]], 1828: [[1828]], 2612: [[2612]], 2518: [[2518]], 2062: [[2062]], 1305: [[1305]], 1226: [[1226]], 1232: [[1232]], 1363: [[1363]], 2801: [[2801]], 1633: [[1633]], 3578: [[3578]], 3687: [[3687]], 1541: [[1541]], 3574: [[3574]], 530: [[530]], 2233: [[2233]], 2753: [[2753]], 2649: [[2649]], 2643: [[2643]], 2687: [[2687]], 3175: [[3175]], 958: [[958]], 2875: [[2875]], 1241: [[1241]], 1184: [[1184]], 2158: [[2158]], 2298: [[2298]], 1658: [[1658]], 1551: [[1551]], 1707: [[1707]], 2624: [[2624]], 2110: [[2110]], 2150: [[2150]], 1617: [[1617]], 1632: [[1632]], 1076: [[1076]], 2198: [[2198]], 1060: [[1060]], 1697: [[1697]], 2002: [[2002]], 2605: [[2605]], 1290: [[1290]], 1092: [[1092]], 1263: [[1263]], 1181: [[1181]], 1028: [[1028]], 2544: [[2544]], 2458: [[2458]], 2287: [[2287]], 1532: [[1532]], 448: [[448]], 267: [[267]], 1558: [[1558]], 1561: [[1561]], 808: [[808]], 492: [[492]], 3860: [[3860]], 2757: [[2757]], 3259: [[3259]], 670: [[670]], 2675: [[2675]], 1881: [[1881]], 3609: [[3609]], 482: [[482]], 3858: [[3858]], 628: [[628]], 3319: [[3319]], 3418: [[3418]], 487: [[487]], 515: [[515]], 598: [[598]], 1123: [[1123]], 3289: [[3289]], 394: [[394]], 1310: [[1310]], 2367: [[2367]], 2379: [[2379]], 1272: [[1272]], 1867: [[1867]], 2942: [[2942]], 1251: [[1251]], 3843: [[3843]], 1151: [[1151]], 3834: [[3834]], 1222: [[1222]], 2432: [[2432]], 3065: [[3065]], 761: [[761]], 3117: [[3117]], 1883: [[1883]], 400: [[400]], 1813: [[1813]], 2680: [[2680]], 1130: [[1130]], 2666: [[2666]], 1973: [[1973]], 1998: [[1998]], 2447: [[2447]], 3450: [[3450]], 2645: [[2645]], 2022: [[2022]], 298: [[298]], 3115: [[3115]], 3913: [[3913]], 1819: [[1819]], 1717: [[1717]], 2676: [[2676]], 1124: [[1124]], 3201: [[3201]], 751: [[751]], 1125: [[1125]], 1135: [[1135]], 318: [[318]], 1919: [[1919]], 55: [[55]], 2815: [[2815]], 1377: [[1377]], 2689: [[2689]], 3108: [[3108]], 683: [[683]], 614: [[614]], 2657: [[2657]], 1931: [[1931]], 3381: [[3381]], 1811: [[1811]], 2714: [[2714]], 2024: [[2024]], 3339: [[3339]], 3297: [[3297]], 1491: [[1491]], 1597: [[1597]], 4034: [[4034]], 2802: [[2802]], 2553: [[2553]], 183: [[183]], 1187: [[1187]], 3818: [[3818]], 577: [[577]], 3026: [[3026]], 2976: [[2976]], 3681: [[3681]], 2007: [[2007]], 2332: [[2332]], 3569: [[3569]], 2720: [[2720]], 3417: [[3417]], 2268: [[2268]], 495: [[495]], 2280: [[2280]], 1750: [[1750]], 1339: [[1339]], 2491: [[2491]], 1830: [[1830]], 635: [[635]], 938: [[938]], 2594: [[2594]], 1199: [[1199]], 1613: [[1613]], 2468: [[2468]], 582: [[582]], 2990: [[2990]], 3073: [[3073]], 1467: [[1467]], 2560: [[2560]], 2215: [[2215]], 2530: [[2530]], 512: [[512]], 3552: [[3552]], 2887: [[2887]], 2134: [[2134]], 2279: [[2279]], 3582: [[3582]], 536: [[536]], 3845: [[3845]], 3736: [[3736]], 2584: [[2584]], 2169: [[2169]], 3527: [[3527]], 900: [[900]], 3344: [[3344]], 3109: [[3109]], 2174: [[2174]], 66: [[66]], 2270: [[2270]], 3206: [[3206]], 2512: [[2512]], 2947: [[2947]], 2874: [[2874]], 2743: [[2743]], 3433: [[3433]], 2060: [[2060]], 2988: [[2988]], 2303: [[2303]], 2334: [[2334]], 268: [[268]], 3000: [[3000]], 1034: [[1034]], 1535: [[1535]], 371: [[371]], 2075: [[2075]], 2327: [[2327]], 2305: [[2305]], 250: [[250]], 2589: [[2589]], 2493: [[2493]], 1856: [[1856]], 2522: [[2522]], 1800: [[1800]], 3240: [[3240]], 710: [[710]], 2166: [[2166]], 561: [[561]], 3359: [[3359]], 2913: [[2913]], 3668: [[3668]], 2070: [[2070]], 3277: [[3277]], 1502: [[1502]], 2187: [[2187]], 971: [[971]], 1649: [[1649]], 1724: [[1724]], 1083: [[1083]], 2628: [[2628]], 1260: [[1260]], 1869: [[1869]], 2793: [[2793]], 3118: [[3118]], 914: [[914]], 1930: [[1930]], 1390: [[1390]], 1668: [[1668]], 1350: [[1350]], 1855: [[1855]], 103: [[103]], 1166: [[1166]], 672: [[672]], 1278: [[1278]], 1710: [[1710]], 1619: [[1619]], 1271: [[1271]], 906: [[906]], 2598: [[2598]], 1945: [[1945]], 2533: [[2533]], 2436: [[2436]], 1407: [[1407]], 1746: [[1746]], 1250: [[1250]], 1416: [[1416]], 1375: [[1375]], 880: [[880]], 2963: [[2963]], 1004: [[1004]], 1207: [[1207]], 1752: [[1752]], 1457: [[1457]], 164: [[164]], 3370: [[3370]], 336: [[336]], 916: [[916]], 940: [[940]], 1924: [[1924]], 1488: [[1488]], 1040: [[1040]], 1868: [[1868]], 1809: [[1809]], 1736: [[1736]], 1238: [[1238]], 1256: [[1256]], 1288: [[1288]], 1285: [[1285]], 959: [[959]], 983: [[983]], 1143: [[1143]], 595: [[595]], 2796: [[2796]], 3123: [[3123]], 1255: [[1255]], 1359: [[1359]], 1069: [[1069]], 1269: [[1269]], 1185: [[1185]], 2550: [[2550]], 1140: [[1140]], 2845: [[2845]], 3315: [[3315]], 3414: [[3414]], 2872: [[2872]], 1604: [[1604]], 2288: [[2288]], 1493: [[1493]], 2684: [[2684]], 1648: [[1648]], 1186: [[1186]], 2093: [[2093]], 569: [[569]], 1993: [[1993]], 1757: [[1757]], 1810: [[1810]], 1146: [[1146]], 1302: [[1302]], 972: [[972]], 1063: [[1063]], 1211: [[1211]], 1608: [[1608]], 999: [[999]], 527: [[527]], 1939: [[1939]], 1049: [[1049]], 3436: [[3436]], 2604: [[2604]], 2698: [[2698]], 2390: [[2390]], 2243: [[2243]], 2568: [[2568]], 1191: [[1191]], 997: [[997]], 1510: [[1510]], 1623: [[1623]], 2383: [[2383]], 2991: [[2991]], 1022: [[1022]], 744: [[744]], 930: [[930]], 1766: [[1766]], 1320: [[1320]], 1699: [[1699]], 3434: [[3434]], 629: [[629]], 1784: [[1784]], 1012: [[1012]], 390: [[390]], 576: [[576]], 1625: [[1625]], 1801: [[1801]], 1032: [[1032]], 2130: [[2130]], 2880: [[2880]], 1048: [[1048]], 3142: [[3142]], 3064: [[3064]], 3337: [[3337]], 1729: [[1729]], 1319: [[1319]], 1878: [[1878]], 1836: [[1836]], 2324: [[2324]], 2462: [[2462]], 1563: [[1563]], 1361: [[1361]], 1568: [[1568]], 388: [[388]], 1515: [[1515]], 1370: [[1370]], 2592: [[2592]], 1853: [[1853]], 1802: [[1802]], 1175: [[1175]], 1738: [[1738]], 2040: [[2040]], 3004: [[3004]], 3686: [[3686]], 1805: [[1805]], 511: [[511]], 3039: [[3039]], 3092: [[3092]], 1495: [[1495]], 1230: [[1230]], 1754: [[1754]], 2065: [[2065]], 1602: [[1602]], 1364: [[1364]], 2135: [[2135]], 3379: [[3379]], 2782: [[2782]], 2905: [[2905]], 3348: [[3348]], 2695: [[2695]], 1580: [[1580]], 2338: [[2338]], 993: [[993]], 2053: [[2053]], 2293: [[2293]], 1265: [[1265]], 2196: [[2196]], 2180: [[2180]], 3202: [[3202]], 1116: [[1116]], 1874: [[1874]], 2249: [[2249]], 2704: [[2704], [2740]], 2740: [[2704], [2740]], 1763: [[1763]], 2538: [[2538]], 1951: [[1951]], 375: [[375]], 2640: [[2640]], 1681: [[1681]], 1121: [[1121]], 2272: [[2272]], 1773: [[1773]], 1411: [[1411]], 3323: [[3323]], 1583: [[1583]], 1820: [[1820]], 976: [[976]], 3387: [[3387]], 3033: [[3033]], 957: [[957]], 1462: [[1462]], 2973: [[2973]], 1031: [[1031]], 3149: [[3149]], 2956: [[2956]], 2993: [[2993]], 1282: [[1282]], 2945: [[2945]], 1927: [[1927]], 2647: [[2647]], 2337: [[2337]], 3435: [[3435]], 3022: [[3022]], 2027: [[2027]], 2000: [[2000]], 2755: [[2755]], 3386: [[3386]], 1020: [[1020]], 2026: [[2026]], 1102: [[1102]], 2987: [[2987]], 1606: [[1606]], 1446: [[1446]], 1018: [[1018]], 2620: [[2620]], 2417: [[2417]], 1984: [[1984]], 1940: [[1940]], 2519: [[2519]], 1075: [[1075]], 1958: [[1958]], 2994: [[2994]], 2435: [[2435]], 3788: [[3788]], 1579: [[1579]], 2571: [[2571]], 2635: [[2635]], 2013: [[2013]], 3712: [[3712]], 2088: [[2088]], 2862: [[2862]], 1887: [[1887]], 3192: [[3192]], 1485: [[1485]], 1149: [[1149]], 2429: [[2429]], 2823: [[2823]], 1311: [[1311]], 3332: [[3332]], 949: [[949]], 2733: [[2733]], 2828: [[2828]], 2672: [[2672]], 3262: [[3262]], 2701: [[2701]], 2362: [[2362]], 1843: [[1843]], 3252: [[3252]], 2339: [[2339]], 2048: [[2048]], 1068: [[1068]], 2428: [[2428]], 1300: [[1300]], 2804: [[2804]], 2564: [[2564]], 1313: [[1313]], 2482: [[2482]], 1397: [[1397]], 2340: [[2340]], 2546: [[2546]], 2507: [[2507]], 2646: [[2646]], 2205: [[2205]], 1622: [[1622]], 2175: [[2175]], 3247: [[3247]], 1877: [[1877]], 2112: [[2112]], 2326: [[2326]], 2504: [[2504]], 2216: [[2216]], 2237: [[2237]], 3704: [[3704]], 1430: [[1430]], 1612: [[1612]], 1799: [[1799]], 1735: [[1735]], 1345: [[1345]], 1192: [[1192]], 1871: [[1871]], 1742: [[1742]], 1229: [[1229]], 1129: [[1129]], 1647: [[1647]], 3666: [[3666]], 3572: [[3572]], 1769: [[1769]], 715: [[715]], 1753: [[1753]], 2669: [[2669]], 1009: [[1009]], 1036: [[1036]], 1082: [[1082]], 1714: [[1714]], 966: [[966]], 1454: [[1454]], 942: [[942]], 2410: [[2410]], 1489: [[1489]], 1423: [[1423]], 1100: [[1100]], 1413: [[1413]], 1841: [[1841]], 1015: [[1015]], 1728: [[1728]], 1786: [[1786]], 3239: [[3239]], 2218: [[2218]], 1103: [[1103]], 969: [[969]], 2602: [[2602]], 945: [[945]], 1971: [[1971]], 1576: [[1576]], 1655: [[1655]], 1081: [[1081]], 1257: [[1257]], 60: [[60]], 3889: [[3889]], 1521: [[1521]], 1438: [[1438]], 1163: [[1163]], 1547: [[1547]], 2520: [[2520]], 2121: [[2121]], 648: [[648]], 706: [[706]], 1066: [[1066]], 2873: [[2873]], 2208: [[2208]], 2183: [[2183]], 2580: [[2580]], 2154: [[2154]], 521: [[521]], 2849: [[2849]], 2833: [[2833]], 907: [[907]], 442: [[442]], 854: [[854]], 1152: [[1152]], 3955: [[3955]], 79: [[79]], 2536: [[2536]], 1402: [[1402]], 305: [[305]], 2679: [[2679]], 3085: [[3085]], 1227: [[1227]], 1158: [[1158]], 1857: [[1857]], 2346: [[2346]], 1298: [[1298]], 1636: [[1636]], 1596: [[1596]], 2891: [[2891]], 3284: [[3284]], 1448: [[1448]], 1329: [[1329]], 1864: [[1864]], 3618: [[3618]], 1522: [[1522]], 1600: [[1600]], 1914: [[1914]], 2583: [[2583]], 1341: [[1341]], 3865: [[3865]], 3293: [[3293]], 2906: [[2906]], 2969: [[2969]], 2050: [[2050]], 2192: [[2192]], 3014: [[3014]], 2773: [[2773]], 3384: [[3384]], 1635: [[1635]], 1665: [[1665]], 1107: [[1107]], 1160: [[1160]], 1832: [[1832]], 2705: [[2705]], 2835: [[2835]], 2977: [[2977]], 2850: [[2850]], 1205: [[1205]], 1898: [[1898]], 2219: [[2219]], 3040: [[3040]], 3163: [[3163]], 1842: [[1842]], 1078: [[1078]], 2239: [[2239]], 1147: [[1147]], 1388: [[1388]], 1351: [[1351]], 750: [[750]], 1715: [[1715]], 1315: [[1315]], 989: [[989]], 898: [[898]], 1751: [[1751]], 1243: [[1243]], 2404: [[2404]], 1943: [[1943]], 2344: [[2344]], 1935: [[1935]], 2202: [[2202]], 1947: [[1947]], 3355: [[3355]], 2394: [[2394]], 2064: [[2064]], 2172: [[2172]], 1962: [[1962]], 1019: [[1019]], 1550: [[1550]], 1691: [[1691]], 1279: [[1279]], 1432: [[1432]], 2396: [[2396]], 1968: [[1968]], 981: [[981]], 2415: [[2415]], 3132: [[3132]], 1884: [[1884]], 1595: [[1595]], 2537: [[2537]], 2271: [[2271]], 2615: [[2615]], 1392: [[1392]], 2330: [[2330]], 2363: [[2363]], 2115: [[2115]], 2853: [[2853]], 1099: [[1099]], 1732: [[1732]], 1824: [[1824]], 1396: [[1396]], 488: [[488]], 2278: [[2278]], 1245: [[1245]], 2310: [[2310]], 1892: [[1892]], 1582: [[1582]], 2816: [[2816]], 1609: [[1609]], 2030: [[2030]], 1986: [[1986]], 2912: [[2912]], 671: [[671]], 3169: [[3169]], 2376: [[2376]], 2311: [[2311]], 2343: [[2343]], 2521: [[2521]], 1816: [[1816]], 2118: [[2118]], 2063: [[2063]], 2386: [[2386]], 2143: [[2143]], 1870: [[1870]], 392: [[392]], 2097: [[2097]], 1281: [[1281]], 2011: [[2011]], 1398: [[1398]], 2633: [[2633]], 1954: [[1954]], 2627: [[2627]], 565: [[565]], 2658: [[2658]], 2463: [[2463]], 2508: [[2508]], 2194: [[2194]], 1614: [[1614]], 1662: [[1662]], 2315: [[2315]], 1994: [[1994]], 1740: [[1740]], 2179: [[2179]], 2484: [[2484]], 2407: [[2407]], 1108: [[1108]], 1638: [[1638]], 1219: [[1219]], 2295: [[2295]], 2131: [[2131]], 2184: [[2184]], 2240: [[2240]], 1323: [[1323]], 927: [[927]], 3120: [[3120]], 2206: [[2206]], 3391: [[3391]], 2164: [[2164]], 2395: [[2395]], 2590: [[2590]], 2083: [[2083]], 2409: [[2409]], 2331: [[2331]], 2369: [[2369]], 1979: [[1979]], 1917: [[1917]], 2123: [[2123]], 2630: [[2630]], 2244: [[2244]], 2329: [[2329]], 2276: [[2276]], 2220: [[2220]], 2485: [[2485]], 2139: [[2139]], 2348: [[2348]], 2464: [[2464]], 2574: [[2574]], 2601: [[2601]], 2275: [[2275]], 2563: [[2563]], 3854: [[3854], [3879]], 3879: [[3854], [3879]], 676: [[676]], 1382: [[1382]], 1764: [[1764]], 1903: [[1903]], 1587: [[1587]], 1875: [[1875]], 1044: [[1044]], 2974: [[2974]], 1682: [[1682]], 1451: [[1451]], 2258: [[2258]], 1963: [[1963]], 1084: [[1084]], 1578: [[1578]], 1859: [[1859]], 2639: [[2639]], 3078: [[3078]], 2636: [[2636]], 3238: [[3238]], 3228: [[3228]], 3174: [[3174]], 3029: [[3029]], 2897: [[2897]], 1404: [[1404]], 1309: [[1309]], 2430: [[2430]], 1848: [[1848]], 3112: [[3112]], 2200: [[2200]], 3243: [[3243]], 934: [[934]], 2489: [[2489]], 2380: [[2380]], 2585: [[2585]], 984: [[984]], 1981: [[1981]], 2025: [[2025]], 2660: [[2660]], 1508: [[1508]], 1592: [[1592]], 63: [[63]], 1506: [[1506]], 1952: [[1952]], 1379: [[1379]], 975: [[975]], 3364: [[3364]], 2012: [[2012]], 988: [[988]], 902: [[902]], 1381: [[1381]], 2717: [[2717]], 3134: [[3134]], 3408: [[3408]], 2377: [[2377]], 2681: [[2681]], 2273: [[2273]], 2351: [[2351]], 2163: [[2163]], 2917: [[2917]], 2511: [[2511]], 2652: [[2652]], 2479: [[2479]], 2471: [[2471]], 2746: [[2746]], 1242: [[1242]], 10: [[10]], 1079: [[1079]], 1054: [[1054]], 1190: [[1190]], 2953: [[2953]], 2617: [[2617]], 1572: [[1572]], 2254: [[2254]], 2445: [[2445]], 2039: [[2039]], 2267: [[2267]], 208: [[208]], 1920: [[1920]], 1524: [[1524]], 2561: [[2561]], 1938: [[1938]], 2185: [[2185]], 2264: [[2264]], 2414: [[2414]], 2798: [[2798]], 2392: [[2392]], 2985: [[2985]], 851: [[851]], 1115: [[1115]], 1316: [[1316]], 1873: [[1873]], 1712: [[1712]], 125: [[125]], 2016: [[2016]], 3021: [[3021]], 3070: [[3070]], 2078: [[2078]], 1653: [[1653]], 1340: [[1340]], 1542: [[1542]], 2970: [[2970]], 1902: [[1902]], 1198: [[1198]], 1925: [[1925]], 1180: [[1180]], 2552: [[2552]], 2556: [[2556]], 2201: [[2201]], 2353: [[2353]], 1643: [[1643]], 3399: [[3399]], 1879: [[1879]], 1389: [[1389]], 1812: [[1812]], 1689: [[1689]], 2575: [[2575]], 1907: [[1907]], 3102: [[3102]], 2188: [[2188]], 2600: [[2600]], 1153: [[1153]], 1796: [[1796]], 2475: [[2475]], 2043: [[2043]], 2010: [[2010]], 1395: [[1395]], 1737: [[1737]], 952: [[952]], 1669: [[1669]], 1267: [[1267]], 2210: [[2210]], 1530: [[1530]], 1659: [[1659]], 365: [[365]], 2140: [[2140]], 2137: [[2137]], 571: [[571]], 2607: [[2607]], 2423: [[2423]], 2492: [[2492]], 153: [[153]], 3765: [[3765]], 2855: [[2855]], 1826: [[1826]], 1793: [[1793]], 2257: [[2257]], 2573: [[2573]], 2460: [[2460]], 3597: [[3597]], 2090: [[2090]], 2578: [[2578]], 2136: [[2136]], 1380: [[1380]], 1201: [[1201]], 1039: [[1039]], 2253: [[2253]], 2623: [[2623]], 2655: [[2655]], 1233: [[1233]], 3094: [[3094]], 2770: [[2770]], 288: [[288]], 1362: [[1362]], 3928: [[3928]], 3047: [[3047]], 652: [[652], [673]], 673: [[652], [673]], 1287: [[1287]], 2860: [[2860]], 2722: [[2722]], 2420: [[2420]], 1946: [[1946]], 2354: [[2354]], 2095: [[2095]], 1849: [[1849]], 2547: [[2547]], 1932: [[1932]], 1929: [[1929]], 1775: [[1775]], 1164: [[1164]], 1365: [[1365]], 2005: [[2005]], 2477: [[2477]], 2356: [[2356]], 2559: [[2559]], 2408: [[2408]], 2549: [[2549]], 2124: [[2124]], 1289: [[1289]], 1795: [[1795]], 1414: [[1414]], 2619: [[2619]], 2352: [[2352]], 2532: [[2532]], 2908: [[2908]], 2500: [[2500]], 2625: [[2625]], 2446: [[2446]], 2539: [[2539]], 1997: [[1997]], 3250: [[3250]], 385: [[385]], 1293: [[1293]], 2852: [[2852]], 2496: [[2496]], 2609: [[2609]], 1336: [[1336]], 3125: [[3125]], 1539: [[1539]], 1652: [[1652]], 1517: [[1517]], 1723: [[1723]], 1969: [[1969]], 3984: [[3984], [4008], [4010], [4015], [4022], [4024], [4035]], 4008: [[3984], [4008], [4010], [4015], [4022], [4024], [4035]], 4010: [[3984], [4008], [4010], [4015], [4022], [4024], [4035]], 4015: [[3984], [4008], [4010], [4015], [4022], [4024], [4035]], 4022: [[3984], [4008], [4010], [4015], [4022], [4024], [4035]], 4024: [[3984], [4008], [4010], [4015], [4022], [4024], [4035]], 4035: [[3984], [4008], [4010], [4015], [4022], [4024], [4035]], 234: [[234]], 2599: [[2599]], 3282: [[3282]], 2323: [[2323]], 2033: [[2033]], 1918: [[1918]], 2190: [[2190]], 610: [[610]], 2433: [[2433]], 2591: [[2591]], 1239: [[1239]], 1651: [[1651]], 1821: [[1821]], 875: [[875], [883], [891], [892]], 883: [[875], [883], [891], [892]], 891: [[875], [883], [891], [892]], 892: [[875], [883], [891], [892]], 2104: [[2104]], 2495: [[2495]], 2045: [[2045]], 2370: [[2370]], 2593: [[2593]], 2074: [[2074]], 2418: [[2418]], 860: [[860]], 2213: [[2213]], 2020: [[2020]], 207: [[207]], 2381: [[2381]], 2307: [[2307]], 2077: [[2077]], 1953: [[1953]], 1989: [[1989]], 2059: [[2059]], 2469: [[2469]], 2122: [[2122]], 2638: [[2638]], 2108: [[2108]], 2374: [[2374]], 2467: [[2467]], 2308: [[2308]], 2261: [[2261]], 1755: [[1755]], 2290: [[2290]], 2551: [[2551]], 2586: [[2586]], 2086: [[2086]], 2654: [[2654]], 2524: [[2524]], 1439: [[1439]], 1463: [[1463]], 1417: [[1417]], 1690: [[1690]], 656: [[656]], 2212: [[2212]], 2299: [[2299]], 2606: [[2606]], 2098: [[2098]], 2109: [[2109]], 2306: [[2306]], 2554: [[2554]], 2055: [[2055]], 2613: [[2613]], 2021: [[2021]], 1967: [[1967]], 2579: [[2579]], 2359: [[2359]], 2442: [[2442]], 1176: [[1176]], 2046: [[2046]], 3006: [[3006]], 1276: [[1276]], 585: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 602: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 607: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 608: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 613: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 624: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 638: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 668: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 674: [[585], [602], [607], [608], [613], [624], [638], [668], [674]], 692: [[692], [801]], 801: [[692], [801]], 1262: [[1262]], 358: [[358], [447], [550]], 447: [[358], [447], [550]], 550: [[358], [447], [550]], 11: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 12: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 15: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 18: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 37: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 43: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 74: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 114: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 209: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 210: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 215: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 287: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 292: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 335: [[11], [12], [15], [18], [37], [43], [74], [114], [209], [210], [215], [287], [292], [335]], 3451: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3453: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3570: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3650: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3709: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3729: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3748: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3798: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3820: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3853: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3856: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3935: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 3974: [[3451], [3453], [3570], [3650], [3709], [3729], [3748], [3798], [3820], [3853], [3856], [3935], [3974]], 2079: [[2079], [2195], [2269], [2457], [2470], [2569], [2596]], 2195: [[2079], [2195], [2269], [2457], [2470], [2569], [2596]], 2269: [[2079], [2195], [2269], [2457], [2470], [2569], [2596]], 2457: [[2079], [2195], [2269], [2457], [2470], [2569], [2596]], 2470: [[2079], [2195], [2269], [2457], [2470], [2569], [2596]], 2569: [[2079], [2195], [2269], [2457], [2470], [2569], [2596]], 2596: [[2079], [2195], [2269], [2457], [2470], [2569], [2596]], 2842: [[2842], [3031], [3071], [3183], [3230]], 3031: [[2842], [3031], [3071], [3183], [3230]], 3071: [[2842], [3031], [3071], [3183], [3230]], 3183: [[2842], [3031], [3071], [3183], [3230]], 3230: [[2842], [3031], [3071], [3183], [3230]], 911: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 918: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1096: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1119: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1145: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1206: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1386: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1466: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1560: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1581: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]], 1834: [[911], [918], [1096], [1119], [1145], [1206], [1386], [1466], [1560], [1581], [1834]]}
    jsdata = json.loads(request.get_data().decode('utf-8'))
    listdata = list(jsdata['raw_txt'])
    with open('usrfile.txt', 'w') as f:
        f.write(jsdata['file'])
    autotree.DviCL('./usrfile.txt')
    full_autotree = autotree.readfile_at()
    #ssm_all_dict = ssm.ssm_generator('usrfile.txt',[])
    #print(len(ssm_all_dict))
    im_all_dict = {0: [107, 3437, 0, 686, 348, 1684, 1912, 3980, 698, 21, 916, 688, 1085, 2661, 3442, 360, 25, 2664, 3506, 2665, 1918, 355, 3448, 23, 1960, 577, 2690, 924, 3443, 573, 1914, 3473, 2670, 3500, 9, 3982, 3468, 705, 901, 2669, 24, 353, 2724, 3455, 908, 17, 897, 3465, 3479, 3446, 2663, 857, 917, 2668, 4, 1923, 1988, 707, 3438, 896, 921, 7, 2667, 2672, 2933, 14, 1936, 687, 369, 13, 1917, 990, 2712, 1, 2679, 3460, 944, 2799, 198, 3488, 3499, 3439, 354, 2696, 8, 3478, 689, 2700, 932, 576, 579, 956, 694, 1919, 2715, 3458, 363, 961, 3490, 955], 1: [2, 3, 16, 26, 29, 30, 31, 32, 34, 38, 39, 40, 41, 44, 48, 51, 53, 65, 67, 73, 75, 76, 77, 79, 83, 84, 85, 86, 87, 89, 90, 97, 99, 103, 111, 112, 114, 115, 117, 119, 122, 129, 130, 134, 136, 140, 141, 142, 143, 144, 148, 153, 155, 160, 161, 162, 166, 169, 170, 176, 185, 186, 187, 188, 190, 194, 195, 199, 200, 201, 212, 218, 221, 225, 232, 234, 235, 245, 246, 252, 256, 257, 260, 264, 266, 270, 271, 273, 277, 279, 280, 281, 283, 284, 291, 292, 298, 299, 306, 307, 310, 314, 315, 318, 320, 322, 326, 329, 331, 332, 334, 335, 339, 342, 343, 344, 345, 347, 357, 358, 359, 361, 366, 373, 375, 376, 378, 380, 383, 390, 391, 394, 395, 397, 398, 402, 403, 409, 410, 412, 414, 415, 422, 430, 431, 432, 433, 434, 442, 444, 446, 449, 451, 452, 457, 458, 461, 463, 465, 469, 475, 477, 481, 482, 483, 484, 491, 492, 493, 496, 497, 500, 507, 508, 510, 511, 513, 515, 516, 517, 519, 524, 526, 528, 531, 536, 537, 538, 542, 543, 545, 548, 550, 552, 553, 558, 560, 565, 567, 568, 570, 574, 580, 588, 589, 591, 595, 596, 597, 598, 606, 620, 627, 629, 632, 633, 637, 640, 641, 650, 651, 653, 661, 666, 697, 699, 703, 712, 713, 714, 715, 717, 718, 721, 725, 726, 737, 738, 740, 741, 742, 747, 748, 749, 754, 761, 763, 764, 768, 772, 774, 776, 779, 780, 784, 785, 788, 789, 792, 797, 798, 801, 802, 803, 807, 809, 810, 814, 815, 816, 821, 822, 824, 827, 828, 829, 830, 831, 835, 836, 840, 842, 843, 844, 845, 846, 847, 851, 852, 853, 856, 860, 861, 867, 868, 870, 874, 880, 883, 895, 898, 903, 913, 923, 927, 930, 933, 934, 941, 943, 947, 948, 949, 953, 954, 966, 967, 969, 972, 974, 975, 976, 977, 979, 980, 982, 985, 988, 989, 992, 993, 995, 1000, 1002, 1011, 1014, 1017, 1018, 1020, 1024, 1025, 1028, 1032, 1033, 1035, 1037, 1041, 1044, 1045, 1049, 1066, 1067, 1072, 1076, 1078, 1079, 1081, 1086, 1097, 1099, 1102, 1107, 1113, 1114, 1120, 1122, 1125, 1127, 1133, 1135, 1137, 1144, 1152, 1156, 1164, 1165, 1172, 1176, 1181, 1187, 1188, 1190, 1191, 1192, 1194, 1195, 1206, 1212, 1214, 1219, 1220, 1222, 1225, 1227, 1229, 1230, 1231, 1235, 1236, 1237, 1238, 1242, 1243, 1246, 1249, 1255, 1256, 1258, 1260, 1261, 1262, 1265, 1271, 1274, 1277, 1284, 1288, 1289, 1293, 1294, 1298, 1303, 1306, 1309, 1310, 1312, 1317, 1318, 1319, 1320, 1322, 1323, 1329, 1333, 1337, 1338, 1346, 1347, 1354, 1368, 1370, 1371, 1373, 1376, 1381, 1383, 1386, 1388, 1389, 1390, 1393, 1395, 1396, 1398, 1399, 1400, 1402, 1405, 1409, 1412, 1413, 1417, 1418, 1420, 1423, 1426, 1427, 1433, 1435, 1436, 1439, 1448, 1453, 1456, 1460, 1461, 1465, 1468, 1472, 1474, 1477, 1479, 1480, 1482, 1483, 1487, 1490, 1497, 1500, 1502, 1503, 1505, 1507, 1508, 1509, 1511, 1514, 1516, 1517, 1524, 1525, 1529, 1534, 1535, 1536, 1543, 1549, 1554, 1556, 1559, 1562, 1563, 1570, 1574, 1577, 1578, 1581, 1584, 1585, 1588, 1589, 1590, 1591, 1596, 1600, 1601, 1602, 1606, 1607, 1610, 1612, 1613, 1621, 1623, 1628, 1629, 1630, 1632, 1636, 1637, 1639, 1642, 1644, 1645, 1650, 1655, 1656, 1659, 1663, 1665, 1668, 1673, 1678, 1680, 1681, 1687, 1688, 1689, 1699, 1700, 1707, 1710, 1712, 1718, 1720, 1721, 1726, 1732, 1734, 1736, 1738, 1739, 1747, 1750, 1751, 1756, 1758, 1762, 1768, 1770, 1773, 1777, 1778, 1779, 1780, 1782, 1784, 1785, 1786, 1791, 1794, 1799, 1802, 1804, 1805, 1806, 1807, 1809, 1812, 1822, 1823, 1824, 1825, 1827, 1828, 1830, 1832, 1836, 1839, 1842, 1845, 1848, 1849, 1853, 1857, 1858, 1859, 1860, 1863, 1865, 1868, 1876, 1878, 1880, 1882, 1883, 1884, 1885, 1888, 1889, 1891, 1892, 1893, 1904, 1906, 1921, 1924, 1925, 1926, 1929, 1932, 1935, 1940, 1941, 1944, 1946, 1948, 1953, 1958, 1962, 1972, 1973, 1975, 1977, 1979, 1983, 1984, 1985, 1989, 1990, 1992, 1993, 1996, 1997, 2001, 2002, 2006, 2007, 2009, 2011, 2012, 2013, 2018, 2020, 2022, 2023, 2024, 2025, 2026, 2030, 2031, 2032, 2034, 2047, 2049, 2051, 2053, 2054, 2056, 2059, 2061, 2069, 2073, 2076, 2078, 2080, 2084, 2086, 2088, 2090, 2095, 2096, 2097, 2098, 2104, 2107, 2113, 2119, 2122, 2124, 2130, 2135, 2138, 2143, 2146, 2154, 2158, 2163, 2166, 2169, 2170, 2179, 2184, 2185, 2190, 2192, 2200, 2201, 2202, 2203, 2205, 2210, 2211, 2214, 2216, 2219, 2222, 2228, 2231, 2232, 2236, 2240, 2242, 2243, 2248, 2249, 2251, 2257, 2258, 2260, 2261, 2262, 2265, 2266, 2267, 2268, 2270, 2271, 2272, 2273, 2274, 2275, 2277, 2278, 2281, 2286, 2290, 2297, 2299, 2303, 2314, 2317, 2324, 2325, 2326, 2327, 2328, 2329, 2331, 2338, 2339, 2340, 2349, 2352, 2354, 2356, 2361, 2363, 2371, 2377, 2380, 2382, 2391, 2395, 2399, 2401, 2403, 2404, 2406, 2407, 2409, 2412, 2416, 2417, 2418, 2420, 2423, 2424, 2427, 2429, 2432, 2433, 2434, 2438, 2444, 2450, 2453, 2461, 2462, 2463, 2470, 2472, 2475, 2477, 2478, 2479, 2482, 2483, 2484, 2485, 2486, 2492, 2495, 2499, 2501, 2504, 2506, 2510, 2511, 2519, 2523, 2530, 2537, 2540, 2546, 2550, 2557, 2559, 2560, 2561, 2563, 2568, 2573, 2576, 2578, 2582, 2583, 2584, 2585, 2594, 2595, 2598, 2600, 2602, 2604, 2613, 2615, 2621, 2622, 2623, 2624, 2625, 2626, 2633, 2636, 2640, 2644, 2646, 2647, 2653, 2654, 2659, 2662, 2673, 2674, 2675, 2676, 2678, 2680, 2683, 2684, 2688, 2689, 2692, 2697, 2698, 2703, 2705, 2708, 2709, 2710, 2713, 2716, 2722, 2729, 2730, 2732, 2735, 2744, 2748, 2750, 2757, 2758, 2762, 2767, 2772, 2773, 2777, 2778, 2780, 2782, 2783, 2787, 2789, 2790, 2791, 2795, 2796, 2797, 2800, 2803, 2809, 2813, 2822, 2823, 2830, 2832, 2833, 2835, 2839, 2840, 2844, 2849, 2853, 2855, 2857, 2860, 2861, 2862, 2863, 2865, 2866, 2870, 2874, 2881, 2883, 2888, 2890, 2892, 2894, 2896, 2904, 2906, 2908, 2909, 2910, 2915, 2916, 2920, 2926, 2929, 2931, 2934, 2939, 2940, 2942, 2944, 2946, 2947, 2949, 2950, 2951, 2955, 2956, 2959, 2960, 2961, 2963, 2964, 2969, 2972, 2974, 2978, 2980, 2983, 2986, 2990, 2997, 3000, 3002, 3007, 3009, 3010, 3014, 3015, 3018, 3020, 3022, 3027, 3029, 3031, 3033, 3035, 3037, 3038, 3040, 3048, 3049, 3058, 3063, 3068, 3069, 3073, 3074, 3075, 3076, 3077, 3078, 3085, 3087, 3088, 3093, 3094, 3095, 3100, 3101, 3111, 3113, 3114, 3118, 3119, 3120, 3121, 3129, 3133, 3137, 3138, 3140, 3142, 3146, 3150, 3151, 3156, 3157, 3158, 3163, 3164, 3170, 3171, 3173, 3174, 3176, 3178, 3179, 3183, 3184, 3186, 3188, 3194, 3196, 3198, 3200, 3202, 3205, 3207, 3208, 3209, 3211, 3212, 3218, 3223, 3224, 3227, 3233, 3235, 3242, 3243, 3244, 3253, 3254, 3255, 3256, 3259, 3262, 3264, 3266, 3274, 3276, 3278, 3280, 3281, 3288, 3289, 3291, 3295, 3299, 3301, 3314, 3318, 3321, 3328, 3331, 3332, 3334, 3335, 3337, 3339, 3340, 3341, 3345, 3346, 3348, 3351, 3355, 3356, 3357, 3359, 3360, 3364, 3370, 3372, 3374, 3381, 3384, 3386, 3388, 3392, 3393, 3395, 3396, 3397, 3400, 3405, 3408, 3410, 3411, 3412, 3414, 3415, 3417, 3420, 3424, 3426, 3427, 3432, 3454, 3456, 3462, 3466, 3471, 3481, 3482, 3486, 3491, 3498, 3501, 3508, 3509, 3514, 3516, 3518, 3519, 3523, 3524, 3525, 3527, 3529, 3534, 3542, 3544, 3545, 3547, 3549, 3550, 3553, 3554, 3555, 3561, 3562, 3563, 3569, 3573, 3577, 3578, 3580, 3587, 3590, 3591, 3592, 3593, 3595, 3596, 3599, 3601, 3603, 3604, 3605, 3608, 3609, 3611, 3613, 3624, 3627, 3629, 3631, 3633, 3634, 3635, 3636, 3639, 3641, 3649, 3650, 3653, 3659, 3661, 3662, 3663, 3665, 3669, 3675, 3678, 3680, 3685, 3687, 3694, 3698, 3700, 3708, 3710, 3713, 3716, 3719, 3720, 3722, 3730, 3731, 3732, 3733, 3737, 3747, 3750, 3762, 3763, 3764, 3768, 3770, 3773, 3774, 3777, 3782, 3787, 3791, 3793, 3794, 3797, 3799, 3800, 3802, 3807, 3815, 3817, 3820, 3822, 3824, 3829, 3830, 3833, 3834, 3835, 3837, 3838, 3839, 3845, 3847, 3850, 3851, 3852, 3855, 3859, 3865, 3868, 3869, 3871, 3872, 3874, 3875, 3880, 3881, 3885, 3886, 3891, 3892, 3895, 3897, 3898, 3899, 3900, 3901, 3903, 3909, 3913, 3917, 3919, 3922, 3926, 3927, 3929, 3930, 3931, 3935, 3937, 3938, 3941, 3943, 3947, 3948, 3950, 3951, 3953, 3954, 3955, 3956, 3959, 3961, 3964, 3965, 3966, 3968, 3969, 3971, 3977, 3987, 3988, 3990, 3994, 4001, 4014, 4019, 4021, 4026, 4030], 2: [5, 6, 10, 20, 22, 28, 45, 56, 58, 60, 62, 63, 66, 72, 80, 82, 88, 91, 92, 93, 94, 96, 98, 104, 105, 106, 108, 109, 110, 113, 118, 120, 121, 123, 125, 127, 128, 131, 132, 135, 137, 146, 156, 158, 165, 171, 172, 175, 177, 178, 181, 182, 184, 191, 196, 197, 202, 203, 204, 208, 211, 213, 214, 223, 224, 227, 228, 229, 230, 231, 236, 237, 238, 239, 242, 243, 247, 248, 249, 254, 258, 261, 262, 263, 265, 272, 274, 276, 278, 285, 290, 294, 297, 300, 303, 304, 308, 312, 313, 323, 324, 325, 328, 330, 333, 338, 341, 350, 352, 362, 367, 368, 370, 371, 372, 374, 385, 387, 388, 389, 392, 396, 400, 404, 405, 408, 413, 416, 417, 418, 419, 420, 421, 423, 424, 425, 426, 427, 428, 436, 438, 439, 440, 445, 450, 455, 456, 459, 460, 462, 466, 471, 473, 478, 479, 486, 487, 488, 489, 490, 494, 495, 502, 503, 504, 505, 506, 509, 512, 514, 518, 520, 521, 522, 523, 525, 527, 529, 530, 533, 534, 539, 541, 544, 546, 547, 554, 555, 556, 557, 559, 561, 563, 566, 569, 582, 583, 584, 590, 592, 593, 599, 600, 601, 604, 605, 609, 610, 614, 615, 617, 618, 619, 621, 623, 625, 628, 630, 631, 634, 635, 636, 643, 644, 645, 646, 647, 652, 654, 657, 660, 662, 663, 664, 665, 669, 670, 673, 674, 675, 678, 679, 680, 681, 683, 684, 685, 690, 693, 695, 696, 701, 702, 706, 708, 709, 711, 716, 719, 720, 722, 723, 724, 727, 728, 730, 731, 733, 734, 735, 736, 739, 745, 751, 752, 755, 756, 758, 760, 762, 765, 766, 767, 770, 773, 777, 778, 781, 782, 783, 786, 787, 793, 795, 800, 804, 805, 813, 818, 819, 820, 823, 826, 834, 838, 839, 841, 848, 849, 850, 862, 863, 864, 869, 873, 879, 881, 885, 889, 893, 899, 900, 902, 905, 906, 907, 909, 912, 914, 915, 919, 920, 922, 925, 931, 936, 938, 940, 942, 945, 946, 951, 952, 957, 958, 959, 960, 962, 963, 964, 965, 968, 970, 971, 973, 978, 983, 984, 986, 987, 991, 994, 996, 997, 999, 1001, 1003, 1004, 1006, 1008, 1009, 1010, 1012, 1013, 1015, 1019, 1021, 1026, 1029, 1030, 1036, 1039, 1040, 1042, 1047, 1048, 1051, 1052, 1053, 1054, 1056, 1059, 1060, 1062, 1064, 1068, 1070, 1074, 1075, 1077, 1080, 1082, 1083, 1084, 1089, 1092, 1095, 1098, 1100, 1101, 1104, 1106, 1108, 1109, 1110, 1112, 1115, 1116, 1117, 1118, 1121, 1123, 1124, 1126, 1128, 1129, 1130, 1131, 1132, 1134, 1136, 1138, 1139, 1142, 1143, 1146, 1148, 1149, 1150, 1153, 1155, 1157, 1158, 1159, 1160, 1161, 1163, 1166, 1167, 1169, 1173, 1174, 1175, 1178, 1179, 1180, 1182, 1183, 1184, 1185, 1186, 1189, 1193, 1196, 1198, 1199, 1201, 1203, 1204, 1205, 1207, 1209, 1210, 1211, 1213, 1215, 1216, 1217, 1218, 1221, 1223, 1226, 1232, 1234, 1239, 1241, 1245, 1247, 1250, 1257, 1259, 1266, 1267, 1269, 1272, 1273, 1275, 1276, 1278, 1279, 1280, 1281, 1282, 1283, 1285, 1286, 1287, 1290, 1291, 1292, 1296, 1297, 1299, 1300, 1302, 1304, 1305, 1307, 1308, 1311, 1313, 1314, 1315, 1316, 1321, 1324, 1327, 1328, 1330, 1331, 1332, 1334, 1335, 1336, 1339, 1340, 1341, 1342, 1344, 1345, 1348, 1349, 1350, 1351, 1352, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1363, 1365, 1366, 1367, 1369, 1374, 1375, 1377, 1379, 1380, 1382, 1385, 1387, 1391, 1392, 1397, 1401, 1404, 1406, 1407, 1408, 1410, 1411, 1414, 1415, 1416, 1419, 1421, 1422, 1425, 1428, 1429, 1431, 1432, 1434, 1437, 1438, 1440, 1441, 1442, 1444, 1445, 1446, 1447, 1449, 1450, 1451, 1452, 1454, 1455, 1457, 1458, 1459, 1462, 1464, 1467, 1469, 1470, 1471, 1473, 1475, 1478, 1481, 1484, 1485, 1488, 1489, 1491, 1495, 1496, 1498, 1501, 1504, 1506, 1510, 1512, 1513, 1515, 1519, 1520, 1522, 1523, 1526, 1528, 1530, 1531, 1532, 1537, 1538, 1539, 1540, 1541, 1542, 1544, 1547, 1550, 1551, 1553, 1557, 1558, 1561, 1564, 1565, 1566, 1567, 1568, 1569, 1571, 1572, 1573, 1575, 1576, 1580, 1582, 1583, 1587, 1592, 1593, 1595, 1597, 1598, 1603, 1604, 1605, 1608, 1609, 1611, 1614, 1616, 1617, 1618, 1619, 1620, 1622, 1624, 1625, 1626, 1631, 1633, 1634, 1635, 1638, 1640, 1641, 1643, 1647, 1649, 1651, 1652, 1653, 1658, 1660, 1661, 1662, 1664, 1666, 1667, 1669, 1670, 1671, 1674, 1675, 1676, 1677, 1682, 1683, 1685, 1686, 1691, 1692, 1694, 1695, 1697, 1698, 1701, 1702, 1703, 1704, 1705, 1706, 1708, 1709, 1714, 1715, 1716, 1717, 1722, 1723, 1724, 1725, 1727, 1728, 1729, 1730, 1735, 1737, 1741, 1742, 1743, 1744, 1745, 1746, 1749, 1752, 1753, 1754, 1757, 1761, 1763, 1764, 1765, 1766, 1767, 1769, 1771, 1772, 1774, 1781, 1783, 1787, 1789, 1790, 1793, 1795, 1796, 1798, 1800, 1801, 1803, 1808, 1810, 1811, 1813, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1826, 1831, 1833, 1835, 1837, 1838, 1840, 1841, 1843, 1844, 1846, 1847, 1850, 1851, 1852, 1861, 1862, 1864, 1866, 1867, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1877, 1879, 1881, 1886, 1894, 1895, 1897, 1898, 1899, 1901, 1902, 1903, 1907, 1909, 1910, 1911, 1913, 1915, 1916, 1920, 1927, 1928, 1930, 1931, 1934, 1937, 1938, 1939, 1942, 1943, 1945, 1947, 1951, 1954, 1955, 1956, 1957, 1959, 1961, 1963, 1964, 1965, 1966, 1968, 1970, 1971, 1976, 1980, 1981, 1982, 1986, 1991, 1994, 1995, 1998, 1999, 2000, 2003, 2004, 2005, 2010, 2016, 2021, 2028, 2029, 2033, 2035, 2036, 2037, 2038, 2039, 2040, 2042, 2043, 2044, 2045, 2046, 2050, 2052, 2055, 2057, 2058, 2060, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2070, 2071, 2072, 2074, 2075, 2077, 2081, 2082, 2083, 2085, 2087, 2091, 2092, 2093, 2100, 2101, 2102, 2103, 2108, 2109, 2110, 2111, 2112, 2114, 2115, 2116, 2117, 2118, 2120, 2121, 2123, 2125, 2126, 2127, 2128, 2131, 2132, 2133, 2134, 2136, 2137, 2139, 2140, 2141, 2142, 2144, 2145, 2147, 2148, 2149, 2150, 2151, 2152, 2153, 2155, 2157, 2159, 2160, 2161, 2164, 2165, 2167, 2171, 2172, 2173, 2174, 2176, 2180, 2181, 2183, 2186, 2187, 2188, 2189, 2191, 2193, 2194, 2196, 2197, 2198, 2199, 2206, 2207, 2208, 2209, 2212, 2213, 2215, 2218, 2220, 2221, 2223, 2224, 2225, 2226, 2227, 2229, 2233, 2234, 2235, 2237, 2239, 2241, 2244, 2246, 2247, 2250, 2253, 2254, 2256, 2259, 2264, 2276, 2279, 2282, 2283, 2284, 2285, 2287, 2288, 2289, 2291, 2292, 2293, 2294, 2295, 2296, 2298, 2300, 2302, 2304, 2306, 2307, 2308, 2309, 2310, 2311, 2313, 2315, 2318, 2319, 2320, 2321, 2322, 2323, 2332, 2333, 2334, 2335, 2336, 2337, 2341, 2342, 2343, 2344, 2345, 2346, 2347, 2348, 2350, 2351, 2353, 2355, 2359, 2360, 2364, 2365, 2366, 2367, 2368, 2369, 2370, 2372, 2374, 2376, 2378, 2381, 2383, 2384, 2385, 2386, 2387, 2390, 2392, 2393, 2394, 2396, 2397, 2398, 2402, 2405, 2408, 2410, 2411, 2413, 2414, 2415, 2419, 2421, 2425, 2426, 2428, 2430, 2435, 2436, 2437, 2439, 2440, 2443, 2445, 2446, 2447, 2448, 2449, 2451, 2452, 2454, 2455, 2458, 2459, 2460, 2464, 2465, 2467, 2468, 2469, 2471, 2473, 2474, 2476, 2480, 2487, 2488, 2489, 2490, 2491, 2494, 2497, 2498, 2500, 2502, 2503, 2507, 2508, 2509, 2512, 2516, 2518, 2520, 2521, 2522, 2525, 2526, 2527, 2529, 2531, 2532, 2533, 2534, 2536, 2538, 2539, 2542, 2543, 2544, 2545, 2547, 2549, 2551, 2552, 2553, 2554, 2555, 2556, 2558, 2562, 2564, 2566, 2567, 2571, 2574, 2575, 2577, 2579, 2586, 2588, 2589, 2590, 2591, 2592, 2593, 2597, 2601, 2603, 2605, 2606, 2607, 2608, 2609, 2610, 2611, 2612, 2614, 2616, 2617, 2618, 2619, 2620, 2627, 2628, 2629, 2630, 2631, 2634, 2635, 2637, 2638, 2639, 2642, 2643, 2645, 2648, 2649, 2650, 2651, 2652, 2655, 2656, 2657, 2658, 2660, 2666, 2681, 2682, 2686, 2687, 2693, 2694, 2699, 2701, 2702, 2706, 2707, 2711, 2717, 2718, 2719, 2720, 2723, 2725, 2726, 2727, 2728, 2731, 2734, 2737, 2738, 2739, 2741, 2742, 2743, 2745, 2746, 2747, 2749, 2751, 2753, 2754, 2755, 2759, 2761, 2763, 2764, 2765, 2766, 2768, 2769, 2770, 2779, 2781, 2785, 2786, 2792, 2793, 2794, 2802, 2805, 2806, 2807, 2810, 2811, 2815, 2818, 2819, 2820, 2825, 2826, 2827, 2828, 2829, 2831, 2836, 2837, 2841, 2843, 2845, 2846, 2848, 2850, 2851, 2854, 2856, 2858, 2864, 2867, 2868, 2869, 2871, 2872, 2873, 2875, 2876, 2877, 2878, 2879, 2880, 2887, 2889, 2891, 2895, 2900, 2901, 2905, 2907, 2911, 2912, 2913, 2914, 2917, 2918, 2919, 2921, 2924, 2925, 2927, 2928, 2932, 2935, 2936, 2937, 2938, 2943, 2945, 2953, 2957, 2958, 2962, 2966, 2967, 2968, 2970, 2973, 2975, 2976, 2977, 2979, 2981, 2982, 2984, 2985, 2987, 2988, 2989, 2991, 2992, 2993, 2994, 2996, 2999, 3001, 3004, 3005, 3011, 3013, 3016, 3017, 3019, 3021, 3023, 3024, 3025, 3026, 3032, 3034, 3036, 3039, 3041, 3042, 3043, 3046, 3047, 3050, 3051, 3052, 3054, 3056, 3057, 3060, 3062, 3064, 3065, 3070, 3072, 3079, 3080, 3081, 3082, 3083, 3084, 3086, 3089, 3090, 3092, 3096, 3097, 3098, 3102, 3103, 3104, 3105, 3106, 3107, 3108, 3109, 3110, 3115, 3116, 3117, 3122, 3123, 3124, 3126, 3128, 3130, 3132, 3135, 3136, 3139, 3141, 3144, 3145, 3148, 3149, 3152, 3153, 3154, 3155, 3159, 3160, 3162, 3165, 3166, 3168, 3169, 3172, 3177, 3180, 3181, 3182, 3185, 3187, 3189, 3190, 3191, 3192, 3193, 3195, 3197, 3199, 3201, 3203, 3204, 3206, 3213, 3214, 3215, 3216, 3219, 3220, 3221, 3222, 3225, 3226, 3228, 3231, 3232, 3237, 3238, 3239, 3240, 3241, 3246, 3247, 3248, 3250, 3252, 3257, 3258, 3260, 3261, 3263, 3265, 3267, 3272, 3273, 3275, 3277, 3283, 3284, 3285, 3286, 3287, 3292, 3293, 3294, 3296, 3297, 3298, 3302, 3303, 3304, 3306, 3307, 3308, 3309, 3312, 3313, 3316, 3317, 3319, 3320, 3323, 3324, 3325, 3327, 3330, 3333, 3338, 3342, 3343, 3344, 3347, 3349, 3350, 3352, 3353, 3354, 3358, 3361, 3362, 3363, 3365, 3366, 3367, 3368, 3369, 3371, 3373, 3377, 3378, 3379, 3382, 3385, 3387, 3390, 3391, 3394, 3398, 3399, 3402, 3403, 3404, 3406, 3416, 3418, 3419, 3421, 3422, 3423, 3425, 3428, 3430, 3431, 3433, 3434, 3435, 3436, 3440, 3447, 3449, 3450, 3452, 3457, 3459, 3461, 3463, 3464, 3469, 3474, 3475, 3476, 3480, 3484, 3485, 3489, 3493, 3495, 3496, 3497, 3503, 3505, 3507, 3511, 3512, 3515, 3517, 3521, 3522, 3526, 3528, 3532, 3535, 3539, 3540, 3546, 3548, 3551, 3556, 3557, 3559, 3567, 3568, 3571, 3574, 3576, 3584, 3586, 3598, 3602, 3606, 3612, 3614, 3615, 3617, 3618, 3620, 3622, 3625, 3628, 3632, 3640, 3642, 3645, 3648, 3651, 3654, 3655, 3656, 3658, 3666, 3667, 3668, 3670, 3672, 3674, 3676, 3677, 3681, 3682, 3684, 3686, 3690, 3692, 3693, 3695, 3696, 3697, 3702, 3705, 3706, 3707, 3711, 3714, 3715, 3718, 3721, 3723, 3728, 3734, 3735, 3736, 3738, 3739, 3740, 3741, 3743, 3749, 3752, 3753, 3756, 3757, 3758, 3759, 3760, 3761, 3765, 3766, 3767, 3769, 3771, 3772, 3775, 3776, 3778, 3779, 3783, 3784, 3785, 3786, 3789, 3790, 3792, 3796, 3801, 3803, 3804, 3809, 3810, 3812, 3813, 3818, 3821, 3823, 3825, 3826, 3827, 3828, 3831, 3832, 3841, 3842, 3844, 3858, 3860, 3861, 3862, 3867, 3870, 3873, 3876, 3877, 3884, 3888, 3889, 3896, 3902, 3905, 3906, 3908, 3915, 3918, 3920, 3921, 3923, 3924, 3932, 3936, 3940, 3945, 3957, 3958, 3960, 3962, 3967, 3970, 3972, 3973, 3976, 3979, 3993, 3995, 4000, 4003, 4029, 4037], 3: [2048, 19, 2089, 46, 2094, 2099, 57, 2105, 59, 2106, 2129, 101, 2156, 2162, 116, 2175, 2177, 2182, 2204, 159, 167, 2217, 180, 2238, 2252, 206, 2255, 2263, 217, 219, 220, 222, 2280, 2301, 2312, 268, 275, 2330, 296, 302, 309, 2357, 2362, 317, 2373, 2379, 337, 2388, 2389, 346, 349, 2400, 365, 381, 407, 2466, 429, 435, 2493, 2496, 464, 2513, 2515, 2517, 470, 2535, 2570, 2572, 2581, 535, 2587, 549, 551, 2599, 575, 578, 2632, 587, 2641, 603, 611, 612, 616, 622, 2671, 626, 2677, 2685, 2695, 658, 659, 2714, 676, 677, 682, 2733, 2752, 2756, 710, 2760, 2771, 2775, 2776, 729, 732, 2784, 746, 2798, 753, 2804, 2812, 2816, 771, 2821, 2834, 794, 2847, 2852, 811, 2859, 825, 832, 833, 2882, 2897, 2898, 2923, 876, 877, 878, 2930, 884, 886, 888, 890, 2948, 904, 2954, 910, 2965, 926, 929, 937, 939, 2995, 2998, 3003, 3008, 3012, 3028, 981, 3030, 1005, 3053, 1007, 1016, 3066, 1023, 1038, 3099, 1055, 1061, 1063, 3112, 1069, 1073, 1087, 1088, 1090, 1091, 1093, 1094, 3143, 3161, 3167, 3175, 1140, 1141, 1151, 3210, 1170, 1171, 1177, 3229, 3234, 3236, 1197, 3245, 3249, 3251, 3269, 3270, 1228, 3279, 1240, 3290, 1244, 1248, 3300, 3310, 1263, 3315, 1268, 3329, 1325, 3380, 3383, 1343, 3409, 1364, 1372, 1378, 3445, 3470, 1424, 3472, 3477, 1443, 3492, 3504, 1463, 3520, 1476, 3530, 3531, 3533, 3536, 1492, 1493, 1494, 3541, 3552, 3558, 3564, 1518, 1521, 3575, 1527, 3579, 3581, 1533, 3588, 1545, 3594, 1548, 1552, 3600, 3610, 3616, 3621, 3623, 1579, 3630, 3638, 1594, 3643, 3646, 1599, 3657, 1615, 3679, 3683, 1646, 1648, 3701, 1654, 3703, 1657, 3712, 1672, 3724, 3725, 3726, 1696, 3754, 1713, 1719, 3780, 1733, 1740, 1748, 3805, 1759, 1760, 3816, 1775, 1788, 3836, 1792, 3843, 1814, 3866, 1829, 3878, 3890, 3893, 3894, 1856, 3907, 3911, 3912, 3933, 3934, 1887, 3939, 1896, 3944, 1900, 1908, 1922, 3975, 1933, 3985, 1950, 1952, 1967, 4017, 1978, 1987, 2008, 2014, 2017, 2019, 2027, 2041], 4: [384, 1154, 3848, 3727, 3857, 1043, 1555, 1301, 150, 790, 152, 2838, 154, 3483, 3863, 3992, 928, 3883, 3375, 3131, 3647, 64, 3271, 1353, 586, 3660, 78, 3664, 3538, 1499, 3583, 1776, 3441, 3952, 1905, 250, 639], 5: [3585, 3745, 163, 3949, 3513, 189]}
    packed_data = {0:full_autotree, 1:tempssm_Facebook, 2:im_all_dict}
   
    return json.dumps(packed_data)
@app.route('/uploadorig', methods = ['POST'])
def get_post_javascript_data_orig():
    jsdata = json.loads(request.get_data().decode('utf-8'))
    #listdata = list(jsdata['raw_txt'])
    with open('usrfile.txt', 'w') as f:
        f.write(jsdata['file'])
    autotree.DviCL('./usrfile.txt')
    full_autotree = autotree.readfile_at()
    ssm_all_dict = ssm.ssm_generator('usrfile.txt',[])
    im_all_dict = ssm.get_IM()
    
    #print(len(ssm_all_dict))
    packed_data = {0:full_autotree, 1:ssm_all_dict, 2:im_all_dict}
    return json.dumps(packed_data)


if __name__ == "__main__":
    app.run(port=8050, debug=True)