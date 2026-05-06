import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import Dashboard from '../views/Dashboard.vue'
import Matches from '../views/Matches.vue'
import Profile from '../views/Profile.vue'

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
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      //Routing for login page: used in AppHeader.vue
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      //Routing for register page: used in Login.vue
      path: '/register',
      component: RegisterView
    },
    {
      //Routing for dashboard page(main interactive screen after log in)
      path: '/dashboard',
      component: Dashboard
    },
    {
      //Routhing for page displaying all matched individuals
      path: '/matches',
      component: Matches
    },
    {
      //Routing to create user profile
      path: '/createprofile',
      component: Profile
    }
  ]
})

export default router
