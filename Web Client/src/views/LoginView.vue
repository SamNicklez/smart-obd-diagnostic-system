<template>
  <div class="login-card">
    <v-card
      class="mx-auto pa-12 pb-8"
      id="card"
      elevation="8"
      rounded="lg"
      style="margin-bottom: 10vh"
    >
      <div class="text-h5 text-center mb-8">Login</div>
      <div class="text-subtitle-1 text-medium-emphasis">Username</div>
      <v-text-field
        density="compact"
        v-model="username"
        maxLength="100"
        placeholder="Username"
        prepend-inner-icon="mdi-account-circle"
        variant="outlined"
      ></v-text-field>
      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        v-model="password"
        placeholder="Enter your password"
        maxLength="15"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        @click:append-inner="visible = !visible"
      ></v-text-field>
      <v-btn
        block
        class="mb-8"
        color="#F06543"
        size="large"
        variant="tonal"
        id="loginButton"
        @click="login"
      >
        Log In
      </v-btn>
    </v-card>
  </div>
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
  data: () => ({
    username: '',
    password: '',
    visible: false
  }),
  methods: {
    /**
     * Logs the user in
     */
    login() {
      let data = JSON.stringify({
        username: this.username,
        password: this.password
      })

      let config = {
        method: 'post',
        maxBodyLength: Infinity,
        url: 'http://127.0.0.1:5000/login',
        headers: {
          'Content-Type': 'application/json'
        },
        data: data
      }
      axios
        .request(config)
        .then((response) => {
          this.cookies.set('token', response.data.token)
          this.$router.push({ name: 'home' })
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
#card {
  width: 35em;
}
</style>
