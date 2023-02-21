//TODO: need to disable autotree sigma graph if new file inputted or change to SSM panel
//TODO: bugs
//TODO: Non-passive event listener
//TODO: avoid to extract subgraph with a prerequisite of opening autotree
//TODO: bug when clicking full graph.
// DO NOT ACCEPT AN EXTRA EMPTY LINE AT THE END
var file = document.getElementById("readfile");
var ssm_all_dict;
var im_all_dict;
var all_node_degree_dict = {};
var ssm_degree_dict = {};
var full_autotree;
var colormap;
var orig_fullgraph = new graphology.Graph();
var extracted_subgraph = new graphology.Graph();
var autotree_fullgraph = new graphology.Graph();
var autotree_subgraph = new graphology.Graph();
var autotree_subgraph_parent = new graphology.Graph();
var autotree_subgraph_child = new graphology.Graph();
var orig_fullgraph_sigma;
var autotree_fullgraph_sigma;
var autotree_subgraph_sigma;
var autotree_subgraph_parent_sigma;
var autotree_subgraph_child_sigma;
var nodenum = 0;
var non_singular_pairs = 0;
var randomseed = Math.floor(Math.random() * 10) + 1;
var total_cell = 0;
var non_leaf_cell = 0;
// nodes collapsing
const thresholdZoom = 0.5;
const thresholdDistance = 10;
var originalNodes = [];
//im
var saved_graph;
file.addEventListener("change", function () {
    var reader = new FileReader();
    reader.onload = function (progressEvent) {
        file = this.result;
        raw_txt = this.result.split(/\s|\n/);
        nodenum = parseInt(raw_txt[0]);
        document.getElementById('nodenum').innerText = raw_txt[0];
        randomseed += nodenum;//avoid dup ref; Now donot work
        document.getElementById('edgenum').innerText = raw_txt[1];
        const ssm_entry_old = document.getElementById('ssm-entry');
        ssm_entry_old.innerHTML = `
        <div class="w-75 h-25 border position-absolute top-50 start-50 translate-middle">
            <button class="btn btn-outline-primary position-absolute top-50 start-50 translate-middle" type="button"  id="ssm-start-btn" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Analyzing...
            </button>
        </div>
        `;
        const autotree_entry = document.getElementById('autotree-entry');
        autotree_entry.innerHTML = `
        <div class="w-75 h-25 border position-absolute top-50 start-50 translate-middle">
        <button class="btn btn-outline-primary position-absolute top-50 start-50 translate-middle" type="button"   id="autotree-start-btn"  data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling" disabled>
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        Analyzing...
        </button>
        </div>`;
        const im_entry = document.getElementById('im-entry');
        im_entry.innerHTML = `
        <div class="w-75 h-25 border position-absolute top-50 start-50 translate-middle">
        <button class="btn btn-outline-primary position-absolute top-50 start-50 translate-middle" type="button"   id="autotree-start-btn"  data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling" disabled>
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        Analyzing...
        </button>
        </div>`;
        render_orig_fullgraph(raw_txt);
        axios.post('/upload', { file, raw_txt })
            .then(function (response) {
                ssm_entry_old.innerHTML = `
                <div class="w-75 h-25 border position-absolute top-50 start-50 translate-middle">
                    <button type='button' class="btn btn-outline-primary position-absolute top-50 start-50 translate-middle" id="ssm-start-btn">View Analysis</button>
                </div>
                `;
                autotree_entry.innerHTML = `
                <div class="w-75 h-25 border position-absolute top-50 start-50 translate-middle">
                <button type='button' class="btn btn-outline-primary position-absolute top-50 start-50 translate-middle" id="autotree-start-btn"  data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">AutoTree Entry</button>
            </div>`;
                im_entry.innerHTML = `
                <div class="w-75 h-25 border position-absolute top-50 start-50 translate-middle">
                <button type='button' class="btn btn-outline-primary position-absolute top-50 start-50 translate-middle" id="im-start-btn">View Analysis</button>
            </div>`;
                let packed_data = response.data;
                console.log(packed_data);
                full_autotree = packed_data[0];

                ssm_all_dict = packed_data[1];
                im_all_dict = packed_data[2];
                autotree_entry_listen();
                ssm_entry_listen();
                im_entry_listen();
            })
            .catch(function (error) {
                console.log(error);
            });
    };
    reader.readAsText(this.files[0]);
});
var orig_fullgraph_layout;
var autotree_fullgraph_layout;
function render_orig_fullgraph(raw_txt) {
    const container = document.getElementById("orig-fullgraph-container");
    orig_fullgraph = new graphology.Graph();
    container.innerHTML = '';
    for (let i = 0; i < raw_txt[0]; i++) {
        orig_fullgraph.addNode(i.toString(), { x: Math.random() * 10, y: Math.random() * 10, size: 2, label: i.toString(), color: "silver" });
    }
    for (let i = 2; i < raw_txt.length; i += 2) {
        orig_fullgraph.addEdge(raw_txt[i], raw_txt[i + 1]);
    }

    const density = graphologyLibrary.metrics.graph.undirectedDensity(orig_fullgraph);
    document.getElementById('density').innerText = density.toString().substring(0, 8);
    all_node_degree_dict = {};
    let all_deg = 0;
    let max_deg = 0;
    orig_fullgraph.forEachNode((node) => {
        let deg = orig_fullgraph.degree(node);
        if (deg > max_deg) {
            max_deg = deg;
        }
        all_deg += deg;
        if (deg in all_node_degree_dict) {
            all_node_degree_dict[deg] = all_node_degree_dict[deg] + 1;
        }
        else {
            all_node_degree_dict[deg] = 1;
        }
        orig_fullgraph.mergeNodeAttributes(node, {
            size: Math.min(deg * 1.5, 5),
            color: '#' + (deg * 1919810).toString(16),
            z: 0
        });
    });
    document.getElementById('max-deg').innerText = max_deg.toString();
    document.getElementById('avg-deg').innerText = (all_deg / nodenum).toString().substring(0, 8);
    graphologyLibrary.metrics.centrality.degree.assign(orig_fullgraph);
    graphologyLibrary.metrics.centrality.pagerank.assign(orig_fullgraph);
    ssm_degree_dict = {};
    render_degree_distribution();
    // eslint-disable-next-line @typescript-eslint/no-unused-vars

    let hoveredEdge = null;
    if (typeof orig_fullgraph_sigma != 'undefined') {
        orig_fullgraph_sigma.kill();
    }
    orig_fullgraph_sigma = new Sigma(orig_fullgraph, container, {

        defaultEdgeColor: "#e6e6e6",
        enableEdgeClickEvents: true,
        enableEdgeWheelEvents: true,
        enableEdgeHoverEvents: "debounce",
        zIndex: true
    });
    const sensibleSettings = graphologyLibrary.layoutForceAtlas2.inferSettings(orig_fullgraph);
    //graphologyLibrary.layoutForceAtlas2(orig_fullgraph, {iterations: 100, convergenceThreshold: 0.1});
    orig_fullgraph_layout = new graphologyLibrary.FA2Layout(orig_fullgraph, {
        settings: sensibleSettings,
    });
    orig_fullgraph_layout.start();
    orig_fullgraph_sigma.on("clickNode", (event) => {
        console.log(orig_fullgraph.getNodeAttributes(event.node));
        let clickednode = event.node;
        document.getElementById('node-id').innerText = clickednode;
        document.getElementById('pagerank').innerText = orig_fullgraph.getNodeAttribute(clickednode, 'pagerank').toString().substring(0, 8);
        document.getElementById('degreeCentrality').innerText = orig_fullgraph.getNodeAttribute(clickednode, 'degreeCentrality').toString().substring(0, 8);
        if (orig_fullgraph_layout.running) {
            orig_fullgraph_layout.stop();
        }
        //if (typeof autotree_fullgraph_layout != 'undefined'){
        //    autotree_fullgraph_layout.stop();
        //}
        //document.getElementById('neighbors').innerText = orig_fullgraph.edges(clickednode).length;
    })
    /*
    const nodeEvents = [
        "enterNode",
        "leaveNode",
        "downNode",
        "clickNode",
        "rightClickNode",
        "doubleClickNode",
        "wheelNode",
    ];
    const edgeEvents = ["downEdge", "clickEdge", "rightClickEdge", "doubleClickEdge", "wheelEdge"];
    const stageEvents = ["downStage", "clickStage", "doubleClickStage", "wheelStage"];

    nodeEvents.forEach((eventType) => orig_fullgraph_sigma.on(eventType, ({ node }) => logEvent(eventType, "node", node)));
    edgeEvents.forEach((eventType) => orig_fullgraph_sigma.on(eventType, ({ edge }) => logEvent(eventType, "edge", edge)));

    orig_fullgraph_sigma.on("enterEdge", ({ edge }) => {
        logEvent("enterEdge", "edge", edge);
        hoveredEdge = edge;
        orig_fullgraph_sigma.refresh();
    });
    orig_fullgraph_sigma.on("leaveEdge", ({ edge }) => {
        logEvent("leaveEdge", "edge", edge);
        hoveredEdge = null;
        orig_fullgraph_sigma.refresh();
    });

    stageEvents.forEach((eventType) => {
        orig_fullgraph_sigma.on(eventType, ({ event }) => {
            logEvent(eventType, "positions", event);
        });
    });
    function logEvent(event, itemType, item) {
        const div = document.createElement("div");
        let message = `Event "${event}"`;
        if (item && itemType) {
            if (itemType === "positions") {
                item = item;
                message += `, x ${item.x}, y ${item.y}`;
            } else {
                const label = itemType === "node" ? orig_fullgraph.getNodeAttribute(item, "label") : orig_fullgraph.getEdgeAttribute(item, "label");
                message += `, ${itemType} ${label || "with no label"} (id "${item}")`;

                if (itemType === "edge") {
                    message += `, source ${orig_fullgraph.getSourceAttribute(item, "label")}, target: ${orig_fullgraph.getTargetAttribute(
                        item,
                        "label",
                    )}`;
                }
            }
        }
        //console.log(message)
    }*/
}
var orig_fullgraph_clicked_node_flag = false;
var orig_fullgraph_current_clicked_node;
function ssm_entry_listen() {
    //orig_fullgraph_layout.kill();
    non_singular_pairs = 0;
    const ssm_start_btn = document.getElementById('ssm-start-btn');
    colormap = {};
    ssm_degree_dict = {};
    let all_size = 0;
    let ssm_all_num = 0;
    Object.entries(ssm_all_dict).forEach(([key, value]) => {
        ssm_all_num++;
        let color = '#F2EBEB';
        if (value.length > 1) {
            if (value[0] in colormap) { }
            else {
                all_size += value.length;
                let deg = orig_fullgraph.degree(value[0]);
                if (deg != 0)// not a seperated node
                    non_singular_pairs += 1;
                if (deg in ssm_degree_dict) {
                    ssm_degree_dict[deg] = ssm_degree_dict[deg] + 1;
                }
                else {
                    ssm_degree_dict[deg] = 1;
                }
            }
            color = '#' + (Math.random() * 11451415511919810).toString(16);
        }
        value.forEach(val =>
            colormap[val] = color);
    });
    ssm_start_btn.addEventListener('click', event => {
        render_degree_distribution();
        orig_fullgraph_sigma.graph.nodes().forEach(node => {
            orig_fullgraph.setNodeAttribute(node, 'color', colormap[node]);
            if (colormap[node] != '#F2EBEB') {
                orig_fullgraph.setNodeAttribute(node, 'size', 3)// orig_fullgraph.degree(node) * 4
            }
            else {
                orig_fullgraph.setNodeAttribute(node, 'size', 3)//orig_fullgraph.degree(node)
            }
        })
        orig_fullgraph_sigma.refresh();
        const ssm_entry_old = document.getElementById('ssm-entry');
        ssm_entry_old.innerHTML = `
        <div class='container p-0 m-0 d-flex flex-column h-100'>
        <table class="table table-hover table-striped  text-center mb-0">
        <tr>
            <td class="border-1 border-end">Total</td>
            <td class='align-middle' id='ssm-total'>N/A</td>
        </tr>
        <tr>
            <td class=" border-1 border-end" style="width: 40%;">Non-singletons</td>
            <td class='align-middle'>`+ non_singular_pairs + `</td>
        </tr>
        <tr>
            <td class=" border-1 border-end">Avg Size</td>
            <td class='align-middle' id='ssm-avg-size'>N/A</td>
        </tr>

        <tr><select class="form-select " aria-label="Default select example">
                <option selected>View an SSM pair</option>
                <option value="1">(13,172)</option>
                <option value="2">(44,112)</option>
                <option value="3">(876,3223)</option>
            </select>
        </tr>
    </table>

    <div class="pt-2 pb-2 ps-3 pe-3 border-1 border-bottom border-top m-0 ">
        <!-- ms-2 me-2  mt-1 -->
        <form role="search">
            <input class="form-control me-0 d-inline" style="width: 70%;" type="search"
                placeholder="Search for a node..." aria-label="Search">
            <button class="btn btn-outline-success float-end w-25"
                type="submit">Search</button>
        </form>
    </div>
    <div class="card w-100 border-0 rounded flex-fill" style="border-radius: 0;">
        <div class="card-header text-center border-top border-1 " style="border-radius: 0; padding:2%;">
            Extracted Subgraph</div>
        <div class="card-body p-0">
            <div class="container-fluid p-0 m-0 h-100 w-100" id="extracted-subgraph"></div>
        </div>
    </div>
    </div>
        `;
        document.getElementById('ssm-total').innerText = ssm_all_num.toString();
        document.getElementById('ssm-avg-size').innerText = (all_size / non_singular_pairs).toString().substring(0, 8);
        /*
        orig_fullgraph_sigma.setSetting("nodeReducer", (node, data)=>{
            const res = { ...data };
            if (node in colormap) {
                res.color = colormap[node];
            }
            else{
                res.color = "silver";
            }
            return res;
        })
        orig_fullgraph_sigma.on("enterNode", ({ node }) => {
            node.color ='#fff';
            orig_fullgraph_sigma.refresh();
        });
        orig_fullgraph_sigma.on("leaveEdge", ({ edge }) => {
            orig_fullgraph_sigma.refresh();
        });
    */
        extracted_subgraph = new graphology.Graph();
        orig_fullgraph_sigma.on("enterNode", ({ node }) => {
            if (orig_fullgraph_clicked_node_flag) {

            }
            else {
                orig_fullgraph_sigma.graph.nodes().forEach(oldnode => {
                    let flag = false;//we cannot use includes here since the elements in the array is an object
                    ssm_all_dict[node].forEach(val => {
                        if (val == oldnode) {
                            flag = true;
                        }
                    })
                    if (flag) {
                        orig_fullgraph.setNodeAttribute(oldnode, 'color', colormap[node]);
                    }
                    else {
                        orig_fullgraph.setNodeAttribute(oldnode, 'color', '#F2EBEB');
                    }
                })
                orig_fullgraph_sigma.refresh();
            }
        });
        orig_fullgraph_sigma.on("leaveNode", ({ node }) => {
            if (orig_fullgraph_clicked_node_flag) {

            }
            else {
                orig_fullgraph_sigma.graph.nodes().forEach(Gnode => {
                    orig_fullgraph.setNodeAttribute(Gnode, 'color', colormap[Gnode]);
                });
                orig_fullgraph_sigma.refresh();
            }

        });
        orig_fullgraph_sigma.on("clickNode", (event) => {
            if (typeof autotree_fullgraph_layout != 'undefined') {
                autotree_fullgraph_layout.stop();
            }
            let clickednode = event.node;
            if (orig_fullgraph_current_clicked_node == clickednode) {
                orig_fullgraph_clicked_node_flag = false;
                orig_fullgraph_current_clicked_node = -1;
                orig_fullgraph_sigma.graph.nodes().forEach(node => {
                    orig_fullgraph.setNodeAttribute(node, 'color', colormap[node]);
                })
                orig_fullgraph_sigma.refresh();
                ///////////////////////////////
                autotree_fullgraph_sigma.graph.nodes().forEach(node => {
                    autotree_fullgraph.setNodeAttribute(node, 'color', '#F2EBEB');
                })
                autotree_fullgraph_sigma.refresh();
                ///////////////////////////////////////////////////
                extracted_subgraph.clear();
                //extracted_subgraph_sigma.kill();
            }
            else {
                extracted_subgraph = new graphology.Graph();
                orig_fullgraph_current_clicked_node = clickednode;
                orig_fullgraph_clicked_node_flag = true;
                
                orig_fullgraph_sigma.graph.nodes().forEach(oldnode => {
                    let flag = false;//we cannot use includes here since the elements in the array is an object
                    ssm_all_dict[clickednode].forEach(val => {
                        if (val == oldnode) {
                            flag = true;
                        }
                    })
                    if (flag) {
                        orig_fullgraph.setNodeAttribute(oldnode, 'color', colormap[clickednode]);
                        let nodeattrs = orig_fullgraph.getNodeAttributes(oldnode);
                        if (extracted_subgraph.hasNode(oldnode)) {
                            // do nothing
                        }
                        else {
                            nodeattrs = { 'x': nodeattrs.x, 'y': nodeattrs.y, 'color': colormap[oldnode] };//nodeattrs.color
                            //console.log(nodeattrs)
                            //console.log(nodeattrs.color)
                            extracted_subgraph.addNode(oldnode, nodeattrs);
                            extracted_subgraph.setNodeAttribute(oldnode, 'color', colormap[oldnode])
                        }
                    }
                    else {
                        orig_fullgraph.setNodeAttribute(oldnode, 'color', '#F2EBEB');
                    }
                })
                orig_fullgraph_sigma.refresh();
                ///////////////////////////////
                //find all edges
                extracted_subgraph.nodes().forEach(src_node => {
                    orig_fullgraph.forEachEdge((edge, attributes, source, target, sourceAttributes, targetAttributes) => {

                        if (src_node == source || src_node == target) {
                            let target_node = source;
                            if (src_node == source) {
                                target_node = target;
                            }
                            if (extracted_subgraph.hasNode(target_node)) {
                                // add edge if not exists
                                if (extracted_subgraph.hasEdge(src_node, target_node)) {
                                    // do nothing
                                }
                                else {
                                    extracted_subgraph.addEdge(src_node, target_node);
                                }
                            }
                            else {
                                let nodeattrs = orig_fullgraph.getNodeAttributes(target_node);
                                nodeattrs = { 'x': nodeattrs.x, 'y': nodeattrs.y, 'color': colormap[target_node] };//nodeattrs.color
                                extracted_subgraph.addNode(target_node, nodeattrs);
                                extracted_subgraph.addEdge(src_node, target_node);

                            }
                        }
                    })
                });
                const container = document.getElementById('extracted-subgraph');
                container.innerHTML = '';
                extracted_subgraph.forEachNode(node => {
                    extracted_subgraph.setNodeAttribute(node, 'size', 5);
                });
                if (typeof extracted_subgraph_sigma != 'undefined') {
                    extracted_subgraph_sigma.kill();
                }
                extracted_subgraph_sigma = new Sigma(extracted_subgraph, container, {
                    defaultEdgeColor: "#e6e6e6",
                    enableEdgeClickEvents: true,
                    enableEdgeWheelEvents: true,
                    enableEdgeHoverEvents: "debounce",
                    allowInvalidContainer: true
                });
                const sensibleSettings2 = graphologyLibrary.layoutForceAtlas2.inferSettings(extracted_subgraph);
                const extracted_subgraph_layout = new graphologyLibrary.FA2Layout(extracted_subgraph, {
                    settings: sensibleSettings2,
                });
                extracted_subgraph_layout.start();
                ////////////////////////////////
                if (typeof autotree_fullgraph_sigma != 'undefined'){
                    autotree_fullgraph_sigma.graph.nodes().forEach(oldnode => {
                    let flag = false;//we cannot use includes here since the elements in the array is an object
                    full_autotree[parseInt(oldnode) + 1].vertex_list.forEach(val => {
                        if (val == clickednode) {
                            flag = true;
                        }
                    })
                    if (flag) {
                        autotree_fullgraph.setNodeAttribute(oldnode, 'color', 'green');//have bug when too big
                    }
                    else {
                        autotree_fullgraph.setNodeAttribute(oldnode, 'color', '#F2EBEB');
                    }
                    });
                    autotree_fullgraph_sigma.refresh();
                }

            }

        });
        // node collapsing
        orig_fullgraph_sigma.camera.on('coordinatesUpdated', ()=>{
            console.log('here');
            if (orig_fullgraph_sigma.camera.ratio > thresholdZoom) {
                // If the zoom level is below the threshold, collapse the nodes
                collapseNodes(orig_fullgraph_sigma);
              } else {
                // If the zoom level is above the threshold, restore the nodes
                restoreNodes(orig_fullgraph_sigma);
              }
        });
        ////////////////////////////////////
        function collapseNodes(s) {
            // Store the original node data
            originalNodes = s.graph.nodes();
          
            // Group the nodes into clusters
            const clusters = groupNodesIntoClusters(originalNodes);
          
            // Remove the individual nodes from the graph
            originalNodes.forEach(node => s.graph.dropNode(node.id));
          
            // Add a new node for each cluster
            clusters.forEach(cluster => {
              s.graph.addNode({
                id: cluster.id,
                size: cluster.size,
                color: cluster.color,
                x: cluster.x,
                y: cluster.y,
                label: `Cluster ${cluster.id}`
                });
            });
        }
        
        // Define a function to restore the nodes
        function restoreNodes(s) {
            // Get the current nodes from the graph
            const nodes = s.graph.nodes();
        
            // Remove the aggregate nodes from the graph
            nodes.forEach(node => {
            if (node.label && node.label.startsWith('Cluster')) {
                s.graph.dropNode(node.id);
            }
            });
        
            // Add the individual nodes back to the graph
            originalNodes.forEach(node => s.graph.addNode(node));
        }
        function groupNodesIntoClusters(nodes) {
            // Placeholder implementation - in practice, you would implement
            // the logic for grouping the nodes into clusters based on your needs
          
            // For this example, we'll group nodes based on their proximity in the layout

            const clusters = [];
            nodes.forEach(node => {
              let addedToCluster = false;
              clusters.forEach(cluster => {
                if (distance(node, cluster) < thresholdDistance) {
                  cluster.nodes.push(node);
                  addedToCluster = true;
                }
              });
              if (!addedToCluster) {
                clusters.push({
                  id: `cluster-${clusters.length + 1}`,
                  size: 10,
                  color: '#ff0000',
                  x: node.x,
                  y: node.y,
                  nodes: [node]
                });
              }
            });
            return clusters;
          }
          
          // Define a function to calculate the distance between two nodes
          function distance(node1, node2) {
            return Math.sqrt(Math.pow(node1.x - node2.x, 2) + Math.pow(node1.y - node2.y, 2));
          }

    })
    ssm_start_btn.disabled = false;
}
var autotree_fullgraph_clicked_node_flag = false;
var autotree_fullgraph_current_clicked_node;
function autotree_entry_listen() {
    const autotree_start_btn = document.getElementById('autotree-start-btn');
    autotree_start_btn.addEventListener('click', event => {
        const autotree_entry = document.getElementById('autotree-entry');
        autotree_entry.innerHTML = `
        <div class="container p-0 m-0 d-flex flex-column h-100">
        <table class="table table-hover table-striped  text-center mb-0">
            <tr>
                <td class="border-1 border-end">Total Cells</td>
                <td class='align-middle' id='total-cells'></td>
            </tr>
            <tr>
                <td class=" border-1 border-end" style="width: 40%;">Non-Leaf Cells</td>
                <td class='align-middle' id='non-leaf-cells'></td>
            </tr>
        </table>
        <div class="pt-2 pb-2 ps-3 pe-3 border-1 border-bottom border-top m-0 d-flex justify-content-center">
                <button class="btn btn-outline-warning "
                    type="button" id='clear-belt'>Clear Asteroid Belt</button>
        </div>
        <div class='card p-0 border-2 w-100 border-0 flex-fill' style=' overflow:hidden'>
            <div class='card-header'>
                <p class='m-0 d-inline align-bottom'>Full AutoTree</p>
                <p class='m-0 d-inline float-end text-secondary' style='cursor:pointer' data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">>>></p>
            </div>
            <div class='card-body p-0'>
                <div class='h-100 w-100' id='autotree-fullgraph-container'></div>
            </div>
        </div>
    </div>`
        render_autotree_fullgraph();
        /*
        orig_fullgraph_sigma.on("clickNode", (event) => {
            let clickednode = event.node;
            const nodeid_doc = document.getElementById('node-id');
            nodeid_doc.innerText = clickednode;
            if (orig_fullgraph_current_clicked_node == clickednode) {
                autotree_fullgraph_sigma.graph.nodes().forEach(node => {
                    autotree_fullgraph.setNodeAttribute(node, 'color', '#F2EBEB');
                })
                autotree_fullgraph_sigma.refresh();
            }
            else {
                autotree_fullgraph_sigma.graph.nodes().forEach(oldnode => {
                    let flag = false;//we cannot use includes here since the elements in the array is an object
                    full_autotree[parseInt(oldnode) + 1].vertex_list.forEach(val => {
                        if (val == clickednode) {
                            flag = true;
                        }
                    })
                    if (flag) {
                        autotree_fullgraph.setNodeAttribute(oldnode, 'color', 'green');//have bug when too big
                    }
                    else {
                        autotree_fullgraph.setNodeAttribute(oldnode, 'color', '#F2EBEB');
                    }
                })
                autotree_fullgraph_sigma.refresh();
            }

        });*/

    })
}
function render_autotree_fullgraph() {
    const container = document.getElementById("autotree-fullgraph-container");
    autotree_fullgraph = new graphology.Graph();
    container.innerHTML = '';
    non_leaf_cell = 0;
    total_cell = Object.keys(full_autotree).length;
    document.getElementById('total-cells').innerText = total_cell.toString();
    for (let val in full_autotree) {
        let tmp_node = full_autotree[val];
        if (tmp_node.size != 1) {
            non_leaf_cell += 1;
        }
        autotree_fullgraph.addNode(tmp_node.order, { x: Math.random(), y: Math.random(), size: Math.max(5 - parseInt(tmp_node.depth), 1) * 1.25, label: tmp_node.order, color: "#F2EBEB" });
    };
    document.getElementById('non-leaf-cells').innerText = non_leaf_cell.toString();
    for (let val in full_autotree) {
        if (full_autotree[val].children[0] != '-1') {
            for (let child in full_autotree[val].children) {
                autotree_fullgraph.addEdge(full_autotree[val].order, full_autotree[val].children[child])
            }
        }
    };
    /*
    autotree_fullgraph.forEachNode((node) => {
        autotree_fullgraph.mergeNodeAttributes(node, {
            size: Math.min(autotree_fullgraph.degree(node) * 1.5, 5),
            color: '#' + (autotree_fullgraph.degree(node) * 1919810).toString(16)
        });
    });*/
    // eslint-disable-next-line @typescript-eslint/no-unused-vars

    let hoveredEdge = null;
    if (typeof autotree_fullgraph_sigma != 'undefined') {
        autotree_fullgraph_sigma.kill();
    }
    autotree_fullgraph_sigma = new Sigma(autotree_fullgraph, container, {
        defaultEdgeColor: "#e6e6e6",
        enableEdgeClickEvents: true,
        enableEdgeWheelEvents: true,
        enableEdgeHoverEvents: "debounce",
        allowInvalidContainer: true
    });
    const sensibleSettings = graphologyLibrary.layoutForceAtlas2.inferSettings(autotree_fullgraph);
    autotree_fullgraph_layout = new graphologyLibrary.FA2Layout(autotree_fullgraph, {
        settings: sensibleSettings,
    });
    autotree_fullgraph_layout.start();
    var orig_fullgraph_saved_colormap = {};//for autotree viz in full graph
    var saved_color;
    autotree_fullgraph_sigma.on("enterNode", ({ node }) => {
        orig_fullgraph.nodes().forEach(Gnode => {
            orig_fullgraph_saved_colormap[Gnode] = orig_fullgraph.getNodeAttribute(Gnode, 'color');
        });
        saved_color = autotree_fullgraph.getNodeAttribute(node, 'color');
        autotree_fullgraph.setNodeAttribute(node, 'color', 'red');
        autotree_fullgraph_sigma.refresh();
        for (let included_node in full_autotree[parseInt(node) + 1].vertex_list) {
            let tmp_id = full_autotree[parseInt(node) + 1].vertex_list[included_node];
            orig_fullgraph.setNodeAttribute(tmp_id, 'color', 'red');
        }
        orig_fullgraph_sigma.refresh();
    });
    autotree_fullgraph_sigma.on("leaveNode", ({ node }) => {
        //orig_fullgraph.clear();
        orig_fullgraph.nodes().forEach(Gnode => {
            orig_fullgraph.setNodeAttribute(Gnode, 'color', orig_fullgraph_saved_colormap[Gnode]);
        });
        orig_fullgraph_sigma.refresh();
        autotree_fullgraph.setNodeAttribute(node, 'color', saved_color);
        autotree_fullgraph_sigma.refresh();
    });
    /*
    orig_fullgraph_sigma.on("clickNode", (event) => {
        let clickednode = event.node;
        const nodeid_doc = document.getElementById('node-id');
        nodeid_doc.innerText = clickednode;
        if (orig_fullgraph_current_clicked_node == clickednode) {
            console.log(clickednode)
            console.log(orig_fullgraph_current_clicked_node)
            orig_fullgraph_clicked_node_flag = false;
            orig_fullgraph_sigma.graph.nodes().forEach(node => {
                orig_fullgraph.setNodeAttribute(node, 'color', colormap[node]);
            })
            orig_fullgraph_sigma.refresh();
            orig_fullgraph_current_clicked_node = clickednode;
        }
        else {
            orig_fullgraph_current_clicked_node = clickednode;
            orig_fullgraph_clicked_node_flag = true;
            orig_fullgraph_sigma.graph.nodes().forEach(oldnode => {
                let flag = false;//we cannot use includes here since the elements in the array is an object
                ssm_all_dict[clickednode].forEach(val => {
                    if (val == oldnode) {
                        flag = true;
                    }
                })
                if (flag) {
                    orig_fullgraph.setNodeAttribute(oldnode, 'color', colormap[clickednode]);
                }
                else {
                    orig_fullgraph.setNodeAttribute(oldnode, 'color', '#F2EBEB');
                }
            })
            orig_fullgraph_sigma.refresh();
        }

    });*/
    const clear_belt_btn = document.getElementById('clear-belt');
    clear_belt_btn.addEventListener('click', event => {
        for (let val in full_autotree) {
            let tmp_node = full_autotree[val];
            if (tmp_node.depth == 1 && tmp_node.size == 1) {
                autotree_fullgraph.dropNode(tmp_node.order);
            }
        };
        autotree_fullgraph_sigma.refresh();
        if (autotree_fullgraph_layout.runnning) {
            // do nothing
        } else {
            autotree_fullgraph_layout.start();
        }
    });
    document.getElementById('autotree-entry-tab').addEventListener('click', event => {
        if (typeof autotree_fullgraph_sigma != 'undefined') {
            autotree_fullgraph_sigma.refresh();
        }
    })
}
function render_degree_distribution() {
    Highcharts.chart('degree-distribution', {
        credits: {
            enabled: false
        },
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: [{
            categories: Object.keys(all_node_degree_dict),
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: '',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: '',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                //format: '{value} mm',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }],
        tooltip: {
            headerFormat: '<span style="font-size:10px">Degree {point.key}</span><br><table>',
            footerFormat: '</table>',
            shared: true
        },/*
        legend: {
            align: 'left',
            x: 80,
            verticalAlign: 'top',
            y: 80,
            floating: true,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || // theme
                'rgba(255,255,255,0.25)'
        },*/
        series: [{
            name: 'SSM',
            type: 'column',
            yAxis: 1,
            data: Object.values(ssm_degree_dict),
            //tooltip: {
            //}

        }, {
            name: 'All Nodes',
            type: 'spline',
            data: Object.values(all_node_degree_dict),
            //tooltip: {
            //}
        }]
    });

}
function factorial(num) {
    if(num < 0){
        return -1;
    }
    else if(num == 0){
        return 1;
    } 
    else{
        return (num * factorial(num - 1));
    }
}
var orig_fullgraph_clicked_node_flag_for_im = false;
function im_entry_listen() {
    //orig_fullgraph_layout.kill();
    const im_start_btn = document.getElementById('im-start-btn');
    var im_colormap = {};
    // from red to yellow, we only modify the middle content in hex color environment
    let start_color = 0; //ff0000
    let end_color = parseInt('ff', 16); // ff'dd'00
    let number_of_rounds = Object.keys(im_all_dict).length; // plus 4 to create big gap between round 0 and round 1
    let gap = end_color / number_of_rounds;
    var colormap_html = '';
    Object.entries(im_all_dict).forEach(([key, value]) => {
        let color = '#ff0000';
        if (value.length > 1) {
            if (key==0){

            }
            else{
                color = '#ff' + (end_color - (number_of_rounds - key) * 25).toString(16).substring(0,2) + '00';
            }
            colormap_html += `<li class="list-group-item d-flex align-items-center">
            <span class="badge rounded-pill me-3" style="background-color:`+ color.substring(0, 7) +`">`+ key +`</span>
            <span class="fw-bold">Round `+ key +`</span>
          </li>`
        }
        value.forEach(val =>{
            im_colormap[val] = color;
        });
        value.forEach(val =>{
            orig_fullgraph.setNodeAttribute(val, 'round', key);
        })
    });
    
    im_start_btn.addEventListener('click', event => {

        orig_fullgraph_sigma.graph.nodes().forEach(node => {
            if (typeof im_colormap[node] != 'undefined') {
                let round_of_node = orig_fullgraph.getNodeAttribute(node, 'round');
                /*
                if(im_colormap[node] == '#ff0000'){
                    round_of_node = 0;
                }
                else{
                    round_of_node = (end_color - parseInt(im_colormap[node].substring(3, 5), 16)) / 25;
                }*/
                orig_fullgraph.setNodeAttribute(node, 'color', im_colormap[node]);  
                let node_size = Math.max(1, (number_of_rounds - round_of_node + 2)/1.5);
                orig_fullgraph.setNodeAttribute(node, 'size', node_size);// (end_color - parseInt(im_colormap[node].substring(3, 5), 16)) / 25  + 1
                let edge_color = im_colormap[node] + (parseInt('dd',16) - 13 * round_of_node).toString(16); // add alpha
                orig_fullgraph.forEachEdge(node, (edge, edge_attr, src, tar, src_attr, tar_attr)=>{
                    if(src == node){
                        if(typeof tar_attr.round != 'undefined'){
                            if ( (tar_attr.round - src_attr.round) == 1 ){
                                orig_fullgraph.setEdgeAttribute(edge, 'color', edge_color);
                                orig_fullgraph.setEdgeAttribute(edge, 'size', 0.25*(number_of_rounds - src_attr.round));
                                } 
                        }
                    }

                    else if(tar == node){
                        if(typeof src_attr.round != 'undefined'){
                            if ( (src_attr.round - tar_attr.round) == 1 ){
                                orig_fullgraph.setEdgeAttribute(edge, 'color', edge_color);
                                orig_fullgraph.setEdgeAttribute(edge, 'size', 0.25*(number_of_rounds - tar_attr.round));
                                } 
                        }
                    }
                    
                })
                //orig_fullgraph.setNodeAttribute(node, 'type', 'triangle')
            }
            else {
                orig_fullgraph.setNodeAttribute(node, 'color', '#d8d8d8');
                orig_fullgraph.setNodeAttribute(node, 'size', 1)//orig_fullgraph.degree(node)
            }
        })
        
        orig_fullgraph_sigma.on("enterNode", ({node})=>{saved_graph = orig_fullgraph.copy();
            //if not clicked before, then update
                //orig_fullgraph_clicked_node_flag_for_im = true;
                let node_round = orig_fullgraph.getNodeAttribute(node, 'round');
                orig_fullgraph.updateEachNodeAttributes((node, attr) => {
                    return {
                      ...attr,
                      color:'#d8d8d8',
                      z:0
                    };
                  });
                orig_fullgraph.updateEachEdgeAttributes((edge, attr) => {
                    return {
                      ...attr,
                      color:'#F2EBEB',
                      zIndex:0
                    };
                  });
                var im_rec = document.getElementById('im-rec').checked;
                recursive_im_viz( node,im_rec, number_of_rounds, parseInt(node_round,10));//true for recursive viz
                orig_fullgraph_sigma.refresh();  
            })
            // if clicked, then restore
            orig_fullgraph_sigma.on("leaveNode", ({node})=>{
                //orig_fullgraph_clicked_node_flag_for_im = false;
                orig_fullgraph = saved_graph.copy();
                orig_fullgraph_sigma.graph = orig_fullgraph;
                orig_fullgraph_sigma.refresh();
            })

        
        orig_fullgraph_sigma.refresh();
        const im_entry_old = document.getElementById('im-entry');
        im_entry_old.innerHTML = `
        <div class="container p-0 m-0 d-flex flex-column h-100">
            <div class="btn-group btn-group-toggle" data-toggle="buttons">
                <label class="btn btn-primary active">
                    <input type="radio" name="options" id="im-rec" autocomplete="off" checked> Recursive
                </label>
                <label class="btn btn-primary">
                    <input type="radio" name="options" id="im-not-rec" autocomplete="off"> Nearest
                </label>
            </div>

            <div class="chart-body bg-light overflow-auto flex-grow-1">
            <ul class="list-group list-group-flush">
                `+colormap_html+`
            </ul>
            </div>
      </div>
      
        `;


    })
    im_start_btn.disabled = false;
}
//recursively shows IM with option. rec for flag
function recursive_im_viz(node, rec,total_round,current_round){
    if (current_round > total_round){
        return
    }console.log(current_round)
    orig_fullgraph.forEachEdge(node, (edge, edge_attr, src, tar, src_attr, tar_attr)=>{
        if(node==src){
            if(parseInt(tar_attr.round,10) - parseInt(src_attr.round,10) == 1){
                let orig_edge_color = saved_graph.getEdgeAttribute(edge, 'color');
                if(typeof orig_edge_color != 'undefined'){//if in orig graph, this edge has been spreaded
                    orig_fullgraph.setNodeAttribute(src, 'color', saved_graph.getNodeAttribute(src, 'color'));
                    orig_fullgraph.setNodeAttribute(tar, 'color', saved_graph.getNodeAttribute(tar, 'color'));
                    orig_fullgraph.setNodeAttribute(src, 'z', 1);
                    orig_fullgraph.setNodeAttribute(tar, 'z', 1);
                    orig_fullgraph.setEdgeAttribute(edge, 'color', orig_edge_color);
                    orig_fullgraph.setEdgeAttribute(edge, 'zIndex', 1);
                    if(rec){
                        if(node == src){
                            recursive_im_viz(tar, rec,total_round,current_round+1);
                        }
                        else{
                            recursive_im_viz(src,rec,total_round,current_round+1);
                        }
                    }
                }
            }
        }
        else if(node==tar){
            if(parseInt(src_attr.round,10) - parseInt(tar_attr.round,10) == 1){
                let orig_edge_color = saved_graph.getEdgeAttribute(edge, 'color');
                if(typeof orig_edge_color != 'undefined'){//if in orig graph, this edge has been spreaded
                    orig_fullgraph.setNodeAttribute(src, 'color', saved_graph.getNodeAttribute(src, 'color'));
                    orig_fullgraph.setNodeAttribute(tar, 'color', saved_graph.getNodeAttribute(tar, 'color'));
                    orig_fullgraph.setNodeAttribute(src, 'z', 1);
                    orig_fullgraph.setNodeAttribute(tar, 'z', 1);
                    orig_fullgraph.setEdgeAttribute(edge, 'color', orig_edge_color);
                    orig_fullgraph.setEdgeAttribute(edge, 'zIndex', 1);
                    if(rec){
                        if(node == src){
                            recursive_im_viz(tar, rec,total_round,current_round+1);
                        }
                        else{
                            recursive_im_viz(src,rec,total_round,current_round+1);
                        }
                    }
                }
            }
        }

        
    })
}