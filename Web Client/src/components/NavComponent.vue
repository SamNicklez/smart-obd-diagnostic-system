<template>
  <v-container>
    <v-app-bar scroll-behavior="hide">
      <v-toolbar-title>
        <v-btn text to="/" variant="plain" class="button">OBD Viewer</v-btn>
      </v-toolbar-title>
      <v-btn @click="openLogin">Login</v-btn>
      <v-btn @click="openGraphs">Graphs</v-btn>
      <v-btn @click="openCodes">DTC</v-btn>
      <v-menu transition="scale-transition" :close-on-content-click="false">
        <template v-slot:activator="{ props }">
          <v-btn icon @click="populateNotifications" v-bind="props">
            <v-icon size="large">mdi-bell</v-icon>
          </v-btn>
        </template>
        <v-list lines="three" style="min-width: 25vw" v-if="this.notifications.length != 0">
          <v-list-item
            v-for="(item, i) in notifications"
            :key="i"
            append-icon="mdi-close"
            @click="closeNoti(i)"
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
            <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
        <v-list lines="three" style="min-width: 25vw" v-else>
          <v-list-item>
            <v-list-item-title>No New Notifications</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  </v-container>
</template>

<script>
import '@mdi/font/css/materialdesignicons.css'
import axios from 'axios'
import { useCookies } from 'vue3-cookies'
export default {
  setup() {
    const { cookies } = useCookies()
    return { cookies }
  },
  data() {
    return {
      searchQuery: '',
      notifications: [
        { title: 'Notification 1', description: 'This is a notification' },
        { title: 'Notification 2', description: 'This is a notification' },
        { title: 'Notification 3', description: 'This is a notification' },
        { title: 'Notification 4', description: 'This is a notification' }
      ]
    }
  },
  created() {
    this.populateNotifications()
  },
  methods: {
    /**
     * Open the login page
     */
    openLogin() {
      this.$router.push('/login')
    },
    openGraphs() {
      this.$router.push('/graphs')
    },
    openCodes() {
      this.$router.push('/dtc')
    },
    /**
     * Populates the notifications
     */
    populateNotifications() {
      let data = ''

      let config = {
        method: 'get',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/grabNotifications',
        headers: {
          Authorization: 'Bearer ' + this.cookies.get('token')
        },
        data: data
      }
      axios
        .request(config)
        .then((response) => {
          if (response.data[1] == []) {
            this.notifications = []
          } else {
            console.log(response.data[1])
            this.notifications = []
            for (let i = 0; i < response.data[1].length; i++) {
              this.notifications.push({
                title: response.data[1][i].code,
                description: 'Engine Code Detected'
              })
            }
          }
        })
        .catch(() => {
          this.notifications = []
        })
    },
    /**
     * Closes a notification
     * @param {int} index
     */
    closeNoti(index) {
      let data = JSON.stringify({
        code: this.notifications[index].title
      })

      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/dismissNotification',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + this.cookies.get('token')
        },
        data: data
      }

      axios
        .request(config)
        .then(() => {
          this.notifications.splice(index, 1)
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
.nav-textfield {
  width: 35em;
  margin: 0 auto;
  color: black;
}

.button {
  color: black;
  font-size: 0.75em;
  margin-left: 0.5vw;
}

.button:hover {
  color: black;
}
</style>
