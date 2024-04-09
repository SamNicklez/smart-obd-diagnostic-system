<template>
  <VCalendar
    v-if="finished"
    borderless
    expanded
    title-position="left"
    :attributes="attrs"
    style="min-height: 40vh"
    :initial-page="{ month: new Date().getMonth() + 1, year: new Date().getFullYear() }"
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
        let sortedData = response.data.slice().sort((a, b) => a.avg_mpg - b.avg_mpg)

        let top20PercentIndex = Math.floor(sortedData.length * 0.8)
        let bottom20PercentIndex = Math.floor(sortedData.length * 0.2)

        let good = sortedData.slice(top20PercentIndex)
        let average = sortedData.slice(bottom20PercentIndex, top20PercentIndex)
        let bad = sortedData.slice(0, bottom20PercentIndex)


        for(let i = 0; i < good.length; i++) {
          let date = new Date(good[i].timestamp)
          attrs_new.push({
            highlight: 'green',
            dates: date,
            popover: {
              label: 'Avg MPG: ' + good[i].avg_mpg,
              visibility: 'focus'
            }
          })
        }
        for(let i = 0; i < average.length; i++) {
          let date = new Date(average[i].timestamp)
          attrs_new.push({
            highlight: 'yellow',
            dates: date,
            popover: {
              label: 'Avg MPG: ' + average[i].avg_mpg,
              visibility: 'focus'
            }
          })
        }
        for(let i = 0; i < bad.length; i++) {
          let date = new Date(bad[i].timestamp)
          attrs_new.push({
            highlight: 'red',
            dates: date,
            popover: {
              label: 'Avg MPG: ' + bad[i].avg_mpg,
              visibility: 'focus'
            }
          })
        }

        // for (let i = 0; i < response.data.length; i++) {
        //   let date = new Date(response.data[i].timestamp)
        //   console.log(response.data[i])
        //   attrs_new.push({
        //     highlight: 'red',
        //     dates: date,
        //     popover: {
        //       label: 'HDJKFHSDKJ]\r\nFhdskjfhdkjs',
        //       visibility: 'focus'
        //     }
        //   })
        //   attrs_new.push({
        //     highlight: 'red',
        //     dates: date,
        //     popover: {
        //       label: 'HDJKFHSDKJ]\r\nFhdskjfhdkjs',
        //       visibility: 'focus'
        //     }
        //   })
        // }
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
