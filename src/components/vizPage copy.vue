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
          :cols="origFullGraphStore.expandFullgraph ? 12 : 6"
          class="pa-1 h-100 expand-transition"
          ref="fullgraphExtendableDiv"
        >
          <v-card
            class="h-100 border-secondary"
            style="overflow: hidden; border-width: 0.1rem !important"
          >
            <origFullGraphComponent />
          </v-card>
        </v-col>
        <v-col
          cols="6"
          :v-show="!origFullGraphStore.expandFullgraph"
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
              <metricsReportComponent />
            </div>

            <div
              class="h-50 w-100 p-1 mt-1 rounded d-flex flex-column justify-content-evenly align-items-center"
              style="border: 0.1rem #6c757d dashed"
            >
              <kNeighborComponent />
            </div>

          </div>
          <div
            class="h-100 w-100 p-0 m-0 ms-1 rounded d-flex flex-column justify-content-evenly align-items-center"
          >

            <div
              class="h-50 w-100 p-1 rounded d-flex flex-column justify-content-evenly align-items-center"
              style="border: 0.1rem #6c757d dashed"
            >
              <autoTreeComponent />
            </div>

            <div
              class="h-50 w-100 p-1 mt-1 rounded d-flex flex-column justify-content-evenly align-items-center"
              style="border: 0.1rem #6c757d dashed"
            >
              <degreeDistComponent />
            </div>

          </div>

        </v-col>
      </v-row>
    </v-container>
  </v-container>

<!--<v-icon size="3rem" color="#6c757d"
                >mdi-plus-circle-outline</v-icon
              >-->
              <!--

          <div
            class="card position-absolute bg-dark"
            :class="demoDivClass"
            :style="demoDivStyle"
            ref="demo-div"
            v-if="showDemoDiv"
          ></div>-->

</template>
<script setup>
import { ref, onMounted } from "vue";
import toolbar from "./tools/toolbar.vue";
import metricsReportComponent from "./tools/metricsReportComponent.vue";
import origFullGraphComponent from "./graphs/origFullGraphComponent.vue";
import degreeDistComponent from "./graphs/degreeDistComponent.vue";
import autoTreeComponent from "./graphs/autoTreeComponent.vue";
import kNeighborComponent from "./graphs/kNeighborComponent.vue";
import { useOrigFullGraphStore } from "@/store/store";
const origFullGraphStore = useOrigFullGraphStore();
// frontend effects related
const fullgraphExtendableDiv = ref(null);
//const showDemoDiv = ref(false);
//const demoDivStyle = ref({});
//const demoDivClass = ref("");
//const isMouseInsideArea = ref(false);
const gridConfig = ref([
  {
    cols: 6,
    classes: "pa-1 h-100 expand-transition",
    items: [
      {
        component: "kNeighborComponent",
        classes: "h-50 w-100 p-1 rounded d-flex flex-column justify-content-evenly align-items-center",
        styles: {
          border: "0.1rem #6c757d dashed"
        }
      },
      {
        component: "autoTreeComponent",
        classes: "h-50 w-100 p-0  mt-1  rounded d-flex flex-column justify-content-evenly align-items-center",
        styles: {
          border: "0.1rem #6c757d dashed"
        }
      },
    ]
  },
  {
    cols: 6,
    classes: "pa-1 d-flex flex-row justify-content-evenly align-items-center",
    items: [
      {
        component: "metricsReportComponent",
        classes: "h-50 w-100 p-1 rounded d-flex flex-column justify-content-evenly align-items-center",
        styles: {
          border: "0.1rem #6c757d dashed"
        }
      },
      {
        component: "degreeDistComponent",
        classes: "h-50 w-100  mt-1 p-1 rounded d-flex flex-column justify-content-evenly align-items-center",
        styles: {
          border: "0.1rem #6c757d dashed"
        }
      },
      // Add other components similarly
    ]
  },
  // Add other columns similarly
]);
onMounted(() => {});
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
