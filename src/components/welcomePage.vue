<!-- the login in front end template -->
<!-- it is the whole html structure of login front end -->
<!-- there are buttons using to register an account -->
<!-- there are buttons using to login for normal user and admin-->

<template>
  <v-container
    fluid
    class="text-center d-flex flex-sm-nowrap align-items-center justify-content-center bg-light h-100"
  >
    <v-card
      class="scrollarea border-3 p-0 me-3 h-100 w-25"
      style="overflow-x: hidden !important"
    >
      <!--posts container-->
      <v-card-title class="fs-4 fw-bold">HISTORY DATA</v-card-title>
      <v-card-text class="h-100 w-100">
        <p class="text text-grey-darken-1">
          History data is saved under flask folder.
        </p>
        <!--
        <v-list
          class="col border-0 list-group list-group-flush d-flex flex-column card w-100"
        >
          <v-list-item
            v-for="post in posts"
            :key="post._id"
            style="
              border-bottom-color: rgba(0, 0, 0, 0.176);
              border-bottom-width: 1px;
              border-bottom-style: solid;
            "
          >-->
        <!--post panel
            <v-card
              class="card-body p-0"
              style="
                border-right-color: rgba(0, 0, 0, 0.176);
                border-right-width: 1px;
                border-right-style: solid;
              "
            >
              <p
                class="card-title font-monospace fs-3 text-start ms-1 text-uppercase p-0 m-0"
              >
                {{ post.filename }}
              </p>
              <v-divider class="m-0"></v-divider>-->
        <!--enable wrap by user input
              <p class="card-text text-start mb-0 ms-1">
                > Node Count: {{ post.nodenum }}
              </p>
              <p class="card-text text-start mb-0 ms-1">
                > Edge Count: {{ post.edgenum }}
              </p>
              <p class="mb-0 me-1 text-start ms-1">
                > Created at: {{ post.time }}
              </p>
            </v-card>-->
        <!--footer containing buttons
            <v-card-actions
              class="p-0 border-0 w-25 align-items-center justify-content-center d-flex w-100"
            >
              <div class="m-0 p-0 w-100 d-flex flex-row justify-space-between">-->
        <!--show list button
                <v-btn class="btn btn-lg border border-1" color="success" dark>
                  <v-icon size="x-large" icon="mdi-open-in-new"></v-icon>
                </v-btn>
                <v-btn
                  class="btn btn-lg border border-1"
                  color="secondary"
                  dark
                >
                  <v-icon size="x-large" icon="mdi-view-list"></v-icon>
                </v-btn>
                <v-btn class="btn btn-lg border border-1" color="red" dark>
                  <v-icon size="x-large" icon="mdi-trash-can-outline"></v-icon>
                </v-btn>
              </div>
            </v-card-actions>
          </v-list-item>
        </v-list>-->
      </v-card-text>
    </v-card>
    <v-card
      class="p-0 text-center w-100 h-100 ms-5 border-0 bg-light align-content-stretch d-flex flex-column"
    >
      <v-card-title primary-title> AutoViz </v-card-title>
      <v-card-subtitle>A Massive Graph Visualization System</v-card-subtitle>
      <v-tooltip text="Tooltip">
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            class="btn btn-lg border border-1 rounded-be-xl"
            color="light"
            style="
              position: absolute;
              left: 0%;
              top: 5%;
              text-align: center;
              transform: translate(0%, -50%);
              border-left: 0 !important;
            "
            dark
            @click="toggleTheme"
          >
            <v-icon
              icon="mdi-brightness-2"
              style="font-size: 1rem"
              v-if="isDarkTheme"
            ></v-icon>

            <v-icon
              icon="mdi-brightness-7"
              style="font-size: 1rem"
              v-else
            ></v-icon>
          </v-btn>
        </template>
        <span>Change Theme</span>
      </v-tooltip>
      <v-list lines="one" class="text-left text-large-overline">
        <v-list-item> </v-list-item>
        <v-list-item class="text-body-1">
          <p>
            This is AutoViz V2.1 Branch <a href="https://cosmograph.app/" class="text-decoration-underline"
            >Cosmos</a
          >, offering full feature support.
          </p>
          <p>
            Autoviz is an advanced graph visualization system for massive
            network visualization and analytics.
          </p>
          <p>
            In addition to basic graph analysis, AutoViz also integrates
            specialized modules dedicated to AutoTree, Symmetric Subgraph
            Matching, and Influence Maximization.
          </p>
          <p>
            This application is the culmination of the FTEC undergraduate final
            year project,
            <span class="font-italic">
              Graph Automorphism over Social Network</span
            >, conducted at The Chinese University of Hong Kong.
          </p>
          <p>
            It is developed by GENG Yihan, WANG Kunyu, and LIU Ziqi, under the
            supervision of Prof. YU Xu Jeffrey.
          </p>
          <v-divider class="mt-2"></v-divider>
          <br />
          <p class="text-overline text-left">Upload a file to get started!</p>
          <v-progress-linear
            indeterminate
            color="grey-lighten-1"
            :height="1"
          ></v-progress-linear>
        </v-list-item>
        <v-list-item>
          <v-file-input
            ref="fileInput"
            label="Upload File"
            @change="
              uploadNewFile(
                $event.target.name,
                $event.target.files,
                $event.target.files.length
              )
            "
            :multiple="false"
            show-size
            show-type
            accept=".txt, .csv, .tsv"
          ></v-file-input
          ><!--:disabled="uploading"-->
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";

import { useOrigFullGraphStore } from "@/store/store.js";
import { useTheme } from "vuetify";
const theme = useTheme();
const isDarkTheme = ref(false);
const toggleTheme = () => {
  theme.global.name.value = theme.global.current.value.dark ? "light" : "dark";
  isDarkTheme.value = !isDarkTheme.value;
  origFullGraphStore.isDarkTheme = isDarkTheme.value;
};

const origFullGraphStore = useOrigFullGraphStore();
// emit
const emit = defineEmits([
  "toggle-child",
  //"update-node-list",
  //"update-edge-list",
  "concurrent-data-listener",
]);
defineProps({
  showWelcomePage: {
    type: Boolean,
    default: true,
  },
});
//const posts = ref({});
/*
const posts = ref({
  0: {
    _id: 0,
    filename: "facebook.csv",
    nodenum: 2000,
    edgenum: 1000,
    time: "21/3/2022",
  },
  1: {
    _id: 0,
    filename: "cosmos.csv",
    nodenum: 2000,
    edgenum: 1000,
    time: "21/3/2022",
  },
});
*/
/*
const emitList = () => {
  //console.log('emit list');
  emit('node-list', 'edge-list');
}*/
//const isUploading = ref(false);
const uploadNewFile = async (name, fileList, fileLen) => {
  if (fileLen != 1) {
    return;
  }
  let file = fileList[0];
  var reader = new FileReader();

  reader.onload = async (event) => {
    emit("concurrent-data-listener", event.target.result);
    let inputStream = event.target.result;
    inputStream = inputStream.replace(/\r\n/g, "\n");
    inputStream = inputStream.replace(/\r/g, "\n");
    let [nodeNum, edgeNum, ...edges] = inputStream.split(/\s+|\n/); //array destruction
    if (edges[edges.length - 1] === "") {
      edges.pop(); // remove empty string at the end of the array
    }
    //console.log(nodenum, edgenum, edges);
    let nodeList = [...new Set(edges)].map((num) => ({ id: num })); //remove duplicate elements

    let edgeList = edges
      .map((el, i, arr) => (i % 2 === 0 ? arr.slice(i, i + 2) : null)) // group every two elements
      .filter((el) => el) // remove null elements
      .map((subArr) => ({ source: subArr[0], target: subArr[1] })); // transform sub-arrays into objects with source and target properties

    //console.log("store");
    //console.log(store);
    origFullGraphStore.initData(nodeNum, edgeNum, nodeList, edgeList);
    //emitList();
    //console.log("Going to Viz...");
    emit("toggle-child");
  };

  reader.onerror = (event) => {
    //console.log("error: " + event.target.error);
    return;
  };

  reader.readAsText(file);
};

/*
    async addUser(user){
      UserService.addUser(user).then(resp=>
        {
          if(resp.status == 205) {
            alert("Invalid information, please check again.");
          }
          else {
            alert("Registered Successfully! Remember to use SID to login.");
          }
        }
      )
    },

    async searchUser(user){
      UserService.searchUser(user).then(resp =>
      {
        //console.log('resp.data')
        //console.log(resp.data[0])
        if(resp.data.length>0)
        {
          //Store current user information in local storage
          var storeInfo = resp.data[0];
          //change status for local storage
          storeInfo['userStatus'] = 'Online';
          //delete password storage in case leaking
          delete storeInfo['password'];
          sessionStorage.setItem("isLogin", JSON.stringify(storeInfo));
          store.commit('setMyInfo', storeInfo);
          //change status in mongodb
          UserService.changeOnlineStatus(user);
          this.$router.push({path:`/home`});
        }
        else
        {
          alert("Invalid account, please check again.");
        }
      }
      )
    }*/
</script>

<style scoped>
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
