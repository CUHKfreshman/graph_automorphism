<script setup>
import { ref } from "vue";
import welcomePage from "../components/welcomePage.vue";
import vizPage from "../components/vizPage.vue";
import { useOrigFullGraphStore, useAutoTreeStore, useCustomizedIMStore } from "@/store/store";
const origFullGraphStore = useOrigFullGraphStore();
const autoTreeStore = useAutoTreeStore();
const customizedIMStore = useCustomizedIMStore();
const showWelcomePage = ref(true);
/*
const nodelist = ref([]);
const edgelist = ref([]);
*/
// to toggle between login and viz page
const toggleChild = () => {
  showWelcomePage.value = !showWelcomePage.value;
};
/*
const updateNodeList = (newnodeList) => {
  //console.log("Updated nodeList:");
  //console.log(newnodeList);
  nodelist.value = newnodeList;
};

const updateEdgeList = (edgeList) => {
  edgelist.value = edgeList;
};
*/
// This function is used to poll the server for new data, and then handle the data.
// The function is called long polling because it will keep polling the server until it gets a response, and then it will poll the server again.

const longPolling = async () => {
  try {
    //console.log("Long polling...");
    const response = await fetch("http://localhost:4000/poll");
    const data = await response.json();
    handleData(data);
    longPolling();
  } catch (error) {
    console.error("Long polling error:", error);
  }
};

const handleData = (resp) => {
  switch (resp.type) {
    case "noData":
      //console.log("No data received");
      break;
    case "AutoTreeData":
      console.log("AT received:", resp.data);
      autoTreeStore.assignAutoTree(resp.data);
      break;
    case "SSMData":
      console.log("SSM Data received", resp.data);
      origFullGraphStore.ssmColormapCreate(resp.data);
      break;
    case "IMData":
      console.log("IM received:", resp.data);
      origFullGraphStore.imColormapCreate(resp.data, true, true);
      break;
    case "customizedIMData":
      console.log("customized IM received:", resp.data);
      customizedIMStore.hasReceived = true;
      if(customizedIMStore.useOrig){
        origFullGraphStore.imColormapCreate(resp.data, true, true);
      }
      else{
        customizedIMStore.imColormapCreate(resp.data, true, true);
      }

      break;
    default:
      console.log("Unhandled response type", resp.type);
      break;
  }
};
const concurrentDataListener = async (edges) => {
  //console.log("listening to data concurrently...");

  const response = await fetch("http://localhost:4000/upload", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(edges),
  });

  if (response.status === 200) {
    //console.log("Response:", response);
  } else {
    //console.log("Response Error:", response);
  }

  longPolling();
};

// add
/* Deprecated EventSource functions
var source;
const concurrentDataListener =  async (edges) => {
  //console.log("listening to data concurrently...");
  source = new EventSource("http://localhost:4000/stream");
  let count = 0;
  source.addEventListener("AutoTreeData", function (event) {
    const data = JSON.parse(event.data);
    //console.log("Response 1:", data);
    count ++;
    if (count == 3){
      source.close();
    }
  });

  source.addEventListener("SSMData", function (event) {
    //console.log("SSM Data received");
    //console.log(event.data);
   origFullGraphStore.ssmColormapCreate(JSON.parse(event.data));
    count ++;
    if (count == 3){
      source.close();
    }
  });

  source.addEventListener("IMData", function (event) {
    const data = JSON.parse(event.data);
    //console.log("Response 3:", data);
    count ++;
    if (count == 3){
      source.close();
    }
  });
  source.addEventListener('error', (event) => {
  console.error('EventSource connection error:', event);
});

  await setTimeout(() => {
    const response = fetch("http://localhost:4000/upload", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(edges),
  }).then(() => {
    //console.log("Response 0:", response);
  });

  }, 5000);

};
const closeEventSource = () => {
  //console.log("Page refresh or unload, closing EventSource");
  if (source) {
    source.close();
  }
};

window.addEventListener("beforeunload", closeEventSource);

onUnmounted(() => {
  //console.log("Unmounted, closing EventSource");
    source.close();
  window.removeEventListener("beforeunload", closeEventSource);
});
*/
</script>

<template>
  <welcomePage
    :show-welcome-page="showWelcomePage"
    @toggle-child="toggleChild"
    @concurrent-data-listener="concurrentDataListener"
    v-if="showWelcomePage"
  /><!--
    @update-node-list="updateNodeList"
    @update-edge-list="updateEdgeList"-->
  <vizPage v-else />
</template>

<style scoped></style>
