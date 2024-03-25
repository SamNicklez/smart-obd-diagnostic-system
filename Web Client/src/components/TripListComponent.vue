<template>
  <div>
    <v-row class="mb-2" v-for="(trip, index) in trips" :key="trip.trip_id">
      <v-col cols="12">
        <v-card
          elevation="2"
          @click="onCardClick(trip)"
          :ripple="true"
          class="d-flex flex-row pa-5"
          hover
        >
          <v-card-title class="flex-grow-1">{{ `Trip ${index + 1}: ${trip.title}` }}</v-card-title>
          <v-card-subtitle
            >Start Time: {{ trip.start_time }} - Drivetime: {{ trip.runtime }}</v-card-subtitle
          >
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'
import { useCookies } from 'vue3-cookies'
export default {
  setup() {
    const { cookies } = useCookies()
    return { cookies }
  },
  data() {
    return {
      trips: []
    }
  },
  created() {
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/grabTrips',
      headers: {
        Authorization: 'Bearer ' + this.cookies.get('token')
      }
    }

    axios
      .request(config)
      .then((response) => {
        let trips = []
        response.data[1].forEach((element) => {
          trips.push({
            id: element.trip_id,
            title: this.formatDate(element.start_time),
            start_time: this.formatTime(element.start_time),
            runtime: this.formatDuration(element.runtime)
          })
        })
        this.trips = trips.reverse()
      })
      .catch((error) => {
        console.log(error)
      })
  },
  methods: {
    onCardClick(trip) {
      console.log('Trip clicked:', trip)
      this.$router.push({ name: 'tripDetail', params: { id: trip.id } })
    },
    formatDate(inputDate) {
      const date = new Date(inputDate)
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      const year = date.getFullYear()
      return `${month}/${day}/${year}`
    },
    formatTime(inputDateTime) {
      const date = new Date(inputDateTime)
      let hours = date.getHours()
      const minutes = date.getMinutes().toString().padStart(2, '0')
      const ampm = hours >= 12 ? 'PM' : 'AM'
      hours = hours % 12
      hours = hours ? hours.toString().padStart(2, '0') : '12'
      return `${hours}:${minutes}${ampm}`
    },
    formatDuration(seconds) {
      if (seconds < 60) {
        return `${Math.round(seconds, 0)} second${seconds === 1 ? '' : 's'}`
      } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60)
        return `${minutes} minute${minutes === 1 ? '' : 's'}`
      } else {
        const hours = Math.floor(seconds / 3600)
        return `${hours} hour${hours === 1 ? '' : 's'}`
      }
    }
  }
}
</script>

<style scoped></style>
