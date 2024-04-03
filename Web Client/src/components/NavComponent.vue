
<template>
  <v-container>
    <v-app-bar scroll-behavior="hide">
      <v-toolbar-title>
        <v-btn text to="/" variant="plain" class="button">OBD Viewer</v-btn>
      </v-toolbar-title>
      <v-btn @click="openLogin">Login</v-btn>
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
     * Perform a search
     */
    performSearch() {
      this.$router.push(`/search/${this.searchQuery}`)
    },
    /**
     * Open the login page
     */
    openLogin() {
      this.$router.push('/login')
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
          Authorization:
            'Bearer ' + this.cookies.get('token'),
        },
        data: data
      }
      axios
        .request(config)
        .then((response) => {
          if(response.data[1] == []){
            this.notifications = []
          } else {
            this.notifications = response.data[1]
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
      this.notifications.splice(index, 1)
      //Somewhere in here, ping server to mark notification as read
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
