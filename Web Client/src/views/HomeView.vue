<script setup>
import TestGraph from '@/components/HeatMapComponent.vue'
</script>

<template>
  <div class="card">
    <h1>Dashboard</h1>
    <br>
    <p>This will eventually have pretty graphs and settings.</p>
    <TestGraph />
  </div>
</template>

<style scoped>
.card {
  background-color: #F06543;
  width: auto;
  height: auto;
  text-align: center;
  font-size: 2em;
  border-radius: 10px;
  padding-left: 10vw;
  padding-right: 10vw;
  padding-bottom: 10vh;
  padding-top: 2.5vh;
  margin-left: 1vw;
  margin-right: 1vw;
  margin-bottom: 5vh;
  color: white;
}
</style>