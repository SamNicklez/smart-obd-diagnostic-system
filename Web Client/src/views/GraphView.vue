<template>
  <div
    style="
      display: flex;
      align-items: center;
      justify-content: space-around;
      max-width: 30vw;
      margin-left: auto;
      margin-right: auto;
    "
  >
    <VueDatePicker :format="format" v-model="startDate" style="flex: 1"></VueDatePicker>
    -
    <VueDatePicker :format="format" v-model="endDate" style="flex: 1"></VueDatePicker>
    <v-btn style="flex: 1; margin-left: 1vw" @click="updateData">Update Graph</v-btn>
  </div>
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
      startDate: null,
      endDate: null,
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
    let todaysDate = new Date().toLocaleDateString('en-US', {
      month: '2-digit',
      day: '2-digit',
      year: 'numeric'
    })
    let oneWeekAgo = new Date(new Date().getTime() - 7 * 24 * 60 * 60 * 1000).toLocaleDateString(
      'en-US',
      {
        month: '2-digit',
        day: '2-digit',
        year: 'numeric'
      }
    )
    this.startDate = oneWeekAgo
    this.endDate = todaysDate
    let data = JSON.stringify({
      start_date: oneWeekAgo,
      end_date: todaysDate
    })

    let config = {
      method: 'post',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/grabSpecificGraphData',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.cookies.get('token')
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
  },
  methods: {
    format(date) {
      const day = date.getDate()
      const month = date.getMonth() + 1
      const year = date.getFullYear()

      return `${month}/${day}/${year}`
    },
    updateData() {
      this.loaded = false
      this.series = []
      this.chartOptions.labels = []
      let startDate = ''
      let endDate = ''
      if (this.startDate == null || this.endDate == null) {
        return
      }
      if (this.startDate > this.endDate) {
        return
      }
      if (typeof this.startDate == 'string') {
        startDate = this.startDate
      } else {
        startDate = this.startDate.toLocaleDateString('en-US', {
          month: '2-digit',
          day: '2-digit',
          year: 'numeric'
        })
      }
      if (typeof this.endDate == 'string') {
        endDate = this.endDate
      } else {
        endDate = this.endDate.toLocaleDateString('en-US', {
          month: '2-digit',
          day: '2-digit',
          year: 'numeric'
        })
      }
      let data = JSON.stringify({
        start_date: startDate,
        end_date: endDate
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
}
</script>
