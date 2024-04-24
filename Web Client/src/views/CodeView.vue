<template>
  <v-container>
    <v-data-table :headers="headers" :items="dtcs" class="elevation-1" :items-per-page="10">
      <template v-slot:[`item.Symptoms`]="{ item }">
        <ul>
          <li v-for="(symptom, index) in splitSymptoms(item.Symptoms)" :key="index">
            {{ symptom.trim() }}
          </li>
        </ul>
      </template>
      <template v-slot:[`item.Causes`]="{ item }">
        <ul>
          <li v-for="(cause, index) in splitSymptoms(item.Causes)" :key="index">
            {{ cause.trim() }}
          </li>
        </ul>
      </template>
      <template v-slot:[`item.Date`]="{ item }">
        {{ formatDate(item.Date) }}
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import { useCookies } from 'vue3-cookies'
import axios from 'axios'

export default {
  setup() {
    const { cookies } = useCookies()
    return { cookies }
  },
  name: 'DtcCodes',
  data() {
    return {
      dtcs: [],
      headers: [
        { title: 'Code', key: 'Code', align: 'start' },
        { title: 'Date', key: 'Date', align: 'start' },
        { title: 'Description', key: 'Description', align: 'start' },
        { title: 'Symptoms', key: 'Symptoms', align: 'start' },
        { title: 'Causes', key: 'Causes', align: 'start' }
      ]
    }
  },
  mounted() {
    this.fetchDtcCodes()
  },
  methods: {
    fetchDtcCodes() {
      let config = {
        method: 'get',
        url: 'http://127.0.0.1:5000/getAllDTC',
        headers: {
          Authorization: 'Bearer ' + this.cookies.get('token')
        }
      }
      axios
        .request(config)
        .then((response) => {
          this.dtcs = response.data
        })
        .catch((error) => {
          console.error('Error fetching data:', error)
        })
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      const options = {
        month: '2-digit',
        day: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      }
      return date.toLocaleString('en-US', options)
    },
    splitSymptoms(symptoms) {
      return symptoms.split(/,(?![^()]*\))/)
    }
  }
}
</script>
