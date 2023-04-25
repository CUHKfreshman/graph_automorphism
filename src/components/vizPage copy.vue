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
        <div class="h-100 w-100 p-0 m-0 grid-container">
          <div
            v-for="(component, index) in components"
            :key="index"
            :class="[
              'p-1 rounded d-flex flex-column justify-content-evenly align-items-center',
              `grid-row-${component.rowSpan}`,
              `grid-col-${component.colSpan}`,
            ]"
            :style="`border: 0.1rem #6c757d dashed`"
          >
          <div class="component-wrapper">
            <component :is="component.component" />
          </div>

<!--            <v-btn small color="primary" @click="changeSize(index)">
              Toggle Size
            </v-btn>
            <v-btn small color="error" @click="removeComponent(index)">
              Remove
            </v-btn>-->

          </div>
        </div>
        </v-col>
      </v-row>
    </v-container>
    <v-snackbar v-model="noSpaceSnackbar">
      Not enough Space (Maximum: 2X2)!

      <template v-slot:actions>
        <v-btn
          color="pink"
          variant="text"
          @click="noSpaceSnackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
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
import { ref, onMounted, computed, nextTick } from "vue";
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
const noSpaceSnackbar = ref(false);

const components = ref([]);
const componentMapping = {
  'Metrics Report': metricsReportComponent,
  'AutoTree': autoTreeComponent,
  'K-Neighbor': kNeighborComponent,
  'Degree Distribution': degreeDistComponent
};
const findNextAvailablePosition = () => {
  let positions = [];
  for (let row = 1; row <= 2; row++) {
    for (let col = 1; col <= 2; col++) {
      positions.push({ row, col });
    }
  }

  for (const position of positions) {
    const occupied = components.value.some(
      (component) =>
        component.row === position.row && component.col === position.col
    );

    if (!occupied) {
      return position;
    }
  }
  return null;
};

const addComponent = (name,rowSpan,colSpan) => {
  //["K-Neighbor", "AutoTree", "Metrics Report","Degree Distribution"]
  console.log("emit received",name);
  if(canAddComponent.value){
    components.value.push({
      component: componentMapping[name],
      name: name,
      rowSpan: rowSpan,
      colSpan: colSpan,
    });
  }
  else{
    noSpaceSnackbar.value = true;
    console.log(components.value)
  }
};

const removeComponent = (name) => {
  const index = components.value.findIndex((c) => c.name === name);
  components.value.splice(index, 1);
};

const canAddComponent = computed(() => {
  let totalRowSpan = 0;
  let totalColSpan = 0;
  for (const component of components.value) {
    totalRowSpan += component.rowSpan;
    totalColSpan += component.colSpan;
  }
  return totalRowSpan < 4 && totalColSpan < 4;
});
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
