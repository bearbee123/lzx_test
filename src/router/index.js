import Vue from 'vue'
import Router from 'vue-router'
import Main from '../components/main.vue'


Vue.use(Router)

const routes = [
    {
        path:"/",
        redirect:"/:user_name"
    },
  {
    path: '/:user_name',
    name: 'Main',
    component: Main
  },

]

const router = new Router({
  mode:"history",
  routes
})

export default router