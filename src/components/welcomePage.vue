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
      <v-card-text class="p-0 d-flex justify-content-center h-100 w-100">
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
          >
            <!--post panel-->
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
              <v-divider class="m-0"></v-divider>
              <!--enable wrap by user input-->
              <p class="card-text text-start mb-0 ms-1">
                > Node Count: {{ post.nodenum }}
              </p>
              <p class="card-text text-start mb-0 ms-1">
                > Edge Count: {{ post.edgenum }}
              </p>
              <p class="mb-0 me-1 text-start ms-1">
                > Created at: {{ post.time }}
              </p>
            </v-card>
            <!--footer containing buttons-->
            <v-card-actions
              class="p-0 border-0 w-25 align-items-center justify-content-center d-flex w-100"
            >
              <div class="m-0 p-0 w-100 d-flex flex-row justify-space-between">
                <!--show list button-->
                <v-btn class="btn btn-lg border border-1" color="success" dark>
                  <v-icon size="x-large">mdi-open-in-new</v-icon>
                </v-btn>
                <v-btn
                  class="btn btn-lg border border-1"
                  color="secondary"
                  dark
                >
                  <v-icon size="x-large">mdi-view-list</v-icon>
                </v-btn>
                <v-btn class="btn btn-lg border border-1" color="red" dark>
                  <v-icon size="x-large">mdi-trash-can-outline</v-icon>
                </v-btn>
              </div>
            </v-card-actions>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
    <v-card
      class="p-0 text-center w-100 h-100 ms-5 border-0 bg-light align-content-stretch d-flex flex-column"
    >
      <v-card-title primary-title> AutoViz </v-card-title>
      <v-card-subtitle>A Massive Graph Visualization System</v-card-subtitle>
      <v-list lines="one" class="text-left text-large-overline">
        <v-list-item> </v-list-item>
        <v-list-item>
          <p>Our system aims to do this and that;</p>
          <p>
            We apply
            <a href="https://cosmograph.app/" class="fst-italic">Cosmograph</a>
            as our visualization framework;
          </p>
          <p>
            We have many features, including full graph visualization, AutoTree,
            SSM, and IM analysis;
          </p>
          <p>Upload a graph file to get started!</p>
        </v-list-item>
        <v-list-item
          ><!--
      <v-btn class="btn btn-outline-dark btn-lg mb-2" style="border-radius: 0rem;">
        Upload a new graph for analysis
        <v-icon class="bi bi-box-arrow-in-up-right"></v-icon>      <input id="file-upload" type="file" style="display: none;"
        @change="uploadNewFile($event.target.name, $event.target.files, $event.target.files.length)" />
      </v-btn>
      <v-btn color="primary" @click="openFileInput()">Upload File</v-btn>-->
          <v-file-input
            ref="fileInput"
            label="Upload a new graph file"
            accept="*"
            @change="
              uploadNewFile(
                $event.target.name,
                $event.target.files,
                $event.target.files.length
              )
            "
            :multiple="false"
            :show-size="true"
            :show-type="true"
          ></v-file-input
          ><!--:disabled="uploading"-->
        </v-list-item>
        <!--
    <v-list-item class="list-group-item bg-light border-0 mt-2 ms-0 p-0 align-self-start d-flex flex-row flex-fill align-items-center justify-content-center w-100">
      <v-carousel class="carousel carousel-dark h-100 slide" data-bs-ride="false">
        <v-carousel-indicators>
          <v-carousel-indicator v-for="(i) in 3" :key="i" :target="`#carouselCaptions1_${i}`"
            :active="i===1"></v-carousel-indicator>
        </v-carousel-indicators>
        <v-carousel-items>
          <v-carousel-item :id="`carouselCaptions1_${i}`" v-for="(i) in 3" :key="i" :active="i===1">
            <v-img src="../assets/login_background.jpg" class="d-block" height="100%" width="100%" alt="..."></v-img>
            <v-carousel-caption>
              <h5>First slide label</h5>
              <p>Some representative placeholder content for the first slide.</p>
            </v-carousel-caption>
          </v-carousel-item>
        </v-carousel-items>
        <v-carousel-control-prev class="carousel-control-prev" data-bs-target="#carouselCaptions1"
          data-bs-slide="prev">
          <v-icon class="carousel-control-prev-icon"></v-icon>
          <span class="visually-hidden">Previous</span>
        </v-carousel-control-prev>
        <v-carousel-control-next class="carousel-control-next" data-bs-target="#carouselCaptions1"
          data-bs-slide="next">
          <v-icon class="carousel-control-next-icon"></v-icon>
          <span class="visually-hidden">Next</span>
        </v-carousel-control-next>
      </v-carousel>
      <v-carousel class="carousel carousel-dark h-100 slide ms-3" data-bs-ride="false">
        <v-carousel-indicators>
          <v-carousel-indicator v-for="(i) in 3" :key="i" :target="`#carouselCaptions_${i}`" :active="i===1">
          </v-carousel-indicator>
        </v-carousel-indicators>
        <v-carousel-items>
<v-carousel-item :id="`carouselCaptions_${i}`" v-for="(i) in 3" :key="i" :active="i===1">
<v-img src="../assets/login_background.jpg" class="d-block" height="100%" width="100%" alt="..."></v-img>
<v-carousel-caption>
<h5>First slide label</h5>
<p>Some representative placeholder content for the first slide.</p>
</v-carousel-caption>
</v-carousel-item>
</v-carousel-items>
<v-carousel-control-prev class="carousel-control-prev" data-bs-target="#carouselCaptions" data-bs-slide="prev">
<v-icon class="carousel-control-prev-icon"></v-icon>
<span class="visually-hidden">Previous</span>
</v-carousel-control-prev>
<v-carousel-control-next class="carousel-control-next" data-bs-target="#carouselCaptions" data-bs-slide="next">
<v-icon class="carousel-control-next-icon"></v-icon>
<span class="visually-hidden">Next</span>
</v-carousel-control-next>
</v-carousel>
</v-list-item>-->
      </v-list>
      <!--<button type="button" class="btn btn-primary" @click="emitToggleChild()">Emit Home</button>-->
    </v-card>
  </v-container>
</template>

<script setup>
/*

const showFirstChild = ref(true);
const nodelist = ref([]);
const edgelist = ref([]);
*/
import { ref } from "vue";
import { useOrigFullgraphStore } from '@/store/app.ts';

const store = useOrigFullgraphStore();
// emit
const emit = defineEmits([
  "toggle-child",
  //"update-node-list",
  //"update-edge-list",
  "concurrent-data-listener",
]);
defineProps({
  showFirstChild: {
    type: Boolean,
    default: true,
  },

});

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

/*
const emitList = () => {
  console.log('emit list');
  emit('node-list', 'edge-list');
}*/

const uploadNewFile = async (name, fileList, fileLen) => {
  if (fileLen != 1) {
    return;
  }
  let file = fileList[0];
  var reader = new FileReader();

  reader.onload = async (event) => {
    let [nodenum, edgenum, ...edges] = event.target.result.split(/\s|\n/); //array destruction
    console.log(nodenum, edgenum, edges);
    let newnodelist = [...new Set(edges)].map((num) => ({ id: num })); //remove duplicate elements

    let newedgelist = edges
      .map((el, i, arr) => (i % 2 === 0 ? arr.slice(i, i + 2) : null)) // group every two elements
      .filter((el) => el) // remove null elements
      .map((subArr) => ({ source: subArr[0], target: subArr[1] })); // transform sub-arrays into objects with source and target properties
    //emit("update-node-list", newnodelist);
    //emit("update-edge-list", newedgelist);
    emit("concurrent-data-listener", edges);
    console.log("store");
    console.log(store);
    store.setNodelist(newnodelist);
    store.setEdgelist(newedgelist);
    //emitList();
    console.log("Going to Viz...");
    emit("toggle-child");
  };

  reader.onerror = (event) => {
    console.log("error: " + event.target.error);
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
        console.log('resp.data')
        console.log(resp.data[0])
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
