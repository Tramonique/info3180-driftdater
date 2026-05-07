import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import Dashboard from '../views/Dashboard.vue'
import Matches from '../views/Matches.vue'
import Profile from '../views/Profile.vue'
import MessageCenter from '../views/MessageCenter.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      component: RegisterView
    },
    {
      path: '/dashboard',
      component: Dashboard
    },
    {
      path: '/matches',
      component: Matches
    },
    {
      path: '/createprofile',
      component: Profile
    },
    {
      path: '/message/:matchID/:receiverID',
      name: 'message',
      component: MessageCenter
    }
  ]
})

export default router