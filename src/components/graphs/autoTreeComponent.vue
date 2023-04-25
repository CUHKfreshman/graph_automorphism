<template>
  <div class="h-100 ma-0 pa-0" ref="autoTreeContainer">
    <canvas ref="autoTreeCanvas" class="h-100 w-100" />
    <!--    <v-btn
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
  </v-btn>-->
  </div>
</template>
<script setup>
import { ref, watch, nextTick, onMounted } from "vue";
import { useAutoTreeStore } from "@/store/store.js";
const autoTreeStore = useAutoTreeStore();
// ref of dom elements for k neighbor
const autoTreeCanvas = ref(null);
const autoTreeContainer = ref(null); /*
watch(
 origFullGraphStore.selectedNode,
  (node) => {
    console.log("kNeighbor Init Triggers");
    if(node != 'undefined')
      KNeighborStore.kNeighborCreate(kNeighborCanvas.value);
  },
  { deep: true }
);*/

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
  autoTreeStore.autoTreeCanvas = autoTreeCanvas.value;
});
</script>
