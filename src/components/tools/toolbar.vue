<template>
  <!--draggable tool bar-->
  <v-card
    class="d-flex flex-column flex-nowrap position-absolute bg-light user-select-none overflow-y-hidden w-auto"
    style="left=50%; z-index:10;cursor: pointer; max-height:50vh;"
  >
    <v-card-title ref="draggableDiv">
      <v-icon large>mdi-drag-horizontal</v-icon>
    </v-card-title>
    <v-tabs v-model="toolbarOverallTab" class="w-100" style="min-height: 10vh">
      <v-tab value="basic">Basic</v-tab>
      <v-tab value="AutoTree">AutoTree</v-tab>
      <v-tab value="SSM">SSM</v-tab>
      <v-tab value="IM">IM</v-tab>
      <v-tab value="layout">Layout</v-tab>
    </v-tabs>
    <v-card-text class="overflow-y-auto">
      <v-window v-model="toolbarOverallTab">
        <v-window-item value="basic">
          <v-btn ref="MetricsReportBtn" realCol="1" realRow="1" color="primary"
            >Metrics Report</v-btn
          >
          <v-btn ref="DegreeDistBtn" realCol="1" realRow="1" color="primary"
            >Degree Distribution</v-btn
          >
          <v-btn ref="ssmRenderBtn" realCol="1" realRow="1" color="primary" @click="origFullgraphStore.ssmColormapRender"
            >SSM</v-btn
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
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation.repulsion
                "
                thumb-label
              ></v-slider>

              <div class="text-caption">Repulsion Theta</div>
              <v-slider
                min="0.3"
                max="2"
                step="0.05"
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation
                    .repulsionTheta
                "
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
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation.linkSpring
                "
                thumb-label
              ></v-slider>

              <div class="text-caption">Link Distance</div>
              <v-slider
                min="1"
                max="20"
                step="0.5"
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation.linkDistance
                "
                thumb-label
              ></v-slider>

              <div class="text-caption">
                Link Distance Random Variation Range
              </div>
              <v-range-slider
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation
                    .linkDistRandomVariationRange
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
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation.gravity
                "
                thumb-label
              ></v-slider>

              <div class="text-caption">Center</div>
              <v-slider
                min="0"
                max="1"
                step="0.01"
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation.center
                "
                thumb-label
              ></v-slider>

              <div class="text-caption">Friction</div>
              <v-slider
                min="0.8"
                max="1"
                step="0.01"
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation.friction
                "
                thumb-label
              ></v-slider>

              <div class="text-caption">Decay</div>
              <v-slider
                min="100"
                max="10000"
                step="100"
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation.decay
                "
                thumb-label
              ></v-slider>

              <div class="text-caption">Repulsion From Mouse</div>
              <v-slider
                min="0"
                max="5"
                step="0.1"
                v-model="
                  origFullgraphStore.origFullgraphConfig.simulation
                    .repulsionFromMouse
                "
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
</template>
<script setup>
import { ref, onMounted, watch } from "vue";
import { useOrigFullgraphStore } from "@/store/app.ts";
const origFullgraphStore = useOrigFullgraphStore();
const toolbarOverallTab = ref("basic");
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
watch(origFullgraphStore.ssm_all_dict, () => {});
onMounted(() => {
  makeToolBarDraggable();
});
</script>
