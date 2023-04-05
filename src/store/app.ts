// Utilities
import { defineStore } from "pinia";
import { Graph } from "@cosmograph/cosmos";
export const useOrigFullgraphStore = defineStore("origFullgraphStore", {
  state: () => ({
    // graph container css effect
    expandFullgraph: false,
    // graph
    nodelist: [],
    edgelist: [],
    origFullgraph: undefined as undefined | Graph,
    origColormap: [],
    ssmColormap: [],
    ssm_all_dict: {},
    // layout options
    origFullgraphConfig: {
      nodeColor: "#4B5BBF",
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
        decay: 10000,
        repulsionFromMouse: 2,
      },
    },
  }),
  getters: {},
  actions: {
    setNodelist(newList) {
      this.nodelist = newList;
    },
    setEdgelist(newList) {
      this.edgelist = newList;
    },
    origFullgraphCreate(origFullgraphCanvas) {
      const degreeToColorHex = (degree, minDegree, maxDegree) => {
        const lerp = (a, b, t) => a + (b - a) * t;
        const revlerp = (a, b, t) => b - (b - a) * t;
        //#226fFF to #ff46b3
        const color_lr = ["#226fFF", "#ff46b3"];
        const r_lr = [];
        const g_lr = [];
        const b_lr = [];

        color_lr.forEach((color) => {
          r_lr.push(parseInt(color.slice(1, 3), 16));
          g_lr.push(parseInt(color.slice(3, 5), 16));
          b_lr.push(parseInt(color.slice(5, 7), 16));
        });

        const linearT = (degree - minDegree) / (maxDegree - minDegree);
        const t = Math.sqrt(linearT);
        const r = Math.round(lerp(r_lr[0], r_lr[1], t));
        const g = Math.round(revlerp(g_lr[0], g_lr[1], t));
        const b = Math.round(revlerp(b_lr[0], b_lr[1], t));
        return "#" + r.toString(16) + g.toString(16) + b.toString(16);
      };

      console.log("creating full graph");
      const initconfig = {
        //backgroundColor: "#FFFFFF",
        nodeSize: 4,
        nodeColor: "#4B5BBF",
        nodeGreyoutOpacity: 0.1,
        linkWidth: 0.1,
        linkColor: "#5F74C2",
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
              this.origFullgraph.selectNodeByIndex(i);
              this.origFullgraph.zoomToNodeByIndex(i);
            } else {
              this.origFullgraph.unselectNodes();
            }
            console.log("Clicked node: ", node);
          },
        },
      };
      // create graph
      this.origFullgraph = new Graph(origFullgraphCanvas, initconfig);
      console.log("Init graph...");
      console.log(this.origFullgraph);
      //For testing
      //let tmpnode = [{ 'id': '0' }, { 'id': '1' }];
      //let tmpedge = [{ 'source': '0', 'target': '1' }];
      this.origFullgraph.setData(this.nodelist, this.edgelist);
      // render by degree initially
      const degreeArray = this.origFullgraph.graph.degree;
      console.log(degreeArray);
      const minDegree = Math.min(...degreeArray);
      const maxDegree = Math.max(...degreeArray);
      this.origColormap = degreeArray.map((degree) =>
        degreeToColorHex(degree, minDegree, maxDegree)
      );
      console.log("origColormap", this.origColormap);
      this.origColormapRender();
      /*
      this.origFullgraphConfig.nodeColor = (node) => {
        return degreeToColorHex(
          degreeArray[parseInt(node.id)],
          minDegree,
          maxDegree
        );
      };
      */
      //this.origFullgraph.zoom(0.9);
      this.origFullgraph.fitView();
    },
    origColormapRender() {
      this.origFullgraphConfig.nodeColor = (node) => {
        return this.origColormap[parseInt(node.id)];
      };
    },
    ssmColormapCreate(data) {
      this.ssm_all_dict = data;
      console.log("ssm_all_dict", this.ssm_all_dict);
      let non_singular_pairs = 0;
      const ssm_degree_dict = {};
      const degreeArray = this.origFullgraph.graph.degree;
      let all_size = 0;
      let ssm_all_num = 0;
      Object.entries(this.ssm_all_dict).forEach(([, value]) => {
          ssm_all_num++;
          let color = '#3a4abb';
          if (value.length > 1) {
              if ( !(value[0] in this.ssmColormap) ) {
                  all_size += value.length;
                  const deg = degreeArray[value[0]];
                  if (deg != 0)// not a seperated node
                      non_singular_pairs += 1;
                  if (deg in ssm_degree_dict) {
                      ssm_degree_dict[deg] = ssm_degree_dict[deg] + 1;
                  }
                  else {
                      ssm_degree_dict[deg] = 1;
                  }
              }
              color = '#' + (Math.random() * 11451415511919810).toString(16).substring(0,6);
          }
          value.forEach(val =>
            this.ssmColormap[val] = color);
      });
      console.log(all_size,ssm_all_num,ssm_degree_dict,non_singular_pairs);
      console.log(this.ssmColormap);
    },
    ssmColormapRender() {
        //render_degree_distribution();
        this.origFullgraphConfig.nodeColor = (node) => {
            return this.ssmColormap[parseInt(node.id)];
            /*
            if (this.ssmColormap[node] != '#F2EBEB') {
                orig_fullgraph.setNodeAttribute(node, 'size', 3)// orig_fullgraph.degree(node) * 4
            }
            else {
                orig_fullgraph.setNodeAttribute(node, 'size', 3)//orig_fullgraph.degree(node)
            }*/
        }
        this.origFullgraph.pause();
    }
  },
});
