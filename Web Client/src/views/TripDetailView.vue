<template>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <v-card>
            <v-card-title>{{ tripDetail.title }}</v-card-title>
            <v-card-subtitle>{{ tripDetail.date }} - Runtime: {{ tripDetail.runtime }} hours</v-card-subtitle>
            <v-card-text>{{ tripDetail.description }}</v-card-text>
            <!-- Additional trip details here -->
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        tripDetail: {},
      };
    },
    // Assuming the trip's ID is passed as a route parameter
    props: ['id'],
    mounted() {
        //console.log(this.id)
      this.fetchTripDetail();
    },
    methods: {
      fetchTripDetail() {
        // Placeholder for fetching trip details, using the prop `id`
        // You would typically make an API call here using this.id to fetch the specific trip details
        // For demonstration, we're using hardcoded data
        const fakeTripDetails = {
          id: this.id,
          title: 'Mountain Adventure',
          date: '2024-03-18',
          runtime: '5',
          description: 'An exciting journey through the mountains.',
          // Add more detailed fields as needed
        };
        this.tripDetail = fakeTripDetails;
      },
    },
  };
  </script>
  