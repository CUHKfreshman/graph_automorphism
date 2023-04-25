<template>
  <div class="h-100 ma-0 pa-0" ref="origFullGraphContainer">
    <canvas ref="origFullGraphCanvas" class="h-100 w-100" />
    <v-btn
      icon
      style="
        position: absolute;
        right: 0%;
        top: 50%;
        text-align: center;
        z-index: 1000;
        transform: translate(0%, -50%);
        background-color: transparent !important;
      "
      @click="expandFullgraphTransition"
    >
      <v-icon style="font-size: 1rem" v-if="store.expandFullgraph"
        >mdi-chevron-double-left</v-icon
      >

      <v-icon style="font-size: 1rem" v-else>mdi-chevron-double-right</v-icon>
    </v-btn>
  </div>
</template>
<script setup>
import { ref, watch, onMounted, nextTick } from "vue";
import { useOrigFullGraphStore } from "@/store/store.js";
const store = useOrigFullGraphStore();
//console.log("store");
//console.log(store);
// ref of dom elements for orig fullgraph
const origFullGraphCanvas = ref(null);
const origFullGraphContainer = ref(null);
// create full graph
// reactive orig fullgraph
//function
const expandFullgraphTransition = () => {
  store.expandFullgraph = !store.expandFullgraph;
  store.origFullGraph.fitView();
};
// watch for changes in full graph config
watch(
  store.origFullGraphConfig,
  () => {
    //console.log(origFullGraphConfig changed");
    //console.log(store.origFullGraph);
    store.origFullGraph.setConfig(store.origFullGraphConfig);
    store.origFullGraph.start();
    //OrigFullGraph.fitView();
  },
  { deep: true }
);
/*
watch(
  store.origFullGraph,
  (g) => {
    //console.log(origFullGraph changed");
    //console.log(g);
  },
  { deep: true }
);*/
onMounted(async () => {
  await nextTick();
  if (origFullGraphContainer.value.clientWidth) {
    store.origFullGraphCreate(origFullGraphCanvas.value);
  }
});
</script>
