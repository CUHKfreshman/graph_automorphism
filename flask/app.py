#import dash_cytoscape as cyto
#from dash import html, Dash, ctx, Dash
#import networkx as nx
#import pandas as pd
#from dash.dependencies import Input, Output, State
#import dash_bootstrap_components as dbc
#import dash_defer_js_import as dji
#import autotree
from math import ceil
from flask import Flask, render_template, request, make_response, jsonify
from flask_cors import CORS, cross_origin
#from flask_sse import sse
from flask.json import JSONEncoder
from time import sleep
#import concurrent.futures
import json
from queue import Queue
import numpy as np
import ssm
import autotree
import pmc
import subsim
import game
import ssa
import ssmForIP #NOTE: TODO: This should be temporary !IMPORTANT
# Note that 'app.json_encoder' is deprecated and will be removed in Flask 2.3
# I dont have time for updates, so I will just use this for now
# Note that app.py can only be triggered from the root path, i.e., "python3 ./flask/app.py", otherwise file path will raise error
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        return super(CustomJSONEncoder, self).default(obj)

app = Flask(__name__, template_folder='templates', static_folder="static", static_url_path='/static')
app.json_encoder = CustomJSONEncoder
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
#app.config["REDIS_URL"] = "redis://localhost"
#app.register_blueprint(sse, url_prefix='/stream')
ssm_all_dict= {}
data_queue = Queue()


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    # Do something
    jsdata = json.loads(request.get_data().decode('utf-8'))
    #listdata = list(jsdata['raw_txt'])
    with open('./flask/usrfile.txt', 'w') as f:
        f.write(str(jsdata))

    autotree.DviCL('./flask/usrfile.txt')
    full_autotree = autotree.readfile_at()
    data = {'type': 'AutoTreeData', 'data': full_autotree}

    data_queue.put(data)
    #send_IMData()
    # Run the other functions concurrently
    '''
    with concurrent.futures.ThreadPoolExecutor() as executor:
        #future1 = executor.submit(send_AutoTreeData)
        future2 = executor.submit(send_SSMData_real)
        future3 = executor.submit(send_IMData)
    '''   
    # Python future 3.12+ (Not yet published) is required for GIL unlock to really concurrent. Thus we use a stable version for demo
    #send_IMData()
    #send_SSMData() 
    print('Concurrent Programmes Returned Successfully.')
    # Get the results of the futures (optional)
    #result1 = future1.result()
    #result2 = future2.result()
    #result3 = future3.result()
    #print(result1, result2, result3)
    #sse.publish("Close",type="close")
    # Return a response
    return jsonify({"status": "success"})


def send_SSMData():
    data = ssm.ssm_generator('./flask/usrfile.txt',[])
    data_queue.put({'type':'SSMData','data':data})
    print(len(data))

def send_IMData():
    #with app.app_context():
        #sse.publish(json.dumps({'data': 'response 3CCCA'}), type='IMData')
    pruned = [107,3437,0,686,348,1684,1912,3980,698,21]
    #pruned = [0]
    prob = 20
    im_all_dict = ssm.get_IM(pruned, prob / 100)
    data = {'type': 'IMData', 'data': im_all_dict}
    data_queue.put(data)
    print(len(im_all_dict))

@app.route('/customizedIM', methods=['POST'])
@cross_origin()
def customizedIM():
    jsdata = json.loads(request.get_data().decode('utf-8'))
    seed_set = [int(i) for i in jsdata['nodes']]
    spread_model = jsdata['spreadModel']
    if spread_model == 'IC':
        
        im_all_dict = ssm.get_IM(seed_set, float(jsdata['spreadProbability']) / 100)
        data = {'type': 'customizedIMData', 'data': im_all_dict}
        data_queue.put(data)
    else:
        im_all_dict = ssmForIP.get_IM_LT(seed_set, int(jsdata['timeLimit']))
        print(im_all_dict)
        data = {'type': 'customizedIMData', 'data': im_all_dict}
        data_queue.put(data)
    return jsonify({"status": "success"})
#default + diy dialog
#dataset //
#coefficient,deg/accumulate by round/stat diff
#comparison++ sigmod, pvldb, icde, kdd 3~4 typical state-of-the-art
#expectation diff/spread trend/orientation diff(by diff nodes stats)
#survey
@app.route('/pmc', methods=['POST'])
@cross_origin()
def getPMC():
    jsdata = json.loads(request.get_data().decode('utf-8'))
    isDIYParameters = jsdata['isDIYParameters'] #bool
    if isDIYParameters:
        diyParameters = jsdata['diyParameters']
        pmc_output = pmc.run_pmc_raw(diyParameters)
        return jsonify(data=pmc_output)
    seedsize = int(jsdata['size'])
    decay = int(jsdata['decay'])
    prob = float(jsdata['spreadProbability']) / 100
    pmc_output = [str(i) for i in pmc.get_pmc_result(seedsize, decay, prob)]
    return jsonify(data=pmc_output)

@app.route('/subsim', methods=['POST'])
@cross_origin()
def getSubsim():
    jsdata = json.loads(request.get_data().decode('utf-8'))
    seedsize, pdist, isDIYParameters, diyParameters, wcvariant, pedge, skew, eps, delta, vanilla, hist = jsdata.values()
    subsim_output = subsim.get_subsim_result(seedsize, pdist, wcvariant, pedge, skew, eps, delta, vanilla, hist)
    return jsonify(data=subsim_output)

@app.route('/game', methods=['POST'])
@cross_origin()
def getGame():
    jsdata = json.loads(request.get_data().decode('utf-8'))
    seedsize = jsdata['size']
    game_output = game.get_game_result(seedsize)
    return jsonify(data=game_output)


@app.route('/ssa', methods=['POST'])
@cross_origin()
def getSSA():
    jsdata = json.loads(request.get_data().decode('utf-8'))
    seedsize = jsdata['size']
    epsilon = jsdata['epsilon']
    delta = jsdata['delta']
    model = jsdata['model']
    isDSSA = (jsdata['isDSSA'] == 'DSSA')
    ssa_output = ssa.get_ssa_result(seedsize, epsilon, delta, model, isDSSA)
    return jsonify(data=ssa_output)
#get_SSA_result(seedsize, epsilon, delta, model, isDSSA)
@app.route('/ip', methods=['POST'])
@cross_origin()
def getIP():
    jsdata = json.loads(request.get_data().decode('utf-8'))
    seed_set = [int(i) for i in jsdata['nodes']]
    result = ssmForIP.ssm_generator('./flask/usrfile.txt', seed_set)
    print("ip:",result)
    return jsonify(data=[str(i) for i in result])
@app.route('/poll', methods=['GET'])
@cross_origin()
def poll():
    while True:
        if not data_queue.empty():
            data = data_queue.get()
            print("sent", data['type'])
            return jsonify(data)

        else:
            sleep(5)
            return jsonify({'type': 'noData'})
            
@app.route('/metrics', methods=['POST'])
@cross_origin()
def getMetrics():
    jsdata = json.loads(request.get_data().decode('utf-8'))
    seed_set = [int(i) for i in jsdata['nodes']]
    prob = float(jsdata['spreadProbability']) / 100
    #currently only cascade
    result = ssmForIP.cs_generator('./flask/usrfile.txt', seed_set, prob)
    
    print('metrics:',result)
    return jsonify(data=result)
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4000, debug=True)
