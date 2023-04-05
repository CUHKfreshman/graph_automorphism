<template>
  <v-container
    fluid
    class="ma-0"
    style="height: 100vh; overflow: hidden"
    no-padding
  >
    <toolbar />
    <v-container
      fluid
      class="pa-0 mt-0 h-100 d-flex flex-sm-nowrap align-center justify-center h-100"
    >
      <v-row class="w-100 h-100 flex-sm-nowrap">
        <v-col
          :cols="origFullgraphStore.expandFullgraph ? 12 : 6"
          class="pa-1 h-100 expand-transition"
          ref="fullgraphExtendableDiv"
        >
          <v-card
            class="h-100 border-secondary"
            style="overflow: hidden; border-width: 0.1rem !important"
          >
            <origFullgraphComponent />
          </v-card>
        </v-col>
        <v-col
          cols="6"
          :v-show="!origFullgraphStore.expandFullgraph"
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
import { ref, onMounted } from "vue";
import toolbar from "./tools/toolbar.vue";
import origFullgraphComponent from "./graphs/origFullgraphComponent.vue";
import { useOrigFullgraphStore } from "@/store/app.ts";
const origFullgraphStore = useOrigFullgraphStore();
// frontend effects related
const fullgraphExtendableDiv = ref(null);
//const btnNameList = ref(["MetricsReportBtn", "DegreeDistBtn"]);
//const btnRealCol = ref(0);
//const btnRealRow = ref(0);
const showDemoDiv = ref(false);
const demoDivStyle = ref({});
const demoDivClass = ref("");
//const isMouseInsideArea = ref(false);

// toggle width 50%/100% of full graph container
/*
const expandFullgraphDiv = () => {
    fullgraphExtendableDiv.value.classList.toggle('w-50');
    fullgraphExtendableDiv.value.classList.toggle('w-100');
};*/

onMounted(() => {
  //console.log(origFullgraphContainer.value);
  // create full graph
  // make buttons draggable
  /*
    btnNameList.value.forEach(refName => {
        makeButtonDraggable(refName);
    });*/
});
</script>

<style scoped>
/* transition for expanding full graph */
.expand-transition {
  transition: all 0.1s ease;
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
