<template>
  <v-container fluid>
    <v-row class="d-flex align-stretch">
      <v-col cols="7">
        <div class="pa-4 d-flex flex-column">
          <HeatMapComponent />
        </div>
      </v-col>
      <v-col cols="5">
        <div class="pa-4 d-flex flex-column">
          <MonthlyStatsComponent />
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-title class="headline mb-2">Your Recent Trips</v-card-title>  
          <TripsComponent />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import HeatMapComponent from '@/components/HeatMapComponent.vue';
import MonthlyStatsComponent from '@/components/MonthlyStatsComponent.vue';
import TripsComponent from '@/components/TripListComponent.vue'; 
export default {
  components: {
    HeatMapComponent,
    MonthlyStatsComponent,
    TripsComponent
  },
};
</script>

<style scoped>
</style>
