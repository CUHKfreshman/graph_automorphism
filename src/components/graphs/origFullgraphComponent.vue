<template>
  <div class="h-100 ma-0 pa-0" ref="origFullgraphContainer">
    <canvas ref="origFullgraphCanvas" class="h-100 w-100" />
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
import { useOrigFullgraphStore } from "@/store/app.ts";
const store = useOrigFullgraphStore();
console.log("store");
console.log(store);
// ref of dom elements for orig fullgraph
const origFullgraphCanvas = ref(null);
const origFullgraphContainer = ref(null);
// create full graph
// reactive orig fullgraph
//function
const expandFullgraphTransition = () => {
  store.expandFullgraph = !store.expandFullgraph;
  store.origFullgraph.fitView();
};
// watch for changes in full graph config
watch(
  store.origFullgraphConfig,
  () => {
    console.log("origFullgraphConfig changed");
    console.log(store.origFullgraph);
    store.origFullgraph.setConfig(store.origFullgraphConfig);
    store.origFullgraph.start();
    //origFullgraph.fitView();
  },
  { deep: true }
);
/*
watch(
  store.origFullgraph,
  (g) => {
    console.log("origFullgraph changed");
    console.log(g);
  },
  { deep: true }
);*/
onMounted(async () => {
  await nextTick();
  if (origFullgraphContainer.value.clientWidth) {
    store.origFullgraphCreate(origFullgraphCanvas.value);
  }
});
</script>
