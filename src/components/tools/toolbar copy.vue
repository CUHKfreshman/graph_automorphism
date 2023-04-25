<template>
  <!--draggable tool bar-->
  <v-card
    class="d-flex flex-column flex-nowrap position-absolute bg-light user-select-none overflow-y-hidden"
    style="left=50%; z-index:10;cursor: pointer; max-height:90vh; max-width: 50vh"
    :class="[collapsed ? 'rounded-0  bg-grey-darken-2' : 'bg-light']"
  >
    <v-card-title
      ref="draggableDiv"
      :style="{ width: titleWidth }"
      class="pa-1"
    >
      <v-tooltip v-model="showRightClickTooltip" location="right">
        <template v-slot:activator="{ props }">
          <v-btn
            icon="mdi-drag-horizontal"
            variant="plain"
            v-bind="props"
            class="rounded-0"
            :class="[collapsed ? ' rounded-0 rounded-be-xl' : '']"
            @contextmenu="handleRightClick"
          >
          </v-btn>
        </template>
        <span>Right Click to Collapse/Expand</span>
      </v-tooltip>
    </v-card-title>
    <v-fade-transition>
      <v-card-text class="overflow-y-auto pa-1" v-show="!collapsed">
        <v-expansion-panels variant="accordion">
          <v-expansion-panel>
            <v-expansion-panel-title>Windows</v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-form v-model="valid">
                <v-container class="pa-0">
                  <v-select
                    :items="windowNameList"
                    v-model="windowSelected"
                    label="Select Window"
                    hide-details
                    class="mb-2"
                  ></v-select>
                  <v-row>
                    <v-col cols="12" sm="6" class="pr-1">
                      <v-select
                        :items="[1, 2]"
                        v-model="colWidthSelected"
                        label="Column Width"
                        hide-details
                      ></v-select>
                    </v-col>

                    <v-col cols="12" sm="6" class="pl-1">
                      <v-select
                        :items="[1, 2]"
                        v-model="rowHeightSelected"
                        label="Row Height"
                        hide-details
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>
              <v-row>
                <v-col class="pr-1">
                  <v-btn
                    color="success"
                    class="w-50"
                    realCol="1"
                    realRow="1"
                    block
                    @click="addComponentEmit()"
                    >Add</v-btn
                  ></v-col
                >
                <v-col class="pl-1">
                  <v-btn
                    color="red"
                    class="w-50"
                    realCol="1"
                    realRow="1"
                    block
                    @click="removeComponentEmit()"
                    >Delete</v-btn
                  ></v-col
                >
              </v-row>
              <v-snackbar v-model="hasWindowSnackbar">
                Window already added!

                <template v-slot:actions>
                  <v-btn
                    color="pink"
                    variant="text"
                    @click="hasWindowSnackbar = false"
                  >
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
              <v-snackbar v-model="noWindowSnackbar">
                Window does not exist!

                <template v-slot:actions>
                  <v-btn
                    color="pink"
                    variant="text"
                    @click="noWindowSnackbar = false"
                  >
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>Basic</v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-btn
                ref="origRenderBtn"
                color="primary"
                block
                @click="renderOrigColormap"
                append-icon="mdi-palette"
                >Render Basic</v-btn
              ></v-expansion-panel-text
            >
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>K Neighbor</v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-text-field
                label="Input K Value"
                v-model="kNeighborStore.kValue"
                class="mt-2"
                hide-details
              >
                <template v-slot:append>
                  <v-icon icon="mdi-plus" color="green" @click="addKValue">
                  </v-icon>
                </template>
                <template v-slot:prepend>
                  <v-icon icon="mdi-minus" color="red" @click="minusKValue">
                  </v-icon>
                </template>
              </v-text-field>
              <v-snackbar v-model="kNeighborValueSnackbar">
                K value must be positive!

                <template v-slot:actions>
                  <v-btn
                    color="pink"
                    variant="text"
                    @click="kNeighborValueSnackbar = false"
                  >
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>AutoTree</v-expansion-panel-title>
            <v-expansion-panel-text
              ><v-btn
                ref="atRenderBtn"
                realCol="1"
                realRow="1"
                color="secondary"
                block
                @click="createATGraph"
                append-icon="mdi-graph-outline"
                >Generate AutoTree</v-btn
              >
              <v-snackbar v-model="autoTreeSnackbar">
                AutoTree window has not been initialized!

                <template v-slot:actions>
                  <v-btn
                    color="pink"
                    variant="text"
                    @click="autoTreeSnackbar = false"
                  >
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>SSM</v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-btn
                ref="ssmRenderBtn"
                realCol="1"
                realRow="1"
                color="primary"
                block
                @click="renderSSMColormap"
                append-icon="mdi-palette"
                >Render SSM</v-btn
              ></v-expansion-panel-text
            >
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>IM</v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-expansion-panels variant="accordion">
                <v-btn
                  ref="imRenderBtn"
                  color="primary"
                  block
                  @click="renderIMColormap"
                  append-icon="mdi-palette"
                  >Render IM</v-btn
                >
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    Customized Rendering
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-form @submit.prevent="customizedIMSubmit">
                      <v-combobox
                        v-model="selectedNodesForIM"
                        multiple
                        chips
                        clearable
                        label="Choose Nodes (input twice for deletion)"
                        hide-details
                      ></v-combobox>
                      <v-text-field
                        append-icon="mdi-percent-outline"
                        label="Spread Probability (%)"
                        v-model="spreadProbability"
                        type="number"
                      ></v-text-field>
                      <v-btn
                        type="submit"
                        block
                        class="mt-2"
                        append-icon="mdi-send"
                        >Submit</v-btn
                      >
                      <v-checkbox
                        label="Use Original Graph"
                        v-model="customizedIMStore.useOrig"
                      ></v-checkbox>
                      <v-btn
                        ref="customizedIMRenderBtn"
                        color="success"
                        block
                        @click="renderCustomizedIMColormap"
                        :loading="!customizedIMStore.hasReceived"
                        :disabled="!customizedIMStore.hasReceived"
                        append-icon="mdi-palette"
                        >Customized Render</v-btn
                      >
                    </v-form>
                    <v-row
                      ><v-col sm="6" class="pr-1"> </v-col
                      ><v-col sm="6" class="pl-1"></v-col
                    ></v-row>
                    <v-snackbar v-model="selectedNodesForIMFallbackSnackbar">
                      Invalid Input for Customized IM!

                      <template v-slot:actions>
                        <v-btn
                          color="pink"
                          variant="text"
                          @click="selectedNodesForIMFallbackSnackbar = false"
                        >
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                    <v-snackbar v-model="customizedIMSnackbar">
                      Customized IM window has not been initialized!

                      <template v-slot:actions>
                        <v-btn
                          color="pink"
                          variant="text"
                          @click="customizedIMSnackbar = false"
                        >
                          Close
                        </v-btn>
                      </template>
                    </v-snackbar>
                  </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    Stepped Visualization
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-btn
                      ref="imRenderBtn"
                      realCol="1"
                      realRow="1"
                      block
                      color="primary"
                      append-icon="mdi-palette-swatch-variant"
                      @click="
                        randomColorGenerator();
                      "
                      >Random Color</v-btn
                    >
                    <v-row>
                      <v-checkbox
                      v-model="selectedIMGraph"
                      label="Original"
                      value="Original"
                    ></v-checkbox>
                    <v-checkbox
                      v-model="selectedIMGraph"
                      label="Competitor"
                      value="Competitor"
                    ></v-checkbox>
                    </v-row>
                    <v-col
                      class="d-flex flex-column justify-center align-start"
                    >
                      <v-row
                        v-for="(
                          color, round
                        ) in currentimRoundColorDict"
                        :key="round"
                        :style="{ color: color }"
                        class="w-100"
                      >
                        <v-col col="12" sm="8" class="pa-0"><v-switch
                          v-model="showRounds[round]"
                          :label="'Round ' + round"
                          :color="color"
                          hide-details
                          inset
                          @change="showRoundHandler(round)"
                        ></v-switch></v-col>
                        <v-col
                        col="12" sm="2" class="pa-0"><p > {{origFullGraphStore.imDistributionDict[round]}}</p></v-col>
                        <v-col col="12" sm="2" class="pa-0"><p  v-if="customizedIMStore.imDistributionDict !== null">
                          {{customizedIMStore.imDistributionDict[round]}}
                        </p></v-col>


                      </v-row>
                      <v-row class="w-100">
                        <v-col col="12" sm="8" class="pa-0">

                        </v-col>
                        <v-col col="12" sm="2" class="pa-0">{{Object.values(origFullGraphStore.imDistributionDict).reduce((a, b) => a + b, 0)}}</v-col>
                        <v-col col="12" sm="2" class="pa-0">{{Object.values(customizedIMStore.imDistributionDict).reduce((a, b) => a + b, 0)}}</v-col>
                      </v-row>
                    </v-col>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-title>Layout</v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-select
                :items="configItems"
                v-model="configType"
                label="Select Config Type"
                prepend-icon="mdi-format-list-bulleted-type"
              ></v-select>
              <div class="text-caption">Repulsion</div>
              <v-slider
                min="0"
                max="2"
                step="0.05"
                v-model="interfaceConfig.simulation.repulsion"
                thumb-label
              ></v-slider>

              <div class="text-caption">Repulsion Theta</div>
              <v-slider
                min="0.3"
                max="2"
                step="0.05"
                v-model="interfaceConfig.simulation.repulsionTheta"
                thumb-label
              ></v-slider>
              <!--
                <div class="text-caption">Repulsion Quadtree Levels</div>
                <v-slider min="5" max="12" step="1" v-model="origFullGraphConfig.simulation.repulsionQuadtreeLevels" thumb-label></v-slider>
                -->
              <div class="text-caption">Link Spring</div>
              <v-slider
                min="0"
                max="2"
                step="0.05"
                v-model="interfaceConfig.simulation.linkSpring"
                thumb-label
              ></v-slider>

              <div class="text-caption">Link Distance</div>
              <v-slider
                min="1"
                max="20"
                step="0.5"
                v-model="interfaceConfig.simulation.linkDistance"
                thumb-label
              ></v-slider>

              <div class="text-caption">
                Link Distance Random Variation Range
              </div>
              <v-range-slider
                v-model="
                  interfaceConfig.simulation.linkDistRandomVariationRange
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
                v-model="interfaceConfig.simulation.gravity"
                thumb-label
              ></v-slider>

              <div class="text-caption">Center</div>
              <v-slider
                min="0"
                max="1"
                step="0.01"
                v-model="interfaceConfig.simulation.center"
                thumb-label
              ></v-slider>

              <div class="text-caption">Friction</div>
              <v-slider
                min="0.8"
                max="1"
                step="0.01"
                v-model="interfaceConfig.simulation.friction"
                thumb-label
              ></v-slider>

              <div class="text-caption">Decay</div>
              <v-slider
                min="100"
                max="10000"
                step="100"
                v-model="interfaceConfig.simulation.decay"
                thumb-label
              ></v-slider>

              <div class="text-caption">Repulsion From Mouse</div>
              <v-slider
                min="0"
                max="5"
                step="0.1"
                v-model="interfaceConfig.simulation.repulsionFromMouse"
                thumb-label
              ></v-slider>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels> </v-card-text
    ></v-fade-transition>
  </v-card>
  <div
    ref="draggingElement"
    draggable="true"
    style="display: none; position: fixed; z-index: 100; top: 0"
  >
    <v-icon icon="mdi-plus" size="2rem"></v-icon>
  </div>
</template>
<script setup>
import { ref, onMounted, watch, reactive, computed } from "vue";
import {
  useOrigFullGraphStore,
  useKNeighborStore,
  useAutoTreeStore,
  useCustomizedIMStore,
} from "@/store/store.js";
//handle collapse toolbar
const showRightClickTooltip = ref(false);
const collapsed = ref(false);
const handleRightClick = (event) => {
  event.preventDefault(); // Prevent the context menu from appearing
  console.log("Right-click or long-press detected!");
  collapsed.value = !collapsed.value;
};
const titleWidth = computed(() => (collapsed.value ? "auto" : "50vh"));
//// emits
const emit = defineEmits(["addComponent", "removeComponent"]);
const addComponentEmit = () => {
  const index = addedWindowNameList.value.indexOf(windowSelected.value);
  if (index > -1) {
    hasWindowSnackbar.value = true;
  } else {
    addedWindowNameList.value.push(windowSelected.value);
    emit(
      "addComponent",
      windowSelected.value,
      rowHeightSelected.value,
      colWidthSelected.value
    );
    if (windowSelected.value == "K-Neighbor") {
      origFullGraphStore.kNeighborEnabled = true;
    }
  }
};
const removeComponentEmit = () => {
  const index = addedWindowNameList.value.indexOf(windowSelected.value);
  if (index > -1) {
    addedWindowNameList.value.splice(index, 1);
    emit("removeComponent", windowSelected.value);
    if (windowSelected.value == "K-Neighbor") {
      origFullGraphStore.kNeighborEnabled = false;
    }
  } else {
    noWindowSnackbar.value = true;
  }
};
//// stores
const origFullGraphStore = useOrigFullGraphStore();
const autoTreeStore = useAutoTreeStore();
const kNeighborStore = useKNeighborStore();
const customizedIMStore = useCustomizedIMStore();
//// snackbars
const autoTreeSnackbar = ref(false);
const customizedIMSnackbar = ref(false);
const kNeighborValueSnackbar = ref(false);
const hasWindowSnackbar = ref(false);
const noWindowSnackbar = ref(false);
//// dragging
const draggingElement = ref(null);
const buttonDragging = ref(false);
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
//// window adder
const windowNameList = ref([
  "K-Neighbor",
  "AutoTree",
  "Metrics Report",
  "Degree Distribution",
  "Customized IM",
]);
const addedWindowNameList = ref([]);
const windowSelected = ref("K-Neighbor");
const rowHeightSelected = ref(1);
const colWidthSelected = ref(1);

//// config for layout target switch
const configType = ref("origFullGraph");
const configs = reactive({
  origFullGraph: origFullGraphStore.origFullGraphConfig,
  kNeighbor: kNeighborStore.kNeighborConfig,
  customizedIM: customizedIMStore.customizedIMConfig,
});
const configItems = ref(Object.keys(configs));

const interfaceConfig = computed(() => configs[configType.value]);
const isRenderColorMap = ref(false);
const renderOrigColormap = () => {
  isRenderColorMap.value = true;
  origFullGraphStore.origColormapRender();
};
const renderSSMColormap = () => {
  isRenderColorMap.value = true;
  origFullGraphStore.ssmColormapRender();
};
const renderIMColormap = () => {
  isRenderColorMap.value = true;
  origFullGraphStore.imColormapRender();
};
const renderCustomizedIMColormap = () => {
  //TODO: check if useOrig
  if (customizedIMStore.useOrig) {
    renderIMColormap();
    return;
  }
  const index = addedWindowNameList.value.indexOf("Customized IM");
  if (index > -1) {
    if (customizedIMStore.customizedIM === null) {
      customizedIMStore.customizedIMCreate();
    } else {
      isRenderColorMap.value = true;
      customizedIMStore.imColormapRender();
    }
  } else {
    customizedIMSnackbar.value = true;
  }
}; /*
watch(
  () => configType.value,
  (newValue) => {
    if (newValue == "kNeighbor") {
      // ... code to switch to kNeighborConfig
      console.log("switch to kNeighborConfig", newValue);
    } else {
      // ... code to switch toorigFullGraphConfig
      console.log("switch to origFullGraphConfig", newValue);
    }
  }
);*/
// watch for changes in full graph config
watch(
  () => origFullGraphStore.origFullGraphConfig,
  (newConfig) => {
    //console.log(origFullGraphConfig changed");
    //console.log(store.origFullGraph);
    configs.origFullGraph = origFullGraphStore.origFullGraphConfig;
    origFullGraphStore.origFullGraph.setConfig(newConfig);
    // if just render color, do not interrupt
    if (!isRenderColorMap.value) {
      origFullGraphStore.origFullGraph.start();
    } else {
      //update k neighbor if exist
      const index = addedWindowNameList.value.indexOf("K-Neighbor");
      if (index > -1) {
        kNeighborStore.kNeighborColorMapRender();
      }
    }
    isRenderColorMap.value = false;
    //OrigFullGraph.fitView();
  },
  { deep: true }
);
//// watch kNeighbor config
watch(
  () => kNeighborStore.kNeighborConfig,
  (newConfig) => {
    //console.log("kNeighborConfig changed", newConfig);
    configs.kNeighbor = kNeighborStore.kNeighborConfig;
    kNeighborStore.kNeighbor.setConfig(newConfig);
    if (!isRenderColorMap.value) {
      kNeighborStore.kNeighbor.start();
    }
    isRenderColorMap.value = false;
  },
  { deep: true }
);
//// watch customizedIM config
watch(
  () => customizedIMStore.customizedIMConfig,
  (newConfig) => {
    //console.log("customizedIMConfig changed", newConfig);
    configs.customizedIM = customizedIMStore.customizedIMConfig;
    customizedIMStore.customizedIM.setConfig(newConfig);
    if (!isRenderColorMap.value) {
      customizedIMStore.customizedIM.start();
    }
    isRenderColorMap.value = false;
  },
  { deep: true }
);
//// kNeighbor value adder
const addKValue = () => {
  kNeighborStore.kValue += 1;
};
const minusKValue = () => {
  if (kNeighborStore.kValue > 1) {
    kNeighborStore.kValue -= 1;
  } else {
    kNeighborValueSnackbar.value = true;
  }
};
//// autoTree graph creator
const createATGraph = () => {
  const index = addedWindowNameList.value.indexOf("AutoTree");
  if (index > -1) {
    autoTreeStore.autoTreeCreate();
  } else {
    autoTreeSnackbar.value = true;
  }
};
//// kneighbor k val watcher
watch(
  () => kNeighborStore.kValue, //TODOlno, use store instead. or solve the problem of new k
  (newVal) => {
    const index = addedWindowNameList.value.indexOf("K-Neighbor");
    if (index > -1) {
      kNeighborStore.kNeighborUpdate(newVal);
    }
  },
  { deep: true }
);

//// im round shower helper
const selectedIMGraph = ref(["Original"]);
const showRounds = ref({});
const showRoundHandler = (round, ) => {
  if(selectedIMGraph.value.includes("Original")){
    origFullGraphStore.imColormapRoundRender(round, showRounds.value[round]);
  }
  if(selectedIMGraph.value.includes("Competitor")){
    customizedIMStore.imColormapRoundRender(round, showRounds.value[round]);
  }

}
const randomColorGenerator = () => {
  if(addedWindowNameList.value.includes("Customized IM")){
    customizedIMStore.imColormapCreate(null, false, false);
  }
    origFullGraphStore.imColormapCreate(null, false, false);


}
const currentimRoundColorDict = computed(() => {
  const origDict = origFullGraphStore.imRoundColorDict;
  const customDict = customizedIMStore.imRoundColorDict;

  const getMaxKey = (dict) => Math.max(...Object.keys(dict).map(Number));
  const origMaxKey = getMaxKey(origDict);
  const customMaxKey = getMaxKey(customDict);
  console.log(origMaxKey, customMaxKey, customMaxKey > origMaxKey ? customDict : origDict)
  // Return the dictionary with the larger max key
  return customMaxKey > origMaxKey ? customDict : origDict;
});
watch(
  currentimRoundColorDict,
  (newDict) => {
    console.log("imRoundColorDict changed", newDict);
    for (const round in newDict) {
      if (!Object.prototype.hasOwnProperty.call(showRounds.value, round)) {
        showRounds.value[round] = false;
      }
    }
  },
  { deep: true }
);  console.log()
/// IM customized render
const selectedNodesForIM = ref([]);
const selectedNodesForIMFallbackSnackbar = ref(false);
const spreadProbability = ref(0.2);
//// check node validaty (rely on bug to perform input twice for deletion. Actually a tricky case but I don have the time to check logic)
watch(selectedNodesForIM, (newVal, oldVal) => {
  // if delete
  if (oldVal.length > newVal.length) {
    return;
  }
  const newNode = newVal[newVal.length - 1];
  let oldSize = oldVal.length;
  if (oldSize > 0) {
    if (oldVal.includes(newNode)) {
      alert("already selected", selectedNodesForIM.value);
      selectedNodesForIMFallbackSnackbar.value = true;
      selectedNodesForIM.value = oldVal;
      return;
    }
  }

  let found = false;
  // this method is for [1, 3, 4, 5] kind of array. if [1, 2, 3] then ok just check maximum
  for (let i = 0; i < origFullGraphStore.nodelist.length; i++) {
    const item = origFullGraphStore.nodelist[i];
    //console.log(item);
    if (item.id === newNode) {
      found = true;
      //alert('found');
      break;
    }
  }
  if (!found) {
    selectedNodesForIMFallbackSnackbar.value = true;
    selectedNodesForIM.value = oldVal;
  }
});
//// deal with server im result check
const customizedIMSubmit = async () => {
  customizedIMStore.hasReceived = false;
  if (selectedNodesForIM.value.length < 1 || spreadProbability.value <= 0) {
    selectedNodesForIMFallbackSnackbar.value = true;
    return;
  }
  const customizedIMResponse = await fetch(
    "http://localhost:4000/customizedIM",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nodes: selectedNodesForIM.value,
        spreadProbability: spreadProbability.value,
      }),
    }
  );
  console.log(
    "CustomizedIM server responded with ",
    customizedIMResponse.status
  );
};
onMounted(() => {
  makeToolBarDraggable();
});
</script>
<style scoped>
.collapsed {
  max-height: none !important;
  width: 64px !important;
}

.collapsed-icon {
  position: absolute;
  right: 0;
  top: 0;
  z-index: 11;
  cursor: pointer;
}

/* Set the width and height of the scrollbar */
::-webkit-scrollbar {
  width: 2px;
  height: 2px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 0;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
