<template>
  <div class="logout-card">
    <v-card
      class="mx-auto pa-12 pb-8"
      elevation="8"
      rounded="lg"
      style="max-width: 35em; margin-bottom: 10vh"
    >
      <div class="text-h5 text-center mb-8">Logout</div>
      <v-alert type="info" class="mb-8" dense> Are you sure you want to log out? </v-alert>
      <v-btn block color="#F06543" size="large" @click="logout"> Log Out </v-btn>
      <v-card-text class="text-center mt-8">
        <a class="text-decoration-none" style="color: #313638; cursor: pointer" @click="goToHome">
          Return to Home <v-icon icon="mdi-home"></v-icon>
        </a>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { useCookies } from 'vue3-cookies'
export default {
  setup() {
    const { cookies } = useCookies()
    return { cookies }
  },
  methods: {
    logout() {
      this.cookies.set('token', '')
      this.$router.push({ name: 'login' })
    },
    goToHome() {
      this.$router.push({ name: 'home' })
    }
  }
}
</script>

<style scoped>
.logout-card {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50vh;
}
</style>
