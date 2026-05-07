import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import Dashboard from '../views/Dashboard.vue'
import Matches from '../views/Matches.vue'
import Profile from '../views/Profile.vue'
import MessageCenter from '../views/MessageCenter.vue'
import SearchView from '../views/SearchView.vue'

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
      //Routing for login page: used in AppHeader.vue
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      //Register page: used in Login.vue
      path: '/register',
      component: RegisterView
    },
    {
      //Dashboard page(main interactive screen after log in)
      path: '/dashboard',
      component: Dashboard
    },
    {
      //Page displaying all matched individuals
      path: '/matches',
      component: Matches
    },
    {
      //To create user profile
      path: '/createprofile',
      component: Profile
    },
    {
      //Messages page
      path: '/message/:matchID/:receiverID',
      name: 'message',
      component: MessageCenter
    },
    {
      //Search specific users by a filter
      path: '/search',
      component: SearchView
    }
  ]
})

export default router