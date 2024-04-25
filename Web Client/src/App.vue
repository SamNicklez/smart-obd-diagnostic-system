<script setup>
import Navbar from '@/components/NavComponent.vue'
</script>

<template>
  <v-app>
    <Navbar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<style>
body,
html,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #e8e9eb;
}

#template {
  background-color: #e8e9eb;
}

#app {
  display: flex;
  flex-direction: column;
  min-width: 100%;
  min-height: 100%;
  background-color: #e8e9eb;
}

.main {
  flex: 1;
  overflow: auto;
  background-color: #e8e9eb;
}

@font-face {
  font-style: normal;
  font-display: auto;
  font-family: 'Poppins';
  src: url('/public/Poppins-Regular.ttf');
}

.v-application__wrap {
  background-color: #e8e9eb;
}

.leaflet-routing-container {
  display: none !important;
}
.leaflet-control-attribution {
  display: none !important;
}
</style>
