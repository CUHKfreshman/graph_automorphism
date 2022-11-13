/*
alert('If you see this alert, then your custom JavaScript script has run!')


function init_cy(){
    let cy = window.cy;
    window.complete_elements = cy.elements();
    window.complete_elements_copy = window.complete_elements.clone();

    window.cy.on('mouseover', 'node', function(e) {
        let sel = e.target;
        cy.elements()
            .difference(sel.outgoers()
                .union(sel.incomers()))
            .not(sel)
            .addClass('semitransp');
        sel.addClass('highlight')
            .outgoers()
            .union(sel.incomers())
            .addClass('highlight');
    });

    window.cy.on('mouseout', 'node', function(e) {
        let sel = e.target;
        cy.elements()
            .removeClass('semitransp');
        sel.removeClass('highlight')
            .outgoers()
            .union(sel.incomers())
            .removeClass('highlight');
    });

    // 🚩 Add Click Event on Node (this is a walk-around solution) >>>
    window.cy.on('click', 'node', function(e) {
        var val = alert(`Node id: ${e.target.id()}`);

    }); // # 🚩<<<
}



function init_slider(){
    document.getElementById('node-slider').addEventListener("change", function(e){
      let cy = window.cy;
    //   // Remove all elements first
      cy.elements().remove()
    //   // Add all elements then; This is more convenient to compute nodes to remove in the original graph than subgraph. 
      cy.add(window.complete_elements_copy);
      var complete_nodes = cy.nodes();
      let percentage = Number(e.target.value);
      let total_length = complete_nodes.length;
      let threshold = total_length * percentage;
      let node2remove = complete_nodes.filter(`node[rank > ${threshold}]`)
      cy.remove(node2remove);

    });
}

function init_callbacks(){
    init_cy();
    init_slider();
}

// When the page is load we add our customized JS code on it to extend functions
// window.addEventListener('load', (event) => {
    
// });

init_callbacks()
*/
/**
 * This example aims at showcasing sigma's performances.
 */
/*
 import Sigma from "sigma";
 import Graph from "graphology";
 import seedrandom from "seedrandom";
 
 import EdgesDefaultProgram from "sigma/rendering/webgl/programs/edge";
 import EdgesFastProgram from "sigma/rendering/webgl/programs/edge.fast";
 
 import circlepack from "graphology-layout/circlepack";
 import clusters from "graphology-generators/random/clusters";
 import FA2Layout from "graphology-layout-forceatlas2/worker";
 import forceAtlas2 from "graphology-layout-forceatlas2";
 
 const rng = seedrandom("sigma");
 
 // 1. Read query string, and set form values accordingly:
 const query = new URLSearchParams(location.search).entries();
 for (const [key, value] of query) {
   const domList = document.getElementsByName(key);
   if (domList.length === 1) {
     (domList[0] ).value = value;
   } else if (domList.length > 1) {
     domList.forEach((dom) => {
       const input = dom ;
       input.checked = input.value === value;
     });
   }
 }
 
 // 2. Read form values to build a full state:
 const state = {
   order: +document.querySelector<HTMLInputElement>("#order")?.value,
   size: +document.querySelector<HTMLInputElement>("#size")?.value,
   clusters: +document.querySelector<HTMLInputElement>("#clusters")?.value,
   edgesRenderer: document.querySelector<HTMLInputElement>('[name="edges-renderer"]:checked')?.value,
 };
 
 // 3. Generate a graph:
 const graph = clusters(Graph, { ...state, rng });
 circlepack.assign(graph, {
   hierarchyAttributes: ["cluster"],
 });
 const colors= {};
 for (let i = 0; i < +state.clusters; i++) {
   colors[i] = "#" + Math.floor(rng() * 16777215).toString(16);
 }
 let i = 0;
 graph.forEachNode((node, { cluster }) => {
   graph.mergeNodeAttributes(node, {
     size: graph.degree(node) / 3,
     label: `Node n°${++i}, in cluster n°${cluster}`,
     color: colors[cluster + ""],
   });
 });
 
 // 4. Render the graph:
 const container = document.getElementById("sigma-container");
 const renderer = new Sigma(graph, container, {
   defaultEdgeColor: "#e6e6e6",
   defaultEdgeType: state.edgesRenderer,
   edgeProgramClasses: {
     "edges-default": EdgesDefaultProgram,
     "edges-fast": EdgesFastProgram,
   },
 });
 
 // 5. Enable FA2 button:
 const fa2Button = document.getElementById("fa2");
 const sensibleSettings = forceAtlas2.inferSettings(graph);
 const fa2Layout = new FA2Layout(graph, {
   settings: sensibleSettings,
 });
 function toggleFA2Layout() {
   if (fa2Layout.isRunning()) {
     fa2Layout.stop();
     fa2Button.innerHTML = `Start layout ▶`;
   } else {
     fa2Layout.start();
     fa2Button.innerHTML = `Stop layout ⏸`;
   }
 }
 fa2Button.addEventListener("click", toggleFA2Layout);
 
 // Cheap trick: tilt the camera a bit to make labels more readable:
 renderer.getCamera().setState({
   angle: 0.2,
 });
 */