/* If use TypeScript, then cannot access to Cosmograph Graph private variables */
// Utilities
import { defineStore } from "pinia";
import { Graph } from "@cosmograph/cosmos";
import graphologyGraph from 'graphology';
import * as graphologyMetrics from 'graphology-library/metrics';

export const useOrigFullGraphStore = defineStore("origFullGraphStore", {
  state: () => ({
    // theme
    isDarkTheme: false,
    // graph container css effect
    kNeighborStore: useKNeighborStore(),
    autoTreeStore: useAutoTreeStore(),
    graphologyStore: useGraphologyStore(),
    customizedIMStore: useCustomizedIMStore(),
    expandFullgraph: false,
    // has analyzed
    hasAnalyzedSSM: false,
    hasAnalyzedOrig: false,
    hasAnalyzedIM: false,
    //has received
    hasReceivedSSM: false,
    hasReceivedIM: false,
    // graph
    nodeList: [],
    edgeList: [],
    nodeNum: 0,
    edgeNum: 0,
    origDegreeDict: {},
    ssmDegreeDict: {},
    //stats
    selectedNode: undefined,
    selectedNodeStats: {},
    ssmNonSingularCount: 0,
    ssmCount: 0,
    maxDegree: 0,
    avgDegree: 0,
    ssmMaxDegree: 0,
    ssmAvgDegree: 0,
    origFullGraph: undefined,
    origColormap: [],
    ssmColormap: [],
    imColormap: [],
    imRoundColorDict: {},
    imPercentDict: {},
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
    initData(newNodeNum, newEdgeNum, newNodeList, newEdgeList) {
      this.hasAnalyzedOrig = false;
      this.nodeNum = newNodeNum;
      this.edgeNum = newEdgeNum;
      this.nodeList = newNodeList;
      this.edgeList = newEdgeList;
      const callbackFlag = this.graphologyStore.initGraphology(newNodeNum, newEdgeNum, newNodeList, newEdgeList);
      if (callbackFlag)
      this.hasAnalyzedOrig = true;
      else console.log("Unhandled Graphology Error");
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
        backgroundColor: "#FFFFFF",
        nodeSize: 4,            //4
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.08,
        linkGreyoutOpacity: 0.08,
        linkWidth: 0.8,
        linkColor: "#b6b6b6", //#5F74C2 is default Cosmos color. #666666 is black theme, #e0e0e0 is white theme
        linkArrows: false,
        linkVisibilityDistanceRange: [0, 150],
        simulation: {
          linkDistance: 11,
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
              this.selectedNodeStats = this.graphologyStore.getNodeStats(node.id);
              //TODO: add a condition
              //handle KNeighbor
              if (this.kNeighborEnabled) {
                this.kNeighborStore.kNeighborCreate();
              }
              console.log("selectedNode", this.selectedNode);
              //handle customizedIM comparison
              if(this.customizedIMStore.customizedIM !== null)
                {
                  this.customizedIMStore.customizedIM.selectNodeByIndex(i, true);
                  this.customizedIMStore.customizedIM.zoomToNodeByIndex(i);
                }

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
      if (this.isDarkTheme) {
        initconfig.backgroundColor = "#222222";
        initconfig.linkColor = "#666666";
      }
      // create graph
      this.origFullGraphConfig = initconfig;
      this.origFullGraph = new Graph(OrigFullGraphCanvas, this.origFullGraphConfig);
      //console.log("Init graph...");
      //console.log(this.origFullGraph);
      //For testing
      //let tmpnode = [{ 'id': '0' }, { 'id': '1' }];
      //let tmpedge = [{ 'source': '0', 'target': '1' }];
      this.origFullGraph.setData(this.nodeList, this.edgeList);
      // render by degree initially
      const degreeArray = this.origFullGraph.graph.degree;
      const minDegree = Math.min(...degreeArray);
      const maxDegree = Math.max(...degreeArray);
      const sumDegree = degreeArray.reduce((acc, val) => acc + val, 0);
      this.avgDegree = sumDegree / degreeArray.length;
      this.maxDegree = maxDegree;
      //color
      let colorLR = ["#226fFF", "#ff46b3"];
      // 1. Create an array of indices sorted based on the corresponding id in nodeList
      const sortedIndices = this.nodeList.map((_, index) => index).sort((a, b) => parseInt(this.nodeList[a].id) - parseInt(this.nodeList[b].id));
      console.log("sortedIndices", sortedIndices);
      // 2. Use the sorted indices to create the origColormap
      this.origColormap = sortedIndices.map(index => {
        return this.curvedColorHex(colorLR, degreeArray[index], minDegree, maxDegree, "linear");
      });
      //size
      this.origDegreeDict = sortedIndices.map(index => {
        return degreeArray[index];
      });
      //console.log("origDegreeDict", typeof this.origDegreeDict);
      this.origFullGraphConfig.nodeSize = (node) => {
        // Find the index of the node.id in the sorted nodeList using sortedIndices
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
      this.origFullGraphConfig.linkColor = this.isDarkTheme ? "#666666" : "#b6b6b6"; //isblack? #666666 : #e0e0e0
      // 2. Implement theorigFullGraphConfig.nodeSize function
      this.toggleView("orig");
    },
    ssmColormapCreate(data) {
      this.hasAnalyzedSSM = false;
      this.ssmAllDict = data;
      //console.log("ssmAllDict", this.ssmAllDict);
      this.ssmNonSingularCount = 0;
      this.ssmMaxDegree = 0;
      this.ssmAvgDegree = 0;
      //const degreeArray = this.origFullGraph.graph.degree;
      //let allSize = 0;
      this.ssmCount = 0;
      Object.entries(this.ssmAllDict).forEach(([, value]) => {
        this.ssmCount++;
        let color = "#F2EBEB";//#3c4bbc
        if (value.length > 1) {
          if (!(value[0] in this.ssmColormap)) {
            //allSize += value.length;
            const deg = this.origDegreeDict[value[0]];
            if (deg != 0)
              // not a seperated node
              this.ssmNonSingularCount++;
            this.ssmAvgDegree += deg;
            if (deg in this.ssmDegreeDict) {
              this.ssmDegreeDict[deg] = this.ssmDegreeDict[deg] + 1;
            } else {
              this.ssmDegreeDict[deg] = 1;
              this.ssmMaxDegree = Math.max(this.ssmMaxDegree, deg);
            }
          }
          color =
            "#" +
            (Math.random() * 1145141919810).toString(16).substring(0, 6);
        }
        value.forEach((val) => (this.ssmColormap[val] = color));
      });
      this.ssmAvgDegree /= this.ssmNonSingularCount;
      for (let i = 0; i <= this.ssmMaxDegree; i++) {
        if (!Object.prototype.hasOwnProperty.call(this.ssmDegreeDict, i)) {
          this.ssmDegreeDict[i] = 0;
        }
      }
      this.hasAnalyzedSSM = true;
      console.log("SSM analysis completed.");
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
      this.origFullGraphConfig.linkColor = this.isDarkTheme ? "#666666" : "#b6b6b6"; //isblack? #666666 : #e0e0e0
      //this.origFullGraphConfig.linkVisibilityDistanceRange = [0, 100000];
      this.toggleView("ssm");
    },
    imColormapCreate(data, isNewData, isGradient) {
      if (isNewData) {
        this.hasAnalyzedIM = false;
        this.imAllDict = data;
        this.imDistributionDict = Object.values(this.imAllDict).map(array => array.length);
        this.imPercentDict = {};
        for (const round in this.imDistributionDict){
          this.imPercentDict[round] = ( parseInt(this.imDistributionDict[round]) / this.nodeNum * 100);
          if(round == 0){
            continue;
          }
          this.imPercentDict[round] += this.imPercentDict[parseInt(round) - 1];

        }
        //console.log("imDistributionDict", this.imDistributionDict);
      }
      this.imRoundColorDict = {};
      this.imColormap = [];
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
            if (Object.prototype.hasOwnProperty.call(this.customizedIMStore.imRoundColorDict, round)) {


              color = this.customizedIMStore.imRoundColorDict[round];
            }
            else {
              color = "#" + (Math.random() * 1145141919810).toString(16).substring(0, 6);

            }
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
        this.hasAnalyzedIM = true;
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
          if (result == "Same" || result == "None") {
            return this.isDarkTheme ? "#666666" : "#b6b6b6";
          }
          else return result;
        }
        else {
          return this.isDarkTheme ? "#666666" : "#b6b6b6";
        }
      };
      //this.origFullGraphConfig.linkColor = "#bcbcbc";
      //this.origFullGraphConfig.linkVisibilityDistanceRange = [0, 100000];
      this.toggleView("im");
    },
    imColormapRoundSelect(roundNum, isAdd) {
      //// no , change to select ids using selectids(imAllDict[round])
      this.imSelectedRounds = isAdd ? [...this.imSelectedRounds, roundNum] : this.imSelectedRounds.filter((item) => item !== roundNum);
      let allNodesToBeSelected = [];
      for (const round of this.imSelectedRounds) {
        if (typeof this.imAllDict[round] === 'undefined') break; // if competitor has more rounds
        allNodesToBeSelected = [...allNodesToBeSelected, ...this.imAllDict[round].map(num => num.toString())];
      }
      this.origFullGraph.unselectNodes();
      this.origFullGraph.selectNodesByIds(allNodesToBeSelected);
      console.log("selected nodes", allNodesToBeSelected);
      console.log("selected rounds", this.imSelectedRounds);
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
    kNeighborNum: 0,
    hasAnalyzedKNeighbor: false,
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
      this.kNeighborNum = 0;
      this.hasAnalyzedKNeighbor = false;
      if (typeof this.kNeighbor !== 'undefined') {
        this.kNeighbor.destroy();
        this.kNeighbor = null;
      }
      //TODO: add a method to check if kneighbor is in the window
      if (typeof this.origFullGraphStore.selectedNode == 'undefined') {
        console.log("no node selected when K Neighbor triggered");
        return
      }

      //console.log("creating kNeighbor");
      const initconfig = {
        backgroundColor: "#FFFFFF",
        nodeSize: 4,            //4
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.1,
        linkWidth: 0.8,
        linkColor: "#b6b6b6", //#5F74C2 is default Cosmos color. #666666 is black theme, #e0e0e0 is white theme
        linkArrows: false,
        linkVisibilityDistanceRange: [0, 150],
        simulation: {
          linkDistance: 18,
          linkSpring: 0.2,
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
      if (this.origFullGraphStore.isDarkTheme) {
        initconfig.backgroundColor = "#222222";
        initconfig.linkColor = "#666666";
      }
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
      // select the initial node
      const pairNodesArray = [nodeID];

      // Initialize an array to store visited nodes
      const visitedNodes = new Set();

      // get the k adjacent nodes of each of the adjacent nodes
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

      //console.log("rawAdjacentNodesArray", rawAdjacentNodesArray);
      const distinctAdjacentNodesArray = Array.from(new Set(rawAdjacentNodesArray));
      //console.log("distinctAdjacentNodesArray", distinctAdjacentNodesArray);

      // Finally select
      const rawAllNodesArray = [
        ...Array.from(visitedNodes),
        ...distinctAdjacentNodesArray,
      ];
      const distinctAllNodesArray = Array.from(new Set(rawAllNodesArray.map(val => val.toString())));

      return distinctAllNodesArray;
    },
    kNeighborUpdate() {
      let selectedNodeNeighbors = this.getKNeighbor(this.origFullGraphStore.selectedNode, this.kValue);
      this.kNeighborNum = selectedNodeNeighbors.length;
      const filteredConnectionsArray = this.origFullGraphStore.edgeList.filter(connection => {
        return (
          selectedNodeNeighbors.includes(connection.source.toString()) &&
          selectedNodeNeighbors.includes(connection.target.toString())
        );
      });

      this.kNeighbor.setData(selectedNodeNeighbors.map(id => ({ id })), filteredConnectionsArray);
      this.hasAnalyzedKNeighbor = true;
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
    hasAnalyzedAutoTree: false,
    hasReceivedAutoTree: false,
    origFullGraphStore: useOrigFullGraphStore(),
    autoTreeRawList: null,
    autoTree: undefined,
    nonAsteroid: [],
    hasDestoryedAsteroid: false,
    autoTreeCanvas: null,
    autoTreeConfig: null,
    autoTreeNodeList: [],
    autoTreeEdgeList: [],
  }),
  actions: {
    assignAutoTree(newData) {

      if (typeof this.autoTree !== 'undefined') {
        this.autoTree.destroy();
        this.autoTree = null;
      }
      this.hasAnalyzedAutoTree = false;
      console.log("assignAutoTree", newData);
      this.autoTreeRawList = newData;
      let nonLeafCell = -1; // minus the root node
      let totalCell = Object.keys(this.autoTreeRawList).length;
      for (let val in this.autoTreeRawList) {
        let tmpNode = this.autoTreeRawList[val];
        if (tmpNode.size != 1) {
          nonLeafCell += 1;
          this.nonAsteroid.push(tmpNode.order);
        }
        else {
          if (tmpNode.depth !== '1') {
            this.nonAsteroid.push(tmpNode.order);
          }
        }
        this.autoTreeNodeList.push(tmpNode.order); //, { x: Math.random(), y: Math.random(), size: Math.max(5 - parseInt(tmp_node.depth), 1) * 1.25, label: tmp_node.order, color: "#F2EBEB" }
      }
      for (let val in this.autoTreeRawList) {
        if (this.autoTreeRawList[val].children[0] != '-1') {
          for (let child in this.autoTreeRawList[val].children) {
            this.autoTreeEdgeList.push({ source: this.autoTreeRawList[val].order, target: this.autoTreeRawList[val].children[child] })
          }
        }
      }
      console.log("at incoming");
      console.log(totalCell, nonLeafCell);
      this.autoTreeNodeList = [...this.autoTreeNodeList].map(item => {
        return { id: item };
      });
      this.autoTreeEdgeList = this.autoTreeEdgeList.map(item => Object.assign({}, item));
    },
    autoTreeCreate() {
      if (typeof this.autoTree !== 'undefined') {
        this.autoTree.destroy();
        this. autoTree = null;
      }

      //console.log("creating kNeighbor");
      const initconfig = {
        backgroundColor: "#FFFFFF",
        nodeSize: (node) => {
          return Math.min(6, this.autoTreeRawList[parseInt(node.id) + 1].size + 1);
        },            //4
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.1,
        linkWidth: 0.8,
        linkColor: "#b6b6b6", //#5F74C2 is default Cosmos color. #666666 is black theme, #e0e0e0 is white theme
        linkArrows: false,
        linkVisibilityDistanceRange: [0, 150],
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
              console.log(this.autoTreeRawList[parseInt(node.id)]['vertex_list']);
              this.autoTree.selectNodeByIndex(i, true);
              this.autoTree.zoomToNodeByIndex(i);
              // index = order + 1
              this.origFullGraphStore.origFullGraph.selectNodesByIds(this.autoTreeRawList[parseInt(node.id) + 1]['vertex_list']);
              this.origFullGraphStore.origFullGraph.fitViewByNodeIds(this.autoTreeRawList[parseInt(node.id) + 1]['vertex_list']);

            } else {
              this.autoTree.unselectNodes();
            }
            //console.log("Clicked node: ", node);
          },
        },
      };
      if (this.origFullGraphStore.isDarkTheme) {
        initconfig.backgroundColor = "#222222";
        initconfig.linkColor = "#666666";
      }
      // create graph
      this.autoTreeConfig = initconfig;
      if (this.hasDestoryedAsteroid) {

        this.autoTreeConfig.nodeSize = (node) => {
          return Math.min(6, this.autoTreeRawList[parseInt(node.id) + 1].size / 3 + 1);
        }
      }
      this.autoTree = new Graph(this.autoTreeCanvas, this.autoTreeConfig);
      this.autoTree.setData(this.autoTreeNodeList, this.autoTreeEdgeList);

      this.autoTree.start();

    },
    asteroidDestroy() {
      // [{id: '1'}, {id: '2'}, {id: '3'},....]
      this.nonAsteroid = [...this.nonAsteroid].map(item => {
        return { id: item };
      });
      const nonAsteroidSet = new Set(this.nonAsteroid.map(node => node.id));
      this.autoTreeEdgeList = this.autoTreeEdgeList.filter((edge) => {
        return nonAsteroidSet.has(edge.source) && nonAsteroidSet.has(edge.target);
      });
      this.autoTreeConfig.nodeSize = (node) => {
        return Math.min(6, this.autoTreeRawList[parseInt(node.id) + 1].size / 3 + 1);
      }
      this.autoTreeNodeList = this.nonAsteroid;
      this.autoTree.setData(this.autoTreeNodeList, this.autoTreeEdgeList);
      this.hasDestoryedAsteroid = true;

    }
  }

});
export const useCustomizedIMStore = defineStore("customizedIMStore", {
  state: () => ({
    origFullGraphStore: useOrigFullGraphStore(),
    hasReceived: false,
    //useOrig: false,
    useNewContainer: false,
    imAllDict: {},
    imDistributionDict: {},
    imRoundColorDict: {},
    imPercentDict: {},
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
      if (this.customizedIM !== null) {
        this.customizedIM.destroy();
        this.customizedIM = null;
      }
      console.log("creating full graph for customizedIM");
      const initconfig = {
        backgroundColor: "#FFFFFF",
        nodeSize: 4,            //4
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.1,
        linkWidth: 0.8,
        linkColor: "#b6b6b6", //#5F74C2 is default Cosmos color. #666666 is black theme, #e0e0e0 is white theme
        linkArrows: false,
        linkVisibilityDistanceRange: [0, 150],
        simulation: {
          linkDistance: 1,
          linkSpring: 0.3,
          repulsion: 1,
          gravity: 0.5,
          friction: 0.85,
        },
        events: {
          //node, i, pos, event
          onClick: (node, i) => {
            if (node && i !== undefined) {
              this.customizedIM.selectNodeByIndex(i, true);
              this.customizedIM.zoomToNodeByIndex(i);
              this.origFullGraphStore.origFullGraph.selectNodeByIndex(i, true);
              this.origFullGraphStore.origFullGraph.zoomToNodeByIndex(i);
            } else {
              this.customizedIM.unselectNodes();
            }
            //console.log("Clicked node: ", node);
          },
        },
      };
      if (this.origFullGraphStore.isDarkTheme) {
        initconfig.backgroundColor = "#222222";
        initconfig.linkColor = "#666666";
      }
      // create graph
      this.customizedIMConfig = initconfig;
      this.customizedIM = new Graph(this.customizedIMCanvas, this.customizedIMConfig);
      this.customizedIM.setData(this.origFullGraphStore.nodeList, this.origFullGraphStore.edgeList);
      // render by degree initially
      const degreeArray = this.customizedIM.graph.degree;
      //console.log('deg');
      //console.log(degreeArray);
      //console.log(this.nodeList);
      const minDegree = Math.min(...degreeArray);
      const maxDegree = Math.max(...degreeArray);
      //color
      // 1. Create an array of indices sorted based on the corresponding id in nodeList
      this.customizedIMConfig.nodeSize = (node) => {
        // Find the index of the node.id in the sorted nodeList using sortedIndices
        return (this.origFullGraphStore.origDegreeDict[parseInt(node.id)] - minDegree) / (maxDegree - minDegree) * 5 + 1;
      };
      this.imColormapRender();
      this.customizedIM.fitView();

    },
    imColormapCreate(data, isNewData, isGradient) {
      if (isNewData) {
        this.imAllDict = data;
        this.imDistributionDict = Object.values(this.imAllDict).map(array => array.length);
        this.imPercentDict = {};
        for (const round in this.imDistributionDict){
          this.imPercentDict[round] = ( parseInt(this.imDistributionDict[round]) / this.origFullGraphStore.nodeNum * 100);
          if(round == 0){
            continue;
          }
          this.imPercentDict[round] += this.imPercentDict[parseInt(round) - 1];
        }

      }
      this.imRoundColorDict = {};
      this.imColormap = [];
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
          if (result == "Same" || result == "None") {
            return this.origFullGraphStore.isDarkTheme ? "#666666" : "#b6b6b6";
          }
          else return result;
        }
        else {
          return this.origFullGraphStore.isDarkTheme ? "#666666" : "#b6b6b6";
        }
      };
      //this.toggleView("im");
    },
    imColormapRoundSelect(roundNum, isAdd) {
      //// no , change to select ids using selectids(imAllDict[round])
      console.log("imColormapRoundSelect", roundNum, isAdd)
      this.imSelectedRounds = isAdd ? [...this.imSelectedRounds, roundNum] : this.imSelectedRounds.filter((item) => item !== roundNum);
      let allNodesToBeSelected = [];
      for (const round of this.imSelectedRounds) {
        if (typeof this.imAllDict[round] === 'undefined') break; // if competitor has more rounds
        allNodesToBeSelected = [...allNodesToBeSelected, ...this.imAllDict[round].map(num => num.toString())];
      }
      this.customizedIM.unselectNodes();
      this.customizedIM.selectNodesByIds(allNodesToBeSelected);
    },
  }
});

export const useGraphologyStore = defineStore("graphologyStore", {
  state: () => ({
    origFullGraphology: null,
    nodeList: [],
    edgeList: [],
    density: 0,
  }),
  actions: {
    initGraphology(nodeNum, edgeNum, nodeList, edgeList) {
      console.log("setGraph");
      console.log(typeof nodeNum, nodeNum);
      console.log(typeof edgeNum, edgeNum);
      console.log(typeof nodeList, nodeList);
      console.log(typeof edgeList, edgeList);
      this.origFullGraphology = new graphologyGraph({ multi: false, type: "undirected", allowSelfLoops: false });
      this.edgeList = edgeList;
      // in graphology, "id" is called "key"
      this.nodeList = nodeList.map(item => {
        return {
          key: item.id,
          ...item
        };
      });
      this.origFullGraphology.import({ nodes: this.nodeList, edges: this.edgeList });
      this.density = graphologyMetrics.graph.undirectedDensity(this.origFullGraphology);
      graphologyMetrics.centrality.degree.assign(this.origFullGraphology);
      console.log("ok", this.origFullGraphology.getNodeAttributes('1'));
      graphologyMetrics.centrality.pagerank.assign(this.origFullGraphology);
      console.log("ok", this.origFullGraphology.getNodeAttributes('1'));
      //graphologyMetrics.centrality.betweenness.assign(this.origFullGraphology);
      //console.log("ok", this.origFullGraphology.getNodeAttributes('1'));
      //graphologyMetrics.centrality.closeness.assign(this.origFullGraphology);
      //console.log("ok", this.origFullGraphology.getNodeAttributes('1'));
      graphologyMetrics.centrality.eigenvector.assign(this.origFullGraphology);
      console.log("ok", this.origFullGraphology.getNodeAttributes('1'));
      //graphologyMetrics.centrality.hits.assign(this.origFullGraphology);
      //console.log("ok", this.origFullGraphology.getNodeAttributes('1'));
      return true;

    },
    getNodeStats(nodeID) {
      let nodeAttrs = this.origFullGraphology.getNodeAttributes(nodeID);
      const stat = {
        id: nodeID,
        degree: this.origFullGraphology.degree(nodeID),
        degreeCentrality: nodeAttrs.degreeCentrality,
        pagerank: nodeAttrs.pagerank
      }
      console.log(stat);
      return stat;
    },
    getNodeListAttr(nodeList, attr){
      let attrList = [];
      for(const node of Object.values(nodeList)){
        attrList.push(this.origFullGraphology.getNodeAttribute(node, attr));
      }
      return attrList.sort((a,b)=>Number(b) - Number(a));
    }
  },

})
