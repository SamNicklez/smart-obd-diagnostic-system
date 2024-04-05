<template>
  <VCalendar
    v-if="finished"
    borderless
    expanded
    title-position="left"
    :attributes="attrs"
    style="min-height: 40vh"
  />
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
      attrs: [],
      finished: false
    }
  },
  created() {
    let startOfLastMonth = new Date(
      new Date().getFullYear(),
      new Date().getMonth() - 1,
      1
    ).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' })
    let endOfCurrentMonth = new Date(
      new Date().getFullYear(),
      new Date().getMonth() + 1,
      0
    ).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: 'numeric' })
    console.log(startOfLastMonth)
    console.log(endOfCurrentMonth)
    let data = JSON.stringify({
      start_date: startOfLastMonth,
      end_date: endOfCurrentMonth
    })

    let config = {
      method: 'POST',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/grabGraphData',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + this.cookies.get('token')
      },
      data: data
    }

    axios
      .request(config)
      .then((response) => {
        let attrs_new = []
        for (let i = 0; i < response.data.length; i++) {
          let date = new Date(response.data[i].timestamp)
          console.log(date)
          attrs_new.push({
            content: 'red', 
            highlight: true,
            dates: date,
          })
        }
        this.attrs = attrs_new
        this.finished = true
      })
      .catch((error) => {
        console.log(error)
      })
  },
  methods: {}
}
</script>
