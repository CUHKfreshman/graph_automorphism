import dash_cytoscape as cyto
from dash import html, Dash, ctx, Dash
import networkx as nx
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_defer_js_import as dji
import autotree

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
                                                            html.Div(id='sigma-container', className='h-100 w-100'),
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
