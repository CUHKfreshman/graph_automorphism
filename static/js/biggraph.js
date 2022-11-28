//TODO: need to disable autotree sigma graph if new file inputted or change to SSM panel
// DO NOT ACCEPT AN EXTRA EMPTY LINE AT THE END
let file = document.getElementById("readfile");
var ssm_all_dict;
var full_autotree;
var colormap;
var orig_fullgraph = new graphology.Graph();
var autotree_fullgraph = new graphology.Graph();
var autotree_subgraph = new graphology.Graph();
var autotree_subgraph_parent = new graphology.Graph();
var autotree_subgraph_child = new graphology.Graph();
var orig_fullgraph_sigma;
var autotree_fullgraph_sigma;
var autotree_subgraph_sigma;
var autotree_subgraph_parent_sigma;
var autotree_subgraph_child_sigma;
file.addEventListener("change", function () {
    var reader = new FileReader();
    reader.onload = function (progressEvent) {
        file = this.result;
        raw_txt = this.result.split(/\s|\n/);
        const nodenum_doc = document.getElementById('nodenum');
        const edgenum_doc = document.getElementById('edgenum');
        nodenum_doc.innerText = raw_txt[0];
        edgenum_doc.innerText = raw_txt[1];
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
                let packed_data = response.data;
                full_autotree = packed_data[0];

                ssm_all_dict = packed_data[1];
                autotree_entry_listen();
                ssm_entry_listen();
            })
            .catch(function (error) {
                console.log(error);
            });
    };
    reader.readAsText(this.files[0]);
});

function render_orig_fullgraph(raw_txt) {
    const container = document.getElementById("orig-fullgraph-container");
    orig_fullgraph = new graphology.Graph();
    container.innerHTML = '';
    for (let i = 0; i < raw_txt[0]; i++) {
        orig_fullgraph.addNode(i.toString(), { x: Math.random() * 10, y: Math.random() * 10, size: 2, label: i.toString(), color: "silver" });
    }
    for (let i = 2; i < raw_txt.length; i += 2) {
        orig_fullgraph.addEdge(raw_txt[i], raw_txt[i + 1])
    }
    let i = 0;
    orig_fullgraph.forEachNode((node) => {
        orig_fullgraph.mergeNodeAttributes(node, {
            size: Math.min(orig_fullgraph.degree(node) * 1.5, 5),
            color: '#' + (orig_fullgraph.degree(node) * 1919810).toString(16)
        });
    });
    // eslint-disable-next-line @typescript-eslint/no-unused-vars

    let hoveredEdge = null;
    orig_fullgraph_sigma = new Sigma(orig_fullgraph, container, {
        defaultEdgeColor: "#e6e6e6",
        enableEdgeClickEvents: true,
        enableEdgeWheelEvents: true,
        enableEdgeHoverEvents: "debounce"
    });
    const sensibleSettings = graphologyLibrary.layoutForceAtlas2.inferSettings(orig_fullgraph);
    const fa2Layout = new graphologyLibrary.FA2Layout(orig_fullgraph, {
        settings: sensibleSettings,
    });
    fa2Layout.start();
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
    var non_singular_pairs = 0;
    const ssm_start_btn = document.getElementById('ssm-start-btn');
    colormap = {};
    Object.entries(ssm_all_dict).forEach(([key, value]) => {
        let color = '#F2EBEB';
        if (value.length > 1) {
            if (value[0] in colormap) { }
            else {
                if (orig_fullgraph.degree(value[0]) != 0)// not a seperated node
                    non_singular_pairs += 1;
            }
            color = '#' + (Math.random() * 11451415511919810).toString(16);
        }

        value.forEach(val =>
            colormap[val] = color);
    });
    ssm_start_btn.addEventListener('click', event => {
        orig_fullgraph_sigma.graph.nodes().forEach(node => {
            orig_fullgraph.setNodeAttribute(node, 'color', colormap[node]);
            if (colormap[node] != '#F2EBEB') {
                orig_fullgraph.setNodeAttribute(node, 'size', 5)// orig_fullgraph.degree(node) * 4
            }
            else {
                orig_fullgraph.setNodeAttribute(node, 'size', 3)//orig_fullgraph.degree(node)
            }
        })
        orig_fullgraph_sigma.refresh();
        const ssm_entry_old = document.getElementById('ssm-entry');
        ssm_entry_old.innerHTML = `
        <table class="table table-hover table-striped table-bordered text-center">
        <tr><td class="w-25">Non-singular SSM Pairs</td><td class='align-middle'>`+ non_singular_pairs + `</td></tr>
        <tr><td class="w-25">Other property1</td><td class='align-middle'>N/A</td></tr>
        <tr><td class="w-25">Other property2</td><td class='align-middle'>N/A</td></tr>
        <tr><td class="w-25">Other property3</td><td class='align-middle'>N/A</td></tr>
        
        <tr><select class="form-select" aria-label="Default select example">
            <option selected>View an SSM pair</option>
            <option value="1">(13,172)</option>
            <option value="2">(44,112)</option>
            <option value="3">(876,3223)</option>
          </select>
        </tr>
    </table>
    
    <div class="p-3 border ms-2 me-2 bg-light mt-1">  
        <form role="search">
        <input class="form-control me-2 w-75 d-inline" type="search" placeholder="Search for a node..." aria-label="Search">
        <button class="btn btn-outline-success float-end" type="submit">Search</button>
        </form>
    </div>
        `;
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
                })
                orig_fullgraph_sigma.refresh();
            }

        });
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
                ///////////////////////////////
                autotree_fullgraph_sigma.graph.nodes().forEach(node => {
                    autotree_fullgraph.setNodeAttribute(node, 'color', '#F2EBEB');
                })
                autotree_fullgraph_sigma.refresh();
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
                ////////////////////////////////
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

        });
        ////////////////////////////////////


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
        <div class='card p-0 border-2' style='height:55vh; overflow:hidden'>
        <div class='card-header'>
            <p class='m-0 d-inline align-bottom'>Full AutoTree</p>
            <p class='m-0 d-inline float-end text-secondary' style='cursor:pointer' data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">>>></p>
        </div>
        <div class='card-body'>
        <div class='h-100 w-100' id='autotree-fullgraph-container'></div>
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
    for (let val in full_autotree) {
        let tmp_node = full_autotree[val];
        autotree_fullgraph.addNode(tmp_node.order, { x: parseInt(tmp_node.order) - parseInt(tmp_node.depth), y: parseInt(tmp_node.depth), size: 6 - parseInt(tmp_node.depth), label: tmp_node.order, color: "#F2EBEB" });
    }

    for (let val in full_autotree) {
        if (full_autotree[val].children[0] != '-1') {
            for (let child in full_autotree[val].children) {
                autotree_fullgraph.addEdge(full_autotree[val].order, full_autotree[val].children[child])
            }
        }
    }
    let i = 0;
    /*
    autotree_fullgraph.forEachNode((node) => {
        autotree_fullgraph.mergeNodeAttributes(node, {
            size: Math.min(autotree_fullgraph.degree(node) * 1.5, 5),
            color: '#' + (autotree_fullgraph.degree(node) * 1919810).toString(16)
        });
    });*/
    // eslint-disable-next-line @typescript-eslint/no-unused-vars

    let hoveredEdge = null;
    autotree_fullgraph_sigma = new Sigma(autotree_fullgraph, container, {
        defaultEdgeColor: "#e6e6e6",
        enableEdgeClickEvents: true,
        enableEdgeWheelEvents: true,
        enableEdgeHoverEvents: "debounce",
        allowInvalidContainer: true
    });
    const sensibleSettings = graphologyLibrary.layoutForceAtlas2.inferSettings(autotree_fullgraph);
    const fa2Layout = new graphologyLibrary.FA2Layout(autotree_fullgraph, {
        settings: sensibleSettings,
    });
    fa2Layout.start();
    var orig_fullgraph_saved_attrs;//for autotree viz in full graph
    var saved_color;
    autotree_fullgraph_sigma.on("enterNode", ({ node }) => {
        orig_fullgraph_saved_attrs = orig_fullgraph.export();
        saved_color = autotree_fullgraph.getNodeAttribute(node, 'color');
        autotree_fullgraph.setNodeAttribute(node,'color','red');
        autotree_fullgraph_sigma.refresh();
        for(let included_node in full_autotree[parseInt(node) + 1].vertex_list){
            let tmp_id = full_autotree[parseInt(node) + 1].vertex_list[included_node];
            orig_fullgraph.setNodeAttribute(tmp_id,'color','red');
        }
        orig_fullgraph_sigma.refresh();
    });
    autotree_fullgraph_sigma.on("leaveNode", ({ node }) => {
        orig_fullgraph.clear();
        orig_fullgraph.import(orig_fullgraph_saved_attrs);
        autotree_fullgraph.setNodeAttribute(node,'color',saved_color);
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
}