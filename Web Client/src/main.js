import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import VueApexCharts from 'vue3-apexcharts'
import VCalendar from 'v-calendar'
import 'v-calendar/style.css'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

const vuetify = createVuetify({
  components,
  directives
})

const app = createApp(App)
app.component('VueDatePicker', VueDatePicker)
app.use(VueApexCharts)
app.use(createPinia())
app.use(VCalendar, {})
app.use(router)
app.use(vuetify)
app.mount('#app')
