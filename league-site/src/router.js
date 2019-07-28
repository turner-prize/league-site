import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import AnnouncementsView from './views/AnnouncementsView.vue'
import TableView from './views/TableView.vue'
import StatsView from './views/StatsView.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/announcementsView',
      name: 'announcementsView',
      component: AnnouncementsView
    },
    {
      path: '/tableView',
      name: 'tableView',
      component: TableView
    },
    {
      path: '/statsView',
      name: 'statsView',
      component: StatsView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    }
  ]
})