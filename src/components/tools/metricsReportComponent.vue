<template>
  <v-card class="h-100 overflow-x-hidden d-flex flex-column">
    <v-card-title class="text-center text-overline py-0"
      >Metrics Report</v-card-title
    >
    <v-card-text
      class=" text-no-wrap overflow-auto"
    >
      <v-table class="w-100 h-100 text-no-wrap " density="compact" hover>
        <thead>
          <tr class="">
            <th class="w-50">METRIC</th>
            <th class=" ">VALUE</th>
          </tr>
        </thead>
        <tbody class="">
          <tr class="bg-teal-darken-3">
            <td colspan="2">
              <p class="text-left text-caption">Graph Statistics</p>
            </td>
          </tr>
          <tr>
            <td class="w-50">Nodes</td>
            <td v-if="origFullGraphStore.hasAnalyzedOrig">{{ origFullGraphStore.nodeNum }}</td>
          </tr>
          <tr>
            <td class="w-50">Edges</td>
            <td v-if="origFullGraphStore.hasAnalyzedOrig">{{ origFullGraphStore.edgeNum }}</td>
          </tr>
          <tr>
            <td class="w-50">Avg Degree</td>
            <td v-if="origFullGraphStore.hasAnalyzedOrig">
              {{ origFullGraphStore.avgDegree.toString().substring(0, 12) }}
            </td>
          </tr>
          <tr>
            <td class="w-50">Max Degree</td>
            <td v-if="origFullGraphStore.hasAnalyzedOrig">{{ origFullGraphStore.maxDegree }}</td>
          </tr>
          <tr>
            <td class="w-50">Density</td>
            <td v-if="origFullGraphStore.hasAnalyzedOrig">{{ graphologyStore.density.toString().substring(0, 12) }}</td>
          </tr>
          <!--nodewise-->
          <tr class="bg-cyan-darken-3">
            <td colspan="2">
              <p class="text-left text-caption">Node Statistics</p>
            </td>
          </tr>
          <tr>
            <td class="w-50">Node ID</td>
            <td>{{
              origFullGraphStore.selectedNode === undefined
              ? ''
              : origFullGraphStore.selectedNode}}</td>
          </tr>
          <tr>
            <td class="w-50">Degree</td>
            <td>{{
                Object.keys(origFullGraphStore.selectedNodeStats).length === 0
                ? ''
                : origFullGraphStore.selectedNodeStats.degree
                    .toString()
              }}</td>
          </tr>
          <tr>
            <td class="w-50">Degree Centrality</td>
            <td>
              {{
                Object.keys(origFullGraphStore.selectedNodeStats).length === 0
                ? ''
                : origFullGraphStore.selectedNodeStats.degreeCentrality
                    .toString()
                    .substring(0, 12)
              }}
            </td>
          </tr>
          <tr>
            <td class="w-50">Pagerank</td>
            <td>
              {{
                Object.keys(origFullGraphStore.selectedNodeStats).length === 0
                ? ''
                : origFullGraphStore.selectedNodeStats.pagerank
                    .toString()
                    .substring(0, 12)
              }}
            </td>
          </tr>
          <!--ssm stats-->
          <tr class="bg-light-blue-darken-3">
            <td colspan="2">
              <p class="text-left text-caption">SSM Statistics</p>
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Non-Singular Count
            </td>
            <td>
              {{ origFullGraphStore.ssmNonSingularCount === 0 ? '' : origFullGraphStore.ssmNonSingularCount }}
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Avg Degree
            </td>
            <td>
              {{ origFullGraphStore.ssmAvgDegree === 0 ? '' : origFullGraphStore.ssmAvgDegree.toString().substring(0,12) }}
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Max Degree
            </td>
            <td>
              {{ origFullGraphStore.ssmMaxDegree === 0 ? '' : origFullGraphStore.ssmMaxDegree }}
            </td>
          </tr>
          <!--im stats-->
          <tr class="bg-blue-accent-4">
            <td colspan="2">
              <p class="text-left text-caption">IM Statistics</p>
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Rounds
            </td>
            <td>
              {{ Object.keys(origFullGraphStore.imDistributionDict).length === 0 ? '' : Object.keys(origFullGraphStore.imDistributionDict).length }}
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Coverage
            </td>
            <td>
              {{ Object.keys(origFullGraphStore.imDistributionDict).length === 0 ? '' :
              (Object.values(
                origFullGraphStore.imDistributionDict
              ).reduce((a, b) => a + b, 0) / origFullGraphStore.nodeNum).toString().substring(0,12) }}
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Node per Round
            </td>
            <td>
              {{ Object.keys(origFullGraphStore.imDistributionDict).length === 0 ? '' :
              (Object.values(
                origFullGraphStore.imDistributionDict
              ).reduce((a, b) => a + b, 0) / Object.keys(origFullGraphStore.imDistributionDict).length).toString().substring(0,12) }}
            </td>
          </tr>
          <!--customedim stats-->
          <tr class="bg-indigo-accent-4">
            <td colspan="2">
              <p class="text-left text-caption">Customized IM Statistics</p>
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Rounds
            </td>
            <td>
              {{ Object.keys(customizedIMStore.imDistributionDict).length === 0 ? '' : Object.keys(customizedIMStore.imDistributionDict).length }}
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Coverage
            </td>
            <td>
              {{ Object.keys(customizedIMStore.imDistributionDict).length === 0 ? '' :
              (Object.values(
                customizedIMStore.imDistributionDict
              ).reduce((a, b) => a + b, 0) / origFullGraphStore.nodeNum).toString().substring(0,12) }}
            </td>
          </tr>
          <tr>
            <td class="w-50">
              Node per Round
            </td>
            <td>
              {{ Object.keys(customizedIMStore.imDistributionDict).length === 0 ? '' :
              (Object.values(
                customizedIMStore.imDistributionDict
              ).reduce((a, b) => a + b, 0) / Object.keys(customizedIMStore.imDistributionDict).length).toString().substring(0,12) }}
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useOrigFullGraphStore, useGraphologyStore, useCustomizedIMStore } from "@/store/store.js";
const origFullGraphStore = useOrigFullGraphStore();
const graphologyStore = useGraphologyStore();
const customizedIMStore = useCustomizedIMStore();
</script>
<style scoped>

/* Set the width and height of the scrollbar */
::-webkit-scrollbar {
  width: 2px;
  height: 2px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 0;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
