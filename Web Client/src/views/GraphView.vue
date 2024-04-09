<template>
  <v-card style="max-width: 90vw; margin-left: 5vw; margin-top: 5vh; padding: 1">
    Options Card
  </v-card>
  <v-card id="chart" style="max-width: 90vw; margin-left: 5vw; margin-top: 5vh">
    <apexchart
      type="line"
      height="350"
      :options="chartOptions"
      :series="series"
      v-if="loaded"
    ></apexchart>
  </v-card>
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
      loaded: false,
      series: [],
      chartOptions: {
        chart: {
          height: 350,
          type: 'line',
          zoom: {
            enabled: false
          },
          animations: {
            enabled: false
          }
        },
        stroke: {
          width: [5, 5, 4],
          curve: 'straight'
        },
        labels: [],
        title: {
          text: 'Your Car Data'
        },
        xaxis: {}
      }
    }
  },
  created() {
    let data = JSON.stringify({
      start_date: '03/15/2024',
      end_date: '04/05/2024'
    })

    let config = {
      method: 'post',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/grabSpecificGraphData',
      headers: {
        'Content-Type': 'application/json',
        Authorization:
          'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MX0.tjVEMiS5O2yNzclwLdaZ-FuzrhyqOT7UwM9Hfc0ZQ8Q'
      },
      data: data
    }

    axios
      .request(config)
      .then((response) => {
        for (let i = 0; i < response.data.length; i++) {
          if (response.data[i]['name'] == 'Dates') {
            for (let j = 0; j < response.data[i]['data'].length; j++) {
              this.chartOptions.labels.push(response.data[i]['data'][j])
            }
          } else {
            this.series.push(response.data[i])
          }
        }
        console.log(JSON.stringify(response.data))
        this.loaded = true
      })
      .catch((error) => {
        console.log(error)
      })
  }
}
</script>
