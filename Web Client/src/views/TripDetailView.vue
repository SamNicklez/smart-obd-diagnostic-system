<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>{{ tripDetail.title }}</v-card-title>
          <v-card-subtitle
            >{{ tripDetail.date }} - Runtime: {{ tripDetail.runtime }} hours</v-card-subtitle
          >
          <v-card-text>{{ tripDetail.description }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      tripDetail: {}
    }
  },
  // Assuming the trip's ID is passed as a route parameter
  props: ['id'],
  mounted() {
    console.log(this.id)
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/grabCurrentTrip?trip_id=13',
      headers: {
        Authorization:
          'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MX0.tjVEMiS5O2yNzclwLdaZ-FuzrhyqOT7UwM9Hfc0ZQ8Q'
      }
    }

    axios
      .request(config)
      .then((response) => {
        console.log(JSON.stringify(response.data[1][0]))
        this.tripDetail = response.data[1][0]
      })
      .catch((error) => {
        console.log(error)
      })
  },
  methods: {}
}
</script>
