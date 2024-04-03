<template>
  <div class="mainDiv">
    <v-card class="mapCard">
      <div :id="mapId" class="map"></div>
      <LRoutingMachine :mapObject="mapObject" :waypoints="waypoints" />
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
      center: { lat: 38.7436056, lng: -2.2304153 },
      osmUrl: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      waypoints: [
          { lat: 0, lng: 0 },
          { lat: 0, lng: 0}
        ]
    }
  },
  props: ['id'],
  async created(){
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
        console.log(JSON.stringify(response.data[1][0]))
        this.tripDetail = response.data[1][0]
        this.waypoints[0].lat = this.tripDetail["start_lat"]
        this.waypoints[0].lng = this.tripDetail["start_lon"]
        this.waypoints[1].lat = this.tripDetail["end_lat"]
        this.waypoints[1].lng = this.tripDetail["end_lon"]
        this.center = this.findMidpoint(this.waypoints[0].lat, this.waypoints[0].lng, this.waypoints[1].lat, this.waypoints[1].lng)

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
  mounted() {
  
  },
  methods: {
    findMidpoint(lat1, lng1, lat2, lng2) {
    const radLat1 = lat1 * Math.PI / 180;
    const radLng1 = lng1 * Math.PI / 180;
    const radLat2 = lat2 * Math.PI / 180;
    const radLng2 = lng2 * Math.PI / 180;

    const dLng = radLng2 - radLng1;

    const bx = Math.cos(radLat2) * Math.cos(dLng);
    const by = Math.cos(radLat2) * Math.sin(dLng);
    const lat3 = Math.atan2(
        Math.sin(radLat1) + Math.sin(radLat2),
        Math.sqrt((Math.cos(radLat1) + bx) * (Math.cos(radLat1) + bx) + by * by)
    );
    const lng3 = radLng1 + Math.atan2(by, Math.cos(radLat1) + bx);

    const midLat = lat3 * 180 / Math.PI;
    const midLng = lng3 * 180 / Math.PI;

    return { lat: midLat, lng: midLng };
}
  }
}
// import axios from 'axios'
// import { useCookies } from 'vue3-cookies'
// export default {
//   setup() {
//     const { cookies } = useCookies()
//     return { cookies }
//   },
//   data() {
//     return {
//       tripDetail: {}
//     }
//   },
//   // Assuming the trip's ID is passed as a route parameter
//   props: ['id'],
//   mounted() {
//     console.log(this.id)
//     let config = {
//       method: 'get',
//       maxBodyLength: Infinity,
//       url: 'http://127.0.0.1:5000/grabCurrentTrip?trip_id=13',
//       headers: {
//         Authorization:
//           'Bearer ' + this.cookies.get('token')
//       }
//     }
//     axios
//       .request(config)
//       .then((response) => {
//         console.log(JSON.stringify(response.data[1][0]))
//         this.tripDetail = response.data[1][0]
//       })
//       .catch((error) => {
//         console.log(error)
//       })
//   },
//   methods: {}
// }
</script>

<style>
.mapCard {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 50vw;
  height: 50vh;
  margin-left: 50vh;
}
.map {
  padding: 5%;
  width: 50vw;
  height: 50vh;
}
</style>
