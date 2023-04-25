<template>

  <v-card
    class="h-100 border-3 p-0 overflow-hidden"
    style="height: 95.5vh"
  >
    <v-card-title class="text-center text-overline py-0">Metrics Report</v-card-title>
    <v-card-text
      class="p-0 h-100 d-flex flex-column align-items-center justify-content-center justify-content-lg-start"
    >
      <v-table density="compact" class="mb-0">
        <tbody>
          <tr>
            <td class="border-1 border-end">Nodes</td>
            <td id="nodenum"></td>
          </tr>
          <tr>
            <td class="border-1 border-end">Edges</td>
            <td id="edgenum"></td>
          </tr>
          <tr>
            <td class="border-1 border-end">Avg Degree</td>
            <td id="avg-deg"></td>
          </tr>
          <tr>
            <td class="border-1 border-end">Max Degree</td>
            <td id="max-deg"></td>
          </tr>
          <tr>
            <td class="border-1 border-end">Density</td>
            <td id="density"></td>
          </tr>
          <tr>
            <td class="border-1 border-end">Node ID</td>
            <td id="node-id"></td>
          </tr>
          <tr>
            <td
              class="border-1 border-end text-nowrap"
              style="width: 32%"
            >
              Degree Centrality
            </td>
            <td id="degreeCentrality"></td>
          </tr>
          <tr>
            <td class="border-1 border-end">Pagerank</td>
            <td id="pagerank"></td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>

</template>
<script setup>

</script>
