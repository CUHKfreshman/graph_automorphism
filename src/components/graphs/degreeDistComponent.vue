<script setup>
import Highcharts from "highcharts";
import highchartsTheme from "highcharts/themes/grid-light";
import { ref, watch, nextTick, onMounted } from "vue";
import { useOrigFullGraphStore } from "@/store/store.js";
import Accessibility from 'highcharts/modules/accessibility';
import exporting from 'highcharts/modules/exporting';
import exportData from 'highcharts/modules/export-data';
import fullscreen from 'highcharts/modules/full-screen';
import offlineExporting from 'highcharts/modules/offline-exporting';
/*
exportData(Highcharts);
offlineExporting(Highcharts);
fullscreen(Highcharts);
Accessibility(Highcharts);
*/
// dirty method. Use built in support in future.
exporting(Highcharts);
Accessibility(Highcharts);
exportData(Highcharts);
fullscreen(Highcharts);
offlineExporting(Highcharts);
highchartsTheme(Highcharts);
const origFullGraphStore = useOrigFullGraphStore();
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
const chart = ref(null);
const hasMounted = ref(false);
const degreeDistCreate = () => {
  if (chart.value !== null) {
    console.log("destroying chart");
    chart.value.destroy();
  }
  let legendBackgroundColor = '#fff';
  let legendFontColor = '#000';
  let buttonBackgroundColor = '#e5e5e5';
  if(origFullGraphStore.isDarkTheme){
    legendBackgroundColor = '#212121';
    legendFontColor = '#f5f5f5';
    buttonBackgroundColor = '#a0a0a0';
  }
  chart.value = Highcharts.chart("degreeDistContainer", {
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
    },
    legend: {
      floating: false,
      backgroundColor: legendBackgroundColor,
      itemStyle: {
        color: legendFontColor,
      },
    },
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
          theme: {
            fill: buttonBackgroundColor,
          },
        },
      },
    },
  });
};
watch(
  () => origFullGraphStore.hasAnalyzedSSM,
  (newVal) => {
    console.log("hasAnalyzedSSM changed", newVal);
    if (newVal && hasMounted.value) {
      degreeDistCreate();
    }
  },
  { immediate: true }
);
/*
  degreeDistContainerParent.value.addEventListener('resize', () => {
  //document.getElementById("degreeDistContainer").style.width = '100%';
  Highcharts.charts[0].reflow(); // Redraw the chart to fit the new width
});*/
onMounted(async () => {
  await nextTick();
  degreeDistCreate();
  hasMounted.value = true;
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
  <div class="h-100 ma-0 pa-0">
    <v-card class="h-100 w-100 flex-fill border-0" style="border-radius: 0">
      <v-card-title
        class="text-center border-1 text-overline py-0"
        style="border-radius: 0"
        >Degree Distribution</v-card-title
      >
      <!--dirty method. use built-in for vue in future. not time for now-->
      <v-card-text class=" w-100 h-100">
        <v-container
          fluid
          class=" w-100 h-100"
          id="degreeDistContainer"
        ></v-container>
      </v-card-text>
    </v-card>
  </div>
</template>
<style scoped></style>
