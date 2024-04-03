<template>
  <div class="mainDiv">
    <v-card class="mapCard">
      <v-card-title class="text-center">Trip Overview</v-card-title>
      <div class="mapContainer">
        <div :id="mapId" class="map"></div>
      </div>
      <LRoutingMachine :mapObject="mapObject" :waypoints="waypoints" />

      <!-- Trip details list -->
      <v-list>
        <v-list-item>
            <v-icon>mdi-speedometer</v-icon>
          Average Engine Load: {{ tripDetail.avg_engine_load }}%
        </v-list-item>
        <v-list-item>
            <v-icon>mdi-fuel</v-icon>
          Average MPG: {{ tripDetail.avg_mpg }} Miles per Gallon
        </v-list-item>
        <v-list-item>
            <v-icon>mdi-timer</v-icon>
          Runtime: {{ formatDuration(tripDetail.runtime) }}
        </v-list-item>
        <v-list-item>
            <v-icon>mdi-clock-start</v-icon>
          Start Time: {{ formatDateTime(tripDetail.start_time) }}
        </v-list-item>
        <v-list-item>
            <v-icon>mdi-clock-end</v-icon>
          End Time: {{ formatDateTime(tripDetail.end_time) }}
        </v-list-item>
      </v-list>
    </v-card>
  </div>
</template>

<script>
import LRoutingMachine from '../components/LRoutingMachine.vue'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import axios from 'axios'
import { useCookies } from 'vue3-cookies'

export default {
  setup() {
    const { cookies } = useCookies()
    return { cookies }
  },
  components: {
    LRoutingMachine
  },
  data() {
    return {
      tripDetail: {},
      mapId: 'map',
      mapObject: null,
      zoom: 6,
      center: { lat: 0, lng: 0 },
      osmUrl: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      waypoints: [
        { lat: 0, lng: 0 },
        { lat: 0, lng: 0 }
      ]
    }
  },
  props: ['id'],
  async created() {
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/grabCurrentTrip?trip_id=' + this.id,
      headers: {
        Authorization: 'Bearer ' + this.cookies.get('token')
      }
    }
    axios
      .request(config)
      .then((response) => {
        this.tripDetail = response.data[1][0]
        this.waypoints[0].lat = this.tripDetail['start_lat']
        this.waypoints[0].lng = this.tripDetail['start_lon']
        this.waypoints[1].lat = this.tripDetail['end_lat']
        this.waypoints[1].lng = this.tripDetail['end_lon']
        this.center = this.findMidpoint(
          this.waypoints[0].lat,
          this.waypoints[0].lng,
          this.waypoints[1].lat,
          this.waypoints[1].lng
        )

        this.mapObject = L.map(this.mapId, {
          zoom: this.zoom,
          center: this.center
        })

        L.tileLayer(this.osmUrl, {
          attribution: this.attribution
        }).addTo(this.mapObject)
      })
      .catch((error) => {
        console.log(error)
      })
  },
  mounted() {},
  methods: {
    findMidpoint(lat1, lng1, lat2, lng2) {
      const radLat1 = (lat1 * Math.PI) / 180
      const radLng1 = (lng1 * Math.PI) / 180
      const radLat2 = (lat2 * Math.PI) / 180
      const radLng2 = (lng2 * Math.PI) / 180

      const dLng = radLng2 - radLng1

      const bx = Math.cos(radLat2) * Math.cos(dLng)
      const by = Math.cos(radLat2) * Math.sin(dLng)
      const lat3 = Math.atan2(
        Math.sin(radLat1) + Math.sin(radLat2),
        Math.sqrt((Math.cos(radLat1) + bx) * (Math.cos(radLat1) + bx) + by * by)
      )
      const lng3 = radLng1 + Math.atan2(by, Math.cos(radLat1) + bx)

      const midLat = (lat3 * 180) / Math.PI
      const midLng = (lng3 * 180) / Math.PI

      return { lat: midLat, lng: midLng }
    },
    formatDateTime(dateTimeString) {
      // Check if the dateTimeString is valid
      if (!dateTimeString || new Date(dateTimeString).toString() === 'Invalid Date') {
        return 'Invalid date'
      }

      // Parse the date-time string into a Date object
      const date = new Date(dateTimeString)

      // Check if the date is valid
      if (isNaN(date.getTime())) {
        return 'Invalid date'
      }

      // Use Intl.DateTimeFormat to format the date-time
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: true, // Use 12-hour clock (set to false for 24-hour clock)
        timeZoneName: 'short' // Include the time zone name
      }

      return new Intl.DateTimeFormat('en-US', options).format(date)
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

<style scoped>
.mapCard {
  width: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.map {
  width: 50vw;
  height: 50vh;
}

.mapContainer {
  width: 100%;
  display: flex;
  justify-content: center;
}

.mainDiv {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  margin: 0;
}
</style>
