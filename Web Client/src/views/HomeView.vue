<template>
  <v-container fluid>
    <!-- First Row with equal-height columns -->
    <v-row class="d-flex align-stretch">
      <!-- First card occupying a larger portion of the screen width -->
      <v-col cols="7">
        <div class="pa-4 d-flex flex-column">
          <!-- Assuming HeatMapComponent should fill the card -->
          <HeatMapComponent />
        </div>
      </v-col>
      <!-- Second card occupying the remaining portion of the screen width -->
      <v-col cols="5">
        <div class="pa-4 d-flex flex-column">
          <!-- Assuming MonthlyStatsComponent should fill the card -->
          <MonthlyStatsComponent />
        </div>
      </v-col>
    </v-row>
    <!-- Second Row -->
    <v-row>
      <!-- Card occupying the full width of the screen -->
      <v-col cols="12">
        <v-card class="pa-4">
          Trips will eventaully go here
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import HeatMapComponent from '@/components/HeatMapComponent.vue';
import MonthlyStatsComponent from '@/components/MonthlyStatsComponent.vue';

export default {
  components: {
    HeatMapComponent,
    MonthlyStatsComponent,
  },
};
</script>

<style scoped>
</style>
