/* If use TypeScript, then cannot access to Graph private variables */
// Utilities
import { defineStore } from "pinia";
import { Graph } from "@cosmograph/cosmos";
export const useOrigFullGraphStore = defineStore("origFullGraphStore", {
  state: () => ({
    // graph container css effect
    kNeighborStore: useKNeighborStore(),
    autoTreeStore: useAutoTreeStore(),
    expandFullgraph: false,
    // graph
    nodelist: [],
    edgelist: [],
    origDegreeDict: {},
    ssmDegreeDict: {},
    selectedNode: undefined,
    origFullGraph: undefined,
    origColormap: [],
    ssmColormap: [],
    imColormap: [],
    imRoundColorDict: {},
    imSelectedRounds: [],
    ssmAllDict: {},
    imAllDict: {},
    imDistributionDict: {},
    atEnabled: false,
    ssmEnabled: false,
    origEnabled: true,
    imEnabled: false,
    kNeighborEnabled: false,
    // layout options
    origFullGraphConfig: {
      nodeColor: "#3c4bbc",
      simulation: {
        repulsion: 1,
        repulsionTheta: 1,
        //repulsionQuadtreeLevels: 9,
        linkSpring: 0.3,
        linkDistance: 5,
        linkDistRandomVariationRange: [1, 1.5],
        gravity: 0.5,
        center: 0.5,
        friction: 0.9,
        decay: 1000,
        repulsionFromMouse: 2,
      },
    },
  }),
  actions: {
    // toggle options for events
    toggleView(view) {
      //console.log("toggleView", view);
      this.atEnabled = view === "at";
      this.ssmEnabled = view === "ssm";
      this.origEnabled = view === "orig";
      this.imEnabled = view === "im";
    },
    setNodelist(newList) {
      console.log(newList);
      this.nodelist = newList;
    },
    setEdgelist(newList) {
      console.log(newList);
      this.edgelist = newList;
    },
    curvedColorHex(colorLR, currentVal, minVal, maxVal, curveOption) {
      //const lerp = (a, b, t) => a + (b - a) * t;
      //const revlerp = (a, b, t) => b - (b - a) * t;
      const combinedLerp = (a, b, t, reverse = false) => reverse ? b - (b - a) * t : a + (b - a) * t;
      //#226fFF to #ff46b3
      //const colorLR = ["#226fFF", "#ff46b3"];
      const rLR = [];
      const gLR = [];
      const bLR = [];

      colorLR.forEach((color) => {
        rLR.push(parseInt(color.slice(1, 3), 16));
        gLR.push(parseInt(color.slice(3, 5), 16));
        bLR.push(parseInt(color.slice(5, 7), 16));
      });

      let t = (currentVal - minVal) / (maxVal - minVal);
      if (curveOption === "sqrt") {
        t = Math.sqrt(t);
      }
      const r = Math.round(combinedLerp(rLR[0], rLR[1], t, rLR[0] > rLR[1]));
      const g = Math.round(combinedLerp(gLR[0], gLR[1], t, gLR[0] > gLR[1]));
      const b = Math.round(combinedLerp(bLR[0], bLR[1], t, bLR[0] > bLR[1]));
      return "#" + r.toString(16).padStart(2, '0') + g.toString(16).padStart(2, '0') + b.toString(16).padStart(2, '0');
    },
    origFullGraphCreate(OrigFullGraphCanvas) {


      //console.log("creating full graph");
      const initconfig = {
        //backgroundColor: "#FFFFFF",
        nodeSize: 4,            //4
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.1,
        linkWidth: 0.1,
        linkColor: "#666666", //#5F74C2 is default Cosmos color. #666666 is black theme, #e0e0e0 is white theme
        linkArrows: false,
        linkGreyoutOpacity: 0,
        simulation: {
          linkDistance: 1,
          linkSpring: 0.3,
          repulsion: 1,
          gravity: 0.25,
          friction: 0.85,
        },
        events: {
          //node, i, pos, event
          onClick: (node, i) => {
            if (node && i !== undefined) {
              this.selectedNode = node.id;
              //TODO: add a condition
              //handle KNeighbor
              if (this.kNeighborEnabled) {
                this.kNeighborStore.kNeighborCreate();
              }
              console.log("selectedNode", this.selectedNode);



              //handle orig full
              if (this.origEnabled) {
                this.origFullGraph.selectNodeByIndex(i, true);
                this.origFullGraph.zoomToNodeByIndex(i);
              }
              else if (this.ssmEnabled) {
                // First, select the initial node
                // const initialNode = node.id;
                const pairNodesArray = this.ssmAllDict[node.id].flat().flat(); // format:[[a], [b]]=>[a,b,]
                ////console.log("pairNodesArray", pairNodesArray)
                // Now, let's get the adjacent nodes of each of the adjacent nodes
                const rawAdjacentNodesArray = [];
                pairNodesArray.forEach(val => {
                  const thisID = val.toString();
                  const tmpNodes = this.origFullGraph.getAdjacentNodes(thisID);

                  rawAdjacentNodesArray.push(...tmpNodes);
                });
                ////console.log("rawAdjacentNodesArray", rawAdjacentNodesArray);
                const distinctAdjacentNodesArray = Array.from(new Set(rawAdjacentNodesArray.map(obj => obj.id.toString())));
                ////console.log("distinctAdjacentNodesArray", distinctAdjacentNodesArray)
                // Finally, we can select all of the nodes we want
                const rawAllNodesArray = [
                  ...pairNodesArray,
                  ...distinctAdjacentNodesArray,
                ];
                const distinctAllNodesArray = Array.from(new Set(rawAllNodesArray.map(val => val.toString())));
                ////console.log("distinctAllNodesArray", distinctAllNodesArray)
                this.origFullGraph.selectNodesByIds(distinctAllNodesArray);
                this.origFullGraph.zoomToNodeByIndex(i);
              }
              else if (this.imEnabled) {
                this.origFullGraph.selectNodeByIndex(i, true);
                this.origFullGraph.zoomToNodeByIndex(i);
              }
            } else {
              this.origFullGraph.unselectNodes();
            }
            //console.log("Clicked node: ", node);
          },
        },
      };
      // create graph
      this.origFullGraph = new Graph(OrigFullGraphCanvas, initconfig);
      //console.log("Init graph...");
      //console.log(this.origFullGraph);
      //For testing
      //let tmpnode = [{ 'id': '0' }, { 'id': '1' }];
      //let tmpedge = [{ 'source': '0', 'target': '1' }];
      this.origFullGraph.setData(this.nodelist, this.edgelist);
      // render by degree initially
      const degreeArray = this.origFullGraph.graph.degree;
      //console.log('deg');
      //console.log(degreeArray);
      //console.log(this.nodelist);
      const minDegree = Math.min(...degreeArray);
      const maxDegree = Math.max(...degreeArray);
      //color
      let colorLR = ["#226fFF", "#ff46b3"];
      // 1. Create an array of indices sorted based on the corresponding id in nodelist
      const sortedIndices = this.nodelist.map((_, index) => index).sort((a, b) => parseInt(this.nodelist[a].id) - parseInt(this.nodelist[b].id));
      console.log("sortedIndices", sortedIndices);
      // 2. Use the sorted indices to create the origColormap
      this.origColormap = sortedIndices.map(index => {
        return this.curvedColorHex(colorLR, degreeArray[index], minDegree, maxDegree, "linear");
      });
      //size
      this.origDegreeDict = sortedIndices.map(index => {
        return degreeArray[index];
      });
      console.log("origDegreeDict", typeof this.origDegreeDict);
      this.origFullGraphConfig.nodeSize = (node) => {
        // Find the index of the node.id in the sorted nodelist using sortedIndices
        return (this.origDegreeDict[parseInt(node.id)] - minDegree) / (maxDegree - minDegree) * 5 + 1;
      };
      /*

      this.origColormap = degreeArray.map((degree) =>
        this.curvedColorHex(colorLR, degree, minDegree, maxDegree, "linear")
      );*/
      //console.log("origColormap", this.origColormap);
      this.origColormapRender();
      /*
      this.origFullGraphConfig.nodeColor = (node) => {
        return this.curvedColorHex(
          degreeArray[parseInt(node.id)],
          minDegree,
          maxDegree,
          "sqrt"
        );
      };
      */
      //this.origFullGraph.zoom(0.9);
      this.origFullGraph.fitView();
    },
    origColormapRender() {
      this.origFullGraphConfig.nodeColor = (node) => {
        return this.origColormap[parseInt(node.id)];
      };
      this.origFullGraphConfig.linkColor = "#666666"; //isblack? #666666 : #e0e0e0
      // 2. Implement theorigFullGraphConfig.nodeSize function
      this.toggleView("orig");
    },
    ssmColormapCreate(data) {
      this.ssmAllDict = data;
      //console.log("ssmAllDict", this.ssmAllDict);
      let non_singular_pairs = 0;
      //const degreeArray = this.origFullGraph.graph.degree;
      let all_size = 0;
      let ssm_all_num = 0;
      Object.entries(this.ssmAllDict).forEach(([, value]) => {
        ssm_all_num++;
        let color = "#F2EBEB";//#3c4bbc
        if (value.length > 1) {
          if (!(value[0] in this.ssmColormap)) {
            all_size += value.length;
            const deg = this.origDegreeDict[value[0]];
            if (deg != 0)
              // not a seperated node
              non_singular_pairs += 1;
            if (deg in this.ssmDegreeDict) {
              this.ssmDegreeDict[deg] = this.ssmDegreeDict[deg] + 1;
            } else {
              this.ssmDegreeDict[deg] = 1;
            }
          }
          color =
            "#" +
            (Math.random() * 1145141919810).toString(16).substring(0, 6);
        }
        value.forEach((val) => (this.ssmColormap[val] = color));
      });
      console.log(all_size, ssm_all_num, this.ssmDegreeDict, non_singular_pairs);
      //console.log(this.ssmColormap);
    },
    ssmColormapRender() {
      //render_degree_distribution();
      this.origFullGraphConfig.nodeColor = (node) => {
        return this.ssmColormap[parseInt(node.id)];
        /*
            if (this.ssmColormap[node] != '#3c4bbc') {
                orig_fullgraph.setNodeAttribute(node, 'size', 3)// orig_fullgraph.degree(node) * 4
            }
            else {
                orig_fullgraph.setNodeAttribute(node, 'size', 3)//orig_fullgraph.degree(node)
            }*/
      };
      this.origFullGraphConfig.linkColor = "#666666"; //#666666
      //this.origFullGraphConfig.linkVisibilityDistanceRange = [0, 100000];
      this.toggleView("ssm");
    },
    imColormapCreate(data, isNewData, isGradient) {
      if (isNewData) {
        this.imAllDict = data;
        this.imDistributionDict = Object.values(this.imAllDict).map(array => array.length);
        console.log("imDistributionDict", this.imDistributionDict);
      }
      // from red to yellow, we only modify the middle content in hex color environment
      //let start_color = 0; //ff0000
      //let endColor = parseInt('ff', 16); // ff'dd'00
      let maxRoundNum = Object.keys(this.imAllDict).length;
      //let gap = end_color / number_of_rounds;
      //var colormap_html = '';
      //var colorarray = ["#012030", "#13678A", "#45C4B0", "#9AEBA3", "#DAFDBA", "#F2EBEB"];
      //var colorarray = ["#BF1F94", "#5503A6", "#3C038C", "#F29F05", "#F25D27", "#F2EBEB"];
      //var colorarray = ["#0554F2", "#05F2F2", "#F2B705", "#F28705", "#F20505", "#F2EBEB"];
      //var colorarray = ["#F77148", "#D64C3E", "#ED516D", "#D63EA6", "#E648F7", "#F2EBEB"];
      //var colorarray = ["#f7c58b", "#593718", "#A65729", "#8C281F", "#0D0D0D", "#F2EBEB"];
      Object.entries(this.imAllDict).forEach(([round, value]) => {
        let colorLR = ["#ff0000", "#ffffcc"];
        let color = "#ff0000"; // begin
        if (value.length > 0) {
          if (isGradient) {
            color = this.curvedColorHex(colorLR, round, 0, maxRoundNum, "linear");
            //color = colorarray[round];
          }
          else {
            color = "#" + (Math.random() * 1145141919810).toString(16).substring(0, 6);
            //color = colorarray[round]; // 3rd round % colorarray.length
          }
          this.imRoundColorDict[round] = color;
          /*

          let color = '#ff0000'; // #ff0000 to #ffff00
          if (value.length > 1) {
            if (key != 0) {
              color = '#ff' + (endColor - (roundNum - key) * 25).toString(16).substring(0, 2) + '00';
            }*/
          /*colormap_html += `<li class="list-group-item d-flex align-items-center">
                <span class="badge rounded-pill me-3" style="background-color:`+ color.substring(0, 7) + `">` + key + `</span>
                <span class="fw-bold">Round `+ key + `</span>
              </li>`*/
        }
        //assign color to each node
        for (const val of value) {
          this.imColormap[val] = color;
        }
      });
      //console.log("imColormap", this.imColormap);
    },
    imColormapRender() {
      //compare which color has smaller roundNum, return the smaller one if their roundNum diff is 1, if same, return "Same", else return "Irrevelant"

      //let maxRoundNum = Object.keys(this.imAllDict).length;
      //const compareColors = (colorA, colorB) => colorA.substring(3, 5) < colorB.substring(3, 5) ? colorA : colorA.substring(3, 5) > colorB.substring(3, 5) ? colorB : "Same";
      const roundDiffCalculator = (colorA, colorB) => {
        // get key value of colorA and colorB from this.imRoundColorDict
        let colorAKey = Object.keys(this.imRoundColorDict).find(
          (key) => this.imRoundColorDict[key] === colorA
        );
        let colorBKey = Object.keys(this.imRoundColorDict).find(
          (key) => this.imRoundColorDict[key] === colorB
        );
        // return the smaller one if their roundNum diff is 1, if same, return "Same", else return "None"
        let roundDiff = colorAKey - colorBKey;
        if (Math.abs(roundDiff) <= 1) {
          return roundDiff === 0 ? "Same" : roundDiff < 0 ? colorA : colorB;
        } else {
          return "None";
        }
        /*
        let colorDifference = parseInt(colorA.substring(3, 5), 16) - parseInt(colorB.substring(3, 5), 16);
        let tDifference = colorDifference / (parseInt("ff", 16) - parseInt("00", 16));
        let currentValDifference = tDifference * maxRoundNum;

        if (Math.abs(currentValDifference) <= 1) {
          return currentValDifference === 0 ? "Same" : (colorDifference < 0 ? colorA : colorB);
        } else {
          return "None";
        }*/
      };
      this.origFullGraphConfig.nodeColor = (node) => {
        return this.imColormap[parseInt(node.id)];
      };
      this.origFullGraphConfig.linkColor = (link) => {
        let src = parseInt(link.source);
        let tar = parseInt(link.target);
        if (Object.prototype.hasOwnProperty.call(this.imColormap, src) && Object.prototype.hasOwnProperty.call(this.imColormap, tar)) {
          let result = roundDiffCalculator(this.imColormap[src], this.imColormap[tar]);
          return result === "Same" ? "#666666" : result;
        }
        else {
          return "#666666";
        }
      };
      //this.origFullGraphConfig.linkColor = "#bcbcbc";
      //this.origFullGraphConfig.linkVisibilityDistanceRange = [0, 100000];
      this.toggleView("im");
    },
    imColormapRoundRender(roundNum, isAdd) {
      //// no , change to select ids using selectids(imAllDict[round])
      this.imSelectedRounds = isAdd ? [...this.imSelectedRounds, roundNum] : this.imSelectedRounds.filter((item) => item !== roundNum);
      let allNodesToBeSelected = [];
      for (const round of this.imSelectedRounds) {
        allNodesToBeSelected = [...allNodesToBeSelected, ...this.imAllDict[round].map(num => num.toString())];
      }
      this.origFullGraph.unselectNodes();
      this.origFullGraph.selectNodesByIds(allNodesToBeSelected);
      //console.log("selected nodes", allNodesToBeSelected);
      //console.log("selected rounds", this.imSelectedRounds);
      //this.origFullGraph.fitView();
      /*
      const getRoundNumByColor = (obj, color) => Object.keys(obj).find(key => obj[key] === color);
      let maxRoundNum = Object.keys(this.imAllDict).length;
      let color = this.imRoundColorDict[roundNum];
      this.origFullGraphConfig.nodeColor = (node) => {
        return this.imColormap[parseInt(node.id)] === color ? this.imColormap[parseInt(node.id)] : "#e0e0e0";
      };
      this.origFullGraphConfig.linkColor = (link) => {
        let src = link.source;
        let tar = link.target;
        if (Object.prototype.hasOwnProperty.call(this.imColormap, src) && Object.prototype.hasOwnProperty.call(this.imColormap, tar)) {
          let result = (this.imColormap[src] === color && this.imColormap[tar] === color) ? color : "#e0e0e0";
          return result;
        }
        else {
          return "#e0e0e0";
        }
      };
      //this.origFullGraphConfig.linkColor = "#bcbcbc";
      //this.origFullGraphConfig.linkVisibilityDistanceRange = [0, 100000];
      this.toggleView("im");*/
    }
  },
});
//TODO: add a color filter for different k
export const useKNeighborStore = defineStore("kNeighborStore", {
  state: () => ({
    origFullGraphStore: useOrigFullGraphStore(),
    kNeighbor: undefined,
    kValue: 1,
    kNeighborConfig: null,
    kNeighborCanvas: undefined,
    kNeighborSelectedNode: null,
    kNeighborSelectedNodeNeighbors: null,
    kNeighborSelectedNodeNeighborsDict: null,
  }),
  actions: {
    // functions: createKNeighbor, updateKNeighbor, deleteKNeighbor? No, use K value to update according to relavive
    kNeighborCreate() {
      if (typeof this.kNeighbor !== 'undefined') {
        this.kNeighbor.destroy();
      }
      //TODO: add a method to check if kneighbor is in the window
      if (typeof this.origFullGraphStore.selectedNode == 'undefined') {
        console.log("no node selected when K Neighbor triggered");
        return
      }

      //console.log("creating kNeighbor");
      const initconfig = {
        //backgroundColor: "#FFFFFF",
        nodeSize: 4,            //4
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.1,
        linkWidth: 0.1,
        linkColor: "#666666", //#5F74C2 is default Cosmos color. #666666 is black theme, #e0e0e0 is white theme
        linkArrows: false,
        linkGreyoutOpacity: 0,
        simulation: {
          linkDistance: 4,
          linkSpring: 0.3,
          repulsion: 2,
          gravity: 0.5,
          center: 0.5,
          friction: 0.85,
        },
        events: {
          //node, i, pos, event
          onClick: (node, i) => {
            if (node && i !== undefined) {
                this.kNeighbor.selectNodeByIndex(i, true);
                this.kNeighbor.zoomToNodeByIndex(i);
            } else {
              this.kNeighbor.unselectNodes();
            }
            //console.log("Clicked node: ", node);
          },
        },
      };
      // create graph
      this.kNeighborConfig = initconfig;
      this.kNeighbor = new Graph(this.kNeighborCanvas, this.kNeighborConfig);
      console.log(this.kNeighborConfig);
      //console.log("Init graph...");
      //console.log(this.kNeighbor);
      //For testing
      //let tmpnode = [{ 'id': '0' }, { 'id': '1' }];
      //let tmpedge = [{ 'source': '0', 'target': '1' }];
      //default k=2
      this.kNeighborUpdate(1);
    },
    getKNeighbor(nodeID, k) {
      // First, select the initial node
      const pairNodesArray = [nodeID];

      // Initialize an array to store visited nodes
      const visitedNodes = new Set();

      // Now, let's get the k adjacent nodes of each of the adjacent nodes
      let rawAdjacentNodesArray = [];
      for (let depth = 0; depth < k; depth++) {
        const nextAdjacentNodesArray = [];

        pairNodesArray.forEach(val => {
          // Check if the node is not visited yet
          if (typeof val != 'undefined') {
            if (!visitedNodes.has(val.toString())) {
              visitedNodes.add(val.toString());
              const thisID = val.toString();
              //console.log("val", val);
              //console.log(thisID);
              const tmpNodes = this.origFullGraphStore.origFullGraph.getAdjacentNodes(thisID);
              //console.log("tmpNodes", tmpNodes.map(obj => obj.id.toString()))
              nextAdjacentNodesArray.push(...tmpNodes.map(obj => obj.id.toString()));
            }
          }
        });

        // Move to the next depth level
        rawAdjacentNodesArray.push(...nextAdjacentNodesArray);
        pairNodesArray.length = 0;
        pairNodesArray.push(...nextAdjacentNodesArray);
      }

      console.log("rawAdjacentNodesArray", rawAdjacentNodesArray);
      const distinctAdjacentNodesArray = Array.from(new Set(rawAdjacentNodesArray));
      console.log("distinctAdjacentNodesArray", distinctAdjacentNodesArray);

      // Finally, we can select all of the nodes we want
      const rawAllNodesArray = [
        ...Array.from(visitedNodes),
        ...distinctAdjacentNodesArray,
      ];
      const distinctAllNodesArray = Array.from(new Set(rawAllNodesArray.map(val => val.toString())));

      return distinctAllNodesArray;
    },
    kNeighborUpdate() {
      let selectedNodeNeighbors = this.getKNeighbor(this.origFullGraphStore.selectedNode, this.kValue);
      //console.log("Updating kNeighbor");
      const filteredConnectionsArray = this.origFullGraphStore.edgelist.filter(connection => {
        return (
          selectedNodeNeighbors.includes(connection.source.toString()) &&
          selectedNodeNeighbors.includes(connection.target.toString())
        );
      });

      //console.log("filteredConnectionsArray", filteredConnectionsArray);
      //console.log("selectedNodeNeighbors", selectedNodeNeighbors);
      //console.log("this.origFullGraphStore.edgelist", this.origFullGraphStore.edgelist);
      //console.log("this.nodelist", this.origFullGraphStore.nodelist);

      this.kNeighbor.setData(selectedNodeNeighbors.map(id => ({ id })), filteredConnectionsArray);

      this.kNeighborRender();
    },
    kNeighborRender() {
      console.log("rendering KNeighbor");
      if (this.origFullGraphStore.origEnabled)
        this.kNeighborConfig.nodeColor = (node) => {
          return node.id == this.origFullGraphStore.selectedNode ? "#1dff08" : this.origFullGraphStore.origColormap[parseInt(node.id)];
        };
      else if (this.origFullGraphStore.ssmEnabled)
        this.kNeighborConfig.nodeColor = (node) => {
          return this.origFullGraphStore.ssmColormap[parseInt(node.id)];
        };
      else if (this.origFullGraphStore.imEnabled)
        this.kNeighborConfig.nodeColor = (node) => {
          return this.origFullGraphStore.imColormap[parseInt(node.id)];
        };
      this.kNeighborConfig.linkColor = "#666666"; //isblack? #666666 : #e0e0e0
      //this.toggleView("orig");

      //this.kNeighbor.setConfig(this.kNeighborConfig);
      this.kNeighbor.start();
      this.kNeighbor.zoomToNodeById(this.origFullGraphStore.selectedNode, undefined, 3);
    },
    kNeighborColorMapRender() {
      if (this.origFullGraphStore.origEnabled)
        this.kNeighborConfig.nodeColor = (node) => {
          return node.id == this.origFullGraphStore.selectedNode ? "#1dff08" : this.origFullGraphStore.origColormap[parseInt(node.id)];
        };
      else if (this.origFullGraphStore.ssmEnabled)
        this.kNeighborConfig.nodeColor = (node) => {
          return this.origFullGraphStore.ssmColormap[parseInt(node.id)];
        };
      else if (this.origFullGraphStore.imEnabled)
        this.kNeighborConfig.nodeColor = (node) => {
          return this.origFullGraphStore.imColormap[parseInt(node.id)];
        };
    }
  },
});

export const useAutoTreeStore = defineStore("autoTreeStore", {
  state: () => ({
    origFullGraphStore: useOrigFullGraphStore(),
    autoTree: null,
    autoTreeGraph: null,
    
    autoTreeCanvas: null,
    autoTreeConfig: null,
    autoTreeNodeList: [],
    autoTreeEdgeList: [],
  }),
  actions: {
    assignAutoTree(autoTree) {
      console.log("assignAutoTree", autoTree);
      this.autoTree = autoTree;
      let nonLeafCell = 0;
      let totalCell = Object.keys(this.autoTree).length;
      for (let val in this.autoTree) {
        let tmpNode = this.autoTree[val];
        if (tmpNode.size != 1) {
          nonLeafCell += 1;
        }
        this.autoTreeNodeList.push(tmpNode.order); //, { x: Math.random(), y: Math.random(), size: Math.max(5 - parseInt(tmp_node.depth), 1) * 1.25, label: tmp_node.order, color: "#F2EBEB" }
      }
      for (let val in this.autoTree) {
        if (this.autoTree[val].children[0] != '-1') {
          for (let child in this.autoTree[val].children) {
            this.autoTreeEdgeList.push({ source: this.autoTree[val].order, target: this.autoTree[val].children[child] })
          }
        }
      }
      console.log("at incoming");
      console.log(totalCell, nonLeafCell);
      console.log([...this.autoTreeNodeList].map(item => {
        return { id: item };
      }));
      console.log(this.autoTreeEdgeList.map(item => Object.assign({}, item)));
    },
    autoTreeCreate() {/*
    if(this.kNeighbor!='undefined'){
      this.kNeighbor.destroy();
    }/*
    //TODO: add a method to check if kneighbor is in the window
    if (this.origFullGraphStore.selectedNode == 'undefined') {
      console.log("no node selected when K Neighbor triggered");
      return
    }*/

      //console.log("creating kNeighbor");
      const initconfig = {
        //backgroundColor: "#FFFFFF",
        nodeSize: 4,            //4
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.1,
        linkWidth: 0.1,
        linkColor: "#666666", //#5F74C2 is default Cosmos color. #666666 is black theme, #e0e0e0 is white theme
        linkArrows: false,
        linkGreyoutOpacity: 0,
        simulation: {
          linkDistance: 4,
          linkSpring: 0.3,
          repulsion: 2,
          gravity: 0.25,
          friction: 0.85,
        },
        events: {
          //node, i, pos, event
          onClick: (node, i) => {
            if (node && i !== undefined) {
              console.log("Clicked cell: ", node, i);
              console.log(this.autoTree[parseInt(node.id)]['vertex_list']);
                this.autoTreeGraph.selectNodeByIndex(i, true);
                this.autoTreeGraph.zoomToNodeByIndex(i);
                // index = order + 1
                this.origFullGraphStore.origFullGraph.selectNodesByIds(this.autoTree[parseInt(node.id) + 1]['vertex_list']);
                this.origFullGraphStore.origFullGraph.fitViewByNodeIds(this.autoTree[parseInt(node.id) + 1]['vertex_list']);

            } else {
              this.autoTreeGraph.unselectNodes();
            }
            //console.log("Clicked node: ", node);
          },
        },
      };
      // create graph
      this.autoTreeConfig = initconfig;
      this.autoTreeGraph = new Graph(this.autoTreeCanvas, this.autoTreeConfig);
      this.autoTreeGraph.setData([...this.autoTreeNodeList].map(item => {
        return { id: item };
      }), this.autoTreeEdgeList.map(item => Object.assign({}, item)));
      this.autoTreeGraph.start();

    },
    asteroidDestroy() {

    }
  }

});
export const useCustomizedIMStore = defineStore("customizedIMStore", {
  state: () => ({
    origFullGraphStore: useOrigFullGraphStore(),
    hasReceived: false,
    useOrig: false,
    imAllDict: {},
    imDistributionDict: {},
    imRoundColorDict: {},
    imSelectedRounds: [],
    imColormap: [],
    customizedIM: null,
    customizedIMCanvas: null,
    customizedIMConfig: null,
    customizedIMNodeList: [],
    customizedIMEdgeList: [],
  }),
  actions: {
    customizedIMCreate() {
      //console.log("creating full graph");
      const initconfig = {
        //backgroundColor: "#FFFFFF",
        nodeSize: 4,            //4
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.1,
        linkWidth: 0.1,
        linkColor: "#666666", //#5F74C2 is default Cosmos color. #666666 is black theme, #e0e0e0 is white theme
        linkArrows: false,
        linkGreyoutOpacity: 0,
        simulation: {
          linkDistance: 1,
          linkSpring: 0.3,
          repulsion: 1,
          gravity: 0.25,
          friction: 0.85,
        },
        events: {
          //node, i, pos, event
          onClick: (node, i) => {
            if (node && i !== undefined) {
                this.customizedIM.selectNodeByIndex(i, true);
                this.customizedIM.zoomToNodeByIndex(i);
            } else {
              this.customizedIM.unselectNodes();
            }
            //console.log("Clicked node: ", node);
          },
        },
      };
      // create graph
      this.customizedIMConfig = initconfig;
      this.customizedIM = new Graph(this.customizedIMCanvas, this.customizedIMConfig);
      this.customizedIM.setData(this.origFullGraphStore.nodelist, this.origFullGraphStore.edgelist);
      // render by degree initially
      const degreeArray = this.customizedIM.graph.degree;
      //console.log('deg');
      //console.log(degreeArray);
      //console.log(this.nodelist);
      const minDegree = Math.min(...degreeArray);
      const maxDegree = Math.max(...degreeArray);
      //color
      // 1. Create an array of indices sorted based on the corresponding id in nodelist
      this.customizedIMConfig.nodeSize = (node) => {
        // Find the index of the node.id in the sorted nodelist using sortedIndices
        return (this.origFullGraphStore.origDegreeDict[parseInt(node.id)] - minDegree) / (maxDegree - minDegree) * 5 + 1;
      };
      this.imColormapRender();
      this.customizedIM.fitView();

    },
    imColormapCreate(data, isNewData, isGradient) {
      if (isNewData) {
        this.imAllDict = data;
        this.imDistributionDict = Object.values(this.imAllDict).map(array => array.length);

      }
      let maxRoundNum = Object.keys(this.imAllDict).length;
      Object.entries(this.imAllDict).forEach(([round, value]) => {
        let colorLR = ["#ff0000", "#ffffcc"];
        let color = "#ff0000"; // begin
        if (value.length > 0) {
          if (isGradient) {
            color = this.origFullGraphStore.curvedColorHex(colorLR, round, 0, maxRoundNum, "linear");
            //color = colorarray[round];
          }
          else {
            color = "#" + (Math.random() * 1145141919810).toString(16).substring(0, 6);
            //color = colorarray[round]; // 3rd round % colorarray.length
          }
          this.imRoundColorDict[round] = color;
          /*

          let color = '#ff0000'; // #ff0000 to #ffff00
          if (value.length > 1) {
            if (key != 0) {
              color = '#ff' + (endColor - (roundNum - key) * 25).toString(16).substring(0, 2) + '00';
            }*/
          /*colormap_html += `<li class="list-group-item d-flex align-items-center">
                <span class="badge rounded-pill me-3" style="background-color:`+ color.substring(0, 7) + `">` + key + `</span>
                <span class="fw-bold">Round `+ key + `</span>
              </li>`*/
        }
        //assign color to each node
        for (const val of value) {
          this.imColormap[val] = color;
        }
      });
      //console.log("imColormap", this.imColormap);
    },
    imColormapRender() {
      const roundDiffCalculator = (colorA, colorB) => {
        // get key value of colorA and colorB from this.imRoundColorDict
        let colorAKey = Object.keys(this.imRoundColorDict).find(
          (key) => this.imRoundColorDict[key] === colorA
        );
        let colorBKey = Object.keys(this.imRoundColorDict).find(
          (key) => this.imRoundColorDict[key] === colorB
        );
        // return the smaller one if their roundNum diff is 1, if same, return "Same", else return "None"
        let roundDiff = colorAKey - colorBKey;
        if (Math.abs(roundDiff) <= 1) {
          return roundDiff === 0 ? "Same" : roundDiff < 0 ? colorA : colorB;
        } else {
          return "None";
        }
      };
      this.customizedIMConfig.nodeColor = (node) => {
        return this.imColormap[parseInt(node.id)];
      };
      this.customizedIMConfig.linkColor = (link) => {
        let src = parseInt(link.source);
        let tar = parseInt(link.target);
        if (Object.prototype.hasOwnProperty.call(this.imColormap, src) && Object.prototype.hasOwnProperty.call(this.imColormap, tar)) {
          let result = roundDiffCalculator(this.imColormap[src], this.imColormap[tar]);
          return result === "Same" ? "#666666" : result;
        }
        else {
          return "#666666";
        }
      };
      //this.toggleView("im");
    },
    imColormapRoundRender(roundNum, isAdd) {
      //// no , change to select ids using selectids(imAllDict[round])
      this.imSelectedRounds = isAdd ? [...this.imSelectedRounds, roundNum] : this.imSelectedRounds.filter((item) => item !== roundNum);
      let allNodesToBeSelected = [];
      for (const round of this.imSelectedRounds) {
        allNodesToBeSelected = [...allNodesToBeSelected, ...this.imAllDict[round].map(num => num.toString())];
      }
      this.customizedIM.unselectNodes();
      this.customizedIM.selectNodesByIds(allNodesToBeSelected);
    },
  }
});
