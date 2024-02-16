<template>
    <v-card>
      <v-card-title>Monthly Stats</v-card-title>
      <v-card-text>
        <v-list dense>
          <v-list-item v-for="item in stats" :key="item.title">
            <v-row align="center" no-gutters>
              <v-col cols="auto" class="mr-2">
                <v-icon :color="item.color">{{ item.icon }}</v-icon>
              </v-col>
              <v-col>
                <v-list-item-content>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
              </v-col>
            </v-row>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </template>
  
  <script>
  export default {
    name: 'MonthlyStatsCard',
    data() {
      return {
        stats: [
          { title: 'Avg Speed: 60 km/h', icon: 'mdi-speedometer', color: 'blue' },
          { title: 'Fuel Eff.: 18 km/l', icon: 'mdi-fuel', color: 'green' },
          { title: 'Brake Wear: 20%', icon: 'mdi-car-brake-alert', color: 'red' },
          { title: 'Oil Level: Good', icon: 'mdi-oil-level', color: 'amber' },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  </style>
  