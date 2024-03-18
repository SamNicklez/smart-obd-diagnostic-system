import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import axios from 'axios'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: (to, from, next) => {
        const token = getCookie('token')
        if (token != null && token != 'null') {
          next('logout')
        }
        else{
          next()
        }
      }
    },
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    }
  ]
})

function getCookie(name) {
  let cookieArray = document.cookie.split(';')
  for (let i = 0; i < cookieArray.length; i++) {
    let cookiePair = cookieArray[i].split('=')
    let cookieName = cookiePair[0].trim()
    if (cookieName === name) {
      return decodeURIComponent(cookiePair[1])
    }
  }
  return null
}

router.beforeEach((to, from, next) => {
  const token = getCookie('token')
  if (token != null && token != 'null') {
    console.log('token exists')
    let config = {
      method: 'get',
      maxBodyLength: Infinity,
      url: 'http://127.0.0.1:5000/verify',
      headers: {
        Authorization: 'Bearer ' + token
      }
    }
    axios
      .request(config)
      .then(() => {
        next()
      })
      .catch(() => {
        next('/login')
      })
  }
  if(to.name === 'login') {
    next()
  }
})

export default router
