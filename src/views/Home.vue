<script setup>
import { ref } from "vue";
import welcomePage from "../components/welcomePage.vue";
import vizPage from "../components/vizPage.vue";
import { useOrigFullgraphStore } from '@/store/app.ts';
const origFullgraphStore = useOrigFullgraphStore();
const showFirstChild = ref(true);
/*
const nodelist = ref([]);
const edgelist = ref([]);
*/
// to toggle between login and viz page
const toggleChild = () => {
  showFirstChild.value = !showFirstChild.value;
};
/*
const updateNodeList = (newnodeList) => {
  console.log("Updated nodeList:");
  console.log(newnodeList);
  nodelist.value = newnodeList;
};

const updateEdgeList = (edgeList) => {
  edgelist.value = edgeList;
};
*/
// add
const concurrentDataListener = async (edges) => {
  console.log("listening to data concurrently...");
  const source = new EventSource("http://localhost:4000/stream");

  source.addEventListener("AutoTreeData", function (event) {
    const data = JSON.parse(event.data);
    console.log("Response 1:", data);
  });

  source.addEventListener("SSMData", function (event) {
    console.log("SSM Data received");
    console.log(event.data);
    origFullgraphStore.ssmColormapCreate(JSON.parse(event.data));
  });

  source.addEventListener("IMData", function (event) {
    const data = JSON.parse(event.data);
    console.log("Response 3:", data);
  });

  source.addEventListener("error", (event) => {
    console.error("EventSource error", event);
  });

  source.addEventListener("close", () => {
    console.log("EventSource connection closed, retrying in 0.5 seconds...");
    setTimeout(source, 500);
  });
  const response = await fetch("http://localhost:4000/upload", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(edges),
  });
  console.log(response);
};
</script>

<template>
  <welcomePage
    :show-first-child="showFirstChild"
    @toggle-child="toggleChild"
    @concurrent-data-listener="concurrentDataListener"
    v-if="showFirstChild"
  /><!--
    @update-node-list="updateNodeList"
    @update-edge-list="updateEdgeList"-->
  <vizPage v-else />
</template>

<style scoped></style>
