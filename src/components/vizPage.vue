<template>
  <v-container
    fluid
    class="ma-0"
    style="height: 100vh; overflow: hidden"
    no-padding
  >
    <toolbar @addComponent="addComponent" @removeComponent="removeComponent" />
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
            style="overflow: hidden; border-width: 0.08rem !important"
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
          <div class="h-100 w-100 p-0 m-0 grid-container" v-if="hasWindow">
            <div
              v-for="(component, index) in components"
              :key="index"
              :class="[
                'p-1 rounded d-flex flex-column justify-content-evenly align-items-center',
                `grid-row-${component.rowSpan}`,
                `grid-col-${component.colSpan}`,
              ]"
            >
              <!--
            :style="`border: 0.1rem #6c757d dashed`"-->
              <v-card class="component-wrapper">
                <component :is="component.component" />
              </v-card>
              <!--            <v-btn small color="primary" @click="changeSize(index)">
              Toggle Size
            </v-btn>
            <v-btn small color="error" @click="removeComponent(index)">
              Remove
            </v-btn>-->
            </div>
          </div>
          <v-card
            style="border: 0.1rem #6c757d"
            class="h-100 w-100 pa-0 ma-0"
            v-else
          >
            <v-skeleton-loader type="image"></v-skeleton-loader>
          </v-card>
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
import { ref } from "vue";
import toolbar from "./tools/toolbar.vue";
import metricsReportComponent from "./tools/metricsReportComponent.vue";
import customizedIMComponent from "./graphs/customizedIMComponent.vue";
import origFullGraphComponent from "./graphs/origFullGraphComponent.vue";
import degreeDistComponent from "./graphs/degreeDistComponent.vue";
import autoTreeComponent from "./graphs/autoTreeComponent.vue";
import kNeighborComponent from "./graphs/kNeighborComponent.vue";
import { useOrigFullGraphStore } from "@/store/store";
const origFullGraphStore = useOrigFullGraphStore();
// frontend effects related
const fullgraphExtendableDiv = ref(null);
const hasWindow = ref(false);
//const showDemoDiv = ref(false);
//const demoDivStyle = ref({});
//const demoDivClass = ref("");
//const isMouseInsideArea = ref(false);
/*
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
onMounted(() => {});*/

const components = ref([]);
const componentMapping = {
  "Metrics Report": metricsReportComponent,
  AutoTree: autoTreeComponent,
  "K Neighbor": kNeighborComponent,
  "Degree Distribution": degreeDistComponent,
  "Customized IM": customizedIMComponent,
};
const addComponent = (name, rowSpan, colSpan) => {
  //["K Neighbor", "AutoTree", "Metrics Report","Degree Distribution"]
  hasWindow.value = true;
  console.log("emit received", name);
  components.value.push({
    component: componentMapping[name],
    name: name,
    rowSpan: rowSpan,
    colSpan: colSpan,
  });
};

const removeComponent = (name) => {
  const index = components.value.findIndex((c) => c.name === name);
  components.value.splice(index, 1);
  if (components.value.length === 0) {
    hasWindow.value = false;
  }
};
</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 0.5rem;
  height: 100%;
  width: 100%;
}
.grid-container > div {
  overflow: hidden;
  width: 100%;
  height: 100%;
}

.component-wrapper {
  height: 100%;
  width: 100%;
  overflow: hidden;
}
.grid-row-1 {
  grid-row: span 1;
}

.grid-row-2 {
  grid-row: span 2;
}

.grid-col-1 {
  grid-column: span 1;
}

.grid-col-2 {
  grid-column: span 2;
}

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
