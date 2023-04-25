<template>
  <v-container fluid class="pa-0 mt-0 h-100 d-flex flex-sm-nowrap align-center justify-center h-100">
    <v-row class="w-100 h-100 flex-sm-nowrap">
      <v-col
        v-for="(col, colIndex) in gridConfig"
        :key="`col-${colIndex}`"
        :cols="col.cols"
        :class="col.classes"
      >
        <div
          v-for="(item, itemIndex) in col.items"
          :key="`item-${itemIndex}`"
          :class="item.classes"
          :style="item.styles"
        >
          <component :is="item.component" />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { defineProps } from "vue";

defineProps({
  gridConfig: {
    type: Array,
    required: true
  }
});
</script>
