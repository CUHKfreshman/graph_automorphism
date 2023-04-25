<script setup>
import { Graph } from "graphology";
import Highcharts from "highcharts";
import highchartsTheme from 'highcharts/themes/grid-light';
import { ref, watch, nextTick, onMounted, watchEffect  } from "vue";
import { useOrigFullGraphStore } from "@/store/store.js";
import Accessibility from 'highcharts/modules/accessibility';
import exporting from 'highcharts/modules/exporting';
import exportData from 'highcharts/modules/export-data';
import fullscreen from 'highcharts/modules/full-screen';
import offlineExporting from 'highcharts/modules/offline-exporting';exporting(Highcharts);
/*
exportData(Highcharts);
offlineExporting(Highcharts);
fullscreen(Highcharts);
Accessibility(Highcharts);
*/

highchartsTheme(Highcharts);
const origFullGraphStore = useOrigFullGraphStore();
const degreeDistContainerParent = ref(null);
/*
Highcharts.setOptions({ // Apply to all charts
    chart: {
        events: {
            beforePrint: function () {
                this.oldhasUserSize = this.hasUserSize;
                this.resetParams = [this.chartWidth, this.chartHeight, false];
                this.setSize(600, 400, false);
            },
            afterPrint: function () {
                this.setSize.apply(this, this.resetParams);
                this.hasUserSize = this.oldhasUserSize;
            }
        }
    }
});*/
var chart = null;
const degreeDistCreate =() =>{
  chart = Highcharts.chart("degreeDistContainer", {
    credits: {
      enabled: false,
    },
    chart: {
      zoomType: "xy",
    },
    title: {
      text: "",
    },
    subtitle: {
      text: "",
    },
    xAxis: [
      {
        categories: Object.keys(origFullGraphStore.origDegreeDict),
        crosshair: true,
      },
    ],
    yAxis: [
      {
        // Primary yAxis
        labels: {
          style: {
            color: Highcharts.getOptions().colors[1],
          },
        },
        title: {
          text: "",
          style: {
            color: Highcharts.getOptions().colors[1],
          },
        },
      },
      {
        // Secondary yAxis
        title: {
          text: "",
          style: {
            color: Highcharts.getOptions().colors[0],
          },
        },
        labels: {
          //format: '{value} mm',
          style: {
            color: Highcharts.getOptions().colors[0],
          },
        },
        opposite: true,
      },
    ],
    tooltip: {
      headerFormat:
        '<span style="font-size:10px">Degree {point.key}</span><br><table>',
      footerFormat: "</table>",
      shared: true,
    } /*
        legend: {
            align: 'left',
            x: 80,
            verticalAlign: 'top',
            y: 80,
            floating: true,
            backgroundColor:
                Highcharts.defaultOptions.legend.backgroundColor || // theme
                'rgba(255,255,255,0.25)'
        },*/,
    series: [
      {
        name: "SSM",
        type: "column",
        yAxis: 1,
        data: Object.values(origFullGraphStore.ssmDegreeDict),
        //tooltip: {
        //}
      },
      {
        name: "All Nodes",
        type: "spline",
        data: Object.values(origFullGraphStore.origDegreeDict),
        //tooltip: {
        //}
      },
    ],
  exporting: {
    buttons: {
      contextButton: {
        x: -15, // move the button 10 pixels to the left
        y: -7, // move the button 10 pixels down
        symbol: "menu",
        theme:{
          fill: '#a0a0a0',
        }
      }
    }
  }
  });
}
/*
  degreeDistContainerParent.value.addEventListener('resize', () => {
  //document.getElementById("degreeDistContainer").style.width = '100%';
  Highcharts.charts[0].reflow(); // Redraw the chart to fit the new width
});*/
onMounted(async () => {
  await nextTick();
  degreeDistCreate();
  /*
  const resizeObserver = new ResizeObserver(() => {
    console.log('resizeing');
    chart.reflow(); // Redraw the chart to fit the new size
  });
  const container = document.getElementById("degreeDistContainerParent");
  resizeObserver.observe(container);*/
});
</script>
<template>
  <div class="h-100 ma-0 pa-0" >
    <v-card class="h-100 w-100 flex-fill border-0" style="border-radius: 0">
      <v-card-title class="text-center border-1" style="border-radius: 0"
        >Degree Distribution</v-card-title
      >
      <v-card-text class="p-0 m-0 w-100 h-100" id="degreeDistContainerParent">
        <v-container
        fluid
          class="p-0 m-0 w-100 h-100"
          id="degreeDistContainer"
        ></v-container>
      </v-card-text>
    </v-card>
  </div>
</template>
<style scoped>
</style>
