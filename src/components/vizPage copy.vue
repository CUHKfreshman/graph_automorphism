<template>
  <v-container
    fluid
    class="ma-0"
    style="height: 100vh; overflow: hidden"
    no-padding
  >
    <!--draggable tool bar-->
    <v-card
      class="d-flex flex-column flex-nowrap position-absolute bg-light user-select-none overflow-y-hidden w-auto"
      style="left=50%; z-index:10;cursor: pointer; max-height:50vh;"
    >
      <v-card-title ref="draggableDiv">
        <v-icon large>mdi-drag-horizontal</v-icon>
      </v-card-title>
      <v-tabs
        v-model="toolbarOverallTab"
        class="w-100"
        style="min-height: 10vh"
      >
        <v-tab value="basic">Basic</v-tab>
        <v-tab value="AutoTree">AutoTree</v-tab>
        <v-tab value="SSM">SSM</v-tab>
        <v-tab value="IM">IM</v-tab>
        <v-tab value="layout">Layout</v-tab>
      </v-tabs>
      <v-card-text class="overflow-y-auto">
        <v-window v-model="toolbarOverallTab">
          <v-window-item value="basic">
            <v-btn
              ref="MetricsReportBtn"
              realCol="1"
              realRow="1"
              color="primary"
              >Metrics Report</v-btn
            >
            <v-btn ref="DegreeDistBtn" realCol="1" realRow="1" color="primary"
              >Degree Distribution</v-btn
            >
          </v-window-item>
          <v-window-item value="AutoTree"> at</v-window-item>
          <v-window-item value="SSM"> ss</v-window-item>
          <v-window-item value="IM">im </v-window-item>
          <v-window-item value="layout">
            <v-card>
              <v-card-text>
                <div class="text-caption">Repulsion</div>
                <v-slider
                  min="0"
                  max="2"
                  step="0.05"
                  v-model="origFullgraphConfig.simulation.repulsion"
                  thumb-label
                ></v-slider>

                <div class="text-caption">Repulsion Theta</div>
                <v-slider
                  min="0.3"
                  max="2"
                  step="0.05"
                  v-model="origFullgraphConfig.simulation.repulsionTheta"
                  thumb-label
                ></v-slider>
                <!--
                  <div class="text-caption">Repulsion Quadtree Levels</div>
                  <v-slider min="5" max="12" step="1" v-model="origFullgraphConfig.simulation.repulsionQuadtreeLevels" thumb-label></v-slider>
                  -->
                <div class="text-caption">Link Spring</div>
                <v-slider
                  min="0"
                  max="2"
                  step="0.05"
                  v-model="origFullgraphConfig.simulation.linkSpring"
                  thumb-label
                ></v-slider>

                <div class="text-caption">Link Distance</div>
                <v-slider
                  min="1"
                  max="20"
                  step="0.5"
                  v-model="origFullgraphConfig.simulation.linkDistance"
                  thumb-label
                ></v-slider>

                <div class="text-caption">
                  Link Distance Random Variation Range
                </div>
                <v-range-slider
                  v-model="
                    origFullgraphConfig.simulation.linkDistRandomVariationRange
                  "
                  min="0.8"
                  max="2.0"
                  step="0.05"
                  thumb-label
                ></v-range-slider>

                <div class="text-caption">Gravity</div>
                <v-slider
                  min="0"
                  max="1"
                  step="0.01"
                  v-model="origFullgraphConfig.simulation.gravity"
                  thumb-label
                ></v-slider>

                <div class="text-caption">Center</div>
                <v-slider
                  min="0"
                  max="1"
                  step="0.01"
                  v-model="origFullgraphConfig.simulation.center"
                  thumb-label
                ></v-slider>

                <div class="text-caption">Friction</div>
                <v-slider
                  min="0.8"
                  max="1"
                  step="0.01"
                  v-model="origFullgraphConfig.simulation.friction"
                  thumb-label
                ></v-slider>

                <div class="text-caption">Decay</div>
                <v-slider
                  min="100"
                  max="10000"
                  step="100"
                  v-model="origFullgraphConfig.simulation.decay"
                  thumb-label
                ></v-slider>

                <div class="text-caption">Repulsion From Mouse</div>
                <v-slider
                  min="0"
                  max="5"
                  step="0.1"
                  v-model="origFullgraphConfig.simulation.repulsionFromMouse"
                  thumb-label
                ></v-slider>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>
    <div
      ref="draggingElement"
      draggable="true"
      style="display: none; position: fixed; z-index: 100; top: 0"
    >
      <v-icon size="2rem">mdi-plus</v-icon>
    </div>
    <v-container
      fluid
      class="pa-0 mt-0 h-100 d-flex flex-sm-nowrap align-center justify-center h-100"
    >
      <v-row class="w-100 h-100 flex-sm-nowrap">
        <v-col
          :cols="expandFullGraph ? 12 : 6"
          class="pa-1 h-100 expand-transition"
          ref="fullgraphExtendableDiv"
        >
          <v-card
            class="h-100 border-secondary"
            style="overflow: hidden; border-width: 0.1rem !important"
          >
            <div class="h-100 w-100" ref="origFullgraphContainer">
              <canvas ref="origFullgraphCanvas" class="h-100 w-100" />
              <v-btn
                icon
                class="position-absolute top-50 translate-middle"
                style="left: 97%; z-index: 9; width: 1rem; min-height: 1rem"
                @click="expandFullGraph = !expandFullGraph"
              >
                <v-icon
                  :class="
                    expandFullGraph
                      ? 'mdi-chevron-double-left'
                      : 'mdi-chevron-double-right'
                  "
                  style="font-size: 1rem"
                ></v-icon>
              </v-btn>
            </div>
          </v-card>
        </v-col>
        <v-col
          cols="6"
          :v-show="!expandFullGraph"
          class="pa-1 d-flex flex-row justify-content-evenly align-items-center"
          ref="editableAreaContainer"
        >
          <div
            class="h-100 w-100 p-0 m-0 rounded d-flex flex-column justify-content-evenly align-items-center"
          >
            <div
              class="h-50 w-100 p-1 rounded d-flex flex-column justify-content-evenly align-items-center"
              style="border: 0.1rem #6c757d dashed"
            >
              <v-card
                class="h-100 border-3 p-0 overflow-hidden"
                style="height: 95.5vh"
              >
                <v-card-title class="text-center">Metrics Report</v-card-title>
                <v-card-text
                  class="p-0 h-100 d-flex flex-column align-items-center justify-content-center justify-content-lg-start"
                >
                  <v-table class="mb-0">
                    <tbody>
                      <tr>
                        <td class="border-1 border-end">Nodes</td>
                        <td id="nodenum"></td>
                      </tr>
                      <tr>
                        <td class="border-1 border-end">Edges</td>
                        <td id="edgenum"></td>
                      </tr>
                      <tr>
                        <td class="border-1 border-end">Avg Degree</td>
                        <td id="avg-deg"></td>
                      </tr>
                      <tr>
                        <td class="border-1 border-end">Max Degree</td>
                        <td id="max-deg"></td>
                      </tr>
                      <tr>
                        <td class="border-1 border-end">Density</td>
                        <td id="density"></td>
                      </tr>
                      <tr>
                        <td class="border-1 border-end">Node ID</td>
                        <td id="node-id"></td>
                      </tr>
                      <tr>
                        <td
                          class="border-1 border-end text-nowrap"
                          style="width: 32%"
                        >
                          Degree Centrality
                        </td>
                        <td id="degreeCentrality"></td>
                      </tr>
                      <tr>
                        <td class="border-1 border-end">Pagerank</td>
                        <td id="pagerank"></td>
                      </tr>
                    </tbody>
                  </v-table>
                  <v-card
                    class="h-50 w-100 flex-fill border-0"
                    style="border-radius: 0"
                  >
                    <v-card-title
                      class="text-center border-1"
                      style="border-radius: 0"
                      >Degree Distribution</v-card-title
                    >
                    <v-card-text class="p-0 m-0">
                      <div
                        class="container-fluid p-0 m-0 w-100 h-100"
                        id="degree-distribution"
                      ></div>
                    </v-card-text>
                  </v-card>
                </v-card-text>
              </v-card>
            </div>
            <div
              class="h-50 w-100 p-1 mt-1 rounded d-flex flex-column justify-content-evenly align-items-center"
              style="border: 0.1rem #6c757d dashed"
            >
              <v-icon size="3rem" color="#6c757d"
                >mdi-plus-circle-outline</v-icon
              >
            </div>
          </div>
          <div
            class="h-100 w-100 p-0 m-0 ms-1 rounded d-flex flex-column justify-content-evenly align-items-center"
          >
            <div
              class="h-50 w-100 p-1 rounded d-flex flex-column justify-content-evenly align-items-center"
              style="border: 0.1rem #6c757d dashed"
            >
              <v-icon size="3rem" color="#6c757d"
                >mdi-plus-circle-outline</v-icon
              >
            </div>
            <div
              class="h-50 w-100 p-1 mt-1 rounded d-flex flex-column justify-content-evenly align-items-center"
              style="border: 0.1rem #6c757d dashed"
            >
              <v-icon size="3rem" color="#6c757d"
                >mdi-plus-circle-outline</v-icon
              >
            </div>
          </div>
          <div
            class="card position-absolute bg-dark"
            :class="demoDivClass"
            :style="demoDivStyle"
            ref="demo-div"
            v-if="showDemoDiv"
          ></div>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>
<script setup>
import { ref, onMounted, nextTick, reactive, watch } from "vue";
import { Graph } from "@cosmograph/cosmos";

const props = defineProps({
  nodelist: Array,
  edgelist: Array,
});
// toolbar tab related
const toolbarOverallTab = ref("basic");
// layout options
const origFullgraphConfig = reactive({
  nodeColor: "#4B5BBF",
  simulation: {
    repulsion: 1,
    repulsionTheta: 1,
    //repulsionQuadtreeLevels: 9,
    linkSpring: 0.3,
    linkDistance: 5,
    linkDistRandomVariationRange: [1, 1.5],
    gravity: 0.5,
    center: 0.5,
    friction: 0.9,
    decay: 10000,
    repulsionFromMouse: 2,
  },
});
var origFullgraph;
// frontend effects related
const expandFullGraph = ref(false);
const buttonDragging = ref(false);
//const btnNameList = ref(["MetricsReportBtn", "DegreeDistBtn"]);
//const btnRealCol = ref(0);
//const btnRealRow = ref(0);
const showDemoDiv = ref(false);
const demoDivStyle = ref({});
const demoDivClass = ref("");
//const isMouseInsideArea = ref(false);
// ref of dom elements for orig fullgraph
const origFullgraphCanvas = ref(null);
const origFullgraphContainer = ref(null);
const draggingElement = ref(null);
const fullgraphExtendableDiv = ref(null);
// ref dom elements for draggable div
// the value of ref is different in this case. It is the proxy of dom, so we need $el to get the real dom
const draggableDiv = ref(null);
// functions
// a helper function to show effects when drag toolbar
const makeToolBarDraggable = () => {
  let draggableDivParent = draggableDiv.value.$el.parentElement; // parent div that contains the draggable div: the real toolbar
  //Draggable Div
  //TODO: add Y axis dragging. When Y change, make it vertical
  // Initialize some variables
  let draggingDiv = false; // Whether the div is being dragged or not
  let mouseX, mouseY; // The mouse position relative to the document
  let offsetX, offsetY; // The offset of the div relative to the mouse
  //console.log(draggableDiv.value.$el);
  // Add a mousedown event listener to the div
  draggableDiv.value.$el.addEventListener("mousedown", function (e) {
    if (!buttonDragging.value) {
      //if not dragging button, then drag container
      // Set dragging to true
      console.log(
        "dragging toolbar with buttonDragging=",
        buttonDragging.value
      );
      draggingDiv = true;

      // Get the mouse position
      mouseX = e.clientX;
      mouseY = e.clientY;

      // Get the offset of the div
      offsetX = draggableDivParent.offsetLeft;
      offsetY = draggableDivParent.offsetTop;
    }
  });

  // Add a mousemove event listener to the document
  document.addEventListener("mousemove", function (e) {
    // If dragging is true
    if (draggingDiv) {
      // Calculate the new position of the div
      let newX = e.clientX - mouseX + offsetX;
      let newY = e.clientY - mouseY + offsetY;

      // Set the div's offset to the new position
      draggableDivParent.style.left = newX + "px";
      draggableDivParent.style.top = newY + "px";
    }
  });

  // Add a mouseup event listener to the document
  document.addEventListener("mouseup", function () {
    // Set dragging to false
    draggingDiv = false;
  });
};

// a helper function to show effects when click buttons in toolbar, currently not used
/*
const makeButtonDraggable = (refName) => {
    let btn = context.refs[refName];
    let dragging = false;
    let mouseX, mouseY, offsetX, offsetY;

    btn.addEventListener("click", startDragging);
    // dragging
    const startDragging = (e) => {
        e.preventDefault();
        buttonDragging.value = true;
        // update real col and row
        btnRealCol.value = btn.getAttribute("realCol");
        btnRealRow.value = btn.getAttribute("realRow");
        console.log("start dragging button", refName, "with realCol=", btnRealCol.value, "and realRow=", btnRealRow.value)
        dragging = true;
        btn.classList.add("disabled");
        mouseX = e.clientX;
        mouseY = e.clientY;
        offsetX = btn.offsetLeft;
        offsetY = btn.offsetTop;

        document.addEventListener("mousemove", handleMouseMove);
        document.addEventListener("mouseup", stopDragging);
    }
    // handle mouse move
    const handleMouseMove = (e) => {
        if (dragging) {
            document.body.style.cursor = "none";
            draggingElement.value.style.display = "block";
            draggingElement.value.style.left = e.clientX - (draggingElement.value.offsetWidth / 2) + "px";
            draggingElement.value.style.top = e.clientY - (draggingElement.value.offsetHeight / 2) + "px";
        }
    }

    const stopDragging = (e) => {
        buttonDragging.value = false;
        dragging = false;
        btn.classList.remove("disabled");
        draggingElement.value.style.display = "none";
        draggingElement.value.style.left = 0;
        draggingElement.value.style.top = 0;
        document.body.style.cursor = "auto";

        document.removeEventListener("mousemove", handleMouseMove);
        document.removeEventListener("mouseup", stopDragging);
    }
};*/

// create full graph
// reactive orig fullgraph
//function
const origFullgraphCreate = () => {
  const degreeToColorHex = (degree, minDegree, maxDegree) => {
    const lerp = (a, b, t) => a + (b - a) * t;
    const revlerp = (a, b, t) => b - (b - a) * t;
    //#226fFF to #ff46b3
    const color_lr = ["#226fFF", "#ff46b3"];
    let r_lr = [];
    let g_lr = [];
    let b_lr = [];

    color_lr.forEach((color) => {
      r_lr.push(parseInt(color.slice(1, 3), 16));
      g_lr.push(parseInt(color.slice(3, 5), 16));
      b_lr.push(parseInt(color.slice(5, 7), 16));
    });

    const linearT = (degree - minDegree) / (maxDegree - minDegree);
    const t = Math.sqrt(linearT);
    const r = Math.round(lerp(r_lr[0], r_lr[1], t));
    const g = Math.round(revlerp(g_lr[0], g_lr[1], t));
    const b = Math.round(revlerp(b_lr[0], b_lr[1], t));
    return "#" + r.toString(16) + g.toString(16) + b.toString(16);
  };

  console.log("creating full graph");
  const initconfig = {
    //backgroundColor: "#FFFFFF",
    nodeSize: 4,
    nodeColor: "#4B5BBF",
    nodeGreyoutOpacity: 0.1,
    linkWidth: 0.1,
    linkColor: "#5F74C2",
    linkArrows: false,
    linkGreyoutOpacity: 0,
    simulation: {
      linkDistance: 1,
      linkSpring: 0.3,
      repulsion: 1,
      gravity: 0.25,
      friction: 0.85,
    },
    events: {
      //node, i, pos, event
      onClick: (node, i) => {
        if (node && i !== undefined) {
          origFullgraph.selectNodeByIndex(i);
          origFullgraph.zoomToNodeByIndex(i);
        } else {
          origFullgraph.unselectNodes();
        }
        console.log("Clicked node: ", node);
      },
    },
  };
  // create graph
  origFullgraph = new Graph(origFullgraphCanvas.value, initconfig);
  console.log("Init graph...");
  console.log(origFullgraph);
  //For testing
  //let tmpnode = [{ 'id': '0' }, { 'id': '1' }];
  //let tmpedge = [{ 'source': '0', 'target': '1' }];
  origFullgraph.setData(props.nodelist, props.edgelist);
  // render by degree initially
  const degreeArray = origFullgraph.graph.degree;
  console.log(degreeArray);
  const minDegree = Math.min(...degreeArray);
  const maxDegree = Math.max(...degreeArray);
  origFullgraphConfig.nodeColor = (node) => {
    return degreeToColorHex(
      degreeArray[parseInt(node.id)],
      minDegree,
      maxDegree
    );
  };

  //origFullgraph.zoom(0.9);
  origFullgraph.fitView();
};

// watch for changes in full graph config
watch(
  origFullgraphConfig,
  () => {
    console.log("origFullgraphConfig changed");
    origFullgraph.setConfig(origFullgraphConfig);
    origFullgraph.start();
    //origFullgraph.fitView();
  },
  { deep: true }
);
// toggle width 50%/100% of full graph container
/*
const expandFullGraphDiv = () => {
    fullgraphExtendableDiv.value.classList.toggle('w-50');
    fullgraphExtendableDiv.value.classList.toggle('w-100');
};*/

onMounted(async () => {
  await nextTick();
  //console.log(origFullgraphContainer.value);
  // create full graph
  if (origFullgraphContainer.value.clientWidth) {
    origFullgraphCreate();
  }
  makeToolBarDraggable();
  // make buttons draggable
  /*
    btnNameList.value.forEach(refName => {
        makeButtonDraggable(refName);
    });*/
});

//watch(origFullgraph, () => {
//    // Add any watchers needed for origFullgraph
//});
/*
return {
    expandFullGraph,
    buttonDragging,
    btnNameList,
    btnRealCol,
    btnRealRow,
    showDemoDiv,
    demoDivStyle,
    demoDivClass,
    isMouseInsideArea,
    origFullgraph,
    origFullgraphCanvas,
    origFullgraphContainer,
    draggingElement,
    fullgraphExtendableDiv,
    draggableDiv,
    expandFullGraphDiv,
    origFullgraphCreate,
    makeToolBarDraggable,
    makeButtonDraggable
};
*/
</script>

<style scoped>
/* transition for expanding full graph */
.expand-transition {
  transition: all 0.2s ease;
}

.rotate {
  transform: rotate(180deg) translateY(-50%);
}

.rotate-icon {
  transform: translateY(-50%);
  transition: transform 1s ease;
}

/* width */
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
