<template>
    <div>
      <v-row class="mb-2" v-for="(trip, index) in trips" :key="trip.id">
        <v-col cols="12">
          <v-card 
            elevation="2" 
            @click="onCardClick(trip)" 
            :ripple="true" 
            class="d-flex flex-row pa-5"
            hover
          >
            <v-card-title class="flex-grow-1">{{ `Trip ${index + 1}: ${trip.title}` }}</v-card-title>
            <v-card-subtitle>{{ trip.date }} - Drivetime: {{ trip.runtime }} hours</v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        // Your fake trips data
        trips: [
          { id: 1, title: 'Mountain Adventure', date: '2024-03-18', runtime: '5' },
          { id: 2, title: 'City Exploration', date: '2024-03-20', runtime: '3' },
          { id: 3, title: 'Beach Holiday', date: '2024-03-22', runtime: '7' },
        ],
      };
    },
    methods: {
      onCardClick(trip) {
        // Handle the card click event
        console.log('Trip clicked:', trip);
        this.$router.push({ name: 'tripDetail', params: { id: trip.id } });
      }
    }
  };
  </script>
  
  <style scoped>
  </style>
  