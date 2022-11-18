
// DO NOT ACCEPT AN EXTRA EMPTY LINE AT THE END
let file = document.getElementById("readfile");
var ssm_all_dict;
var colormap;
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
            <button type='button' class="btn btn-outline-primary position-absolute top-50 start-50 translate-middle" id="ssm-start-btn">Start Analysis</button>
        </div>
        `;
        const autotree_entry = document.getElementById('autotree-entry');
        autotree_entry.innerHTML = `
        <div class="w-75 h-25 border position-absolute top-50 start-50 translate-middle">
        <button type='button' class="btn btn-outline-primary position-absolute top-50 start-50 translate-middle" id="autotree-start-btn"  data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">AutoTree Entry</button>
    </div>`
        render_graph(raw_txt);
        axios.post('/upload', { file, raw_txt })
            .then(function (response) {
                console.log(response);
                ssm_all_dict = response.data;
                ssm_entry_listen();
                autotree_entry_listen();
            })
            .catch(function (error) {
                console.log(error);
            });
    };
    reader.readAsText(this.files[0]);
});

var fullgraph = new graphology.Graph();
var fullgraph_render;
function render_graph(raw_txt) {
    const container = document.getElementById("sigma-container");
    fullgraph = new graphology.Graph();
    container.innerHTML = '';
    for (let i = 0; i < raw_txt[0]; i++) {
        fullgraph.addNode(i.toString(), { x: Math.random() * 10, y: Math.random() * 10, size: 2, label: i.toString(), color: "silver" });
    }
    for (let i = 2; i < raw_txt.length; i += 2) {
        fullgraph.addEdge(raw_txt[i], raw_txt[i + 1])
    }
    let i = 0;
    fullgraph.forEachNode((node) => {
        fullgraph.mergeNodeAttributes(node, {
            size: Math.min(fullgraph.degree(node) * 1.5, 22),
            color: '#' + (fullgraph.degree(node) * 1919810).toString(16)
        });
    });
    // eslint-disable-next-line @typescript-eslint/no-unused-vars

    let hoveredEdge = null;
    fullgraph_render = new Sigma(fullgraph, container, {
        defaultEdgeColor: "#e6e6e6",
        enableEdgeClickEvents: true,
        enableEdgeWheelEvents: true,
        enableEdgeHoverEvents: "debounce"
    });
    const sensibleSettings = graphologyLibrary.layoutForceAtlas2.inferSettings(fullgraph);
    const fa2Layout = new graphologyLibrary.FA2Layout(fullgraph, {
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

    nodeEvents.forEach((eventType) => fullgraph_render.on(eventType, ({ node }) => logEvent(eventType, "node", node)));
    edgeEvents.forEach((eventType) => fullgraph_render.on(eventType, ({ edge }) => logEvent(eventType, "edge", edge)));

    fullgraph_render.on("enterEdge", ({ edge }) => {
        logEvent("enterEdge", "edge", edge);
        hoveredEdge = edge;
        fullgraph_render.refresh();
    });
    fullgraph_render.on("leaveEdge", ({ edge }) => {
        logEvent("leaveEdge", "edge", edge);
        hoveredEdge = null;
        fullgraph_render.refresh();
    });

    stageEvents.forEach((eventType) => {
        fullgraph_render.on(eventType, ({ event }) => {
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
                const label = itemType === "node" ? fullgraph.getNodeAttribute(item, "label") : fullgraph.getEdgeAttribute(item, "label");
                message += `, ${itemType} ${label || "with no label"} (id "${item}")`;

                if (itemType === "edge") {
                    message += `, source ${fullgraph.getSourceAttribute(item, "label")}, target: ${fullgraph.getTargetAttribute(
                        item,
                        "label",
                    )}`;
                }
            }
        }
        //console.log(message)
    }*/
}
var clicked_node_flag = false;
var current_clicked_node;
function ssm_entry_listen(){
    var non_singular_pairs = 0;
    const ssm_start_btn = document.getElementById('ssm-start-btn');
    colormap = {};
    Object.entries(ssm_all_dict).forEach(([key, value]) => {
        let color = '#F2EBEB';
        if(value.length >1){
            if(value[0] in colormap) {}
            else{
                if (fullgraph.degree(value[0])!=0)// not a seperated node
                non_singular_pairs += 1;
            }
            color = '#' + (Math.random() * 11451415511919810).toString(16);
        }
        
        value.forEach(val=>
            colormap[val] = color);
    });
    ssm_start_btn.addEventListener('click', event => {
        fullgraph_render.graph.nodes().forEach(node=>{
            fullgraph.setNodeAttribute(node, 'color', colormap[node]);
            if (colormap[node] != '#F2EBEB'){
                fullgraph.setNodeAttribute(node, 'size', fullgraph.degree(node) * 4)
            }
            else{
                fullgraph.setNodeAttribute(node, 'size', fullgraph.degree(node))
            }
        })
        fullgraph_render.refresh();
        const ssm_entry_old = document.getElementById('ssm-entry');
        ssm_entry_old.innerHTML = `
        <table class="table table-hover table-striped table-bordered text-center">
        <tr><td class="w-25">Non-singular SSM Pairs</td><td class='align-middle'>`+non_singular_pairs+`</td></tr>
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
        fullgraph_render.setSetting("nodeReducer", (node, data)=>{
            const res = { ...data };
            if (node in colormap) {
                res.color = colormap[node];
            }
            else{
                res.color = "silver";
            }
            return res;
        })
        fullgraph_render.on("enterNode", ({ node }) => {
            node.color ='#fff';
            fullgraph_render.refresh();
        });
        fullgraph_render.on("leaveEdge", ({ edge }) => {
            fullgraph_render.refresh();
        });
    */
        fullgraph_render.on("enterNode", ({ node }) => {
            if(clicked_node_flag){

            }
            else{
                fullgraph_render.graph.nodes().forEach(oldnode=>{
                    let flag = false;//we cannot use includes here since the elements in the array is an object
                    ssm_all_dict[node].forEach(val=>{
                        if(val == oldnode){
                            flag = true;
                        }
                    })
                    if (flag){
                        fullgraph.setNodeAttribute(oldnode, 'color', colormap[node]);
                    }
                    else{
                        fullgraph.setNodeAttribute(oldnode, 'color', '#F2EBEB');
                    }
                })
                fullgraph_render.refresh();
            }
        });
        fullgraph_render.on("leaveNode", ({ leftnode }) => {
            if(clicked_node_flag){

            }
            else{
                fullgraph_render.graph.nodes().forEach(node=>{
                    fullgraph.setNodeAttribute(node, 'color', colormap[node]);
                })   
            fullgraph_render.refresh();
            }

        });
        fullgraph_render.on("clickNode", ( event ) => {
            clickednode = event.node;
            const nodeid_doc = document.getElementById('node-id');
            nodeid_doc.innerText = clickednode;
            if (current_clicked_node == clickednode){
                console.log(clickednode)
                console.log(current_clicked_node)
                clicked_node_flag = false;
                fullgraph_render.graph.nodes().forEach(node=>{
                    fullgraph.setNodeAttribute(node, 'color', colormap[node]);
                })   
                fullgraph_render.refresh();
                current_clicked_node = clickednode;
            }
            else{
                current_clicked_node = clickednode;
                clicked_node_flag = true;
                fullgraph_render.graph.nodes().forEach(oldnode=>{
                    let flag = false;//we cannot use includes here since the elements in the array is an object
                    ssm_all_dict[clickednode].forEach(val=>{
                        if(val == oldnode){
                            flag = true;
                        }
                    })
                    if (flag){
                        fullgraph.setNodeAttribute(oldnode, 'color', colormap[clickednode]);
                    }
                    else{
                        fullgraph.setNodeAttribute(oldnode, 'color', '#F2EBEB');
                    }
                })
                fullgraph_render.refresh();
            }

        });

    })
}
function autotree_entry_listen(){
    const autotree_start_btn = document.getElementById('autotree-start-btn');
    autotree_start_btn.addEventListener('click', event=>{
        const autotree_entry = document.getElementById('autotree-entry');
        autotree_entry.innerHTML = `
        <div class='card p-0 border-2' style='height:55vh; overflow:hidden'>
        <div class='card-header'>
            <p class='m-0 d-inline align-bottom'>Full AutoTree</p>
            <p class='m-0 d-inline float-end text-secondary' style='cursor:pointer' data-bs-toggle="offcanvas" data-bs-target="#offcanvasScrolling" aria-controls="offcanvasScrolling">>>></p>
        </div>
        <div class='card-body'></div>
    </div>`
    })
}