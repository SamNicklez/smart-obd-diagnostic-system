<template>
  <v-card>
    <v-card-title>{{ this.title }}</v-card-title>
    <v-card-text>
      <v-list dense>
        <v-list-item v-for="item in stats" :key="item.title">
          <v-row no-gutters>
            <v-col cols="auto" class="mr-2">
              <v-icon :color="item.color">{{ item.icon }}</v-icon>
            </v-col>
            <v-col>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-col>
          </v-row>
        </v-list-item>
      </v-list>
    </v-card-text>
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
  name: 'MonthlyStatsCard',
  data() {
    return {
      title: 'Monthly Stats',
      stats: [
        { title: 'Avg Speed: 60 km/h', icon: 'mdi-speedometer', color: 'blue' },
        { title: 'Fuel Eff.: 18 km/l', icon: 'mdi-fuel', color: 'green' },
        { title: 'Brake Wear: 20%', icon: 'mdi-car-brake-alert', color: 'red' },
        { title: 'Oil Level: Good', icon: 'mdi-oil-level', color: 'amber' }
      ]
    }
  },
  created() {
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/grabCurrentData',
      headers: {
        Authorization:
          'Bearer ' + this.cookies.get('token')
      }
    }

    axios
      .request(config)
      .then((response) => {
        console.log(response.data[1][0])
        var date = response.data[1][0]['timestamp'].replace(/(\d{4})-(\d{1,2})-(\d{1,2})/, function(match,y,m,d) 
        {
          return m + '/' + d + '/' + y;
        });
        this.title = "Most Recent Day Stats (" + date + ")"
        let speed_var = "Average Speed: " + response.data[1][0]['avg_speed'] + " mph"
        let fuel_var = "Fuel Efficiency: " + response.data[1][0]['avg_mpg'] + " mpg"
        let oil_var = "Average Oil Temp: " + response.data[1][0]['avg_oil_temp'] + " \u00B0F"
        let runtime = "Total Runtime: " + Math.round(response.data[1][0]['runtime']/60) + " hours"
        let coolant_var = "Average Coolant Temp: " + response.data[1][0]['avg_coolant_temp'] + " \u00B0F"
        this.stats = [
        { title: speed_var, icon: 'mdi-speedometer', color: 'blue' },
        { title: fuel_var, icon: 'mdi-fuel', color: 'green' },
        { title: runtime, icon: 'mdi-car-brake-alert', color: 'red' },
        { title: oil_var, icon: 'mdi-oil-level', color: 'amber' },
        { title: coolant_var, icon: 'mdi-car-coolant-level', color: 'purple' }
                    ]
      })
      .catch((error) => {
        console.log(error)
      })
  }
}
</script>

<style scoped></style>
