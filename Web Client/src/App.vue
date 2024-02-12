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
  background-color: #E8E9EB;
}

#template {
  background-color: #E8E9EB;
}

#app {
  display: flex;
  flex-direction: column;
  min-width: 100%;
  min-height: 100%;
  background-color: #E8E9EB;
}

.main {
  flex: 1;
  overflow: auto;
  background-color: #E8E9EB;
}

@font-face {
  font-style: normal;
  font-display: auto;
  font-family: "Poppins";
  src: url('/public/Poppins-Regular.ttf');
}

.v-application__wrap {
  background-color: #E8E9EB;
}
</style>

