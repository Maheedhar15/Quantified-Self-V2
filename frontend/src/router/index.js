import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView'
import RegisterView from '../views/RegisterView'
import TrackersView from '@/views/TrackersView';
import CreateTracker from '@/views/CreateTracker'
import DeleteTracker from '@/views/DeleteTracker'
import UpdateTracker from '@/views/UpdateTracker'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  },
  {
    path: '/dashboard/:id',
    name: 'Dashboard',
    component: HomeView
  },
  {
    path: '/trackers/:id',
    name:'Trackers',
    component: TrackersView
  },
  {
    path: '/about',
    name: 'about,'
  },
  {
    path: '/logout/:id',
    name: 'logout'
  },
  {
    path: '/createtracker/:id',
    name: 'createtracker',
    component: CreateTracker
  },
  {
    path: '/trackers/:id/Delete',
    name: 'tdelete',
    component: DeleteTracker
  },
  {
    path: '/trackers/:id/Update',
    name: 'tupdate',
    component: UpdateTracker
  },

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
