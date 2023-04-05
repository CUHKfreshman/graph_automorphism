
<template>
  <v-app>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script setup>
</script>

<style>
#app {
  width: 100%;
  height: 100%;
  max-height:100%;
  min-height:100vh;
  overflow-y:hidden;
  padding: 0;
  margin: 0;
  display: flex;
  /*IMPORTANT: to beatify layout*/
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/*
#sidebar.collapse {
  width: 0!important;
  padding: 0!important;

  transition: all 0.1s cubic-bezier(0.445, 0.05, 0.55, 0.95);
}
#sidebar.show {
  width: 20%!important;
  padding: 1rem!important;

  transition: all 0.3s cubic-bezier(0.075, 0.82, 0.165, 1);
}
#sidebar.collapsing {
  width: 0!important;
  padding: 0!important;
  transition: all 0.14s cubic-bezier(0.445, 0.05, 0.55, 0.95);
}*/
</style>
