<script>
export default {
  methods: {
    /**
     * Routes to the home page
     */
    goHome() {
      this.$router.push('/')
    }
  }
}
</script>

<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12" outlined>
          <v-card-text>
            <div class="d-flex justify-center">
              <v-img
                contain
                max-width="200"
                src="https://cdn-icons-png.flaticon.com/512/2748/2748558.png"
                alt="404 Error"
              ></v-img>
            </div>
            <h1 class="text-center">Ope! Page not found.</h1>
            <p class="text-center">The page you are looking for doesn't exist or has been moved.</p>
            <v-btn color="#F06543" class="mx-auto d-block" @click="goHome">Go Back Home</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.fill-height {
  max-height: 30em;
  width: 120em;
  display: flex;
  justify-content: center;
  align-items: center;
}

.text-center {
  margin-top: 2.5vh;
  margin-bottom: 1vh;
}
</style>
