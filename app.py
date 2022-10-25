import dash_cytoscape as cyto
from dash import html
from dash import Dash
import networkx as nx
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_defer_js_import as dji
import autotree

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

def get_autotree_elements(vertex_list):
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

cyto_stylesheet = [
    # {'selector': '.TP', 'style': {'color':'red',"background-color": "red", }},
    # {'selector': '.FP', 'style': {'color':'lightblue', "background-color": "blue" }},
    # {'selector': '.center', 'style': {'color':'green', "background-color": "green" }},
    # {'selector': '.Real-Node', 'style': {'shape': 'circle'} },
    # {'selector': '.Fake-Node', 'style': {'shape': 'triangle'} },
    {'selector': 'node', 'style': {'width':'data(width)', 'height':'data(height)','font-size': '8px','label':None } },#'data(label)'
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

def init_autotree_graph():
    #element_nodes, element_edges = get_autotree_elements(vertex_list)
    new_cyg = cyto.Cytoscape(
        id='cy-component-autotree',
        layout={'name': 'cose'}, # spread cose
        style={'width': '100%', 'height': '100%', 'background':'#FFF'},
        stylesheet=cyto_stylesheet,
        elements=[{'data': {'id': '0', 'label': '0', 'width': '0px', 'height': '0px'}, 'classes': 'node'}],#init a false node in order to avoid error
        minZoom=1e-2,
        maxZoom=1e3,
        
    )
    return new_cyg

autotree.DviCL('input3.txt')# generate autotree
full_autotree = autotree.readfile_at()#read at.txt
app = Dash(__name__, assets_ignore='./custom-script.js',external_stylesheets=[dbc.themes.PULSE])
server = app.server
cyto_graph, FULL_GRAPH = get_cyto_graph('./input3.txt')
autotree_graph = init_autotree_graph()
autotree_offcanvas = html.Div(
    [
        dbc.Offcanvas(
            
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
                                                            cyto_graph,
                                                            
                                                            #dji.Import(src="./custom-script.js")
                                                        ],
                                                        id='cyto_div', class_name='border-3 p-0', style={"height":"95vh"},
                                                    ),
                                                ],width=8, class_name='p-2'),
                                                dbc.Col([
                                                    dbc.Row([
                                                        dbc.Row([
                                                            dbc.Card
                                                            (
                                                                [
                                                                    html.Div([html.P('Corresponding AutoTree',className='m-0 d-inline align-bottom'),
                                                                              html.P('>>>', className='m-0 d-inline float-end text-secondary', id='autotree-entry',n_clicks=0)], className='card-header'),
                                                                    autotree_graph,
                                                                ],
                                                                id='auto_tree',class_name='p-0 border-2', style={'height':'40vh','overflow':'hidden'}
                                                            )
                                                        ]),
                                                        dbc.Row([
                                                            dbc.Tabs([
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
                                                                                html.Tr([html.Td("Node ID",className='w-25'),html.Td(id='cytoscape-tapNodeData-output')]),
                                                                                
                                                                                html.Tr([html.Td("Autotree Size",className='w-25'),html.Td(id='size-output')]),
                                                                                
                                                                                html.Tr([html.Td("Vertices",className='w-25'),html.Td(id='vertex-output')]),
                                                                                
                                                                                html.Tr([html.Td("Labels",className='w-25'),html.Td(id='label-output')]),
                                                                                
                                                                                html.Tr([html.Td("Children Size",className='w-25'),html.Td(id='childrensize-output')]),
                                                                                
                                                                                html.Tr([html.Td("Children",className='w-25'),html.Td(id='children-output')]),
                                                                                
                                                                                html.Tr([html.Td("Parent",className='w-25'),html.Td(id='parent-output')]),
                                                                                
                                                                                html.Tr([html.Td("Signature",className='w-25'),html.Td(id='sig-output')]),
                                                                                
                                                                                html.Tr([html.Td("Depth",className='w-25'),html.Td(id='depth-output')]),
                                                                            ]),
                                                                            hover=True,bordered=True,striped=True,style={'width':'100.5%', 'margin-left':'-0.25%','margin-top':'-0.25%'}
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

@app.callback(Output('cy-component', 'stylesheet'),
              Input('cy-component', 'tapNodeData'))
def update_stylesheet(NodeData):
    new_styles=[]
    if NodeData is not None:
        print(NodeData)
        new_styles =    [
            {
                'selector': f'#{NodeData["id"]}',
                'style': {
                    'background-color': 'red'
                }
            }]

    return cyto_stylesheet + new_styles


#@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
#              Input('cy-component', 'tapNodeData'))
#def display_TapNodeData(data):
#    if data:
#        return str(data['id'])


# update autotree TODO: now we only get the largest tree
@app.callback([ Output('cy-component-autotree', 'elements'),
                Output('cytoscape-tapNodeData-output', 'children'),
                Output('size-output','children'),
                Output('vertex-output','children'),
                Output('label-output','children'),
                Output('childrensize-output','children'),
                Output('children-output','children'),
                Output('parent-output','children'),
                Output('sig-output','children'),
                Output('depth-output','children')],
                [Input('cy-component', 'tapNodeData'),
                State('cy-component-autotree', 'elements'),
                State('cytoscape-tapNodeData-output', 'children'),
                State('size-output','children'),
                State('vertex-output','children'),
                State('label-output','children'),
                State('childrensize-output','children'),
                State('children-output','children'),
                State('parent-output','children'),
                State('sig-output','children'),
                State('depth-output','children')])
def update_autotree(data, elements, id, size, vertex, label, children_size, children, parent, sig, depth):
    if data:
        selected_id = str(data['id'])
        corr_trees = autotree.find_autotrees(full_autotree, selected_id) # all autotrees which have the selected node
        if len(corr_trees) != 0:#if has autotree
            # now we only deal with the first one(largest)
            largest_tree = corr_trees[1]#TODO: More functionalities in autotree analyzer
            element_nodes, element_edges = get_autotree_elements(largest_tree['vertex_list'])
            #print(element_nodes + element_edges)
            print(largest_tree)
            return  element_nodes + element_edges, str(data['id']), largest_tree['size'], str(largest_tree['vertex_list']), str(largest_tree['label']), largest_tree['children_size'], str(largest_tree['children']), largest_tree['parent'], largest_tree['sig'], largest_tree['depth']
    return elements, id, size, vertex, label, children_size, children, parent, sig, depth


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
   
if __name__ == '__main__':
    app.run_server(debug=True)
